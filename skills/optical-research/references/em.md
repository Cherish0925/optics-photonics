# em

Solve Maxwell's equations when wavelength-scale structure, polarization coupling, near fields or dispersive materials determine the observable. FDTD (Meep, Lumerical, Tidy3D, FDTDX), FEM (COMSOL, JCMsuite, FEniCSx, NGSolve) and integral/scattering approaches have different meshes and boundary assumptions.

Define geometry units, epsilon(omega), permeability, source spectrum, port modes and outgoing boundaries. Compare R+T+A against the correctly normalized input; interference monitors may require a reference calculation. Refine mesh and simulation duration separately; inspect PML distance/thickness and mode truncation. Save complex fields and reference planes, not only images. Gradients require a model whose material and geometry parameterization agree with the solver's derivative conventions. HPC thread, MPI and GPU requests belong to the executable launch and cluster allocation.

Use software_details for the selected tool’s primary documentation and implementation links.
