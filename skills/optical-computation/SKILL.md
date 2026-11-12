---
name: optical-computation
description: "Connect optical software environments, model and simulate optical systems, run native research programs and parallel calculations, collect versioned research episodes for learning, retrieve scientific results, or install optical MCP and plugin connections."
---

# Optical computation

Write one complete program per scientific task and submit it. A background worker runs it in the solver's own environment and keeps running after the agent or the MCP connection ends.

| Stage | Tools |
| --- | --- |
| Choose software | `software_search`, `software_details` |
| Connect its environment | `environments`, `prepare_environment`, `bind_environment`, `discover_native_software`, `bind_native_software`, `register_software` |
| Run | `submit_calculation`, `submit_workflow`, `sample_episodes`, `compute_resources` |
| Follow | `run_status`, `list_runs`, `cancel_run`, `resume_run` |
| Read results | `result_files`, `read_result`, `read_array`, `download_result` |

1. **Connect.** `software_details(tool)` gives the installation source, native interfaces and packaged operations. `environments` lists what is configured; `refresh=true` only when current availability matters. Bind an existing interpreter with `bind_environment(tool, python=...)`, or install a listed recipe with `prepare_environment` and wait for that run. Meep comes from its own electromagnetic-solver distribution, not the unrelated PyPI package.
2. **Program.** Use a packaged `action` when its physical model matches the task. Otherwise submit Python `source` that uses the software's full native API: it receives `INPUTS` and `OUTPUT_DIR` and sets `RESULT` to compact JSON. Save arrays, meshes, models and plots as files in OUTPUT_DIR, with units and sampling conventions. Keep a tightly coupled loop or a live solver session inside one program.
3. **Submit.** `submit_calculation` returns `run_id` at once; pass the same `request_id` when retrying a submission. `submit_workflow` takes steps with `id`, `tool`, `action` or `source`, `inputs`, and optional `after`, `bindings`, `requirements`, `timeout` in seconds. Steps without `after` run in parallel. `{"value":{"step":"solve","path":["result","R"]}}` binds a predecessor value; `{"field":{"step":"solve","file":"field.npz"}}` binds the location of a predecessor file or folder, for arrays, meshes and models. Pass `run_id` to add steps to an existing run.
4. **Follow.** `run_status(run_id, wait=25)` waits for completion while other calls are answered. `list_runs` finds earlier work after reconnecting. `cancel_run` stops a run. `resume_run` reruns unfinished steps and keeps completed steps and every attempt's files; read the earlier log, and any saved remote job ID, before restarting a remote calculation.
5. **Read.** `result_files(run_id, prefix="solve/")` lists files with sizes and array shapes. `read_result` returns a byte range of a text or log file. `read_array` returns part of an NPY or NPZ array (`index`, `member`, `max_elements`); read arrays in parts, not as whole files.

**Resources.** `compute_resources(cpu=..., pools={...})` sets shared CPU and named capacities such as GPU slots and solver licenses. `bind_environment` sets a tool's threads, concurrency, environment variables and resource requirements; a step may add `requirements`, and all quantities are acquired together across runs. Set concurrency to what the license and the machine allow. MPI ranks, GPUs and cluster or cloud queues are configured in the solver's own launcher. A program that starts a cloud or cluster job saves the job ID in its result and continues that job through the provider's API.

Read when the task needs it:

- [programs](references/programs.md): executable programs, the command line, tools outside the catalogue.
- [native-software](references/native-software.md): installed Lumerical, COMSOL, OpticStudio and CST.
- [episodes](references/episodes.md): `sample_episodes`, retries and continued collections.
- [hosts](references/hosts.md): host packages, remote workstations, long runs and updates.
