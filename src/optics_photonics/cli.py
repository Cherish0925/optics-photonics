"""One entry point for people, shell agents and native MCP hosts."""
import argparse
import json
from pathlib import Path
import sys
from . import __version__, catalogue, environments, execution, operations
from .iop import Client, step


def object_argument(value):
    return json.loads(Path(value[1:]).read_text(encoding='utf-8') if value.startswith('@') else value)


def main(argv=None):
    parser = argparse.ArgumentParser(prog='optics-photonics', description='Optical software and research connections')
    parser.add_argument('--version', action='version', version=__version__)
    commands = parser.add_subparsers(dest='command', required=True)
    search = commands.add_parser('search'); search.add_argument('query', nargs='?', default=''); search.add_argument('--domain'); search.add_argument('--license-group', choices=('open','paid','limited')); search.add_argument('--limit',type=int,default=20); search.add_argument('--offset',type=int,default=0); search.add_argument('--language',choices=('zh','en'),default='en')
    info = commands.add_parser('info'); info.add_argument('tool'); info.add_argument('--language',choices=('zh','en'),default='en')
    env = commands.add_parser('environments')
    bind = commands.add_parser('bind'); bind.add_argument('tool'); choice=bind.add_mutually_exclusive_group(required=True); choice.add_argument('--python'); choice.add_argument('--command-json',type=object_argument); bind.add_argument('--threads',type=int,default=1); bind.add_argument('--concurrency',type=int,default=1); bind.add_argument('--cwd')
    prep = commands.add_parser('prepare'); prep.add_argument('tool'); prep.add_argument('--python')
    for name in ('run','submit'):
        run = commands.add_parser(name); run.add_argument('tool'); run.add_argument('action',nargs='?',default=''); run.add_argument('--inputs',type=object_argument,default={}); run.add_argument('--program',type=Path)
        if name == 'run': run.add_argument('--output'); run.add_argument('--timeout',type=float)
        else: run.add_argument('--name',default='Optics research'); run.add_argument('--request-id')
    attach=commands.add_parser('attach'); attach.add_argument('tool')
    workflow=commands.add_parser('submit-workflow'); workflow.add_argument('file',type=Path); workflow.add_argument('--name',default='Optics research'); workflow.add_argument('--request-id'); workflow.add_argument('--run-id')
    for name in ('status','files','cancel'):
        item=commands.add_parser(name); item.add_argument('run_id')
    download=commands.add_parser('download'); download.add_argument('artifact_id'); download.add_argument('destination')
    commands.add_parser('mcp')
    commands.add_parser('tools')
    call=commands.add_parser('call'); call.add_argument('tool'); call.add_argument('arguments',type=object_argument)
    from .packages import HOSTS
    connect=commands.add_parser('connect'); connect.add_argument('host',choices=HOSTS); connect.add_argument('--output',required=True); connect.add_argument('--python')
    a=vars(parser.parse_args(argv)); command=a.pop('command')
    try:
        if command == 'search': result=catalogue.search(**a)
        elif command == 'info': result={**catalogue.software(**a),'execution':operations.details(a['tool'])}
        elif command == 'environments': result={'environments':environments.available()}
        elif command == 'bind': a['command']=a.pop('command_json'); result=environments.bind(**a)
        elif command == 'prepare': result=environments.prepare(**a)
        elif command in ('run','submit'):
            source=a.pop('program'); source=source.read_text(encoding='utf-8') if source else ''
            request={k:a.pop(k) for k in ('inputs','action')}; request['source']=source
            tool=a.pop('tool')
            if command=='run': result=execution.run(tool,request,**a)
            else: result=Client().submit([step(tool,**request)],**a)
        elif command == 'attach': result=Client().attach(**a)
        elif command == 'submit-workflow':
            steps=json.loads(a.pop('file').read_text(encoding='utf-8')); result=Client().submit(steps,**a)
        elif command in ('status','files','cancel'):
            result=getattr(Client(), {'status':'run'}.get(command,command))(**a)
        elif command == 'download': result=Client().download(**a)
        elif command == 'connect':
            from .packages import package
            result=package(a.pop('output'),**a)
        elif command in ('mcp','tools','call'):
            from .mcp import serve, invoke, TOOLS
            if command=='mcp': serve(); return
            if command=='tools': result={'tools':[{'name':n,'description':d,'inputSchema':s} for n,d,s in TOOLS]}
            else: result=invoke(a['tool'],a['arguments'])
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False))
    except (ValueError, KeyError, OSError, RuntimeError) as error:
        print(json.dumps({'error':str(error)},ensure_ascii=False),file=sys.stderr)
        raise SystemExit(1) from None
