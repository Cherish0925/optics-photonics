<p align="right"><a href="README.zh-CN.md">中文</a> · <b>English</b></p>

![Optics · Photonics — software, physics, programmable access](docs/assets/readme-header.webp)

# Optics-Photonics AI Lab

A research environment for optics and photonics that agents and researchers install as a Python package, MCP server, plugin or Skills. It selects software from a catalogue of 97 tools, runs complete native research programs in their own environments, keeps long calculations running after the agent disconnects, and returns scientific files that can be read in parts. Its physical framework is **Field + Matter + Interaction**.

| Read | Explore the data | Build on it |
| --- | --- | --- |
| [English HTML](https://cherish0925.github.io/Optics-Photonics-AI-Lab/) · [中文 HTML](https://cherish0925.github.io/Optics-Photonics-AI-Lab/index.zh.html) | [English JSON](data/catalogue.en.json) · [中文 JSON](data/catalogue.zh.json) | [Agent entry point](llms.txt) · [Contributing](CONTRIBUTING.md) |
| [English Markdown](docs/catalogue.en.md) · [中文 Markdown](docs/catalogue.zh.md) | [Source index](data/resources.en.json) · [Schema](data/schema.json) | [Examples](examples/) · [Develop](#develop) |
| [Foundations](docs/foundations.html) · [基础框架](docs/foundations.zh.html) | [Foundation source](foundations/README.md) | [Execution](docs/EXECUTION.md) · [Native software](docs/NATIVE.md) |

The [English](https://raw.githubusercontent.com/Cherish0925/Optics-Photonics-AI-Lab/main/docs/index.html) and [Chinese](https://raw.githubusercontent.com/Cherish0925/Optics-Photonics-AI-Lab/main/docs/index.zh.html) HTML pages are self-contained and open offline. The [full catalogue page](https://cherish0925.github.io/Optics-Photonics-AI-Lab/catalogue.html) adds comparison and CSV/JSON export.

## Install

| Host | Install |
| --- | --- |
| Agentic Research OS | Download the [Research OS package](https://github.com/Cherish0925/Optics-Photonics-AI-Lab/releases/download/optics-v0.5.1/Optics-Photonics-0.5.1-ResearchOS.zip), extract it and install the directory containing `plugin.json`; it carries native executors for six system/architecture combinations, MCP, the catalogue and both Skills, and uses the host's Python. Or **Extensions → Plugins → Add from link** with `https://github.com/Cherish0925/Optics-Photonics-AI-Lab/tree/main/connect/agentic-research-os`. |
| Codex | `codex plugin marketplace add Cherish0925/Optics-Photonics-AI-Lab`, then `codex plugin add optics-photonics@optics-photonics` |
| Claude Code | `claude plugin marketplace add Cherish0925/Optics-Photonics-AI-Lab`, then `claude plugin install optics-photonics@optics-photonics` |
| Qiushi | Editions built on Research OS use the package above; other editions use `optics-photonics connect qiushi` for MCP or command access. |
| DeepSeek Harness | Project index `https://raw.githubusercontent.com/Cherish0925/Optics-Photonics-AI-Lab/main/docs/dsh/index.json`, or `optics-photonics connect deepseek` for a specific interpreter. |
| Any MCP host, Python, shell | Install the wheel below and register `optics-photonics mcp` as a stdio server. |

```sh
python -m pip install "https://github.com/Cherish0925/Optics-Photonics-AI-Lab/releases/download/optics-v0.5.1/optics_photonics-0.5.1-py3-none-any.whl"
optics-photonics prepare tmm
optics-photonics connect agentic-research-os --output optics-plugin
```

The connector needs Python 3.10+ on Windows, macOS or Linux and has no third-party dependencies; marketplace plugins run it with `python` from the host's PATH, otherwise generate a package for a specific interpreter with `optics-photonics connect HOST`. Each solver keeps its own Python, platforms and license. Run the MCP server on the machine that holds the scientific software, locally or over SSH. [Connection guide](docs/CONNECT.md) · [Interactive guide](https://cherish0925.github.io/Optics-Photonics-AI-Lab/connect.html) · [Releases](https://github.com/Cherish0925/Optics-Photonics-AI-Lab/releases)

## How a calculation runs

1. **Choose software.** `software_search` and `software_details` return the physical method, interfaces, installation source and packaged operations of each catalogue entry. `register_software` adds a tool outside the catalogue.
2. **Connect its environment.** `prepare_environment` installs a documented recipe into an isolated environment; `bind_environment` reuses an existing interpreter or executable; `discover_native_software` and `bind_native_software` connect installed COMSOL, Lumerical, OpticStudio and CST SDKs ([native sessions](docs/NATIVE.md)).
3. **Submit a complete program.** A Python program receives `INPUTS` and `OUTPUT_DIR`, uses the solver's full native API and sets `RESULT`; an executable uses the same files through environment variables. `submit_calculation` returns a run ID at once; `submit_workflow` adds dependent or parallel steps; a later step receives values, or the locations of files, from earlier ones.
4. **Continue and read results.** `run_status` waits up to 25 s per call; other requests on the same connection are answered meanwhile. Runs survive disconnection and are found again with `list_runs`. `result_files`, `read_result` and `read_array` return file listings, byte ranges and parts of NPY/NPZ arrays. `resume_run` reruns unfinished steps and keeps completed ones.
5. **Collect episodes.** `sample_episodes` runs Gymnasium-style environments in parallel solver workers and stores seeds, actions, observations and rewards for learning ([episodes](docs/LEARNING.md)).

The same operations are available as `optics-photonics` commands, a Python API and a TypeScript client. 16 open libraries have packaged calculations that have been run; the four commercial session adapters have run against SDK doubles, not yet against licensed solvers.

## Execution

A Rust executor owns solver processes, cancellation and deadlines. Python connects scientific SDKs and coordinates jobs. SQLite stores runs and admits steps against shared CPU and named capacities such as GPUs and solver licenses, across all runs on the host. The TypeScript client connects agent hosts. MPI ranks, GPU selection and cluster queues remain in each solver's own launcher. [Execution and resources](docs/EXECUTION.md)

## Physical foundation

> **Optics / Photonics = Field + Matter + Interaction**

**Field** is the classical or quantized electromagnetic field and its states; **matter** includes microscopic degrees of freedom, materials, devices and detectors; **interaction** is the exchange of energy, momentum and information between them. Free propagation is field dynamics, components are structured matter, and a measurement is a designed field–matter interaction. The catalogue and Skills are organized by this framework, from geometrical and wave optics to nanophotonics, fibers, lasers, imaging, spectroscopy and quantum optics, each within the limits of its effective theory. [Foundations](docs/foundations.html) · [Markdown source](foundations/)

## Catalogue

- **29 commercial**, **65 open-source** and **3 free-with-restrictions** tools. Free clients, paid solvers, academic licenses and external PDKs are distinguished.
- Each entry records physical methods, use cases, programming interfaces, compute environment, license, application basis, limitations and primary sources. Reviewed **2026-10-20**.
- API, CLI and macros are listed separately from **official / community / unverified** MCP servers and agent Skills. A documentation MCP is not treated as a solver interface.
- Stable `id` values are shared by both languages. Agents start at [`llms.txt`](llms.txt) and read [`llms-full.txt`](llms-full.txt) or the JSON.

Models connect through the physical quantities they exchange:

| Task | What passes between models | Examples in the catalogue |
| --- | --- | --- |
| Lens → image → inference | Pupil field, aberrations, PSF, sampling, detector response | OpticStudio, CODE V, Optiland, prysm, POPPY |
| Unit cell → metasurface → system | Complex transmission / reflection, polarization, angle, wavelength | torcwa, grcwa, Meep, Lumerical, Tidy3D, Diffractio |
| Layout → device → circuit | Process layers, ports, reference planes, normalized S-parameters | gdsfactory, KLayout, IPKISS, JCMsuite, SAX |
| Pulse → link → receiver | Complex envelope, time grid, dispersion, nonlinearity, noise | Luna, py-fmas, RP Fiber Power, VPI, OptiCommPy |
| Thermomechanics → cavity → readout | Deformation, index changes, operating point, noise spectra | COMSOL, Finesse, HCIPy |
| Sample → propagation → reconstruction | The measured observable and its forward operator | MCX, MMC, PyNX, pyDHM, HoloPy |

Units, reference frames, field conventions and model assumptions must match at each connection.

## Develop

```bash
git clone https://github.com/Cherish0925/Optics-Photonics-AI-Lab.git
cd Optics-Photonics-AI-Lab
python -m pip install -e ".[rl]"
python -m unittest discover -s tests
python scripts/build.py
python scripts/package_marketplace.py
```

`build.py` regenerates the HTML, Markdown, source index and agent documents from `data/`; `package_marketplace.py` regenerates the bundled Research OS copy after source or Skill changes. Generated files are committed. `OPTICS_SCIENCE_TESTS=1` enables the cases that run scientific libraries.

| Path | Purpose |
| --- | --- |
| `src/optics_photonics/` | Connector: catalogue, environments, execution, jobs, result arrays, episode sampling, MCP, CLI |
| `native/executor/` | Rust process executor |
| `clients/typescript/` | TypeScript client for agent hosts |
| `skills/` | Agent Skills and domain references |
| `connect/` | Generated host packages |
| `data/` | Bilingual catalogue, connections, domains and schema |
| `src/render.py`, `scripts/build.py` | Website and document generation |
| `examples/` | Native programs, solver sessions and the episode example |
| `foundations/` | Field · Matter · Interaction framework |

## License

Original code and catalogue descriptions are [MIT](LICENSE). Referenced software, documentation, PDKs and data keep their own licenses. The embedded Noto-derived font subset is [SIL OFL 1.1](docs/assets/FONT_LICENSE.txt). See [NOTICE](NOTICE). Package names, commands, plugin IDs and stored environments are unchanged since the repository was renamed.
