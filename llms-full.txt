# Optics · Photonics — software catalogue

Reviewed: 2026-10-20 | 96 tools and product families

Original descriptions and code: MIT. Linked products retain their own licenses.

This is a source-based selection study, not installation testing of every solver. Unverified does not mean absent.

## Commercial / paid

### Ansys Zemax OpticStudio

ID: `opticstudio` | Geometrical optics & lighting, Wave optics & propagation

- **Physical method:** Sequential / nonsequential ray tracing; physical optics propagation
- **Purpose:** Lens design, aberrations, tolerancing, stray light and selected coherent propagation workflows.
- **Programmable interface:** ZOS-API .NET with Python, C#, C++ and MATLAB; ZPL macros; standalone and interactive connections.
- **Compute:** Windows application; background instances still require a valid license.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Vendor engineering applications and automation examples cover imaging, lenses and illumination.
- **Limitations:** Sequential optics, nonsequential optics and POP expose different models and results. A community MCP does not cover the entire ZOS-API.
- **MCP (community):** [Community OpticStudioMCPServer using ZOS-API](https://github.com/jaruiz6363/OpticStudioMCPServer)
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://optics.ansys.com/hc/en-us/articles/42661773562899-Sample-code-for-ZOS-API-users)
- [Official documentation / website](https://optics.ansys.com/hc/en-us/articles/42661790380179-ZOS-API-NET-An-Overview)

### Keysight CODE V

ID: `codev` | Geometrical optics & lighting, Wave optics & propagation

- **Physical method:** Imaging optics design and optimization
- **Purpose:** Lens starting points, aberration optimization, tolerance analysis and image quality evaluation.
- **Programmable interface:** Macro-PLUS scripts, commands and batch design workflows. Consult the installed version for external automation details.
- **Compute:** Licensed local application with macro-driven execution.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Keysight imaging optics product with lens and mobile-camera design workflows.
- **Limitations:** Older resources use the Synopsys CODE V name; use the current Keysight product and documentation.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://www.keysight.com.cn/cn/zh/products/software/optical-solutions-software/optical-design-solutions/codev.html)

### Keysight LightTools

ID: `lighttools` | Geometrical optics & lighting

- **Physical method:** Nonsequential ray tracing / illumination
- **Purpose:** Illumination, light guides, displays and stray light, with source, material and scattering models.
- **Programmable interface:** Built-in macros and LTAPI automation; third-party Python wrappers are available.
- **Compute:** Primarily a licensed desktop application.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Official illumination product with CODE V to LightTools design workflows.
- **Limitations:** Python wrappers and the application have separate maintenance cycles. Source and BSDF data strongly affect results.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://www.keysight.com/es/en/products/software/optical-solutions-software/optical-design-solutions/lighttools.html)
- [Community integration](https://github.com/Mestas/Lighttools)

### FRED

ID: `fred` | Geometrical optics & lighting, Wave optics & propagation

- **Physical method:** Nonsequential tracing; coherent and incoherent optics
- **Purpose:** Propagation through complex optomechanical systems, scattering, stray light and laser systems.
- **Programmable interface:** Built-in scripting and .frs workflows; official examples include trace-and-analysis loops.
- **Compute:** Windows; multithreading, distributed execution or FREDmpc GPU computing depend on the edition.
- **License:** Commercial; conditional university gratis licenses require application
- **Application basis:** Photon Engineering supplies engineering applications, executable scripting examples and academic programs.
- **Limitations:** Built-in scripting is documented; a complete native Python API has not been established here.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Scripting / programming reference](https://support.photonengr.com/article/176-raytrace-and-analysis-loop)
- [Official product / platform](https://photonengr.com/)
- [Free / paid feature boundaries](https://photonengr.com/academic-licenses)

### TracePro

ID: `tracepro` | Geometrical optics & lighting

- **Physical method:** Monte Carlo ray tracing
- **Purpose:** Illumination, stray light, optical flux and optomechanical geometry analysis and optimization.
- **Programmable interface:** Scheme macros; the manual documents DDE and macro automation.
- **Compute:** Desktop application with macro / DDE integration.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Lambda Research engineering product with a 2026 user manual.
- **Limitations:** Desktop sessions need lifecycle management. A macro interface is not itself an MCP server.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official manual](https://lambdares.com/hubfs/TracePro_Users_Manual_2026.pdf)
- [Official documentation / website](https://lambdares.com/tracepro-2)

### OSLO

ID: `oslo` | Geometrical optics & lighting

- **Physical method:** Sequential optics / lens design
- **Purpose:** Optical layouts, aberrations, optimization and tolerance calculations.
- **Programmable interface:** CCL programming and command system; features depend on the edition.
- **Compute:** Windows; CCL scripting.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Lambda Research lens design product with a separately listed free EDU edition.
- **Limitations:** Commercial and EDU editions expose different capabilities; the free edition has its own entry.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://lambdares.com/oslo)
- [Official documentation / website](https://lambdares.com/edu)
- [Scripting / programming reference](https://lambdares.com/hubfs/Support/support/oslo/oslo_releases/OSLOProgramReference.pdf)

### ASAP

ID: `asap` | Geometrical optics & lighting, Wave optics & propagation

- **Physical method:** Nonsequential optics / physical optics
- **Purpose:** Complex optical systems, illumination, scattering and stray light analysis.
- **Programmable interface:** Official integrated Python, VBScript and other scripting support for automated analyses.
- **Compute:** Licensed desktop and solver environment.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Breault Research Organization optical analysis product.
- **Limitations:** Match the scripting host, object model and license configuration to the installed release.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Scripting / programming reference](https://breault.com/asap/)

### VirtualLab Fusion

ID: `virtuallab` | Wave optics & propagation, Geometrical optics & lighting, Periodic structures & metasurfaces

- **Physical method:** Field tracing / hybrid optical modeling
- **Purpose:** Joint modeling of diffraction, polarization, gratings, free-space systems and complex optical elements.
- **Programmable interface:** Official Programming API, programmable elements and scripts; documented extensions to Python / MATLAB workflows.
- **Compute:** Windows; in-product programming and external workflows.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** LightTrans wave-optics platform with optical element and application libraries.
- **Limitations:** Hybrid solvers exchange particular field representations; a hybrid workflow is not necessarily one full-wave Maxwell solution.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://programmingreference.lighttrans.com/2026.2/api/VirtualLab.Programming.html)
- [Official documentation / website](https://www.lighttrans.com/product/virtuallab-fusion/frequently-asked-questions/general-faqs.html)

### Ansys Speos

ID: `speos` | Geometrical optics & lighting, Computational imaging

- **Physical method:** Light transport / photometry / visual simulation
- **Purpose:** Illumination, automotive lighting, displays, sensors and human-vision-related optomechanical design.
- **Programmable interface:** Speos scripts; Ansys optical-automation supplies public Python automation and interoperability code.
- **Compute:** Runs with the relevant Ansys / CAD host environment.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Ansys engineering product with an officially maintained optical automation library.
- **Limitations:** The automation library is MIT-licensed; the Speos solver is not. Hosts may use different Python runtimes.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://optics.ansys.com/hc/en-us/articles/24752772596371-Optical-Automation-library-introduction)
- [Source repository](https://github.com/ansys/optical-automation)

### Ansys Lumerical

ID: `lumerical` | Electromagnetics & devices, Integrated photonics & layout, Periodic structures & metasurfaces

- **Physical method:** FDTD / modes / multiphysics / photonic circuits
- **Purpose:** FDTD, MODE, Multiphysics and INTERCONNECT form a device-to-circuit product family.
- **Programmable interface:** lumapi Python; LSF scripts; lumopt inverse design; lumslurm scheduling.
- **Compute:** Local and cluster execution; product and HPC licenses are configured separately.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Official applications cover nanophotonics, silicon photonics and optical transceiver links.
- **Limitations:** Python clients and MCP do not replace solver licenses. Each product has distinct physical models and output formats.
- **MCP (official):** [PyLumerical MCP published by the official Ansys organization](https://github.com/ansys/pylumerical-mcp)
- **Agent Skill (community):** [Community Lumerical_MCP_Skill](https://github.com/zxqcreations/Lumerical_MCP_Skill)

Sources:
- [Python interface](https://optics.ansys.com/hc/en-us/articles/360037824513-Python-API-overview)
- [MCP implementation / documentation](https://github.com/ansys/pylumerical-mcp)

### COMSOL Multiphysics

ID: `comsol` | Electromagnetics & devices, Geometrical optics & lighting, Lasers & precision interferometry

- **Physical method:** FEM / rays / multiphysics
- **Purpose:** Wave optics and ray optics coupled to thermal, structural and charge-transport models.
- **Programmable interface:** Official Java API and batch execution; LiveLink for MATLAB; third-party Python bridges.
- **Compute:** Windows / Linux / macOS; batch and server execution depend on licensing.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Official multiphysics platform and API; optical capabilities require the corresponding modules.
- **Limitations:** Third-party Python packages are not official Python APIs. Match optical, thermal, CAD and parallel licenses to the task.
- **MCP (community):** [Community comsol-mcp implementation](https://github.com/Ching-Chiang/comsol-mcp)
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://www.comsol.com/support/learning-center/article/overview-of-the-comsol-api-107912)
- [Official documentation / website](https://www.comsol.com/livelink-for-matlab)
- [MCP implementation / documentation](https://github.com/Ching-Chiang/comsol-mcp)

### CST Studio Suite

ID: `cst` | Electromagnetics & devices, Periodic structures & metasurfaces

- **Physical method:** Time-domain / frequency-domain electromagnetics
- **Purpose:** Electromagnetics from RF and terahertz to selected optical problems, including structural response and coupling.
- **Programmable interface:** Official Python automation, VBA macros and batch solver workflows.
- **Compute:** Desktop modeling and licensed compute environment.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** SIMULIA engineering electromagnetics software with official Python workflows.
- **Limitations:** Use dispersion and mesh settings appropriate to the wavelength. The Learning Edition is not equivalent to the complete solver.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Python interface](https://www.3ds.com/products/simulia/cst-studio-suite)
- [Python interface](https://blog.3ds.com/brands/simulia/cst-studio-suite-release-2021x-highlights/)

### Keysight RSoft Photonic Device Tools

ID: `rsoft` | Electromagnetics & devices, Periodic structures & metasurfaces, Integrated photonics & layout, Lasers & precision interferometry

- **Physical method:** FDTD / BPM / RCWA / FEM / EME / semiconductor lasers
- **Purpose:** Device tools include FullWAVE, BeamPROP, DiffractMOD, FemSIM, ModePROP and LaserMOD.
- **Programmable interface:** Parametric CAD, MOST scans and optimization; confirm scripting and external integration for each component.
- **Compute:** Module-dependent; selected solvers support GPUs or clusters.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Keysight photonic-device product family with links to CODE V, LightTools and ADS workflows.
- **Limitations:** Counted as one product family. Its component solvers implement different physical approximations.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://www.keysight.com/zz/en/products/software/optical-solutions-software/photonic-design-solutions.html)

### JCMsuite

ID: `jcm` | Electromagnetics & devices, Periodic structures & metasurfaces, Integrated photonics & layout

- **Physical method:** High-order FEM / electromagnetic inverse problems
- **Purpose:** Nanophotonics, waveguides, scattering, lithography and parameter reconstruction.
- **Programmable interface:** Official jcmwave Python; MATLAB / Octave and C interfaces; optimization and batch tasks.
- **Compute:** Local or cluster execution driven by Python.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** JCMwave photonics simulation product with dedicated interface documentation.
- **Limitations:** Geometry, meshes and boundary conditions must be modeled; an optimization API does not ensure parameter identifiability.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://www.jcmwave.com/jcmsuite/interface/)
- [Python interface](https://docs.jcmwave.com/JCMsuite/html/PythonInterface/bf647454e36069fd16f1a7a35cf6a865.html)

### Photon Design FIMMWAVE / FIMMPROP

ID: `photond` | Electromagnetics & devices, Integrated photonics & layout, Fibers & communications

- **Physical method:** Mode solving / eigenmode expansion
- **Purpose:** Waveguide and fiber modes, photonic-device propagation and mode conversion.
- **Programmable interface:** Official command-line, Python and MATLAB scripting; community pyFIMM is a wrapper reference.
- **Compute:** Licensed local solvers with scripting.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Photon Design waveguide and photonic-device design tools.
- **Limitations:** Converge mode truncation and propagation segmentation. Other Photon Design products have different modeling boundaries.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Scripting / programming reference](https://photond.com/fimmwave/features/scripting-optimisation)
- [Official documentation / website](https://photond.com/fimmwave/options/feature-option-table)

### Flexcompute Tidy3D

ID: `tidy3d` | Electromagnetics & devices, Integrated photonics & layout, Periodic structures & metasurfaces

- **Physical method:** Cloud FDTD / photonic device simulation
- **Purpose:** Define devices and simulations in Python, then submit cloud solves and analyze results.
- **Programmable interface:** Official Python API, web.run and batch execution; official MCP / agent plugins.
- **Compute:** Local modeling and analysis; Flexcompute cloud solver.
- **License:** Client: LGPL-2.1; cloud solving uses FlexCredits / commercial plans
- **Application basis:** Public case studies, publications and vendor research / industrial applications.
- **Limitations:** An open-source client is not a free local solver. Distinguish documentation tools from execution capabilities enabled by a bridge.
- **MCP (official):** [Official tidy3d-mcp / FlexAgent: documentation and bridge tools](https://github.com/flexcompute/plugin-marketplace)
- **Agent Skill (official):** [Official flexagent simulation, analysis and documentation Skills](https://github.com/flexcompute/plugin-marketplace)

Sources:
- [Free / paid feature boundaries](https://docs.flexcompute.com/projects/tidy3d/en/stable/faq/docs/faq/How-is-using-Tidy3D-billed.html)
- [Python interface](https://github.com/flexcompute/tidy3d)
- [Agent plugins / Skills](https://github.com/flexcompute/plugin-marketplace)

### Luceda IPKISS

ID: `ipkiss` | Integrated photonics & layout

- **Physical method:** Parametric cells / circuits / PDKs
- **Purpose:** Reusable PIC design combines geometry, ports, compact models, layout and verification.
- **Programmable interface:** Native Python framework, PDK packages, device-simulation drivers and Canvas integration.
- **Compute:** Python with local licensing and PDK environment.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Luceda provides foundry PDK support and fabrication-oriented design workflows.
- **Limitations:** An open PDK does not make IPKISS free. Evaluate PDK licensing, process constraints and model coverage separately.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://www.lucedaphotonics.com/luceda-photonics-design-platform)
- [API / project documentation](https://academy.lucedaphotonics.com/tutorials/device_sim/)

### VPIphotonics Design Suite

ID: `vpi` | Fibers & communications, Integrated photonics & layout, Lasers & precision interferometry

- **Physical method:** Optical communications / photonic circuits and systems
- **Purpose:** Joint simulation of transmitters, fiber links, amplifiers, receiver DSP and integrated photonics.
- **Programmable interface:** Official external simulation API; Python, MATLAB, C++ and COM co-simulation and custom modules.
- **Compute:** Licensed system-simulation environment with external code integration.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Vendor applications cover optical communication and photonic-device engineering.
- **Limitations:** System-level models are not device-level Maxwell solvers. Define sampling, noise and signal normalization explicitly.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://www.vpiphotonics.com/Tools/DesignSuite/Features/)
- [Official product / platform](https://www.vpiphotonics.com/Tools/DesignSuite/)

### Optiwave OptiSystem

ID: `optisystem` | Fibers & communications, Integrated photonics & layout

- **Physical method:** Optical communication links / signal systems
- **Purpose:** Modulation, fiber transmission, amplification, detection and bit-error performance.
- **Programmable interface:** Python / MATLAB co-simulation components; official examples for external execution and result access.
- **Compute:** Desktop system-simulation projects.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Optiwave provides optical-link and co-simulation examples.
- **Limitations:** A Python algorithm component does not establish a headless API for every GUI capability.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Python interface](https://optiwave.com/forums/topic/co-simulation-using-python/)
- [Official manual](https://cdn.optiwave.com/wp-content/uploads/2017/11/OptiSystem_15_New_Features.pdf)

### Essential Macleod

ID: `macleod` | Thin films & materials

- **Physical method:** Thin-film transfer / optimization / process analysis
- **Purpose:** Multilayer coatings, reflection and transmission, color, group delay and manufacturing analysis.
- **Programmable interface:** The Function extension offers BASIC-like scripts and object access; spreadsheet macros.
- **Compute:** Local desktop and built-in scripting.
- **License:** Commercial; Function and other extensions depend on the configuration
- **Application basis:** Thin Film Center coating design and manufacturing-analysis software.
- **Limitations:** Scripting depends on the purchased extensions; it is not presented here as a remote Python API.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://www.thinfilmcenter.com/essential.php)
- [Scripting / programming reference](https://www.thinfilmcenter.com/function.php)

### OptiLayer / OptiRE / OptiChar

ID: `optilayer` | Thin films & materials

- **Physical method:** Thin-film design / characterization / manufacturing inversion
- **Purpose:** Multilayer optimization, spectral inversion and in-process manufacturing correction.
- **Programmable interface:** Official COM Automation with Python examples; OptiReOpt for production integration.
- **Compute:** Pro editions support multiple platforms; COM automation is platform-dependent.
- **License:** Commercial; academic terms, modules and concurrent execution depend on the contract
- **Application basis:** Vendor documentation explicitly covers integration with production control and online characterization.
- **Limitations:** Cross-platform GUI support does not imply cross-platform COM. Check the API of the specific Pro release.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://optilayer.com/com-automation/)
- [Python interface](https://optilayer.com/development-history/new-features-in-optilayer-2018-version-12-83/)
- [Official product / platform](https://optilayer.com/downloads/)

### RP Fiber Power

ID: `rpfiber` | Fibers & communications, Lasers & precision interferometry

- **Physical method:** Fiber modes / gain / pulse propagation
- **Purpose:** Fiber lasers and amplifiers: pump, signal, ASE, dynamics and ultrashort pulses.
- **Programmable interface:** Built-in scripting language, generated scripts and custom forms.
- **Compute:** Local product; scripts define models and loops.
- **License:** Commercial
- **Application basis:** RP Photonics specialized fiber-design software.
- **Limitations:** The documented interface is a physics scripting environment; a general external API was not established in this review.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://www.rp-photonics.com/rp_fiber_power_interface.html)
- [Scripting / programming reference](https://www.rp-photonics.com/software_script_language.html)

### RP Resonator / RP ProPulse

ID: `rpresonator` | Lasers & precision interferometry, Fibers & communications

- **Physical method:** Resonators / pulse dynamics
- **Purpose:** Laser cavity modes and stability, and ultrashort-pulse round trips; choose between the two products by task.
- **Programmable interface:** Built-in scripting, interactive forms that generate models, and iteration loops.
- **Compute:** Local scripted simulation.
- **License:** Commercial; the two products are licensed separately
- **Application basis:** RP Photonics specialized laser and ultrafast software.
- **Limitations:** Cavity-mode design and nonlinear pulse simulation use different assumptions and are not interchangeable.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://www.rp-photonics.com/software_overview.html)
- [Scripting / programming reference](https://www.rp-photonics.com/rp_propulse_interface.html)

### Crosslight APSYS / PICS3D

ID: `crosslight` | Lasers & precision interferometry, Electromagnetics & devices

- **Physical method:** Optoelectronic semiconductor TCAD
- **Purpose:** Coupled electrical, optical and thermal modeling of LEDs, semiconductor lasers and related devices.
- **Programmable interface:** Official product and application scope confirmed; a general public API or MCP remains unverified.
- **Compute:** Specialized semiconductor-device simulation environment.
- **License:** Commercial; configured by TCAD module
- **Application basis:** Crosslight lists PICS3D, semiconductor industry applications and research publications.
- **Limitations:** Useful for coupled carriers, gain and temperature; obtain version-specific documentation for external automation.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://crosslight.com/)

### SYNOPSYS Lens Design(OSD)

ID: `synopsys-osd` | Geometrical optics & lighting

- **Physical method:** Lens design / optimization
- **Purpose:** Lens design software from Optical Systems Design, separate from the former Synopsys optical software business.
- **Programmable interface:** Command / macro-driven workflows; complete external API not verified.
- **Compute:** Desktop design application.
- **License:** Commercial; official trial has time and surface-count limits
- **Application basis:** OSD maintains official product, trial and macro documentation.
- **Limitations:** Do not confuse this product with the former vendor of CODE V and RSoft. A 30-day trial is not permanently free software.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://osdoptics.com/accessinstallation/)
- [Scripting / programming reference](https://osdoptics.com/wp-content/uploads/2024/09/SYNOPSYSTM-Lens-Design-Software-Starting-Guide-Ui-Plus.pdf)

### TFCalc

ID: `tfcalc` | Thin films & materials

- **Physical method:** Thin-film design / spectral optimization
- **Purpose:** Spectral performance, design and optimization of multilayer thin films.
- **Programmable interface:** Stable public API not verified; evaluate it primarily as a desktop product.
- **Compute:** Desktop application.
- **License:** Commercial; currently operated by Hulinks
- **Application basis:** The original developer states that Hulinks took over the business in 2022.
- **Limitations:** Use the current vendor for licensing; automation remains an item to confirm.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://www.sspectra.com/)
- [Official documentation / website](https://www.hulinks.co.jp/en/)

### MATLAB / Simulink

ID: `matlab` | Derivation & digital foundations, Computational imaging, Fibers & communications

- **Physical method:** Numerical computing / signals / control systems
- **Purpose:** Optical algorithms, signal processing, parameter estimation, controls and system models, with task-specific toolboxes.
- **Programmable interface:** MATLAB Engine API, batch execution, Simulink API and the official MATLAB MCP Server.
- **Compute:** Local or server; GPU and parallel features depend on toolboxes and hardware.
- **License:** Commercial / academic; toolboxes licensed separately
- **Application basis:** MathWorks scientific engineering environment with official agent integration.
- **Limitations:** Open-source MATLAB scripts do not imply free execution. Only compatible code can run without MATLAB through Octave.
- **MCP (official):** [Official MathWorks MATLAB MCP Server](https://github.com/matlab/matlab-mcp-server)
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [MCP implementation / documentation](https://github.com/matlab/matlab-mcp-server)
- [Official documentation / website](https://www.mathworks.com/help/cloudcenter/ug/run-matlab-with-ai-agentic-and-ai-assistant-applications.html)

### Wolfram Mathematica

ID: `mathematica` | Derivation & digital foundations, Quantum optics

- **Physical method:** Symbolic derivation / numerical computing
- **Purpose:** Wave equations, asymptotic expansions, integrals, matrices and mixed symbolic-numerical derivation.
- **Programmable interface:** Wolfram Language, wolframscript, official Python Client and official Wolfram MCP.
- **Compute:** Local or cloud computational kernel.
- **License:** Commercial Mathematica; local MCP requires an appropriately licensed kernel
- **Application basis:** Wolfram computational platform and AgentTools.
- **Limitations:** Analytical results depend on parameter domains and assumptions; this is not a substitute for a specialized optical field solver.
- **MCP (official):** [Official Wolfram Local / Cloud MCP](https://www.wolfram.com/ai/mcp/)
- **Agent Skill (official):** [Official WolframResearch AgentSkills](https://github.com/WolframResearch/AgentTools)

Sources:
- [MCP implementation / documentation](https://www.wolfram.com/ai/mcp/)
- [MCP implementation / documentation](https://www.wolfram.com/artificial-intelligence/mcp/local/wolfram-mcp-local/)
- [Maintainer repository](https://github.com/WolframResearch/AgentTools)

### Maple

ID: `maple` | Derivation & digital foundations

- **Physical method:** Computer algebra / numerics / code generation
- **Purpose:** Analytical modeling, symbolic derivation, differential equations and executable formula generation.
- **Programmable interface:** OpenMaple Python / C / Java API; command-line kernel.
- **Compute:** Local computational kernel and APIs.
- **License:** Commercial / academic
- **Application basis:** Maplesoft mathematical computing platform with OpenMaple documentation.
- **Limitations:** Provides derivation and model reduction, rather than a complete library of optical materials, boundaries and detector models.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Python interface](https://jp.maplesoft.com/support/help/maple/view.aspx?path=OpenMaple%2FPython%2FAPI)
- [Official manual](https://www.maplesoft.com/documentation_center/maple2024/ProgrammingGuide.pdf)

## Free & open source

### Meep

ID: `meep` | Electromagnetics & devices, Periodic structures & metasurfaces, Integrated photonics & layout

- **Physical method:** FDTD / adjoint optimization
- **Purpose:** Full-wave propagation, resonances, scattering and nanophotonic devices.
- **Programmable interface:** Python, Scheme and C++; scripted execution, HDF5 outputs and adjoint optimization.
- **Compute:** CPU / MPI; the standard release is not assumed to be a GPU solver.
- **License:** GPL-2.0 family
- **Application basis:** MIT / NanoComp research software with methods papers and examples.
- **Limitations:** Spatial and temporal resolution, PML and dispersion control numerical error; whole macroscopic optical benches are usually impractical for FDTD.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/NanoComp/meep)
- [License / usage terms](https://raw.githubusercontent.com/NanoComp/meep/HEAD/LICENSE)

### MPB

ID: `mpb` | Electromagnetics & devices, Periodic structures & metasurfaces

- **Physical method:** Frequency-domain eigenmodes / plane waves
- **Purpose:** Photonic-crystal bands, modes and periodic-medium eigenproblems.
- **Programmable interface:** Python / Scheme; programmable parameter sweeps and mode-data analysis.
- **Compute:** CPU / MPI.
- **License:** GPL-2.0 family
- **Application basis:** MIT Photonic Bands includes methods papers and tutorials.
- **Limitations:** Eigenmode calculation is distinct from arbitrary time-domain propagation; respect periodicity, material and boundary assumptions.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/NanoComp/mpb)
- [License / usage terms](https://raw.githubusercontent.com/NanoComp/mpb/HEAD/COPYING)

### FDTDX

ID: `fdtdx` | Electromagnetics & devices, Integrated photonics & layout

- **Physical method:** Differentiable FDTD
- **Purpose:** Three-dimensional photonic structures and gradient-based inverse design.
- **Programmable interface:** Native Python / JAX, automatic differentiation and programmable geometry.
- **Compute:** GPU with the appropriate JAX backend.
- **License:** MIT
- **Application basis:** Public implementation and research methods for differentiable simulation.
- **Limitations:** An emerging framework: check current material support, model coverage and memory requirements.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/ymahlau/fdtdx)
- [License / usage terms](https://raw.githubusercontent.com/ymahlau/fdtdx/HEAD/LICENSE)

### openEMS

ID: `openems` | Electromagnetics & devices

- **Physical method:** EC-FDTD
- **Purpose:** Electromagnetics, RF and terahertz structures and related wave propagation.
- **Programmable interface:** Python and Octave / MATLAB interfaces; command-line solver.
- **Compute:** CPU; parallel support depends on the build.
- **License:** GPL-3.0
- **Application basis:** Open electromagnetic solver with public tutorials.
- **Limitations:** At optical frequencies, check dispersion, meshing and interface support instead of reusing RF defaults.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/thliebig/openEMS)
- [License / usage terms](https://raw.githubusercontent.com/thliebig/openEMS/HEAD/COPYING)

### S⁴ / S4

ID: `s4` | Periodic structures & metasurfaces, Thin films & materials

- **Physical method:** RCWA / Fourier modal method
- **Purpose:** Reflection, transmission and diffraction orders in periodic layered structures and gratings.
- **Programmable interface:** Lua scripting; Python interface depends on the build.
- **Compute:** Local CPU; batch execution.
- **License:** GPL-2.0 family
- **Application basis:** Stanford Fan group solver for layered periodic structures.
- **Limitations:** Finite-size edges and isolated nonperiodic objects are outside the standard periodic-cell model.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/victorliu/S4)
- [License / usage terms](https://raw.githubusercontent.com/victorliu/S4/HEAD/COPYING)

### torcwa

ID: `torcwa` | Periodic structures & metasurfaces, Thin films & materials

- **Physical method:** Differentiable RCWA
- **Purpose:** Gradient optimization of periodic nanostructures, metasurface cells and gratings.
- **Programmable interface:** Native Python / PyTorch and automatic differentiation.
- **Compute:** CPU / CUDA GPU.
- **License:** LGPL-3.0
- **Application basis:** TORCWA methods paper and simulation examples accompany the code.
- **Limitations:** Fourier order and material discontinuities affect convergence; a periodic cell is not a complete finite metalens.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/kch3782/torcwa)
- [License / usage terms](https://raw.githubusercontent.com/kch3782/torcwa/HEAD/LICENSE)

### grcwa

ID: `grcwa` | Periodic structures & metasurfaces, Thin films & materials

- **Physical method:** Differentiable RCWA
- **Purpose:** Multilayer periodic structures, diffraction and topology optimization research.
- **Programmable interface:** Python with an Autograd backend.
- **Compute:** CPU; backend-dependent configuration.
- **License:** GPL-3.0
- **Application basis:** Public paper, interfaces and reflection / transmission optimization examples.
- **Limitations:** Autograd does not automatically imply GPU support. Match materials and periodicity to the model.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/weiliangjinca/grcwa)
- [License / usage terms](https://raw.githubusercontent.com/weiliangjinca/grcwa/HEAD/LICENSE)

### legume

ID: `legume` | Periodic structures & metasurfaces, Electromagnetics & devices

- **Physical method:** GME / PWE / differentiable eigenproblems
- **Purpose:** Photonic-crystal slabs, modes and radiative-loss analysis.
- **Programmable interface:** Python; automatic differentiation and optimization workflows.
- **Compute:** Local numerical computing.
- **License:** MIT
- **Application basis:** Fan group research software with methodological publications.
- **Limitations:** Specific expansions and truncations define the model; this is not a general 3D time-domain engine.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/fancompute/legume)
- [License / usage terms](https://raw.githubusercontent.com/fancompute/legume/HEAD/LICENSE)

### Ceviche

ID: `ceviche` | Electromagnetics & devices, Integrated photonics & layout

- **Physical method:** Differentiable FDFD / FDTD
- **Purpose:** Small-scale electromagnetic inverse design and automatic-differentiation research.
- **Programmable interface:** Python / Autograd; examples compose the solver with optimizers.
- **Compute:** Local CPU numerical computation.
- **License:** MIT
- **Application basis:** Research implementation accompanying automatic differentiation of Maxwell solvers.
- **Limitations:** Useful for prototypes and methods research, rather than a complete industrial 3D design environment.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/fancompute/ceviche)
- [License / usage terms](https://raw.githubusercontent.com/fancompute/ceviche/HEAD/LICENSE)

### tmm

ID: `tmm` | Thin films & materials

- **Physical method:** Transfer-matrix method
- **Purpose:** Planar multilayer reflection, transmission and absorption, including coherent and incoherent layer combinations.
- **Programmable interface:** Native Python / NumPy; coh_tmm, inc_tmm and related functions.
- **Compute:** CPU; straightforward parameter sweeps and optimization.
- **License:** MIT
- **Application basis:** Author-provided theory manual and thin-film absorption implementation.
- **Limitations:** The planar-layer model does not describe arbitrary lateral patterning, rough scattering or all finite-beam effects.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/sbyrnes321/tmm)
- [License / usage terms](https://raw.githubusercontent.com/sbyrnes321/tmm/HEAD/LICENSE.txt)

### Solcore

ID: `solcore` | Thin films & materials, Electromagnetics & devices

- **Physical method:** Solar-cell / semiconductor optoelectronic modeling
- **Purpose:** Material parameters, optical absorption and solar-cell device calculations.
- **Programmable interface:** Python API; composes transfer-matrix and other optical / electrical models.
- **Compute:** Local numerical computation; optional components may have separate dependencies.
- **License:** LGPL-3.0 family
- **Application basis:** Open research framework for solar-cell modeling with publications and examples.
- **Limitations:** Choose the optical and carrier-transport model appropriate to the device; optional external solvers have independent requirements.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Maintainer repository](https://github.com/qpv-research-group/solcore5)
- [Official documentation / website](https://docs.solcore.solar/en/latest/Optics/optics.html)
- [License / usage terms](https://raw.githubusercontent.com/qpv-research-group/solcore5/HEAD/LICENSE.txt)

### RayOptics

ID: `rayoptics` | Geometrical optics & lighting

- **Physical method:** Sequential ray tracing / imaging optics
- **Purpose:** Lens layouts, paraxial calculations, aberrations and optical-system analysis in Python.
- **Programmable interface:** Native Python; scripts, notebooks and optical-model objects.
- **Compute:** Local CPU.
- **License:** BSD-3-Clause
- **Application basis:** Public optical-design library with tutorials and lens examples.
- **Limitations:** Open access and programmability do not imply feature parity with every commercial tolerance or optimization tool.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/mjhoptics/ray-optics)
- [License / usage terms](https://raw.githubusercontent.com/mjhoptics/ray-optics/HEAD/LICENSE)

### Optiland

ID: `optiland` | Geometrical optics & lighting, Wave optics & propagation

- **Physical method:** Differentiable ray tracing / optical design
- **Purpose:** Lenses, freeform surfaces, polarization, coatings and differentiable imaging systems.
- **Programmable interface:** Native Python; NumPy / PyTorch backends; JSON and selected commercial-format interoperability.
- **Compute:** CPU / CUDA GPU; automatic differentiation.
- **License:** MIT
- **Application basis:** Actively developed optical-design platform with research and engineering examples.
- **Limitations:** Capabilities evolve quickly. File import or a familiar interface does not establish full commercial-product equivalence.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/optiland/optiland)
- [License / usage terms](https://raw.githubusercontent.com/optiland/optiland/HEAD/LICENSE)

### Raysect

ID: `raysect` | Geometrical optics & lighting, Scattering & particles

- **Physical method:** Physically based ray tracing / spectroscopy
- **Purpose:** Spectral light transport, optical geometry and synthetic diagnostics.
- **Programmable interface:** Python API with compiled numerical components; programmable scenes and observers.
- **Compute:** CPU; parallel sampling according to configuration.
- **License:** BSD-3-Clause
- **Application basis:** Research framework used for synthetic optical diagnostics, including fusion-related workflows.
- **Limitations:** A ray transport framework requires appropriate emission, material and detector models; coherent wave effects need separate treatment.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/raysect/source)
- [License / usage terms](https://raw.githubusercontent.com/raysect/source/HEAD/LICENSE.txt)

### DCC-Lab RayTracing

ID: `raytracing` | Geometrical optics & lighting, Lasers & precision interferometry

- **Physical method:** Paraxial ABCD / Gaussian optics
- **Purpose:** Teaching, first-order optical systems, ray bundles and Gaussian-beam propagation.
- **Programmable interface:** Python objects for matrices, elements, paths and analysis.
- **Compute:** Local CPU.
- **License:** MIT
- **Application basis:** DCC-Lab package with documented optical-system examples.
- **Limitations:** Paraxial optics cannot replace high-NA, strongly aberrated or full nonsequential models.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/DCC-Lab/RayTracing)
- [License / usage terms](https://raw.githubusercontent.com/DCC-Lab/RayTracing/HEAD/LICENSE)

### LightPipes

ID: `lightpipes` | Wave optics & propagation, Lasers & precision interferometry

- **Physical method:** Scalar wave propagation
- **Purpose:** Diffraction, interference, apertures and laser-beam propagation.
- **Programmable interface:** Native Python functions for field construction and propagation.
- **Compute:** Local CPU numerical arrays.
- **License:** BSD-3-Clause
- **Application basis:** Established wave-optics package with examples and reference documentation.
- **Limitations:** Respect scalar / paraxial assumptions and field-grid sampling; it is not a general vector Maxwell solver.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/opticspy/lightpipes)
- [License / usage terms](https://raw.githubusercontent.com/opticspy/lightpipes/HEAD/LICENSE.txt)

### POPPY

ID: `poppy` | Wave optics & propagation, Computational imaging

- **Physical method:** Physical optics propagation / PSFs
- **Purpose:** Fourier and Fresnel propagation through pupils and optical surfaces, especially astronomical imaging.
- **Programmable interface:** Python API and reusable optical elements; integrates with scientific Python.
- **Compute:** CPU; acceleration depends on optional array / FFT backends.
- **License:** BSD-3-Clause
- **Application basis:** Space Telescope Science Institute-associated physical-optics software with telescope applications.
- **Limitations:** Pupil sampling, propagation conventions and wavelength dependence must match the instrument model.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/spacetelescope/poppy)
- [License / usage terms](https://raw.githubusercontent.com/spacetelescope/poppy/HEAD/LICENSE.md)

### HCIPy

ID: `hcipy` | Wave optics & propagation, Computational imaging

- **Physical method:** High-contrast imaging / adaptive optics
- **Purpose:** Wavefront propagation, coronagraphy, turbulence, wavefront sensing and adaptive-optics modeling.
- **Programmable interface:** Native Python; composable fields, optical elements and estimators.
- **Compute:** Local numerical computing.
- **License:** MIT
- **Application basis:** Research framework with methods literature and high-contrast imaging examples.
- **Limitations:** A simulation does not provide a complete real-time instrument controller; model detector response and control timing explicitly.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/ehpor/hcipy)
- [License / usage terms](https://raw.githubusercontent.com/ehpor/hcipy/HEAD/LICENSE)

### prysm

ID: `prysm` | Wave optics & propagation, Geometrical optics & lighting, Computational imaging

- **Physical method:** Imaging optics / wavefronts / metrology
- **Purpose:** PSFs, MTFs, wavefront analysis and optical metrology calculations.
- **Programmable interface:** Native Python and numerical array interfaces.
- **Compute:** Local CPU; selected backends and features may support acceleration.
- **License:** MIT
- **Application basis:** Open optics library with engineering-oriented examples and documentation.
- **Limitations:** Define pupil coordinates, units and normalization before comparing data from different software.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/brandondube/prysm)
- [License / usage terms](https://raw.githubusercontent.com/brandondube/prysm/HEAD/LICENSE.md)

### Diffractio

ID: `diffractio` | Wave optics & propagation, Computational imaging

- **Physical method:** Scalar and vector diffraction
- **Purpose:** Diffraction, polarization and free-space propagation with multiple numerical methods.
- **Programmable interface:** Python API for scalar / vector sources, masks and fields.
- **Compute:** Local CPU; method-dependent multiprocessing.
- **License:** GPL-3.0
- **Application basis:** Research software with method documentation and examples.
- **Limitations:** Each propagation algorithm has its own approximation and sampling requirements; vector support alone is not full-wave device modeling.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/optbrea/diffractio)
- [License / usage terms](https://raw.githubusercontent.com/optbrea/diffractio/HEAD/LICENSE)

### TorchOptics

ID: `torchoptics` | Wave optics & propagation, Computational imaging

- **Physical method:** Differentiable wave optics
- **Purpose:** Optimize optical fields and systems jointly with numerical or learned reconstruction.
- **Programmable interface:** Native Python / PyTorch with automatic differentiation.
- **Compute:** CPU / GPU.
- **License:** MIT
- **Application basis:** Open differentiable-optics research framework.
- **Limitations:** Sampling and propagation assumptions still apply; a valid gradient does not guarantee a physically adequate forward model.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/MatthewFilipovich/torchoptics)
- [License / usage terms](https://raw.githubusercontent.com/MatthewFilipovich/torchoptics/HEAD/LICENSE)

### waveprop

ID: `waveprop` | Wave optics & propagation, Computational imaging

- **Physical method:** Numerical diffraction propagation
- **Purpose:** Fresnel, Fraunhofer and angular-spectrum propagation for imaging and holography experiments.
- **Programmable interface:** Python; selected PyTorch differentiable implementations.
- **Compute:** CPU / GPU depending on method and backend.
- **License:** MIT
- **Application basis:** Open wave-propagation package with research examples.
- **Limitations:** Check band limits, aliasing and the assumptions of the selected propagation approximation.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/ebezzam/waveprop)
- [License / usage terms](https://raw.githubusercontent.com/ebezzam/waveprop/HEAD/LICENSE)

### gdsfactory

ID: `gdsfactory` | Integrated photonics & layout

- **Physical method:** Parametric layout / PDK / photonic design
- **Purpose:** Build reusable photonic components, routing, layouts and simulation connections.
- **Programmable interface:** Native Python, PCells, PDKs, netlists and solver adapters; official component-designer Skill.
- **Compute:** Local layout; external solvers and commercial services have separate execution environments.
- **License:** MIT core; commercial services, external PDKs and solvers licensed separately
- **Application basis:** Open PIC design ecosystem with fabrication and foundry-related workflows.
- **Limitations:** The open core does not license external PDKs or proprietary solvers; geometry alone does not establish device performance.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (official):** [Official gdsfactory component-designer Skill](https://github.com/gdsfactory/gdsfactory/blob/main/.agents/skills/gdsfactory-component-designer/SKILL.md)

Sources:
- [API / project documentation](https://github.com/gdsfactory/gdsfactory)
- [License / usage terms](https://raw.githubusercontent.com/gdsfactory/gdsfactory/HEAD/LICENSE)

### KLayout

ID: `klayout` | Integrated photonics & layout

- **Physical method:** Layout editing / DRC / LVS
- **Purpose:** Inspect and process chip layouts and run geometric / connectivity verification.
- **Programmable interface:** Python / Ruby APIs, macros, batch mode and the Python module.
- **Compute:** Local CPU; GUI or headless workflows.
- **License:** GPL-3.0
- **Application basis:** Established layout and verification software used in semiconductor and photonic design.
- **Limitations:** DRC / LVS check layout rules and connectivity, not the optical performance of a device.
- **MCP (community):** [Community klayout-draw-mcp; Python-module layout operations](https://github.com/geniuskey/klayout-draw-mcp)
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/KLayout/klayout)
- [License / usage terms](https://raw.githubusercontent.com/KLayout/klayout/HEAD/LICENSE)

### SAX

ID: `sax` | Integrated photonics & layout

- **Physical method:** Differentiable photonic circuits
- **Purpose:** Compose frequency-dependent scattering models and optimize photonic circuits.
- **Programmable interface:** Python / JAX; callable component models and netlists.
- **Compute:** CPU / GPU through JAX.
- **License:** Apache-2.0
- **Application basis:** Open photonic circuit-modeling library used in the gdsfactory ecosystem.
- **Limitations:** Port conventions, reference planes, phase and normalization must agree across compact models.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/flaport/sax)
- [License / usage terms](https://raw.githubusercontent.com/flaport/sax/HEAD/LICENSE)

### SiEPIC-Tools

ID: `siepic` | Integrated photonics & layout

- **Physical method:** Silicon photonics design tools
- **Purpose:** KLayout-based photonic layout, routing, verification and design workflows.
- **Programmable interface:** Python macros and KLayout extensions; integrates with PDKs and simulation tools.
- **Compute:** Local KLayout / Python environment.
- **License:** MIT; PDKs licensed separately
- **Application basis:** SiEPIC research and education ecosystem for silicon photonics.
- **Limitations:** Core tooling, PDKs and linked commercial circuit solvers have separate licenses and model coverage.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/SiEPIC/SiEPIC-Tools)
- [License / usage terms](https://raw.githubusercontent.com/SiEPIC/SiEPIC-Tools/HEAD/LICENSE.md)

### Nazca Design

ID: `nazca` | Integrated photonics & layout

- **Physical method:** Parametric photonic layout
- **Purpose:** Python-defined photonic components, routing and mask layouts.
- **Programmable interface:** Native Python; reusable building blocks and PDK interfaces.
- **Compute:** Local layout generation.
- **License:** AGPL-3.0-or-later; commercial services and PDKs are separate
- **Application basis:** Open photonic design framework with documented PDK and design workflows.
- **Limitations:** The core is AGPL-licensed; commercial services and external PDKs are separate. Layout generation is not an optical solve.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [License / usage terms](https://nazca-design.org/about/)
- [Official documentation / website](https://nazca-design.org/manual/introduction.html)

### ADDA

ID: `adda` | Scattering & particles, Electromagnetics & devices

- **Physical method:** Discrete dipole approximation
- **Purpose:** Scattering and absorption by particles with complex shape or material distributions.
- **Programmable interface:** Command-line solver, input geometry and material files; scripts can drive sweeps and parse results.
- **Compute:** CPU / MPI; OpenCL acceleration in supported builds.
- **License:** GPL-3.0
- **Application basis:** Established DDA research code with methods publications.
- **Limitations:** Converge the dipole discretization and solver tolerance; large refractive contrast and size can increase computational cost.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/adda-team/adda)
- [License / usage terms](https://raw.githubusercontent.com/adda-team/adda/HEAD/LICENSE)

### miepython

ID: `miepython` | Scattering & particles

- **Physical method:** Mie scattering
- **Purpose:** Scattering, absorption and angular patterns of spherical particles.
- **Programmable interface:** Native Python functions and array-oriented calculations.
- **Compute:** Local CPU.
- **License:** MIT
- **Application basis:** Open Mie-scattering implementation with theory and examples.
- **Limitations:** The standard model assumes spheres and its stated material / embedding-medium conditions.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/scottprahl/miepython)
- [License / usage terms](https://raw.githubusercontent.com/scottprahl/miepython/HEAD/LICENSE.txt)

### treams

ID: `treams` | Scattering & particles, Periodic structures & metasurfaces

- **Physical method:** T-matrix / multipole scattering
- **Purpose:** Electromagnetic scattering, translations and periodic arrangements using multipole expansions.
- **Programmable interface:** Python API for bases, translation operators and scattering matrices.
- **Compute:** Local CPU numerical linear algebra.
- **License:** MIT
- **Application basis:** Research implementation with T-matrix methods documentation.
- **Limitations:** Basis truncation, particle models and translation conventions control accuracy and applicability.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/tfp-photonics/treams)
- [License / usage terms](https://raw.githubusercontent.com/tfp-photonics/treams/HEAD/LICENSE)

### SMUTHI

ID: `smuthi` | Scattering & particles, Thin films & materials

- **Physical method:** Multiple scattering near layered media
- **Purpose:** Scattering by particles interacting with planar layered environments.
- **Programmable interface:** Python API for particles, layers, illumination and simulations.
- **Compute:** CPU; optional acceleration depends on dependencies.
- **License:** MIT
- **Application basis:** Research software for scattering by complex particles near interfaces.
- **Limitations:** Respect the supported particle models, planar-layer assumptions and multipole convergence conditions.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [License / usage terms](https://smuthi.readthedocs.io/en/latest/_source/01%20about/about_smuthi.html)
- [Maintainer repository](https://github.com/KMCzajkowski/smuthi)

### pyGDM

ID: `pygdm` | Electromagnetics & devices, Scattering & particles

- **Physical method:** Green dyadic method
- **Purpose:** Nanophotonic scattering, near fields and inverse-design research.
- **Programmable interface:** Python API, programmable geometries, materials and optimization workflows.
- **Compute:** CPU; acceleration and parallelism depend on numerical configuration.
- **License:** GPL-3.0 family
- **Application basis:** Open research toolbox with methods publications and tutorials.
- **Limitations:** Discretization and the Green-function environment define the physical model; confirm convergence and material assumptions.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Methods publication](https://wiechapeter.gitlab.io/)
- [API / project documentation](https://homepages.laas.fr/pwiecha/pygdm_doc/apidoc.html)
- [Official documentation / website](https://gitlab.com/wiechapeter/pyGDM2)

### QuTiP

ID: `qutip` | Quantum optics, Lasers & precision interferometry

- **Physical method:** Open quantum systems
- **Purpose:** Quantum states, density matrices, master equations, dynamics and quantum-optics observables.
- **Programmable interface:** Native Python; quantum objects, solvers and numerical interfaces.
- **Compute:** CPU; optional solver backends and parallel workflows.
- **License:** BSD-3-Clause
- **Application basis:** Established open quantum-dynamics ecosystem with research publications.
- **Limitations:** Hilbert-space truncation and the validity of the chosen Hamiltonian / dissipators must be justified.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/qutip/qutip)
- [License / usage terms](https://raw.githubusercontent.com/qutip/qutip/HEAD/LICENSE.txt)

### QuantumOptics.jl

ID: `quantumoptics` | Quantum optics

- **Physical method:** Quantum optics / open-system dynamics
- **Purpose:** Quantum operators, states, dissipation and time evolution in Julia.
- **Programmable interface:** Native Julia API; composable bases, operators and solvers.
- **Compute:** Local numerical computing; Julia ecosystem integration.
- **License:** MIT
- **Application basis:** QuantumOptics.jl research framework with documented quantum-optics examples.
- **Limitations:** Specify the physical Hamiltonian, dissipation and basis truncation; classical fields do not directly replace quantum states.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/qojulia/QuantumOptics.jl)
- [License / usage terms](https://raw.githubusercontent.com/qojulia/QuantumOptics.jl/HEAD/LICENSE.md)

### Perceval

ID: `perceval` | Quantum optics, Integrated photonics & layout

- **Physical method:** Discrete-variable photonic quantum circuits
- **Purpose:** Linear-optical circuits, photon-counting states and photonic quantum algorithms.
- **Programmable interface:** Python API; local backends and separately configured remote services.
- **Compute:** Local simulators; remote hardware / services have separate terms.
- **License:** MIT local software; remote services have separate terms
- **Application basis:** Quandela open photonic quantum-computing framework.
- **Limitations:** The simulator and a physical quantum processor are different resources; noise and device models require explicit configuration.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/Quandela/Perceval)
- [License / usage terms](https://raw.githubusercontent.com/Quandela/Perceval/HEAD/LICENSE)

### Strawberry Fields

ID: `strawberry` | Quantum optics, Integrated photonics & layout

- **Physical method:** Continuous-variable quantum photonics
- **Purpose:** Gaussian and non-Gaussian photonic quantum circuits and algorithms.
- **Programmable interface:** Python API, circuit programs and simulation backends.
- **Compute:** Local computation; backend-dependent acceleration.
- **License:** Apache-2.0
- **Application basis:** Xanadu open continuous-variable quantum-photonics framework.
- **Limitations:** Check supported Python / dependency versions. Fock cutoffs and backend assumptions affect accuracy and scale.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/XanaduAI/strawberryfields)
- [License / usage terms](https://raw.githubusercontent.com/XanaduAI/strawberryfields/HEAD/LICENSE)

### Luna.jl

ID: `luna` | Fibers & communications, Lasers & precision interferometry

- **Physical method:** Nonlinear ultrafast pulse propagation
- **Purpose:** Broadband pulse propagation, nonlinear fibers and related ultrafast dynamics.
- **Programmable interface:** Native Julia API and scripted models.
- **Compute:** CPU; parallel calculations according to configuration.
- **License:** MIT
- **Application basis:** Ultrafast research package with documented propagation models and publications.
- **Limitations:** Choose envelope or field-resolved formulations consistently with bandwidth, dispersion and nonlinearity.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/LupoLab/Luna.jl)
- [License / usage terms](https://raw.githubusercontent.com/LupoLab/Luna.jl/HEAD/LICENSE)

### py-fmas

ID: `pyfmas` | Fibers & communications, Lasers & precision interferometry

- **Physical method:** Forward-model pulse propagation
- **Purpose:** Research on nonlinear pulse propagation in dispersive waveguides.
- **Programmable interface:** Python classes for propagation models, grids and solvers.
- **Compute:** Local CPU numerical computation.
- **License:** MIT
- **Application basis:** Open research implementation with analytic-signal-based propagation methods.
- **Limitations:** The forward-propagation assumption and chosen material model delimit the physical regime.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/omelchert/py-fmas)
- [License / usage terms](https://raw.githubusercontent.com/omelchert/py-fmas/HEAD/LICENSE.md)

### laserfun

ID: `laserfun` | Fibers & communications, Lasers & precision interferometry

- **Physical method:** Nonlinear fiber pulse propagation
- **Purpose:** Numerical pulse evolution and supercontinuum-related modeling.
- **Programmable interface:** Python interface for pulses, fibers and nonlinear propagation.
- **Compute:** Local CPU.
- **License:** MIT
- **Application basis:** Open pulse-propagation package with examples.
- **Limitations:** Use measured dispersion and nonlinear parameters; verify temporal resolution and applicability of the propagation model.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/laserfun/laserfun)
- [License / usage terms](https://raw.githubusercontent.com/laserfun/laserfun/HEAD/LICENSE)

### OptiCommPy

ID: `opticomm` | Fibers & communications

- **Physical method:** Optical communications / DSP
- **Purpose:** Coherent transmission, channel models, modulation, receivers and digital signal processing.
- **Programmable interface:** Native Python with modular transmitter, channel and DSP functions.
- **Compute:** CPU; selected numerical acceleration depends on dependencies.
- **License:** GPL-3.0
- **Application basis:** Research and education software for optical communication systems.
- **Limitations:** System models require consistent units, sample rates and noise conventions; they do not resolve every device electromagnetically.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/edsonportosilva/OptiCommPy)
- [License / usage terms](https://raw.githubusercontent.com/edsonportosilva/OptiCommPy/HEAD/LICENSE)

### Finesse 3

ID: `finesse` | Lasers & precision interferometry, Wave optics & propagation, Quantum optics

- **Physical method:** Frequency-domain interferometers / Gaussian modes
- **Purpose:** Laser interferometers, cavities, mode mismatch and noise-related optical responses.
- **Programmable interface:** Python API and KatScript model language; programmable analyses.
- **Compute:** Local numerical computing.
- **License:** GPL-3.0 family
- **Application basis:** Research software developed around precision interferometry and gravitational-wave instrumentation.
- **Limitations:** Frequency-domain / modal assumptions and truncation differ from general transient full-wave modeling.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://finesse.ifosim.org/docs/latest/)
- [Official documentation / website](https://finesse.docs.ligo.org/finesse-ligo/index.html)
- [Official documentation / website](https://git.ligo.org/finesse/finesse3)

### reZonator 2

ID: `rezonator` | Lasers & precision interferometry, Geometrical optics & lighting

- **Physical method:** Gaussian-beam / laser-resonator design
- **Purpose:** Resonator stability, Gaussian beams and first-order optical systems.
- **Programmable interface:** Desktop GUI and project files; a complete stable headless API was not verified.
- **Compute:** Local desktop application.
- **License:** GPL-3.0
- **Application basis:** Open laser-resonator analysis software with documentation.
- **Limitations:** Paraxial models do not resolve arbitrary aberrations or nonlinear pulse dynamics.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Maintainer repository](https://github.com/orion-project/rezonator2)
- [License / usage terms](https://raw.githubusercontent.com/orion-project/rezonator2/HEAD/LICENSE)

### MCX

ID: `mcx` | Biomedical photon transport, Scattering & particles

- **Physical method:** GPU Monte Carlo photon transport
- **Purpose:** Light propagation, fluence and time-resolved transport in scattering tissue.
- **Programmable interface:** Command-line / JSON configurations and language bindings; programmable batch simulations.
- **Compute:** GPU transport; supported hardware and backends depend on the build.
- **License:** GPL-3.0
- **Application basis:** Established biomedical photon-transport research software.
- **Limitations:** Standard photon packets track transport statistics rather than coherent optical phase; do not use them directly for interference.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/fangq/mcx)
- [License / usage terms](https://raw.githubusercontent.com/fangq/mcx/HEAD/LICENSE.txt)

### MMC

ID: `mmc` | Biomedical photon transport, Scattering & particles

- **Physical method:** Mesh-based Monte Carlo photon transport
- **Purpose:** Photon transport through tissue represented by tetrahedral meshes.
- **Programmable interface:** Command-line / configuration files and language bindings.
- **Compute:** CPU; acceleration depends on the selected implementation.
- **License:** GPL-3.0
- **Application basis:** Research code for mesh-based biomedical optical transport.
- **Limitations:** Mesh quality, boundary models and tissue parameters determine validity; standard transport does not preserve coherent phase.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/fangq/mmc)
- [License / usage terms](https://raw.githubusercontent.com/fangq/mmc/HEAD/LICENSE.txt)

### HoloPy

ID: `holopy` | Computational imaging, Scattering & particles

- **Physical method:** Computational holography / scattering inference
- **Purpose:** Model holograms and infer particle or sample parameters from measured images.
- **Programmable interface:** Python API connecting scattering calculations, image handling and inference.
- **Compute:** Local CPU; dependencies and scattering backend determine parallel support.
- **License:** GPL-3.0
- **Application basis:** Research software for digital holography and particle characterization.
- **Limitations:** Match the scattering model, illumination, imaging geometry and noise to the measured hologram.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/manoharan-lab/holopy)
- [License / usage terms](https://raw.githubusercontent.com/manoharan-lab/holopy/HEAD/LICENSE)

### pyDHM

ID: `pydhm` | Computational imaging, Wave optics & propagation

- **Physical method:** Digital holographic microscopy
- **Purpose:** Numerical reconstruction, propagation, phase shifting and aberration compensation.
- **Programmable interface:** Native Python functions for holographic processing.
- **Compute:** Local CPU.
- **License:** MIT
- **Application basis:** Research package and accompanying digital-holographic-microscopy publication.
- **Limitations:** Reconstruction choices depend on acquisition geometry, sampling and reference-wave configuration.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Maintainer repository](https://github.com/catrujilla/pyDHM)
- [Official documentation / website](https://catrujilla.github.io/pyDHM/)
- [Methods publication](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0275818)

### PyNX

ID: `pynx` | Computational imaging, X-rays & beamlines

- **Physical method:** Coherent diffraction / ptychography reconstruction
- **Purpose:** GPU reconstruction and processing of coherent diffraction imaging experiments.
- **Programmable interface:** Python API and command-line reconstruction tools.
- **Compute:** GPU through supported CUDA / OpenCL environments.
- **License:** CeCILL-B
- **Application basis:** ESRF coherent-imaging research software.
- **Limitations:** Match the observation model, detector geometry, coherence assumptions and experimental metadata to the reconstruction.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [License / usage terms](https://pynx.esrf.fr/en/stable/)
- [Official documentation / website](https://pynx.esrf.fr/en/stable/scripts/)

### Mitsuba 3

ID: `mitsuba` | Geometrical optics & lighting, Computational imaging

- **Physical method:** Physically based / differentiable rendering
- **Purpose:** Radiometric light transport, inverse rendering and programmable materials / sensors.
- **Programmable interface:** Python / C++ API; differentiable variants through Dr.Jit.
- **Compute:** CPU / GPU depending on the selected variant.
- **License:** BSD-3-Clause
- **Application basis:** Open rendering research framework with methods publications.
- **Limitations:** Path tracing and differentiability do not imply a complete coherent wave-optics model.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/mitsuba-renderer/mitsuba3)
- [License / usage terms](https://raw.githubusercontent.com/mitsuba-renderer/mitsuba3/HEAD/LICENSE)

### PBRT v4

ID: `pbrt` | Geometrical optics & lighting, Computational imaging

- **Physical method:** Physically based spectral rendering
- **Purpose:** Research-grade scene rendering with physical light transport, materials and cameras.
- **Programmable interface:** C++ source, scene descriptions and command-line execution.
- **Compute:** CPU / GPU depending on build and scene support.
- **License:** Apache-2.0
- **Application basis:** Reference implementation accompanying Physically Based Rendering.
- **Limitations:** A scene description is not a general lens-design or coherent-wave solver; match camera and material models to the experiment.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/mmp/pbrt-v4)
- [License / usage terms](https://raw.githubusercontent.com/mmp/pbrt-v4/HEAD/LICENSE.txt)

### SRW

ID: `srw` | X-rays & beamlines, Wave optics & propagation

- **Physical method:** Synchrotron radiation / wavefront propagation
- **Purpose:** Radiation from synchrotron sources and propagation through X-ray beamlines.
- **Programmable interface:** Python interface and scripted radiation / propagation models.
- **Compute:** CPU; parallel workflows depend on configuration.
- **License:** BSD-3-Clause; Python execution does not require IGOR Pro
- **Application basis:** Established synchrotron-radiation research software.
- **Limitations:** Select source, coherence and propagation approximations appropriate to the beamline; Python use does not require IGOR Pro.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/ochubar/SRW)
- [License / usage terms](https://pypi.org/project/oasys-srwpy/1.0.3/)

### SHADOW4 / OASYS

ID: `shadow` | X-rays & beamlines, Geometrical optics & lighting

- **Physical method:** X-ray ray tracing / beamline workflows
- **Purpose:** Mirrors, crystals, gratings and beam transport in synchrotron beamlines; OASYS supplies graphical workflows.
- **Programmable interface:** Native SHADOW4 Python; OASYS plugins; batch simulations can be scripted.
- **Compute:** Local Python; graphical workflow is optional.
- **License:** SHADOW4: MIT; OASYS and plugins have their own licenses
- **Application basis:** Synchrotron optics tools maintained by the OASYS project organization.
- **Limitations:** OASYS is an integration environment, not a single solver; wave effects need the corresponding models or hybrid methods.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Maintainer repository](https://github.com/oasys-kit/shadow4)
- [License / usage terms](https://github.com/oasys-kit/shadow4/blob/master/LICENSE)
- [Maintainer repository](https://github.com/oasys-kit/OASYS1-shadow4)

### xrt

ID: `xrt` | X-rays & beamlines, Geometrical optics & lighting, Wave optics & propagation

- **Physical method:** X-ray ray and wave tracing
- **Purpose:** Synchrotron sources, crystals, mirrors and beamline calculations.
- **Programmable interface:** Python; programmable beamlines and batch analysis.
- **Compute:** CPU; selected calculations use OpenCL.
- **License:** MIT
- **Application basis:** Public X-ray optics research software and documentation.
- **Limitations:** Crystal diffraction, source models and statistical sampling have distinct validity limits; this is not a general full-wave grid solver.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/kklmn/xrt)
- [License / usage terms](https://raw.githubusercontent.com/kklmn/xrt/HEAD/LICENSE.txt)

### SymPy

ID: `sympy` | Derivation & digital foundations

- **Physical method:** Symbolic algebra
- **Purpose:** Derive Jones / ABCD matrices, dispersion relations, derivatives, integrals and approximations.
- **Programmable interface:** Python; numerical-function and code generation.
- **Compute:** CPU.
- **License:** BSD-3-Clause
- **Application basis:** General symbolic-computing library with a software publication.
- **Limitations:** Make domains, branches and approximation conditions explicit; the library does not automatically provide a complete optical model.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/sympy/sympy)
- [License / usage terms](https://raw.githubusercontent.com/sympy/sympy/HEAD/LICENSE)

### SageMath

ID: `sage` | Derivation & digital foundations

- **Physical method:** Mathematical computing system
- **Purpose:** Algebra, equations, symbolic and numerical research for more complex theoretical derivations.
- **Programmable interface:** Python-style interface, CLI and notebooks.
- **Compute:** Local mathematical computing environment.
- **License:** GPL family; bundled components retain their respective licenses
- **Application basis:** Long-maintained open mathematical software.
- **Limitations:** Theoretical computing infrastructure rather than a ready-made optical design application.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://www.sagemath.org/)

### FreeCAD

ID: `freecad` | Derivation & digital foundations, Geometrical optics & lighting

- **Physical method:** Parametric mechanical CAD
- **Purpose:** Optomechanical supports, packaging, assemblies and manufacturable geometry for simulation.
- **Programmable interface:** Python API, macros and plugins.
- **Compute:** Local CAD with scripted modeling.
- **License:** LGPL-2.1 family; components may have additional licenses
- **Application basis:** Established open engineering CAD project.
- **Limitations:** CAD geometry does not automatically specify optical surfaces, materials or boundary conditions; semantic conversion is required.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/FreeCAD/FreeCAD)
- [License / usage terms](https://raw.githubusercontent.com/FreeCAD/FreeCAD/HEAD/LICENSE)

### Gmsh

ID: `gmsh` | Derivation & digital foundations, Electromagnetics & devices

- **Physical method:** Geometry / finite-element meshing
- **Purpose:** Controlled meshes for optical FEM, thermal and structural models.
- **Programmable interface:** Python, C, C++ and Julia APIs; CLI and .geo scripts.
- **Compute:** Local CPU.
- **License:** GPL; commercial relicensing available separately
- **Application basis:** Established research meshing software.
- **Limitations:** Mesh generation still requires a field / thermal solver and explicit physical boundary conditions.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [License / usage terms](https://gmsh.info/)
- [Official manual](https://gmsh.info/doc/texinfo/)

### scikit-image

ID: `scikitimage` | Computational imaging, Derivation & digital foundations

- **Physical method:** Image processing / reconstruction algorithms
- **Purpose:** Filter, segment, register, transform and quantify experimental images.
- **Programmable interface:** Native Python API.
- **Compute:** Local CPU.
- **License:** Primarily BSD-3-Clause; see the license inventory for individual files
- **Application basis:** Scientific image-processing ecosystem with software publications.
- **Limitations:** Image enhancement is not proof of recovered physical information; connect processing to imaging and noise models.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/scikit-image/scikit-image)
- [License / usage terms](https://raw.githubusercontent.com/scikit-image/scikit-image/HEAD/LICENSE.txt)

### napari

ID: `napari` | Computational imaging, Derivation & digital foundations

- **Physical method:** Multidimensional image visualization / plugins
- **Purpose:** Inspect images, volumes, labels and reconstruction results; develop analysis plugins.
- **Programmable interface:** Python API, CLI and plugin system.
- **Compute:** Qt / GPU visualization; analysis depends on plugins.
- **License:** BSD-3-Clause
- **Application basis:** Open scientific imaging ecosystem.
- **Limitations:** An application plugin is not automatically an agent Skill. Call analysis libraries directly for batch computation.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/napari/napari)
- [License / usage terms](https://raw.githubusercontent.com/napari/napari/HEAD/LICENSE)

### refractiveindex.info database

ID: `refractiveindex` | Derivation & digital foundations, Thin films & materials, Electromagnetics & devices

- **Physical method:** Optical constants database
- **Purpose:** Refractive index, extinction coefficient and source literature for optical material models.
- **Programmable interface:** Machine-readable YAML, accessible from Python and other languages; a database rather than a solver.
- **Compute:** Local data or website lookup.
- **License:** CC0 database; source publications retain their own rights
- **Application basis:** Public optical constants database with literature provenance.
- **Limitations:** Match wavelength, temperature, sample and measurement conditions; the same material name does not guarantee interchangeable n and k.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Maintainer repository](https://github.com/polyanskiy/refractiveindex.info-database)
- [License / usage terms](https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/HEAD/LICENSE)
- [Official documentation / website](https://refractiveindex.info/)

### FEniCSx / DOLFINx

ID: `fenics` | Electromagnetics & devices, Derivation & digital foundations

- **Physical method:** Custom FEM / partial differential equations
- **Purpose:** Implement Helmholtz, Maxwell and thermal research models using variational formulations.
- **Programmable interface:** Python / C++; UFL weak forms; MPI and numerical backends.
- **Compute:** CPU / MPI; complex-number support depends on the build.
- **License:** DOLFINx: LGPL-3.0-or-later; components licensed separately
- **Application basis:** Official FEniCS open finite-element environment and methods documentation.
- **Limitations:** Choose correct function spaces, weak forms and boundaries; it is not a turnkey replacement for an application-specific multiphysics product.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Maintainer repository](https://github.com/FEniCS/dolfinx)
- [Official documentation / website](https://fenicsproject.org/)

### Netgen / NGSolve

ID: `ngsolve` | Electromagnetics & devices, Derivation & digital foundations

- **Physical method:** High-order FEM / electromagnetics / multiphysics
- **Purpose:** Electromagnetic modes and custom coupled equations, with Netgen meshing.
- **Programmable interface:** Python / C++; official Maxwell and eigenmode tutorials.
- **Compute:** Local / parallel computation.
- **License:** LGPL-2.1; consult individual component licenses
- **Application basis:** Official electromagnetic and multiphysics tutorials and research implementations.
- **Limitations:** Requires explicit spaces, materials and boundaries; its strength is control over equations and numerical methods.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Maintainer repository](https://github.com/NGSolve/ngsolve)
- [Maxwell tutorial](https://ngsolve.org/ngsolve/docs/i-tutorials/unit-2.4-Maxwell/Maxwellevp.html)

### NumPy / SciPy

ID: `scipy` | Derivation & digital foundations, Computational imaging

- **Physical method:** Arrays / optimization / fitting / signals
- **Purpose:** Optical data processing, fitting, ODEs, FFTs, optimization and statistics underpin many specialized libraries.
- **Programmable interface:** Native Python; NumPy arrays and scipy.optimize, integrate, signal and other modules.
- **Compute:** Local CPU; selected functionality supports other array backends.
- **License:** BSD family; dependencies and components retain their own licenses
- **Application basis:** Long-maintained scientific Python infrastructure.
- **Limitations:** Numerical algorithms do not define an instrument or its optical physics; construct objectives from the relevant physical models.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://numpy.org/)
- [Official documentation / website](https://scipy.org/)

### JAX

ID: `jax` | Derivation & digital foundations

- **Physical method:** Automatic differentiation / JIT / numerics
- **Purpose:** Develop differentiable optical solvers, optimizers and surrogates; used by FDTDX and SAX.
- **Programmable interface:** Python; jit, grad, vmap and related transformations.
- **Compute:** CPU / GPU / TPU depending on the installation.
- **License:** Apache-2.0
- **Application basis:** Open numerical and machine-learning infrastructure.
- **Limitations:** Automatic differentiation does not remove discretization or model error; match complex derivatives, precision and memory to the physics.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official documentation / website](https://docs.jax.dev/en/latest/)
- [Source repository](https://github.com/jax-ml/jax)

### PyTorch

ID: `pytorch` | Derivation & digital foundations, Computational imaging

- **Physical method:** Tensors / automatic differentiation / surrogates
- **Purpose:** Develop joint optics-algorithm models, inverse networks and fast surrogates; used by torcwa and TorchOptics.
- **Programmable interface:** Python / C++; Autograd and GPU tensor interfaces.
- **Compute:** CPU / GPU depending on hardware and backend.
- **License:** BSD family; see the license inventory for third-party components
- **Application basis:** Established machine-learning and scientific-computing infrastructure.
- **Limitations:** Establish surrogate error and valid parameter ranges independently; a network output is not automatically a physical solution.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Official product / platform](https://pytorch.org/)
- [Source repository](https://github.com/pytorch/pytorch)

## Free / restricted

### PhotonForge Community

ID: `photonforge` | Integrated photonics & layout

- **Physical method:** PIC design / circuits / layout verification
- **Purpose:** Local layout, schematics, routing and circuit simulation, with links to Tidy3D device models.
- **Programmable interface:** Native Python; official agent plugins and PCell, routing and verification Skills.
- **Compute:** Local Python; DRC / LVS use KLayout; device solvers run in the cloud.
- **License:** Community local features are free, including commercial use; this does not establish an open-source platform; cloud device solves are paid
- **Application basis:** Official Flexcompute 2.0 documentation separates free local features from paid cloud computation.
- **Limitations:** The official MCP includes documentation retrieval. Actual model execution often uses Python run by the agent.
- **MCP (official):** [Official PhotonForge documentation MCP, used alongside Python execution](https://github.com/flexcompute/plugin-marketplace)
- **Agent Skill (official):** [Official PCell, verification, circuit, version and serialization Skills](https://github.com/flexcompute/plugin-marketplace)

Sources:
- [Free / paid feature boundaries](https://docs.flexcompute.com/projects/photonforge/en/latest/getting_started.html)
- [Agent plugins / Skills](https://github.com/flexcompute/plugin-marketplace)

### OSLO EDU

ID: `osloedu` | Geometrical optics & lighting

- **Physical method:** Educational lens design
- **Purpose:** Free learning environment for lens layouts, ray tracing and basic analysis.
- **Programmable interface:** Commands / macros within EDU limits; do not assume all commercial-edition interfaces are available.
- **Compute:** Windows desktop.
- **License:** Free proprietary educational edition; limited features; no course enrollment required according to the vendor
- **Application basis:** Lambda Research official free edition.
- **Limitations:** Suited to teaching and small models; not an equivalent replacement for a complete industrial lens-design environment.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [Free / paid feature boundaries](https://lambdares.com/edu)

### PtyPy

ID: `ptypy` | Computational imaging, X-rays & beamlines

- **Physical method:** Ptychographic phase retrieval
- **Purpose:** Iterative reconstruction and experimental data processing for scanning coherent diffraction imaging.
- **Programmable interface:** Python, MPI and CUDA / CuPy acceleration engines.
- **Compute:** Local / MPI / GPU, depending on the selected engine.
- **License:** Academic License: academic and noncommercial use only; source-available, with field-of-use restrictions
- **Application basis:** The project includes publications, experimental reconstruction templates and parallel implementations.
- **Limitations:** Commercial R&D, commissioned work and service use cannot simply be treated like ordinary MIT / BSD software.
- **MCP (unverified):** Dedicated MCP not verified in this review
- **Agent Skill (unverified):** Dedicated agent Skill not verified in this review

Sources:
- [API / project documentation](https://github.com/ptycho/ptypy)
- [License / usage terms](https://raw.githubusercontent.com/ptycho/ptypy/HEAD/LICENSE)

