import json
import math
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from optics_photonics.operations import calculate, EXAMPLES
from optics_photonics.environments import bind
from optics_photonics.execution import run


@unittest.skipUnless(os.environ.get('OPTICS_SCIENCE_TESTS')=='1','Set OPTICS_SCIENCE_TESTS=1 in the scientific environment')
class ScienceTests(unittest.TestCase):
    def test_skills_have_readable_yaml_metadata(self):
        import yaml
        for path in (Path(__file__).resolve().parents[1]/'skills').glob('*/SKILL.md'):
            metadata=yaml.safe_load(path.read_text(encoding='utf-8').split('---',2)[1])
            self.assertEqual(metadata['name'],path.parent.name)
            self.assertIsInstance(metadata['description'],str)

    def test_all_packaged_calculations_execute_in_their_native_libraries(self):
        with tempfile.TemporaryDirectory() as tmp:
            for tool,(action,inputs) in EXAMPLES.items():
                with self.subTest(tool=tool):
                    result=calculate(tool,action,inputs,Path(tmp)/tool)
                    json.dumps(result,allow_nan=False)
                    if 'data' in result:self.assertTrue((Path(tmp)/tool/result['data']).is_file())

    def test_independent_film_solvers_agree_and_conserve_power(self):
        with tempfile.TemporaryDirectory() as tmp:
            for polarization in ('s','p'):
                for angle in (0,35):
                    a=calculate('tmm','spectrum',{'n':[1,1.45,1.52],'thickness_nm':[100],'wavelength_nm':[550],'angle_deg':angle,'polarization':polarization},tmp)
                    b=calculate('grcwa','film',{'epsilon':[1,1.45**2,1.52**2],'thickness_over_wavelength':[0,100/550,0],'angle_deg':angle,'polarization':polarization},tmp)
                    self.assertAlmostEqual(a['first'][1],b['R'],places=10)
                    self.assertAlmostEqual(b['R']+b['T'],1,places=10)

    def test_lossless_sphere_extinction_equals_scattering(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=calculate('miepython',*EXAMPLES['miepython'],tmp)
            self.assertAlmostEqual(a['first'][1],a['first'][2],places=12)

    def test_ray_matrix_and_exact_symbolic_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=calculate('raytracing',*EXAMPLES['raytracing'],tmp)
            b=calculate('sympy',*EXAMPLES['sympy'],tmp)
            self.assertAlmostEqual(a['ray_out'][0],-.001,places=12)
            self.assertAlmostEqual(a['matrix'][0][1],0,places=12)
            self.assertEqual(b['determinant'],'1')

    def test_two_level_rabi_population(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=calculate('qutip',*EXAMPLES['qutip'],tmp)
            self.assertAlmostEqual(a['maximum'],1,places=7)
            self.assertLess(abs(a['last']),1e-8)

    def test_native_program_keeps_full_api_and_result_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            bind('tmm',python=sys.executable,path=tmp)
            source='import tmm, numpy as np\nr=tmm.coh_tmm("s",[1,1.5],[np.inf,np.inf],0,550)\nnp.savetxt(OUTPUT_DIR/"R.csv",[r["R"]])\nRESULT={"R":float(r["R"]),"wavelength_nm":INPUTS["wavelength_nm"]}'
            a=run('tmm',{'source':source,'inputs':{'wavelength_nm':550}},path=tmp,timeout=30)['record']
            self.assertAlmostEqual(a['result']['R'],.04,places=12)
            self.assertIn('R.csv',a['files'])
            self.assertIn('tmm',a['environment']['versions'])
            self.assertIn('program.py',a['files'])


if __name__=='__main__':unittest.main()
