import itertools
import json
import os
from pathlib import Path
import random
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from optics_photonics import arrays, jobs
from optics_photonics.mcp import invoke


def npy(values, descr, shape, fortran=False):
    """NPY bytes written without NumPy; values are in C order."""
    header = repr({'descr': descr, 'fortran_order': fortran, 'shape': tuple(shape)})
    header += ' ' * (63 - (10 + len(header)) % 64) + '\n'
    code, size, kind = arrays.element(descr)
    if fortran:
        positions = list(itertools.product(*(range(n) for n in shape)))
        order = sorted(range(len(positions)), key=lambda i: positions[i][::-1])
        values = [values[i] for i in order]
    flat = [part for v in values for part in ((v.real, v.imag) if kind == 'c' else (v,))]
    return b'\x93NUMPY\x01\x00' + struct.pack('<H', len(header)) + header.encode('latin1') + \
        struct.pack(code[0] + code[1:] * len(values), *flat)


class ArrayReadingCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_selection_matches_python_indexing_in_both_storage_orders(self):
        shape = (3, 4, 5)
        values = [float(i) for i in range(60)]
        nested = [[[values[(i * 4 + j) * 5 + k] for k in range(5)] for j in range(4)] for i in range(3)]
        rng = random.Random(3)
        for fortran in (False, True):
            file = self.root / f'a{int(fortran)}.npy'
            file.write_bytes(npy(values, '<f8', shape, fortran))
            for _ in range(200):
                index = []
                for n in shape[:rng.randint(0, 3)]:
                    if rng.random() < .3:
                        index.append(rng.randrange(-n, n))
                    else:
                        index.append([rng.choice([None, 0, 1, -2]), rng.choice([None, n, -1, 2]), rng.choice([None, 1, 2, 3])])
                expected = nested
                def take(value, items):
                    if not items: return value
                    item, rest = items[0], items[1:]
                    if type(item) is int: return take(value[item], rest)
                    return [take(v, rest) for v in value[slice(*item)]]
                index_full = index + [[None, None, None]] * (3 - len(index))
                self.assertEqual(arrays.read(file, index=index, max_elements=1000)['values'], take(expected, index_full),
                                 (fortran, index))

    def test_types_complex_nonfinite_scalar_and_empty_axes(self):
        (self.root / 'c.npy').write_bytes(npy([1 + 2j, -3j], '<c16', (2,)))
        self.assertEqual(arrays.read(self.root / 'c.npy'), {'dtype': '<c16', 'shape': [2], 'selection': [[0, 2, 1]],
                         'result_shape': [2], 'downsampled': False, 'real': [1.0, 0.0], 'imag': [2.0, -3.0]})
        (self.root / 'f.npy').write_bytes(npy([1.0, float('nan'), float('inf'), -float('inf')], '>f4', (4,)))
        self.assertEqual(arrays.read(self.root / 'f.npy')['values'], [1.0, 'nan', 'inf', '-inf'])
        (self.root / 'i.npy').write_bytes(npy([7], '<i8', ()))
        self.assertEqual(arrays.read(self.root / 'i.npy')['values'], 7)
        (self.root / 'b.npy').write_bytes(npy([True, False, True], '|b1', (3,)))
        self.assertEqual(arrays.read(self.root / 'b.npy', index=[1])['values'], False)
        (self.root / 'e.npy').write_bytes(npy([], '<f8', (0, 3)))
        self.assertEqual(arrays.read(self.root / 'e.npy')['values'], [])
        (self.root / 's.npy').write_bytes(npy([1.0] * 6, '<f8', (2, 3)))
        self.assertEqual(arrays.read(self.root / 's.npy', index=[[0, 2], [1, 1]])['values'], [[], []])
        with self.assertRaises(ValueError):
            arrays.read(self.root / 's.npy', index=[0, 0, 0])

    def test_large_selection_is_thinned_and_incomplete_data_is_reported(self):
        values = [float(i) for i in range(200 * 300)]
        data = npy(values, '<f8', (200, 300))
        (self.root / 'big.npy').write_bytes(data)
        result = arrays.read(self.root / 'big.npy', max_elements=1000)
        self.assertTrue(result['downsampled'])
        self.assertLessEqual(len(result['values']) * len(result['values'][0]), 1000)
        (start0, _, step0), (start1, _, step1) = result['selection']
        self.assertEqual(result['values'][1][1], values[(start0 + step0) * 300 + start1 + step1])
        self.assertEqual(result['result_shape'], [29, 30])  # at most 31 per axis: 31 * 31 <= 1000
        # A short axis such as ports or field components stays whole.
        (self.root / 'ports.npy').write_bytes(npy(values[:4000], '<f8', (1000, 2, 2)))
        ports = arrays.read(self.root / 'ports.npy', max_elements=1000)
        self.assertEqual((ports['selection'], ports['result_shape']), ([[0, 1000, 4], [0, 2, 1], [0, 2, 1]], [250, 2, 2]))
        self.assertEqual(ports['values'][1], [[16.0, 17.0], [18.0, 19.0]])
        (self.root / 'part.npy').write_bytes(data[:len(data) // 2])
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            arrays.read(self.root / 'part.npy')
        self.assertEqual(arrays.describe(self.root / 'part.npy'), {'dtype': '<f8', 'shape': [200, 300]})

    def test_files_still_being_written_and_unsupported_types_are_reported(self):
        data = npy([1.0, 2.0], '<f8', (2,))
        for length in (0, 4, 6, 9, 30):
            (self.root / 'partial.npy').write_bytes(data[:length])
            for function in (arrays.describe, arrays.read):
                with self.assertRaises(ValueError):
                    function(self.root / 'partial.npy')
        for descr in ('<U5', '|O', '<M8[ns]', [('x', '<f8')]):
            header = repr({'descr': descr, 'fortran_order': False, 'shape': (1,)}) + '\n'
            (self.root / 'other.npy').write_bytes(b'\x93NUMPY\x01\x00' + struct.pack('<H', len(header)) + header.encode() + b'\0' * 64)
            self.assertEqual(arrays.describe(self.root / 'other.npy')['shape'], [1])
            with self.assertRaisesRegex(ValueError, 'supports boolean, integer, real and complex'):
                arrays.read(self.root / 'other.npy')
        with zipfile.ZipFile(self.root / 'whole.npz', 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('field.npy', npy([float(i) for i in range(4000)], '<f8', (4000,)))
        whole = (self.root / 'whole.npz').read_bytes()
        (self.root / 'partial.npz').write_bytes(whole[:len(whole) // 2])
        for function in (arrays.describe, arrays.read):
            with self.assertRaisesRegex(ValueError, 'NPZ file is incomplete'):
                function(self.root / 'partial.npz')

    def test_compressed_npz_members(self):
        with zipfile.ZipFile(self.root / 'r.npz', 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('field.npy', npy([float(i) for i in range(12)], '<f8', (3, 4)))
            archive.writestr('trace.npy', npy([1j, 2.0], '<c8', (2,)))
        self.assertEqual(arrays.describe(self.root / 'r.npz')['arrays'],
                         {'field': {'dtype': '<f8', 'shape': [3, 4]}, 'trace': {'dtype': '<c8', 'shape': [2]}})
        self.assertEqual(arrays.read(self.root / 'r.npz', member='field', index=[[1, 3], 2])['values'], [6.0, 10.0])
        with self.assertRaisesRegex(ValueError, 'field, trace'):
            arrays.read(self.root / 'r.npz')

    def test_numpy_written_arrays_match_numpy_indexing(self):
        try:
            import numpy as np
        except ImportError:
            self.skipTest('NumPy is an optional scientific dependency')
        rng = np.random.default_rng(0)
        for dtype in ('<f8', '>f4', '<f2', '<i2', '>i8', '|u1', '<c8', '<c16'):
            data = rng.normal(size=(4, 5, 6)) + (1j * rng.normal(size=(4, 5, 6)) if dtype[1] == 'c' else 0)
            for order in ('C', 'F'):
                array = np.asarray(data.astype(dtype), order=order)
                np.save(self.root / 'a.npy', array)
                for index in ([1, [None, None, 2]], [[1, None], -1], [[None, None, 3], [1, 4], [0, 6, 5]]):
                    got = arrays.read(self.root / 'a.npy', index=index)
                    expected = array[tuple(i if type(i) is int else slice(*i) for i in index)]
                    if dtype[1] == 'c':
                        self.assertTrue(np.array_equal(np.array(got['real']) + 1j * np.array(got['imag']), expected))
                    else:
                        self.assertTrue(np.array_equal(np.array(got['values'], dtype=expected.dtype), expected))


class RunArrayCase(unittest.TestCase):
    def test_listing_by_prefix_and_reading_through_mcp(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            run = home / 'runs' / 'study'
            for step in ('solve', 'sweep'):
                (run / step / 'attempt-1').mkdir(parents=True)
                (run / step / 'attempt-1' / 'log.txt').write_text(step)
            (run / 'solve' / 'attempt-1' / 'field.npy').write_bytes(npy([0.5, 1.5, 2.5, 3.5], '<f8', (2, 2)))
            (run / 'solve' / 'attempt-1' / 'writing.npy').write_bytes(b'\x93NUMPY\x01')
            (run / 'solve' / 'attempt-1' / 'writing.npz').write_bytes(b'PK\x03\x04')
            listing = jobs.files('study', path=home, prefix='solve/')
            self.assertEqual([f['file'] for f in listing['files']], ['solve/attempt-1/field.npy', 'solve/attempt-1/log.txt',
                             'solve/attempt-1/writing.npy', 'solve/attempt-1/writing.npz'])
            self.assertEqual(listing['files'][0]['array'], {'dtype': '<f8', 'shape': [2, 2]})
            self.assertTrue(all('array' not in f for f in listing['files'][1:]))
            self.assertEqual(jobs.files('study', path=home, prefix='sweep/attempt-1/l')['total'], 1)
            with self.assertRaises(ValueError):
                jobs.files('study', path=home, prefix='../..')
            with patch.dict(os.environ, {'OPTICS_HOME': str(home)}):
                result = invoke('read_array', {'run_id': 'study', 'file': 'solve/attempt-1/field.npy', 'index': [[None, None], 1]})
                same = invoke('read_array', {'run_id': 'study', 'file': 'solve/attempt-1/field.npy', 'index': [None, 1]})
            self.assertEqual(result['values'], [1.5, 3.5])
            self.assertEqual(same, result)
            json.dumps(result, allow_nan=False)


if __name__ == '__main__':
    unittest.main()
