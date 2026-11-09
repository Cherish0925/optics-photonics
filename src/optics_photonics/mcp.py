"""Dependency-free MCP stdio server. Long calculations are submitted to IOP."""
import json
import sys
from . import __version__, catalogue, environments, operations
from .iop import Client, step


def schema(properties=None, required=None):
    return {'type':'object','properties':properties or {},'required':required or [],'additionalProperties':False}


STRING = {'type':'string'}
TOOLS = [
    ('software_search', 'Find optical software by physical problem, domain and license; paginated results. Does not imply installation.', schema({'query':STRING,'domain':STRING,'license_group':{'enum':['open','paid','limited']},'offset':{'type':'integer','minimum':0},'limit':{'type':'integer','minimum':1,'maximum':100},'language':{'enum':['zh','en']}})),
    ('software_details', 'Read native interfaces, installation source, upstream MCP/Skills and executable operation inputs for one software.', schema({'tool':STRING,'language':{'enum':['zh','en']}},['tool'])),
    ('environments', 'List configured local scientific interpreters and executable availability.', schema()),
    ('bind_environment', 'Connect an existing scientific Python environment or explicit native executable; does not install a solver.', schema({'tool':STRING,'python':STRING,'command':{'type':'array','items':STRING,'minItems':1},'threads':{'type':'integer','minimum':1},'concurrency':{'type':'integer','minimum':1},'cwd':STRING},['tool'])),
    ('attach_iop', 'Register one configured software environment with the IOP service on this computer.', schema({'tool':STRING},['tool'])),
    ('submit_calculation', 'Start a durable IOP calculation and return its run ID immediately. source runs a complete native Python program with INPUTS, OUTPUT_DIR and RESULT. Reuse request_id when retrying.', schema({'tool':STRING,'inputs':{'type':'object'},'action':STRING,'source':STRING,'name':STRING,'request_id':STRING},['tool'])),
    ('submit_workflow', 'Submit dependent or independent IOP steps in one request. Each step uses device optics-ID, operation calculate, arguments {action,inputs,source}, id and after. Supply run_id to append a batch to an existing external experiment.', schema({'steps':{'type':'array','items':{'type':'object'},'minItems':1},'name':STRING,'request_id':STRING,'run_id':STRING},['steps'])),
    ('run_status', 'Read execution state and compact results; the IOP service continues after this MCP connection closes.', schema({'run_id':STRING},['run_id'])),
    ('cancel_run', 'Cancel an IOP run and its active calculations.', schema({'run_id':STRING},['run_id'])),
    ('result_files', 'List files retained by an IOP run.', schema({'run_id':STRING},['run_id'])),
    ('download_result', 'Stream an IOP artifact to a new file on the MCP host computer; avoids copying scientific arrays into the conversation.', schema({'artifact_id':STRING,'destination':STRING},['artifact_id','destination'])),
]


def invoke(name, args):
    if name == 'software_search': return catalogue.search(**args)
    if name == 'software_details':
        return {**catalogue.software(**args), 'execution':operations.details(args['tool'])}
    if name == 'environments': return {'environments':environments.available()}
    if name == 'bind_environment': return environments.bind(**args)
    client = Client()
    if name == 'attach_iop': return client.attach(**args)
    if name == 'submit_calculation':
        data = dict(args)
        name = data.pop('name','Optics research'); key = data.pop('request_id',None)
        return client.submit([step(**data)], name=name, request_id=key)
    if name == 'submit_workflow': return client.submit(**args)
    if name == 'run_status': return client.run(**args)
    if name == 'cancel_run': return client.cancel(**args)
    if name == 'result_files': return {'files':client.files(**args)}
    if name == 'download_result': return client.download(**args)
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
                          'capabilities':{'tools':{'listChanged':False}},
                          'instructions':'Search software, read its operation inputs, select an installed environment, and submit long calculations to IOP. Native programs use INPUTS, OUTPUT_DIR and a JSON RESULT. Solver installation and license requirements remain those of the upstream software.'}
            elif method == 'ping': result = {}
            elif method == 'tools/list':
                result = {'tools':[{'name':n,'description':d,'inputSchema':s} for n,d,s in TOOLS]}
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
