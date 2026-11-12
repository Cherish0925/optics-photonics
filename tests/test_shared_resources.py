import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parent))
from optics_photonics import environments, jobs
from optics_photonics.signals import Wakeup, notify
from support import workspace


class ResourceCase(unittest.TestCase):
    def test_arbitrary_software_shares_a_license_pool_and_keeps_results_bounded(self):
        with workspace() as folder:
            root=Path(folder); home=root/'home'; solver=root/'solver.py'
            solver.write_text('''import os,json,time
from pathlib import Path
lock=Path(os.environ['LICENSE_PATH'])
with lock.open('x') as stream: stream.write('active')
time.sleep(.04)
lock.unlink()
Path(os.environ['OPTICS_RESULT_FILE']).write_text(json.dumps({'values':list(range(10000))}))
''')
            jobs.resources(cpu=4,pools={'shared-solver':1},path=home)
            for tool in ('solver-a','solver-b'):
                environments.register(tool,tool,'Research solver',kind='command',path=home)
                environments.bind(tool,command=[sys.executable,str(solver)],concurrency=4,
                    requirements={'shared-solver':1},env={'LICENSE_PATH':str(root/'license')},path=home)
            runs=[jobs.submit([{'id':str(i),'tool':tool} for i in range(4)],path=home)['run_id'] for tool in ('solver-a','solver-b')]
            for run in runs:
                result=jobs.status(run,path=home,wait=15,include_results=False)
                self.assertEqual(result['state'],'succeeded',result)
                self.assertLess(len(json.dumps(result)),2500)
                detailed=jobs.status(run,path=home)
                self.assertEqual(len(detailed['steps'][0]['result']['result']['values']),10000)
            with patch.object(environments,'probe',side_effect=AssertionError('Do not start an interpreter')):
                self.assertEqual(environments.page(path=home,limit=1)['next_offset'],1)
            # Give detached workers time to close inherited log handles on Windows.
            end=time.monotonic()+5
            while any(not worker_free(home, run) for run in runs) and time.monotonic()<end: time.sleep(.02)
            if os.name=='nt': time.sleep(.1)

    def test_notification_arriving_before_wait_is_not_lost(self):
        with tempfile.TemporaryDirectory() as home:
            with Wakeup(home) as wake:
                notify(home)
                start=time.monotonic();wake.wait(timeout=1)
                self.assertLess(time.monotonic()-start,.5)

    def test_long_dependency_chain_and_unknown_resource(self):
        steps=[{'id':str(i),'tool':'arbitrary','after':[str(i-1)] if i else []} for i in range(15000)]
        self.assertEqual(len(jobs.validate(steps)),15000)
        with self.assertRaises(ValueError): jobs.validate([{'id':'a','tool':'x','requirements':{'gpu':0}}])


def worker_free(home, run):
    with jobs.worker_lock(home,run) as available: return available
