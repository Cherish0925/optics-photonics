"""Arrays that carry their physical meaning between programs.

A program saves named arrays with ``save``; each array states what it is, its
unit, what its axes are, and the conventions needed to use it (time dependence
of complex amplitudes, sign of a path difference, normalization, reference
planes, port order, material source). ``FILE.npz`` holds the numbers and ``FILE.json`` the descriptions.
Another program reads both with ``load`` and converts units or conventions
explicitly; ``read_array`` returns the same description with the coordinates
of the values it returns.

    from optics_photonics import data
    data.save(OUTPUT_DIR / 'pupil', {
        'field': data.quantity(E, 'pupil field', unit='1', axes=['y', 'x'],
                               time_dependence='exp(-i omega t)',
                               wavelength={'value': 550, 'unit': 'nm'}),
        'x': data.quantity(x, 'pupil coordinate', unit='mm'),
        'y': data.quantity(y, 'pupil coordinate', unit='mm')})

    pupil = data.load(INPUTS['pupil'])
    x = pupil['field'].axis('x').to('m').values

An axis is the name of a one-dimensional array in the same file, or
``{'name', 'unit', 'start', 'step'}`` for uniform sampling, or
``{'name', 'labels'}`` for ports, modes and channels. Only ``save`` and
``load`` need NumPy; descriptions are read without it.
"""
import json
import math
import os
from pathlib import Path

FORMAT = 'optics-photonics/data/1'
TIME_DEPENDENCE = ('exp(-i omega t)', 'exp(+i omega t)')
WAVEFRONT = ('positive leads', 'positive lags')  # a longer optical path lags
C, H = 299792458.0, 6.62607015e-34

# Factors to the SI unit of each kind. Spectral kinds convert into one another through frequency.
UNITS = {
    'length': {'m': 1, 'cm': 1e-2, 'mm': 1e-3, 'um': 1e-6, 'µm': 1e-6, 'μm': 1e-6, 'nm': 1e-9, 'pm': 1e-12, 'angstrom': 1e-10, 'Å': 1e-10},
    'frequency': {'Hz': 1, 'kHz': 1e3, 'MHz': 1e6, 'GHz': 1e9, 'THz': 1e12, 'PHz': 1e15},
    'angular frequency': {'rad/s': 1},
    'wavenumber': {'1/m': 1, '1/cm': 1e2, 'cm^-1': 1e2, '1/um': 1e6},
    'energy': {'J': 1, 'eV': 1.602176634e-19, 'meV': 1.602176634e-22},
    'angle': {'rad': 1, 'mrad': 1e-3, 'deg': math.pi / 180, 'arcmin': math.pi / 10800, 'arcsec': math.pi / 648000},
    'time': {'s': 1, 'ms': 1e-3, 'us': 1e-6, 'µs': 1e-6, 'ns': 1e-9, 'ps': 1e-12, 'fs': 1e-15},
}
# Frequency in Hz from the SI value of a spectral kind, and back; a length is a vacuum wavelength.
SPECTRAL = {
    'frequency': (lambda v: v, lambda f: f),
    'length': (lambda v: C / v, lambda f: C / f),
    'angular frequency': (lambda v: v / (2 * math.pi), lambda f: 2 * math.pi * f),
    'wavenumber': (lambda v: C * v, lambda f: f / C),
    'energy': (lambda v: v / H, lambda f: H * f),
}


def kind(unit):
    for name, units in UNITS.items():
        if unit in units:
            return name
    known = ', '.join(unit for units in UNITS.values() for unit in units)
    raise ValueError(f'Unknown unit {unit!r}; convertible units: {known}')


def convert(values, unit, target):
    """Values in another unit of the same kind, or between spectral quantities.

    Wavelength (in vacuum), frequency, angular frequency, wavenumber 1/wavelength
    and photon energy convert into one another, element by element.
    """
    if unit == target:
        return values
    source, wanted = kind(unit), kind(target)
    value = values * UNITS[source][unit]
    if source != wanted:
        if source not in SPECTRAL or wanted not in SPECTRAL:
            raise ValueError(f'{unit} ({source}) does not convert to {target} ({wanted})')
        value = SPECTRAL[wanted][1](SPECTRAL[source][0](value))
    return value / UNITS[wanted][target]


class Quantity:
    """An array with its description; arithmetic is done on ``values``."""

    def __init__(self, values, description, siblings=None):
        self.values, self.description = values, description
        self._siblings = {} if siblings is None else siblings  # the file's arrays, shared while loading

    def __repr__(self):
        return f'Quantity({self.description.get("quantity")!r}, unit={self.description.get("unit")!r}, shape={getattr(self.values, "shape", ())})'

    @property
    def unit(self):
        return self.description.get('unit')

    def to(self, unit):
        """The same quantity in another unit; the description records the unit it came from."""
        if self.unit is None:
            raise ValueError('This array does not state its unit')
        if unit == self.unit:
            return self
        description = {**self.description, 'unit': unit, 'converted_from': {**self.description.get('converted_from', {}), 'unit': self.unit}}
        return Quantity(convert(self.values, self.unit, unit), description, self._siblings)

    def phasor(self, time_dependence):
        """Complex amplitudes under the given time dependence, conjugated when the stored one differs."""
        if time_dependence not in TIME_DEPENDENCE:
            raise ValueError('time_dependence is one of: ' + ', '.join(TIME_DEPENDENCE))
        stored = self.description.get('time_dependence')
        if stored not in TIME_DEPENDENCE:
            raise ValueError('This array does not state its time dependence: ' + ' or '.join(TIME_DEPENDENCE))
        if stored == time_dependence:
            return self
        description = {**self.description, 'time_dependence': time_dependence,
                       'converted_from': {**self.description.get('converted_from', {}), 'time_dependence': stored}}
        return Quantity(self.values.conjugate(), description, self._siblings)

    def wavefront(self, sign):
        """A path difference under the given sign, negated when the stored one differs.

        'positive leads' is the convention of Wyant and Creath, Zemax, Code V and
        POPPY; 'positive lags' is an optical path length excess, as in Goodman
        and Born and Wolf.
        """
        if sign not in WAVEFRONT:
            raise ValueError('wavefront is one of: ' + ', '.join(WAVEFRONT))
        stored = self.description.get('wavefront')
        if stored not in WAVEFRONT:
            raise ValueError('This array does not state its wavefront sign: ' + ' or '.join(WAVEFRONT))
        if stored == sign:
            return self
        description = {**self.description, 'wavefront': sign,
                       'converted_from': {**self.description.get('converted_from', {}), 'wavefront': stored}}
        return Quantity(-self.values, description, self._siblings)

    def axis(self, name):
        """Coordinates along a named axis as a Quantity; labels for a labelled axis."""
        import numpy as np
        for position, axis in enumerate(self.description.get('axes', [])):
            if isinstance(axis, str) and axis == name:
                if name not in self._siblings:
                    raise ValueError(f'The file has no coordinate array named {name}')
                return self._siblings[name]
            if isinstance(axis, dict) and axis.get('name') == name:
                if 'labels' in axis:
                    return list(axis['labels'])
                values = axis['start'] + axis['step'] * np.arange(self.values.shape[position])
                return Quantity(values, {'quantity': name, **({'unit': axis['unit']} if 'unit' in axis else {})})
        raise ValueError(f'No axis named {name}; axes: ' + ', '.join(axis_name(a) for a in self.description.get('axes', [])))


def quantity(values, quantity=None, *, unit=None, axes=None, **conventions):
    """Describe an array: what it is, its unit, its axes, and the conventions it follows."""
    import numpy as np
    description = {key: value for key, value in (('quantity', quantity), ('unit', unit), ('axes', axes)) if value is not None}
    return Quantity(np.asarray(values), {**description, **conventions})


def axis_name(axis):
    return axis if isinstance(axis, str) else str(axis.get('name'))


def check(name, item, arrays):
    """Reject a description that does not fit its array, saying what to change."""
    values, description = item.values, item.description
    if values.dtype.hasobject:
        raise ValueError(f'{name}: save numeric arrays, not Python objects')
    if not isinstance(description.get('unit', ''), str) or not isinstance(description.get('quantity', ''), str):
        raise ValueError(f'{name}: quantity and unit are text')
    for key, allowed in (('time_dependence', TIME_DEPENDENCE), ('wavefront', WAVEFRONT)):
        if description.get(key) is not None and description[key] not in allowed:
            raise ValueError(f'{name}: {key} is one of: ' + ', '.join(allowed))
    axes = description.get('axes')
    if axes is None:
        return
    if not isinstance(axes, list) or len(axes) != values.ndim:
        raise ValueError(f'{name}: give one axis per dimension; the array has {values.ndim}')
    for length, axis in zip(values.shape, axes):
        if isinstance(axis, str):
            other = arrays.get(axis)
            if other is None or other.values.ndim != 1 or other.values.shape[0] != length:
                raise ValueError(f'{name}: axis {axis} needs a one-dimensional array {axis} of length {length} in the same file')
        elif isinstance(axis, dict) and isinstance(axis.get('name'), str):
            if 'labels' in axis:
                if not isinstance(axis['labels'], list) or len(axis['labels']) != length:
                    raise ValueError(f'{name}: axis {axis["name"]} needs {length} labels')
            elif not all(isinstance(axis.get(key), (int, float)) and math.isfinite(axis[key]) for key in ('start', 'step')):
                raise ValueError(f'{name}: axis {axis["name"]} needs labels, or start and step')
        else:
            raise ValueError(f'{name}: an axis is an array name, or an object with name and labels or start and step')


def save(file, arrays):
    """Write named described arrays to FILE.npz and their descriptions to FILE.json.

    Returns the two file names. Both files appear complete or not at all.
    """
    import numpy as np
    file = Path(file)
    file = file.with_suffix('') if file.suffix in ('.npz', '.json') else file
    if not isinstance(arrays, dict) or not arrays:
        raise ValueError('Give a mapping from array name to data.quantity(...)')
    arrays = {str(name): item if isinstance(item, Quantity) else quantity(item) for name, item in arrays.items()}
    for name, item in arrays.items():
        check(name, item, arrays)
    record = {'format': FORMAT, 'arrays': {name: {'dtype': item.values.dtype.str, 'shape': list(item.values.shape), **item.description}
                                           for name, item in arrays.items()}}
    text = json.dumps(record, ensure_ascii=False, indent=1, allow_nan=False)
    numbers, description = file.with_name(file.name + '.npz'), file.with_name(file.name + '.json')
    partial = file.with_name(file.name + '.partial.npz')
    with partial.open('wb') as stream:
        np.savez_compressed(stream, **{name: item.values for name, item in arrays.items()})
    os.replace(partial, numbers)
    partial = file.with_name(file.name + '.partial.json')
    partial.write_text(text + '\n', encoding='utf-8')
    os.replace(partial, description)
    return {'data': numbers.name, 'description': description.name, 'arrays': list(arrays)}


def load(file):
    """Read FILE.npz with FILE.json: a mapping from array name to Quantity."""
    import numpy as np
    file = Path(file)
    numbers = file if file.suffix == '.npz' else file.with_suffix('.npz') if file.suffix == '.json' else file.with_name(file.name + '.npz')
    described = descriptions(numbers) or {}
    result = {}
    with np.load(numbers, allow_pickle=False) as archive:
        for name in archive.files:
            description = {key: value for key, value in described.get(name, {}).items() if key not in ('dtype', 'shape')}
            result[name] = Quantity(archive[name], description, result)
    return result


def descriptions(file):
    """Descriptions written beside an array file, by array name; None when there are none."""
    file = Path(file)
    try:
        record = json.loads(file.with_suffix('.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or record.get('format') != FORMAT or not isinstance(record.get('arrays'), dict):
        return None
    return record['arrays']


def summary(description):
    """The short form shown in file listings."""
    short = {key: description[key] for key in ('quantity', 'unit') if key in description}
    if 'axes' in description:
        short['axes'] = [axis_name(axis) for axis in description['axes']]
    return short


def located(description, described, selection, coordinates):
    """Where the selected values lie: coordinates of each kept axis, and the position of each dropped one.

    ``selection`` holds, per array axis, an index or [start, stop, step];
    ``coordinates(name, positions)`` reads those positions of a coordinate array.
    """
    axes, at = [], []
    for axis, chosen in zip(description.get('axes', []), selection):
        positions = range(*chosen) if isinstance(chosen, list) else [chosen]
        entry = {'name': axis_name(axis)}
        if isinstance(axis, str):
            if 'unit' in described.get(axis, {}):
                entry['unit'] = described[axis]['unit']
            values = coordinates(axis, chosen)
        elif 'labels' in axis:
            values = [axis['labels'][position] for position in positions]
        else:
            if 'unit' in axis:
                entry['unit'] = axis['unit']
            values = [float(format(axis['start'] + axis['step'] * position, '.12g')) for position in positions]
        if isinstance(chosen, list):
            axes.append({**entry, 'labels' if isinstance(axis, dict) and 'labels' in axis else 'values': values})
        else:
            at.append({**entry, 'value': values[0] if isinstance(values, list) else values})
    return axes, at
