"""Generate relocatable plugin bundles and host-native connection configurations."""
import json
import os
from pathlib import Path
import shutil
import shlex
import sys
from . import __version__
from .catalogue import resources

HOSTS = ('agentic-research-os','codex','claude','deepseek','qiushi','mcp')


def shell_command(arguments):
    if os.name == 'nt':
        return '& ' + ' '.join("'" + str(value).replace("'", "''") + "'" for value in arguments)
    return shlex.join(str(value) for value in arguments)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def package(destination, host='mcp', python=None):
    if host not in HOSTS: raise ValueError('Unknown host: '+host)
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
                  'description':'Optical software, native calculations and research methods', 'skills':skills}
    if host == 'agentic-research-os':
        descriptor['mcpServers'] = {'optics':{'transport':'stdio','command':'${RESEARCH_PYTHON}',
            'args':['-B','${PACKAGE_ROOT}/server.py','mcp'], 'protocol_version':'2025-11-25'}}
        write(target/'plugin.json',descriptor)
        instructions = 'Install this directory or its ZIP as an Agentic Research OS plugin. Activate its returned revision in the current workspace. The package uses the host Python and carries all connector code, catalogue data and Skills. Configure scientific software on the IOP computer.'
    elif host in ('codex','claude'):
        folder = '.codex-plugin' if host == 'codex' else '.claude-plugin'
        # Both native plugin formats support a shared .mcp.json and discovered skills/ directory.
        native = {k:v for k,v in descriptor.items() if k!='skills'}
        if host == 'codex':
            native.update(skills='./skills/', mcpServers='./.mcp.json', requires_local_executor=True,
                          interface={'displayName':'Optics & Photonics','shortDescription':'Optical software and research calculations','developerName':'AI4Instruments'})
        write(target/folder/'plugin.json', native)
        write(target/'.mcp.json', {'mcpServers':{'optics':server}})
        write(target/'mcp.json', {'mcpServers':{'optics':server}})
        instructions = ('Register this local plugin directory in '+host+'. Its MCP configuration points to the selected Python and this directory. Regenerate with `optics-photonics connect '+host+' --output PATH` after relocating it. The accompanying host connection command is recorded below.')
        if host == 'codex':
            command = ['codex','mcp','add','optics','--',interpreter,'-B',str(target/'server.py'),'mcp']
        else:
            command = ['claude','mcp','add','--transport','stdio','optics','--',interpreter,'-B',str(target/'server.py'),'mcp']
        instructions += '\n\n```'+('powershell' if os.name == 'nt' else 'sh')+'\n'+shell_command(command)+'\n```\n'
    elif host == 'deepseek':
        overlay = [{'insert':[{'id':'optics-photonics','name':'@deepseek-ai/dsh-mcp-client',
                    'config':{'serverName':'optics','transport':'stdio',**server,'env':{},'cwd':str(target)}}]}]
        # JSON is valid YAML and preserves Windows paths without manual escaping.
        write(target/'optics.cordis.yml',overlay)
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
    (target/'INSTALL.md').write_text(instructions+'\n\nIOP: https://github.com/Cherish0925/AI4Instruments/tree/main/iop\nOptics: https://github.com/Cherish0925/optics-photonics\n', encoding='utf-8')
    return {'directory':str(target),'host':host,'version':__version__,'skills':len(skills)}
