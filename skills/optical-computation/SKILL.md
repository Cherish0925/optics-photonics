---
name: optical-computation
description: "Connect optical software environments, model and simulate optical systems, run native research programs and parallel calculations, retrieve scientific results, or install optical MCP and plugin connections."
---

# Optical computation

Use a complete program for the scientific task. The connector and each solver may have different Python environments. Computation, background jobs and result access are provided by this package.

1. Read `software_details(tool)` and `environments`. Connect an existing interpreter with `bind_environment(tool, python=...)`. For a listed install recipe, call `prepare_environment` and wait for its run to succeed. From a shell use `optics-photonics prepare TOOL`; a different Python can be selected with `--python PATH`. For Meep use its documented electromagnetic-solver distribution, not the unrelated PyPI package.
   For installed Lumerical, COMSOL, OpticStudio or CST, use `discover_native_software` and `bind_native_software`. Read [native software sessions](references/native-software.md) for SDK selection, project operations and complete native programs.
2. Use a packaged `action` when its physical model matches the task. Otherwise submit a complete Python `source` using the software's full native API. It receives `INPUTS` and `OUTPUT_DIR`, and sets `RESULT` to compact JSON. Save arrays, meshes, models and plots in OUTPUT_DIR, with units and sampling conventions. Keep tightly coupled loops or a live software session in one program.
3. Call `submit_calculation`; retain its `run_id` and `request_id`. Reuse request_id when retrying the same submission. The independent worker continues after MCP disconnects. Find existing work with `list_runs`, inspect it with `run_status`, and read written files with `result_files` and `read_result`. `download_result` copies a file on the MCP host.
4. Submit independent or dependent work with `submit_workflow`. Each step has `id`, `tool`, `inputs`, `action` or `source`, optional `after`, `bindings` and `timeout` in seconds. Omitted or empty `after` permits parallel execution. A binding `{"value":{"step":"solve","path":["result","R"]}}` copies a predecessor value into INPUTS['value'] and adds the dependency. Use the predecessor's `output` path to transfer large files. For a continued research run, pass run_id when adding new steps.
5. Use `compute_resources` for the shared CPU capacity. `bind_environment` sets per-tool threads and concurrency. Match concurrency to the software's actual session/permission/license behavior. Configure MPI ranks, GPUs and cluster/cloud scheduling through the native launcher. Save cloud job IDs when assigned and use the provider's continuation API within the program.
6. Cancel via `cancel_run`. `resume_run` keeps successful steps and reruns unfinished steps, preserving each attempt's files. Read the prior result/log and any saved remote job ID before restarting a remote calculation.

Without MCP, use `optics-photonics` or `python -m optics_photonics`: `search`, `info`, `prepare`, `bind`, `run`, `submit`, `submit-workflow`, `runs`, `status`, `files`, `read`, `download`, `cancel`, `resume`, `resources`. Use `--inputs "@inputs.json"` for a file and `--program research.py` for a full program; `search --license-group open` selects open-source tools.

Native executable programs read JSON from `OPTICS_REQUEST_FILE` or stdin, write scientific files under `OPTICS_OUTPUT_DIR`, and write JSON to `OPTICS_RESULT_FILE`. Bind them using an executable/argument array; optional placeholders are `{request}`, `{output}`, `{result}`. C/C++/C#/Java/Julia and vendor programs use this interface directly.

Create a host package with `optics-photonics connect HOST --output DIR`, choosing agentic-research-os, codex, claude, deepseek, qiushi or mcp. Follow DIR/INSTALL.md. For Research OS install and activate the package revision; for DeepSeek use its Cordis overlay. Run the MCP process on the machine containing the scientific environment, locally or through SSH. Install a new plugin version into a new directory; retain existing environments and research data.
