"""Run an extracted release (or installed wheel) without importing the checkout.

Requires the MCP client in this script's environment and NumPy/TMM in the
solver environment. --previous-run checks that an update retained an old run;
omit --solver-python on that invocation to reuse the saved environment.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def result(response):
    assert not getattr(response, 'is_error', getattr(response, 'isError', False)), response
    return json.loads(response.content[0].text)


def parameters(options):
    env = {key: value for key, value in os.environ.items() if key != 'PYTHONPATH'}
    env.update(OPTICS_HOME=str(options.home), MPLBACKEND='Agg')
    if not options.package:
        return StdioServerParameters(command=options.python, args=['-m', 'optics_photonics', 'mcp'], env=env, cwd=options.home.parent)
    root = options.package
    for manifest in ('.mcp.json', 'mcp.json', 'plugin.json'):
        file = root / manifest
        if file.exists():
            servers = json.loads(file.read_text(encoding='utf-8')).get('mcpServers', {})
            if 'optics' in servers:
                server = servers['optics']
                break
    else:
        server = {'command': options.python, 'args': [str(root / 'server.py'), 'mcp']}
    # These substitutions belong to the respective host formats. Codex uses cwd,
    # not PLUGIN_ROOT; it must not be made to pass by expanding an unknown variable.
    if (root / '.codex-plugin').exists():
        replacements = {}
    elif (root / '.claude-plugin').exists():
        replacements = {'${CLAUDE_PLUGIN_ROOT}': str(root)}
    elif server['command'] == '${RESEARCH_PYTHON}':
        replacements = {'${PACKAGE_ROOT}': str(root), '${RESEARCH_PYTHON}': options.python}
    else:
        replacements = {'${PLUGIN_ROOT}': str(root)}
    def expand(value):
        for name, replacement in replacements.items():
            value = value.replace(name, replacement)
        assert '${' not in value, value
        return value
    return StdioServerParameters(command=expand(server['command']),
                                 args=[expand(value) for value in server['args']],
                                 cwd=root / server.get('cwd', '.'), env=env)


async def exercise(options):
    params = parameters(options)
    source = '''import sys,time,tmm,numpy as np
time.sleep(0.5)
r=tmm.coh_tmm('s',[1,1.5],[np.inf,np.inf],0,550)
np.savetxt(OUTPUT_DIR/'spectrum.csv',[[550,r['R']]],delimiter=',')
RESULT={'R':float(r['R']),'python':sys.version.split()[0]}
'''
    if not options.legacy:
        source += '''from optics_photonics import data
data.save(OUTPUT_DIR/'spectrum',{
 'R':data.quantity([r['R'],r['R']],'reflectance',unit='1',axes=['wavelength']),
 'wavelength':data.quantity([500,550],'vacuum wavelength',unit='nm')})
'''
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            info = getattr(initialized, 'server_info', getattr(initialized, 'serverInfo', None))
            assert info.version == options.version, initialized
            names = {tool.name for tool in (await session.list_tools()).tools}
            assert len(names) == 22, names
            if options.previous_run:
                old = result(await session.call_tool('run_status', {'run_id': options.previous_run, 'include_results': True}))
                assert old['state'] == 'succeeded', old
                assert abs(old['steps'][0]['result']['result']['R'] - .04) < 1e-12
            if options.solver_python:
                result(await session.call_tool('bind_environment', {'tool': 'tmm', 'python': options.solver_python}))
            if not options.legacy:
                guide = await session.call_tool('read_guide', {'topic': 'data'})
                assert not getattr(guide, 'is_error', getattr(guide, 'isError', False)), guide
                assert 'data.save' in guide.content[0].text
            run = result(await session.call_tool('submit_calculation', {'tool': 'tmm', 'source': source}))['run_id']
    # A new server process attaches to the calculation submitted before disconnection.
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            until = time.monotonic() + 60
            while True:
                state = result(await session.call_tool('run_status', {'run_id': run, 'wait': 5, 'include_results': True}))
                if state['state'] not in ('queued', 'running') or time.monotonic() > until:
                    break
            assert state['state'] == 'succeeded', state
            computed = state['steps'][0]['result']['result']
            assert abs(computed['R'] - .04) < 1e-12, computed
            files = result(await session.call_tool('result_files', {'run_id': run}))['files']
            csv = next(entry['file'] for entry in files if entry['file'].endswith('spectrum.csv'))
            text = result(await session.call_tool('read_result', {'run_id': run, 'file': csv}))['data']
            destination = options.home / ('download-' + run + '.csv')
            result(await session.call_tool('download_result', {'run_id': run, 'file': csv, 'destination': str(destination)}))
            assert destination.read_bytes() == text.encode('utf-8')
            if not options.legacy:
                array = next(entry['file'] for entry in files if entry['file'].endswith('spectrum.npz'))
                selected = result(await session.call_tool('read_array', {'run_id': run, 'file': array, 'member': 'R', 'index': [[None, None, -1]]}))
                assert selected['description']['unit'] == '1', selected
                assert selected['axes'] == [{'name': 'wavelength', 'unit': 'nm', 'values': [550, 500]}], selected
                assert all(abs(value - .04) < 1e-12 for value in selected['values']), selected
    print(json.dumps({'version': options.version, 'package': str(options.package) if options.package else 'installed wheel',
                      'tools': len(names), 'run_id': run, 'result': computed, 'reconnect': 'passed',
                      'described_arrays': not options.legacy, 'previous_run': options.previous_run}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path, help='Extracted directory containing server.py; omit for an installed wheel')
    parser.add_argument('--python', default=sys.executable, help='Connector interpreter for Research OS, Connect or the installed wheel')
    parser.add_argument('--solver-python', help='Bind TMM to this existing interpreter; omit to reuse a saved binding')
    parser.add_argument('--home', type=Path, required=True, help='Dedicated research directory for this installation check')
    parser.add_argument('--version', required=True)
    parser.add_argument('--previous-run', help='A successful run made by an older release in the same home')
    parser.add_argument('--legacy', action='store_true', help='Check a pre-0.7.0 release without described arrays')
    options = parser.parse_args()
    options.home = options.home.absolute()
    options.home.mkdir(parents=True, exist_ok=True)
    if options.package:
        options.package = options.package.absolute()
    options.python = os.path.abspath(options.python)
    if options.solver_python:
        options.solver_python = os.path.abspath(options.solver_python)
    asyncio.run(exercise(options))
