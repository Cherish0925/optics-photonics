# Optics-Photonics AI Lab 0.4.0

The repository now uses its independent environment name, Optics-Photonics-AI-Lab. Existing Python imports, CLI commands, plugin IDs and saved software bindings remain unchanged.

- Register research libraries and executable solvers outside the published catalogue. Bind their installed environments and use the same native programs, background jobs and result interfaces.
- Collect complete research episodes in native worker processes through Python, CLI or MCP. Programs define their environment and policy using the Gymnasium reset/step interface.
- Distribute disjoint episode IDs across workers while preserving the same seed for each episode. Existing CPU and per-software concurrency limits apply.
- Save ordered observations, actions, scalar rewards and termination information as JSON Lines, with typed NumPy arrays in separate files. Read results incrementally and retain completed records if a later episode fails.
- Include a runnable broadband dielectric-coating environment using TMM and Gymnasium, with explicit material assumptions and power-balance output.
- Update repository and installation links after the rename. Research OS and other generated host packages carry the same source and Skills.

IOP is not a dependency. Native solver installations and licenses remain associated with the computing host. Sampling is local worker parallelism; distributed learner coordination and solver-specific state restoration remain with the research program and learning framework.
