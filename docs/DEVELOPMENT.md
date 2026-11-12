# Optical research environment: development handoff

[中文](DEVELOPMENT.zh-CN.md) · [Contributing](../CONTRIBUTING.md) · [Execution](EXECUTION.md)

The objective is to let researchers and agents connect real computing environments, run complete optical research programs, combine software and retain scientific results that can be interpreted and reused. Optics-Photonics-AI-Lab installs, runs and releases independently.

## Current implementation · 0.7.0

The 0.6.0 integration and the subsequent `data-descriptions` and `host-launch` contributions are integrated. Subsequent work starts from these capabilities:

| Work | Implemented | Remaining |
| --- | --- | --- |
| OP-01 / OP-02 | Concurrent MCP requests, separately cancellable waits, incremental dependency scheduling | Performance measurements for representative long and wide studies |
| OP-03 | NPY/NPZ selections, file references between steps, prefix listings, TypeScript file transfer | Persistent file indexing and additional scientific formats |
| OP-04 / OP-08 | Described arrays, units/coordinates/conventions and HCIPy → POPPY pupil-to-image exchange | More scientific quantities and the periodic-structure and photonic-circuit exchange paths |
| OP-12 | Completed-episode indexes, retry/continuation with changed worker count, separate solver errors | Shared datasets and asynchronous learner integration |
| OP-14 / OP-15 | Movable native/portable packages, managed Python launch, on-demand guides, concise Skills | Continued native host runs as host releases change |
| OP-05 / OP-06 / OP-07 / OP-09–11 / OP-13 / OP-16 | Existing APIs remain available | Distributed integrations, complete research programs, remote jobs and broader software coverage |

Catalogue entries, working adapters and complete scientific workflows remain distinct. The environment accepts software outside the catalogue; each solver keeps its own platform and licensing requirements.

## Next contributions

Prioritize **OP-05**: independently distributable software integrations. Build on the OP-04 data API and the first OP-08 exchange to extend **OP-07/08** across more programs. Contributors with licensed workstations can advance **OP-06**; remote computing infrastructure supports **OP-09/10**. The entries below retain their identifiers for coordination.

## Execution and data

### OP-01 · Concurrent MCP requests

Implemented in 0.6.0: bounded concurrent tool calls, a separate lane for status waits, serialized replies, request cancellation and accepted calculations continuing after disconnection. TypeScript requests support AbortSignal. See [mcp.py](../src/optics_photonics/mcp.py) and [client](../clients/typescript/src/index.ts).

### OP-02 · Large workflow scheduling

Implemented in 0.6.0: readiness and dependency state stay in the worker, appended steps load incrementally and scheduling reads exclude completed results. CPU and named capacities remain shared across runs. Measure SQL, launch and solver time separately before introducing persistent compute workers. See [jobs.py](../src/optics_photonics/jobs.py).

### OP-03 · Large files and array access

0.6.0 walks one directory at a time and limits metadata reads to the requested page; a prefix selects one step or folder. It still traverses matching names to count them. Add persistent file indexing for older runs and files from active programs. References should identify run, step, attempt and relative path so they remain meaningful across machines.

Extend bounded byte reads with numerical selections, channels and requested downsampling. Start with memory-mapped NPY; add chunked formats according to actual solver output. Downstream inputs should refer to files without copying arrays through JSON. Remote download must transfer contents to the client rather than merely returning a server path.

Deliver bounded reads for many files, files still being written and datasets larger than memory. Start in [jobs.py](../src/optics_photonics/jobs.py), [native.export](../src/optics_photonics/native.py) and [mcp.py](../src/optics_photonics/mcp.py). Coordinate with OP-01 and OP-04.

### OP-04 · Scientific data descriptions

Implemented in 0.7.0: `data.quantity`, `data.save` and `data.load` exchange NPZ arrays with JSON descriptions. Coordinates can be named arrays, uniform samples or channel/port labels. `read_array` returns descriptions and the coordinates matching slices, reversed selections and downsampling, without requiring NumPy in the connector.

Unit and spectral conversions, complex time dependence and wavefront sign changes are explicit and retain their origin. Spectral conversions also update the physical quantity name. Descriptions accept normalization, reference planes and material sources as needed; ordinary arrays and scalar results remain usable without them.

The [HCIPy → POPPY exchange](../examples/exchange/) saves an aberrated pupil, converts path-difference sign and units, and reproduces image displacement and Strehl ratio. Continue coverage for meshes, rays, density matrices and other software through the same mechanism. Implementation: [data.py](../src/optics_photonics/data.py), [arrays.py](../src/optics_photonics/arrays.py).

## Software and research capabilities

### OP-05 · Independently installable software integrations

Preserve `register_software`, `bind_environment`, native programs and command execution. Let integration packages carry software identity, version/platform requirements, installation sources, capabilities, runnable programs and domain references, including software outside the catalogue.

Report installation, interpreter selection, SDK access, session opening and actual calculation separately. Collect missing configuration once, reuse working environments and install scientific dependencies on demand. Connector updates preserve environments and prior runs.

Deliver independently packaged Python, native-command and SDK integrations without changing core dispatch. Define discovery, installation, updating and removal. Start in [environments.py](../src/optics_photonics/environments.py), [catalogue.py](../src/optics_photonics/catalogue.py), [packages.py](../src/optics_photonics/packages.py) and [connections.json](../data/connections.json).

### OP-06 · Complete native-software research

For COMSOL, Lumerical, OpticStudio and CST, complete project loading/creation, parameter changes, solving/analysis, result extraction, model saving and session shutdown. Use separate PRs per software; retain its full native API.

Prioritize repeated session startup, version differences, license release and interrupted-project recovery. Actual workstation runs record software version, platform and operations performed. Identify community bridges separately from vendor SDKs.

Deliver a real research program that repeatedly changes and computes a model, saves it and reloads it. Independent runs own separate outputs; reconnecting retrieves their results. Start in [native.py](../src/optics_photonics/native.py), [examples/native](../examples/native/) and [NATIVE.md](NATIVE.md). This can proceed beside OP-05, gradually adopting OP-04.

### OP-07 · Open-software research coverage

Extend the 16 packaged library calculations into complete programs, and connect catalogue tools without complete execution paths. Organize by research need; these examples are not a closed support list. New software follows OP-05.

| Research object | Initial programs and integrations |
| --- | --- |
| Geometrical optics and illumination | Optiland / Raysect: real rays, nonsequential propagation and system optimization |
| Diffraction, imaging and polarization | HCIPy / POPPY / LightPipes / py-pol: complex fields, aberrations, PSF/OTF, polarization and reconstruction |
| Films, materials and scattering | TMM / Mie: dispersion, absorption, angle/wavelength dependence and material sources |
| Maxwell equations, periodic structures and modes | Meep / MPB / grcwa / legume: meshes, boundaries, sources, modes, fields and flux |
| Integrated photonics | gdsfactory / KLayout / SAX: layouts, device ports, S-parameters and circuits |
| Fibers, pulses, lasers and cavities | Relevant catalogue software: complex envelopes, dispersion, nonlinearity, gain and noise |
| Quantum optics | QuTiP: open systems, dissipation, correlations and measurement results |
| Tissue optics, X-rays and inverse problems | Relevant transport, beamline and reconstruction tools: geometry, sources, materials and observables |

Deliver environment preparation, a parameterized research program, scientific output, usage and model conditions for each integration. Use an analytical limit, convergence change or another method when it establishes the scientific result. Adding catalogue rows is not a substitute for an executable workflow.

### OP-08 · Research across multiple programs

The fields/aberrations → PSF path is implemented in 0.7.0 with HCIPy and POPPY; run it from [steps.json](../examples/exchange/steps.json). The other two paths remain: periodic-structure complex reflection/transmission → finite-device propagation, and layout → device S-parameters → circuit response.

Each conversion states its approximation, units, sampling, phase and reference plane. Geometry, materials and parameters remain replaceable.

Deliver a run initiated from one parameter file, with intermediate results and final observables, and the ability to replace a software component. Depends on OP-03, OP-04 and relevant OP-06/07 integrations.

## Continuing computation and learning

### OP-09 · Remote and cluster job continuation

SSH can already launch MCP; remote solver task IDs currently remain the research program's responsibility. Persist backend, job ID, state and result location so submission, attachment, status, cancellation and download share the existing run interface.

Start with Slurm and Tidy3D as two distinct execution systems. Reconnect to existing tasks after interruption. If a submission response is lost, use provider-supported identifiers to find the task; otherwise retain an unknown submission outcome rather than automatically submitting again. Distinguish network interruption from solver failure.

Deliver reconnection after connector restart, remote result retrieval and cancellation of the actual remote task. Use existing computing accounts; state which portions ran locally when remote infrastructure is unavailable. See [Slurm](https://slurm.schedmd.com/rest_api.html) and [Tidy3D](https://docs.flexcompute.com/projects/tidy3d/en/latest/api/submit_simulations.html). Depends on OP-03/05 and coordinates with OP-10.

### OP-10 · Apply resource choices to solvers

Existing `cpu`, `requirements` and `pools` administer local shared quantities; some adapters already pass thread counts. Map them explicitly to solver threads, MPI ranks, GPU devices and remote queues, and retain effective launch settings.

License capacity comes from workstation configuration or a supported license-service query. Describe the capacity source and actual availability separately. Preserve queued work and its reason when a resource is unavailable. The relevant backend confirms completion of active work.

Deliver simultaneous studies that actually respect thread, GPU and software-concurrency settings. An external scheduler remains responsible for cluster allocation. Start in [jobs.resources](../src/optics_photonics/jobs.py), [environments.bind](../src/optics_photonics/environments.py) and [native.session](../src/optics_photonics/native.py).

### OP-11 · Continue inside long programs

`resume_run` retains successful steps and reruns unfinished steps. Add optional progress and save-point interfaces for long sweeps, optimization and solver programs. Reload solver state when supported; otherwise continue from an explicitly saved program step.

Retain program version, inputs, completion position and needed model files. Remote jobs use OP-09 attachment. Live local sessions remain inside research processes; arbitrary SDK objects are not presumed serializable.

Deliver an interrupted sweep that retains completed parameter points and computes the remainder without resubmitting existing work. Depends on OP-03 and adopts OP-04 output descriptions.

### OP-12 · Episode continuation and datasets

0.6.0 indexes completed episodes and resumes collection without repeating them, including a changed worker count. Dataset assembly should select attempts explicitly and preserve interrupted records. Task and policy versions identify changes in the scientific program.

Retain `terminated`, `truncated` and final observations. Represent collection failure, solver failure and a scientific task's negative reward separately. Support different physical models, action spaces and observation structures.

Deliver resumption with a changed worker count and no duplicate completed episode in the assembled dataset. Read by task, policy version, episode and attempt. Depends on OP-03/11; start in [sampling.py](../src/optics_photonics/sampling.py).

### OP-13 · Parallel collection and learner integration

Build on OP-12 with asynchronous episode allocation, capacity-limited data transfer and policy updates. Keep numerical loops in scientific processes, without an MCP call per action. Support lightweight CPU environments, heavier full-wave computations and long-lived solver sessions.

Deliver a real learner connection that collects data and updates a policy. Report worker count, episode-duration distribution, collection throughput, waiting and resource use. Complete single-host operation before extending through OP-09; learning frameworks own the training algorithm.

## Installation, knowledge and collaboration

### OP-14 · Host installation and updates

Complete actual installation paths for Research OS/Qiushi, Codex, Claude Code, DeepSeek Harness and ordinary MCP. Record host version, interface and installation, connection, execution and update results separately. Generating a package does not establish that a host has used it.

Deliver clean-directory installation, computation from the host, disconnection/reconnection, file retrieval and updating while preserving environments and research data. Address three-system paths, spaces, multiple Python installations and headless servers. State marketplace listing only after it is published.

Start in [packages.py](../src/optics_photonics/packages.py), [connect](../connect/), the [TypeScript client](../clients/typescript/) and [package_release.py](../scripts/package_release.py).

### OP-15 · Task-specific research instructions

Keep the two entry Skills short and executable; load domain references on demand. Software instructions answer which model applies, how to prepare the environment, submit a complete program, interpret output and continue after interruption. Match the actual tool arguments.

Deliver usable entry points for installed tools, new tools, remote programs and cross-tool research while loading only relevant material. Edit canonical sources and regenerate package copies. Start in [skills](../skills/), [mcp.py](../src/optics_photonics/mcp.py) and [package_marketplace.py](../scripts/package_marketplace.py); update alongside the implemented capabilities above.

### OP-16 · Catalogue and integration status

Update software versions, licenses, installation, platforms and primary references per entry. Record the source date and distinguish documentation, installation route, executable programs and the actual environments/operations exercised. Retain the previous date for entries not reread.

Deliver synchronized Chinese/English/JSON with discovery by research task, platform, license and executable capability. Third-party packages can join without changing the core. Let research coverage determine catalogue growth. Start in [English](../data/catalogue.en.json), [Chinese](../data/catalogue.zh.json), [connections.json](../data/connections.json) and [build.py](../scripts/build.py).

## Collaboration and delivery

Start each contribution on a separate branch from current main, after reading open PRs and related branches. A PR addresses a usable behavior and explains the change, usage, environment actually used and any external environment still needed. OP IDs aid handoff; one task may need more than one PR.

OP-01/02/03/09/11 often touch execution code: agree on interface changes before splitting edits. OP-05/06/07/15/16 can proceed with separate contributors. Preserve project names, software IDs, existing calls and research data; format changes include an explicit reading/migration path. Preserve contributor attribution.

TypeScript handles hosts and clients, Rust native processes, Python scientific software/programs and SQL tasks/resources. Move responsibilities when measured behavior warrants it.

Use the repository's relevant execution workflows for changed source, regenerate bundled plugins where affected, and let maintainers coordinate releases. Describe features through concrete operations, data and results.
