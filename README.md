<p align="right"><a href="README.zh-CN.md">中文</a> · <b>English</b></p>

![Optics · Photonics — software, physics, programmable access](docs/assets/readme-header.webp)

# Optics · Photonics

A bilingual software catalogue for optical science and engineering: **what each tool models, how it is licensed, and how people and AI agents can use it.**

**96 tools and product families · 14 domains · 200 documentation and integration links**

| Read | Explore the data | Build on it |
| --- | --- | --- |
| [English HTML](https://cherish0925.github.io/optics-photonics/) · [中文 HTML](https://cherish0925.github.io/optics-photonics/index.zh.html) | [English JSON](data/catalogue.en.json) · [中文 JSON](data/catalogue.zh.json) | [Agent entry point](llms.txt) · [Contributing](CONTRIBUTING.md) |
| [English Markdown](docs/catalogue.en.md) · [中文 Markdown](docs/catalogue.zh.md) | [Source index](data/resources.en.json) · [Schema](data/schema.json) | [Examples](examples/) · [Build instructions](#develop) |

Download [English HTML](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/docs/index.html) or [Chinese HTML](https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/docs/index.zh.html) and open either in a browser. Each file contains its own styles, scripts, font subset, catalogue and source index. Browsing, filtering, comparison and exports work offline; opening external documentation requires internet access.

## What is inside

- **29 commercial / paid**, **64 free and open-source**, and **3 free or source-available tools with restrictions**. Free clients, paid solvers, academic-only licenses and external PDKs are distinguished.
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

url = "https://raw.githubusercontent.com/Cherish0925/optics-photonics/main/data/catalogue.en.json"
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
git clone https://github.com/Cherish0925/optics-photonics.git
cd optics-photonics
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
