import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parent))
from optics_photonics import environments, jobs, sampling
from support import remove


PROGRAM = '''import random
class Environment:
    def reset(self, *, seed, options):
        self.rng = random.Random(seed)
        self.value = self.rng.random()
        self.steps = 0
        return {'value': self.value}, {'seed': seed}
    def step(self, action):
        self.steps += 1
        self.value += action
        return {'value': self.value}, self.value, self.steps == 3, False, {}
    def close(self): pass
def make_env(): return Environment()
def make_policy(seed):
    rng = random.Random(seed + 1000)
    return lambda observation: rng.uniform(-1, 1)
'''


class SamplingCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.task = {'id': 'task', 'version': '1'}
        self.policy = {'id': 'policy', 'version': '2'}
        self.namespace = {}
        exec(PROGRAM, self.namespace)

    def tearDown(self):
        remove(self.temp)

    def collect(self, folder, **kwargs):
        return sampling.collect(self.namespace['make_env'], self.namespace['make_policy'],
            output=self.root/folder, task=self.task, policy=self.policy, **kwargs)

    def test_worker_partition_preserves_episode_seeds_actions_and_observations(self):
        self.collect('single', episodes=7, seed=42)
        for i in range(3): self.collect(str(i), episodes=7, start=i, stride=3, seed=42)
        def records(folders):
            rows = []
            for folder in folders:
                for row in sampling.records(self.root/folder):
                    row.pop('time', None); rows.append(row)
            return sorted(rows, key=lambda row: (row['episode_id'], {'episode':0,'transition':1,'episode_end':2}[row['type']], row.get('sequence', -1)))
        self.assertEqual(records(['single']), records(['0','1','2']))

    def test_sampling_limit_preserves_final_observation_and_truncation(self):
        result = self.collect('limited', episodes=1, max_steps=2)
        self.assertEqual(result['transitions'], 2)
        records = list(sampling.records(self.root/'limited'))
        self.assertFalse(records[-2]['terminated'])
        self.assertTrue(records[-2]['truncated'])
        self.assertEqual(records[-2]['info']['sampling_limit'], 2)
        self.assertAlmostEqual(records[-1]['return'], sum(r['reward'] for r in records if r['type'] == 'transition'))
        with self.assertRaises(FileExistsError): self.collect('limited')

    def test_arrays_keep_dtype_shape_and_do_not_alias_reused_buffers(self):
        try: import numpy as np
        except ImportError: self.skipTest('NumPy is an optional scientific dependency')
        class ArrayEnvironment:
            def reset(self, **kwargs):
                self.data = np.array([1, 2], dtype='float32')
                return self.data, {}
            def step(self, action):
                self.data[:] += action
                action[:] = 99
                return self.data, np.float32(2), np.bool_(False), np.bool_(False), {}
            def close(self): pass
        sampling.collect(ArrayEnvironment, lambda seed: lambda obs: np.array([2, 3], dtype='float32'),
            output=self.root/'arrays', task=self.task, policy=self.policy, max_steps=2)
        rows = list(sampling.records(self.root/'arrays', arrays=True))
        np.testing.assert_array_equal(rows[0]['observation'], [1, 2])
        np.testing.assert_array_equal(rows[1]['action'], [2, 3])
        np.testing.assert_array_equal(rows[1]['observation'], [3, 5])
        np.testing.assert_array_equal(rows[2]['observation'], [5, 8])
        self.assertEqual(rows[1]['action'].dtype, np.dtype('float32'))

    def test_failures_close_environment_keep_completed_records_and_do_not_fake_termination(self):
        closed = []
        class Environment:
            def reset(self, **kwargs): return 0, {}
            def step(self, action): raise RuntimeError('solver failed')
            def close(self): closed.append(True)
        with self.assertRaisesRegex(RuntimeError, 'solver failed'):
            sampling.collect(Environment, lambda seed: lambda obs: 1, output=self.root/'failed',
                             task=self.task, policy=self.policy)
        self.assertEqual(closed, [True])
        self.assertEqual([r['type'] for r in sampling.records(self.root/'failed')], ['episode'])
        with (self.root/'failed'/'trajectory.jsonl').open('a') as file: file.write('{"interrupted":')
        self.assertEqual(len(list(sampling.records(self.root/'failed'))), 1)

    def test_batch_uses_background_scheduler_and_survives_client_reconnection(self):
        # Worker execution uses Python itself; no optional solver dependency.
        home = self.root/'home'
        environments.register('research-model', 'Research model', 'A user-defined environment', modules=['random'], path=home)
        environments.bind('research-model', python=sys.executable, concurrency=2, path=home)
        jobs.resources(cpu=2, path=home)
        kwargs = dict(task=self.task, policy=self.policy, episodes=6, workers=3, max_steps=3, seed=91,
                      request_id='episodes', path=home)
        run = sampling.submit('research-model', PROGRAM, **kwargs)
        self.assertEqual(sampling.submit('research-model', PROGRAM, **kwargs), run)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            state = jobs.status(run['run_id'], path=home)
            if state['state'] in jobs.TERMINAL: break
            time.sleep(.05)
        self.assertEqual(state['state'], 'succeeded', state)
        self.assertEqual(sum(s['result']['result']['episodes'] for s in state['steps']), 6)
        self.assertEqual(sum(s['result']['result']['transitions'] for s in state['steps']), 18)
        paths = list((home/'runs'/run['run_id']).glob('*/attempt-*/samples/trajectory.jsonl'))
        ids = [r['episode_id'] for p in paths for r in sampling.records(p.parent) if r['type'] == 'episode']
        self.assertEqual(sorted(ids), list(range(6)))
        while time.monotonic() < deadline:
            with jobs.worker_lock(home, run['run_id']) as free:
                if free: break
            time.sleep(.05)

    def test_real_coating_environment_has_consistent_power_and_gym_spaces(self):
        import os
        if os.environ.get('OPTICS_SCIENCE_TESTS') != '1':
            self.skipTest('Enable scientific packages with OPTICS_SCIENCE_TESTS=1')
        from gymnasium.utils.env_checker import check_env
        namespace = {}
        source = Path(__file__).resolve().parents[1] / 'examples/learning/thin_film.py'
        exec(source.read_text(), namespace)
        check_env(namespace['make_env'](), skip_render_check=True)
        result = sampling.collect(namespace['make_env'], namespace['make_policy'],
            task={'id':'coating','version':'1'}, policy=self.policy, episodes=4, seed=41,
            output=self.root/'coating')
        self.assertEqual(result['transitions'], 48)
        rows = [r for r in sampling.records(self.root/'coating', arrays=True) if r['type']=='transition']
        self.assertLess(max(r['info']['energy_balance_error'] for r in rows), 1e-12)
        self.assertTrue(all(abs(r['reward'] + r['info']['mean_reflectance']) < 1e-14 for r in rows))
