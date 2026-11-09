# foundation

Use SymPy/Sage for symbolic derivation; SciPy for numerical optimization and integration; JAX/PyTorch for differentiated arrays; Gmsh/FreeCAD for geometry; refractiveindex.info for sourced optical constants. These tools support a physical model rather than determine it.

Make units, coordinate frames, complex dtype and array axes explicit at software interfaces. Record material provenance and interpolation domain. Preserve the assumptions of a symbolic simplification before substituting numeric values. Scaling and conditioning often matter more than optimizer choice. For automatic differentiation, compare a few directional derivatives with an independent numerical change when custom operations or discontinuous geometry are introduced. Record precision, solver version, model files and random seed with results; use HDF5/NPZ/FITS/GDS or CSV for the corresponding scientific data rather than flattening arrays into chat text.

Use software_details for the selected tool’s primary documentation and implementation links.
