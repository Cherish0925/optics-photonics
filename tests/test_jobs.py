import errno
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from optics_photonics import environments, jobs

FIXTURE = '''import json,os,sys,time
from pathlib import Path
p=json.loads(Path(os.environ['OPTICS_REQUEST_FILE']).read_text())['inputs']
if p.get('marker'): Path(p['marker']).write_text('started')
if p.get('wait_for'):
 end=time.monotonic()+8
 while not Path(p['wait_for']).exists():
  if time.monotonic()>end: raise RuntimeError('Parallel peer did not start')
  time.sleep(.02)
if p.get('fail_once') and not Path(p['fail_once']).exists():
 Path(p['fail_once']).touch(); raise RuntimeError('First attempt stopped')
if p.get('critical'):
 with Path(p['critical']).open('x') as f: f.write('active')
 time.sleep(.15)
 Path(p['critical']).unlink()
if p.get('child'):
 import subprocess
 subprocess.Popen([sys.executable,'-c',"import time;from pathlib import Path;p=Path("+repr(p['child'])+");[(p.write_text(str(i)),time.sleep(.05)) for i in range(2000)]"])
 time.sleep(100)
time.sleep(p.get('sleep',0))
Path(os.environ['OPTICS_OUTPUT_DIR'],'value.csv').write_text(str(p.get('value',1)+p.get('other',0)))
Path(os.environ['OPTICS_RESULT_FILE']).write_text(json.dumps({'value':p.get('value',1)+p.get('other',0)}))
'''


class JobsTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.home=self.root/'config';self.script=self.root/'solver.py';self.script.write_text(FIXTURE)
        environments.bind('scipy',command=[sys.executable,str(self.script)],path=self.home,concurrency=3)
        jobs.resources(cpu=2,path=self.home)
        self.runs=[]
    def tearDown(self):
        for run in self.runs:
            with jobs.worker_lock(self.home,run) as free: active=not free
            if active:
                jobs.cancel(run,path=self.home)
                self.wait(run)
            end=time.monotonic()+5
            while time.monotonic()<end:
                with jobs.worker_lock(self.home,run) as free:
                    if free: break
                time.sleep(.05)
        # After unlocking, a worker finishes notifications and checks for queued
        # work. Its final database access can overlap directory removal; Windows
        # may also retain an inherited log handle until the process exits.
        end=time.monotonic()+5
        while True:
            try:
                self.tmp.cleanup()
                break
            except OSError as exc:
                finishing = exc.errno == errno.ENOTEMPTY or (os.name == 'nt' and isinstance(exc, PermissionError))
                if not finishing or time.monotonic() >= end: raise
                time.sleep(.02)
    def submit(self,steps,**kwargs):
        r=jobs.submit(steps,path=self.home,**kwargs);self.runs.append(r['run_id']);return r
    def wait(self,run,timeout=25):
        end=time.monotonic()+timeout
        while time.monotonic()<end:
            result=jobs.status(run,path=self.home)
            if result['state'] in jobs.TERMINAL:return result
            time.sleep(.05)
        self.fail('Background calculation did not finish: '+str(result))
    def step(self,id,**inputs):return {'id':id,'tool':'scipy','inputs':inputs}

    def test_parallel_dependency_binding_and_request_reuse(self):
        a=self.root/'a';b=self.root/'b'
        steps=[self.step('a',value=20,marker=str(a),wait_for=str(b)),self.step('b',value=22,marker=str(b),wait_for=str(a)),
               {**self.step('sum'),'bindings':{'value':{'step':'a','path':['result','value']},'other':{'step':'b','path':['result','value']}}}]
        submission=self.submit(steps,request_id='sum-request')
        self.assertEqual(jobs.submit(steps,path=self.home,request_id='sum-request'),submission)
        result=self.wait(submission['run_id']);self.assertEqual(result['state'],'succeeded',result)
        self.assertEqual(result['steps'][2]['result']['result']['value'],42)
        with self.assertRaises(ValueError):jobs.submit([self.step('other')],path=self.home,request_id='sum-request')
        files=jobs.files(submission['run_id'],path=self.home)
        file=next(f['file'] for f in files['files'] if f['file'].startswith('sum/') and f['file'].endswith('value.csv'))
        self.assertEqual(jobs.read_result(submission['run_id'],file,path=self.home)['data'],'42')
        jobs.download(submission['run_id'],file,str(self.root/'copy.csv'),path=self.home)
        self.assertEqual((self.root/'copy.csv').read_text(),'42')

    def test_total_capacity_is_shared_between_runs(self):
        jobs.resources(cpu=1,path=self.home)
        runs=[self.submit([self.step('s'+str(i),critical=str(self.root/'exclusive')) for i in range(2)])['run_id'] for _ in range(2)]
        for run in runs:self.assertEqual(self.wait(run)['state'],'succeeded')

    def test_appended_steps_respect_existing_software_concurrency(self):
        environments.bind('scipy',command=[sys.executable,str(self.script)],path=self.home,concurrency=1)
        with patch.object(jobs,'start_worker'):
            run=self.submit([self.step('first',critical=str(self.root/'exclusive'))])['run_id']
            environments.bind('scipy',command=[sys.executable,str(self.script)],path=self.home,concurrency=2)
            jobs.submit([self.step('second',critical=str(self.root/'exclusive'))],run_id=run,path=self.home)
        jobs.start_worker(run,path=self.home)
        result=self.wait(run)
        self.assertEqual(result['state'],'succeeded',result)

    def test_append_and_resume_keep_completed_steps(self):
        r=self.submit([self.step('complete',value=3),{**self.step('retry',fail_once=str(self.root/'flag')),'after':['complete']},
                       {**self.step('dependent'),'after':['retry']}])['run_id']
        first=self.wait(r);self.assertEqual(first['state'],'failed')
        self.assertEqual(first['steps'][2]['state'],'blocked')
        jobs.resume(r,path=self.home);second=self.wait(r);self.assertEqual(second['state'],'succeeded',second)
        self.assertEqual(second['steps'][0]['attempt'],1)
        self.assertEqual(second['steps'][1]['attempt'],2)
        jobs.submit([{**self.step('append'),'bindings':{'value':{'step':'complete','path':['result','value']}}}],run_id=r,path=self.home)
        final=self.wait(r);self.assertEqual(final['state'],'succeeded',final)
        self.assertEqual(final['steps'][3]['result']['result']['value'],3)

    def test_cancel_terminates_native_process_tree(self):
        child=self.root/'child.txt'
        r=self.submit([self.step('slow',child=str(child))])['run_id']
        end=time.monotonic()+10
        while not child.exists() and time.monotonic()<end:time.sleep(.05)
        self.assertTrue(child.exists())
        jobs.cancel(r,path=self.home);self.assertEqual(self.wait(r)['state'],'cancelled')
        snapshot=child.read_bytes();time.sleep(.3);self.assertEqual(child.read_bytes(),snapshot)

    def test_resume_while_finished_worker_is_closing(self):
        with patch.object(jobs,'start_worker'):
            run=self.submit([self.step('retry',value=42)])['run_id']
            with jobs.worker_lock(self.home,run) as held:
                self.assertTrue(held)
                with jobs.database(self.home) as db:
                    db.execute("UPDATE runs SET state='running' WHERE id=?",(run,))
                with self.assertRaisesRegex(ValueError,'still executing'):
                    jobs.resume(run,path=self.home)
                with jobs.database(self.home) as db:
                    db.execute("UPDATE steps SET state='failed' WHERE run_id=?",(run,))
                    db.execute("UPDATE runs SET state='failed' WHERE id=?",(run,))
                self.assertTrue(jobs.resume(run,path=self.home)['resumed'])
        jobs.start_worker(run,path=self.home)
        result=self.wait(run)
        self.assertEqual(result['state'],'succeeded',result)
        self.assertEqual(result['steps'][0]['attempt'],2)
        self.assertEqual(result['steps'][0]['result']['result']['value'],42)

    def test_timeout_and_invalid_workflows(self):
        r=self.submit([{**self.step('slow',sleep=5),'timeout':.2}])['run_id']
        result=self.wait(r);self.assertEqual(result['state'],'failed')
        self.assertIn('exceeded',result['steps'][0]['error'])
        for invalid in ([{**self.step('cycle'),'after':['cycle']}],[{**self.step('missing'),'after':['none']}],[self.step('../outside')]):
            with self.assertRaises(ValueError):jobs.submit(invalid,path=self.home)
        self.assertFalse((self.root/'outside').exists())

    def test_cli_submission_outlives_its_process(self):
        env={**os.environ,'OPTICS_HOME':str(self.home),'PYTHONPATH':str(Path(__file__).resolve().parents[1]/'src')}
        process=subprocess.run([sys.executable,'-m','optics_photonics','submit','scipy','--inputs',json.dumps({'value':42,'sleep':.3})],env=env,capture_output=True,text=True,check=True)
        run=json.loads(process.stdout)['run_id'];self.runs.append(run)
        self.assertEqual(self.wait(run)['steps'][0]['result']['result']['value'],42)


if __name__=='__main__':unittest.main()
