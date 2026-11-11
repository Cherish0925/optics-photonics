"""Dependency-free MCP stdio server. Calculations run independently in the background."""
import json
import sys
from . import __version__, catalogue, environments, operations
from . import jobs


def schema(properties=None, required=None):
    return {'type':'object','properties':properties or {},'required':required or [],'additionalProperties':False}


STRING = {'type':'string'}
TOOLS = [
    ('software_search', 'Find optical software by physical problem, domain and license; paginated results. Does not imply installation.', schema({'query':STRING,'domain':STRING,'license_group':{'enum':['open','paid','limited']},'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':100},'language':{'enum':['zh','en']}})),
    ('software_details', 'Read native interfaces, installation source, upstream MCP/Skills and executable operation inputs for one software.', schema({'tool':STRING,'language':{'enum':['zh','en']}},['tool'])),
    ('register_software', 'Register a local research library, solver or executable that is not in the published catalogue. Provide its identity, installed module/distribution names and documentation sources; then use bind_environment. Registration does not download or execute it.', schema({'tool':STRING,'name':STRING,'description':STRING,'kind':{'enum':['python','command']},'modules':{'type':'array','items':STRING},'distributions':{'type':'array','items':STRING},'sources':{'type':'array','items':STRING}},['tool','name','description'])),
    ('registered_software', 'List locally registered research tools beyond the published software catalogue.', schema()),
    ('environments', 'Read a short page of configured software. refresh=true checks only this page’s installed programs; tool selects one connection.', schema({'tool':STRING,'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':100},'refresh':{'type':'boolean'}})),
    ('discover_native_software', 'Find local Lumerical, COMSOL, OpticStudio and CST installation paths; inspect adapter requirements and native program examples. Does not launch a licensed solver.', schema({'roots':{'type':'array','items':STRING}})),
    ('bind_native_software', 'Connect an installed commercial solver SDK to its own Python environment. Each calculation owns a software session with full native API, project load/save and data export.', schema({'tool':STRING,'python':STRING,'sdk_path':STRING,'options':{'type':'object'},'threads':{'type':'integer','minimum':1},'concurrency':{'type':'integer','minimum':1},'requirements':{'type':'object','additionalProperties':{'type':'integer','minimum':1}},'env':{'type':'object','additionalProperties':STRING}},['tool'])),
    ('prepare_environment', 'Install a documented software recipe into its isolated Python environment in the background; returns a run ID. Existing environments can be bound directly.', schema({'tool':STRING,'python':STRING,'request_id':STRING},['tool'])),
    ('bind_environment', 'Connect an existing scientific Python environment or explicit native executable; does not install a solver.', schema({'tool':STRING,'python':STRING,'command':{'type':'array','items':STRING,'minItems':1},'threads':{'type':'integer','minimum':1},'concurrency':{'type':'integer','minimum':1},'cwd':STRING,'requirements':{'type':'object','additionalProperties':{'type':'integer','minimum':1}},'env':{'type':'object','additionalProperties':STRING}},['tool'])),
    ('compute_resources', 'Read or update shared CPU and named resource capacities (GPU, solver license, memory slots). Requirements are acquired together across all runs; adapters select the actual hardware or license.', schema({'cpu':{'type':'integer','minimum':1},'pools':{'type':'object','additionalProperties':{'type':'integer','minimum':1}}})),
    ('submit_calculation', 'Start an independent background calculation and return its run ID immediately. source runs a complete native Python program with INPUTS, OUTPUT_DIR and RESULT. Reuse request_id when retrying.', schema({'tool':STRING,'inputs':{'type':'object'},'action':STRING,'source':STRING,'name':STRING,'request_id':STRING,'timeout':{'type':'number','exclusiveMinimum':0}},['tool'])),
    ('sample_episodes', 'Run complete research episodes in independent native worker processes. source defines make_env() with Gymnasium-style reset/step/close and make_policy(seed) returning an action function. task/policy need id/version. CPU and software concurrency settings apply across jobs. Each worker saves trajectory.jsonl and typed arrays; read through result_files/read_result. No solver installation or training algorithm is implied.', schema({'tool':STRING, 'source':STRING, 'task':{'type':'object'}, 'policy':{'type':'object'}, 'episodes':{'type':'integer','minimum':1}, 'workers':{'type':'integer','minimum':1}, 'max_steps':{'type':'integer','minimum':1}, 'seed':{'type':'integer','minimum':0}, 'inputs':{'type':'object'}, 'options':{'type':'object'}, 'request_id':STRING, 'timeout':{'type':'number','exclusiveMinimum':0}}, ['tool','source','task','policy','episodes'])),
    ('submit_workflow', 'Submit dependent or independent calculation steps in one request. Each step has id, tool, action or source, inputs, after, optional timeout and bindings {input_name: {step, path: [keys]}}. Supply run_id to append a batch to an existing research run.', schema({'steps':{'type':'array','items':{'type':'object'},'minItems':1},'name':STRING,'request_id':STRING,'run_id':STRING},['steps'])),
    ('run_status', 'Read compact execution state. wait (0–25 seconds) waits for completion without repeated calls. Results stay in files by default; include_results returns step values. Calculations continue after disconnection.', schema({'run_id':STRING,'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':200},'include_results':{'type':'boolean'},'wait':{'type':'number','minimum':0,'maximum':25}},['run_id'])),
    ('cancel_run', 'Cancel a research run and its active calculations.', schema({'run_id':STRING},['run_id'])),
    ('result_files', 'List files written so far by a research run, including running calculations.', schema({'run_id':STRING,'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':500}},['run_id'])),
    ('download_result', 'Copy a result file to a new destination on the MCP host computer.', schema({'run_id':STRING,'file':STRING,'destination':STRING},['run_id','file','destination'])),
    ('read_result', 'Read a bounded part of a result or log. Text returns UTF-8; binary returns base64.', schema({'run_id':STRING,'file':STRING,'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':65536}},['run_id','file'])),
    ('list_runs', 'Find previous and active research runs after reconnecting.', schema({'state':STRING,'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':200}})),
    ('resume_run', 'Rerun unfinished steps of a stopped research run, keeping completed steps and previous output files.', schema({'run_id':STRING},['run_id'])),
]


def invoke(name, args):
    if name == 'software_search': return catalogue.search(**args)
    if name == 'software_details':
        return {**environments.software(**args), 'execution':operations.details(args['tool'])}
    if name == 'register_software': return environments.register(**args)
    if name == 'registered_software': return {'software': environments.registered()}
    if name == 'environments': return environments.page(**args)
    if name in ('discover_native_software','bind_native_software'):
        from . import native
        return native.discover(**args) if name == 'discover_native_software' else native.bind(**args)
    if name == 'bind_environment': return environments.bind(**args)
    if name == 'prepare_environment': return jobs.prepare(**args)
    if name == 'compute_resources': return jobs.resources(**args)
    if name == 'submit_calculation':
        data = dict(args)
        name = data.pop('name','Optics research'); key = data.pop('request_id',None)
        return jobs.submit([{'id':'calculate',**data}],name=name,request_id=key)
    if name == 'sample_episodes':
        from . import sampling
        return sampling.submit(**args)
    if name == 'submit_workflow': return jobs.submit(**args)
    if name == 'run_status': return jobs.status(**{'include_results':False, **args})
    if name == 'cancel_run': return jobs.cancel(**args)
    if name == 'result_files': return jobs.files(**args)
    if name == 'download_result': return jobs.download(**args)
    if name == 'read_result': return jobs.read_result(**args)
    if name == 'resume_run': return jobs.resume(**args)
    if name == 'list_runs': return jobs.list_runs(**args)
    raise ValueError('Unknown tool: '+name)


def serve(input_stream=None, output_stream=None):
    incoming, outgoing = input_stream or sys.stdin, output_stream or sys.stdout
    supported = {'2025-11-25','2025-06-18','2025-03-26','2024-11-05'}
    for line in incoming:
        if not line.strip(): continue
        id = None
        try:
            request = json.loads(line)
            if not isinstance(request, dict) or request.get('jsonrpc') != '2.0':
                raise ValueError('Expected a JSON-RPC 2.0 request')
            if 'id' not in request: continue
            id = request['id']; method = request.get('method'); params = request.get('params', {})
            if method == 'initialize':
                proposed = params.get('protocolVersion')
                result = {'protocolVersion':proposed if proposed in supported else '2025-11-25',
                          'serverInfo':{'name':'optics-photonics','version':__version__},
                          'capabilities':{'tools':{'listChanged':False},'resources':{}},
                          'instructions':'Search software, read its operation inputs, select an installed environment, and submit long calculations to the independent background worker. Native programs use INPUTS, OUTPUT_DIR and a JSON RESULT. Solver installation and license requirements remain those of the upstream software.'}
            elif method == 'ping': result = {}
            elif method == 'tools/list':
                result = {'tools':[{'name':n,'description':d,'inputSchema':s} for n,d,s in TOOLS]}
            elif method == 'resources/list':
                result = {'resources':[{'uri':'optics://guides/'+name,'name':name,'mimeType':'text/markdown'}
                    for name in ('optical-computation','optical-research')]}
            elif method == 'resources/read':
                uri = params.get('uri','')
                name = uri.removeprefix('optics://guides/')
                if uri != 'optics://guides/'+name or name not in ('optical-computation','optical-research'):
                    raise ValueError('Unknown optical guide')
                text = (catalogue.resources()/'skills'/name/'SKILL.md').read_text(encoding='utf-8')
                result = {'contents':[{'uri':uri,'mimeType':'text/markdown','text':text}]}
            elif method == 'tools/call':
                try:
                    name = params['name']; args = params.get('arguments', {})
                    spec = next((s for n,d,s in TOOLS if n == name), None)
                    if spec is None: raise ValueError('Unknown tool: '+name)
                    if not isinstance(args, dict) or set(args)-set(spec['properties']) or set(spec['required'])-set(args):
                        raise ValueError('Arguments do not match this tool’s input schema')
                    value = invoke(name, args)
                    result = {'content':[{'type':'text','text':json.dumps(value,ensure_ascii=False,allow_nan=False)}], 'structuredContent':value, 'isError':False}
                except Exception as error:
                    result = {'content':[{'type':'text','text':str(error)}], 'isError':True}
            else:
                outgoing.write(json.dumps({'jsonrpc':'2.0','id':id,'error':{'code':-32601,'message':'Method not found'}})+'\n'); outgoing.flush(); continue
            response = {'jsonrpc':'2.0','id':id,'result':result}
        except json.JSONDecodeError:
            response = {'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Invalid JSON'}}
        except Exception as error:
            response = {'jsonrpc':'2.0','id':id,'error':{'code':-32600,'message':str(error)}}
        outgoing.write(json.dumps(response,ensure_ascii=False,allow_nan=False)+'\n'); outgoing.flush()
