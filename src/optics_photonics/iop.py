"""IOP HTTP interface. Scheduling, durable runs and cancellation remain in IOP."""
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlparse
from urllib.request import Request, build_opener, ProxyHandler, HTTPRedirectHandler
import uuid
from .execution import definition


def origin(value):
    p = urlparse(value)
    return p.scheme.lower(), p.hostname, p.port or (443 if p.scheme == 'https' else 80)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Use the direct IOP endpoint; request was redirected')


class Client:
    def __init__(self, endpoint=None):
        location = Path(os.environ.get('IOP_HOME', Path.home()/'.iop'))/'config.json'
        config = json.loads(location.read_text(encoding='utf-8')) if location.exists() else {}
        host = config.get('host', '127.0.0.1')
        if host in ('0.0.0.0', '::'): host = '127.0.0.1'
        if ':' in host and not host.startswith('['): host = '['+host+']'
        local = f"http://{host}:{config.get('port',8765)}"
        self.endpoint = (endpoint or os.environ.get('IOP_ENDPOINT') or local).rstrip('/')
        parsed = urlparse(self.endpoint)
        if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('IOP_ENDPOINT must be an http(s) service URL without embedded credentials')
        self.token = os.environ.get('IOP_TOKEN', config.get('token', '') if origin(self.endpoint)==origin(local) else '')
        handlers = [NoRedirect()]
        if parsed.hostname in ('localhost','127.0.0.1','::1'): handlers.append(ProxyHandler({}))
        self.open = build_opener(*handlers).open

    def request(self, route, body=None, destination=None):
        data = json.dumps(body, allow_nan=False).encode() if body is not None else None
        headers = {'Content-Type':'application/json','Authorization':'Bearer '+self.token}
        try:
            with self.open(Request(self.endpoint+route, data=data, headers=headers), timeout=30) as response:
                if destination:
                    target = Path(destination).expanduser().resolve()
                    target.parent.mkdir(parents=True, exist_ok=True)
                    # Exclusive create avoids replacing research data on a repeated download.
                    with target.open('xb') as output:
                        import shutil
                        shutil.copyfileobj(response, output)
                    return {'path':str(target), 'bytes':target.stat().st_size}
                return json.loads(response.read())
        except HTTPError as error:
            raise RuntimeError(f'IOP {error.code}: {error.read().decode(errors="replace")}') from None

    def attach(self, tool, path=None):
        if urlparse(self.endpoint).hostname not in ('localhost','127.0.0.1','::1'):
            raise ValueError('Run attach on the IOP computer: its driver uses local executable and environment paths')
        record = definition(tool, path)
        resources = self.request('/v1/resources')['capacities']
        if 'cpu' not in resources:
            cores = len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else (os.cpu_count() or 1)
            self.request('/v1/resources', {'capacities':{**resources,'cpu':cores}})
        current = next((d for d in self.request('/v1/devices') if d['id']==record['id']), None)
        if current:
            route = '/v1/devices/'+quote(record['id'],safe='')+'/configuration'
            if self.request(route) == record:
                return current
            return self.request(route, {'definition':record,'expected_revision':current['revision']})
        return self.request('/v1/devices', record)

    def submit(self, steps, name='Optics research', request_id=None, run_id=None):
        key = request_id or str(uuid.uuid4())
        if run_id:
            result = self.request('/v1/runs/'+quote(run_id,safe='')+'/batches', {'steps':steps,'request_id':key})
        else:
            result = self.request('/v1/runs', {'name':name,'steps':steps,'request_id':key})
        return {'request_id':key, 'submission':result}

    def run(self, run_id):
        return self.request('/v1/runs/'+quote(run_id,safe=''))

    def cancel(self, run_id):
        return self.request('/v1/runs/'+quote(run_id,safe='')+'/cancel', {})

    def files(self, run_id):
        return self.request('/v1/runs/'+quote(run_id,safe='')+'/artifacts')

    def download(self, artifact_id, destination):
        return self.request('/v1/artifacts/'+quote(artifact_id,safe=''), destination=destination)


def step(tool, inputs=None, action='', source='', id='calculate', after=None):
    return {'id':id,'device':'optics-'+tool,'operation':'calculate',
            'arguments':{'action':action,'inputs':inputs or {},'source':source},'after':after or []}
