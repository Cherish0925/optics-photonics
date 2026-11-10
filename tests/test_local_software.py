import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from optics_photonics import environments, execution, sampling
from optics_photonics.mcp import invoke


class LocalSoftwareCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.home = self.root/'home'

    def tearDown(self):
        self.temp.cleanup()

    def test_new_python_tool_uses_the_full_native_program_path(self):
        item = environments.register('custom-wave-model', 'Custom wave model',
            'Locally developed numerical model', modules=['math'], sources=['https://example.org/model'], path=self.home)
        environments.bind('custom-wave-model', python=sys.executable, path=self.home)
        result = execution.run('custom-wave-model', {'source': 'import math\nRESULT={"amplitude":math.cos(INPUTS["phase"])}',
            'inputs': {'phase': 0.0}}, path=self.home)
        self.assertEqual(result['record']['result']['amplitude'], 1)
        self.assertEqual(environments.software('custom-wave-model', path=self.home), item)
        self.assertEqual(environments.available(self.home)[0]['environment']['available'], True)
        self.assertEqual(environments.read(self.home)['tools']['custom-wave-model']['definition'], item)

    def test_new_executable_uses_the_existing_file_and_result_protocol(self):
        environments.register('compiled-solver', 'Compiled solver', 'External program', kind='command', path=self.home)
        source = self.root/'solver.py'
        source.write_text('import os,json\nfrom pathlib import Path\np=json.loads(Path(os.environ["OPTICS_REQUEST_FILE"]).read_text())\nPath(os.environ["OPTICS_RESULT_FILE"]).write_text(json.dumps({"answer":2*p["inputs"]["value"]}))\n')
        environments.bind('compiled-solver', command=[sys.executable, str(source)], path=self.home)
        result = execution.run('compiled-solver', {'inputs': {'value': 21}}, path=self.home)
        self.assertEqual(result['record']['answer'], 42)
        with self.assertRaisesRegex(ValueError, 'Python or native SDK'):
            sampling.submit('compiled-solver', 'pass', task={'id':'a','version':'1'}, policy={'id':'p','version':'1'},
                            episodes=1, path=self.home)

    def test_local_registration_does_not_replace_catalogue_or_other_homes(self):
        with self.assertRaisesRegex(ValueError, 'published catalogue'):
            environments.register('tmm', 'Replacement', 'Different tool', path=self.home)
        for tool in ('../tool', 'a/b', 'Upper Case'):
            with self.assertRaises(ValueError): environments.register(tool, 'Name', 'Description', path=self.home)
        with patch.dict('os.environ', {'OPTICS_HOME': str(self.home)}):
            invoke('register_software', {'tool':'lab-model','name':'Lab model','description':'Private research model','modules':['math']})
            self.assertEqual(invoke('registered_software', {})['software'][0]['id'], 'lab-model')
            self.assertEqual(invoke('software_details', {'tool':'lab-model'})['origin'], 'local')
        self.assertEqual(environments.registered(self.root/'other'), [])
        with self.assertRaises(ValueError): environments.software('lab-model', path=self.root/'other')
