"""Arrays keep their physical meaning from the program that writes them to the one that reads them."""
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from optics_photonics import arrays, data, environments, jobs
from test_arrays import npy
from support import workspace

ROOT = Path(__file__).resolve().parents[1]
SCIENCE = os.environ.get('OPTICS_SCIENCE_TESTS') == '1'


class ConversionCase(unittest.TestCase):
    def test_units_convert_within_a_kind_and_between_spectral_quantities(self):
        self.assertAlmostEqual(data.convert(1550.0, 'nm', 'um'), 1.55)
        self.assertAlmostEqual(data.convert(1550.0, 'nm', 'THz'), 299792.458 / 1550.0, places=9)
        self.assertAlmostEqual(data.convert(1.0, 'eV', 'nm'), 1239.841984, places=5)
        self.assertAlmostEqual(data.convert(10000.0, '1/cm', 'um'), 1.0)
        self.assertAlmostEqual(data.convert(193.414489, 'THz', 'rad/s'), 2 * math.pi * 193.414489e12, delta=1e3)
        self.assertAlmostEqual(data.convert(180.0, 'deg', 'rad'), math.pi)
        self.assertAlmostEqual(data.convert(1.0, 'arcsec', 'rad'), math.pi / 648000)
        self.assertEqual(data.convert(7, 'ps', 'ps'), 7)
        with self.assertRaisesRegex(ValueError, 'does not convert'):
            data.convert(1.0, 'nm', 'deg')
        with self.assertRaisesRegex(ValueError, 'Unknown unit'):
            data.convert(1.0, 'furlong', 'm')


class DescribedReadingCase(unittest.TestCase):
    """The connector reads descriptions and coordinates without NumPy."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.file = Path(self.temp.name) / 'device.npz'
        s = [complex(k, -k) for k in range(3 * 2 * 2)]
        with zipfile.ZipFile(self.file, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('S.npy', npy(s, '<c16', (3, 2, 2)))
            archive.writestr('wavelength.npy', npy([1500.0, 1550.0, 1600.0], '<f8', (3,)))
            archive.writestr('profile.npy', npy([float(k) for k in range(6)], '<f8', (6,)))
        ports = ['in', 'through']
        self.file.with_suffix('.json').write_text(json.dumps({'format': data.FORMAT, 'arrays': {
            'S': {'quantity': 'S-parameters', 'unit': '1', 'time_dependence': 'exp(-i omega t)', 'normalization': 'power waves',
                  'axes': ['wavelength', {'name': 'out', 'labels': ports}, {'name': 'in', 'labels': ports}]},
            'wavelength': {'quantity': 'vacuum wavelength', 'unit': 'nm'},
            'profile': {'quantity': 'intensity', 'unit': 'W/m^2', 'axes': [{'name': 'x', 'unit': 'um', 'start': -1.0, 'step': 0.5}]}}}))

    def tearDown(self):
        self.temp.cleanup()

    def test_a_selection_states_its_quantity_and_where_its_values_lie(self):
        part = arrays.read(self.file, member='S', index=[[0, 3, 2], 1, None])
        self.assertEqual(part['real'], [[2.0, 3.0], [10.0, 11.0]])
        self.assertEqual(part['description']['quantity'], 'S-parameters')
        self.assertEqual(part['description']['time_dependence'], 'exp(-i omega t)')
        self.assertEqual(part['axes'], [{'name': 'wavelength', 'unit': 'nm', 'values': [1500.0, 1600.0]},
                                        {'name': 'in', 'labels': ['in', 'through']}])
        self.assertEqual(part['at'], [{'name': 'out', 'value': 'through'}])
        uniform = arrays.read(self.file, member='profile', index=[[1, 6, 2]])
        self.assertEqual(uniform['axes'], [{'name': 'x', 'unit': 'um', 'values': [-0.5, 0.5, 1.5]}])
        self.assertNotIn('at', uniform)

    def test_a_descending_selection_returns_coordinates_in_the_same_order(self):
        part = arrays.read(self.file, member='S', index=[[None, None, -1], 0, 0])
        self.assertEqual(part['real'], [8.0, 4.0, 0.0])
        self.assertEqual(part['axes'], [{'name': 'wavelength', 'unit': 'nm', 'values': [1600.0, 1550.0, 1500.0]}])
        part = arrays.read(self.file, member='profile', index=[[4, 0, -2]])
        self.assertEqual((part['values'], part['axes'][0]['values']), ([4.0, 2.0], [1.0, 0.0]))
        self.assertEqual(arrays.read(self.file, member='S', index=[[2, 2], 0, 0])['axes'][0]['values'], [])

    def test_downsampled_values_keep_matching_coordinates(self):
        part = arrays.read(self.file, member='profile', max_elements=3)
        self.assertTrue(part['downsampled'])
        self.assertEqual(part['values'], [0.0, 2.0, 4.0])
        self.assertEqual(part['axes'][0]['values'], [-1.0, 0.0, 1.0])

    def test_listing_shows_quantity_unit_and_axis_names(self):
        listed = arrays.describe(self.file)['arrays']
        self.assertEqual(listed['S'], {'dtype': '<c16', 'shape': [3, 2, 2], 'quantity': 'S-parameters', 'unit': '1', 'axes': ['wavelength', 'out', 'in']})
        self.assertEqual(listed['wavelength']['unit'], 'nm')

    def test_arrays_without_a_description_or_with_a_wrong_one_still_read(self):
        description = self.file.with_suffix('.json')
        record = json.loads(description.read_text())
        record['arrays']['profile']['axes'] = ['missing']
        description.write_text(json.dumps(record))
        part = arrays.read(self.file, member='profile')
        self.assertEqual(part['values'], [0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertNotIn('axes', part)
        for text in ('{"format": "other"}', 'not json'):
            description.write_text(text)
            self.assertNotIn('description', arrays.read(self.file, member='profile'))
        description.unlink()
        self.assertEqual(set(arrays.describe(self.file)['arrays']['S']), {'dtype', 'shape'})


try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, 'NumPy is not installed')
class DescribedArraysCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.wavelength = np.linspace(450, 650, 5)
        self.field = np.exp(1j * np.outer(self.wavelength, np.arange(8)) / 100)

    def tearDown(self):
        self.temp.cleanup()

    def saved(self):
        return data.save(self.root / 'result', {
            'E': data.quantity(self.field, 'electric field', unit='V/m', time_dependence='exp(-i omega t)',
                               axes=['wavelength', {'name': 'x', 'unit': 'um', 'start': -1.0, 'step': 0.25}]),
            'opd': data.quantity(np.arange(8.0), 'optical path difference', unit='nm', wavefront='positive lags',
                                 axes=[{'name': 'x', 'unit': 'um', 'start': -1.0, 'step': 0.25}]),
            'wavelength': data.quantity(self.wavelength, 'vacuum wavelength', unit='nm')})

    def test_saved_arrays_load_with_axes_units_and_conventions(self):
        self.assertEqual(self.saved(), {'data': 'result.npz', 'description': 'result.json', 'arrays': ['E', 'opd', 'wavelength']})
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['result.json', 'result.npz'])
        for location in ('result', 'result.npz', 'result.json'):
            loaded = data.load(self.root / location)
            np.testing.assert_array_equal(loaded['E'].values, self.field)
        field = loaded['E']
        self.assertEqual(field.unit, 'V/m')
        np.testing.assert_allclose(field.axis('wavelength').to('um').values, self.wavelength / 1000)
        np.testing.assert_allclose(field.axis('wavelength').to('THz').values, 299792.458 / self.wavelength)
        np.testing.assert_allclose(field.axis('x').to('nm').values, -1000 + 250 * np.arange(8))
        self.assertEqual(field.axis('wavelength').to('um').description['converted_from'], {'unit': 'nm'})
        with self.assertRaisesRegex(ValueError, 'No axis named z; axes: wavelength, x'):
            field.axis('z')

    def test_conventions_convert_explicitly_and_keep_their_origin(self):
        self.saved()
        loaded = data.load(self.root / 'result.npz')
        same = loaded['E'].phasor('exp(-i omega t)')
        self.assertIs(same, loaded['E'])
        other = loaded['E'].phasor('exp(+i omega t)')
        np.testing.assert_array_equal(other.values, self.field.conj())
        self.assertEqual(other.description['converted_from'], {'time_dependence': 'exp(-i omega t)'})
        leading = loaded['opd'].wavefront('positive leads').to('m')
        np.testing.assert_allclose(leading.values, -np.arange(8.0) * 1e-9)
        self.assertEqual(leading.description['converted_from'], {'wavefront': 'positive lags', 'unit': 'nm'})
        with self.assertRaisesRegex(ValueError, 'does not state its time dependence'):
            loaded['wavelength'].phasor('exp(+i omega t)')
        with self.assertRaisesRegex(ValueError, 'does not state its wavefront sign'):
            loaded['E'].wavefront('positive leads')

    def test_spectral_conversion_updates_the_physical_quantity(self):
        wavelength = data.quantity([1550.0], 'vacuum wavelength', unit='nm')
        frequency = wavelength.to('THz')
        self.assertEqual(frequency.description['quantity'], 'frequency')
        self.assertEqual(frequency.description['converted_from'], {'quantity': 'vacuum wavelength', 'unit': 'nm'})
        self.assertEqual(frequency.to('eV').description['quantity'], 'photon energy')
        restored = frequency.to('um')
        self.assertEqual(restored.description['quantity'], 'vacuum wavelength')
        np.testing.assert_allclose(restored.values, [1.55])
        self.assertEqual(wavelength.to('um').description['quantity'], 'vacuum wavelength')

    def test_a_description_that_does_not_fit_is_refused_and_writes_nothing(self):
        for arrays_, message in (
                ({'E': data.quantity(self.field, axes=['wavelength'])}, 'one axis per dimension; the array has 2'),
                ({'E': data.quantity(self.field, axes=['wavelength', 'x'])}, 'one-dimensional array wavelength of length 5'),
                ({'E': data.quantity(self.field, axes=[{'name': 'w', 'labels': ['a']}, {'name': 'x', 'start': 0, 'step': 1}])}, 'needs 5 labels'),
                ({'E': data.quantity(self.field, axes=[{'name': 'w', 'start': 0}, {'name': 'x', 'start': 0, 'step': 1}])}, 'labels, or start and step'),
                ({'E': data.quantity(self.field, time_dependence='e^{jwt}')}, 'time_dependence is one of'),
                ({'E': data.quantity(self.field, wavefront='leads')}, 'wavefront is one of'),
                ({'E': data.quantity(np.array([object()]))}, 'numeric arrays')):
            with self.assertRaisesRegex(ValueError, message):
                data.save(self.root / 'refused', arrays_)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_the_connector_reads_what_a_program_saved(self):
        self.saved()
        part = arrays.read(self.root / 'result.npz', member='E', index=[2, [0, 8, 3]])
        self.assertEqual(part['at'], [{'name': 'wavelength', 'unit': 'nm', 'value': 550.0}])
        self.assertEqual(part['axes'], [{'name': 'x', 'unit': 'um', 'values': [-1.0, -0.25, 0.5]}])
        np.testing.assert_allclose(part['real'], self.field[2, 0:8:3].real)


@unittest.skipUnless(SCIENCE, 'Set OPTICS_SCIENCE_TESTS=1 in the scientific environment')
class ExchangeCase(unittest.TestCase):
    def test_a_pupil_written_by_hcipy_gives_the_same_image_in_poppy(self):
        steps = json.loads((ROOT / 'examples/exchange/steps.json').read_text())
        for step in steps:
            step['source'] = (ROOT / 'examples/exchange' / step.pop('program')).read_text()
        with workspace() as home:
            for tool in ('hcipy', 'poppy'):
                environments.bind(tool, python=sys.executable, path=home)
            run = jobs.submit(steps, path=home)['run_id']
            for _ in range(12):
                status = jobs.status(run, path=home, wait=25)
                if status['state'] not in ('queued', 'running'):
                    break
            self.assertEqual(status['state'], 'succeeded', status)
            pupil, image = (step['result']['result'] for step in status['steps'])
            read = jobs.read_array(run, 'pupil/attempt-1/pupil.npz', member='opd', index=[128, [0, 256, 64]], path=home)
            listed = jobs.files(run, prefix='image/', path=home)['files']
        # Units, axes and the sign of the path difference arrive with the array.
        self.assertEqual(read['description']['unit'], 'nm')
        self.assertEqual(read['description']['wavefront'], 'positive lags')
        self.assertEqual([axis['name'] for axis in read['axes']], ['x'])
        self.assertEqual(read['at'][0]['name'], 'y')
        psf = next(entry for entry in listed if entry['file'].endswith('psf.npz'))['array']['arrays']['psf']
        self.assertEqual((psf['quantity'], psf['axes']), ('point spread function', ['y', 'x']))
        # Zernike 2 (tilt along x, 100 nm RMS) moves the image by 4 sigma / D; 4 and 7 (25 nm RMS together) lower the peak.
        tilt, strehl = 4 * 100e-9 / 1.0, math.exp(-(2 * math.pi * math.hypot(20, 15) / 550) ** 2)
        for result in (pupil, image):
            self.assertAlmostEqual(result['centroid_rad'][0] / tilt, 1, delta=0.03)
            self.assertGreater(result['centroid_rad'][1], 0)
        self.assertAlmostEqual(image['centroid_rad'][0] / pupil['centroid_rad'][0], 1, delta=0.01)
        self.assertAlmostEqual(image['centroid_rad'][1] / pupil['centroid_rad'][1], 1, delta=0.05)
        self.assertAlmostEqual(image['strehl'], strehl, delta=0.003)
        self.assertAlmostEqual(pupil['strehl'], image['strehl'], delta=0.01)


if __name__ == '__main__':
    unittest.main()
