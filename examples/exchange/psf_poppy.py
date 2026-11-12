"""Image of a point source through a saved pupil (POPPY), with the Strehl ratio.

INPUTS: pupil (location of pupil.npz written by another program), pixel_arcsec, pixels.
The pupil file states its units and the sign of its path difference. POPPY takes
metres, metres per pixel, and a path difference that is positive where the
wavefront leads (a tilt rising toward +x moves the image toward -x); all three
are converted from the description.
"""
import numpy as np
import astropy.units as u
import poppy
from optics_photonics import data

pupil = data.load(INPUTS['pupil'])
opd = pupil['opd'].wavefront('positive leads').to('m')
x = opd.axis('x').to('m').values
stated = opd.description['wavelength']
wavelength = data.convert(stated['value'], stated['unit'], 'm')
sampling = float(x[1] - x[0])


def image(path_difference):
    system = poppy.OpticalSystem(npix=len(x), pupil_diameter=len(x) * sampling * u.m, oversample=1)
    system.add_pupil(poppy.ArrayOpticalElement(transmission=pupil['transmission'].values, opd=path_difference,
                                               pixelscale=sampling * u.m / u.pixel, name='saved pupil'))
    system.add_detector(pixelscale=INPUTS['pixel_arcsec'], fov_pixels=INPUTS['pixels'])
    return system.calc_psf(wavelength=wavelength)[0].data


aberrated, reference = image(opd.values), image(np.zeros_like(opd.values))
pixel = INPUTS['pixel_arcsec']
angle = (np.arange(INPUTS['pixels']) - (INPUTS['pixels'] - 1) / 2) * pixel
saved = data.save(OUTPUT_DIR / 'psf', {
    'psf': data.quantity(aberrated, 'point spread function', unit='1', normalization='sum over all angles = entrance power = 1',
                         axes=[{'name': 'y', 'unit': 'arcsec', 'start': float(angle[0]), 'step': pixel},
                               {'name': 'x', 'unit': 'arcsec', 'start': float(angle[0]), 'step': pixel}],
                         wavelength=stated),
})
total = aberrated.sum()
RESULT = {**saved, 'strehl': float(aberrated.max() / reference.max()),
          'centroid_rad': [float(data.convert((aberrated.sum(axis=0) * angle).sum() / total, 'arcsec', 'rad')),
                           float(data.convert((aberrated.sum(axis=1) * angle).sum() / total, 'arcsec', 'rad'))],
          'captured_power': float(total)}
