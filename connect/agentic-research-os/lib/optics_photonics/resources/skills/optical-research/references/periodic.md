# periodic

RCWA (S4, torcwa, grcwa), plane-wave eigensolvers (MPB), guided-mode expansion (legume) and time-domain Bloch simulations answer different questions. A periodic unit cell represents an infinite periodic structure unless a finite aperture is modeled separately.

Record lattice vectors, reciprocal-vector convention, Bloch wavevector, incidence angle, polarization and diffraction-order labels. Normalize frequency as a/lambda only when a is explicitly defined. For RCWA vary Fourier orders and material factorization; near grazing orders and resonances can need special treatment. For band diagrams preserve eigenvectors to track modes across crossings. A real band frequency does not by itself give radiative loss. Transfer complex transmission with phase and reference plane before using a unit-cell library for a finite metasurface.

Use software_details for the selected tool’s primary documentation and implementation links.
