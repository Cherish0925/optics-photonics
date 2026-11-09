---
name: optical-computation
description: Install or connect optical software environments, run native optical research programs, configure an MCP host, or submit durable parallel and sequential calculations to IOP.
---

# Optical computation

Use the smallest complete program for the scientific task, with the upstream software's full API available. The connector and scientific interpreter may be different environments.

Without MCP, use `optics-photonics` or `python -m optics_photonics`. The matching CLI commands are `search` (software_search), `info` (software_details), `bind` (bind_environment), `attach` (attach_iop), `submit` (submit_calculation), `status`, `files`, `download` and `cancel`. Filter licensing with `search --license-group open`; run `--help` for argument syntax.

1. Read `software_details(tool)` and `environments`. For an existing Python environment use `bind_environment(tool, python=...)`. For a native executable provide an argument array; its program reads `IOP_REQUEST_FILE`, writes files in `IOP_OUTPUT_DIR`, and writes a JSON result to `IOP_RESULT_FILE`.
2. When no environment exists, `optics-photonics prepare TOOL` installs a listed recipe into a separate environment. Other tools use their official installation instructions. Do not install the unrelated PyPI `meep` package as the electromagnetic solver. Commercial APIs require the vendor's installation and license. A library being importable does not prove that its license, GPU or remote service is ready.
3. For a short local task use `optics-photonics run TOOL ACTION --inputs @inputs.json`. `info TOOL` gives the exact packaged example and its physical assumptions. For a full native program use `--program research.py`. It receives `INPUTS` (JSON), `OUTPUT_DIR` (Path) and must set `RESULT` to a compact JSON object. Save arrays, meshes and models in OUTPUT_DIR. Use explicit units in input/output names.
4. For durable work, run `attach_iop(tool)` on the computer hosting both IOP and the software environment, then `submit_calculation`. The returned run ID survives the MCP connection. Poll `run_status` at a rate suitable for the solver, and use `result_files` / `download_result` for data. A download path is on the MCP host, not necessarily the user's computer.
5. Submit sweeps with `submit_workflow`: each step has `id`, `device: optics-TOOL`, `operation: calculate`, `arguments: {action, inputs, source}` and `after`. Explicit `after: []` allows independent work. `after: [id]` establishes ordering, not data transfer. IOP `bindings` transfers predecessor results. Use a single native program for shared solver sessions and tightly coupled iterations.
6. Reuse the same request_id for a retried submission. For an existing IOP external experiment pass its run_id to submit_workflow. Do not create one experiment per numeric point. Cancel via cancel_run rather than abandoning an expensive calculation.

For Python libraries, threads sets OMP/OpenBLAS/MKL/NumExpr thread limits and reserves that many IOP CPU units. concurrency limits simultaneous operations for that software. These settings do not configure MPI, a commercial license server, a GPU allocation or a cluster queue; set those through the software or scheduler launcher. A vendor session that cannot overlap should use concurrency=1.

The first local attach initializes an absent IOP CPU pool from the CPUs available to that computer. It preserves existing capacities. Subsequent allocation changes belong to IOP resource configuration.

A native program can own an entire commercial/cloud session: open, construct model, solve, extract, save and close in try/finally. Save remote job IDs immediately; follow the service's resume API rather than submitting again after an interruption. IOP 0.8.5 does not automatically reconstruct arbitrary third-party sessions.

Install a host connection with `optics-photonics connect HOST --output DIR`. HOST is agentic-research-os, codex, claude, deepseek, qiushi or mcp. Read DIR/INSTALL.md; preserve existing host settings. For Agentic Research OS, install the plugin and activate its installed revision. For DeepSeek use the generated Cordis overlay. A new plugin version does not change an existing scientific environment automatically.
