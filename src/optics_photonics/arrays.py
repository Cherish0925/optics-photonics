"""Read parts of NPY and NPZ arrays without NumPy and without loading whole arrays.

The connector has no scientific dependencies, while solvers write fields,
spectra and S-parameters as NPY/NPZ. A selection reads only the bytes it
needs (compressed NPZ members are decompressed as a stream up to the last
selected element), so a large result can be inspected from any MCP host.
"""
import ast
import itertools
import math
import re
import struct
import zipfile
from pathlib import Path

MAGIC = b'\x93NUMPY'
LIMIT = 100_000
FORMATS = {('f', 2): 'e', ('f', 4): 'f', ('f', 8): 'd', ('i', 1): 'b', ('i', 2): 'h', ('i', 4): 'i', ('i', 8): 'q',
           ('u', 1): 'B', ('u', 2): 'H', ('u', 4): 'I', ('u', 8): 'Q', ('b', 1): '?', ('c', 8): 'ff', ('c', 16): 'dd'}


def header(stream):
    """Return (dtype, shape, fortran_order, data offset) of an NPY stream."""
    start = stream.read(8)
    if start[:6] != MAGIC:
        raise ValueError('Not an NPY array')
    try:
        size_format = '<H' if start[6] == 1 else '<I'
        length = struct.unpack(size_format, stream.read(struct.calcsize(size_format)))[0]
        text = stream.read(length)
        if len(text) < length:
            raise ValueError('short header')
        meta = ast.literal_eval(text.decode('utf-8' if start[6] >= 3 else 'latin1'))
        return meta['descr'], tuple(meta['shape']), bool(meta['fortran_order']), 8 + struct.calcsize(size_format) + length
    except (IndexError, KeyError, SyntaxError, TypeError, ValueError, struct.error):
        # A file that is still being written, or a damaged header.
        raise ValueError('The NPY header is incomplete or unreadable') from None


def element(descr):
    """struct format, item size and kind for a numeric NPY dtype such as '<f8' or '<c16'."""
    match = re.fullmatch(r'([<>|=])([a-zA-Z])(\d+)', descr) if isinstance(descr, str) else None
    code = FORMATS.get((match[2], int(match[3]))) if match else None
    if code is None:
        raise ValueError('read_array supports boolean, integer, real and complex arrays, not ' + repr(descr))
    return {'<': '<', '>': '>', '|': '<', '=': '='}[match[1]] + code, int(match[3]), match[2]


def npz(file):
    """Open an NPZ file; its arrays are readable once the archive directory is written."""
    try:
        return zipfile.ZipFile(file)
    except zipfile.BadZipFile:
        raise ValueError('The NPZ file is incomplete or not a ZIP archive') from None


def describe(file, member=None):
    """dtype and shape of an NPY file, or of every array in an NPZ file."""
    file = Path(file)
    if file.suffix == '.npz':
        with npz(file) as archive:
            names = [n for n in archive.namelist() if n.endswith('.npy')]
            if member is not None:
                names = [_member(archive, member)]
            result = {}
            for name in names[:50]:
                with archive.open(name) as stream:
                    descr, shape, _, _ = header(stream)
                result[name[:-4]] = {'dtype': descr, 'shape': list(shape)}
            return {'arrays': result, 'count': len(names)}
    with file.open('rb') as stream:
        descr, shape, _, _ = header(stream)
    return {'dtype': descr, 'shape': list(shape)}


def _member(archive, member):
    names = [n for n in archive.namelist() if n.endswith('.npy')]
    if member is None:
        if len(names) != 1:
            raise ValueError('Name one array of this NPZ file: ' + ', '.join(n[:-4] for n in names[:50]))
        return names[0]
    name = member if member.endswith('.npy') else member + '.npy'
    if name not in names:
        raise ValueError('Unknown array in NPZ file: ' + str(member))
    return name


def selection(shape, index):
    """Normalize an index list: an integer selects one position and drops that axis;
    [start, stop] or [start, stop, step] keeps it, with Python slice meaning."""
    index = list(index or [])
    if len(index) > len(shape):
        raise ValueError(f'The array has {len(shape)} axes')
    axes = []
    for n, item in itertools.zip_longest(shape, index):
        if item is None:
            axes.append([0, n, 1, True])
        elif type(item) is int:
            position = item + n if item < 0 else item
            if not 0 <= position < n:
                raise ValueError(f'Index {item} is outside an axis of length {n}')
            axes.append([position, position + 1, 1, False])
        elif isinstance(item, list) and 1 <= len(item) <= 3 and all(v is None or type(v) is int for v in item):
            start, stop, step = (item + [None, None])[:3]
            if step is not None and step < 1:
                raise ValueError('Use a positive step')
            start, stop, step = slice(start, stop, step).indices(n)
            axes.append([start, max(start, stop), step, True])
        else:
            raise ValueError('Each index is an integer or [start, stop, step]')
    return axes


def thin(axes, limit):
    """Keep at most c elements per axis, with the largest c whose selection fits the limit.

    Axes longer than c get a uniform step; shorter ones (ports, components,
    channels) stay whole, and a square grid keeps equal steps.
    """
    lengths = [len(range(a, b, s)) for a, b, s, _ in axes]
    if math.prod(lengths) <= limit:
        return False
    low, high = 1, max(lengths)
    while low < high:
        cap = (low + high + 1) // 2
        if math.prod(min(n, cap) for n in lengths) <= limit: low = cap
        else: high = cap - 1
    for axis, n in zip(axes, lengths):
        if n > low: axis[2] *= math.ceil(n / low)
    return True


def read(file, *, member=None, index=None, max_elements=10_000):
    """Read a selection of an NPY array or NPZ member as JSON-compatible values.

    Values beyond max_elements (at most 100000) are thinned by uniform steps on
    the longest selected axes; the returned selection states the steps used.
    Complex arrays return real and imag; non-finite numbers are 'nan', 'inf'
    or '-inf'.
    """
    if type(max_elements) is not int or not 1 <= max_elements <= LIMIT:
        raise ValueError(f'max_elements must be between 1 and {LIMIT}')
    file = Path(file)
    try:
        if file.suffix == '.npz':
            with npz(file) as archive:
                name = _member(archive, member)
                size = archive.getinfo(name).file_size
                with archive.open(name) as stream:
                    return {'member': name[:-4], **_read(stream, size, index, max_elements)}
        if member is not None:
            raise ValueError('member applies to NPZ files')
        with file.open('rb') as stream:
            return _read(stream, file.stat().st_size, index, max_elements)
    except (struct.error, zipfile.BadZipFile, EOFError):
        raise ValueError('The array data ended before the selected values') from None


def _read(stream, size, index, max_elements):
    descr, shape, fortran, offset = header(stream)
    code, itemsize, kind = element(descr)
    total = math.prod(shape) * itemsize
    if size - offset < total:
        raise ValueError(f'The array is incomplete: {size - offset} of {total} data bytes are present')
    axes = selection(shape, index)
    thinned = thin(axes, max_elements)
    strides = [itemsize] * len(shape)
    order = range(len(shape) - 2, -1, -1) if not fortran else range(1, len(shape))
    for k in order:
        strides[k] = strides[k + 1] * shape[k + 1] if not fortran else strides[k - 1] * shape[k - 1]
    ranges = [range(a, b, s) for a, b, s, _ in axes]
    kept = [k for k, a in enumerate(axes) if a[3]]
    result_shape = [len(ranges[k]) for k in kept]
    width = 2 if kind == 'c' else 1
    flat = [None] * (math.prod(result_shape) * width)
    # Visit elements in storage order so compressed members stream forward.
    fast = len(shape) - 1 if not fortran else 0
    outer = list(range(len(shape) - 1)) if not fortran else list(reversed(range(1, len(shape))))
    unit = struct.Struct(code)
    if shape and all(len(r) for r in ranges):
        for combination in itertools.product(*(ranges[k] for k in outer)):
            where = dict(zip(outer, combination))
            base = offset + sum(where[k] * strides[k] for k in outer)
            span = ranges[fast]
            if span.step <= 16:  # one read covers the span along the contiguous axis
                stream.seek(base + span.start * itemsize)
                data = stream.read((span[-1] - span.start + 1) * itemsize)
                values = [unit.unpack_from(data, (i - span.start) * itemsize) for i in span]
            else:
                values = []
                for i in span:
                    stream.seek(base + i * itemsize); values.append(unit.unpack(stream.read(itemsize)))
            for i, value in zip(span, values):
                where[fast] = i
                linear = 0
                for k in kept:
                    linear = linear * len(ranges[k]) + ranges[k].index(where[k])
                flat[linear * width:(linear + 1) * width] = value
    elif not shape:
        stream.seek(offset)
        flat = list(unit.unpack(stream.read(itemsize)))
    result = {'dtype': descr, 'shape': list(shape), 'selection': [[a, b, s] if keep else a for a, b, s, keep in axes],
              'result_shape': result_shape, 'downsampled': thinned}
    if kind == 'c':
        result['real'] = nest([plain(v) for v in flat[0::2]], result_shape)
        result['imag'] = nest([plain(v) for v in flat[1::2]], result_shape)
    else:
        result['values'] = nest([plain(v) for v in flat], result_shape)
    return result


def plain(value):
    if isinstance(value, float) and not math.isfinite(value):
        return 'nan' if value != value else ('inf' if value > 0 else '-inf')
    return value


def nest(values, shape):
    """Nested lists in C order; also handles axes of length zero."""
    if not shape:
        return values[0]
    if len(shape) == 1:
        return values
    size = math.prod(shape[1:])
    return [nest(values[i * size:(i + 1) * size], shape[1:]) for i in range(shape[0])]
