# Data

Save arrays so that another program, or a later read, knows what they are.

**Write.** In a program, `from optics_photonics import data`, then:

```python
data.save(OUTPUT_DIR / 'device', {
    'S': data.quantity(S, 'S-parameters', unit='1', time_dependence='exp(-i omega t)', normalization='power waves',
                       axes=['wavelength', {'name': 'out', 'labels': ports}, {'name': 'in', 'labels': ports}]),
    'wavelength': data.quantity(wavelength, 'vacuum wavelength', unit='nm')})
```

This writes `device.npz` and `device.json`. An axis is the name of a one-dimensional array in the same file, `{name, unit, start, step}` for uniform sampling, or `{name, labels}` for ports, modes and channels. State what the next reader needs and nothing else:

| Data | State |
| --- | --- |
| Field | unit, axes, time dependence, wavelength or frequency, component, normalization |
| Spectrum | unit, spectral axis with its unit, angle and polarization, whether amplitude or power |
| S-parameters | time dependence, normalization, port labels in order, reference planes |
| Image | unit, pixel axes, normalization, wavelength |
| Path difference | unit, wavefront sign |
| Material data | source, version, conditions of validity |

Two conventions have fixed values because programs disagree about them. The time dependence of complex amplitudes is `exp(-i omega t)` or `exp(+i omega t)`. The wavefront sign of a path difference is `positive leads` (Wyant and Creath, Zemax, Code V, POPPY) or `positive lags` (an optical path length excess, as in Goodman and Born and Wolf). Other statements are free text or JSON.

**Read in another program.** Bind the file as an input, `{"pupil": {"step": "pupil", "file": "pupil.npz"}}`, then `arrays = data.load(INPUTS['pupil'])`. For an array `a`: `a.values` is the NumPy array, `a.to('m')` converts the unit, `a.axis('x')` gives the coordinates, `a.phasor('exp(+i omega t)')` conjugates when the stored time dependence differs, and `a.wavefront('positive leads')` negates when the stored sign differs. Each conversion is recorded in the description, and one that the description does not support is refused. `data.convert(1550, 'nm', 'THz')` converts lengths, angles and times, and converts vacuum wavelength, frequency, angular frequency, wavenumber and photon energy into one another.

**Read from the agent.** `result_files` shows the quantity, unit and axis names of each array. `read_array` returns the description, the coordinates and units of the values it returns (also after downsampling), and the position of every axis fixed by an integer index.

**Worked case.** `examples/exchange` passes an aberrated pupil from HCIPy to POPPY. The path difference is stored in nanometres with `positive lags`; POPPY takes metres with `positive leads`. With both conversions the two programs place the image on the same side and agree with the analytic tilt and Strehl ratio; without the sign conversion the image is mirrored.
