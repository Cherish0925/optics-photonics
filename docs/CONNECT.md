# Optics & Photonics connections

One package supplies software discovery, native-program execution, MCP and research Skills. IOP supplies the persistent service, native process supervision, scheduling and experiment records. Optical solvers retain their own APIs and installation environments.

## Install

Python 3.10 or newer runs the connector on Windows, macOS and Linux. Solver support follows each solver's own OS, architecture, Python and license requirements.

```sh
python -m pip install "git+https://github.com/Cherish0925/optics-photonics.git@optics-v0.1.0"
optics-photonics search "thin film" --license-group open
optics-photonics info tmm
optics-photonics prepare tmm
optics-photonics run tmm spectrum --inputs '{"n":[1,1.45,1.52],"thickness_nm":[100],"wavelength_nm":[450,550,650]}'
```

On shells with different JSON quoting rules, save the JSON in `inputs.json` and use `--inputs @inputs.json`. A release wheel can be installed without Git. `python -m optics_photonics` is equivalent to the CLI entry point.

`prepare` creates an isolated environment for a tested installation recipe. To reuse a solver installation:

```sh
optics-photonics bind tmm --python /path/to/scientific/python --threads 1 --concurrency 4
optics-photonics environments
```

`--python` points to the scientific interpreter, including a virtual environment. Each software may have a different interpreter. `OPTICS_HOME` selects the configuration directory; the default is `~/.optics-photonics`.

## Connect a Harness

```sh
optics-photonics connect agentic-research-os --output optics-plugin
```

| Host | Generated connection | Use |
| --- | --- | --- |
| Agentic Research OS | `plugin.json`, bundled Python code and Skills | Install the directory/ZIP and activate its installed revision. Uses `${RESEARCH_PYTHON}`. |
| Codex | `.codex-plugin/plugin.json`, `.mcp.json`, Skills | Native plugin or the `codex mcp add` command in `INSTALL.md`. |
| Claude Code | `.claude-plugin/plugin.json`, `.mcp.json`, Skills | `claude --plugin-dir PATH` or the MCP registration command in `INSTALL.md`. |
| DeepSeek Harness | `optics.cordis.yml` | `dsh web --patch PATH/optics.cordis.yml`; uses `@deepseek-ai/dsh-mcp-client`. |
| Qiushi | MCP configuration and shell entry | Agentic Research OS editions use its native package; other editions use MCP or `tools` / `call`. |
| Other MCP hosts | `mcp.json` | Register the stdio command in that host's configuration format. |

Replace `agentic-research-os` with `codex`, `claude`, `deepseek`, `qiushi` or `mcp`. Generated local configurations use the selected interpreter and absolute directory. Regenerate after moving them. Host packages contain their code and resources; no source checkout is needed at runtime. Existing host settings are not overwritten.

An update replaces the connector/plugin version, retaining `OPTICS_HOME` and scientific environments. Install a new wheel or Git tag, generate a new package directory, and update the host's installed plugin. Research OS revision activation uses its own package manager. A local stdio server requires a host that can launch local programs; cloud-only hosts need an execution environment or their own bridge.

## Native programs and durable calculations

A native Python program receives `INPUTS` (JSON), `OUTPUT_DIR` (Path), and sets `RESULT` to a compact JSON object. It can import the full upstream API, call optimizers, retain a solver session throughout a calculation, and write any scientific file format. Examples live in [`examples/programs`](../examples/programs).

```sh
optics-photonics run tmm --program research.py --inputs @inputs.json
```

For work that must continue after an Agent disconnects, install [IOP Runtime](https://github.com/Cherish0925/AI4Instruments/releases) on the computing host. Run the following on that host:

```sh
optics-photonics attach tmm
optics-photonics submit tmm --program research.py --inputs @inputs.json --request-id study-001
optics-photonics status RUN_ID
optics-photonics files RUN_ID
optics-photonics download ARTIFACT_ID spectrum.csv
```

Local IOP configuration supplies the endpoint and token. For a remote IOP service, set `IOP_ENDPOINT` and `IOP_TOKEN`; software registration still runs on the computing host because interpreter and worker paths belong to it. Remote Agents submit source and inputs through MCP/API; the native process executes on the IOP computer.

A workflow is a JSON array of IOP steps: `id`, `device`, `operation`, `arguments`, `after`, and optional `bindings`. Use explicit `after: []` for independent calculations, dependencies for ordering, and `bindings` for result transfer. `submit-workflow --run-id RUN_ID` appends a batch to an existing external experiment. The same IOP experiment can include physical instruments and digital computations. Use one native program where a live vendor session must be preserved.

The first local attach creates a missing CPU pool from the available CPU count and preserves existing capacities. `threads` sets common numerical thread limits; `concurrency` controls simultaneous processes for a software environment. Actual MPI, GPU, license and cluster allocations belong to the solver/launcher. No hardware or license capacity is inferred from a catalogue entry.

IOP 0.8.5 publishes command-generated files when their workflow finishes; explicit IOP artifact uploads can make data available during a continuous experiment. Save third-party remote job IDs and use the provider's own resume mechanism; arbitrary remote solver sessions are not recreated automatically.

## Coverage

All 96 catalogue entries have connection records, including primary documentation and upstream MCP/Skill links. Their execution status is separate:

| Coverage | What is supplied |
| --- | --- |
| 13 software libraries | Installation recipes and executed calculations: tmm, miepython, raytracing, LightPipes, POPPY, HCIPy, QuTiP, SymPy, SciPy, scikit-image, KLayout, grcwa, legume. |
| 58 Python API descriptions, including those 13 | Import discovery, interpreter binding and full native-program route. Remaining libraries require their native installation and have not all been run here. |
| 33 native software interfaces | A shared executable/argument adapter; vendor-specific launch programs and licenses must be supplied. These are documented routes, not prebuilt complete vendor drivers. |
| 4 tools with unconfirmed automation | Source records; no automatic execution claim. |
| 1 material database | Data source and provenance; not a solver. |
| 14 research domains | Model selection, physical quantities, units and transfer between programs, loaded only when needed. |

A native executable wrapper reads JSON from `IOP_REQUEST_FILE` (or stdin), saves files in `IOP_OUTPUT_DIR`, and writes compact JSON to `IOP_RESULT_FILE`. Bind it with `--command-json '["executable","argument"]'`. C, C++, C#, Java, Julia and commercial batch programs use this same process interface; there is no need to rewrite them in Python.

MCP exposes 11 tools covering selection, environments, registration, submission, status, cancellation and files. Large results remain in files. Original official/community MCP entries retain their authorship and stated scope; this package is maintained by this repository, not endorsed by those vendors.

## Development

```sh
python -m pip install -e .
python scripts/build.py
python -m unittest discover -s tests
python -m pip install -r requirements-science.txt
OPTICS_SCIENCE_TESTS=1 python -m unittest discover -s tests
python -m build
```

PowerShell: `$env:OPTICS_SCIENCE_TESTS="1"` before the scientific test command. `scripts/check_iop_connection.py` additionally needs the released IOP package with its native executor and the MCP Python SDK. It exercises a real submitted optical program, retry, MCP disconnection, reconnection and file download.

Host format sources: [Codex plugin package](https://developers.openai.com/plugins/build/plugins), [Claude plugin reference](https://code.claude.com/docs/en/plugins-reference), [DeepSeek native MCP configuration](https://deepseek-harness.github.io/deepseek-harness/en/guide/mcp-memory). Solver sources are linked per entry in `data/connections.json`.
