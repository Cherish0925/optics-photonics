"""Independent background calculations, dependency graphs and persisted results."""
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import time
import threading
import uuid

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from optics_photonics import environments, execution

TERMINAL = {'succeeded', 'failed', 'cancelled', 'blocked', 'interrupted'}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def cores():
    return len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else (os.cpu_count() or 1)


@contextmanager
def database(path=None):
    root = environments.home(path)
    root.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(root/'jobs.sqlite3', timeout=30)
    db.row_factory = sqlite3.Row
    if db.execute('PRAGMA user_version').fetchone()[0] == 0:
        db.execute('PRAGMA journal_mode=WAL')
        db.executescript('''
        CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, name TEXT, state TEXT,
          created REAL, finished REAL, cancel INTEGER DEFAULT 0, launched REAL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY, payload TEXT, run_id TEXT);
        CREATE TABLE IF NOT EXISTS steps(run_id TEXT, id TEXT, specification TEXT, environment TEXT,
          state TEXT, result TEXT, error TEXT, started REAL, finished REAL, attempt INTEGER DEFAULT 1,
          PRIMARY KEY(run_id,id));
        CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value INTEGER);
        CREATE INDEX IF NOT EXISTS active_steps ON steps(state);
    ''')
        db.execute("INSERT OR IGNORE INTO settings VALUES('cpu',?)", (cores(),))
        db.execute('PRAGMA user_version=1')
        db.commit()
    try:
        yield db
        db.commit()
    except BaseException:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def worker_lock(path, run_id):
    folder = environments.home(path)/'runs'/run_id
    folder.mkdir(parents=True, exist_ok=True)
    stream = (folder/'worker.lock').open('a+b')
    if stream.tell() == 0:
        stream.write(b'0'); stream.flush()
    stream.seek(0)
    acquired = False
    try:
        if os.name == 'nt':
            import msvcrt
            try: msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1); acquired = True
            except OSError: pass
        else:
            import fcntl
            try: fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB); acquired = True
            except BlockingIOError: pass
        yield acquired
    finally:
        if acquired:
            if os.name == 'nt':
                stream.seek(0); msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)
        stream.close()


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', value):
        raise ValueError('Use letters, digits, dots, underscores or hyphens for step and run IDs')
    return value


def validate(steps, previous=None):
    if not isinstance(steps, list) or not steps:
        raise ValueError('Provide a nonempty steps array')
    graph = {s['id']: list(s.get('after', [])) for s in previous or []}
    result = []
    for item in steps:
        if not isinstance(item, dict): raise ValueError('Each step must be an object')
        s = dict(item)
        identifier(s.get('id'))
        if s['id'] in graph: raise ValueError('Duplicate step ID: '+s['id'])
        if set(s)-{'id','tool','action','source','inputs','after','bindings','timeout'}:
            raise ValueError('A step accepts id, tool, action, source, inputs, after, bindings and timeout')
        if not isinstance(s.get('tool'), str): raise ValueError('Each step needs a software tool ID')
        if not isinstance(s.get('inputs', {}), dict): raise ValueError('inputs must be an object')
        if not isinstance(s.get('after', []), list): raise ValueError('after must be a list of step IDs')
        if not isinstance(s.get('bindings', {}), dict): raise ValueError('bindings must be an object')
        if s.get('timeout') is not None and (isinstance(s['timeout'], bool) or not isinstance(s['timeout'], (int,float)) or s['timeout'] <= 0):
            raise ValueError('timeout must be positive seconds')
        s.setdefault('after', [])
        for key, reference in s.get('bindings', {}).items():
            if not isinstance(reference, dict) or set(reference)-{'step','path'} or not isinstance(reference.get('step'),str):
                raise ValueError('A binding needs step and an optional path array')
            if not isinstance(reference.get('path', []), list): raise ValueError('Binding path must be an array of object keys or array indices')
            if reference['step'] not in s['after']: s['after'].append(reference['step'])
        graph[s['id']] = s['after']
        result.append(s)
    remaining = dict(graph)
    while remaining:
        ready = [key for key, deps in remaining.items() if all(dep in graph and dep not in remaining for dep in deps)]
        if not ready: raise ValueError('Workflow contains a cycle or an unknown predecessor')
        for key in ready: del remaining[key]
    return result


def start_worker(run_id, path=None):
    identifier(run_id)
    root = environments.home(path)
    with worker_lock(root, run_id) as available:
        if not available: return
    with database(root) as db:
        db.execute('BEGIN IMMEDIATE')
        row=db.execute('SELECT state,launched FROM runs WHERE id=?',(run_id,)).fetchone()
        if not row or row['state'] in TERMINAL or time.time()-row['launched']<5: return
        db.execute('UPDATE runs SET launched=? WHERE id=?',(time.time(),run_id))
    directory = root/'runs'/run_id
    options = {'creationflags': subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == 'nt' else {'start_new_session': True}
    with (directory/'worker.log').open('ab') as log:
        process = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()), str(root), run_id],
                         stdin=subprocess.DEVNULL, stdout=log, stderr=log, cwd=root, close_fds=True, **options)
    threading.Thread(target=process.wait,daemon=True).start()


def submit(steps, name='Optical research', request_id=None, run_id=None, path=None, _environments=None):
    key = request_id or str(uuid.uuid4())
    payload = encoded({'steps':steps,'name':name,'run_id':run_id})
    with database(path) as db:
        db.execute('BEGIN IMMEDIATE')
        prior = db.execute('SELECT * FROM requests WHERE id=?', (key,)).fetchone()
        if prior:
            if prior['payload'] != payload: raise ValueError('This request_id already belongs to different inputs')
            result_id = prior['run_id']
        else:
            result_id = identifier(run_id) if run_id else str(uuid.uuid4())
            existing = db.execute('SELECT * FROM runs WHERE id=?', (result_id,)).fetchone()
            if run_id and not existing: raise ValueError('Unknown run: '+run_id)
            if existing and existing['cancel']: raise ValueError('Resume the cancelled run before appending steps')
            previous = [json.loads(r[0]) for r in db.execute('SELECT specification FROM steps WHERE run_id=?', (result_id,))]
            checked = validate(steps, previous)
            capacity = db.execute("SELECT value FROM settings WHERE key='cpu'").fetchone()[0]
            prepared = []
            for spec in checked:
                environment = (_environments or {}).get(spec['tool']) or execution.binding(spec['tool'], path)
                if environment['threads'] > capacity:
                    raise ValueError(f"{spec['tool']} requests {environment['threads']} CPU threads; configured capacity is {capacity}")
                prepared.append((result_id,spec['id'],encoded(spec),encoded(environment),'queued'))
            if not existing:
                db.execute('INSERT INTO runs(id,name,state,created) VALUES(?,?,?,?)', (result_id,name,'queued',time.time()))
            else:
                db.execute("UPDATE runs SET state=CASE WHEN state='running' THEN state ELSE 'queued' END,finished=NULL WHERE id=?", (result_id,))
            db.executemany('INSERT INTO steps(run_id,id,specification,environment,state) VALUES(?,?,?,?,?)', prepared)
            db.execute('INSERT INTO requests VALUES(?,?,?)', (key,payload,result_id))
    start_worker(result_id, path)
    return {'run_id':result_id, 'request_id':key}


def prepare(tool, python=None, request_id=None, path=None):
    from .catalogue import software
    if not software(tool)['connection'].get('pip'):
        raise ValueError('Use this software’s native installer, then bind its environment')
    config={'kind':'command','command':[sys.executable,'-B',str(Path(__file__).with_name('setup_worker.py'))],'threads':1,'concurrency':1,'cwd':None}
    return submit([{'id':'install','tool':tool,'inputs':{'tool':tool,'python':python,'home':str(environments.home(path))}}],name='Prepare '+tool,request_id=request_id,path=path,_environments={tool:config})


def reconcile(path=None):
    with database(path) as db:
        runs = [r[0] for r in db.execute("SELECT id FROM runs WHERE state='running'")]
    for run_id in runs:
        with worker_lock(path, run_id) as available:
            if not available: continue
            with database(path) as db:
                db.execute("UPDATE steps SET state='interrupted',error='Background worker stopped; completed results are retained',finished=? WHERE run_id=? AND state='running'", (time.time(),run_id))
                db.execute("UPDATE runs SET state='interrupted',finished=? WHERE id=? AND state='running'", (time.time(),run_id))


def status(run_id, path=None, offset=0, limit=50):
    identifier(run_id)
    if offset < 0 or not 1 <= limit <= 200: raise ValueError('Use offset >= 0 and limit between 1 and 200')
    reconcile(path)
    with database(path) as db:
        row = db.execute('SELECT * FROM runs WHERE id=?', (run_id,)).fetchone()
        if not row: raise ValueError('Unknown run: '+run_id)
        result = dict(row)
        result['counts'] = dict(db.execute('SELECT state,count(*) FROM steps WHERE run_id=? GROUP BY state', (run_id,)))
        items = db.execute('SELECT id,state,result,error,started,finished,attempt FROM steps WHERE run_id=? ORDER BY rowid LIMIT ? OFFSET ?', (run_id,limit+1,offset)).fetchall()
        result['steps'] = [{**dict(s), 'result':json.loads(s['result']) if s['result'] else None} for s in items[:limit]]
        result['next_offset'] = offset+limit if len(items)>limit else None
    if result['state']=='queued': start_worker(run_id, path)
    return result


def list_runs(state=None, offset=0, limit=20, path=None):
    if offset<0 or not 1<=limit<=200: raise ValueError('Use offset >= 0 and limit between 1 and 200')
    reconcile(path)
    with database(path) as db:
        rows=db.execute('SELECT id,name,state,created,finished FROM runs WHERE (? IS NULL OR state=?) ORDER BY created DESC LIMIT ? OFFSET ?',(state,state,limit+1,offset)).fetchall()
    return {'runs':[dict(r) for r in rows[:limit]],'next_offset':offset+limit if len(rows)>limit else None}


def cancel(run_id, path=None):
    identifier(run_id)
    with database(path) as db:
        if not db.execute('SELECT 1 FROM runs WHERE id=?', (run_id,)).fetchone(): raise ValueError('Unknown run: '+run_id)
        db.execute('UPDATE runs SET cancel=1 WHERE id=?', (run_id,))
    start_worker(run_id, path)
    return {'run_id':run_id,'cancel_requested':True}


def resume(run_id, path=None):
    identifier(run_id)
    with worker_lock(path, run_id) as available:
        if not available: raise ValueError('This run is still executing')
        with database(path) as db:
            if not db.execute('SELECT 1 FROM runs WHERE id=?', (run_id,)).fetchone(): raise ValueError('Unknown run: '+run_id)
            db.execute("UPDATE steps SET state='queued',result=NULL,error=NULL,started=NULL,finished=NULL,attempt=attempt+1 WHERE run_id=? AND state<>'succeeded'", (run_id,))
            db.execute("UPDATE runs SET state='queued',cancel=0,finished=NULL WHERE id=?", (run_id,))
    start_worker(run_id, path)
    return {'run_id':run_id,'resumed':True}


def resources(cpu=None, path=None):
    with database(path) as db:
        if cpu is not None:
            if type(cpu) is not int or cpu < 1: raise ValueError('cpu must be a positive integer')
            pending=[json.loads(r[0])['threads'] for r in db.execute("SELECT environment FROM steps WHERE state='queued'")]
            if pending and max(pending)>cpu: raise ValueError('A queued calculation requires more threads than this capacity')
            db.execute("UPDATE settings SET value=? WHERE key='cpu'", (cpu,))
        return {'cpu':db.execute("SELECT value FROM settings WHERE key='cpu'").fetchone()[0]}


def file_path(run_id, file, path=None):
    identifier(run_id)
    root = (environments.home(path)/'runs'/run_id).resolve()
    selected = (root/file).resolve()
    if not selected.is_relative_to(root) or not selected.is_file(): raise ValueError('Unknown result file')
    return selected


def files(run_id, path=None, offset=0, limit=100):
    identifier(run_id)
    if offset<0 or not 1<=limit<=500: raise ValueError('Use offset >= 0 and limit between 1 and 500')
    root = environments.home(path)/'runs'/run_id
    if not root.is_dir(): raise ValueError('Unknown run: '+run_id)
    found = []
    for item in sorted(root.rglob('*')):
        if item.is_file() and not item.is_symlink() and item.name != 'worker.lock':
            found.append({'file':str(item.relative_to(root)).replace(os.sep,'/'),'bytes':item.stat().st_size})
    return {'run_id':run_id, 'files':found[offset:offset+limit], 'total':len(found), 'next_offset':offset+limit if offset+limit<len(found) else None}


def download(run_id, file, destination, path=None):
    source = file_path(run_id, file, path)
    target = Path(destination).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open('rb') as incoming, target.open('xb') as outgoing: shutil.copyfileobj(incoming, outgoing)
    return {'path':str(target),'bytes':target.stat().st_size}


def read_result(run_id, file, offset=0, limit=16384, path=None):
    if offset<0 or not 1<=limit<=65536: raise ValueError('Use offset >= 0 and limit between 1 and 65536 bytes')
    source = file_path(run_id,file,path)
    with source.open('rb') as stream:
        stream.seek(offset); content=stream.read(limit)
    try: data=content.decode('utf-8'); format='utf-8'
    except UnicodeDecodeError: data=base64.b64encode(content).decode('ascii'); format='base64'
    return {'file':file,'offset':offset,'encoding':format,'data':data,'next_offset':offset+len(content) if offset+len(content)<source.stat().st_size else None}


def resolved_inputs(spec, results):
    inputs = dict(spec.get('inputs', {}))
    for key, reference in spec.get('bindings', {}).items():
        value = results[reference['step']]
        for part in reference.get('path', []): value = value[part]
        inputs[key] = value
    return inputs


def perform(run_id, row, path):
    spec, config = json.loads(row['specification']), json.loads(row['environment'])
    output = environments.home(path)/'runs'/run_id/row['id']/('attempt-'+str(row['attempt']))
    def cancelled():
        with database(path) as db: return bool(db.execute('SELECT cancel FROM runs WHERE id=?',(run_id,)).fetchone()[0])
    try:
        with database(path) as db:
            results = {r['id']:json.loads(r['result']) for r in db.execute("SELECT id,result FROM steps WHERE run_id=? AND state='succeeded'",(run_id,))}
        request = {'action':spec.get('action',''),'source':spec.get('source',''),'inputs':resolved_inputs(spec,results)}
        result = execution.run(spec['tool'],request,output=output,configuration=config,timeout=spec.get('timeout'),cancel=cancelled)
        record = result['record']
        result = {'output':result['output'], **record} if isinstance(record,dict) and 'result' in record else {'output':result['output'],'result':record}
        state, error = 'succeeded', None
    except execution.Cancelled as exc:
        state, result, error = 'cancelled', None, str(exc)
    except Exception as exc:
        state, result, error = 'failed', None, str(exc)
    with database(path) as db:
        db.execute('UPDATE steps SET state=?,result=?,error=?,finished=? WHERE run_id=? AND id=?', (state,encoded(result) if result is not None else None,error,time.time(),run_id,row['id']))


def work(run_id, path):
    with worker_lock(path,run_id) as available:
        if not available: return
        reconcile(path)
        with database(path) as db:
            run = db.execute('SELECT state FROM runs WHERE id=?',(run_id,)).fetchone()
            if not run or run[0] in TERMINAL: return
            db.execute("UPDATE runs SET state='running',launched=0 WHERE id=?",(run_id,))
        with ThreadPoolExecutor(max_workers=resources(path=path)['cpu']) as pool:
            pending = {}
            while True:
                for key, future in list(pending.items()):
                    if future.done(): future.result(); del pending[key]
                with database(path) as db:
                    db.execute('BEGIN IMMEDIATE')
                    cancelled = db.execute('SELECT cancel FROM runs WHERE id=?',(run_id,)).fetchone()[0]
                    rows = db.execute('SELECT * FROM steps WHERE run_id=? ORDER BY rowid',(run_id,)).fetchall()
                    states = {r['id']:r['state'] for r in rows}
                    if all(s in TERMINAL for s in states.values()):
                        state = 'cancelled' if cancelled else ('succeeded' if all(s=='succeeded' for s in states.values()) else 'failed')
                        db.execute('UPDATE runs SET state=?,finished=? WHERE id=?',(state,time.time(),run_id))
                        break
                    active = [(json.loads(r['specification']),json.loads(r['environment'])) for r in db.execute("SELECT specification,environment FROM steps WHERE state='running'")]
                    used = sum(c['threads'] for s,c in active)
                    counts = Counter(s['tool'] for s,c in active)
                    cpu = db.execute("SELECT value FROM settings WHERE key='cpu'").fetchone()[0]
                    ready = []
                    for row in rows:
                        if row['state'] != 'queued': continue
                        spec, config = json.loads(row['specification']),json.loads(row['environment'])
                        if cancelled:
                            db.execute("UPDATE steps SET state='cancelled',finished=? WHERE run_id=? AND id=?",(time.time(),run_id,row['id'])); continue
                        if any(states[d] in TERMINAL-{'succeeded'} for d in spec['after']):
                            db.execute("UPDATE steps SET state='blocked',error='A predecessor did not complete',finished=? WHERE run_id=? AND id=?",(time.time(),run_id,row['id'])); continue
                        if not all(states[d]=='succeeded' for d in spec['after']): continue
                        concurrency = min([config['concurrency']]+[c['concurrency'] for s,c in active if s['tool']==spec['tool']])
                        if used+config['threads']>cpu or counts[spec['tool']]>=concurrency: continue
                        db.execute("UPDATE steps SET state='running',started=? WHERE run_id=? AND id=?",(time.time(),run_id,row['id']))
                        used+=config['threads']; counts[spec['tool']]+=1; active.append((spec,config)); ready.append(dict(row))
                for row in ready: pending[row['id']]=pool.submit(perform,run_id,row,path)
                time.sleep(.1)
    with database(path) as db:
        restart = db.execute("SELECT state FROM runs WHERE id=?",(run_id,)).fetchone()[0]=='queued'
    if restart: start_worker(run_id,path)


if __name__=='__main__':
    work(sys.argv[2], sys.argv[1])
