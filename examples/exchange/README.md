# A pupil passed between two programs

`pupil_hcipy.py` builds an aberrated circular pupil from Zernike coefficients and saves it with `data.save`. `psf_poppy.py` receives the file, converts what POPPY needs, and computes the image and its Strehl ratio. `steps.json` holds every parameter and the binding between the two steps.

```sh
optics-photonics bind hcipy --python /path/to/python
optics-photonics bind poppy --python /path/to/python
optics-photonics submit-workflow examples/exchange/steps.json
optics-photonics status RUN_ID
optics-photonics array RUN_ID image/attempt-1/psf.npz --member psf --index "[128, [96, 160, 8]]"
```

The pupil file states that the path difference is in nanometres and positive where the wavefront lags. POPPY takes metres, positive where the wavefront leads, so `psf_poppy.py` calls `.wavefront('positive leads').to('m')`. Both programs then report the same image shift, 3.9e-7 rad along x for a 100 nm RMS tilt on a 1 m aperture (4σ/D = 4.0e-7 rad), and POPPY's Strehl ratio 0.9225 matches exp(-(2πσ/λ)²) = 0.9217 for the 25 nm RMS of defocus and coma. Leaving out the sign conversion mirrors the image. Run with HCIPy 0.7.1 and POPPY 1.2.0; `tests/test_data.py` repeats it when `OPTICS_SCIENCE_TESTS=1`.

Replace either program to change the software: any writer that saves `transmission`, `opd`, `x` and `y` with their descriptions can feed `psf_poppy.py`, and any reader of the file can replace it.
