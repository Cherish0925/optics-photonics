"""One entry point for people, shell agents and native MCP hosts."""
import argparse
import json
from pathlib import Path
import sys
import subprocess
from . import __version__, catalogue, environments, execution, jobs


def object_argument(value):
    return json.loads(Path(value[1:]).read_text(encoding='utf-8') if value.startswith('@') else value)


def main(argv=None):
    for stream in (sys.stdin,sys.stdout,sys.stderr):
        if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(prog='optics-photonics', description='Optical software and research connections')
    parser.add_argument('--version', action='version', version=__version__)
    commands = parser.add_subparsers(dest='command', required=True)
    search = commands.add_parser('search'); search.add_argument('query', nargs='?', default=''); search.add_argument('--domain'); search.add_argument('--license-group', choices=('open','paid','limited')); search.add_argument('--limit',type=int,default=20); search.add_argument('--offset',type=int,default=0); search.add_argument('--language',choices=('zh','en'),default='en')
    info = commands.add_parser('info'); info.add_argument('tool'); info.add_argument('--language',choices=('zh','en'),default='en')
    register = commands.add_parser('register-software'); register.add_argument('definition', type=object_argument)
    commands.add_parser('registered-software')
    env = commands.add_parser('environments')
    discovery = commands.add_parser('discover'); discovery.add_argument('--root', dest='roots', action='append')
    native_bind = commands.add_parser('bind-native'); native_bind.add_argument('tool'); native_bind.add_argument('--python'); native_bind.add_argument('--sdk-path'); native_bind.add_argument('--options', type=object_argument, default={}); native_bind.add_argument('--threads', type=int, default=1); native_bind.add_argument('--concurrency', type=int, default=1); native_bind.add_argument('--requirements', type=object_argument); native_bind.add_argument('--env', type=object_argument)
    bind = commands.add_parser('bind'); bind.add_argument('tool'); choice=bind.add_mutually_exclusive_group(required=True); choice.add_argument('--python'); choice.add_argument('--command-json',type=object_argument); bind.add_argument('--threads',type=int,default=1); bind.add_argument('--concurrency',type=int,default=1); bind.add_argument('--cwd'); bind.add_argument('--requirements',type=object_argument); bind.add_argument('--env',type=object_argument)
    prep = commands.add_parser('prepare'); prep.add_argument('tool'); prep.add_argument('--python')
    for name in ('run','submit'):
        run = commands.add_parser(name); run.add_argument('tool'); run.add_argument('action',nargs='?',default=''); run.add_argument('--inputs',type=object_argument,default={}); run.add_argument('--program',type=Path)
        if name == 'run': run.add_argument('--output'); run.add_argument('--timeout',type=float)
        else: run.add_argument('--name',default='Optical research'); run.add_argument('--request-id'); run.add_argument('--timeout',type=float)
    sample = commands.add_parser('sample'); sample.add_argument('tool'); sample.add_argument('program', type=Path)
    sample.add_argument('--task', type=object_argument, required=True); sample.add_argument('--policy', type=object_argument, required=True)
    sample.add_argument('--episodes', type=int, required=True); sample.add_argument('--workers', type=int, default=1)
    sample.add_argument('--max-steps', type=int, default=1000); sample.add_argument('--seed', type=int, default=0)
    sample.add_argument('--inputs', type=object_argument, default={}); sample.add_argument('--options', type=object_argument, default={})
    sample.add_argument('--continue-from', nargs='*', default=[], metavar='RUN_ID'); sample.add_argument('--on-error', choices=['stop','continue'], default='stop')
    sample.add_argument('--request-id'); sample.add_argument('--timeout', type=float)
    resources=commands.add_parser('resources'); resources.add_argument('--cpu',type=int); resources.add_argument('--pools',type=object_argument)
    workflow=commands.add_parser('submit-workflow'); workflow.add_argument('file',type=Path,help='JSON file containing a top-level array of steps; each step needs id and tool'); workflow.add_argument('--name',default='Optics research'); workflow.add_argument('--request-id'); workflow.add_argument('--run-id')
    for name in ('status','files','cancel','resume'):
        item=commands.add_parser(name); item.add_argument('run_id')
        if name in ('status','files'):
            item.add_argument('--offset',type=int,default=0); item.add_argument('--limit',type=int,default=50 if name=='status' else 100)
        if name == 'files': item.add_argument('--prefix',default='')
        if name == 'status':
            item.add_argument('--wait',type=float,default=0); item.add_argument('--summary',dest='include_results',action='store_false')
    download=commands.add_parser('download'); download.add_argument('run_id'); download.add_argument('file'); download.add_argument('destination')
    array=commands.add_parser('array',help='Read part of an NPY array or NPZ member'); array.add_argument('run_id'); array.add_argument('file'); array.add_argument('--member'); array.add_argument('--index',type=json.loads,help='JSON list, e.g. [10, [0, 100, 2]]'); array.add_argument('--max-elements',type=int,default=10000)
    read=commands.add_parser('read'); read.add_argument('run_id'); read.add_argument('file'); read.add_argument('--offset',type=int,default=0); read.add_argument('--limit',type=int,default=16384)
    runs=commands.add_parser('runs'); runs.add_argument('--state'); runs.add_argument('--offset',type=int,default=0); runs.add_argument('--limit',type=int,default=20)
    commands.add_parser('mcp')
    commands.add_parser('tools')
    call=commands.add_parser('call'); call.add_argument('tool'); call.add_argument('arguments',type=object_argument)
    from .packages import HOSTS
    connect=commands.add_parser('connect'); connect.add_argument('host',choices=HOSTS); connect.add_argument('--output',required=True); connect.add_argument('--python'); connect.add_argument('--managed-python',dest='managed',action='store_true',help='Use uv to select Python on the destination machine (Codex, Claude, portable)')
    a=vars(parser.parse_args(argv)); command=a.pop('command')
    try:
        if command == 'search': result=catalogue.search(**a)
        elif command == 'info': result=environments.details(**a)
        elif command == 'register-software': result=environments.register(**a['definition'])
        elif command == 'registered-software': result={'software':environments.registered()}
        elif command == 'environments': result={'environments':environments.available()}
        elif command in ('discover', 'bind-native'):
            from . import native
            result = native.discover(**a) if command == 'discover' else native.bind(**a)
        elif command == 'bind': a['command']=a.pop('command_json'); result=environments.bind(**a)
        elif command == 'prepare': result=environments.prepare(**a)
        elif command in ('run','submit'):
            source=a.pop('program'); source=source.read_text(encoding='utf-8') if source else ''
            request={k:a.pop(k) for k in ('inputs','action')}; request['source']=source
            tool=a.pop('tool')
            if command=='run': result=execution.run(tool,request,**a)
            else:
                timeout=a.pop('timeout'); result=jobs.submit([{'id':'calculate','tool':tool,**request,'timeout':timeout}],**a)
        elif command == 'sample':
            from . import sampling
            a['source'] = a.pop('program').read_text(encoding='utf-8'); result = sampling.submit(**a)
        elif command == 'resources': result=jobs.resources(**a)
        elif command == 'runs': result=jobs.list_runs(**a)
        elif command == 'submit-workflow':
            steps=json.loads(a.pop('file').read_text(encoding='utf-8')); result=jobs.submit(steps,**a)
        elif command in ('status','files','cancel','resume','download','read','array'):
            result=getattr(jobs, {'read':'read_result','array':'read_array'}.get(command,command))(**a)
        elif command == 'connect':
            from .packages import package
            result=package(a.pop('output'),**a)
        elif command in ('mcp','tools','call'):
            from .mcp import serve, invoke, TOOLS
            if command=='mcp': serve(); return
            if command=='tools': result={'tools':[{'name':n,'description':d,'inputSchema':s} for n,d,s in TOOLS]}
            else: result=invoke(a['tool'],a['arguments'])
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(json.dumps({'error':str(error)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(1) from None
