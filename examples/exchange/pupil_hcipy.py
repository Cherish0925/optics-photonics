"""Aberrated circular pupil from Zernike coefficients (HCIPy), saved with units and conventions.

INPUTS: diameter_m, wavelength_nm, samples, zernike_rms_nm {Noll index: RMS in nm},
        pixels_per_lambda_over_d, radius_lambda_over_d.
Writes pupil.npz and pupil.json. RESULT also holds HCIPy's own Strehl ratio and
image centroid, so that a program reading the files can be compared with it.
"""
import numpy as np
import hcipy as hp
from optics_photonics import data

diameter, wavelength = INPUTS['diameter_m'], INPUTS['wavelength_nm'] * 1e-9
grid = hp.make_pupil_grid(INPUTS['samples'], diameter)
transmission = hp.evaluate_supersampled(hp.make_circular_aperture(diameter), grid, 4)
# Noll-ordered Zernike modes with unit RMS over the aperture; coefficients are RMS path differences.
# The pupil field below is transmission * exp(+2 pi i opd / wavelength) with time dependence
# exp(-i omega t), so a positive value is a longer optical path: that part of the wavefront lags.
coefficients = {int(index): rms for index, rms in INPUTS['zernike_rms_nm'].items()}
modes = hp.make_zernike_basis(max(coefficients), diameter, grid)
opd_nm = sum(rms * modes[index - 1] for index, rms in coefficients.items())

focal = hp.make_focal_grid(INPUTS['pixels_per_lambda_over_d'], INPUTS['radius_lambda_over_d'], spatial_resolution=wavelength / diameter)
propagate = hp.FraunhoferPropagator(grid, focal)
image = propagate(hp.Wavefront(transmission * np.exp(2j * np.pi * opd_nm * 1e-9 / wavelength), wavelength)).power
reference = propagate(hp.Wavefront(transmission, wavelength)).power

side = lambda field: np.asarray(field.shaped)
inside = transmission > 0.5
saved = data.save(OUTPUT_DIR / 'pupil', {
    'transmission': data.quantity(side(transmission), 'amplitude transmission', unit='1', axes=['y', 'x']),
    'opd': data.quantity(side(opd_nm), 'optical path difference', unit='nm', axes=['y', 'x'], wavefront='positive lags',
                         wavelength={'value': INPUTS['wavelength_nm'], 'unit': 'nm', 'medium': 'vacuum'}),
    'x': data.quantity(grid.separated_coords[0], 'pupil coordinate', unit='m'),
    'y': data.quantity(grid.separated_coords[1], 'pupil coordinate', unit='m'),
})
RESULT = {**saved, 'strehl': float(image.max() / reference.max()),
          'centroid_rad': [float((image * focal.x).sum() / image.sum()), float((image * focal.y).sum() / image.sum())],
          'rms_opd_nm': float(np.sqrt(np.mean(np.asarray(opd_nm)[inside] ** 2)))}
