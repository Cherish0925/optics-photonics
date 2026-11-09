# imaging

Model the forward measurement before selecting inversion. PSF/OTF formation, sensor sampling, coherence and noise determine whether deconvolution, holographic reconstruction, ptychography or parameter fitting is appropriate. scikit-image, HoloPy, pyDHM, PtyPy and PyNX cover different parts of this chain.

Record pixel pitch, magnification, wavelength, pupil, axial coordinates, camera offset/gain and units. A normalized display image is not raw measurement data. Treat registration shift as the transform applied to moving data, including axis order. For inverse problems compare predictions in the measurement domain, identify nonunique parameters and use held-out observations where they distinguish models. Save solver settings, initialization and residuals. Synthetic recovery alone does not show that an experimental noise/model mismatch has been resolved.

Use software_details for the selected tool’s primary documentation and implementation links.
