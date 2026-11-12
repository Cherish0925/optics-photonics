from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from optics_photonics import episodes, sampling
from test_sampling import PROGRAM

IOP_EXPORT = Path(__file__).with_name('data') / 'iop-episode.jsonl'


class EpisodeReadingCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        namespace = {}
        exec(PROGRAM, namespace)
        sampling.collect(namespace['make_env'], namespace['make_policy'], output=self.root / 'samples',
                         task={'id': 'task', 'version': '1'}, policy={'id': 'policy', 'version': '2'},
                         episodes=2, seed=5)

    def tearDown(self):
        self.temp.cleanup()

    def test_simulated_and_instrument_episodes_share_one_layout(self):
        found = list(episodes.read(self.root / 'samples', IOP_EXPORT, run_id='sim-run'))
        self.assertEqual([e['source'] for e in found], ['simulation', 'simulation', 'instrument'])
        self.assertEqual([e['episode_id'] for e in found], ['0', '1', 'sample-0'])
        self.assertEqual([e['run_id'] for e in found], ['sim-run', 'sim-run', 'run_example'])
        keys = {'source', 'run_id', 'step', 'attempt', 'episode_id', 'definition', 'task', 'policy', 'seed',
                'observation', 'info', 'transitions', 'complete', 'error'}
        step_keys = set(episodes.TRANSITION_FIELDS) | {'operation_ids'}
        for episode in found:
            self.assertEqual(set(episode), keys)
            self.assertTrue(episode['complete'])
            for i, step in enumerate(episode['transitions']):
                self.assertEqual(set(step), step_keys)
                self.assertEqual(step['sequence'], i)
        simulated, instrument = found[0], found[2]
        self.assertEqual(simulated['seed'], 5)
        self.assertEqual(len(simulated['transitions']), 3)
        self.assertEqual(simulated['transitions'][0]['operation_ids'], [])
        self.assertEqual(instrument['seed'], 19)
        self.assertEqual(instrument['observation']['angle_actual'], 0.0)
        self.assertEqual(len(instrument['transitions'][0]['operation_ids']), 1)

    def test_unscored_instrument_records_are_excluded_from_training_pairs(self):
        pairs = list(episodes.scored(episodes.read(IOP_EXPORT)))
        self.assertEqual([t['sequence'] for _, t in pairs], [1, 2])
        self.assertEqual(len(list(episodes.scored(episodes.read(self.root / 'samples')))), 6)

    def test_interrupted_episode_is_kept_only_on_request(self):
        file = self.root / 'samples' / 'trajectory.jsonl'
        lines = file.read_text(encoding='utf-8').splitlines(keepends=True)
        # Drop the second episode_end and leave a partial final line.
        file.write_text(''.join(lines[:-1]) + '{"type": "transi', encoding='utf-8')
        self.assertEqual(len(list(episodes.read(file))), 1)
        partial = list(episodes.read(file, complete=False))
        self.assertEqual(len(partial), 2)
        self.assertFalse(partial[1]['complete'])
        self.assertEqual(len(partial[1]['transitions']), 3)


if __name__ == '__main__':
    unittest.main()
