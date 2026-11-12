"""Execute published plugin layouts after moving them outside the repository."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from optics_photonics.packages import package, managed_server


class MarketplaceTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('uv'), 'Marketplace launchers use uv; fixed-interpreter packages do not')
    def test_native_marketplaces_and_research_os_launch_after_relocation(self):
        requests = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {
                'protocolVersion': '2025-11-25', 'capabilities': {},
                'clientInfo': {'name': 'marketplace-install', 'version': '1'}}},
            {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {
                'name': 'software_search', 'arguments': {'query': 'tmm'}}},
        ]
        with tempfile.TemporaryDirectory(prefix='Optics installed package ') as temporary:
            root = Path(temporary)
            native = root / 'native plugin'
            native.mkdir()
            for directory in ('src', 'data', 'skills', '.codex-plugin', '.claude-plugin', '.agents'):
                shutil.copytree(ROOT / directory, native / directory,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            for filename in ('server.py', '.mcp.json', 'mcp.codex.json'):
                shutil.copy2(ROOT / filename, native / filename)
            research = root / 'Research OS plugin'
            shutil.copytree(ROOT / 'connect/agentic-research-os', research)
            for folder in ('.agents/plugins', '.claude-plugin'):
                market = json.loads((native / folder / 'marketplace.json').read_text())
                self.assertEqual(market['plugins'][0]['name'], 'optics-photonics')
            specs = [
                (native, json.loads((native / 'mcp.codex.json').read_text())['mcpServers']['optics']),
                (native, json.loads((native / '.mcp.json').read_text())['mcpServers']['optics']),
                (research, json.loads((research / 'plugin.json').read_text())['mcpServers']['optics']),
            ]
            for package, spec in specs:
                with self.subTest(command=spec):
                    # Native Codex does not expand PLUGIN_ROOT; its cwd is plugin-relative.
                    args = [arg.replace('${CLAUDE_PLUGIN_ROOT}', str(package))
                            .replace('${PACKAGE_ROOT}', str(package)) for arg in spec['args']]
                    command = sys.executable if spec['command'] == '${RESEARCH_PYTHON}' else spec['command']
                    env = {key: value for key, value in os.environ.items() if key != 'PYTHONPATH'}
                    env['OPTICS_HOME'] = str(root / 'state')
                    cwd = package / spec['cwd'] if 'cwd' in spec else root
                    process = subprocess.run([command, *args], cwd=cwd, env=env,
                        input='\n'.join(map(json.dumps, requests))+'\n', capture_output=True,
                        text=True, timeout=30, check=True)
                    replies = sorted((json.loads(line) for line in process.stdout.splitlines()), key=lambda r:r['id'])
                    self.assertEqual([reply['id'] for reply in replies], [1, 2, 3])
                    self.assertGreaterEqual(len(replies[1]['result']['tools']), 17)
                    result = replies[2]['result']['structuredContent']
                    self.assertEqual(result['items'][0]['id'], 'tmm')

    def test_native_manifests_use_their_host_path_rules(self):
        for filename, host in [('mcp.codex.json','codex'),('.mcp.json','claude')]:
            self.assertEqual(json.loads((ROOT/filename).read_text())['mcpServers']['optics'], managed_server(host))

    def test_generated_native_plugins_move_without_regeneration(self):
        with tempfile.TemporaryDirectory(prefix='Optics relocation ') as temporary:
            root = Path(temporary)
            for host in ('codex','claude'):
                original, moved = root/host, root/(host+' installed')
                package(original, host)
                original.rename(moved)
                spec = json.loads((moved/'.mcp.json').read_text())['mcpServers']['optics']
                arguments = [x.replace('${CLAUDE_PLUGIN_ROOT}',str(moved)) for x in spec['args']]
                # Start from another workspace, just as a real host does.
                cwd = moved/spec['cwd'] if 'cwd' in spec else root
                arguments[-1:] = ['search','mie scattering sphere']
                result = subprocess.run([spec['command'],*arguments],cwd=cwd,capture_output=True,text=True,check=True)
                self.assertEqual(json.loads(result.stdout)['items'][0]['id'],'miepython')

    @unittest.skipUnless(shutil.which('uv'), 'Portable launcher uses uv')
    def test_managed_packages_move_and_keep_existing_research(self):
        with tempfile.TemporaryDirectory(prefix='Optics managed ') as temporary:
            root = Path(temporary)
            home = root/'research'
            home.mkdir(); (home/'notes.txt').write_text('Retain this research')
            for host in ('codex','claude','portable'):
                original, moved = root/host, root/(host+' updated')
                package(original, host, managed=True)
                original.rename(moved)
                manifest = '.mcp.json' if host in ('codex','claude') else 'mcp.json'
                spec = json.loads((moved/manifest).read_text())['mcpServers']['optics']
                self.assertEqual(spec['command'], 'uv')
                self.assertNotIn(str(original), json.dumps(spec))
                args = [x.replace('${PLUGIN_ROOT}',str(moved)).replace('${CLAUDE_PLUGIN_ROOT}',str(moved)) for x in spec['args']]
                args[-1:] = ['search','xray beamline']
                cwd = moved/spec['cwd'] if 'cwd' in spec else root
                env = {**os.environ,'OPTICS_HOME':str(home),'UV_PYTHON_DOWNLOADS':'never'}
                result = subprocess.run([spec['command'],*args],cwd=cwd,env=env,capture_output=True,text=True,timeout=30,check=True)
                self.assertIn('xrt', [row['id'] for row in json.loads(result.stdout)['items']])
            self.assertEqual((home/'notes.txt').read_text(),'Retain this research')


if __name__ == '__main__':
    unittest.main()
