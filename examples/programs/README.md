# Native research programs

These files run through `optics-photonics run TOOL --program FILE --inputs @INPUTS.json` or independent background `submit`. `INPUTS`, `OUTPUT_DIR` and `RESULT` are supplied by the connector. Every upstream API remains available.

- `thinfilm_optimization.py`: tmm + SciPy, constant-index single-layer coating. Install SciPy in the selected tmm interpreter before use. `thinfilm_inputs.json` provides a complete case. The local forward run found approximately 96.04 nm and 2.652% mean reflectance over 450–700 nm.
- `lumerical_session.py`: a persistent lumapi session for an existing model. Requires a licensed installation, its compatible Python environment, a real model and its object/monitor names. This example was not executed against licensed Lumerical here.

The program can construct geometry, run multiple solves and retain an upstream session for as long as required. Submit separate workflow steps for independent jobs. Save remote job IDs to OUTPUT_DIR as soon as they are assigned, and use provider-specific resume APIs when needed.
