import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from optics_photonics import catalogue, environments, execution, operations
from optics_photonics.mcp import serve
from optics_photonics.packages import package, HOSTS


class ConnectionTests(unittest.TestCase):
    def test_tmm_recipe_includes_its_undeclared_numpy_dependency(self):
        record = catalogue.software('tmm')['connection']
        self.assertIn('numpy', record['pip'])
        self.assertIn('numpy', record['modules'])
        self.assertIn('numpy', record['distributions'])
        generated = Path(__file__).resolve().parents[1] / 'connect/agentic-research-os/lib/optics_photonics/resources/data/connections.json'
        self.assertEqual(json.loads(generated.read_text(encoding='utf-8'))['tmm'], record)

    def test_every_catalogued_tool_has_a_source_and_connection(self):
        entries = catalogue.catalogue()
        self.assertEqual({r['id'] for r in entries}, set(catalogue.connections()))
        for row in entries:
            record = catalogue.software(row['id'])['connection']
            self.assertTrue(record['sources'])
            self.assertIn(record['kind'], ('python','native','manual','data'))
            if record['pip']:
                self.assertTrue(record['modules'])
                self.assertTrue(record['distributions'])
            if record['operations']:
                self.assertIn(row['id'], operations.EXAMPLES)

    def test_catalogue_pagination_and_domain_selection(self):
        a = catalogue.search(domain='film',limit=2)
        b = catalogue.search(domain='film',offset=2,limit=100)
        self.assertEqual(len(a['items'])+len(b['items']),a['total'])
        self.assertEqual(set(x['id'] for x in a['items']) & set(x['id'] for x in b['items']),set())
        self.assertEqual(catalogue.search('tmm')['items'][0]['id'],'tmm')

    def test_search_uses_bilingual_domain_names_and_normalized_terms(self):
        for query in ('thin film','thin-film','ＴＨＩＮ　ＦＩＬＭ','薄膜'):
            items = catalogue.search(query,license_group='open',limit=100)['items']
            self.assertTrue({'tmm','grcwa'} <= {row['id'] for row in items},query)
        self.assertEqual(catalogue.search('py pol')['items'][0]['id'],'py-pol')

    def test_search_ranks_related_word_forms_and_reports_missing_words(self):
        def found(query, **options):
            return [(row['id'], row.get('missing')) for row in catalogue.search(query, limit=100, **options)['items']]
        # Plural, participle and joined forms of the catalogue's words.
        self.assertEqual(found('photonic crystal bands')[0], ('mpb', None))
        self.assertEqual(found('mie scattering sphere')[0], ('miepython', None))
        self.assertEqual({tool for tool, _ in found('xray beamline')}, {tool for tool, _ in found('x-ray beamline')})
        self.assertIn(('xrt', None), found('xray beamline'))
        # A word matches the start of a word: ring is not found inside scattering.
        self.assertNotIn('miepython', [tool for tool, _ in found('ring')])
        # Three or more words also return software one word short, after the full matches.
        ranked = found('mie scattering sphere')
        self.assertIn(('treams', ['sphere']), ranked)
        self.assertEqual([missing for _, missing in ranked], sorted((missing for _, missing in ranked), key=bool))
        # Two words must both match while some software has both.
        self.assertTrue(all(missing is None for _, missing in found('thin film')))
        self.assertEqual(found('zzzz film'), [(tool, ['zzzz']) for tool, _ in found('film')])
        self.assertEqual(found('zzzz yyyy'), [])
        self.assertEqual(len(found('')), len(catalogue.catalogue()))

    def test_mcp_initialization_and_tool_call(self):
        requests = [
            {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25'}},
            {'jsonrpc':'2.0','method':'notifications/initialized'},
            {'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'software_details','arguments':{'tool':'tmm'}}},
            {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'software_details','arguments':{'tool':'missing'}}},
            {'jsonrpc':'2.0','id':4,'method':'ping'}]
        out=io.StringIO();serve(io.StringIO('\n'.join(json.dumps(r) for r in requests)),out)
        # Tool calls complete independently; replies are matched by request ID.
        messages=sorted((json.loads(s) for s in out.getvalue().splitlines()),key=lambda m:m['id'])
        self.assertEqual([m['id'] for m in messages],[1,2,3,4])
        self.assertEqual(messages[1]['result']['structuredContent']['execution']['operations'][0]['name'],'spectrum')
        self.assertTrue(messages[2]['result']['isError'])
        self.assertEqual(messages[-1]['result'],{})

    def test_each_host_package_runs_without_scientific_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            for host in HOSTS:
                p=Path(tmp)/host
                package(p,host)
                result=subprocess.run([sys.executable,'-B',str(p/'server.py'),'search','tmm'],cwd=tmp,capture_output=True,text=True,check=True)
                self.assertEqual(json.loads(result.stdout)['items'][0]['id'],'tmm')
                self.assertEqual(len(list((p/'skills').glob('*/SKILL.md'))),2)
                with self.assertRaises(ValueError):package(p,host)
                if host=='deepseek':
                    overlay=json.loads((p/'optics.cordis.yml').read_text())
                    self.assertEqual(overlay[0]['insert'][0]['name'],'@deepseek-ai/dsh-mcp-client')
                if host=='codex':
                    self.assertEqual(json.loads((p/'.codex-plugin/plugin.json').read_text())['mcpServers'],'./.mcp.json')

    def test_package_versions_are_found_without_packages_distributions(self):
        # Python 3.9 lacks importlib.metadata.packages_distributions; the worker reads the same facts itself.
        from optics_photonics import worker
        with tempfile.TemporaryDirectory() as tmp:
            for name, module, files in (('listed-names', 'listed_module', {'top_level.txt': 'listed_module\n'}),
                                        ('recorded-files', 'recorded_module', {'RECORD': 'recorded_module/__init__.py,,\nrecorded_files-1.0.dist-info/METADATA,,\n'})):
                folder = Path(tmp) / (name.replace('-', '_') + '-1.0.dist-info')
                folder.mkdir()
                (folder / 'METADATA').write_text('Metadata-Version: 2.1\nName: ' + name + '\nVersion: 1.0\n')
                for file, text in files.items():
                    (folder / file).write_text(text)
                (Path(tmp) / module).mkdir()
                (Path(tmp) / module / '__init__.py').write_text('')
            sys.path.insert(0, tmp)
            try:
                found = worker.distributions(native=None)
            finally:
                sys.path.remove(tmp)
        self.assertEqual(found['listed_module'], ['listed-names'])
        self.assertEqual(found['recorded_module'], ['recorded-files'])

    def test_probe_keeps_virtual_environment_interpreter(self):
        # A venv interpreter may be a symlink to the base Python on Unix.
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([sys.executable,'-m','venv','--without-pip',tmp],check=True)
            executable=Path(tmp)/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
            result=environments.probe('tmm',executable)
            self.assertEqual(Path(result['prefix']).resolve(),Path(tmp).resolve())
            self.assertNotEqual(Path(result['prefix']).resolve(),Path(result['base_prefix']).resolve())
            self.assertEqual(Path(result['python']).parent.resolve(),executable.parent.resolve())

    def test_native_process_request_and_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            wrapper=Path(tmp)/'solver.py'
            wrapper.write_text('import json,os\nfrom pathlib import Path\np=json.loads(Path(os.environ["OPTICS_REQUEST_FILE"]).read_text())\nPath(os.environ["OPTICS_RESULT_FILE"]).write_text(json.dumps({"value":p["inputs"]["value"]*2}))\n')
            environments.bind('comsol',command=[sys.executable,str(wrapper)],path=Path(tmp)/'config')
            r=execution.run('comsol',{'inputs':{'value':21}},path=Path(tmp)/'config')
            self.assertEqual(r['record']['value'],42)
            with self.assertRaises(ValueError):execution.run('comsol',{},path=Path(tmp)/'config',output=r['output'])

    def test_concurrent_environment_registration_keeps_every_tool(self):
        with tempfile.TemporaryDirectory() as tmp:
            ids = ['tmm','grcwa','scipy','optiland','gdsfactory','py-pol']
            code = '''from optics_photonics.environments import bind, read
import sys
for i in range(20):
    bind(sys.argv[1],command=[sys.executable],path=sys.argv[2],threads=i+1)
    assert read(sys.argv[2])['tools'][sys.argv[1]]['threads']==i+1
'''
            workers = [subprocess.Popen([sys.executable, '-c', code, tool, tmp],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for tool in ids]
            try:
                outcomes = [(process, process.communicate(timeout=30)) for process in workers]
                for process, (_, error) in outcomes:
                    self.assertEqual(process.returncode, 0, error)
            finally:
                for process in workers:
                    if process.poll() is None:
                        process.kill(); process.communicate()
            configured = environments.read(tmp)['tools']
            self.assertEqual(set(configured), set(ids))
            self.assertTrue(all(item['threads'] == 20 for item in configured.values()))

    def test_concurrent_threads_keep_software_and_connections(self):
        from concurrent.futures import ThreadPoolExecutor
        with tempfile.TemporaryDirectory() as tmp:
            def add(index):
                tool = 'local-' + str(index)
                environments.register(tool, tool, 'Local command', kind='command', path=tmp)
                environments.bind(tool, command=[sys.executable], path=tmp)
                return environments.software(tool, path=tmp)
            with ThreadPoolExecutor(max_workers=8) as pool:
                definitions = list(pool.map(add, range(24)))
            configured = environments.read(tmp)
            self.assertEqual(set(configured['software']), {item['id'] for item in definitions})
            self.assertEqual(set(configured['tools']), set(configured['software']))

    def test_invalid_setup_does_not_change_connections(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):environments.bind('tmm',python=sys.executable,threads=0,path=tmp)
            self.assertFalse((Path(tmp)/'connections.json').exists())


if __name__=='__main__':unittest.main()
