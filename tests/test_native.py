"""Exercise adapter ownership and transport with SDK doubles, without solver licenses."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from optics_photonics import native, environments, execution, jobs
from support import workspace


LUMAPI = '''from pathlib import Path
import json
class FDTD:
 def __init__(self, **options): self.options=options; self.path=None; self.value=0
 def load(self, path): self.value=json.loads(Path(path).read_text())["value"]
 def save(self, path):
  self.path=Path(path); self.path.write_text(json.dumps({"value":self.value}))
 def close(self):
  if self.path: self.path.with_suffix(".closed").write_text("closed")
 def run(self): self.value+=1
'''


class NativeTests(unittest.TestCase):
    def test_sdk_discovery_and_failed_binding_leave_configuration_unchanged(self):
        with workspace() as folder:
            root = Path(folder)
            sdk = root/'Lumerical'/'v260'/'api'/'python'
            sdk.mkdir(parents=True)
            (sdk/'lumapi.py').write_text(LUMAPI)
            found = native.discover([str(root)])['installations']
            self.assertTrue(any(row.get('sdk_path') == str(sdk.resolve()) for row in found))
            with patch.object(native.platform, 'system', return_value='Linux'):
                bound = native.bind('lumerical', python=sys.executable, sdk_path=str(sdk), path=root/'home')
                self.assertTrue(bound['sdk']['importable'])
                before = environments.read(root/'home')
                with self.assertRaises(ValueError): native.bind('lumerical', sdk_path=str(root/'missing'), path=root/'home')
                self.assertEqual(environments.read(root/'home'), before)

    def test_native_program_saves_copy_and_closes_after_success_and_failure(self):
        with workspace() as folder:
            root = Path(folder)
            (root/'lumapi.py').write_text(LUMAPI)
            original = root/'original.fsp'
            original.write_text('{"value": 3}')
            with patch.object(native.platform, 'system', return_value='Linux'):
                native.bind('lumerical', python=sys.executable, sdk_path=str(root), path=root/'home', threads=2)
            request = {'inputs': {'project': str(original)}, 'source': 'SESSION.run()\nRESULT={"value": MODEL.value, "threads":SESSION.options["serverArgs"]["threads"]}'}
            result = execution.run('lumerical', request, path=root/'home')
            out = Path(result['output'])
            self.assertEqual(result['record']['result'], {'value': 4, 'threads': '2'})
            self.assertEqual(json.loads(original.read_text())['value'], 3)
            self.assertEqual(json.loads((out/'model.fsp').read_text())['value'], 4)
            self.assertTrue((out/'model.closed').exists())
            failed = root/'failed'
            with self.assertRaisesRegex(RuntimeError, 'research failed'):
                execution.run('lumerical', {**request, 'source': 'raise ValueError("research failed")'}, output=failed, path=root/'home')
            self.assertTrue((failed/'model.closed').exists())
            self.assertEqual(json.loads(original.read_text())['value'], 3)

    def test_all_session_owners_release_after_program_error(self):
        for tool in ('comsol', 'opticstudio', 'cst'):
            with self.subTest(tool=tool), workspace() as folder:
                root = Path(folder)
                events = []
                save = lambda path: Path(path).write_text('working copy')
                model = SimpleNamespace(save=save, save_as=save)
                owner = SimpleNamespace(create=lambda name:model, connect=lambda **kw:model, new_mws=lambda:model,
                    remove=lambda obj:events.append('release'), disconnect=lambda:events.append('release'), close=lambda:events.append('release'))
                sdk = SimpleNamespace(start=lambda **kw:owner, ZOS=lambda **kw:owner, DesignEnvironment=lambda:owner)
                connection = {'adapter':tool, 'options':{}, 'threads':2}
                with patch.object(native.importlib, 'import_module', return_value=sdk):
                    with self.assertRaisesRegex(ValueError, 'study failure'):
                        with native.session(connection, {}, root) as ns:
                            self.assertTrue(ns['PROJECT_FILE'].exists())
                            raise ValueError('study failure')
                self.assertEqual(events, ['release'])

    def test_native_background_job_survives_client_exit(self):
        with workspace() as folder:
            root = Path(folder)
            (root/'lumapi.py').write_text(LUMAPI)
            connection = {'kind':'native','adapter':'lumerical','python':sys.executable,'sdk_path':str(root),
                'options':{'module':'lumapi','product':'FDTD','hide':True},'threads':1,'concurrency':1,'cwd':None}
            environments.save({'tools':{'lumerical':connection}},root/'home')
            program = root/'research.py'
            program.write_text('import time\ntime.sleep(.3)\nSESSION.run()\nRESULT={"value":MODEL.value}')
            client = subprocess.run([sys.executable,'-m','optics_photonics','submit','lumerical','--program',str(program)],
                env={**os.environ,'OPTICS_HOME':str(root/'home')}, capture_output=True,text=True,check=True)
            run_id = json.loads(client.stdout)['run_id']
            deadline = time.monotonic()+30
            while time.monotonic()<deadline:
                status=jobs.status(run_id,path=root/'home')
                if status['state'] in jobs.TERMINAL: break
                time.sleep(.05)
            self.assertEqual(status['state'],'succeeded',status)
            self.assertTrue(list((root/'home'/'runs'/run_id).rglob('model.closed')))
            # A worker releases its lock just before its log closes on Windows.
            for _ in range(50):
                with jobs.worker_lock(root/'home',run_id) as acquired:
                    if acquired: break
                time.sleep(.02)


if __name__ == '__main__': unittest.main()
