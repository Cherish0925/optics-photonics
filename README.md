<p align="right"><a href="README.zh-CN.md">中文</a> · <b>English</b></p>

![Optics · Photonics — software, physics, programmable access](docs/assets/readme-header.webp)

# Optics-Photonics AI Lab

An independent digital research environment for optics and photonics: scientific software, native programs, background calculations, MCP, plugins and research Skills. Its physical foundation is **Field + Matter + Interaction**.

**Native programs · Background computation · MCP · Skills · Agent plugins**

| Read | Explore the data | Build on it |
| --- | --- | --- |
| [English HTML](https://cherish0925.github.io/Optics-Photonics-AI-Lab/) · [中文 HTML](https://cherish0925.github.io/Optics-Photonics-AI-Lab/index.zh.html) | [English JSON](data/catalogue.en.json) · [中文 JSON](data/catalogue.zh.json) | [Agent entry point](llms.txt) · [Contributing](CONTRIBUTING.md) |
| [English Markdown](docs/catalogue.en.md) · [中文 Markdown](docs/catalogue.zh.md) | [Source index](data/resources.en.json) · [Schema](data/schema.json) | [Examples](examples/) · [Build instructions](#develop) |
| [Foundations](docs/foundations.html) · [基础框架](docs/foundations.zh.html) | [Foundation source](foundations/README.md) | **Field · Matter · Interaction** |

Download [English HTML](https://raw.githubusercontent.com/Cherish0925/Optics-Photonics-AI-Lab/main/docs/index.html) or [Chinese HTML](https://raw.githubusercontent.com/Cherish0925/Optics-Photonics-AI-Lab/main/docs/index.zh.html) and open either in a browser. The self-contained pages cover installation, Agent connections, software, research methods and results. The [full software catalogue](https://cherish0925.github.io/Optics-Photonics-AI-Lab/catalogue.html) retains comparisons and source exports. External documentation opens online.

## Install and run

**Agentic Research OS:** in **Extensions → Plugins → Add from link**, paste
`https://github.com/Cherish0925/Optics-Photonics-AI-Lab/tree/main/connect/agentic-research-os`,
install `optics-photonics`, then activate it. The package carries its MCP server,
catalogue and both Skills and uses Research OS's Python. No separate connector
installation is needed. [Other hosts and updates](docs/CONNECT.md#install-from-a-marketplace).


The repository now includes an installable connector, native-program execution, MCP and research Skills. [Connection guide](docs/CONNECT.md) · [Interactive guide](https://cherish0925.github.io/Optics-Photonics-AI-Lab/connect.html) · [Release packages](https://github.com/Cherish0925/Optics-Photonics-AI-Lab/releases).

```sh
python -m pip install "git+https://github.com/Cherish0925/Optics-Photonics-AI-Lab.git@optics-v0.4.0"
optics-photonics prepare tmm
optics-photonics connect agentic-research-os --output optics-plugin
```

Native session adapters connect installed COMSOL, Lumerical, OpticStudio and CST; [setup and operations](docs/NATIVE.md). 16 libraries have executed scientific calculations; all 97 catalogue entries have connection descriptions and primary sources. Native programs retain each solver's full API. Independent background workers execute parallel and dependent calculations, coordinate CPU resources, preserve completed steps and return scientific files. Closing the Agent does not stop submitted jobs.

Host packages cover Agentic Research OS, Codex, Claude Code, DeepSeek Harness, Qiushi and generic MCP. The connector runs on Windows, macOS and Linux; each scientific solver keeps its own supported platforms and license.

## Research episodes and parallel sampling

Version 0.4.0 adds complete episode sampling inside native software workers. Define a Gymnasium-style environment and policy in a Python program; submit it through `sample_episodes`, the Python SDK or `optics-photonics sample`. Workers share the existing CPU and software concurrency settings. Every episode retains its task/policy version, deterministic seed, actions, observations, reward and termination state. Arrays remain typed numerical files.

[Episode API and executable coating example](docs/LEARNING.md). Research OS and other host bundles include the same implementation. The package remains independent of IOP. Existing package names, commands, plugin IDs and stored software environments are unchanged after the repository rename.

## Physical foundation

The repository uses one compact model to connect the catalogue across subfields and scales:

> **Optics / Photonics = Field + Matter + Interaction**

Here **field** means the classical or quantized electromagnetic field and its states; **matter** includes microscopic degrees of freedom, materials, devices and detectors; **interaction** covers the mechanisms by which field and matter exchange energy, momentum and information. Free propagation is field dynamics; optical components are structured matter; measurement is a controlled field–matter interaction. The framework spans quantum optics, nanophotonics, lasers, fibers, imaging, spectroscopy, wave optics and geometrical optics while preserving the limits of each effective theory.

Read the complete [English foundation](docs/foundations.html) or [中文基础框架](docs/foundations.zh.html). Maintainable Markdown sources live in [`foundations/`](foundations/).

## What is inside

- **29 commercial / paid**, **65 free and open-source**, and **3 free or source-available tools with restrictions**. Free clients, paid solvers, academic-only licenses and external PDKs are distinguished.
- Each entry includes physical methods, use cases, programming interfaces, compute environment, licensing, application basis, limitations and primary sources.
- API, CLI and macros are documented independently from **official / community / unverified MCP and agent Skills**. A documentation MCP is not assumed to execute a solver.
- Search by task or interface, filter by license and domain, compare up to four tools, and export CSV or JSON.
- A searchable resource index links websites, manuals, code, license texts and agent integrations to their corresponding software.
- Seven physical-model families, six composable workflows, digital-twin / surrogate guidance, and four short code examples connect the directory to actual research tasks.

## Start with the physical representation

| Task | What passes between models | Examples in the catalogue |
| --- | --- | --- |
| Lens → image → inference | Pupil field, aberrations, PSF, sampling, detector response | OpticStudio, CODE V, Optiland, prysm, POPPY |
| Unit cell → metasurface → system | Complex transmission / reflection, polarization, angle, wavelength | torcwa, grcwa, Meep, Lumerical, Tidy3D, Diffractio |
| Layout → device → circuit | Process layers, ports, reference planes, normalized S-parameters | gdsfactory, KLayout, IPKISS, JCMsuite, SAX |
| Pulse → link → receiver | Complex envelope, time grid, dispersion, nonlinearity, noise | Luna, py-fmas, RP Fiber Power, VPI, OptiCommPy |
| Thermomechanics → cavity → readout | Deformation, index changes, operating point, noise spectra | COMSOL, Finesse, HCIPy |
| Sample → propagation → reconstruction | The actual measured observable and its forward operator | MCX, MMC, PyNX, pyDHM, HoloPy |

Each workflow identifies the physical quantities to exchange. Match units, reference frames, field conventions and model assumptions across tools.

## Use with an agent

Start at [`llms.txt`](llms.txt). Read [`llms-full.txt`](llms-full.txt) for the complete English catalogue, or consume the JSON directly. Stable `id` values identify the same tools in both languages.

```python
import json
from urllib.request import urlopen

url = "https://raw.githubusercontent.com/Cherish0925/Optics-Photonics-AI-Lab/main/data/catalogue.en.json"
tools = json.load(urlopen(url))
candidates = [t for t in tools
              if t["group"] == "open"
              and "periodic" in t["cats"]
              and t["route"] == "api"]
for tool in candidates:
    print(tool["id"], tool["api"], tool["sources"])
```

Follow the linked documentation to prepare the environment and call the native interface. Connector records identify their scope and provenance: official, community or unverified.

## Develop

Python **3.10+**, standard library only:

```bash
git clone https://github.com/Cherish0925/Optics-Photonics-AI-Lab.git
cd Optics-Photonics-AI-Lab
python scripts/build.py
python -m unittest discover -s tests
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000/` for English or `/index.zh.html` for Chinese. Edit `data/catalogue.en.json` and `data/catalogue.zh.json`, then rebuild. Source data, translated interface strings and rendering code are kept separate. Generated HTML is committed so readers can download it without running a build.

| Path | Purpose |
| --- | --- |
| `data/catalogue.{en,zh}.json` | Complete bilingual entries with shared identifiers and source URLs |
| `data/domains.{en,zh}.json` | Fourteen task domains |
| `data/resources.{en,zh}.json` | Generated source index, including connector links |
| `data/schema.json` | Machine-readable catalogue contract |
| `src/` | HTML renderer, resource index and English interface strings |
| `scripts/build.py` | Reproducible HTML, Markdown, source-index and agent-document generation |
| `docs/` | Self-contained website editions and readable catalogues |
| `examples/` | Short interface examples with explicit prerequisites |
| `community/` | Reusable English / Chinese launch descriptions |

## Scope and contributions

Reviewed **2026-10-20** against vendor documentation, maintainer repositories, licenses and author materials. Each entry records its application basis and model conditions.

Useful contributions include missing tools, primary-source corrections, license changes, new interfaces, reproducible examples and translation improvements. See [CONTRIBUTING.md](CONTRIBUTING.md).

**License:** original project code and catalogue descriptions are [MIT](LICENSE). Referenced software, documentation, PDKs and data retain their own licenses. The embedded Noto-derived font subset is [SIL OFL 1.1](docs/assets/FONT_LICENSE.txt). See [NOTICE](NOTICE).
