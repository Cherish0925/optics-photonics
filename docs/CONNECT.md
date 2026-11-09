# Optics & Photonics research tools

An independent package for optical software, native research programs, background calculations, MCP, Skills and plugins. Software selection, model construction, solving, optimization and results share one interface.

## Install and calculate

The connector supports Python 3.10+ on Windows, macOS and Linux. Each solver uses its own supported Python version, operating system and license. Different tools may use different environments.

```sh
python -m pip install "git+https://github.com/Cherish0925/optics-photonics.git@optics-v0.2.0"
optics-photonics info tmm
optics-photonics prepare tmm
optics-photonics run tmm spectrum --inputs "@inputs.json"
```

Use these inputs:

```json
{"n":[1,1.45,1.52],"thickness_nm":[100],"wavelength_nm":[450,550,650]}
```

The result includes the output directory, scientific result and software versions; the spectrum is saved as CSV. A release wheel can be installed without Git. Every command also works through `python -m optics_photonics`.

## Environments and complete programs

```sh
optics-photonics bind tmm --python "/path/to/scientific/python" --threads 1 --concurrency 4
optics-photonics environments
optics-photonics resources --cpu 8
optics-photonics run tmm --program research.py --inputs "@inputs.json"
```

`prepare` installs a documented recipe into a separate environment. `bind` reuses an existing one. `threads` sets common numerical-library thread limits; `concurrency` limits simultaneous processes for one software. Total CPU capacity is shared by background runs. Configure MPI, GPUs, vendor licenses and cluster queues in the solver's native launcher.

A Python program receives `INPUTS` and `OUTPUT_DIR`, and sets `RESULT` to compact JSON. It can use the complete upstream API, retain a live solver session and perform arbitrary optimization or iteration. Save arrays, meshes and models under OUTPUT_DIR. Native program examples are in [examples/programs](../examples/programs).

A native executable reads JSON from `OPTICS_REQUEST_FILE` or stdin, writes files under `OPTICS_OUTPUT_DIR`, and writes its JSON result to `OPTICS_RESULT_FILE`. `bind --command-json` accepts an executable/argument array with optional `{request}`, `{output}`, `{result}` placeholders. C, C++, C#, Java, Julia and commercial batch tools keep their native implementation.

## Background runs and dependencies

```sh
optics-photonics submit tmm --program research.py --inputs "@inputs.json" --request-id study-001
optics-photonics runs
optics-photonics status RUN_ID
optics-photonics files RUN_ID
optics-photonics read RUN_ID calculate/attempt-1/result.json
optics-photonics download RUN_ID calculate/attempt-1/spectrum.csv spectrum.csv
```

Submission returns immediately. The independent worker continues when the submitting CLI or MCP process exits. Reuse `request-id` for retries of the same submission. Written files can be read while the run is active.

A workflow is an array of steps with `id`, `tool`, `inputs`, `action` or `source`, optional `after`, `bindings` and `timeout`. Independent steps run within resource limits. A binding such as `{"value":{"step":"solve","path":["result","R"]}}` copies a predecessor result into the input named `value` and adds the dependency. `output` in a predecessor result identifies its directory for large-file exchange.

```sh
optics-photonics submit-workflow workflow.json --request-id study-002
optics-photonics submit-workflow next-steps.json --run-id RUN_ID
optics-photonics cancel RUN_ID
optics-photonics resume RUN_ID
```

Append preserves the research run. Resume retains successful steps and reruns unfinished steps into separate attempt directories. Provider-specific cloud job IDs and session continuation belong in the native research program. Complete examples appear in the [Chinese guide](CONNECT.zh-CN.md).

## Agent hosts

```sh
optics-photonics connect agentic-research-os --output optics-plugin
```

| Host | Package and activation |
| --- | --- |
| Agentic Research OS | Extract the release ZIP, install the directory containing `plugin.json`, activate the installed revision. Uses `${RESEARCH_PYTHON}`. |
| Codex | `connect codex` generates a native plugin and MCP registration command. |
| Claude Code | `connect claude`; use `claude --plugin-dir PATH` or the generated MCP command. |
| DeepSeek Harness | `connect deepseek`; use `dsh web --patch PATH/optics.cordis.yml`. |
| Qiushi | Research OS editions use its native package; other editions use `connect qiushi` for MCP or command access. |
| Other MCP hosts | `connect mcp`; register the stdio command in the host's format. |

MCP provides software search, environment preparation/binding, resource settings, submission, history, status, cancellation, resumption and result access. `prepare_environment` installs a listed recipe in the background and returns a run ID; successful installation registers the environment. Two Skills and 14 domain references supply scientific methods on demand.

Computations run on the MCP host. SSH can launch the stdio server on a workstation with the scientific software: `ssh -T USER@HOST /path/to/python -m optics_photonics mcp`. `read_result` returns bounded text/binary contents. `download_result` copies to a path on the MCP host; use SSH/SFTP for large remote files.

Install a new wheel or tag and generate a new plugin directory to update. Configuration, scientific environments and research records remain under `OPTICS_HOME` or `~/.optics-photonics`.

## Software and extension model

The bilingual catalogue separates commercial, open-source and restricted tools. Each connection retains primary interface documentation and upstream MCP/Skill sources. Filter executed calculations in the interactive guide. `software_details` gives native APIs, installation recipes, runnable inputs and physical conventions.

Extend software through a connection record, environment and native program using the same job/file interface. Vendor SDKs, GUI applications, MPI and cloud services retain their own launch/session requirements. Exchange units, coordinates, sampling, normalization and material sources alongside fields, spectra, S-parameters and models.

## Development

```sh
python -m pip install -e . build mcp -r requirements-science.txt
python scripts/build.py
OPTICS_SCIENCE_TESTS=1 python -m unittest discover -s tests -v
python scripts/check_standalone_connection.py
```

PowerShell: set `$env:OPTICS_SCIENCE_TESTS="1"` before running the tests. Native Windows/macOS/Linux jobs run scientific calculations, background scheduling, cancellation, installed-wheel/plugin checks and real MCP disconnection/reconnection.

Host format sources: [Codex](https://developers.openai.com/plugins/build/plugins), [Claude Code](https://code.claude.com/docs/en/plugins-reference), [DeepSeek Harness](https://deepseek-harness.github.io/deepseek-harness/en/guide/mcp-memory).
