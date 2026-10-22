# Foundations: Field · Matter · Interaction

[中文](README.zh-CN.md) · [English HTML](../docs/foundations.html) · [中文 HTML](../docs/foundations.zh.html)

## The compact model

For optics and photonics, the most useful general decomposition is

\[
\boxed{\text{Optics / Photonics} = \text{Field} + \text{Matter} + \text{Interaction}}
\]

This is an organizing principle, not a replacement for Maxwell theory, quantum electrodynamics, solid-state physics, statistical mechanics or device engineering. Its value is that the same three-part structure survives across wavelengths, scales, classical and quantum descriptions, scientific research and engineered systems.

A slightly more explicit dynamical form is

\[
H = H_{\mathrm{field}} + H_{\mathrm{matter}} + H_{\mathrm{int}}
    + H_{\mathrm{drive}} + H_{\mathrm{env}},
\]

or, in classical continuum language,

\[
\text{Maxwell dynamics} + \text{constitutive response} + \text{sources and boundaries}.
\]

Free-space propagation belongs to the field's own dynamics. Sources, detectors, modulators, gain media, samples and optical components are matter systems coupled to the field. Geometry enters mainly through the spatial structure of matter, interfaces, boundaries and background space.

## 1. Field

The field is the optical degree of freedom itself.

At the classical level it is the electromagnetic field, represented by quantities such as

\[
\mathbf E(\mathbf r,t),\quad
\mathbf B(\mathbf r,t),\quad
\mathbf D(\mathbf r,t),\quad
\mathbf H(\mathbf r,t).
\]

At the quantum level it is the quantized electromagnetic field. The electric and magnetic fields become operators and the normal modes are described by creation and annihilation operators such as

\[
\hat a_k,\qquad \hat a_k^\dagger.
\]

A photon is not an alternative to the electromagnetic field. It is an excitation of the quantized electromagnetic field. Quantum optics therefore still contains the electromagnetic field; it changes the state space and observables used to describe it.

The field carries the familiar optical degrees of freedom:

- frequency and wavelength;
- wave vector and momentum;
- phase;
- polarization and helicity;
- amplitude and intensity;
- spatial mode and wavefront;
- temporal mode and pulse shape;
- spin and orbital angular momentum;
- coherence and correlation functions;
- photon number and number statistics;
- squeezing, entanglement and other nonclassical state structure.

These are different coordinates, observables or state properties of the same field sector. Optical information is encoded in these states and correlations; information is not an additional physical substance.

## 2. Matter

Matter means every material or effective material degree of freedom that can generate, guide, absorb, scatter, amplify, detect or otherwise respond to light.

It includes electrons and holes; atoms, ions and molecules; nuclei when relevant to the transition; lattice motion and phonons; spins and magnons; excitons; carrier and plasma oscillations; collective electronic degrees of freedom; biological tissue, fluids, gases, glasses, crystals, metals and semiconductors.

An optical component is structured matter. A lens is a material distribution with a chosen geometry and refractive response. A waveguide is structured matter that supports selected electromagnetic eigenmodes. A metasurface is a subwavelength spatial distribution of electromagnetic response. A detector is matter engineered to convert a field state into an electronic, thermal, chemical or mechanical record.

At a coarse-grained classical level, much of matter can be compressed into response functions such as

\[
\varepsilon(\mathbf r,\omega),\quad
\mu(\mathbf r,\omega),\quad
\sigma(\mathbf r,\omega),\quad
\chi^{(1)},\chi^{(2)},\chi^{(3)},\ldots
\]

At a microscopic or quantum level, those response functions are themselves consequences of the underlying matter Hamiltonian and its coupling to the electromagnetic field.

## 3. Interaction

Interaction is what turns field and matter into optics.

| Process | Field–matter interpretation |
| --- | --- |
| Reflection / refraction | Boundary and material response reorganize the field |
| Absorption | Field energy is transferred into matter degrees of freedom |
| Emission | Excited matter transfers energy into the electromagnetic field |
| Stimulated emission | An incident field drives coherent emission from gain matter |
| Scattering | Matter redirects field momentum, phase, polarization or frequency |
| Dispersion | Material response depends on frequency |
| Birefringence | Material response depends on polarization and direction |
| Nonlinear optics | Matter response depends nonlinearly on field amplitude |
| Raman / Brillouin processes | Light couples to molecular, vibrational or acoustic degrees of freedom |
| Magneto-optics | Electromagnetic response is coupled to magnetic order or spin |
| Plasmonics | Electromagnetic field couples to collective charge motion |
| Polaritons | Light and matter excitations hybridize strongly |
| Optomechanics | Optical fields exchange momentum and energy with mechanical modes |
| Photodetection | A field state creates a measurable matter excitation |

Interference and diffraction do not require matter at every point. They are manifestations of field superposition and propagation. They still fit the framework: they belong primarily to the field sector, while apertures, boundaries, sources and detectors are matter or boundary conditions.

## 4. One framework across theory levels

### Fundamental level

For ordinary light–matter physics, quantum electrodynamics provides the microscopic field-theory language:

\[
S = S_{\mathrm{EM}} + S_{\mathrm{matter}} + S_{\mathrm{interaction}}.
\]

The electromagnetic gauge field and charged matter fields are the underlying degrees of freedom.

### Effective quantum level

Quantum optics and cavity QED retain selected optical and material modes. A typical model has the form

\[
H =
\hbar\omega_c a^\dagger a
+\frac{\hbar\omega_0}{2}\sigma_z
+\hbar g(a^\dagger\sigma_-+a\sigma_+)
+\cdots.
\]

The same decomposition remains visible: optical mode, matter mode, coupling.

### Classical electromagnetic level

For macroscopic devices and most photonics:

\[
\nabla\times\mathbf E=-\partial_t\mathbf B,\qquad
\nabla\times\mathbf H=\mathbf J+\partial_t\mathbf D,
\]

plus constitutive relations and source terms.

### Wave-optics level

Under the appropriate approximations, Maxwell theory reduces to wave, Helmholtz, Fresnel, Fourier or paraxial propagation models.

### Geometrical-optics level

When wavelength is much smaller than the scale on which the medium varies, the field admits an eikonal or ray description. Rays are not a separate fundamental entity; they are a short-wavelength description of field propagation.

A useful hierarchy is

\[
\text{QED}
\rightarrow
\text{effective light–matter Hamiltonians}
\rightarrow
\text{Maxwell + material response}
\rightarrow
\text{wave optics}
\rightarrow
\text{ray optics}.
\]

Moving downward gives more microscopic detail. Moving upward gives simpler models with a narrower validity domain.

## 5. One framework across scales

| Scale / field | Typical representation |
| --- | --- |
| Quantum optics | Quantized optical modes + quantum emitters + coupling |
| Nanophotonics | Maxwell field + nanoscale structured response |
| Plasmonics | EM field + electron-density collective modes |
| Metasurfaces | EM field + engineered subwavelength susceptibility |
| Integrated photonics | Guided modes + waveguide / resonator matter + coupling |
| Fiber optics | Guided field + dielectric profile + dispersion / nonlinearity |
| Laser physics | Cavity field + gain medium + pump + loss |
| Imaging | Propagating field + object response + detector + inference |
| Spectroscopy | Prepared field + sample degrees of freedom + measured response |
| Geometrical optics | Rays / eikonal field + interfaces and index profile |
| Astronomical optics | Field propagation + matter + atmosphere / spacetime background |

## 6. One framework across the electromagnetic spectrum

The electromagnetic field is the same physical field across radio, microwave, terahertz, infrared, visible, ultraviolet, X-ray and gamma-ray frequencies. What changes strongly with frequency is which matter degrees of freedom dominate the interaction.

Examples:

- microwave: rotations, spins, circuits and collective electronic response;
- terahertz: phonons, low-energy excitations and carrier dynamics;
- infrared: molecular vibrations, phonons and thermal radiation;
- visible / near-IR: electronic transitions, dielectric response and semiconductor transitions;
- ultraviolet: higher electronic transitions and ionization;
- X-rays: inner-shell electrons and high-momentum scattering;
- gamma rays: nuclear and relativistic particle processes.

Optics and photonics are used conventionally for different subsets of this spectrum in different communities, but the field–matter–interaction framework itself is electromagnetic-spectrum wide.

## 7. Devices are structured matter that implements transformations

A useful engineering abstraction is

\[
\text{input field state}
\longrightarrow
\text{structured matter + interaction}
\longrightarrow
\text{output field / matter state}.
\]

A device can be understood by five questions:

1. What field state enters?
2. What matter or geometry is present?
3. What coupling law applies?
4. What state leaves or is stored in matter?
5. What observable is measured?

Examples:

- **Lens:** geometry + refractive response transform the wavefront.
- **Polarizer:** anisotropic matter selects or transforms polarization components.
- **Waveplate:** birefringent matter accumulates a controlled phase difference.
- **Grating:** periodic structure couples momentum components.
- **Fiber:** a dielectric profile supports guided modes and controls dispersion/nonlinearity.
- **Laser:** pumped gain matter and resonant field modes form a driven dissipative system.
- **Camera:** electromagnetic energy is converted into electronic charge and then data.
- **SLM:** externally controlled matter changes phase, amplitude or polarization spatially.
- **Metasurface:** subwavelength matter realizes a designed local or nonlocal scattering operator.

## 8. Experiments can be written as a state-transformation chain

Nearly every optical experiment can be organized as

\[
\text{source}
\rightarrow
\text{state preparation}
\rightarrow
\text{propagation}
\rightarrow
\text{sample / device interaction}
\rightarrow
\text{detection}
\rightarrow
\text{inference / control}.
\]

The source prepares a field state through a matter–field interaction; propagation evolves the field; samples and devices transform field and matter states; detectors implement another field–matter interaction; inference maps measured observables to the scientific quantity of interest; feedback changes sources, devices or sample controls and closes the loop.

This is a useful bridge between fundamental physics and automated laboratories.

## 9. Engineering is often an inverse problem

Forward optics asks

\[
(\text{field},\text{matter},\text{coupling})
\longrightarrow
\text{observable}.
\]

Design asks the inverse question:

\[
\text{desired observable or transformation}
\longrightarrow
\text{matter geometry, control and field preparation}.
\]

Lens design, inverse nanophotonics, metasurface synthesis, pulse shaping, illumination design, computational imaging and experiment control can all be viewed this way.

The common optimization variables are drawn from three places:

- **field:** amplitude, phase, spectrum, polarization, spatial/temporal modes;
- **matter:** composition, geometry, topology, state, temperature, carrier density, magnetization;
- **interaction / control:** coupling strength, pump, bias, modulation, boundary conditions, timing.

## 10. Measurement and information

Measurement does not need a separate physical ontology. A detector is another matter system coupled to the field. What is special is that the interaction is engineered to create a stable record.

Classically, a detector measures functions of intensity, phase, spectrum, polarization or arrival time. Quantum mechanically, measurement is represented by observables or POVMs acting on the field–matter state. The recorded outcome is generated through physical coupling to a measurement apparatus.

Information is encoded in distinguishable field or joint field–matter states: amplitude, phase, frequency, polarization, space, time, photon number, correlations and entanglement.

Communication, sensing and imaging differ mainly in what state is prepared, what channel acts on it and what inference is performed at the output.

## 11. Important boundaries of the framework

**It does not mean every optical calculation should start from QED.** Use the lowest-level model that retains the physics needed by the question.

**Matter is not always passive.** Gain, driven media, nonlinear response, non-equilibrium carrier populations and active quantum systems are matter dynamics.

**Field and matter are not always cleanly separable.** In strong coupling, polaritons and other hybrid excitations are the natural degrees of freedom. The decomposition still identifies the parent sectors and their coupling, but the eigenstates are mixed.

**Geometry is not an independent substance.** In most laboratory optics it enters through material layout, interfaces and boundary conditions. In gravitational optics, spacetime geometry is a genuine background degree of freedom and should be added explicitly.

**Not every electromagnetic phenomenon is conventionally called optics.** The framework is wider than disciplinary naming conventions.

## 12. The shortest accurate statements

### Scientific

> Optics and photonics study the states and dynamics of the electromagnetic field, the states and responses of matter, and the interactions that generate, transform, guide, detect and control them.

### Engineering

> An optical system prepares a field, lets it propagate and interact with structured matter, and converts the resulting field or matter state into a useful function or measurement.

### Fundamental

> Light is the electromagnetic quantum field and its excitations; optical phenomena arise from field dynamics and from its coupling to matter, subject to the relevant background geometry and environment.

## 13. A practical modelling checklist

For any optical problem, identify:

1. **Field:** classical or quantum? wavelength, bandwidth, modes, polarization, coherence, power / photon statistics?
2. **Matter:** what microscopic or effective degrees of freedom matter?
3. **Interaction:** linear, nonlinear, resonant, dissipative, scattering, gain, measurement?
4. **Geometry:** dimensions, interfaces, boundaries, periodicity, disorder, ports?
5. **Regime:** quantum / classical, near / far field, linear / nonlinear, weak / strong coupling, equilibrium / driven?
6. **Approximation:** QED, effective Hamiltonian, Maxwell, Helmholtz, paraxial, coupled-mode, ray?
7. **Observable:** field, spectrum, image, force, temperature, current, count rate, correlation, state fidelity?
8. **Validation:** conservation laws, convergence, limiting cases, calibration and experimental uncertainty?

If these eight items are explicit, the physical problem is usually well posed enough to choose a solver, design an experiment or build an automated workflow.

---

This foundation complements the repository's software catalogue. The catalogue answers **which tool can model the system**; this document answers **what the system is, at the level that survives across tools and subfields**.
