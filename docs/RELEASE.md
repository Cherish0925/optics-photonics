Independent digital optics and photonics research, from software selection to running calculations and retrieving results.

Version 0.3.1 fixes clean-environment installation of the TMM solver: the connection recipe now installs and verifies NumPy alongside TMM. The Research OS plugin and Connect packages include the corrected recipe.

- Native session adapters for installed Lumerical, COMSOL, OpticStudio and CST: SDK discovery and binding, owned sessions, project load/save, full native programs and scientific data export. Commercial adapter lifecycle tests use SDK doubles; licensed solver execution requires the target workstation.
- Background calculations run independently of the Agent process. Parallel and dependent steps share a CPU budget and per-software concurrency settings.
- SQLite stores research runs, source programs, inputs, environment settings and results. Reconnecting uses the same run ID; request IDs prevent duplicate submissions. Resume retains completed steps and starts a new attempt for unfinished steps.
- MCP supports background environment preparation, calculation submission, progress, cancellation, result browsing and chunked file reading. Plugins use the same independent implementation.
- 16 executable scientific libraries, including new Optiland real-ray tracing, gdsfactory layout and py-pol polarization calculations. Native programs retain the complete upstream APIs.
- 97 software descriptions, 14 research domains and 202 original documentation and integration links, with Chinese and English interactive guides.

Install with Python 3.10+ or the release wheel. The Research OS ZIP contains an installable plugin; the Connect ZIP generates packages for Codex, Claude Code, DeepSeek Harness, Qiushi and generic MCP. Software environments are independent of plugin updates.

Windows, macOS and Linux CI runs the scientific calculations, background scheduling, cancellation, installed wheel, generated plugin and real MCP disconnect/reconnect workflow. Scientific solvers retain their supported platforms, dependencies and licenses.

[中文指南](https://cherish0925.github.io/optics-photonics/connect.zh.html) · [English guide](https://cherish0925.github.io/optics-photonics/connect.html)
