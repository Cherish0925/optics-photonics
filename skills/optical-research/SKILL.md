---
name: optical-research
description: Select optical and photonic software and mathematical representations for research: ray, wave, Maxwell, thin films, PICs, fibers, lasers, scattering, quantum optics, tissue optics, X-rays, imaging and materials.
---

# Optical research

Start with the observable and the physical representation. A focal spot, scattering matrix, photon arrival distribution and density matrix require different models. State wavelength range, length scales, coherence, polarization, material response and intended accuracy before selecting a solver.

Use `software_search` to find candidates, then `software_details` for the selected software. The catalogue distinguishes open, paid and limited licenses. A documented API, an installed environment and an executed calculation are separate properties. Upstream documentation MCPs do not necessarily run a solver.

Read only the relevant domain reference below. Each gives the variables to transfer between programs and the numerical questions that change a conclusion.

- Ray and illumination: [ray](references/ray.md).
- Diffraction and wavefronts: [wave](references/wave.md).
- Full-wave electromagnetics: [em](references/em.md).
- Periodic media and modes: [periodic](references/periodic.md).
- Thin films and materials: [film](references/film.md).
- Photonic circuits and layout: [pic](references/pic.md).
- Fiber propagation: [fiber](references/fiber.md).
- Lasers and resonators: [laser](references/laser.md).
- Particle scattering: [scatter](references/scatter.md).
- Quantum optical systems: [quantum](references/quantum.md).
- Tissue optics: [bio](references/bio.md).
- X-ray sources and beamlines: [xray](references/xray.md).
- Imaging and inverse problems: [imaging](references/imaging.md).
- Shared numerical and material tools: [foundation](references/foundation.md).

Use the native software API when the research requires functions beyond the packaged examples. Keep equations, assumptions, material sources and units with the calculation. For installation and execution, use the optical-computation Skill. Ask a person for physical geometry, license access or experimental conditions only when they cannot be obtained from the supplied project.
