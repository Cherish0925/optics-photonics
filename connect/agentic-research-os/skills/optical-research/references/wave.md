# wave

Represent a coherent field as complex amplitude E(x,y), with polarization components when needed. Fresnel, Fraunhofer and angular-spectrum propagation use different scale assumptions. LightPipes, POPPY, HCIPy, prysm, Diffractio and TorchOptics expose these operations. Choose vector propagation for high numerical aperture when scalar approximations fail.

Record wavelength, index, coordinate origin, pixel pitch, extent, Fourier sign and field normalization. Distinguish field 1/e radius from intensity 1/e² radius. Change pixel spacing and window size independently: a finer grid with unchanged extent does not resolve truncation. Preserve physical power when resampling; a sum of samples is not a spatial integral until pixel area is included. Use an analytic Gaussian or Airy pattern to locate scale errors, then evaluate aberrations and measured pupils.

Use software_details for the selected tool’s primary documentation and implementation links.
