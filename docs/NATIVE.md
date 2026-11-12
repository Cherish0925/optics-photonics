# Local optical software

The native session adapters connect installed COMSOL, Lumerical, OpticStudio and CST to the same background jobs used by scientific Python programs. The Agent supplies a project and a research program. A worker owns the software session, saves a working model in the run directory, executes the program and releases the session. Independent projects can run concurrently; an optimization loop can keep its model loaded throughout one program.

| Software | Connection | Execution host | Available operations |
| --- | --- | --- | --- |
| Lumerical | Vendor `lumapi`, or `ansys.lumerical.core` | Windows / Linux, supported vendor installation | FDTD / MODE / DEVICE / INTERCONNECT sessions; project load/save; object properties; solve; monitor results; full scripting API |
| COMSOL | Community MPh bridge to the installed COMSOL Java API | Windows / Linux / macOS | Model load/create/save; parameters with units; studies; evaluation; full `MODEL.java` and `SESSION.java` |
| OpticStudio | Community ZOSPy bridge to ZOS-API | Windows | Standalone session; optical system load/save; lens and nonsequential editors; native analyses, ray tracing and optimization |
| CST | Vendor `cst.interface` and `cst.results` | Windows / Linux where the vendor SDK is supported | Design environment; project load/save; native modeling/history; solver; result-tree access |

## Connect once

Run `optics-photonics discover`; add `--root /software/location` for a custom installation directory. Discovery checks known layouts and returns paths and adapter requirements. It neither starts a solver nor acquires a license. `bind-native` checks SDK module discovery in the chosen interpreter and saves the connection. The first submitted job opens the licensed session.

```sh
optics-photonics bind-native lumerical --python /path/to/python --sdk-path /path/to/lumerical/api/python --threads 4
optics-photonics bind-native comsol --python /path/to/python-with-mph --threads 4
optics-photonics bind-native opticstudio --python /path/to/python-with-zospy
optics-photonics bind-native cst --python /path/to/vendor-compatible-python --sdk-path /path/to/python_cst_libraries
```

Use the interpreter supported by the installed SDK, with Python 3.9+ for this worker. Install MPh or ZOSPy in that interpreter when using their bridges. Installing a bridge does not install COMSOL or OpticStudio. `software_details` lists the package requirements and primary API documentation. COMSOL version and OpticStudio DLL location can be supplied through `--options "@options.json"`. Lumerical options are `product`, `hide`, and `module`; the default product is FDTD. COMSOL and Lumerical receive the configured thread count. CST and OpticStudio thread controls belong to their native solver configuration; the shared job scheduler uses `threads` as the reserved CPU allocation.

MCP equivalents are `discover_native_software` and `bind_native_software`. Existing jobs retain the connection settings with which they were submitted.

## Execute a project

Save the absolute project path in `inputs.json`:

```json
{"project":"/work/optical-model.mph","parameters":{"wavelength":"1550[nm]"},"results":["ewfd.normE"]}
```

```sh
optics-photonics submit comsol solve_project --inputs "@inputs.json"
optics-photonics submit comsol --program research.py --inputs "@inputs.json"
```

The expression and parameter names must exist in the project. `inspect_project` opens and saves a project without solving; `solve_project` uses the selected COMSOL study, Lumerical solver or CST solver. OpticStudio uses analysis-specific programs instead of a generic solve command.

A native program receives `INPUTS`, `OUTPUT_DIR`, `SDK`, `SESSION`, `MODEL`, `PROJECT_FILE`, and `EXPORT(value, name)`. It sets `RESULT` to compact JSON. `MODEL` is the native optical system/project, except COMSOL where it is the MPh model and exposes the complete vendor object as `MODEL.java`. The working model is saved before and after a successful program; arrays and complex fields are exported as NPZ with JSON structure metadata. Use native file formats and streaming writes for very large outputs. Relative material, geometry or external-data references still need their documented project paths.

The examples in [examples/native](../examples/native) include a COMSOL parameter sweep, Lumerical monitor extraction, an OpticStudio MTF analysis and CST result export. These are programs to adapt to the user's project, not bundled licensed models. Native-session lifetime tests use SDK doubles; these commercial solvers have not been run in this development environment. Normal completion and Python exceptions close owned sessions. Forced cancellation terminates the worker process tree; vendor services launched outside that tree can require vendor-specific recovery.

The MCP server can run on a different workstation from the Agent through SSH. An Agent on macOS can therefore use an OpticStudio installation on Windows; it does not make OpticStudio a native macOS application.

API sources: [Lumerical sessions](https://optics.ansys.com/hc/en-us/articles/360041873053-Session-Management-Python-API), [MPh sessions](https://mph.readthedocs.io/en/stable/api/mph.start.html), [COMSOL model access](https://mph.readthedocs.io/en/stable/api/mph.Model.html), [ZOSPy connections](https://zospy.readthedocs.io/en/stable/api/zospy.zpcore.ZOS.html), [ZOSPy MTF](https://zospy.readthedocs.io/en/stable/api/zospy.analyses.mtf.fft_mtf.FFTMTF.html), [CST Python automation](https://events.3ds.com/python-driven-automation-electromagnetic-simulations). CST's installed `Online Help/Python` documents the API for the local version.
