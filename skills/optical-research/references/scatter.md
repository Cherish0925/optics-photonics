# scatter

Choose Mie theory for homogeneous spheres, T-matrices for appropriate particles and bases, DDA for discretized particles, or full-wave solvers for general structures. miepython, treams, SMUTHI, ADDA and pyGDM expose distinct representations.

Specify particle geometry, medium index, complex-index sign, polarization, illumination and cross-section normalization. A dimensionless efficiency Q needs its reference geometric area to become a cross section. Preserve the angular quadrature and phase function normalization when coupling to transport. Refine dipole spacing or multipole order. For passive lossless particles extinction and scattering should agree; absorption requires the solver's sign convention. Multiple scattering and substrate effects cannot in general be recreated by summing isolated-particle intensities.

Use software_details for the selected tool’s primary documentation and implementation links.
