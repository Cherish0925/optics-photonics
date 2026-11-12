"""Generate relocatable plugin bundles and host-native connection configurations."""
import json
import os
from pathlib import Path
import shutil
import shlex
import sys
from . import __version__
from .catalogue import resources

HOSTS = ('agentic-research-os','codex','claude','deepseek','qiushi','mcp','portable')


def shell_command(arguments):
    if os.name == 'nt':
        return '& ' + ' '.join("'" + str(value).replace("'", "''") + "'" for value in arguments)
    return shlex.join(str(value) for value in arguments)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def managed_server(host):
    """A movable entry point using the host's actual plugin path rules."""
    script = {'codex':'server.py', 'claude':'${CLAUDE_PLUGIN_ROOT}/server.py',
              'portable':'${PLUGIN_ROOT}/server.py'}[host]
    server = {'command':'uv', 'args':['run','--no-project','--python','>=3.10','--',script,'mcp']}
    if host == 'codex': server['cwd'] = '.'
    if host == 'portable': server.update(type='stdio', cwd='./')
    return server


def package(destination, host='mcp', python=None, *, managed=False):
    if host not in HOSTS: raise ValueError('Unknown host: '+host)
    if managed and (python or host not in ('codex','claude','portable')):
        raise ValueError('Managed Python applies to Codex, Claude or portable packages without a selected Python')
    if host == 'portable' and python:
        raise ValueError('Portable packages select Python on the destination machine; use a native host or mcp for a fixed interpreter')
    target = Path(destination).expanduser().resolve()
    if target.exists() and any(target.iterdir()):
        raise ValueError('Choose a new package directory; existing host configuration is kept')
    target.mkdir(parents=True, exist_ok=True)
    code = target/'lib'/'optics_photonics'
    shutil.copytree(Path(__file__).parent, code, ignore=shutil.ignore_patterns('__pycache__','resources','*.pyc'))
    for directory in ('data','skills'):
        shutil.copytree(resources()/directory, code/'resources'/directory)
    shutil.copytree(resources()/'skills', target/'skills')
    shutil.copy2(resources()/'LICENSE', target/'LICENSE')
    shutil.copy2(resources()/'LICENSE', code/'resources'/'LICENSE')
    (target/'server.py').write_text('from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parent/"lib"))\nfrom optics_photonics.cli import main\nmain()\n', encoding='utf-8')
    interpreter = os.path.abspath(os.path.expanduser(str(python or sys.executable)))
    server = {'command':interpreter, 'args':['-B',str(target/'server.py'),'mcp']}
    skills = ['skills/'+p.name for p in sorted((target/'skills').iterdir()) if (p/'SKILL.md').exists()]
    descriptor = {'name':'optics-photonics', 'version':__version__,
                  'description':'Optical research environment: solvers, native programs and episode sampling', 'skills':skills}
    if host == 'portable':
        write(target/'plugin.json', {'$schema':'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
            **{k:v for k,v in descriptor.items() if k != 'skills'}, 'license':'MIT'})
        write(target/'mcp.json', {'$schema':'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
            'mcpServers':{'optics':managed_server('portable')}})
        instructions = 'Install this directory in a host supporting Agent Plugins 1.0.0. Skills and mcp.json are discovered at the package root. Install uv (https://docs.astral.sh/uv/getting-started/installation/) on the execution host; it selects Python 3.10+ and downloads an interpreter only if needed. The package can be moved between machines. For an offline host with a selected Python, generate a native host or MCP package instead.'
    elif host == 'agentic-research-os':
        descriptor['mcpServers'] = {'optics':{'transport':'stdio','command':'${RESEARCH_PYTHON}',
            'args':['-B','${PACKAGE_ROOT}/server.py','mcp'], 'protocol_version':'2025-11-25'}}
        write(target/'plugin.json',descriptor)
        instructions = 'Extract the release ZIP if needed, then install the directory containing plugin.json as an Agentic Research OS plugin. Activate its returned revision in the current workspace. The package uses the host Python and carries all connector code, catalogue data and Skills. Configure scientific software on the computing host.'
    elif host in ('codex','claude'):
        folder = '.codex-plugin' if host == 'codex' else '.claude-plugin'
        # Codex resolves cwd relative to the plugin; Claude expands CLAUDE_PLUGIN_ROOT.
        native = {**{k:v for k,v in descriptor.items() if k!='skills'}, 'author':{'name':'Optics & Photonics'}}
        if host == 'codex':
            native.update(skills='./skills/', mcpServers='./.mcp.json', requires_local_executor=True,
                          interface={'displayName':'Optics & Photonics','shortDescription':'Optical software and research calculations','developerName':'Optics & Photonics'})
        write(target/folder/'plugin.json', native)
        native_server = {'command':interpreter, 'args':['-B','server.py','mcp'], 'cwd':'.'} if host == 'codex' else \
                        {'command':interpreter, 'args':['-B','${CLAUDE_PLUGIN_ROOT}/server.py','mcp']}
        if managed: native_server = managed_server(host)
        write(target/'.mcp.json', {'mcpServers':{'optics':native_server}})
        if not managed: write(target/'mcp.json', {'mcpServers':{'optics':server}})
        instructions = ('Register this local plugin directory in '+host+'. The native plugin resolves its own directory and uses the selected Python. Moving it on this machine preserves that connection; generate a package again when selecting a different Python or computer. The standalone mcp.json and registration command below use this installation path.')
        if managed:
            instructions = 'Install uv (https://docs.astral.sh/uv/getting-started/installation/) on the execution host, then load this directory as a '+host+' plugin. It selects Python 3.10+ and downloads an interpreter only if needed. Move or update this package without changing its MCP paths. Environments and runs remain under OPTICS_HOME or ~/.optics-photonics.'
        elif host == 'codex':
            command = ['codex','mcp','add','optics','--',interpreter,'-B',str(target/'server.py'),'mcp']
        else:
            command = ['claude','mcp','add','--transport','stdio','optics','--',interpreter,'-B',str(target/'server.py'),'mcp']
        if not managed:
            instructions += '\n\n```'+('powershell' if os.name == 'nt' else 'sh')+'\n'+shell_command(command)+'\n```\n'
    elif host == 'deepseek':
        overlay = [{'insert':[{'id':'optics-photonics','name':'@deepseek-ai/dsh-mcp-client',
                    'config':{'serverName':'optics','transport':'stdio',**server,'env':{},'cwd':str(target)}}]}]
        # JSON is valid YAML and preserves Windows paths without manual escaping.
        write(target/'optics.cordis.yml',overlay)
        write(target/'cordis.patch.yml',overlay)
        write(target/'package.json', {'name':'dsh-optics-photonics','version':__version__,'description':descriptor['description'],
            'type':'module','main':'index.js','license':'MIT','dsh':{'bundle':{'patch':'./cordis.patch.yml'}},
            'peerDependencies':{'@deepseek-ai/dsh-mcp-client':'*'}})
        (target/'index.js').write_text('export {}\n',encoding='utf-8')
        instructions = 'Start with:\n\n```'+('powershell' if os.name == 'nt' else 'sh')+'\n'+shell_command(['dsh','web','--patch',str(target/'optics.cordis.yml')])+'\n```\nFor persistent activation, merge the single insert patch into the profile’s cordis.patch.yml. Keep other profile entries. This uses DeepSeek’s native dsh-mcp-client, not a Claude configuration file.'
    elif host == 'qiushi':
        write(target/'plugin.json', {**descriptor,'mcpServers':{'optics':{'transport':'stdio',**server}}})
        write(target/'mcp.json',{'mcpServers':{'optics':server}})
        (target/'optics').write_text('#!/bin/sh\nexec '+shlex.quote(interpreter)+' -B "$(dirname "$0")/server.py" "$@"\n', encoding='utf-8')
        (target/'optics').chmod(0o755)
        instructions = 'For Qiushi deployments based on Agentic Research OS, use the agentic-research-os bundle. Other Qiushi hosts can register this mcp.json or invoke server.py tools / server.py call TOOL JSON through their shell interface. Native plugin loading depends on the host edition.'
    else:
        write(target/'mcp.json', {'mcpServers':{'optics':server}})
        instructions = 'Register the optics stdio server from mcp.json in a compatible MCP host. Use the matching host’s own configuration format. This connector needs Python 3.10 or newer; the scientific environment may use a different interpreter.'
    (target/'INSTALL.md').write_text(instructions+'\n\nOptics: https://github.com/Cherish0925/Optics-Photonics-AI-Lab\n', encoding='utf-8')
    return {'directory':str(target),'host':host,'version':__version__,'skills':len(skills)}
