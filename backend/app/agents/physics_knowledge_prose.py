"""
PhysicsKnowledgeProse — Comprehensive Academic Knowledge Generators for Engineering Physics.
Provides authentic university-level pedagogical treatises, derivations, solved numericals,
and conceptual review questions across all 5 standard B.Tech syllabus units:
  Unit 1: Quantum Mechanics
  Unit 2: Wave Optics
  Unit 3: Lasers
  Unit 4: Fiber Optics
  Unit 5: Electromagnetism & Special Relativity
"""

from typing import List, Tuple, Dict, Any


def generate_quantum_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Quantum Mechanics topics."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    # -------------------------------------------------------------------------
    # Topic 1: Introduction to Quantum Mechanics
    # -------------------------------------------------------------------------
    if "intro" in t_low:
        if any(k in s_low for k in ["blackbody", "inadequacy", "rayleigh", "ultraviolet", "historical foundation"]):
            paragraphs.append(
                "The foundational emergence of quantum mechanics at the turn of the twentieth century was driven by the catastrophic breakdown of Newtonian mechanics and classical Maxwellian electrodynamics at microscopic atomic scales. "
                "Throughout the nineteenth century, physical reality was envisioned as an immutable dichotomy: matter consisted of localized Newtonian particles obeying deterministic trajectories, while radiation consisted of continuous Maxwellian electromagnetic waves exhibiting spatial diffraction and interference. "
                "However, classical thermodynamics governed by the equipartition theorem assigned an average thermal energy $\\langle E \\rangle = k_B T$ to every electromagnetic standing wave mode inside an isothermal cavity, "
                "yielding the Rayleigh-Jeans spectral energy density $u(\\nu)d\\nu = \\frac{8\\pi k_B T}{c^3}\\nu^2 d\\nu$, which diverges toward infinity at high frequencies—an absurdity known as the ultraviolet catastrophe."
            )
            paragraphs.append(
                "Max Planck resolved this blackbody radiation crisis in December 1900 by proposing a radical mathematical departure from classical statistical mechanics. "
                "Planck hypothesized that the atomic resonators constituting cavity walls absorb and emit radiant energy strictly in discrete, indivisible packets or quanta: $E = h\\nu = \\hbar\\omega$, where $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$. "
                "Evaluating the canonical partition function for discrete harmonic levels $E_n = n h \\nu$ yielded the celebrated Planck radiation distribution law:\n\n"
                "$$u(\\nu)d\\nu = \\frac{8\\pi h \\nu^3}{c^3}\\frac{1}{e^{h\\nu / k_B T} - 1}d\\nu$$\n\n"
                "In the low-frequency limit ($h\\nu \\ll k_B T$), expanding the exponential recovers the Rayleigh-Jeans formula, whereas in the high-frequency regime ($h\\nu \\gg k_B T$), it reproduces Wien's exponential decay, matching experimental spectrophotometry across all temperatures."
            )
            paragraphs.append(
                "This revolutionary discovery revealed that energy exchange at atomic scales is intrinsically discrete rather than continuous. "
                "By demonstrating that cavity radiation modes cannot be excited without supplying a threshold quantum of energy $h\\nu$, Planck prevented the ultraviolet modes from draining infinite thermal energy from the cavity. "
                "This single theoretical breakthrough inaugurated the quantum era, compelling physicists to reconsider the foundational assumptions of classical continuous field theories."
            )
        elif any(k in s_low for k in ["photoelectric", "einstein", "photon", "compton"]):
            paragraphs.append(
                "In 1905, Albert Einstein extended Planck's quantum concept by postulating that electromagnetic radiation is not merely emitted and absorbed in discrete quanta, but propagates through space as localized corpuscular packets termed photons. "
                "When a monochromatic photon of energy $E = h\\nu$ strikes a metallic surface, its entire quantum of energy is transferred instantaneously to an individual conduction electron, giving the Einstein photoelectric equation:\n\n"
                "$$h\\nu = W_0 + K_{max} = h\\nu_0 + \\frac{1}{2}m v_{max}^2$$\n\n"
                "where $W_0 = h\\nu_0$ represents the characteristic material work function and $\\nu_0$ is the threshold cutoff frequency below which no electron emission can occur, regardless of light intensity."
            )
            paragraphs.append(
                "The photon theory brilliantly resolved the three major paradoxes of classical wave theory: the instantaneous emission of photoelectrons without measurable time delay, the strict dependence of maximum kinetic energy on radiation frequency rather than beam intensity, and the existence of a definitive threshold frequency $\\nu_0$. "
                "Under classical wave theory, continuous wavefronts would distribute incident electromagnetic energy across millions of surface atoms, requiring hours of continuous exposure for an electron to accumulate sufficient work function energy. "
                "Measuring the retarding stopping potential $V_s$ against frequency established Millikan's relation $e V_s = h\\nu - W_0$, experimentally confirming Planck's constant with exceptional precision."
            )
            paragraphs.append(
                "Arthur Compton definitively confirmed the corpuscular kinematics of radiation in 1923 by scattering monochromatic X-rays off graphite target electrons. "
                "Treating the interaction as a relativistic elastic collision between a photon of momentum $p = h/\\lambda$ and an electron at rest yielded the Compton wavelength shift $\\Delta\\lambda = \\lambda' - \\lambda = \\frac{h}{m_e c}(1 - \\cos\\theta)$, "
                "where $\\lambda_c = \\frac{h}{m_e c} = 0.0243\\text{ \\AA}$ is the Compton wavelength. "
                "This decisive experiment proved conclusively that photons carry directed relativistic momentum as well as quantized energy."
            )
        else: # Postulates / Foundational / Planck Postulate
            paragraphs.append(
                "The foundational postulates of modern quantum mechanics synthesize the wave and corpuscular paradigms into a unified, mathematically rigorous operator framework in Hilbert space. "
                "Postulate 1 asserts that any physically realizable state of a quantum system is completely described by a complex state vector or wave function $\\Psi(\\mathbf{r}, t)$, which contains all knowable physical information concerning the system. "
                "Postulate 2 specifies that every physically observable dynamical variable (such as position, momentum, angular momentum, or total energy) is represented by a linear Hermitian operator acting upon the state space."
            )
            paragraphs.append(
                "Postulate 3 dictates that the only possible numerical outcome of an experimental measurement of an observable $A$ is one of the discrete eigenvalues $a_n$ satisfying the operator eigenvalue equation $\\hat{A}\\psi_n = a_n \\psi_n$. "
                "Postulate 4, formulated by Max Born, states that if the system is in normalized state $\\Psi$, the probability of obtaining eigenvalue $a_n$ upon measurement is given by the modulus squared of the inner product: $P(a_n) = |\\langle \\psi_n | \\Psi \\rangle|^2$. "
                "Immediately following the measurement, the state collapses into the corresponding eigenfunction $\\psi_n$."
            )
            paragraphs.append(
                "Postulate 5 governs the temporal evolution of an undisturbed quantum state via the Time-Dependent Schrödinger Equation: $i\\hbar\\frac{\\partial\\Psi}{\\partial t} = \\hat{H}\\Psi$, where $\\hat{H}$ denotes the Hamiltonian operator. "
                "Together, these foundational postulates replace Newtonian deterministic trajectory mechanics with a probabilistic state-space geometry, establishing the theoretical cornerstone for all modern microphysics."
            )

    # -------------------------------------------------------------------------
    # Topic 2: Wave Nature of Particles
    # -------------------------------------------------------------------------
    elif "wave nature" in t_low:
        if any(k in s_low for k in ["davisson", "germer", "thomson", "experiment"]):
            paragraphs.append(
                "The definitive empirical confirmation that material particles possess an authentic wave character was achieved in 1927 by Clinton Davisson and Lester Germer at Bell Telephone Laboratories. "
                "Their high-vacuum experimental apparatus directed a collimated beam of electrons, accelerated from a heated tungsten filament across an adjustable electrostatic potential difference $V$, normally onto the target surface of a polished nickel single crystal. "
                "The angular distribution of elastically scattered electrons was precisely measured as a function of scattering angle using an electrostatic Faraday collector connected to a sensitive galvanometer."
            )
            paragraphs.append(
                "Davisson and Germer observed that for an accelerating potential of $V = 54\\text{ V}$, a sharp, pronounced scattering intensity peak emerged at an azimuth scattering angle of $\\phi = 50^\\circ$. "
                "Treating the nickel single crystal as a three-dimensional diffraction grating with Bragg lattice interplanar spacing $d = 0.091\\text{ nm}$, the glancing angle with the atomic Bragg planes is $\\theta = 90^\\circ - \\phi/2 = 65^\\circ$. "
                "Applying Bragg's law of diffraction $2d\\sin\\theta = n\\lambda$ for first-order reflection ($n=1$) yielded an experimentally deduced wavelength:\n\n"
                "$$\\lambda_{exp} = 2 d \\sin\\theta = 2(0.091\\text{ nm})\\sin(65^\\circ) = 0.165\\text{ nm}$$\n\n"
                "Comparing this empirical measurement against de Broglie's theoretical prediction $\\lambda = \\frac{1.227}{\\sqrt{54}}\\text{ nm} = 0.167\\text{ nm}$ revealed extraordinary agreement within 1.2%."
            )
            paragraphs.append(
                "Simultaneously, George Paget Thomson at the University of Aberdeen demonstrated transmission diffraction by projecting a high-energy beam of cathode rays through ultra-thin polycrystalline gold and platinum foils. "
                "Thomson observed sharp concentric circular diffraction rings upon a photographic plate behind the foil, identical to X-ray powder diffraction patterns and confirming wave interference. "
                "While J.J. Thomson had won the Nobel Prize in 1906 for discovering the electron as a particle, his son G.P. Thomson shared the 1937 Nobel Prize with Davisson for proving that the electron behaves as a wave."
            )
        elif any(k in s_low for k in ["dual", "duality", "radiation duality", "evolution", "historical evolution"]):
            paragraphs.append(
                "Wave-particle duality asserts that physical entities exhibit both corpuscular and wave characteristics depending upon the nature of the experimental apparatus used to observe them. "
                "In macroscopic mechanics, physical objects possess definite spatial coordinates $\\mathbf{r}(t)$ and conjugate momenta $\\mathbf{p}(t)$ tracing continuous deterministic paths through phase space. "
                "Waves, conversely, are extended spatial disturbances characterized by wavelength $\\lambda$, frequency $\\nu$, phase velocity $v_p$, and the capacity for mutual superposition, diffraction, and interference."
            )
            paragraphs.append(
                "The historical evolution began when electromagnetic radiation, long modeled exclusively as Maxwellian waves, demonstrated particle attributes in the photoelectric and Compton effects. "
                "In 1924, Louis de Broglie reasoned that nature embodies reciprocal symmetry: if radiation exhibits corpuscular properties, material particles must correspondingly manifest undulatory wave properties. "
                "Niels Bohr synthesized this insight into the Principle of Complementarity, stating that wave and particle descriptions are mutually exclusive yet mutually indispensable representations of physical reality."
            )
            paragraphs.append(
                "Crucially, wave and particle behaviors never manifest simultaneously in the same experimental detection event. "
                "When propagating through apertures or crystal lattices, an electron exhibits wave interference; when striking a detector pixel or ionizing a gas molecule, it deposits discrete localized momentum at a single point. "
                "Thus, wave-particle duality represents not a physical contradiction, but a manifestation of quantum state projection upon macroscopic measuring apparatuses."
            )
        elif any(k in s_low for k in ["expression", "wavelength", "relation", "accelerat"]):
            paragraphs.append(
                "The mathematical formulation of matter waves directly connects kinematic mechanical observables to undulatory wave parameters. "
                "For any material particle of rest mass $m$ moving with non-relativistic velocity $v$, momentum is $p = mv$, yielding the canonical de Broglie wavelength expression:\n\n"
                "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2m E_k}}$$\n\n"
                "where $E_k$ represents the kinetic energy of the particle."
            )
            paragraphs.append(
                "When a charged particle with charge $q$ is accelerated from rest through an electrostatic potential difference $V$, the electrostatic work done equals acquired kinetic energy: $E_k = qV$. "
                "Substituting into the momentum relation produces:\n\n"
                "$$\\lambda = \\frac{h}{\\sqrt{2mqV}}$$\n\n"
                "For an electron ($m_e = 9.109 \\times 10^{-31}\\text{ kg}, q = 1.602 \\times 10^{-19}\\text{ C}$), inserting fundamental constants gives the standard engineering formula:\n\n"
                "$$\\lambda_e = \\frac{1.227}{\\sqrt{V}}\\text{ nm} = \\frac{12.27}{\\sqrt{V}}\\text{ \\AA}$$\n\n"
                "For accelerating voltages between 50 V and 150 V, electron wavelengths span 0.1 to 0.17 nm, matching interplanar spacings in crystalline solids."
            )
            paragraphs.append(
                "At relativistic velocities where kinetic energy approaches or exceeds rest mass energy $m_0 c^2$, the relativistic momentum $p = \\gamma m_0 v = \\frac{\\sqrt{E^2 - m_0^2 c^4}}{c}$ must be employed. "
                "This yields the relativistic de Broglie wavelength:\n\n"
                "$$\\lambda_{rel} = \\frac{h}{\\sqrt{2m_0 qV\\left(1 + \\frac{qV}{2m_0 c^2}\\right)}}$$\n\n"
                "For high-voltage electron microscopes operating at 200 kV, relativistic contraction reduces the electron wavelength to $0.00251\\text{ nm}$, dramatically improving resolving capability."
            )
        elif any(k in s_low for k in ["packet", "phase", "group", "representation"]):
            paragraphs.append(
                "An infinite monochromatic harmonic matter wave $\\psi(x, t) = A e^{i(kx - \\omega t)}$ extends uniformly across all space and carries zero spatial localization, making it incapable of representing an isolated particle. "
                "To resolve this localization problem, quantum mechanics constructs a localized wavepacket through continuous Fourier superposition of plane waves spanning a narrow distribution of wavenumbers $k$:\n\n"
                "$$\\Psi(x, t) = \\frac{1}{\\sqrt{2\\pi}} \\int_{-\\infty}^{\\infty} A(k) e^{i(kx - \\omega(k) t)} dk$$"
            )
            paragraphs.append(
                "Expanding the angular frequency $\\omega(k)$ in a Taylor series about central wavenumber $k_0$: $\\omega(k) \\approx \\omega_0 + \\left(\\frac{d\\omega}{dk}\\right)_{k_0}(k - k_0)$, "
                "the wavepacket factors into a rapidly oscillating carrier wave modulated by a slowly varying spatial envelope propagating at group velocity $v_g = \\frac{d\\omega}{dk}$. "
                "Using de Broglie's relations $E = \\hbar\\omega$ and $p = \\hbar k$ establishes that $v_g = \\frac{dE}{dp} = \\frac{p}{m} = v_{particle}$, proving that the envelope precisely tracks the mechanical velocity of the particle."
            )
            paragraphs.append(
                "Because quantum matter waves propagate in vacuum with a quadratic dispersion relation $\\omega(k) = \\frac{\\hbar k^2}{2m}$, different Fourier components travel at different phase velocities $v_p = \\frac{\\hbar k}{2m}$. "
                "As a consequence, the wavepacket undergoes progressive spatial dispersion over time, with its spatial width broadening according to $\\Delta x(t) = \\Delta x_0 \\sqrt{1 + \\left(\\frac{\\hbar t}{2m(\\Delta x_0)^2}\\right)^2}$, "
                "illustrating the dynamical dispersion inherent to Schrödinger wave mechanics."
            )
        elif any(k in s_low for k in ["microscop", "electron beam", "semiconductor", "metrology", "tem", "sem"]):
            paragraphs.append(
                "The practical exploitation of electron matter waves has revolutionized modern high-resolution imaging and semiconductor metrology. "
                "According to Abbe's optical diffraction criterion, the resolving limit of any imaging instrument is bounded by $d = \\frac{0.61\\lambda}{\\text{NA}}$, where $\\text{NA}$ is numerical aperture. "
                "While optical microscopy is limited by visible wavelengths ($400-700\\text{ nm}$) to resolving features no smaller than $\\sim 200\\text{ nm}$, electron matter waves operating at accelerating potentials of 100 to 300 kV achieve picometer wavelengths ($2-4\\text{ pm}$)."
            )
            paragraphs.append(
                "In Transmission Electron Microscopy (TEM) and High-Resolution TEM (HRTEM), this dramatic wavelength reduction enables direct sub-angstrom visualization of individual atomic columns and crystal defects in advanced materials. "
                "Scanning Electron Microscopy (SEM) utilizes focused electron beams to scan specimen topographies with depth-of-field orders of magnitude superior to optical microscopes, providing critical morphological diagnostics in material fracture and biological sciences."
            )
            paragraphs.append(
                "In semiconductor manufacturing, Electron Beam Lithography (EBL) utilizes ultra-focused relativistic electron beams to pattern sub-10 nm features on silicon wafers, bypassing optical reticle diffraction limits. "
                "Furthermore, Low-Energy Electron Diffraction (LEED) and Reflection High-Energy Electron Diffraction (RHEED) serve as indispensable real-time in-situ diagnostics during molecular beam epitaxy (MBE) crystal growth."
            )
        else: # Amplitude / Born Probability / Default
            paragraphs.append(
                "The physical meaning of the de Broglie matter wave was resolved in 1926 by Max Born through the probabilistic interpretation of quantum mechanics. "
                "Unlike classical electromagnetic waves where the square of the field amplitude corresponds to physical energy density, the quantum wave function $\\Psi(\\mathbf{r}, t)$ represents a complex probability amplitude. "
                "The modulus squared $P(\\mathbf{r}, t) = |\\Psi(\\mathbf{r}, t)|^2 = \\Psi^* \\Psi$ defines the probability density per unit volume of finding the material particle at spatial coordinate $\\mathbf{r}$ at time $t$."
            )
            paragraphs.append(
                "Because the physical particle must exist somewhere in coordinate space with absolute certainty, every physically admissible matter wave must satisfy the unit normalization integral across all space:\n\n"
                "$$\\int_{-\\infty}^{\\infty} |\\Psi(\\mathbf{r}, t)|^2 d^3r = 1$$\n\n"
                "This normalization condition requires that the wave function belong to the Hilbert space of square-integrable functions $L^2(\\mathbb{R}^3)$ and vanish asymptotically as $|\\mathbf{r}| \\to \\infty$."
            )
            paragraphs.append(
                "Born's probability postulate established that microscopic determinism is replaced by rigorous statistical predictability. "
                "While individual particle detection events are intrinsically stochastic, the spatial distribution of large ensembles of identically prepared particles reproduces the probability density $|\\Psi|^2$ with absolute mathematical precision."
            )

    # -------------------------------------------------------------------------
    # Topic 3: de Broglie Hypothesis
    # -------------------------------------------------------------------------
    elif "de broglie" in t_low or "broglie" in t_low:
        if any(k in s_low for k in ["historical", "inadequacy", "motivation"]):
            paragraphs.append(
                "In his landmark 1924 doctoral dissertation at the Sorbonne, Prince Louis de Broglie proposed a profound symmetry in the fundamental laws of nature. "
                "Classical nineteenth-century physics had maintained a rigid dichotomy: radiation was described by Maxwell's continuous electromagnetic wave equations, while matter was governed by Newton's discrete corpuscular laws. "
                "However, the discoveries of the photoelectric effect and Compton scattering established that electromagnetic radiation carries discrete particle-like momentum $p = h/\\lambda$."
            )
            paragraphs.append(
                "De Broglie reasoned that if radiant energy displays corpuscular characteristics under appropriate experimental conditions, material entities such as electrons must likewise manifest undulatory wave behavior. "
                "Furthermore, de Broglie recognized that classical mechanics was utterly incapable of explaining Niels Bohr's ad-hoc quantum postulate that atomic orbital angular momentum is quantized in discrete units: $L = mvr = n\\hbar = \\frac{nh}{2\\pi}$. "
                "Classical electrodynamics predicted that orbiting electrons undergo continuous Larmor radiation acceleration, spiraling into the nucleus in picoseconds."
            )
            paragraphs.append(
                "By postulating that an electron possesses an intrinsic matter wavelength $\\lambda = h/p$, de Broglie provided the physical rationale for Bohr's quantization condition. "
                "An electron orbit is stable if and only if the matter wave forms a constructive, non-interfering circular standing wave: the orbit circumference must accommodate an exact integer number of wavelengths: $2\\pi r = n\\lambda = n\\frac{h}{p} \\implies mvr = \\frac{nh}{2\\pi}$. "
                "This elegant wave-mechanical deduction converted Bohr's arbitrary empirical postulate into a natural consequence of wave resonance."
            )
        elif any(k in s_low for k in ["dual", "nature"]):
            paragraphs.append(
                "The concept of the dual nature of matter represents one of the foundational cornerstones of modern quantum mechanics, resolving the century-long paradox concerning the wave-particle dichotomy. "
                "In 1924, Louis de Broglie synthesized Planck's quantum theory and Einstein's special relativity to postulate that wave-particle duality is a universal property of nature: radiant energy behaves as discrete photon particles, and material particles possessing momentum simultaneously exhibit intrinsic wave oscillations."
            )
            paragraphs.append(
                "The de Broglie hypothesis relates the corpuscular momentum $p = mv$ of a moving body to its characteristic matter wavelength $\\lambda$ through Planck's constant $h$:\n\n"
                "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2m E_k}}$$\n\n"
                "For a charged particle of mass $m$ and charge $q$ accelerated from rest through an electrostatic potential difference $V$, the kinetic energy acquired is $E_k = qV$, establishing the practical wavelength equation:\n\n"
                "$$\\lambda = \\frac{h}{\\sqrt{2mqV}}$$\n\n"
                "For an electron ($m_e = 9.109 \\times 10^{-31}\\text{ kg}$, $e = 1.602 \\times 10^{-19}\\text{ C}$), this yields the operational formula $\\lambda_e = \\frac{1.227}{\\sqrt{V}}\\text{ nm} = \\frac{12.27}{\\sqrt{V}}\\text{ \\AA}$."
            )
            paragraphs.append(
                "Definitive experimental verification of matter waves was achieved in 1927 by Clinton Davisson and Lester Germer at Bell Labs. "
                "By directing low-energy electrons at a nickel crystal lattice, they detected pronounced diffraction peaks obeying Bragg's law $2d\\sin\\theta = n\\lambda$, measuring an electron wavelength that agreed with de Broglie's prediction to within 1%. "
                "Simultaneously, G. P. Thomson observed transmission diffraction rings using thin gold foils, confirming that electrons, neutrons, and atoms all manifest wave-particle duality governed by Max Born's probability interpretation."
            )
        elif any(k in s_low for k in ["postulate", "matter-wave", "matter wave characteristics"]):
            paragraphs.append(
                "The de Broglie matter-wave postulate asserts that every physical particle of mass $m$ moving with velocity $v$ and linear momentum $p = mv$ possesses an associated undulatory wave of wavelength $\\lambda = \\frac{h}{p}$. "
                "Matter waves, commonly designated as de Broglie waves, possess fundamental physical characteristics that distinguish them sharply from classical mechanical or electromagnetic waves. "
                "First, matter waves are not acoustic disturbances requiring an elastic material medium, nor are they transverse vector oscillations of electromagnetic fields."
            )
            paragraphs.append(
                "Second, matter waves are complex scalar probability amplitude fields whose modulus squared governs physical measurement likelihoods in Hilbert space. "
                "Third, the propagation velocities of matter waves exhibit anomalous dispersion: their phase velocity $v_p = c^2/v$ is superluminal ($v_p > c$), whereas their wavepacket group velocity $v_g = v$ exactly matches the subluminal particle velocity. "
                "Fourth, matter waves are universal: they are independent of particle electric charge, applying identically to neutral neutrons, charged protons, and complex buckyball carbon molecules ($C_{60}$)."
            )
            paragraphs.append(
                "The manifestation of matter waves depends fundamentally upon the mass scale of the entity. "
                "For macroscopic bodies (such as a 0.1 kg ball moving at 10 m/s), the de Broglie wavelength is $\\lambda \\approx 6.6 \\times 10^{-34}\\text{ m}$—twenty orders of magnitude smaller than atomic nuclei—rendering diffraction effects completely undetectable. "
                "Conversely, for microscopic electrons ($m_e \\approx 9.1 \\times 10^{-31}\\text{ kg}$), the matter wavelength is on the order of angstroms, directly matching crystal lattice spacings and dominating microscopic physics."
            )
        elif any(k in s_low for k in ["derivation", "relation", "wavelength"]):
            paragraphs.append(
                "The mathematical derivation of the de Broglie wavelength relation begins from Einstein's relativistic mass-energy equivalence and Planck's quantum hypothesis. "
                "For a photon of zero rest mass propagating at the speed of light $c$, total energy is expressed as $E = pc$ and $E = h\\nu = \\frac{hc}{\\lambda}$. "
                "Equating both expressions yields the photon momentum-wavelength relation: $pc = \\frac{hc}{\\lambda} \\implies p = \\frac{h}{\\lambda} \\implies \\lambda = \\frac{h}{p}$."
            )
            paragraphs.append(
                "De Broglie boldly extended this relation from zero rest-mass radiation quanta to material particles possessing finite rest mass $m$ moving with velocity $v$:\n\n"
                "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv}$$\n\n"
                "Expressing momentum in terms of non-relativistic kinetic energy $E_k = \\frac{p^2}{2m} \\implies p = \\sqrt{2m E_k}$, the matter wavelength is formulated as:\n\n"
                "$$\\lambda = \\frac{h}{\\sqrt{2m E_k}}$$"
            )
            paragraphs.append(
                "For a charged particle carrying charge $q$ accelerated from rest across an electrostatic potential difference $V$, the acquired kinetic energy is $E_k = qV$. "
                "Substituting into the wavelength equation yields:\n\n"
                "$$\\lambda = \\frac{h}{\\sqrt{2mqV}}$$\n\n"
                "For an electron, inserting $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$, $m_e = 9.109 \\times 10^{-31}\\text{ kg}$, and $e = 1.602 \\times 10^{-19}\\text{ C}$ gives $\\lambda_e = \\frac{1.227}{\\sqrt{V}}\\text{ nm}$, establishing the benchmark formula used in electron diffraction analysis."
            )
        elif any(k in s_low for k in ["phase", "group", "velocity"]):
            paragraphs.append(
                "Matter waves propagate with two distinct characteristic velocities: phase velocity $v_p$ and group velocity $v_g$. "
                "Phase velocity is defined as the rate at which surfaces of constant phase advance through space: $v_p = \\frac{\\omega}{k} = \\nu \\lambda$. "
                "Using Einstein's total relativistic energy $E = mc^2 = \\hbar\\omega$ and relativistic momentum $p = mv = \\hbar k$, substituting yields:\n\n"
                "$$v_p = \\frac{\\omega}{k} = \\frac{E}{p} = \\frac{mc^2}{mv} = \\frac{c^2}{v}$$\n\n"
                "Because physical particle velocities are strictly subluminal ($v < c$), the phase velocity of a de Broglie wave is strictly superluminal ($v_p > c$)."
            )
            paragraphs.append(
                "This superluminal phase velocity does not violate Einstein's theory of special relativity because an infinite monochromatic wave carries zero localized energy or information. "
                "Physical signals and material particles are represented by localized wavepackets synthesized from a frequency spectrum $\\omega(k)$, propagating at group velocity $v_g = \\frac{d\\omega}{dk}$. "
                "Differentiating using the de Broglie relations $E = \\hbar\\omega$ and $p = \\hbar k$:\n\n"
                "$$v_g = \\frac{d\\omega}{dk} = \\frac{dE}{dp}$$\n\n"
                "For non-relativistic mechanics where $E = \\frac{p^2}{2m}$, $v_g = \\frac{d}{dp}\\left(\\frac{p^2}{2m}\\right) = \\frac{p}{m} = v$."
            )
            paragraphs.append(
                "In relativistic mechanics where $E^2 = p^2 c^2 + m_0^2 c^4$, implicit differentiation gives $2E\\frac{dE}{dp} = 2pc^2 \\implies v_g = \\frac{pc^2}{E} = \\frac{(\\gamma m_0 v)c^2}{\\gamma m_0 c^2} = v$. "
                "Thus, in both non-relativistic and relativistic domains, the group velocity of the matter wave packet is identically equal to the translational particle velocity $v$, proving the physical coherence of the wavepacket model."
            )
        elif any(k in s_low for k in ["confirmation", "davisson", "germer", "crystal"]):
            paragraphs.append(
                "Experimental confirmation of the de Broglie hypothesis was achieved in 1927 by Clinton Davisson and Lester Germer at Bell Telephone Laboratories. "
                "While investigating secondary electron emissions from a polycrystalline nickel target, an accidental laboratory explosion ruptured the vacuum tube, causing high-temperature oxidation of the nickel surface. "
                "To reduce the nickel oxide back to pure metal, Davisson and Germer baked the target in a hydrogen oven for hours, which inadvertently recrystallized the nickel into large single crystals."
            )
            paragraphs.append(
                "Upon resuming bombardment with low-energy electrons, they observed sharp, discrete angular intensity peaks characteristic of X-ray crystal diffraction. "
                "At an accelerating potential of $V = 54\\text{ V}$, a dominant diffraction maximum occurred at scattering angle $\\phi = 50^\\circ$, corresponding to Bragg glancing angle $\\theta = 65^\\circ$ on lattice planes spaced at $d = 0.091\\text{ nm}$. "
                "Applying Bragg's law $2d\\sin\\theta = n\\lambda$ yielded an experimental wavelength $\\lambda = 0.165\\text{ nm}$, matching de Broglie's prediction $\\lambda = 0.167\\text{ nm}$ within 1.2%."
            )
            paragraphs.append(
                "Concurrently, George Paget Thomson confirmed electron wave diffraction using high-velocity cathode rays transmitted through thin metallic foils. "
                "Subsequent experiments demonstrated diffraction of thermal neutrons (Fermi, 1936), neutral helium atoms (Estermann and Stern, 1930), and large organic molecules, "
                "proving beyond doubt that the de Broglie matter wave relation is a universal law of nature."
            )
        elif any(k in s_low for k in ["limitation", "relativistic", "interpretation"]):
            paragraphs.append(
                "While the de Broglie hypothesis provides a revolutionary bridge between classical mechanics and quantum mechanics, it has specific physical limitations. "
                "First, single-particle matter wave equations fail to describe many-body systems in physical three-dimensional space: for an $N$-particle system, the state function $\\Psi(\\mathbf{r}_1, \\mathbf{r}_2, \\dots, \\mathbf{r}_N, t)$ propagates in an abstract $3N$-dimensional configuration space rather than ordinary physical space."
            )
            paragraphs.append(
                "Second, non-relativistic matter wave formulations break down when particle speeds approach the speed of light ($v \\to c$). "
                "In relativistic regimes, relativistic wave equations such as the Klein-Gordon equation (for spin-0 bosons) and the Dirac equation (for spin-1/2 fermions) must be employed, introducing negative energy states and predicting antimatter."
            )
            paragraphs.append(
                "Third, matter waves cannot be interpreted as classical fluid distributions of dispersed matter or electric charge. "
                "As demonstrated by wavepacket dispersion, a physical charge distribution would undergo irreversible spatial disintegration over time, whereas electrons maintain point-like charge and mass upon detection, affirming Max Born's probability amplitude interpretation."
            )
        else: # Microscopy / Engineering / Modern Applications / Default
            paragraphs.append(
                "Modern engineering relies heavily on de Broglie wave physics across nanotechnology and materials science. "
                "The most celebrated application is the Transmission Electron Microscope (TEM) and Scanning Transmission Electron Microscope (STEM), which utilize picometer electron matter wavelengths to achieve sub-0.05 nm spatial resolution, visualizing single atoms and crystal dislocation cores."
            )
            paragraphs.append(
                "In structural biology and condensed matter physics, Thermal Neutron Diffraction provides an indispensable tool. "
                "Thermal neutrons with kinetic energies $E_k \\approx k_B T \\approx 0.025\\text{ eV}$ possess de Broglie wavelengths of $\\lambda \\approx 0.18\\text{ nm}$, perfectly suited for probing crystal lattices, magnetic spin structures, and hydrogen positions in biological macromolecules."
            )
            paragraphs.append(
                "Furthermore, Atom Interferometry exploits the matter-wave nature of laser-cooled cold atoms to create ultra-precise quantum sensors. "
                "Matter-wave interferometers achieve unprecedented sensitivities in measuring gravitational gradients, rotational accelerations, and fundamental physical constants, forming the basis for next-generation GPS-free quantum inertial navigation."
            )

    # -------------------------------------------------------------------------
    # Topic 4: Phase Velocity and Group Velocity
    # -------------------------------------------------------------------------
    elif "phase" in t_low or "group" in t_low or "velocity" in t_low:
        if any(k in s_low for k in ["derivation", "mathematical"]):
            paragraphs.append(
                "To rigorously derive phase and group velocities, consider the superposition of two harmonic waves of equal amplitude $A$ with slightly different angular frequencies $\\omega_1 = \\omega_0 + \\Delta\\omega$, $\\omega_2 = \\omega_0 - \\Delta\\omega$ and wavenumbers $k_1 = k_0 + \\Delta k$, $k_2 = k_0 - \\Delta k$:\n\n"
                "$$\\Psi(x, t) = A\\cos(k_1 x - \\omega_1 t) + A\\cos(k_2 x - \\omega_2 t)$$"
            )
            paragraphs.append(
                "Applying the trigonometric identity $\\cos\\alpha + \\cos\\beta = 2\\cos\\left(\\frac{\\alpha-\\beta}{2}\\right)\\cos\\left(\\frac{\\alpha+\\beta}{2}\\right)$ yields:\n\n"
                "$$\\Psi(x, t) = 2A \\cos(\\Delta k \\cdot x - \\Delta\\omega \\cdot t) \\cos(k_0 x - \\omega_0 t)$$\n\n"
                "This represents a high-frequency carrier wave $\\cos(k_0 x - \\omega_0 t)$ moving at phase velocity $v_p = \\frac{\\omega_0}{k_0}$, modulated by a slowly varying spatial envelope $2A\\cos(\\Delta k \\cdot x - \\Delta\\omega \\cdot t)$ propagating at group velocity $v_g = \\lim_{\\Delta k \\to 0}\\frac{\\Delta\\omega}{\\Delta k} = \\frac{d\\omega}{dk}$."
            )
            paragraphs.append(
                "Differentiating the quantum dispersion relation $\\omega(k) = \\frac{E}{\\hbar} = \\frac{\\hbar k^2}{2m}$ yields $v_g = \\frac{d\\omega}{dk} = \\frac{\\hbar k}{m} = \\frac{p}{m} = v$. "
                "Simultaneously, the phase velocity is $v_p = \\frac{\\omega}{k} = \\frac{\\hbar k}{2m} = \\frac{v}{2}$. "
                "Thus, for a non-relativistic free particle, the group velocity is exactly double the phase velocity: $v_g = 2 v_p$."
            )
        elif any(k in s_low for k in ["superposition", "formation", "harmonic", "phase velocity"]):
            paragraphs.append(
                "When harmonic waves propagate through any physical medium, phase velocity $v_p$ defines the speed at which individual surfaces of constant phase (wavefronts) advance. "
                "For a monochromatic plane wave component described by harmonic function $\\cos(kx - \\omega t)$, setting the phase argument constant ($kx - \\omega t = \\text{const}$) and taking the time derivative yields the canonical phase velocity definition: $v_p = \\frac{\\omega}{k} = \\nu \\lambda$."
            )
            paragraphs.append(
                "For a de Broglie matter wave in vacuum, substituting Einstein's total relativistic energy $E = mc^2 = \\hbar\\omega$ and momentum $p = mv = \\hbar k$ produces a startling result:\n\n"
                "$$v_p = \\frac{\\omega}{k} = \\frac{E}{p} = \\frac{mc^2}{mv} = \\frac{c^2}{v}$$\n\n"
                "Because physical particle velocities are strictly subluminal ($v < c$), the phase velocity of a matter wave is strictly superluminal ($v_p > c$). "
                "This does not violate special relativity because an individual monochromatic wavefront of infinite extent carries zero localized energy or signal."
            )
            paragraphs.append(
                "The relationship between group velocity and phase velocity is governed by Rayleigh's dispersion formula: $v_g = v_p + k\\frac{dv_p}{dk} = v_p - \\lambda \\frac{dv_p}{d\\lambda}$. "
                "In non-dispersive media $dv_p/d\\lambda = 0$, so $v_g = v_p$; however, matter waves in vacuum are inherently dispersive ($v_p = v/2$ non-relativistically), requiring wavepacket analysis to track localized particle motion."
            )
        else: # Interpretation / Velocity of Matter Waves / Group Velocity and Wave Packets / Default
            paragraphs.append(
                "Because an infinite monochromatic plane wave $\\psi(x, t) = A e^{i(kx - \\omega t)}$ extends uniformly from $-\\infty$ to $+\\infty$, it provides zero spatial localization and cannot represent an individual localized particle. "
                "To represent a physical particle, quantum wave mechanics constructs a localized wave packet synthesized from a continuous Fourier superposition of plane waves spanning a narrow band of frequencies $\\omega(k)$ and wavenumbers $k$:\n\n"
                "$$\\Psi(x, t) = \\frac{1}{\\sqrt{2\\pi}} \\int_{-\\infty}^{\\infty} A(k) e^{i(kx - \\omega(k) t)} dk$$"
            )
            paragraphs.append(
                "Expanding the dispersion relation $\\omega(k)$ in a Taylor series about central wavenumber $k_0$: $\\omega(k) \\approx \\omega_0 + \\left(\\frac{d\\omega}{dk}\\right)_{k_0}(k - k_0)$, the wavepacket factors into a rapidly oscillating carrier wave modulated by a slowly varying spatial envelope. "
                "The modulation envelope propagates at the group velocity $v_g = \\frac{d\\omega}{dk}$. "
                "Using the de Broglie quantum relations $E = \\hbar\\omega$ and $p = \\hbar k$, we evaluate the group velocity directly:\n\n"
                "$$v_g = \\frac{d\\omega}{dk} = \\frac{d(E/\\hbar)}{d(p/\\hbar)} = \\frac{dE}{dp}$$\n\n"
                "For a non-relativistic particle of mass $m$ with kinetic energy $E = \\frac{p^2}{2m}$, differentiating yields $v_g = \\frac{d}{dp}\\left(\\frac{p^2}{2m}\\right) = \\frac{p}{m} = v_{particle}$."
            )
            paragraphs.append(
                "In relativistic mechanics where $E^2 = p^2 c^2 + m_0^2 c^4$, implicit differentiation yields $2E \\frac{dE}{dp} = 2pc^2 \\implies v_g = \\frac{pc^2}{E} = \\frac{(\\gamma m_0 v)c^2}{\\gamma m_0 c^2} = v_{particle}$. "
                "This fundamental identity proves that the group velocity of a quantum matter wavepacket identically tracks the physical translational velocity of the material particle."
            )

    # -------------------------------------------------------------------------
    # Topic 5: Heisenberg Uncertainty Principle
    # -------------------------------------------------------------------------
    elif "uncertainty" in t_low or "heisenberg" in t_low:
        if any(k in s_low for k in ["concept", "measurement problem", "statement"]):
            paragraphs.append(
                "Formulated by Werner Heisenberg in 1927, the uncertainty principle represents an inherent mathematical property of wave mechanics rather than an experimental measurement limitation. "
                "Any localized spatial state is represented by a wavepacket synthesized from a continuous Fourier superposition of plane waves: $\\psi(x) = \\frac{1}{\\sqrt{2\\pi}}\\int A(k)e^{ikx}dk$. "
                "According to the classical Fourier bandwidth theorem, the effective spatial width $\\Delta x$ and the wavenumber spread $\\Delta k$ satisfy the reciprocal inequality $\\Delta x \\cdot \\Delta k \\ge \\frac{1}{2}$."
            )
            paragraphs.append(
                "Multiplying this wave inequality by the reduced Planck constant $\\hbar$ and identifying physical particle momentum as $p_x = \\hbar k$ yields the celebrated position-momentum uncertainty relation:\n\n"
                "$$\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}$$\n\n"
                "where $\\hbar = \\frac{h}{2\\pi} \\approx 1.055 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$. "
                "The uncertainty principle dictates that conjugate observables cannot both possess sharply defined values simultaneously in any quantum state."
            )
            paragraphs.append(
                "Similarly, the conjugate relationship between energy and time is bounded by $\\Delta E \\cdot \\Delta t \\ge \\frac{\\hbar}{2}$, which governs the natural spectral linewidth $\\Delta\\nu \\ge \\frac{1}{4\\pi\\tau}$ of excited atomic states with finite radiative lifetime $\\tau$. "
                "This fundamental inequality establishes the impossibility of assigning classical deterministic phase-space trajectories to microscopic particles."
            )
        elif any(k in s_low for k in ["formulation", "wavepacket derivation", "derivation"]):
            paragraphs.append(
                "The mathematical derivation of the Heisenberg uncertainty principle arises directly from the non-commutative operator algebra of quantum mechanics. "
                "In quantum theory, physical observables are represented by Hermitian operators acting on Hilbert space. "
                "For any two Hermitian operators $\\hat{A}$ and $\\hat{B}$, the Robertson-Schrödinger inequality proves that their statistical variances satisfy:\n\n"
                "$$\\Delta A \\cdot \\Delta B \\ge \\frac{1}{2} |\\langle [\\hat{A}, \\hat{B}] \\rangle|$$"
            )
            paragraphs.append(
                "Evaluating the commutator between the position operator $\\hat{x} = x$ and the linear momentum operator $\\hat{p}_x = -i\\hbar\\frac{\\partial}{\\partial x}$ on an arbitrary wave function $\\psi(x)$:\n\n"
                "$$[\\hat{x}, \\hat{p}_x]\\psi = x\\left(-i\\hbar\\frac{\\partial\\psi}{\\partial x}\\right) - \\left(-i\\hbar\\frac{\\partial(x\\psi)}{\\partial x}\\right) = -i\\hbar x\\frac{\\partial\\psi}{\\partial x} + i\\hbar\\psi + i\\hbar x\\frac{\\partial\\psi}{\\partial x} = i\\hbar\\psi$$\n\n"
                "Since $[\\hat{x}, \\hat{p}_x] = i\\hbar$, substituting into the Robertson inequality yields $\\Delta x \\cdot \\Delta p_x \\ge \\frac{1}{2}|\\langle i\\hbar \\rangle| = \\frac{\\hbar}{2}$."
            )
            paragraphs.append(
                "Minimum uncertainty wavepackets (states satisfying $\\Delta x \\Delta p_x = \\hbar/2$) are uniquely described by Gaussian wavefunctions of the form $\\psi(x) = \\left(\\frac{1}{2\\pi\\sigma^2}\\right)^{1/4} e^{-x^2/(4\\sigma^2)} e^{ip_0 x/\\hbar}$. "
                "For any other non-Gaussian wavepacket geometry, the uncertainty product strictly exceeds $\\hbar/2$."
            )
        elif any(k in s_low for k in ["single-slit", "diffraction", "evidence", "experimental"]):
            paragraphs.append(
                "Heisenberg illustrated the uncertainty principle through his famous gamma-ray microscope thought experiment and the single-slit electron diffraction experiment. "
                "Consider a beam of monoenergetic electrons propagating along the $x$-axis with momentum $p_x = h/\\lambda$, incident upon a narrow slit of width $d = \\Delta y$ oriented along the $y$-axis. "
                "Before reaching the slit, the electrons have zero transverse momentum uncertainty: $p_y = 0 \\implies \\Delta p_y = 0$."
            )
            paragraphs.append(
                "Upon passing through the slit, the electron's position is localized within the slit aperture, introducing a spatial uncertainty $\\Delta y = d$. "
                "Due to wave diffraction, the transmitted electron beam spreads into a diffraction pattern whose central maximum subtends an angle $\\theta$ given by $d\\sin\\theta = \\lambda$. "
                "An electron diffracted within the central lobe acquires transverse momentum $p_y$ ranging from $-p_x\\sin\\theta$ to $+p_x\\sin\\theta$, yielding transverse momentum uncertainty $\\Delta p_y \\approx p_x\\sin\\theta = \\frac{h}{\\lambda}\\frac{\\lambda}{d} = \\frac{h}{d}$."
            )
            paragraphs.append(
                "Multiplying the spatial localization by the transverse momentum spread yields:\n\n"
                "$$\\Delta y \\cdot \\Delta p_y \\approx d \\cdot \\frac{h}{d} = h > \\frac{\\hbar}{2}$$\n\n"
                "Attempting to localize the electron more precisely by narrowing the slit width $d$ inevitably widens the diffraction angle $\\theta$, proportionally increasing $\\Delta p_y$ and validating the uncertainty principle."
            )
        elif any(k in s_low for k in ["nucleus", "implication", "non-existence", "physical implications"]):
            paragraphs.append(
                "The Heisenberg uncertainty principle entails profound physical implications that permanently dismantle classical determinism in microscopic physics. "
                "In classical mechanics, Laplace determinism asserted that precise knowledge of initial coordinates $\\mathbf{r}(0)$ and velocities $\\mathbf{v}(0)$ uniquely determines the entire future and past trajectories of a physical system. "
                "In quantum mechanics, because canonically conjugate operators do not commute ($[\\hat{x}, \\hat{p}_x] = i\\hbar$), it is mathematically impossible to prepare a quantum state with simultaneous vanishing variances in both coordinate and momentum."
            )
            paragraphs.append(
                "A foundational physical consequence is proving the impossibility of an electron residing permanently inside an atomic nucleus. "
                "Because atomic nuclei have characteristic radii of $R \\approx 10^{-14}\\text{ m}$, any electron confined within a nucleus would have a maximum position uncertainty $\\Delta x \\approx 2 \\times 10^{-14}\\text{ m}$. "
                "Applying the uncertainty relation yields a minimum momentum uncertainty $\\Delta p \\ge \\frac{\\hbar}{2\\Delta x} \\approx 2.64 \\times 10^{-21}\\text{ kg}\\cdot\\text{m/s}$. "
                "Evaluating the corresponding relativistic kinetic energy $E \\approx pc$ reveals an energy exceeding $15\\text{ to }20\\text{ MeV}$. "
                "Because beta-decay emission energies rarely exceed $2\\text{ to }3\\text{ MeV}$, electrons cannot pre-exist within the nucleus as constituent entities, proving they are synthesized dynamically during radioactive beta decay."
            )
            paragraphs.append(
                "Another critical consequence is the existence of non-zero zero-point energy: a quantum harmonic oscillator cannot come to complete rest at the origin ($x=0, p=0$) because that would violate $\\Delta x \\Delta p \\ge \\hbar/2$. "
                "Consequently, the ground state possesses an irreducible ground-state energy $E_0 = \\frac{1}{2}\\hbar\\omega$, preventing the collapse of atoms and stabilizing all matter in the universe."
            )
        else: # Metrology / Sensing / Quantum Limits / Default
            paragraphs.append(
                "In modern engineering, the Heisenberg uncertainty principle dictates the fundamental performance boundary known as the Standard Quantum Limit (SQL) in precision metrology. "
                "In ultra-sensitive laser interferometers such as the Laser Interferometer Gravitational-Wave Observatory (LIGO), measuring mirror displacements at the sub-attometer scale ($10^{-19}\\text{ m}$) requires balancing photon shot noise against radiation pressure back-action noise."
            )
            paragraphs.append(
                "To surpass the Standard Quantum Limit, quantum optical engineers utilize squeezed states of light. "
                "By redistributing quantum fluctuations between conjugate quadratures (amplitude and phase), noise in the phase quadrature can be squeezed below the vacuum level at the expense of anti-squeezing the non-critical amplitude quadrature, "
                "directly exploiting the uncertainty relation to enhance astronomical gravitational wave detection ranges by over 50%."
            )
            paragraphs.append(
                "Similarly, in quantum sensing, nitrogen-vacancy (NV) diamond centers and atomic vapor cell magnetometers utilize squeezed spin states to achieve femtotesla magnetic field sensitivities, enabling non-invasive magnetoencephalography and nanoscale nuclear magnetic resonance imaging."
            )

    # -------------------------------------------------------------------------
    # Topic 6: Operators in Quantum Mechanics
    # -------------------------------------------------------------------------
    elif "operator" in t_low:
        if any(k in s_low for k in ["position", "momentum", "hamiltonian", "differential"]):
            paragraphs.append(
                "Under the Dirac-von Neumann coordinate representation, physical kinematic observables and governing dynamical equations are mapped to differential operators acting on state functions in Hilbert space. "
                "The mathematical formulation begins with the classical spatial coordinate $x$ mapping to the multiplicative operator $\\hat{x} = x$, while linear momentum $p_x$ is represented by the spatial gradient operator:\n\n"
                "$$\\hat{p}_x = -i\\hbar \\frac{\\partial}{\\partial x}$$\n\n"
                "The kinetic energy operator is derived by squaring the momentum operator: $\\hat{T} = \\frac{\\hat{p}_x^2}{2m} = -\\frac{\\hbar^2}{2m}\\frac{\\partial^2}{\\partial x^2}$."
            )
            paragraphs.append(
                "The total energy observable corresponds to the Hamiltonian operator $\\hat{H}$, summing kinetic and potential energy operators:\n\n"
                "$$\\hat{H} = \\hat{T} + \\hat{V} = -\\frac{\\hbar^2}{2m}\\nabla^2 + V(\\mathbf{r}, t)$$\n\n"
                "In three dimensions, the vector momentum operator is $\\hat{\\mathbf{p}} = -i\\hbar\\nabla$, and the orbital angular momentum operator is defined as the cross product $\\hat{\\mathbf{L}} = \\mathbf{r} \\times \\hat{\\mathbf{p}} = -i\\hbar(\\mathbf{r} \\times \\nabla)$."
            )
            paragraphs.append(
                "Evaluating the commutator between position and momentum operators across an arbitrary test wave function $\\psi(x)$ demonstrates that:\n\n"
                "$$[\\hat{x}, \\hat{p}_x]\\psi = x\\left(-i\\hbar \\frac{\\partial\\psi}{\\partial x}\\right) - \\left(-i\\hbar \\frac{\\partial(x\\psi)}{\\partial x}\\right) = -i\\hbar x\\frac{\\partial\\psi}{\\partial x} + i\\hbar x\\frac{\\partial\\psi}{\\partial x} + i\\hbar\\psi = i\\hbar\\psi$$\n\n"
                "Because $[\\hat{x}, \\hat{p}_x] = i\\hbar \\ne 0$, position and momentum are mutually non-commuting, incompatible observables, mathematically generating the Heisenberg uncertainty relation."
            )
        elif any(k in s_low for k in ["commutator", "algebra", "uncertainty"]):
            paragraphs.append(
                "Commutator algebra forms the structural foundation of quantum mechanics, governing the compatibility and simultaneous measurability of physical observables. "
                "The commutator of two linear operators $\\hat{A}$ and $\\hat{B}$ is defined as $[\\hat{A}, \\hat{B}] = \\hat{A}\\hat{B} - \\hat{B}\\hat{A}$. "
                "If $[\\hat{A}, \\hat{B}] = 0$, the operators are said to commute; physically, commuting observables share a complete set of simultaneous eigenfunctions, meaning they can be measured simultaneously to arbitrary precision without mutual interference."
            )
            paragraphs.append(
                "Commutator brackets obey fundamental algebraic identities identical to classical Poisson brackets:\n\n"
                "1. Linearity: $[\\hat{A}, \\hat{B} + \\hat{C}] = [\\hat{A}, \\hat{B}] + [\\hat{A}, \\hat{C}]$\n"
                "2. Anti-symmetry: $[\\hat{A}, \\hat{B}] = -[\\hat{B}, \\hat{A}]$\n"
                "3. Distributivity (Leibniz rule): $[\\hat{A}, \\hat{B}\\hat{C}] = [\\hat{A}, \\hat{B}]\\hat{C} + \\hat{B}[\\hat{A}, \\hat{C}]$\n"
                "4. Jacobi identity: $[\\hat{A}, [\\hat{B}, \\hat{C}]] + [\\hat{B}, [\\hat{C}, \\hat{A}]] + [\\hat{C}, [\\hat{A}, \\hat{B}]] = 0$"
            )
            paragraphs.append(
                "When two operators do not commute ($[\\hat{A}, \\hat{B}] \\ne 0$), measuring one observable inevitably perturbs the quantum state and randomizes the outcome of the other. "
                "For example, orbital angular momentum components satisfy $[\\hat{L}_x, \\hat{L}_y] = i\\hbar\\hat{L}_z$, demonstrating that distinct angular momentum components cannot be simultaneously known, whereas each commutes with the total angular momentum: $[\\hat{L}^2, \\hat{L}_z] = 0$."
            )
        elif any(k in s_low for k in ["hermitian", "conservation", "observable"]):
            paragraphs.append(
                "An operator $\\hat{A}$ in quantum mechanics is defined as Hermitian (self-adjoint) if it satisfies the inner-product condition $\\langle \\psi_1 | \\hat{A} \\psi_2 \\rangle = \\langle \\hat{A} \\psi_1 | \\psi_2 \\rangle$, or in integral notation:\n\n"
                "$$\\int_{-\\infty}^{\\infty} \\psi_1^* (\\hat{A}\\psi_2) dx = \\int_{-\\infty}^{\\infty} (\\hat{A}\\psi_1)^* \\psi_2 dx$$"
            )
            paragraphs.append(
                "Hermiticity is a mandatory requirement for observable operators because the statistical expectation value $\\langle A \\rangle = \\int \\psi^* \\hat{A} \\psi dx$ corresponds to actual laboratory meter readings, which must be strictly real: $\\langle A \\rangle^* = \\langle A \\rangle$. "
                "Hermitian operators possess two vital mathematical properties: all their eigenvalues are strictly real numbers, and eigenfunctions corresponding to distinct eigenvalues are mutually orthogonal."
            )
            paragraphs.append(
                "Furthermore, the time derivative of an observable's expectation value is governed by Ehrenfest's theorem:\n\n"
                "$$\\frac{d\\langle A \\rangle}{dt} = \\frac{1}{i\\hbar}\\langle [\\hat{A}, \\hat{H}] \\rangle + \\left\\langle \\frac{\\partial\\hat{A}}{\\partial t}\\right\\rangle$$\n\n"
                "Consequently, if an explicit time-independent operator commutes with the Hamiltonian ($[\\hat{A}, \\hat{H}] = 0$), its expectation value is constant in time: $\\frac{d\\langle A \\rangle}{dt} = 0$, identifying $\\hat{A}$ as a constant of motion and fundamental conservation law."
            )
        else: # Formalism / Linear Operators / Default
            paragraphs.append(
                "The mathematical motivation for operator formalism in quantum mechanics arises from the necessity to represent observable physical quantities as linear transformations on state vectors in Hilbert space. "
                "An operator $\\hat{A}$ in quantum mechanics is defined as an operational rule that transforms a state vector $\\psi$ into another vector $\\psi'$. "
                "Physical consistency requires operators representing observables to satisfy linearity: $\\hat{A}(c_1\\psi_1 + c_2\\psi_2) = c_1\\hat{A}\\psi_1 + c_2\\hat{A}\\psi_2$ for any complex scalars $c_1, c_2$. "
                "Furthermore, because the expectation value $\\langle A \\rangle = \\int \\psi^* \\hat{A} \\psi dx$ corresponds to the statistical mean of actual experimental meter readings, expectation values must be strictly real numbers ($\\langle A \\rangle^* = \\langle A \\rangle$)."
            )
            paragraphs.append(
                "In Dirac's bra-ket notation, an arbitrary state is represented by ket vector $|\\psi\\rangle$ belonging to complex Hilbert space $\\mathcal{H}$, and its dual is represented by bra vector $\\langle\\psi|$. "
                "A linear operator $\\hat{A}$ maps kets to kets: $\\hat{A}|\\psi\\rangle = |\\phi\\rangle$. "
                "Given an orthonormal basis $\\{|e_n\\rangle\\}$, the operator can be expressed as a matrix with matrix elements $A_{mn} = \\langle e_m | \\hat{A} | e_n \\rangle$, linking operator calculus directly to linear matrix algebra."
            )
            paragraphs.append(
                "Linear operators preserve the superposition principle: if a system is prepared in a linear combination of states, the transformed state is the identical linear combination of transformed components. "
                "This linear structure ensures that quantum probability amplitudes undergo unitary, norm-preserving transformations under physical time evolution and spatial symmetries."
            )

    # -------------------------------------------------------------------------
    # Topic 7: Eigenvalues and Eigenfunctions
    # -------------------------------------------------------------------------
    elif "eigen" in t_low:
        if any(k in s_low for k in ["equation", "postulate", "definition", "eigenvalue equations"]):
            paragraphs.append(
                "The quantum eigenvalue equation $\\hat{A}\\psi_n = a_n \\psi_n$ constitutes the core mathematical postulate governing measurement in quantum mechanics. "
                "When an observable operator $\\hat{A}$ acts on an eigenstate $\\psi_n$, the resulting operation scales the state function by a scalar eigenvalue $a_n$. "
                "According to the Dirac-von Neumann measurement postulate, performing a measurement of observable $A$ on a quantum system prepared in an arbitrary superposition state $\\Psi = \\sum c_n \\psi_n$ projects the system into one of the discrete eigenstates $\\psi_n$, yielding the measured outcome $a_n$ with probability $P(a_n) = |c_n|^2 = |\\langle \\psi_n | \\Psi \\rangle|^2$."
            )
            paragraphs.append(
                "Immediately following the measurement, the state collapses into the corresponding eigenfunction $\\psi_n$. "
                "A subsequent measurement of observable $A$ performed immediately thereafter will yield the identical eigenvalue $a_n$ with 100% certainty, confirming that the measurement process leaves the system in a definite eigenstate of the measured observable."
            )
            paragraphs.append(
                "Eigenvalue equations appear universally across quantum physics: the Time-Independent Schrödinger Equation $\\hat{H}\\psi = E\\psi$ is the energy eigenvalue equation; the momentum eigenvalue equation is $-i\\hbar\\frac{\\partial\\psi}{\\partial x} = p\\psi$, yielding plane-wave eigenfunctions $\\psi_p(x) = e^{ipx/\\hbar}$; "
                "and angular momentum eigenvalue equations define spherical harmonic eigenfunctions $Y_l^m(\\theta, \\phi)$ with quantized eigenvalues $\\hat{L}^2 Y_l^m = l(l+1)\\hbar^2 Y_l^m$."
            )
        elif any(k in s_low for k in ["real", "derivation", "proof"]):
            paragraphs.append(
                "A rigorous mathematical theorem in quantum mechanics proves that all eigenvalues of a Hermitian operator are strictly real numbers. "
                "Let $\\hat{A}$ be a Hermitian operator, and let $\\psi$ be a normalized non-trivial eigenfunction ($\\|\\psi\\| \\ne 0$) corresponding to eigenvalue $a$, satisfying the eigenvalue equation $\\hat{A}\\psi = a\\psi$."
            )
            paragraphs.append(
                "Taking the inner product of both sides with eigenfunction $\\psi$ gives:\n\n"
                "$$\\langle \\psi | \\hat{A} \\psi \\rangle = \\langle \\psi | a \\psi \\rangle = a \\langle \\psi | \\psi \\rangle = a \\int_{-\\infty}^{\\infty} |\\psi|^2 dx$$\n\n"
                "Applying the Hermiticity definition $\\langle \\psi | \\hat{A} \\psi \\rangle = \\langle \\hat{A} \\psi | \\psi \\rangle$, the left-hand side can be re-evaluated as:\n\n"
                "$$\\langle \\hat{A} \\psi | \\psi \\rangle = \\langle a \\psi | \\psi \\rangle = a^* \\langle \\psi | \\psi \\rangle = a^* \\int_{-\\infty}^{\\infty} |\\psi|^2 dx$$"
            )
            paragraphs.append(
                "Subtracting the two expressions yields:\n\n"
                "$$(a - a^*) \\int_{-\\infty}^{\\infty} |\\psi|^2 dx = 0$$\n\n"
                "Because $\\psi$ is a physical, non-trivial wave function, the norm integral $\\int |\\psi|^2 dx > 0$ cannot vanish. "
                "Therefore, the scalar factor must vanish identically: $a - a^* = 0 \\implies a = a^*$, rigorously proving that all eigenvalues of any Hermitian operator are strictly real numbers."
            )
        else: # Orthogonality / Completeness / Default
            paragraphs.append(
                "A foundational mathematical property of Hermitian operators is that their eigenfunctions corresponding to distinct eigenvalues are mutually orthogonal. "
                "Let $\\hat{A}$ be a Hermitian operator with two distinct eigenvalues $a_m \\ne a_n$ satisfying eigenvalue equations $\\hat{A}\\psi_m = a_m \\psi_m$ and $\\hat{A}\\psi_n = a_n \\psi_n$. "
                "Evaluating the inner product $\\int \\psi_m^* (\\hat{A}\\psi_n) dx = a_n \\int \\psi_m^* \\psi_n dx$."
            )
            paragraphs.append(
                "Applying the Hermiticity definition $\\int \\psi_m^* (\\hat{A}\\psi_n) dx = \\int (\\hat{A}\\psi_m)^* \\psi_n dx$, the right-hand side becomes $\\int (a_m \\psi_m)^* \\psi_n dx = a_m \\int \\psi_m^* \\psi_n dx$ (since $a_m$ is real). "
                "Subtracting the two equations yields:\n\n"
                "$$(a_n - a_m) \\int \\psi_m^* \\psi_n dx = 0$$\n\n"
                "Because $a_m \\ne a_n$, the integral must vanish identically: $\\int \\psi_m^* \\psi_n dx = 0$ for $m \\ne n$. "
                "Normalizing these functions yields the orthonormality condition $\\int \\psi_m^* \\psi_n dx = \\delta_{mn}$."
            )
            paragraphs.append(
                "Furthermore, the complete set of orthonormal eigenfunctions forms a dense basis spanning Hilbert space, allowing any arbitrary physical wave function $\\Psi(x)$ to be expanded as a linear superposition $\\Psi(x) = \\sum c_n \\psi_n(x)$ where $c_n = \\int \\psi_n^* \\Psi dx$. "
                "The closure or completeness relation is expressed as $\\sum_n \\psi_n(x)\\psi_n^*(x') = \\delta(x - x')$, guaranteeing that any physically admissible state can be synthesized from the eigenstate basis."
            )

    # -------------------------------------------------------------------------
    # Topic 8: Time-Dependent Schrödinger Equation
    # -------------------------------------------------------------------------
    elif "time-dependent" in t_low or "tdse" in t_low:
        if any(k in s_low for k in ["continuity", "current", "conservation"]):
            paragraphs.append(
                "The physical validity of the Time-Dependent Schrödinger Equation (TDSE) is anchored by its preservation of total probability across time. "
                "Because a quantum particle must exist somewhere in space with certainty, the unit normalization condition $\\int_{-\\infty}^{\\infty} |\\Psi(\\mathbf{r}, t)|^2 d^3r = 1$ must remain strictly invariant during temporal evolution."
            )
            paragraphs.append(
                "Taking the time derivative of the probability density $P(\\mathbf{r}, t) = \\Psi^* \\Psi$ and substituting the TDSE alongside its complex conjugate yields:\n\n"
                "$$\\frac{\\partial P}{\\partial t} = \\Psi^* \\frac{\\partial\\Psi}{\\partial t} + \\Psi \\frac{\\partial\\Psi^*}{\\partial t} = \\Psi^* \\left(\\frac{1}{i\\hbar}\\hat{H}\\Psi\\right) + \\Psi \\left(-\\frac{1}{i\\hbar}\\hat{H}^*\\Psi^*\\right)$$\n\n"
                "Substituting $\\hat{H} = -\\frac{\\hbar^2}{2m}\\nabla^2 + V$ simplifies the expression to the local continuity equation:\n\n"
                "$$\\frac{\\partial P}{\\partial t} + \\nabla \\cdot \\mathbf{J} = 0$$\n\n"
                "where the vector quantity $\\mathbf{J}(\\mathbf{r}, t) = \\frac{\\hbar}{2mi}(\\Psi^* \\nabla \\Psi - \\Psi \\nabla \\Psi^*)$ represents the probability current density."
            )
            paragraphs.append(
                "Integrating the continuity equation over all space and applying Gauss's divergence theorem confirms that:\n\n"
                "$$\\frac{d}{dt}\\int P d^3r = -\\int (\\nabla \\cdot \\mathbf{J}) d^3r = -\\oint \\mathbf{J} \\cdot d\\mathbf{A} = 0$$\n\n"
                "provided the wave function vanishes at spatial infinity. "
                "This rigorously proves that the Schrödinger equation preserves unitary probability conservation without unphysical probability decay or growth."
            )
        elif any(k in s_low for k in ["derivation in 1d", "mathematical derivation", "derivation"]):
            paragraphs.append(
                "In 1926, Erwin Schrödinger formulated the fundamental dynamical wave equation of non-relativistic quantum mechanics by seeking a wave equation consistent with de Broglie's relations $E = \\hbar\\omega$ and $p = \\hbar k$. "
                "For a free non-relativistic particle propagating in one dimension as plane matter wave $\\Psi(x, t) = A e^{i(kx - \\omega t)}$, differentiating with respect to space and time yields $\\frac{\\partial\\Psi}{\\partial x} = ik\\Psi$, $\\frac{\\partial^2\\Psi}{\\partial x^2} = -k^2\\Psi$, and $\\frac{\\partial\\Psi}{\\partial t} = -i\\omega\\Psi$."
            )
            paragraphs.append(
                "Relating total energy to kinetic and potential energy via classical Hamiltonian mechanics $E = \\frac{p^2}{2m} + V(x, t)$, we multiply by wave function $\\Psi(x, t)$ and substitute operator equivalents $E \\to i\\hbar\\frac{\\partial}{\\partial t}$ and $p \\to -i\\hbar\\frac{\\partial}{\\partial x}$:\n\n"
                "$$i\\hbar \\frac{\\partial \\Psi(x, t)}{\\partial t} = -\\frac{\\hbar^2}{2m} \\frac{\\partial^2 \\Psi(x, t)}{\\partial x^2} + V(x, t)\\Psi(x, t)$$\n\n"
                "Because time appears as a first-order derivative, specifying an initial quantum state $\\Psi(x, 0)$ uniquely and deterministically determines the state at all future times through the unitary time-evolution operator $\\hat{U}(t, 0) = \\exp(-i\\hat{H}t/\\hbar)$."
            )
            paragraphs.append(
                "Generalizing to three dimensions yields the canonical Time-Dependent Schrödinger Equation:\n\n"
                "$$i\\hbar \\frac{\\partial \\Psi(\\mathbf{r}, t)}{\\partial t} = \\hat{H}\\Psi(\\mathbf{r}, t) = \\left(-\\frac{\\hbar^2}{2m}\\nabla^2 + V(\\mathbf{r}, t)\\right)\\Psi(\\mathbf{r}, t)$$\n\n"
                "The complex number $i = \\sqrt{-1}$ is an indispensable physical component of the equation; without it, the equation would resemble a classical heat diffusion equation rather than an oscillatory, phase-preserving wave equation."
            )
        elif any(k in s_low for k in ["motivation", "operator formulation"]):
            paragraphs.append(
                "The physical motivation underlying the Time-Dependent Schrödinger Equation was to replace classical trajectory mechanics with a linear wave equation that honors wave-particle duality while remaining consistent with energy conservation. "
                "Classical electromagnetic wave equations involve a second-order time derivative $\\frac{\\partial^2\\phi}{\\partial t^2} = c^2 \\nabla^2\\phi$. "
                "However, substituting the de Broglie relations $E = \\hbar\\omega$ and $p = \\hbar k$ into a second-order wave equation yields $E^2 \\propto p^2$, which corresponds to relativistic mass-less radiation rather than non-relativistic matter where kinetic energy is quadratic in momentum: $E_k = \\frac{p^2}{2m}$."
            )
            paragraphs.append(
                "To reproduce the classical dispersion relation $E = \\frac{p^2}{2m}$, the wave equation must be linear in the time derivative $\\frac{\\partial}{\\partial t}$ while remaining quadratic in spatial derivatives $\\nabla^2$. "
                "Furthermore, a first-order time derivative ensures that specifying the initial state $\\Psi(\\mathbf{r}, 0)$ alone completely determines the future evolution of the state, in harmony with the quantum state postulate."
            )
            paragraphs.append(
                "Mapping total energy $E$ to the differential operator $\\hat{E} = i\\hbar\\frac{\\partial}{\\partial t}$ and momentum to $\\hat{\\mathbf{p}} = -i\\hbar\\nabla$, the operator equation $\\hat{E}\\Psi = \\hat{H}\\Psi$ directly generates the TDSE. "
                "This operational formulation anchors all subsequent quantum dynamics, from atomic spectroscopy to quantum field theory."
            )
        else: # Significance / Dynamic Systems / Default
            paragraphs.append(
                "The Time-Dependent Schrödinger Equation serves as the master dynamic equation for non-relativistic quantum physics, governing how quantum states evolve in time under external potentials. "
                "Because the equation is strictly linear, any linear superposition of valid solutions is itself a valid physical solution, directly validating the quantum superposition principle for dynamic systems."
            )
            paragraphs.append(
                "For time-independent Hamiltonians $\\hat{H}$, the formal solution to the TDSE is expressed via the unitary time-evolution operator: $\\Psi(\\mathbf{r}, t) = \\hat{U}(t, 0)\\Psi(\\mathbf{r}, 0) = \\exp(-i\\hat{H}t/\\hbar)\\Psi(\\mathbf{r}, 0)$. "
                "Because $\\hat{H}$ is Hermitian, $\\hat{U}(t)$ is strictly unitary ($\\hat{U}^\\dagger \\hat{U} = \\hat{I}$), guaranteeing that probability norms and inner products between distinct quantum states remain strictly invariant across time."
            )
            paragraphs.append(
                "In dynamic systems such as semiconductor quantum wells subjected to oscillating laser fields, or atoms undergoing stimulated emission, the TDSE describes coherent state transitions and Rabi oscillations. "
                "It provides the theoretical framework required to design modern quantum computing gates, semiconductor nanolasers, and ultrafast laser spectroscopy experiments."
            )

    # -------------------------------------------------------------------------
    # Topic 9: Time-Independent Schrödinger Equation
    # -------------------------------------------------------------------------
    elif "time-independent" in t_low or "tise" in t_low:
        if any(k in s_low for k in ["stationary", "stationary states"]):
            paragraphs.append(
                "Stationary states represent the fundamental building blocks of quantum wave mechanics. "
                "When a quantum system occupies an energy eigenstate $\\Psi_n(\\mathbf{r}, t) = \\psi_n(\\mathbf{r})e^{-iE_n t/\\hbar}$, the position probability density $P(\\mathbf{r}, t)$ satisfies:\n\n"
                "$$P(\\mathbf{r}, t) = |\\Psi_n(\\mathbf{r}, t)|^2 = |\\psi_n(\\mathbf{r})|^2 \\cdot |e^{-iE_n t/\\hbar}|^2 = |\\psi_n(\\mathbf{r})|^2 \\cdot 1 = |\\psi_n(\\mathbf{r})|^2$$\n\n"
                "Because the temporal phase factor has unit modulus, the spatial probability distribution is strictly static and invariant in time, explaining why electrons in atomic orbitals do not radiate electromagnetic energy despite classical Maxwellian acceleration predictions."
            )
            paragraphs.append(
                "Furthermore, evaluating the expectation value of any time-independent observable $\\hat{A}$ in a stationary state yields $\\langle A \\rangle = \\int \\Psi_n^* \\hat{A} \\Psi_n d^3r = \\int \\psi_n^* \\hat{A} \\psi_n d^3r = \\text{constant}$. "
                "The system exhibits strictly zero physical dynamics in all observables, occupying a state of definite energy $E_n$ with zero energy variance: $\\Delta E = \\sqrt{\\langle H^2 \\rangle - \\langle H \\rangle^2} = 0$."
            )
            paragraphs.append(
                "Transition radiation occurs only when a system occupies a non-stationary coherent superposition of two or more distinct stationary states $\\Psi = c_1\\psi_1 e^{-iE_1 t/\\hbar} + c_2\\psi_2 e^{-iE_2 t/\\hbar}$. "
                "In such superpositions, the probability density oscillates at the Bohr transition frequency $\\omega_{21} = \\frac{E_2 - E_1}{\\hbar}$, producing an oscillating electric dipole that emits or absorbs photons."
            )
        elif any(k in s_low for k in ["separation", "variables", "separation of variables"]):
            paragraphs.append(
                "When the potential energy field $V(\\mathbf{r})$ is stationary and independent of time, the Time-Dependent Schrödinger Equation can be solved using the separation of variables technique. "
                "Assuming a product solution of the form $\\Psi(\\mathbf{r}, t) = \\psi(\\mathbf{r})\\phi(t)$, we substitute into the TDSE: $i\\hbar \\psi(\\mathbf{r})\\frac{d\\phi(t)}{dt} = \\phi(t)\\left[-\\frac{\\hbar^2}{2m}\\nabla^2\\psi(\\mathbf{r}) + V(\\mathbf{r})\\psi(\\mathbf{r})\\right]$."
            )
            paragraphs.append(
                "Dividing both sides by $\\psi(\\mathbf{r})\\phi(t)$ separates spatial and temporal variables onto opposite sides of the equation:\n\n"
                "$$\\frac{i\\hbar}{\\phi(t)}\\frac{d\\phi(t)}{dt} = \\frac{1}{\\psi(\\mathbf{r})}\\left[-\\frac{\\hbar^2}{2m}\\nabla^2\\psi(\\mathbf{r}) + V(\\mathbf{r})\\psi(\\mathbf{r})\\right] = E$$\n\n"
                "Because the left side depends exclusively on time while the right depends exclusively on spatial coordinates, both must equal a common separation constant $E$ representing total energy. "
                "The temporal equation integrates directly to $\\phi(t) = e^{-iEt/\\hbar}$, while the spatial equation produces the Time-Independent Schrödinger Equation (TISE):\n\n"
                "$$-\\frac{\\hbar^2}{2m}\\nabla^2 \\psi(\\mathbf{r}) + V(\\mathbf{r})\\psi(\\mathbf{r}) = E\\psi(\\mathbf{r}) \\implies \\hat{H}\\psi(\\mathbf{r}) = E\\psi(\\mathbf{r})$$\n\n"
                "Solving this spatial eigenvalue equation subject to physical boundary conditions determines the allowed energy eigenvalues $E_n$ and stationary wave functions $\\psi_n(\\mathbf{r})$."
            )
            paragraphs.append(
                "The general time-dependent solution is then expressed as an arbitrary linear superposition of all stationary state modes:\n\n"
                "$$\\Psi(\\mathbf{r}, t) = \\sum_{n=1}^\\infty c_n \\psi_n(\\mathbf{r}) e^{-iE_n t/\\hbar}$$\n\n"
                "where expansion coefficients $c_n = \\int \\psi_n^*(\\mathbf{r})\\Psi(\\mathbf{r}, 0)d^3r$ are determined by the initial boundary conditions at $t=0$."
            )
        elif any(k in s_low for k in ["derivation", "differential", "formulation"]):
            paragraphs.append(
                "The Time-Independent Schrödinger Equation represents a linear second-order ordinary differential equation in one dimension:\n\n"
                "$$\\frac{d^2\\psi(x)}{dx^2} + \\frac{2m}{\\hbar^2}(E - V(x))\\psi(x) = 0$$\n\n"
                "Defining the local kinetic wavenumber $k(x) = \\sqrt{\\frac{2m(E - V(x))}{\\hbar^2}}$, the differential equation takes the form $\\frac{d^2\\psi}{dx^2} + k^2(x)\\psi = 0$ in classically allowed regions where $E > V(x)$."
            )
            paragraphs.append(
                "In classically forbidden regions where $E < V(x)$, the kinetic energy is formally negative, and wavenumber becomes imaginary: $k(x) = i\\kappa(x)$, where $\\kappa(x) = \\sqrt{\\frac{2m(V(x) - E)}{\\hbar^2}}$. "
                "The differential equation transforms into $\\frac{d^2\\psi}{dx^2} - \\kappa^2(x)\\psi = 0$, yielding real exponential decay solutions $\\psi(x) \\sim e^{-\\kappa x}$. "
                "This behavior forms the mathematical basis for quantum barrier penetration and tunneling."
            )
            paragraphs.append(
                "At the classical turning points where $E = V(x)$, the second derivative vanishes ($\\frac{d^2\\psi}{dx^2} = 0$), representing an inflection point where the wave function transitions smoothly from sinusoidal oscillatory behavior to exponential evanescent decay. "
                "Enforcing boundary matching across turning points discretizes the energy spectrum into quantized levels $E_n$."
            )
        else: # Boundary Conditions / Admissible Wave Functions / Default
            paragraphs.append(
                "For a mathematical solution of the Time-Independent Schrödinger Equation to represent a physically admissible quantum state, it must satisfy four standard boundary conditions. "
                "First, $\\psi(\\mathbf{r})$ must be single-valued everywhere in space: multiple values at a single point would yield multiple contradictory probability densities $|\\psi|^2$, violating physical reality."
            )
            paragraphs.append(
                "Second, $\\psi(\\mathbf{r})$ must be continuous everywhere. A discontinuity in $\\psi$ would imply an infinite first derivative $\\nabla\\psi$, requiring infinite momentum and infinite kinetic energy. "
                "Third, the spatial gradient $\\nabla\\psi(\\mathbf{r})$ must be continuous everywhere, except across boundaries where the potential energy $V(\\mathbf{r})$ becomes infinitely discontinuous (as in idealized rigid walls). "
                "If $\\nabla\\psi$ were discontinuous across finite potentials, the second derivative $\\nabla^2\\psi$ would contain a Dirac delta function, which the finite Schrödinger equation could not balance."
            )
            paragraphs.append(
                "Fourth, $\\psi(\\mathbf{r})$ must be square-integrable over all space: $\\int_{-\\infty}^{\\infty} |\\psi|^2 d^3r < \\infty$. "
                "This square-integrability criterion mandates that $\\psi(\\mathbf{r}) \\to 0$ asymptotically as $|\\mathbf{r}| \\to \\infty$, ensuring that the total probability can be normalized to unity and eliminating non-physical divergent solutions."
            )

    # -------------------------------------------------------------------------
    # Topic 10: Physical Interpretation of the Wave Function
    # -------------------------------------------------------------------------
    elif "interpretation" in t_low or "born" in t_low:
        if any(k in s_low for k in ["normalization", "rigor", "integral"]):
            paragraphs.append(
                "The normalization condition represents the foundational mathematical constraint ensuring that quantum probability amplitudes conform to Kolmogorov probability theory. "
                "Because a physical quantum particle must reside somewhere in the universe with absolute certainty, the total integrated probability density over all coordinate space must equal unity:\n\n"
                "$$\\int_{-\\infty}^{\\infty} |\\Psi(\\mathbf{r}, t)|^2 d^3r = 1$$"
            )
            paragraphs.append(
                "Any unnormalized wave function $\\phi(\\mathbf{r}, t)$ obtained as an arbitrary solution to the linear Schrödinger equation can be normalized by calculating the normalization constant $N$:\n\n"
                "$$N = \\left( \\int_{-\\infty}^{\\infty} |\\phi(\\mathbf{r}, t)|^2 d^3r \\right)^{-1/2} \\implies \\Psi(\\mathbf{r}, t) = N \\phi(\\mathbf{r}, t)$$\n\n"
                "Because the Schrödinger Hamiltonian $\\hat{H}$ is Hermitian, the time derivative of the normalization integral vanishes identically ($\frac{d}{dt}\\int |\\Psi|^2 d^3r = 0$), guaranteeing that a state normalized at $t = 0$ remains permanently normalized for all future time."
            )
            paragraphs.append(
                "Mathematical rigor requires wave functions to reside within the Hilbert space of square-integrable functions $L^2(\\mathbb{R}^3)$. "
                "States that are not square-integrable, such as idealized infinite plane waves $e^{ikx}$, do not represent physical bound states and must be treated either as idealized distributions normalized via Dirac delta functions $\\int \\psi_k^* \\psi_{k'} dx = \\delta(k - k')$, or synthesized into square-integrable wavepackets."
            )
        elif any(k in s_low for k in ["collapse", "measurement", "wavepacket collapse"]):
            paragraphs.append(
                "The concept of wavepacket collapse, or state-vector reduction, addresses the profound transition between quantum superpositions and definite macroscopic measurement outcomes. "
                "Prior to measurement, a quantum system occupies a coherent linear superposition of orthonormal eigenstates: $|\\Psi\\rangle = \\sum_n c_n |\\psi_n\\rangle$, where $|c_n|^2$ denotes the probability of obtaining eigenvalue $a_n$."
            )
            paragraphs.append(
                "According to the Copenhagen interpretation and von Neumann's projection postulate, the irreversible interaction between the microscopic quantum system and a macroscopic measuring apparatus projects the state vector instantaneously into a single eigenstate $|\\psi_k\\rangle$: $|\\Psi\\rangle \\xrightarrow{\\text{measurement}} |\\psi_k\\rangle$. "
                "All alternative probability branches vanish, and the quantum phase coherence between superposition components is destroyed."
            )
            paragraphs.append(
                "Modern quantum measurement theory explains this apparent discontinuity through quantum decoherence. "
                "Decoherence demonstrates that entangling the quantum system with the vast degrees of freedom of the surrounding environment rapidly dissipates off-diagonal phase interference terms on timescales of femtoseconds, "
                "converting the pure quantum superposition into an apparent classical statistical mixture without violating unitary Schrödinger evolution."
            )
        else: # Max Born Probability Postulate / Default
            paragraphs.append(
                "In 1926, Max Born formulated the statistical interpretation of quantum mechanics, for which he was awarded the 1954 Nobel Prize in Physics. "
                "Schrödinger had initially attempted to interpret the wave function $\\Psi(\\mathbf{r}, t)$ as a continuous physical fluid density of electron matter or charge distributed through space. "
                "However, Born recognized that wavepackets disperse over time while physical particles maintain point-like charge and mass upon detection, postulating that $\\Psi$ represents a complex probability amplitude."
            )
            paragraphs.append(
                "According to Born's postulate, the modulus squared of the wave function defines the spatial probability density:\n\n"
                "$$P(\\mathbf{r}, t) = |\\Psi(\\mathbf{r}, t)|^2 = \\Psi^*(\\mathbf{r}, t)\\Psi(\\mathbf{r}, t)$$\n\n"
                "The probability of locating the particle within an infinitesimal volume element $d^3r = dx\\,dy\\,dz$ centered at position $\\mathbf{r}$ at time $t$ is $dP = |\\Psi(\\mathbf{r}, t)|^2 d^3r$. "
                "Because $\\Psi$ is complex ($\\Psi = |\\Psi|e^{i\\theta}$), its global phase $\\theta$ is physically unobservable, yet spatial phase gradients $\\nabla\\theta$ govern probability current and momentum."
            )
            paragraphs.append(
                "Born's probabilistic interpretation revolutionized the philosophy of science. "
                "Physics no longer predicted deterministic trajectories $\\mathbf{r}(t)$; instead, quantum mechanics calculates the exact statistical probability distribution of finding particles in given spatial states, "
                "a probabilistic framework confirmed by every precision experiment in modern microphysics."
            )

    # -------------------------------------------------------------------------
    # Topic 11: Particle in a 1D Box / Infinite Potential Well
    # -------------------------------------------------------------------------
    elif "box" in t_low or "well" in t_low:
        if any(k in s_low for k in ["energy", "quantization", "eigenvalues"]):
            paragraphs.append(
                "To derive the quantized energy spectrum and normalized wave functions for a particle of mass $m$ confined within a one-dimensional box of width $L$, "
                "we apply the time-independent Schrödinger equation subject to rigid Dirichlet boundary conditions $\\psi(0) = 0$ and $\\psi(L) = 0$. "
                "With quantized wavenumber $k_n = \\frac{n\\pi}{L}$, we equate $k_n$ to the definition $k_n = \\frac{\\sqrt{2mE_n}}{\\hbar}$, yielding:\n\n"
                "$$E_n = \\frac{\\hbar^2 k_n^2}{2m} = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2} = \\frac{n^2 h^2}{8mL^2}, \\quad n = 1, 2, 3, \\dots$$\n\n"
                "where $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ denotes Planck's constant and $n$ is the principal quantum number. "
                "Crucially, the state $n = 0$ is physically inadmissible because it would yield $\\psi(x) = 0$ everywhere, representing the complete absence of the particle. "
                "Consequently, the lowest accessible energy state is the non-zero ground state $E_1 = \\frac{h^2}{8mL^2}$, known as the zero-point energy."
            )
            paragraphs.append(
                "The normalization constant $A$ is determined by enforcing the unit total probability integral across the spatial enclosure:\n\n"
                "$$\\int_0^L |\\psi_n(x)|^2 dx = A^2 \\int_0^L \\sin^2\\left(\\frac{n\\pi x}{L}\\right) dx = A^2 \\frac{L}{2} = 1 \\implies A = \\sqrt{\\frac{2}{L}}$$\n\n"
                "The complete normalized stationary spatial wave functions $\\psi_n(x)$ are therefore expressed analytically as:\n\n"
                "$$\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right)$$\n\n"
                "The presence of a mandatory zero-point energy demonstrates that complete rest is forbidden in quantum mechanics, as an exact zero momentum would violate the Heisenberg uncertainty relation $\\Delta x \\cdot \\Delta p_x \\ge \\hbar/2$ within a finite confinement width $L$."
            )
            paragraphs.append(
                "The energy level separation $\\Delta E = E_{n+1} - E_n = (2n + 1)\\frac{h^2}{8mL^2}$ increases linearly with quantum number $n$. "
                "Transitions between consecutive levels involve emitting or absorbing photons of frequency $\\nu = \\frac{\\Delta E}{h} = (2n+1)\\frac{h}{8mL^2}$. "
                "As the box width $L$ expands toward macroscopic dimensions, the energy spacing $\\Delta E \\propto 1/L^2$ approaches zero, smoothly recovering the classical continuous energy continuum."
            )
        elif any(k in s_low for k in ["normalization", "probability density", "density distributions"]):
            paragraphs.append(
                "The probability density distributions for a particle in an infinite potential well are given by $P_n(x) = |\\psi_n(x)|^2 = \\frac{2}{L}\\sin^2\\left(\\frac{n\\pi x}{L}\\right)$. "
                "Plotting $P_n(x)$ across the well reveals distinct quantum spatial features sharply contrasting with classical expectations. "
                "In the ground state ($n=1$), the probability density is maximal at the exact center of the well ($x = L/2$) and smoothly drops to zero at the boundary walls."
            )
            paragraphs.append(
                "For excited states ($n > 1$), the wave function possesses $n - 1$ interior nodes where the wave function and probability density vanish identically ($P_n(x) = 0$). "
                "For instance, in the first excited state ($n=2$), the particle has zero probability of ever being detected at the center $x = L/2$, yet it has equal probability peaks on either side at $x = L/4$ and $x = 3L/4$. "
                "In classical mechanics, a particle bouncing elastically between rigid walls spends equal time at all positions, exhibiting a strictly uniform probability density $P_{classical}(x) = 1/L$ everywhere inside the box."
            )
            paragraphs.append(
                "The connection between the quantum and classical distributions is elucidated by Bohr's correspondence principle. "
                "As the quantum number $n$ becomes very large ($n \\gg 1$), the spatial oscillations of $\\sin^2(n\\pi x / L)$ become exceedingly dense. "
                "Any macroscopic detector with finite spatial resolution integrates over many rapid oscillations; because the spatial average of $\\sin^2\\theta$ is $\\frac{1}{2}$, $\\langle P_n(x) \\rangle = \\frac{2}{L}\\left(\\frac{1}{2}\\right) = \\frac{1}{L}$, exactly recovering the uniform classical probability density."
            )
        elif any(k in s_low for k in ["laser", "nanostructure", "application", "quantum well lasers"]):
            paragraphs.append(
                "The particle-in-a-box model serves as the foundational physical blueprint for modern semiconductor quantum heterostructures and quantum well devices. "
                "By sandwiching an ultra-thin layer of a narrow-bandgap semiconductor (such as GaAs, thickness $\\sim 5-10\\text{ nm}$) between two layers of a wider-bandgap semiconductor (such as AlGaAs), "
                "conduction band electrons and valence band holes are confined within an authentic one-dimensional potential well."
            )
            paragraphs.append(
                "This nanoscale spatial confinement quantizes the electronic energy levels in the perpendicular direction. "
                "In Quantum Well Lasers, this discrete energy quantization significantly sharpens the electronic density of states from a 3D parabolic distribution into a 2D step function, "
                "dramatically reducing the threshold current density and thermal sensitivity compared to conventional bulk semiconductor lasers."
            )
            paragraphs.append(
                "Furthermore, the emission wavelength of quantum well lasers and quantum dot devices can be continuously engineered simply by adjusting the physical thickness $L$ of the well during epitaxial growth: $\\lambda_{emission} \\propto \\frac{1}{E_g + \\frac{h^2}{8m^* L^2}}$. "
                "This quantum size effect powers optical telecommunication lasers operating at 1.31 and 1.55 $\\mu$m, quantum cascade lasers for molecular sensing, and quantum well infrared photodetectors (QWIP)."
            )
        elif any(k in s_low for k in ["correspondence", "classical limit"]):
            paragraphs.append(
                "Bohr's correspondence principle dictates that quantum theoretical predictions must smoothly converge to classical Newtonian physics in the macroscopic limit. "
                "For the particle in a box, this transition occurs when the quantum number $n$ becomes enormous, or when the physical mass $m$ and box width $L$ represent everyday macroscopic scales."
            )
            paragraphs.append(
                "Consider a macroscopic ball of mass $m = 1\\text{ g} = 10^{-3}\\text{ kg}$ confined inside a box of width $L = 10\\text{ cm} = 0.1\\text{ m}$, moving at an ordinary speed of $v = 1\\text{ cm/s} = 0.01\\text{ m/s}$. "
                "The kinetic energy is $E = \\frac{1}{2}mv^2 = 5 \\times 10^{-8}\\text{ J}$. "
                "Equating this energy to the quantum formula $E_n = \\frac{n^2 h^2}{8mL^2}$ yields a quantum number on the order of $n \\approx 3 \\times 10^{24}$."
            )
            paragraphs.append(
                "The energy difference between adjacent levels at this quantum scale is $\\Delta E = \\frac{(2n+1)h^2}{8mL^2} \\approx 3 \\times 10^{-32}\\text{ J}$. "
                "This energy spacing is forty orders of magnitude smaller than the thermal energy $k_B T \\approx 4 \\times 10^{-21}\\text{ J}$ at room temperature, making the discrete energy spectrum utterly indistinguishable from a continuous classical continuum. "
                "Simultaneously, the nodal spacing $\\Delta x = L/n \\approx 3 \\times 10^{-26}\\text{ m}$ is infinitely finer than any physical probe, rendering the quantum probability density completely indistinguishable from the uniform classical distribution."
            )
        elif any(k in s_low for k in ["formulation", "governing equations", "mathematical formulation"]):
            paragraphs.append(
                "The mathematical formulation of the particle in a box specifies the differential equation inside the potential well. "
                "With $V(x) = 0$ in the interior domain $0 < x < L$, the Time-Independent Schrödinger Equation simplifies to $-\\frac{\\hbar^2}{2m}\\frac{d^2\\psi(x)}{dx^2} = E\\psi(x)$. "
                "Rearranging into standard Helmholtz oscillator form yields $\\frac{d^2\\psi(x)}{dx^2} + k^2\\psi(x) = 0$, where wavenumber $k = \\frac{\\sqrt{2mE}}{\\hbar}$."
            )
            paragraphs.append(
                "Because the potential $V(x) = \\infty$ everywhere outside the well ($x \\le 0, x \\ge L$), the probability of finding the particle in the exterior barriers is identically zero: $\\psi(x) = 0$. "
                "Enforcing continuity of the wave function at the hard physical interfaces requires Dirichlet boundary conditions: $\\psi(0) = 0$ and $\\psi(L) = 0$. "
                "However, the derivative $\\frac{d\\psi}{dx}$ is not continuous at the boundaries because the potential energy undergoes an infinite discontinuous jump."
            )
            paragraphs.append(
                "The general linear combination of independent solutions within the well is $\\psi(x) = A\\sin(kx) + B\\cos(kx)$. "
                "Setting the stage for boundary value matching, this mathematical formulation establishes that the physical particle behaves as a trapped de Broglie matter wave undergoing continuous total internal reflection between rigid barriers."
            )
        elif any(k in s_low for k in ["derivation", "boundary", "dirichlet", "boundary conditions"]):
            paragraphs.append(
                "To formulate the boundary value problem for a particle of mass $m$ inside a one-dimensional box, we specify the potential energy profile: $V(x) = 0$ for $0 < x < L$, and $V(x) = \\infty$ for $x \\le 0$ and $x \\ge L$. "
                "In the exterior regions ($x \\le 0, x \\ge L$), the infinite potential barrier represents an impenetrable wall, requiring $\\psi(x) = 0$ everywhere outside the box. "
                "Enforcing wave function continuity at the interfaces mandates rigid Dirichlet boundary conditions: $\\psi(0) = 0$ and $\\psi(L) = 0$."
            )
            paragraphs.append(
                "Inside the interior cavity ($0 < x < L$), the potential $V(x) = 0$, reducing the Time-Independent Schrödinger Equation to the harmonic oscillator differential equation:\n\n"
                "$$\\frac{d^2\\psi(x)}{dx^2} + k^2 \\psi(x) = 0, \\quad k = \\frac{\\sqrt{2mE}}{\\hbar}$$\n\n"
                "The general mathematical solution is a linear combination of sinusoids: $\\psi(x) = A\\sin(kx) + B\\cos(kx)$. "
                "Applying the left boundary condition at $x = 0$ requires $\\psi(0) = A\\sin(0) + B\\cos(0) = B = 0$, eliminating the cosine term and leaving $\\psi(x) = A\\sin(kx)$."
            )
            paragraphs.append(
                "Applying the right boundary condition at $x = L$ requires $\\psi(L) = A\\sin(kL) = 0$. "
                "To obtain a non-trivial physical solution ($A \\ne 0$), the argument must satisfy the discrete transcendental condition $kL = n\\pi$, "
                "establishing discrete wavenumber quantization $k_n = \\frac{n\\pi}{L}$ for positive integer quantum numbers $n = 1, 2, 3, \\dots$. "
                "This rigorous boundary matching demonstrates that energy quantization in quantum mechanics arises naturally from wave boundary constraints, exactly analogous to standing harmonics on a vibrating acoustic string."
            )
        else: # Concept / Geometry / Default
            paragraphs.append(
                "Consider a non-relativistic quantum particle of mass $m$ confined within a one-dimensional infinite potential well defined by: "
                "$V(x) = 0$ for $0 < x < L$, and $V(x) = \\infty$ for $x \\le 0$ and $x \\ge L$. "
                "Because the potential barrier is infinitely impenetrable outside the well, the particle has zero probability of penetrating the walls, "
                "mandating rigid Dirichlet boundary conditions: $\\psi(0) = 0$ and $\\psi(L) = 0$. "
                "Within the interior interval $0 < x < L$, the time-independent Schrödinger equation simplifies to $\\frac{d^2\\psi}{dx^2} + k^2\\psi = 0$, where wavenumber $k = \\frac{\\sqrt{2mE}}{\\hbar}$."
            )
            paragraphs.append(
                "The physical concept of the potential well model represents the most fundamental solvable paradigm in quantum mechanics, illustrating how spatial confinement alone forces continuous physical quantities into discrete, quantized states. "
                "The geometry of the well confines the wave function entirely within the interval $[0, L]$, creating internal standing waves whose nodes and antinodes dictate where the particle may and may not be found."
            )
            paragraphs.append(
                "The particle-in-a-box model demonstrates three universal hallmarks of quantum confinement: the quantization of energy levels into discrete steps $E_n \\propto n^2$, the existence of a non-zero zero-point ground state energy $E_1 > 0$, and the appearance of nodal structures in spatial probability distributions. "
                "These insights form the conceptual foundation for understanding electronic structures in atoms, quantum dots, and conjugated organic molecules."
            )

    # -------------------------------------------------------------------------
    # Topic 12: Quantum Mechanical Applications
    # -------------------------------------------------------------------------
    elif "application" in t_low or "quantum mechanical applications" in t_low or "tunnel" in t_low:
        if any(k in s_low for k in ["barrier", "tunnel", "penetration", "stm", "tunneling devices"]):
            paragraphs.append(
                "Quantum mechanical barrier penetration, or quantum tunneling, represents one of the most striking departures from classical physics. "
                "In classical mechanics, a particle of energy $E$ incident upon a potential barrier of height $V_0 > E$ is strictly reflected: it possesses negative kinetic energy inside the barrier, which is physically impossible. "
                "In quantum wave mechanics, the wave function inside the barrier satisfies $\\frac{d^2\\psi}{dx^2} - \\kappa^2\\psi = 0$, where $\\kappa = \\frac{\\sqrt{2m(V_0 - E)}}{\\hbar}$, yielding an exponentially decaying evanescent wave $\\psi(x) \\sim e^{-\\kappa x}$."
            )
            paragraphs.append(
                "For a barrier of finite spatial width $a$, the evanescent wave does not completely extinguish before reaching the opposite barrier interface. "
                "It emerges on the other side as a transmitted wave with finite non-zero amplitude, resulting in a transmission probability:\n\n"
                "$$T \\approx 16 \\frac{E}{V_0}\\left(1 - \\frac{E}{V_0}\\right) e^{-2\\kappa a}$$\n\n"
                "Because transmission decays exponentially with barrier thickness $a$ and decay factor $\\kappa$, tunneling is extraordinarily sensitive to nanoscale barrier dimensions. "
                "This quantum phenomenon governs alpha decay in nuclear physics, explaining why alpha particle half-lives vary across 24 orders of magnitude for small variations in alpha energy (Geiger-Nuttall law)."
            )
            paragraphs.append(
                "In modern nanotechnology, the primary application of quantum barrier tunneling is the Scanning Tunneling Microscope (STM), invented by Gerd Binnig and Heinrich Rohrer in 1981 (1986 Nobel Prize). "
                "In an STM, an atomically sharp conductive metal tip is brought within sub-nanometer proximity of a conductive sample surface. "
                "Applying a small bias voltage causes electrons to tunnel through the vacuum gap; because tunneling current scales exponentially with gap separation ($I \\propto e^{-2\\kappa s}$), changing the gap by a single angstrom ($0.1\\text{ nm}$) alters the tunneling current by a factor of 10. "
                "Scanning the tip across the surface while maintaining constant tunneling current maps the surface topography with atomic resolution, allowing individual atoms to be visualized and manipulated."
            )
        else: # Heterostructures / Quantum Dots / SQUIDs / Devices / Default
            paragraphs.append(
                "The second quantum revolution exploits quantum mechanical coherence, superposition, and confinement to engineer transformative solid-state electronic and optoelectronic devices. "
                "Nanoscale semiconductor heterostructures confine charge carriers across zero, one, or two dimensions: quantum wells exhibit 2D planar confinement, quantum wires exhibit 1D confinement, and quantum dots provide complete 3D spatial confinement."
            )
            paragraphs.append(
                "In Quantum Dots ('artificial atoms'), 3D confinement discretizes the electronic density of states into delta-function energy levels. "
                "By tuning the physical radius $R$ of the quantum dot nanocrystal, the effective optical bandgap shifts according to the Brus equation: $\\Delta E_g \\propto \\frac{\\hbar^2 \\pi^2}{2m^* R^2}$, "
                "allowing precise color tuning across the entire visible and infrared spectrum. This powers high-color-gamut Quantum Dot Displays (QLED), biological fluorescent biomarkers, and ultra-high-efficiency multi-junction solar cells."
            )
            paragraphs.append(
                "Furthermore, macroscopic quantum coherence enables Superconducting Quantum Interference Devices (SQUIDs). "
                "A SQUID consists of a superconducting loop interrupted by one or two insulating Josephson tunneling barriers. "
                "Exploiting fluxoid quantization $\\Phi_0 = \\frac{h}{2e} \\approx 2.07 \\times 10^{-15}\\text{ Wb}$ and quantum phase interference across the junctions, SQUIDs detect magnetic field variations on the order of $10^{-15}\\text{ T}$ (femtoteslas). "
                "This extraordinary sensitivity enables Magnetoencephalography (MEG) brain imaging, geophysical magnetometry, and provides the read-out architecture for superconducting transmon qubits in quantum supercomputing."
            )

    # -------------------------------------------------------------------------
    # Fallback / General Blueprint Archetypes
    # -------------------------------------------------------------------------
    else:
        if any(k in s_low for k in ["concept", "principle", "fundamental"]):
            paragraphs.append(
                f"The foundational concept of {topic} forms an integral cornerstone of modern physics and technical engineering. "
                "Historically, classical mechanical formulations proved insufficient to explain experimental observations involving microscopic atomic phenomena and high-frequency wave propagation. "
                "By establishing formal mathematical relationships between boundary constraints, state variables, and conservation laws, the conceptual framework provides an unambiguous description of underlying physical reality."
            )
            paragraphs.append(
                f"Under rigorous analysis, {subtopic} addresses the physical mechanisms governing energy distribution and state transitions. "
                "Physical observables are systematically categorized into generalized coordinates and conjugate momenta, ensuring that the physical state conforms to fundamental invariance principles. "
                "This conceptual treatment provides the physical intuition necessary to construct analytical governing equations and interpret empirical measurement outcomes."
            )
            paragraphs.append(
                f"Furthermore, understanding the principles governing {topic} enables predictive modeling in advanced technological contexts. "
                "Whether analyzing microscale charge transport, resonant field interactions, or relativistic kinematics, "
                "the foundational principles establish the theoretical boundaries within which modern engineering systems operate."
            )
        elif any(k in s_low for k in ["formulation", "equation", "mathematical"]):
            paragraphs.append(
                f"The mathematical formulation of {topic} translates physical principles into rigorous analytical governing equations. "
                "Beginning from first principles and conservation theorems, the physical system is defined across a continuous manifold parameterized by spatial coordinates and time. "
                "Differential operators and constitutive material parameters are introduced to represent field interactions and dynamical state responses."
            )
            paragraphs.append(
                f"In treating {subtopic}, governing differential equations are developed by balancing localized flux rates against source and dissipation densities. "
                "Linearizing the governing equations for small perturbations yields standard eigenvalue equations of the form $\\mathcal{L}\\psi = \\lambda\\psi$, "
                "where the differential operator $\\mathcal{L}$ embodies the geometry, boundary conditions, and material properties of the system."
            )
            paragraphs.append(
                "Establishing this formal mathematical framework guarantees that solutions satisfy existence and uniqueness criteria. "
                "It enables the derivation of analytical dispersion relations, normal modes, and response functions that characterize the system under arbitrary external excitations."
            )
        elif any(k in s_low for k in ["derivation", "proof", "analytical"]):
            paragraphs.append(
                f"The analytical derivation for {topic} proceeds systematically from foundational postulates and governing differential equations. "
                "Applying boundary conditions and symmetry constraints, the general solution is simplified into specific functional forms. "
                "Step-by-step algebraic substitution isolates key physical parameters, eliminating redundant degrees of freedom."
            )
            paragraphs.append(
                f"Evaluating {subtopic} requires applying integral transforms and orthogonality relations across the domain. "
                "Integrating the governing differential equation subject to Dirichlet and Neumann boundary conditions yields the definitive closed-form relation connecting independent variables to observable response metrics. "
                "Each intermediate mathematical step is justified by physical continuity and energy conservation constraints."
            )
            paragraphs.append(
                "The derived analytical result provides quantitative predictive power, demonstrating how changing operational parameters influences physical behavior. "
                "Comparing the derived expression against limiting asymptotic cases confirms consistency with established classical and quantum benchmarks."
            )
        elif any(k in s_low for k in ["interpretation", "significance", "physical interpretation"]):
            paragraphs.append(
                f"The physical interpretation of {topic} connects abstract mathematical solutions to measurable laboratory phenomena. "
                "Analyzing spatial distributions, phase relationships, and spectral characteristics reveals how energy, momentum, and information propagate through the physical medium. "
                "Eigenvalues correspond to observable measurement spectra, while eigenfunctions determine localized probability densities and field amplitudes."
            )
            paragraphs.append(
                f"In the context of {subtopic}, examining limiting cases provides deep insight into operational behavior. "
                "In high-energy or macroscopic limits, solutions converge smoothly to classical continuum mechanics according to the correspondence principle. "
                "Conversely, in low-energy or microscopic limits, discrete quantum effects and wave interference dominate the physical response."
            )
            paragraphs.append(
                "This physical understanding bridges theoretical modeling and experimental verification. "
                "It enables engineers and physicists to identify key sensitivities, optimize operational parameters, and avoid non-physical regimes in practical devices."
            )
        elif any(k in s_low for k in ["application", "engineering", "technological"]):
            paragraphs.append(
                f"Technological applications of {topic} span modern telecommunications, solid-state electronics, and advanced materials engineering. "
                "By translating foundational wave and quantum principles into practical device architectures, engineers exploit microscopic phenomena to achieve macroscopic performance enhancements."
            )
            paragraphs.append(
                f"Specifically, {subtopic} plays a vital role in optimizing device efficiency, signal fidelity, and energy throughput. "
                "In solid-state and optoelectronic systems, tailoring spatial dimensions and material interfaces allows precise control over resonant frequencies, carrier mobilities, and optical transmission spectra. "
                "These engineering innovations underpin high-speed semiconductor components, sensor networks, and precision metrology instruments."
            )
            paragraphs.append(
                "Ongoing research continues to expand the technological frontier through nano-fabrication and quantum-enhanced devices. "
                "As physical dimensions scale down to the nanometer regime, the governing principles discussed here provide the essential design rules for next-generation computing and communication hardware."
            )
        else: # Limitations / Boundary Conditions / General Default
            paragraphs.append(
                f"The operational limitations and boundary behavior of {topic} define the domain of validity for the underlying mathematical models. "
                "All physical theories rely upon specific idealizations—such as non-relativistic approximations, linear material responses, or isolated boundary conditions—which break down when subjected to extreme operating parameters."
            )
            paragraphs.append(
                f"Analyzing {subtopic} highlights the precise conditions under which higher-order corrections or alternative theoretical frameworks must be incorporated. "
                "When field strengths produce non-linear saturation, or when velocities approach the speed of light, relativistic or non-linear field equations become mandatory to prevent non-physical divergences."
            )
            paragraphs.append(
                "Recognizing these operational boundaries is essential for sound engineering design and scientific research. "
                "It ensures that analytical and computational models remain robust, reliable, and predictive across all practical operating regimes."
            )

    return paragraphs



def generate_wave_optics_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Wave Optics topics."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    # Topic 1: Introduction to Wave Optics
    if "intro" in t_low:
        if "huygens" in s_low:
            paragraphs.append(
                "Christian Huygens formulated his celebrated wave construction principle in 1678, postulating that every point on an advancing wavefront acts as a secondary source of spherical wavelets. "
                "These secondary wavelets propagate forward through the medium with the characteristic phase velocity of the wave, and the new wavefront at any subsequent instant is defined geometrically as the forward envelope tangent to all secondary wavelets."
            )
            paragraphs.append(
                "Applying Huygens' wave construction to a plane wavefront incident obliquely upon a plane boundary between two media of refractive indices $n_1$ and $n_2$ rigorously derives the fundamental laws of geometric optics from wave principles. "
                "Let a plane wavefront $AB$ strike the interface at angle of incidence $i$. As point $B$ travels distance $BC = v_1 t$ in medium 1, the secondary wavelet from point $A$ expands across distance $AD = v_2 t$ in medium 2. "
                "Drawing tangent $CD$ defines the refracted wavefront. From the geometry of right triangles $\\Delta ABC$ and $\\Delta ADC$ with common hypotenuse $AC$:\n\n"
                "$$\\sin i = \\frac{BC}{AC} = \\frac{v_1 t}{AC}, \\quad \\sin r = \\frac{AD}{AC} = \\frac{v_2 t}{AC}$$\n\n"
                "Dividing the two relations yields Snell's law of refraction:\n\n"
                "$$\\frac{\\sin i}{\\sin r} = \\frac{v_1}{v_2} = \\frac{c / n_1}{c / n_2} = \\frac{n_2}{n_1} = \\mu$$\n\n"
                "This wave-theoretical derivation demonstrated that light travels slower in optically denser media ($v_2 < v_1$ when $n_2 > n_1$), directly contradicting Newton's corpuscular model which had incorrectly predicted faster velocities in denser media."
            )
        else:
            paragraphs.append(
                "The historical development of optical physics witnessed a protracted debate between Isaac Newton's corpuscular theory and Christian Huygens' wave theory. "
                "Newton posited that light consists of microscopic material corpuscles emitted by luminous bodies, which explained rectilinear propagation and sharp geometric shadows. "
                "However, the corpuscular theory struggled to explain partial reflection, refraction into denser media without acceleration, and the non-scattering crossing of light beams."
            )
            paragraphs.append(
                "The wave theory emerged triumphant in the early nineteenth century through the pioneering experiments of Thomas Young and Augustin-Jean Fresnel. "
                "Fresnel synthesized Huygens' wavelet construction with the principle of mutual wave interference, creating the Huygens-Fresnel wave theory. "
                "This unified framework proved that light propagation is governed by harmonic scalar and vector fields, and that classical rectilinear propagation is merely an asymptotic limiting case when the optical aperture dimensions are vastly larger than the optical wavelength ($\\lambda \\ll D$)."
            )

    # Topic 2: Interference of Light
    elif "interference of light" in t_low or (t_low == "interference"):
        if "condition" in s_low:
            paragraphs.append(
                "To observe stable, high-contrast, stationary optical interference fringes, the interfering light waves must satisfy four rigorous conditions: "
                "1. **Coherence:** The phase difference $\\delta$ between the interfering sources must remain strictly invariant over the observation time interval. "
                "Independent thermal light sources undergo random phase jumps every $10^{-9}\\text{ to }10^{-10}\\text{ seconds}$, causing rapid intensity fluctuations that average out to uniform illumination $I = I_1 + I_2$ unless derived from a common wavefront or laser oscillator."
            )
            paragraphs.append(
                "2. **Monochromaticity:** The light sources must emit radiation over a vanishingly narrow frequency band $\\Delta\\nu \\approx 0$. If polychromatic white light is used, different spectral wavelengths produce overlapping fringe patterns of varying spatial widths, washing out the pattern after only a few central colored fringes.\n"
                "3. **Equal or Comparable Amplitudes:** High fringe contrast (visibility $V = \\frac{I_{max} - I_{min}}{I_{max} + I_{min}}$) requires $a_1 \\approx a_2$. When amplitudes are equal, $I_{min} = 0$ and fringe visibility reaches unity ($V = 1$).\n"
                "4. **State of Polarization:** The interfering waves must oscillate in identical states of polarization. As established by the Fresnel-Arago laws, light waves polarized in mutually orthogonal planes cannot interfere to produce spatial intensity modulation."
            )
        else:
            paragraphs.append(
                "The physical phenomenon of optical interference arises from the linear superposition principle governing electromagnetic wave propagation. "
                "Consider two monochromatic light waves emitted from coherent sources with identical angular frequency $\\omega$ and wavenumbers $k$, "
                "described by scalar electric fields $E_1 = a_1 \\cos(kx - \\omega t)$ and $E_2 = a_2 \\cos(kx - \\omega t + \\delta)$, "
                "where $\\delta$ represents the constant spatial phase difference between the two waves."
            )
            paragraphs.append(
                "According to the principle of linear superposition, the resultant electric field at any spatial coordinate is the algebraic sum $E = E_1 + E_2$. "
                "Expanding using trigonometric addition identities yields a resultant harmonic wave $E = A \\cos(kx - \\omega t + \\theta)$, "
                "where the resultant amplitude $A$ satisfies:\n\n"
                "$$A^2 = a_1^2 + a_2^2 + 2 a_1 a_2 \\cos\\delta$$\n\n"
                "Because the optical intensity $I$ recorded by detectors is proportional to the time-averaged square of the electric field ($I \\propto \\langle E^2 \\rangle$), "
                "the spatial intensity distribution is given by the general interference equation:\n\n"
                "$$I = I_1 + I_2 + 2 \\sqrt{I_1 I_2} \\cos\\delta$$\n\n"
                "The cross-term $2\\sqrt{I_1 I_2}\\cos\\delta$ is the interference term. "
                "When $\\delta = 2n\\pi$ ($n = 0, 1, 2, \\dots$), $\\cos\\delta = +1$, producing constructive interference with maximum intensity $I_{max} = (\\sqrt{I_1} + \\sqrt{I_2})^2$. "
                "When $\\delta = (2n + 1)\\pi$, $\\cos\\delta = -1$, producing destructive interference with minimum intensity $I_{min} = (\\sqrt{I_1} - \\sqrt{I_2})^2$. "
                "If the amplitudes are equal ($I_1 = I_2 = I_0$), the intensity profile simplifies to $I = 4 I_0 \\cos^2(\\delta / 2)$, "
                "varying from a maximum of $4I_0$ to total darkness $0$, preserving total integrated radiant energy across the interference field."
            )

    # Topic 3: Coherent Sources
    elif "coherent" in t_low:
        if "temporal" in s_low:
            paragraphs.append(
                "Temporal coherence measures the correlation between the phase of a light wave at a given spatial point at time $t$ and its phase at the same point at a later time $t + \\tau$. "
                "In atomic emission, an excited atom radiates an electromagnetic wave train of finite duration $\\tau_c$, known as the coherence time. "
                "During this interval $\\tau_c$, the phase of the radiated wave remains continuous and predictable."
            )
            paragraphs.append(
                "The longitudinal distance across which the wave remains sinusoidally phase-correlated is the coherence length $l_c = c \\tau_c$. "
                "According to the Fourier bandwidth theorem, the temporal duration $\\tau_c$ and the spectral frequency spread $\\Delta\\nu$ satisfy $\\tau_c \\cdot \\Delta\\nu \\approx 1$. "
                "Relating frequency spread to spectral wavelength spread $\\Delta\\lambda$ via $|\\Delta\\nu| = \\frac{c}{\\lambda^2} \\Delta\\lambda$ yields the canonical coherence length expression:\n\n"
                "$$l_c = c \\tau_c = \\frac{c}{\\Delta\\nu} = \\frac{\\lambda^2}{\\Delta\\lambda}$$\n\n"
                "For conventional filtered incandescent sources, the linewidth $\\Delta\\lambda \\approx 10\\text{ nm}$ yields an extremely short coherence length $l_c \\approx 0.03\\text{ mm}$. "
                "In contrast, stabilized continuous-wave gas lasers (such as Helium-Neon) achieve linewidths below $10^{-6}\\text{ nm}$, "
                "yielding coherence lengths exceeding hundreds of meters or even kilometers, which is essential for long-range holography and precision interferometry."
            )
        else:
            paragraphs.append(
                "Spatial coherence characterizes the phase correlation between light vibrations at two spatially separated points $P_1$ and $P_2$ across the wavefront at the same instant of time $t$. "
                "If an extended light source has lateral linear dimension $w$ and illuminates an aperture plane at distance $D$, light arriving at points separated by lateral distance $d$ "
                "remains mutually coherent only if the path difference from opposite edges of the source to the aperture points is less than half a wavelength: $w \\cdot \\frac{d}{D} \\le \\frac{\\lambda}{2}$."
            )
            paragraphs.append(
                "This geometric constraint defines the spatial coherence width $l_s = \\frac{\\lambda D}{2w} = \\frac{\\lambda}{2\\theta}$, where $\\theta = w/D$ is the angular subtense of the luminous source. "
                "In optical system design, creating coherent secondary sources from thermal emitters requires either division of wavefront "
                "(as in Young's double slit or Fresnel biprism, where two parts of the same wavefront are isolated within the spatial coherence width) "
                "or division of amplitude (as in thin films, Michelson interferometers, or Newton's rings, where partial reflection splits the wave amplitude uniformly across the entire beam)."
            )

    # Topic 4: Young's Double Slit Experiment
    elif "young" in t_low or "double slit" in t_low:
        if "fringe" in s_low or "derivation" in s_low:
            paragraphs.append(
                "To derive the fringe width expression in Young's double slit experiment, consider two narrow slits $S_1$ and $S_2$ separated by distance $d$ illuminating a screen at distance $D$ ($D \\gg d$). "
                "Let $P$ be a point on the observation screen at vertical distance $y$ from the central optical axis. "
                "From the geometric right triangles $\\Delta S_1 P N_1$ and $\\Delta S_2 P N_2$, the paths traveled by the two interfering rays are:\n\n"
                "$$S_2 P^2 = D^2 + \\left(y + \\frac{d}{2}\\right)^2, \\quad S_1 P^2 = D^2 + \\left(y - \\frac{d}{2}\\right)^2$$"
            )
            paragraphs.append(
                "Subtracting the two equations yields $S_2 P^2 - S_1 P^2 = 2yd$. Factoring gives $(S_2 P - S_1 P)(S_2 P + S_1 P) = 2yd$. "
                "Under the paraxial approximation ($D \\gg d$ and $D \\gg y$), $S_2 P + S_1 P \\approx 2D$, yielding the optical path difference:\n\n"
                "$$\\Delta = S_2 P - S_1 P = \\frac{yd}{D}$$\n\n"
                "For bright fringes (constructive interference), the path difference must equal an integer number of wavelengths: $\\Delta = n\\lambda \\implies y_n = \\frac{n\\lambda D}{d}$ for $n = 0, \\pm 1, \\pm 2, \\dots$. "
                "The fringe width $\\beta$ is defined as the linear distance between two consecutive bright or dark fringes:\n\n"
                "$$\\beta = y_{n+1} - y_n = \\frac{(n+1)\\lambda D}{d} - \\frac{n\\lambda D}{d} = \\frac{\\lambda D}{d}$$\n\n"
                "This formula proves that the fringes are equally spaced across the observation screen, with fringe separation directly proportional to optical wavelength $\\lambda$ and screen distance $D$, and inversely proportional to slit separation $d$."
            )
        else:
            paragraphs.append(
                "In 1801, Thomas Young performed the double-slit experiment that provided the first incontrovertible experimental proof of the wave nature of light. "
                "Young allowed sunlight to pass through a pinhole in a window shutter, producing a spatially coherent expanding wavefront that illuminated two closely spaced pinholes (or parallel slits $S_1$ and $S_2$) in an opaque screen. "
                "On an observation screen placed beyond the double aperture, Young observed a series of alternating bright and dark bands rather than two geometric images of the slits."
            )
            paragraphs.append(
                "The experimental arrangement demonstrated division of wavefront: the primary expanding spherical wavefront reaches slits $S_1$ and $S_2$ with identical phase, transforming them into two synchronized coherent secondary sources. "
                "Where wave crests from $S_1$ superimpose constructively upon crests from $S_2$, light intensity reaches a maximum; where crests coincide destructively with troughs, mutual cancellation produces total darkness. "
                "This seminal demonstration successfully dismantled Newton's corpuscular dogma and established wave optics as the definitive physical model of light."
            )

    # Topic 5: Thin Film Interference
    elif "thin film" in t_low:
        if "transmitted" in s_low:
            paragraphs.append(
                "In transmitted thin-film light, the interfering rays emerging from the bottom interface undergo internal reflections exclusively at boundaries with rarer media, "
                "producing zero phase change. Consequently, the optical path difference in transmitted light is simply $\\Delta = 2\\mu t\\cos r$ without any phase shift. "
                "This makes the transmitted fringe conditions exactly complementary to the reflected fringes: the film is bright when $2\\mu t\\cos r = n\\lambda$ "
                "and dark when $2\\mu t\\cos r = (2n + 1)\\lambda/2$."
            )
            paragraphs.append(
                "Thin-film interference powers vital modern optical engineering technologies. "
                "In anti-reflective coatings applied to camera lenses and solar panels, a thin dielectric film (such as magnesium fluoride, $\\text{MgF}_2$, $\\mu = 1.38$) "
                "is vacuum-deposited onto glass ($\\mu_g = 1.52$). By selecting a film thickness equal to a quarter-wavelength ($t = \\lambda / 4\\mu$) at normal incidence ($r=0$), "
                "the path difference between reflections from the upper and lower surfaces equals $2\\mu t = \\lambda/2$. "
                "Because both reflections occur at rarer-to-denser interfaces, both experience a $\\pi$ phase shift; their relative path difference remains $\\lambda/2$, "
                "causing complete destructive interference that suppresses surface reflection from 4% down to under 0.1%."
            )
        else:
            paragraphs.append(
                "Interference in thin films arises through division of amplitude when an incident monochromatic light ray strikes a transparent film of thickness $t$ and refractive index $\\mu$. "
                "At the upper surface, a fraction of the wave is reflected while the remainder refracts into the film at angle $r$, undergoes internal reflection at the lower interface, "
                "and emerges back into the original medium parallel to the first reflected ray."
            )
            paragraphs.append(
                "The geometric optical path difference between the two reflected rays is $\\Delta_{geo} = 2\\mu t\\cos r$. "
                "Crucially, according to Stokes' relations governing dielectric reflection, when light is reflected at the surface of an optically denser medium, it experiences an abrupt phase shift of $\\pi$ radians, "
                "equivalent to adding or subtracting a path difference of $\\lambda/2$. The effective path difference in reflected light is therefore:\n\n"
                "$$\\Delta = 2\\mu t\\cos r - \\frac{\\lambda}{2}$$\n\n"
                "Constructive interference occurs when $\\Delta = n\\lambda \\implies 2\\mu t\\cos r = \\left(n + \\frac{1}{2}\\right)\\lambda$, creating a bright film. "
                "Destructive interference occurs when $\\Delta = \\left(n + \\frac{1}{2}\\right)\\lambda \\implies 2\\mu t\\cos r = n\\lambda$, rendering the film completely dark."
            )

    # Topic 6: Newton's Rings
    elif "newton" in t_low:
        if "measurement" in s_low or "wavelength" in s_low:
            paragraphs.append(
                "Newton's rings provide a classic demonstration of thin-film interference produced by division of amplitude in a variable-thickness wedge air film. "
                "The experimental arrangement comprises a plano-convex lens of very large radius of curvature $R$ resting on an optically flat glass plate. "
                "An air film of gradually increasing thickness $t$ is enclosed between the spherical curved surface and the plane plate. "
                "From the geometry of a circle of radius $R$, the thickness $t$ of the air film at a radial distance $r$ from the central point of contact is given by $t = \\frac{r^2}{2R}$."
            )
            paragraphs.append(
                "Illuminating the setup normally with monochromatic light ($\\cos r = 1$), the optical path difference in reflected light is $\\Delta = 2t + \\lambda/2 = \\frac{r^2}{R} + \\frac{\\lambda}{2}$. "
                "At the center of contact ($r=0$), $t=0$, so $\\Delta = \\lambda/2$, which satisfies the condition for destructive interference; hence, the central spot is always dark in reflected light. "
                "For the $n$-th dark ring, the condition for destruction is $\\Delta = \\left(n + \\frac{1}{2}\\right)\\lambda \\implies \\frac{r_n^2}{R} + \\frac{\\lambda}{2} = \\left(n + \\frac{1}{2}\\right)\\lambda \\implies \\frac{r_n^2}{R} = n\\lambda$. "
                "Expressing in terms of ring diameter $D_n = 2 r_n$ yields the dark ring diameter equation:\n\n"
                "$$D_n^2 = 4 n \\lambda R$$\n\n"
                "For two dark rings of orders $n$ and $n + p$, subtracting their squared diameters eliminates zero-offset errors:\n\n"
                "$$D_{n+p}^2 - D_n^2 = 4(n+p)\\lambda R - 4n\\lambda R = 4 p \\lambda R \\implies \\lambda = \\frac{D_{n+p}^2 - D_n^2}{4 p R}$$\n\n"
                "This formula allows high-precision experimental determination of optical wavelength $\\lambda$. "
                "Furthermore, if a liquid of refractive index $\\mu$ is introduced between the lens and plate, the path difference becomes $2\\mu t + \\lambda/2$, compressing the ring diameters according to $D_n^2 = \\frac{4n\\lambda R}{\\mu}$, allowing precision measurement of liquid refractive index as $\\mu = \\frac{(D_{n+p}^2 - D_n^2)_{air}}{(D_{n+p}^2 - D_n^2)_{liquid}}$."
            )
        else:
            paragraphs.append(
                "Newton's rings represent fringes of equal thickness (Fizeau fringes), where each ring traces out a locus of constant air-film thickness $t$. "
                "Because the air-film profile possesses circular cylindrical symmetry about the optical axis, the resulting interference fringes form concentric, "
                "alternating bright and dark circular rings centered on the point of contact."
            )
            paragraphs.append(
                "A notable geometric characteristic of Newton's rings is that the spacing between consecutive rings decreases progressively as the ring order $n$ increases. "
                "Because the ring diameter scales with the square root of the ring index ($D_n \\propto \\sqrt{n}$), the difference $\\Delta D = \\sqrt{n+1} - \\sqrt{n} \\approx \\frac{1}{2\\sqrt{n}}$ "
                "diminishes rapidly, causing the fringes to crowd together toward the outer periphery of the lens. "
                "This optical test serves as an indispensable standard in optical fabrication workshops for testing lens curvature and surface flatness down to nanometer tolerances."
            )

    # Topic 7: Fraunhofer Diffraction
    elif "fraunhofer" in t_low:
        if "intensity" in s_low:
            paragraphs.append(
                "To derive the single-slit Fraunhofer diffraction intensity profile, consider a monochromatic plane wave of wavelength $\\lambda$ incident normally on a slit of width $a$. "
                "Integrating secondary wavelet amplitudes across the slit aperture from $x = -a/2$ to $x = +a/2$ yields total complex electric field amplitude:\n\n"
                "$$E(\\theta) = \\int_{-a/2}^{a/2} \\frac{E_0}{a} e^{i \\frac{2\\pi}{\\lambda} x \\sin\\theta} dx = E_0 \\frac{\\sin\\alpha}{\\alpha}$$\n\n"
                "where the phase parameter $\\alpha$ is defined as $\\alpha = \\frac{\\pi a \\sin\\theta}{\\lambda}$."
            )
            paragraphs.append(
                "Squaring the field amplitude yields the celebrated single-slit Fraunhofer diffraction intensity distribution:\n\n"
                "$$I(\\theta) = I_0 \\left( \\frac{\\sin\\alpha}{\\alpha} \\right)^2$$\n\n"
                "The central maximum occurs at $\\theta = 0$ (where $\\lim_{\\alpha \\to 0} \\frac{\\sin\\alpha}{\\alpha} = 1$), producing peak intensity $I_0$. "
                "Diffraction minima occur wherever $\\sin\\alpha = 0$ with $\\alpha \\ne 0$, which mandates $\\alpha = m\\pi \\implies a \\sin\\theta = m\\lambda$ for $m = \\pm 1, \\pm 2, \\dots$. "
                "The angular half-width of the central maximum is $\\theta_1 \\approx \\frac{\\lambda}{a}$, giving a total angular spread of $2\\lambda/a$. "
                "Secondary maxima occur at transcendental roots of $\\tan\\alpha = \\alpha$ (at $\\alpha \\approx \\pm 1.43\\pi, \\pm 2.46\\pi$), possessing drastically reduced intensities of $I_1 \\approx 0.047 I_0$ (4.7%) and $I_2 \\approx 0.016 I_0$ (1.6%)."
            )
        else:
            paragraphs.append(
                "Fraunhofer diffraction represents far-field wave diffraction where both the incident wavefront and the diffracted wavefront are effectively planar, "
                "which is realized experimentally by placing collimating and focusing lenses before and after the diffracting aperture. "
                "Consider a monochromatic plane wave of wavelength $\\lambda$ incident normally upon a long rectangular slit of width $a$. "
                "According to Huygens' principle, the slit aperture acts as a continuous line of secondary wavelet sources of infinitesimal width $dx$."
            )
            paragraphs.append(
                "The physical intensity profile of Fraunhofer single-slit diffraction illustrates the reciprocal relationship between aperture dimension and wave spreading. "
                "As the slit width $a$ is narrowed toward the wavelength $\\lambda$, the angular spread of the central maximum $\\theta \\approx \\lambda/a$ expands dramatically, "
                "eventually spreading light across the entire half-space. Conversely, when $a \\gg \\lambda$, the diffraction spread shrinks to zero, recovering classical geometric optics with sharp shadow boundaries."
            )

    # Topic 8: Diffraction Grating
    elif "grating" in t_low:
        if "dispersive" in s_low or "power" in s_low:
            paragraphs.append(
                "The angular dispersive power $\\frac{d\\theta}{d\\lambda}$ measures the rate of angular separation per unit wavelength change. "
                "Differentiating the fundamental grating equation $(a + b)\\sin\\theta = n\\lambda$ with respect to $\\lambda$ gives:\n\n"
                "$$(a + b) \\cos\\theta \\frac{d\\theta}{d\\lambda} = n \\implies \\frac{d\\theta}{d\\lambda} = \\frac{n}{(a + b) \\cos\\theta}$$\n\n"
                "This demonstrates that angular dispersion is directly proportional to spectral order $n$ and inversely proportional to grating element $(a+b)$."
            )
            paragraphs.append(
                "A grating with 15,000 lines per inch exhibits an extremely small grating element $(a+b) \\approx 1.69\\,\\mu\\text{m}$, producing powerful dispersion that separates closely spaced spectral doublets such as the sodium D-lines (589.0 nm and 589.6 nm). "
                "Furthermore, if a principal maximum condition $(a+b)\\sin\\theta = n\\lambda$ coincides with a single-slit diffraction minimum $a\\sin\\theta = m\\lambda$, that spectral order vanishes completely from the spectrum, producing a missing order defined by the integer ratio $\\frac{a+b}{a} = \\frac{n}{m}$."
            )
        else:
            paragraphs.append(
                "A plane transmission diffraction grating consists of an array of a large number $N$ of parallel, equidistant, closely spaced transparent slits separated by opaque ruling lines. "
                "Let $a$ represent the width of each transparent slit and $b$ the width of each opaque ruling. "
                "The distance between centers of adjacent slits, $(a + b)$, is called the grating element or grating pitch."
            )
            paragraphs.append(
                "When a plane monochromatic wave of wavelength $\\lambda$ strikes the grating at normal incidence, each slit diffracts light into secondary wavelets. "
                "The path difference between corresponding wavelets emerging from adjacent slits at diffraction angle $\\theta$ is $\\Delta = (a + b)\\sin\\theta$. "
                "For waves from all $N$ slits to interfere constructively, this path difference must equal an integral number of wavelengths, establishing the fundamental grating equation:\n\n"
                "$$(a + b) \\sin\\theta = n \\lambda, \\quad n = 0, \\pm 1, \\pm 2, \\dots$$\n\n"
                "where $n$ represents the spectral order. The zero-th order ($n=0$) corresponds to undeviated light where all wavelengths overlap at $\\theta = 0$. "
                "For higher orders ($n \\ge 1$), diffracted angles depend on wavelength, dispersing composite light into its constituent spectral lines with razor-sharp intensity maxima."
            )

    # Topic 9: Resolving Power
    elif "resolving" in t_low:
        if "grating" in s_low or "resolving power of" in s_low:
            paragraphs.append(
                "For a diffraction grating with $N$ rulings in order $n$, the principal maximum for wavelength $\\lambda + d\\lambda$ occurs at angle $\\theta + d\\theta$ satisfying $(a+b)\\sin(\\theta + d\\theta) = n(\\lambda + d\\lambda)$. "
                "According to the Rayleigh criterion, this peak is just resolved from wavelength $\\lambda$ if it falls on the first adjacent diffraction minimum of $\\lambda$. "
                "The first minimum occurs when the total path difference across the entire grating width $N(a+b)$ equals $N n \\lambda + \\lambda$, so $(a+b)\\sin(\\theta + d\\theta) = n\\lambda + \\frac{\\lambda}{N}$."
            )
            paragraphs.append(
                "Equating these two expressions yields:\n\n"
                "$$n(\\lambda + d\\lambda) = n\\lambda + \\frac{\\lambda}{N} \\implies n d\\lambda = \\frac{\\lambda}{N}$$\n\n"
                "Rearranging defines the chromatic resolving power $R$ of a diffraction grating:\n\n"
                "$$R = \\frac{\\lambda}{d\\lambda} = n N$$\n\n"
                "This elegant result demonstrates that resolving power depends exclusively on the product of spectral order $n$ and total number of rulings $N$ illuminated by the incident beam, completely independent of the grating pitch $(a+b)$. "
                "To resolve the sodium doublet ($d\\lambda = 0.6\\text{ nm}$ at $\\lambda = 589.3\\text{ nm}$), the minimum required resolving power is $R = 589.3 / 0.6 \\approx 982$, which requires a minimum of $N = 491$ lines in second order ($n=2$)."
            )
        else:
            paragraphs.append(
                "Lord Rayleigh formulated the criterion governing the physical limit of resolution for optical instruments forming diffraction patterns. "
                "According to the Rayleigh criterion, two closely spaced spectral lines of wavelengths $\\lambda$ and $\\lambda + d\\lambda$ are considered just resolved "
                "when the principal maximum of the diffraction pattern of one wavelength falls exactly upon the first diffraction minimum of the adjacent wavelength."
            )
            paragraphs.append(
                "Resolving power measures the capacity of an optical system to separate images of two closely spaced point objects or spectral lines. "
                "It is inversely related to the limit of resolution: the smaller the angular or spatial separation between two just-resolvable features, the higher the resolving power of the instrument. "
                "For circular telescope apertures of diameter $D$, the angular limit of resolution is $\\theta_{min} = 1.22 \\frac{\\lambda}{D}$, highlighting why large astronomical mirrors are required to distinguish close binary stars."
            )

    # Topic 10: Polarization of Light
    elif "polarization" in t_low:
        if "double refraction" in s_low or "birefringence" in s_low or "refraction" in s_low:
            paragraphs.append(
                "Discovered by Erasmus Bartholin in 1669, double refraction (birefringence) occurs when an unpolarized light ray enters an anisotropic crystalline medium such as calcite ($\\text{CaCO}_3$) or quartz ($\\text{SiO}_2$), splitting into two distinct refracted rays polarized in mutually orthogonal planes. "
                "The two refracted rays are classified as the Ordinary ray (O-ray) and the Extraordinary ray (E-ray)."
            )
            paragraphs.append(
                "The O-ray obeys Snell's law of refraction in all directions, traveling with an identical phase velocity $v_o = c/n_o$ regardless of orientation because its electric field vector vibrates perpendicular to the crystal's optic axis, forming a spherical Huygens wavelet envelope. "
                "The E-ray violates Snell's law, traveling with an angle-dependent velocity $v_e(\\theta)$ and forming an ellipsoidal wavelet envelope. "
                "In negative uniaxial crystals like calcite ($n_o > n_e$), the E-ray travels faster than the O-ray along all directions except along the optic axis, where both wavelets touch ($v_o = v_e$). "
                "William Nicol utilized this phenomenon to construct the Nicol prism, cementing two calcite prisms with Canada balsam ($n = 1.55$) to eliminate the O-ray via total internal reflection while transmitting 100% plane-polarized E-rays."
            )
        else:
            paragraphs.append(
                "Polarization is a unique vector characteristic of transverse waves, describing the spatial orientation and geometric trace of the oscillating electric field vector $\\mathbf{E}$ over time. "
                "In unpolarized natural light emitted by thermal sources, electric field vectors oscillate randomly in all planes perpendicular to the propagation vector $\\mathbf{k}$. "
                "When light is plane-polarized, electric field oscillations are confined to a single fixed spatial plane."
            )
            paragraphs.append(
                "In 1812, Sir David Brewster discovered that when unpolarized light is incident upon a transparent dielectric surface (such as glass of refractive index $\\mu$) at a specific angle of incidence $i_p$ (the polarizing angle or Brewster's angle), "
                "the reflected light becomes 100% linearly polarized with its electric field vector oscillating strictly parallel to the reflecting interface (perpendicular to the plane of incidence). "
                "At Brewster's angle, the reflected and refracted rays are mutually perpendicular ($i_p + r = 90^\\circ$). "
                "Applying Snell's law $\\mu = \\frac{\\sin i_p}{\\sin r} = \\frac{\\sin i_p}{\\sin(90^\\circ - i_p)} = \\frac{\\sin i_p}{\\cos i_p}$ yields Brewster's law:\n\n"
                "$$\\tan i_p = \\mu$$\n\n"
                "For crown glass with $\\mu = 1.5$, Brewster's angle is $i_p = \\arctan(1.5) \\approx 56.3^\\circ$. This principle is widely utilized in polarizing sunglasses, laser Brewster windows to eliminate reflection losses, and anti-glare photography filters."
            )

    # Fallback / General Wave Optics
    else:
        paragraphs.append(
            f"Wave optics provides the physical and mathematical foundation for analyzing optical phenomena where the wave nature of light cannot be neglected. "
            f"In the context of {topic}, analyzing {subtopic} reveals how electromagnetic field oscillations produce constructive and destructive interference, spatial diffraction, or polarization control."
        )
        paragraphs.append(
            "These phenomena govern modern high-precision optical technologies, including anti-reflective thin-film coatings, high-resolution spectrometers, laser resonators, and nanophotonic waveguides."
        )

    return paragraphs


def generate_laser_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Laser topics with rigorous pedagogical depth."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    # Topic 1: Introduction to Lasers
    if "intro" in t_low:
        if "monochromatic" in s_low or "coherence" in s_low:
            paragraphs.append(
                "The distinguishing characteristics of laser radiation—extreme monochromaticity, spatial and temporal coherence, high directionality, and radiant brightness—separate lasers fundamentally from conventional thermal emitters. "
                "Conventional sources, such as incandescent lamps or gas discharges, generate optical flux through uncorrelated spontaneous emission events where individual atoms emit wave trains with randomized phases, polarizations, and propagation trajectories."
            )
            paragraphs.append(
                "In contrast, laser emission arises through stimulated emission within an optical resonant cavity, locking emitted photons into identical spatial and temporal electromagnetic modes. "
                "Spatial coherence ensures wavefronts remain uncorrupted across transverse apertures, allowing beams to be focused to diffraction-limited spot sizes of diameter $d \\approx 1.22 \\lambda / \\text{NA}$. "
                "Temporal coherence is characterized by long coherence times $\\tau_c = 1 / \\Delta\\nu$ and coherence lengths $l_c = c\\tau_c = c / \\Delta\\nu$. In stabilized single-frequency lasers, linewidths $\\Delta\\nu$ contract to kilohertz levels, yielding coherence lengths spanning hundreds of kilometers."
            )
            paragraphs.append(
                "These coherence properties enable precision optical interferometry, gravitational wave detection, high-resolution spectroscopy, and holographic data storage. "
                "Furthermore, beam divergence is bounded strictly by the diffraction limit $\\theta = 1.22 \\lambda / D$, producing highly collimated directional beams capable of delivering targeted energy across astronomical distances."
            )
        else:
            paragraphs.append(
                "The acronym LASER stands for 'Light Amplification by Stimulated Emission of Radiation'. "
                "Conceptualized theoretically by Albert Einstein in 1917 and demonstrated experimentally by Theodore Maiman in 1960 using a synthetic ruby crystal, lasers represent one of the foundational triumphs of twentieth-century applied physics."
            )
            paragraphs.append(
                "Every operational laser architecture incorporates three essential physical subsystems: "
                "1. **Active Gain Medium:** A macroscopic collection of atoms, ions, or semiconductor quantum structures with quantized energy manifolds capable of establishing population inversion.\n"
                "2. **Pumping Mechanism:** An external excitation source (optical flashlamps, electrical discharges, or carrier injection) delivering energy to selectively populate upper excited states over lower levels.\n"
                "3. **Optical Resonant Cavity:** A pair of dielectric-coated mirrors (one highly reflective mirror $R_1 \\approx 100\\%$ and an output coupler $R_2 < 100\\%$) providing positive optical feedback to recirculate stimulated photons through the gain volume."
            )
            paragraphs.append(
                "Lasing begins when single-pass round-trip optical gain exceeds cavity losses: $R_1 R_2 e^{2(\\gamma_{th} - \\alpha)L} = 1$, where $\\gamma_{th}$ is the threshold gain coefficient and $\\alpha$ represents distributed scattering and absorption losses. "
                "Once threshold is surpassed, stimulated multiplication rapidly depletes inverted populations until saturated gain balances total loss, sustaining stable continuous-wave or pulsed laser oscillations."
            )

    # Topic 2: Spontaneous Emission
    elif "spontaneous emission" in t_low or ("spontaneous" in t_low and "stimulated" not in t_low):
        if "lifetime" in s_low:
            paragraphs.append(
                "Spontaneous emission is the quantum relaxation process whereby an isolated atom in an excited state $E_2$ spontaneously decays to a lower state $E_1$ without external electromagnetic stimulation. "
                "The decay rate is governed exclusively by the atomic structure and the quantum electrodynamic density of vacuum electromagnetic states."
            )
            paragraphs.append(
                "The rate of population loss from state $E_2$ is governed by the differential equation:\n\n"
                "$$-\\left(\\frac{dN_2}{dt}\\right)_{spont} = A_{21} N_2$$\n\n"
                "where $A_{21}$ is Einstein's coefficient of spontaneous emission. Integrating this rate equation from initial population $N_2(0)$ yields exponential population decay: $N_2(t) = N_2(0) e^{-A_{21}t} = N_2(0) e^{-t / \\tau_{sp}}$, where $\\tau_{sp} = 1 / A_{21}$ defines the natural radiative lifetime of the excited state."
            )
            paragraphs.append(
                "For dipole-allowed electronic transitions in optical systems, typical spontaneous radiative lifetimes range from $10^{-8}\\text{ s}$ to $10^{-7}\\text{ s}$. "
                "Because spontaneous emission occurs with random phase and isotropic spatial orientation, it generates incoherent background noise in laser amplifiers, setting the fundamental Schawlow-Townes linewidth limit for laser oscillators."
            )
        else:
            paragraphs.append(
                "The quantum mechanical mechanism of spontaneous emission is explained through quantum electrodynamics (QED) as stimulated emission induced by zero-point vacuum electromagnetic fluctuations. "
                "Even in a total vacuum at absolute zero temperature, virtual vacuum field fluctuations perturb the excited atomic dipole, triggering radiative relaxation. In terms of quantum dipole radiation theory, the spontaneous emission transition probability is proportional to the modulus squared of the electric dipole matrix element $\\mu_{12} = \\langle \\psi_1 | e\\mathbf{r} | \\psi_2 \\rangle$, meaning transitions between states with identical parity are strictly dipole-forbidden."
            )
            paragraphs.append(
                "When an atom decays spontaneously, it emits a single photon carrying energy precisely equal to the atomic band separation: $h\\nu = E_2 - E_1$. "
                "Because each atom decays independently at an uncorrelated instance, the emitted radiation exhibits random polarization, random wavefront phases, and an isotropic $4\\pi$ steradian emission direction."
            )
            paragraphs.append(
                "In atomic systems with competing non-radiative relaxation channels (such as phonon emission or collision deactivation with rate $W_{nr}$), the effective state lifetime becomes $\\tau = (A_{21} + W_{nr})^{-1}$. "
                "Maximizing radiative quantum efficiency $\\eta_r = A_{21} / (A_{21} + W_{nr})$ is a critical prerequisite in selecting active materials for efficient solid-state and semiconductor lasers."
            )

    # Topic 3: Stimulated Emission
    elif "stimulated emission" in t_low or ("stimulated" in t_low and "absorption" not in t_low):
        if "einstein" in s_low or "probability" in s_low:
            paragraphs.append(
                "Stimulated emission, predicted by Albert Einstein in 1917, is the microscopic mechanism that provides coherent optical amplification in all laser systems. "
                "When an incident resonant photon of energy $h\\nu = E_2 - E_1$ interacts with an atom in excited state $E_2$, the oscillatory electric field induces the atomic dipole to transition downward to state $E_1$."
            )
            paragraphs.append(
                "The rate of stimulated transitions is proportional to both the excited state population $N_2$ and the spectral energy density $u(\\nu)$ of the incident radiation field:\n\n"
                "$$\\left(\\frac{dN_2}{dt}\\right)_{stim} = -B_{21} N_2 u(\\nu)$$\n\n"
                "where $B_{21}$ represents Einstein's coefficient of stimulated emission. The downward transition emits a second photon that is physically identical in frequency, phase, polarization, and propagation wavevector $\\mathbf{k}$ to the incident photon."
            )
            paragraphs.append(
                "This identical replication creates an avalanche multiplication of coherent photons: one photon triggers two, two trigger four, and $2^N$ coherent photons emerge through successive atomic encounters. "
                "Stimulated emission dominates over spontaneous emission when the radiation density satisfies $u(\\nu) \\gg A_{21} / B_{21}$, which requires high cavity photon densities achievable within low-loss optical resonators."
            )
        else:
            paragraphs.append(
                "Coherent photon multiplication is the physical foundation of laser amplification. "
                "Because the stimulated photon is emitted into the exact quantum mechanical mode occupied by the stimulating incident photon, the electromagnetic wave experiences phase-coherent gain."
            )
            paragraphs.append(
                "As an optical beam of intensity $I(z)$ propagates through an active gain medium along the $z$-axis, stimulated transitions add energy to the wave according to the differential equation:\n\n"
                "$$\\frac{dI(z)}{dz} = \\sigma_{21} (N_2 - N_1) I(z) = \\gamma(\\nu) I(z)$$\n\n"
                "where $\\sigma_{21} = \\sigma_{12}$ is the stimulated transition cross-section, and $\\gamma(\\nu) = \\sigma (N_2 - N_1)$ represents the optical gain coefficient. When $N_2 > N_1$, the gain coefficient is positive, resulting in exponential spatial amplification: $I(z) = I(0) e^{\\gamma z}$."
            )
            paragraphs.append(
                "If $N_2 < N_1$, absorption exceeds stimulated emission, causing exponential attenuation. "
                "Therefore, net optical amplification is physically impossible unless the active medium is pumped into a non-equilibrium state of population inversion where $N_2 > N_1$."
            )

    # Topic 4: Absorption Process
    elif "absorption" in t_low:
        if "cross section" in s_low:
            paragraphs.append(
                "The absorption cross section $\\sigma_{12}(\\nu)$ quantifies the effective geometric area presented by an absorbing atom to incident radiation of frequency $\\nu$. "
                "It directly relates the microscopic atomic transition probability to the macroscopic optical attenuation of a propagating light wave."
            )
            paragraphs.append(
                "The absorption cross section is related to Einstein's coefficient $B_{12}$ and the normalized atomic line-shape function $g(\\nu)$ by the formulation:\n\n"
                "$$\\sigma_{12}(\\nu) = \\frac{h\\nu}{c} B_{12} g(\\nu)$$\n\n"
                "where $\\int_{-\\infty}^{\\infty} g(\\nu) d\\nu = 1$. The macroscopic absorption coefficient $\\alpha(\\nu)$ of a medium with ground-state atomic density $N_1$ is $\\alpha(\\nu) = N_1 \\sigma_{12}(\\nu)$, leading directly to the Beer-Lambert attenuation law $I(z) = I(0) e^{-\\alpha z}$."
            )
            paragraphs.append(
                "Broadening mechanisms—homogeneous broadening (natural lifetime and phonon collisions) and inhomogeneous broadening (Doppler shift in gases or local crystal field variations in glasses)—dictate the spectral width of $g(\\nu)$. "
                "Understanding the magnitude and spectral profile of $\\sigma_{12}(\\nu)$ is essential for matching pump source emission spectra (such as flashlamps or laser diodes) to the absorption bands of active laser crystals. At the resonant transition frequency $\\nu_0$, the peak atomic cross-section evaluates to $\\sigma_0 = \\frac{\\lambda^2}{2\\pi} \\frac{A_{21}}{\\Delta\\nu}$, demonstrating that narrow atomic transitions interact far more strongly with resonant radiation fields than broadened bands."
            )
        else:
            paragraphs.append(
                "Induced absorption (or stimulated absorption) is the upward electronic transition where an atom in a lower energy level $E_1$ absorbs a photon of energy $h\\nu = E_2 - E_1$ from an external electromagnetic field and jumps to excited state $E_2$."
            )
            paragraphs.append(
                "The rate of induced upward transitions is formulated as:\n\n"
                "$$\\left(\\frac{dN_1}{dt}\\right)_{abs} = -B_{12} N_1 u(\\nu)$$\n\n"
                "where $B_{12}$ is Einstein's coefficient of induced absorption. Under thermodynamic equilibrium, absorption balances stimulated and spontaneous emission, preventing macroscopic light amplification. The transition probability per unit time per atom for induced upward absorption $W_{12} = B_{12} u(\nu)$ is strictly proportional to the external spectral radiation energy density $u(\nu)$."
            )
            paragraphs.append(
                "In any unpumped thermal medium, Boltzmann statistics dictates that $N_1 \\gg N_2$, meaning incident resonant photons are absorbed far more frequently than stimulated photons are created. "
                "To overcome this intrinsic absorption barrier and achieve laser action, an external energy pumping system must continuously inject energy to force $N_2$ to exceed $N_1$."
            )

    # Topic 5: Population Inversion
    elif "population inversion" in t_low or ("population" in t_low and "inversion" in t_low):
        if "pumping" in s_low:
            paragraphs.append(
                "Pumping is the process of supplying external energy to an active laser medium to produce and sustain population inversion ($N_2 > N_1$). "
                "Because thermal equilibrium always favors lower energy states, pumping must be an energetic non-equilibrium process capable of driving atoms upward faster than their spontaneous relaxation rate."
            )
            paragraphs.append(
                "Common pumping mechanisms include: "
                "1. **Optical Pumping:** Using intense flashlamps or diode laser arrays to excite active atoms, widely utilized in solid-state systems like Nd:YAG and Ruby.\n"
                "2. **Electrical Discharge Pumping:** Accelerating electrons in an electric field to collide with gas atoms or molecules, utilized in He-Ne, Argon ion, and $\\text{CO}_2$ gas lasers.\n"
                "3. **Direct Electrical Carrier Injection:** Forward-biasing a semiconductor p-n junction to inject electrons and holes into a degenerate recombination region.\n"
                "4. **Chemical Pumping:** Utilizing exothermic chemical reactions to generate population inversion directly in product molecules (e.g., HF and chemical oxygen-iodine lasers)."
            )
            paragraphs.append(
                "Achieving steady-state population inversion requires an energy level scheme of at least three or four levels. "
                "In a three-level system, the lower laser level is the ground state, requiring more than 50% of all ground-state atoms to be excited before reaching threshold. "
                "In a four-level system, the lower laser level decays rapidly to the ground state, remaining nearly unpopulated ($N_1 \\approx 0$), which reduces threshold pump power by orders of magnitude."
            )
        else:
            paragraphs.append(
                "In any thermodynamic system at thermal equilibrium temperature $T$, atomic population distributions across discrete energy states obey the classical Maxwell-Boltzmann distribution law:\n\n"
                "$$\\frac{N_2}{N_1} = \\frac{g_2}{g_1} e^{-(E_2 - E_1) / k_B T}$$\n\n"
                "where $g_1, g_2$ are statistical degeneracy factors and $k_B$ is the Boltzmann constant."
            )
            paragraphs.append(
                "For optical transitions where photon energy $\\Delta E = h\\nu \\approx 2\\text{ eV}$ and thermal energy at room temperature ($T = 300\\text{ K}$) is $k_B T \\approx 0.0259\\text{ eV}$, the exponential factor evaluates to $e^{-2 / 0.0259} \\approx e^{-77} \\approx 10^{-34}$. "
                "Consequently, the excited state population $N_2$ in thermal equilibrium is virtually zero. Stimulated emission is completely overwhelmed by resonant absorption."
            )
            paragraphs.append(
                "Population inversion represents a state where $N_2 > (g_2/g_1) N_1$, a condition mathematically equivalent to an effective 'negative absolute temperature' in the Boltzmann equation. "
                "Because a two-level atomic system driven by radiation reaches at most equal populations ($N_2 = N_1$) due to equal absorption and stimulated emission coefficients ($B_{12} = B_{21}$), steady-state population inversion fundamentally requires multi-level quantum dynamics."
            )

    # Topic 6: Metastable States
    elif "metastable" in t_low:
        if "role" in s_low or "lasing" in s_low:
            paragraphs.append(
                "Metastable states play an indispensable functional role in laser physics by serving as an energy reservoir where excited atoms accumulate to establish population inversion. "
                "Without a metastable state, excited atoms would decay spontaneously back to the ground state almost instantaneously, preventing population accumulation."
            )
            paragraphs.append(
                "In a typical laser pumping cycle, atoms are optically or electrically excited from ground state $E_0$ to a high-energy pump band $E_3$. "
                "From $E_3$, atoms undergo rapid non-radiative relaxation (via crystal lattice phonon emission or molecular collisions) to the metastable state $E_2$ with picosecond time constants ($\\tau_{32} \\sim 10^{-11}\\text{ s}$). "
                "Because the subsequent decay from $E_2$ to $E_1$ is constrained by selection rules, atoms become trapped in $E_2$, allowing $N_2$ to grow until it surpasses lower state population $N_1$."
            )
            paragraphs.append(
                "The existence of a metastable level decouples the optical pump absorption process from the lasing transition. "
                "This ensures that strong pump flux can continuously feed the active medium without perturbing the coherence and monochromaticity of the stimulating laser field oscillating between $E_2$ and $E_1$."
            )
        else:
            paragraphs.append(
                "A metastable state is an excited atomic or molecular energy state that has an unusually long radiative lifetime compared to ordinary excited states. "
                "While ordinary excited electronic states decay through dipole-allowed transitions in $10^{-8}\\text{ s}$ to $10^{-7}\\text{ s}$, metastable states exhibit radiative lifetimes ranging from $10^{-4}\\text{ s}$ to several seconds or milliseconds."
            )
            paragraphs.append(
                "This extended lifetime occurs because direct electric dipole transitions ($E1$) from the metastable state to lower states are strictly forbidden by quantum mechanical selection rules. "
                "Transitions can only proceed through much weaker, higher-order multipole processes, such as magnetic dipole ($M1$) or electric quadrupole ($E2$) interactions, which have matrix elements several orders of magnitude smaller."
            )
            paragraphs.append(
                "Prominent examples of metastable states include the $2^2E$ level in $\\text{Cr}^{3+}$ ions in ruby lasers (lifetime $\\sim 3\\text{ ms}$), the $2^1S_0$ and $2^3S_1$ states in neutral helium (lifetimes of milliseconds to seconds), and the ${}^4F_{3/2}$ upper lasing level of $\\text{Nd}^{3+}$ in Nd:YAG crystals (lifetime $\\sim 230\\text{ }\\mu\\text{s}$)."
            )

    # Topic 7: Einstein Coefficients
    elif "einstein" in t_low:
        if "ratio" in s_low:
            paragraphs.append(
                "The ratio between Einstein's spontaneous emission coefficient $A_{21}$ and stimulated emission coefficient $B_{21}$ reveals the fundamental relationship between classical thermodynamics and quantum radiation theory. "
                "By equating the atomic transition rates in thermodynamic equilibrium with Planck's blackbody distribution law, Einstein derived this exact universal ratio."
            )
            paragraphs.append(
                "Equating upward and downward transition rates yields:\n\n"
                "$$N_1 B_{12} u(\\nu) = N_2 A_{21} + N_2 B_{21} u(\\nu)$$\n\n"
                "Substituting the Boltzmann ratio $N_1/N_2 = e^{h\\nu/k_BT}$ (for equal degeneracies $g_1=g_2$) and recognizing $B_{12} = B_{21}$ leads to:\n\n"
                "$$u(\\nu) = \\frac{A_{21}/B_{21}}{e^{h\\nu/k_BT} - 1}$$\n\n"
                "Comparing this directly with Planck's radiation formula $u(\\nu) = \\frac{8\\pi h\\nu^3}{c^3} \\frac{1}{e^{h\\nu/k_BT} - 1}$ establishes the celebrated Einstein relations:\n\n"
                "$$B_{12} = B_{21}, \\quad \\frac{A_{21}}{B_{21}} = \\frac{8\\pi h\\nu^3}{c^3}$$\n\n"
                "This proves that the ratio of spontaneous to stimulated emission scales cubically with radiation frequency ($\\propto \\nu^3$)."
            )
            paragraphs.append(
                "The cubic frequency dependence explains why constructing lasers in the ultraviolet, X-ray, and gamma-ray regimes requires enormously higher pump power densities than optical or microwave masers. "
                "Because spontaneous emission losses scale as $\\nu^3$, maintaining population inversion at high frequencies demands vast pump flux before spontaneous decay empties the upper state."
            )
        else:
            paragraphs.append(
                "In 1917, Albert Einstein introduced three phenomenological coefficients to describe the interaction between atomic energy states and an ambient electromagnetic radiation field: "
                "$A_{21}$ (spontaneous emission rate per atom), $B_{21}$ (stimulated emission probability per atom per unit radiation density), and $B_{12}$ (induced absorption probability per atom per unit radiation density)."
            )
            paragraphs.append(
                "Einstein's statistical formulation represented a major conceptual breakthrough by demonstrating that Planck's blackbody radiation law could be derived entirely from microscopic atomic transitions without invoking classical electromagnetic standing waves. "
                "Under thermal equilibrium, the principle of detailed balance mandates that the rate of upward transitions exactly balances the combined rate of downward transitions."
            )
            paragraphs.append(
                "Einstein's discovery of stimulated emission and the equality $B_{12} = B_{21}$ established the theoretical possibility of optical amplification. "
                "It revealed that photons do not act solely as independent particles, but participate in stimulated radiative processes that replicate identical quanta in a single field mode."
            )

    # Topic 8: Ruby Laser
    elif "ruby laser" in t_low or ("ruby" in t_low and "laser" in t_low):
        if "resonator" in s_low or "cavity" in s_low:
            paragraphs.append(
                "The optical resonator cavity in Theodore Maiman's original 1960 ruby laser was formed directly on the active ruby cylinder itself by grinding and polishing its flat end faces parallel to within fractions of an optical wavelength. "
                "One end face was coated with thick silver to achieve $100\\%$ reflection, while the opposing output end was coated with partial silver ($R \\approx 90\\%$) to permit laser beam out-coupling."
            )
            paragraphs.append(
                "In modern solid-state laser engineering, external dielectric mirrors with multi-layer quarter-wave interference coatings replace metallic coatings to minimize absorption losses. "
                "The resonator enforces standing-wave axial mode conditions $L = m(\\lambda / 2n)$, where $L$ is the physical cavity length, $n$ is the refractive index of ruby ($n \\approx 1.76$), and $m$ is an integer mode index ($m \\sim 10^5$). "
                "Longitudinal mode spacing is given by $\\Delta\\nu = c / (2nL)$, producing multiple discrete spectral frequencies within the atomic fluorescence linewidth."
            )
            paragraphs.append(
                "Because ruby exhibits thermal lensing under heavy flashlamp pumping, modern resonator designs employ slightly concave curved mirrors to maintain optical cavity stability and suppress higher-order transverse electromagnetic modes ($\text{TEM}_{mn}$), ensuring clean Gaussian fundamental $\\text{TEM}_{00}$ spatial output."
            )
        else:
            paragraphs.append(
                "The ruby laser is a solid-state three-level laser system. "
                "The active medium consists of a synthetic sapphire crystal (aluminum oxide, $\\text{Al}_2\\text{O}_3$) in which approximately $0.05\\%$ of the $\\text{Al}^{3+}$ lattice sites are substituted by trivalent chromium ions ($\\text{Cr}^{3+}$), imparting a pink-red color."
            )
            paragraphs.append(
                "The energy level scheme operates as follows: "
                "1. **Optical Pumping:** A helical xenon flashlamp emits intense broad-spectrum light, exciting $\\text{Cr}^{3+}$ ions from the ground state ${}^4A_2$ into broad green (${}^4T_2$) and violet (${}^4T_1$) absorption bands.\n"
                "2. **Fast Non-Radiative Relaxation:** Within picoseconds ($\\tau \\sim 10^{-11}\\text{ s}$), excited ions relax non-radiatively via phonon interactions down to the metastable ${}^2E$ state.\n"
                "3. **Lasing Transition:** The ${}^2E$ state has a long radiative lifetime of $\\tau \\approx 3\\text{ ms}$. Lasing occurs as ions undergo stimulated transitions from ${}^2E$ back to ground state ${}^4A_2$, emitting coherent deep-red radiation at $\\lambda = 694.3\\text{ nm}$."
            )
            paragraphs.append(
                "Because the lower lasing level is the ground state, more than half of all chromium ions must be pumped into the excited state before optical gain can overcome absorption. "
                "This high population threshold requires massive flashlamp electrical discharge energies, causing the ruby laser to operate typically in a pulsed mode with significant thermal dissipation."
            )

    # Topic 9: He-Ne Laser
    elif "he-ne" in t_low or "helium-neon" in t_low:
        if "energy transfer" in s_low or "resonant" in s_low:
            paragraphs.append(
                "The core excitation mechanism in the Helium-Neon laser relies on resonant collisional energy transfer between excited helium atoms and ground-state neon atoms. "
                "Helium gas and neon gas are mixed in an approximate ratio of $10:1$ at a low total pressure of a few torr within a sealed fused silica discharge tube."
            )
            paragraphs.append(
                "When a high-voltage DC electrical discharge is struck (typically $1-2\\text{ kV}$ with a operating current of $5-10\\text{ mA}$), energetic free electrons collide with ground-state helium atoms: $e^- + \\text{He}(1^1S) \\to \\text{He}^*(2^1S_0, 2^3S_1) + e^-$. "
                "The $2^1S_0$ ($20.61\\text{ eV}$) and $2^3S_1$ ($19.82\\text{ eV}$) levels in helium are metastable with millisecond lifetimes because radiative transitions to ground are dipole-forbidden."
            )
            paragraphs.append(
                "By remarkable atomic coincidence, the $2^1S_0$ and $2^3S_1$ levels in helium nearly perfectly match the $3s$ ($20.66\\text{ eV}$) and $2s$ ($19.78\\text{ eV}$) excited energy levels of neon (energy difference $< 0.05\\text{ eV}$). "
                "Inelastic collisions between metastable helium atoms and ground-state neon atoms transfer energy with near-unity probability: $\\text{He}^*(2^1S_0) + \\text{Ne} \\to \\text{He} + \\text{Ne}^*(3s_2) + \\Delta E$, selectively pumping neon atoms into the upper lasing levels."
            )
        else:
            paragraphs.append(
                "The Helium-Neon (He-Ne) laser, demonstrated by Ali Javan, William Bennett, and Donald Herriott in 1960, is a continuous-wave four-level gas laser. "
                "It produces continuous coherent light at the characteristic visible red wavelength of $\\lambda = 632.8\\text{ nm}$, as well as infrared wavelengths at $1.15\\text{ }\\mu\\text{m}$ and $3.39\\text{ }\\mu\\text{m}$."
            )
            paragraphs.append(
                "The lasing cycle operates across neon's electronic configuration: "
                "1. Neon atoms are pumped to the $3s$ manifold via resonant collisions with metastable helium.\n"
                "2. Stimulated emission occurs between the $3s_2$ upper level and the $2p_4$ lower level, emitting photons at $\\lambda = 632.8\\text{ nm}$.\n"
                "3. Neon atoms in the $2p_4$ level rapidly decay spontaneously to the lower $1s$ level within nanoseconds ($\\tau \\sim 10^{-8}\\text{ s}$), maintaining a completely empty lower lasing level ($N_1 \\approx 0$).\n"
                "4. Finally, neon atoms in the $1s$ metastable level de-excite back to ground through collisions with the tube's glass walls."
            )
            paragraphs.append(
                "Because He-Ne lasers operate on four-level atomic kinetics, the pumping threshold is extremely low, enabling stable, low-noise continuous-wave oscillation with narrow linewidths. "
                "This makes the He-Ne laser an enduring benchmark standard for optical alignment, interferometry, barcode scanning, and university physics laboratories worldwide."
            )

    # Topic 10: Semiconductor Diode Laser
    elif "semiconductor" in t_low or "diode laser" in t_low:
        if "threshold" in s_low or "current" in s_low:
            paragraphs.append(
                "Threshold current density $J_{th}$ is the minimum electrical current per unit junction area required to establish optical gain equal to total cavity loss in a semiconductor laser diode. "
                "Below threshold, the device behaves as an ordinary light-emitting diode (LED), radiating spontaneous incoherent light in all directions."
            )
            paragraphs.append(
                "Optical gain in the active junction layer increases approximately linearly with injected current density: $\\gamma(J) = g_0 (J - J_{nom})$, where $g_0$ is the differential gain coefficient and $J_{nom}$ is the transparency current density. "
                "Equating optical round-trip gain with cavity internal losses $\\alpha_i$ and mirror transmission losses $\\alpha_m = \\frac{1}{2L}\\ln\\left(\\frac{1}{R_1 R_2}\\right)$ gives the threshold condition:\n\n"
                "$$\\Gamma g_0 (J_{th} - J_{nom}) = \\alpha_i + \\frac{1}{2L}\\ln\\left(\\frac{1}{R_1 R_2}\\right)$$\n\n"
                "where $\\Gamma$ is the optical confinement factor quantifying the spatial overlap between the optical wave mode and the active layer."
            )
            paragraphs.append(
                "Solving for $J_{th}$ yields $J_{th} = J_{nom} + \\frac{1}{\\Gamma g_0}\\left[\\alpha_i + \\frac{1}{2L}\\ln\\left(\\frac{1}{R_1 R_2}\\right)\\right]$. "
                "In modern double-heterostructure and quantum well lasers, strong carrier confinement and optical waveguiding dramatically compress $J_{th}$ to a few hundred amperes per square centimeter, permitting reliable room-temperature continuous-wave operation with milliwatt to watt output powers."
            )
        else:
            paragraphs.append(
                "The semiconductor diode laser (injection laser diode) is an optoelectronic device that generates coherent light directly from electrical current. "
                "It consists of a heavily doped p-n junction fabricated from direct bandgap compound semiconductors such as gallium arsenide (GaAs, emitting at $\\sim 840\\text{ nm}$) or indium gallium arsenide phosphide (InGaAsP, emitting at $1.3-1.55\\text{ }\\mu\\text{m}$)."
            )
            paragraphs.append(
                "Under strong forward bias, large densities of electrons from the n-side conduction band and holes from the p-side valence band are injected into the active depletion layer. "
                "When the quasi-Fermi level separation exceeds the semiconductor bandgap ($E_{Fc} - E_{Fv} > E_g$, known as the Bernard-Duraffourg condition), population inversion of free carriers is achieved. "
                "Electrons and holes recombine radiatively across the bandgap, emitting coherent photons with frequency $h\\nu \\approx E_g$."
            )
            paragraphs.append(
                "Optical feedback is provided naturally by the cleaved semiconductor facet crystal planes, which have a high Fresnel reflectance ($R \\approx 30\\%$) due to the high refractive index of semiconductors ($n \\approx 3.6$). "
                "Due to their microscopic footprint, high electrical-to-optical power conversion efficiency ($> 50\\%$), and direct electrical modulation capability, semiconductor diode lasers form the indispensable physical foundation of modern fiber-optic communications, optical discs, and lidar systems."
            )

    # Topic 11: Industrial and Medical Applications
    elif "application" in t_low or "industrial" in t_low or "medical" in t_low:
        if "communication" in s_low or "fiber" in s_low:
            paragraphs.append(
                "In modern optical telecommunications, semiconductor lasers serve as the primary optical transmitters feeding high-speed global fiber-optic networks. "
                "Distributed Feedback (DFB) lasers and Vertical-Cavity Surface-Emitting Lasers (VCSELs) provide single-longitudinal-mode emission with sub-megahertz linewidths, operating at standard infrared telecommunication windows ($1310\\text{ nm}$ zero-dispersion window and $1550\\text{ nm}$ minimum-attenuation window)."
            )
            paragraphs.append(
                "Direct current modulation or external electro-optic Mach-Zehnder modulators impress digital data streams onto the optical carrier at rates exceeding $100\\text{ Gbps}$ per wavelength channel. "
                "Wavelength Division Multiplexing (WDM) combines dozens of distinct laser wavelengths into a single glass fiber, enabling terabit-per-second aggregate data bandwidths across transoceanic submarine cable systems."
            )
            paragraphs.append(
                "Furthermore, Erbium-Doped Fiber Amplifiers (EDFAs) optically amplify these telecommunication signals using $980\\text{ nm}$ or $1480\\text{ nm}$ semiconductor pump lasers directly in the optical domain without electronic regeneration, revolutionizing global internet connectivity and cloud computing architectures. By eliminating the need for expensive electronic transponders at intermediate repeater huts, optical amplification enables all-optical long-haul networks spanning thousands of kilometers."
            )
        else:
            paragraphs.append(
                "In industrial manufacturing, high-power lasers—including continuous-wave and pulsed fiber lasers, disk lasers, and $\\text{CO}_2$ gas lasers delivering powers from hundreds of watts to tens of kilowatts—have transformed precision materials processing. "
                "Laser beams can be tightly focused to spot sizes under $100\\text{ }\\mu\\text{m}$, generating immense localized power densities exceeding $10^7\\text{ W/cm}^2$."
            )
            paragraphs.append(
                "These extreme power densities enable rapid, narrow-kerf cutting of thick steel, titanium, and aluminum alloys, as well as deep-penetration keyhole welding with minimal heat-affected zones. "
                "Ultrafast picosecond and femtosecond lasers enable 'cold ablation' precision micromachining of brittle semiconductors, ceramics, and polymers without thermal cracking or material slag."
            )
            paragraphs.append(
                "In medical and surgical applications, lasers offer bloodless surgical incision and selective photothermolysis: "
                "Argon lasers photocoagulate ruptured retinal blood vessels in diabetic retinopathy; excimer lasers ($193\\text{ nm}$) ablate corneal tissue with sub-micron accuracy in LASIK vision correction; and pulsed Nd:YAG or Holmium lasers pulverize kidney stones through endoscopic lithotripsy, maximizing therapeutic precision while minimizing patient trauma. In laser welding and additive manufacturing (selective laser melting), localized thermal energy delivers high-strength metallurgical joins with minimal thermal distortion and negligible residual mechanical stress."
            )

    # Fallback / General Lasers
    else:
        paragraphs.append(
            f"Laser physics represents an essential cornerstone of modern engineering optics and quantum electronics. "
            f"In the analysis of {topic}, examining {subtopic} establishes the fundamental mechanisms of coherent stimulated emission, population inversion dynamics, and optical cavity feedback."
        )
        paragraphs.append(
            "Laser systems uniquely combine quantum state transitions with electromagnetic wave optics. "
            "Rigorous analysis of transition cross-sections, pumping efficiencies, and resonator losses dictates the achievable optical gain, threshold conditions, and output beam characteristics."
        )
        paragraphs.append(
            "From precision spectroscopy and manufacturing to telecommunications and medical diagnostics, the principles governing laser operation provide the foundational framework for modern photonic technology."
        )

    return paragraphs



def generate_fiber_optics_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Fiber Optics topics with rigorous pedagogical depth."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    # Topic 1: Introduction to Optical Fiber
    if "intro" in t_low:
        if "guidance" in s_low or "principle" in s_low:
            paragraphs.append(
                "The guidance of electromagnetic energy through dielectric waveguides is governed by Maxwell's equations subject to cylindrical boundary conditions. "
                "An optical fiber guides optical wave modes along its longitudinal axis through total internal reflection occurring at the cylindrical interface between an inner glass core and an outer cladding."
            )
            paragraphs.append(
                "Because the core refractive index $n_1$ exceeds the cladding refractive index $n_2$ ($n_1 > n_2$), optical rays incident upon the core-cladding interface at angles greater than the critical angle $\\phi_c = \\arcsin(n_2/n_1)$ suffer total internal reflection with zero refractive energy leakage. "
                "Maxwell's boundary conditions mandate that the electric and magnetic field amplitudes decay exponentially into the lower-index cladding as an evanescent wave: $E(r) \\propto e^{-\\gamma (r - a)}$ for radial distances $r > a$, where $a$ is the core radius."
            )
            paragraphs.append(
                "This evanescent wave phenomenon requires that the cladding layer possess a thickness of at least several optical wavelengths. "
                "Adequate cladding thickness shields the guided wave packet from environmental surface contaminants, mechanical microbending, and ambient absorption, ensuring low-loss optical propagation over transcontinental distances."
            )
        else:
            paragraphs.append(
                "Optical fibers are cylindrical dielectric waveguides fabricated from ultra-pure silica glass ($\text{SiO}_2$) designed to transmit optical signals over vast distances with minimal attenuation and immense bandwidth. "
                "The foundational operating principle rests upon total internal reflection, first demonstrated in water streams by Daniel Colladon and Jacques Babinet in the 1840s, and pioneered for telecommunications by Charles Kao and George Hockham in 1966."
            )
            paragraphs.append(
                "When a ray of light propagating in an optically dense medium of refractive index $n_1$ encounters a boundary with an optically rarer medium of refractive index $n_2$ ($n_1 > n_2$), Snell's law governs refraction: $n_1 \\sin\\phi_1 = n_2 \\sin\\phi_2$. "
                "As the angle of incidence $\\phi_1$ increases, the refracted angle $\\phi_2$ approaches $90^\\circ$. The critical angle $\\phi_c$ is reached when the refracted ray travels parallel to the interface:\n\n"
                "$$\\phi_c = \\arcsin\\left(\\frac{n_2}{n_1}\\right)$$\n\n"
                "For any angle of incidence exceeding the critical angle ($\\phi_1 > \\phi_c$), no light enters the second medium as a propagating wave; instead, $100\\%$ of the incident optical power is reflected back into the dense medium."
            )
            paragraphs.append(
                "Unlike metallic coaxial cables that experience severe skin-effect losses at radio and microwave frequencies, dielectric optical waveguides transmit terahertz optical carriers with negligible resistive dissipation. "
                "Furthermore, optical fibers are completely immune to electromagnetic interference (EMI), radio-frequency interference (RFI), and ground-loop electrical hazards."
            )

    # Topic 2: Optical Fiber Structure
    elif "structure" in t_low or ("core" in t_low and "cladding" in t_low):
        if "profile" in s_low or "refractive" in s_low:
            paragraphs.append(
                "The refractive index profile $n(r)$ describes the variation of refractive index as a function of radial distance $r$ from the central fiber axis. "
                "In fiber optic engineering, the radial profile governs the propagation velocity of different optical modes and determines whether a waveguide experiences severe modal dispersion."
            )
            paragraphs.append(
                "Refractive index profiles are mathematically classified using the power-law parameter $\\alpha$:\n\n"
                "$$n(r) = \\begin{cases} n_1 \\left[1 - 2\\Delta \\left(\\frac{r}{a}\\right)^\\alpha \\right]^{1/2} & \\text{for } r \\le a \\\\[8pt] n_2 = n_1 (1 - 2\\Delta)^{1/2} & \\text{for } r > a \\end{cases}$$\n\n"
                "where $a$ is the core radius and $\\Delta = \\frac{n_1^2 - n_2^2}{2n_1^2} \\approx \\frac{n_1 - n_2}{n_1}$ represents the relative fractional index difference. When $\\alpha \\to \\infty$, the profile represents a step-index fiber; when $\\alpha = 2$, it represents an optimal parabolic graded-index fiber."
            )
            paragraphs.append(
                "Controlled chemical vapor deposition processes—such as Modified Chemical Vapor Deposition (MCVD) or Outside Vapor Deposition (OVD)—dope silica with germanium dioxide ($\\text{GeO}_2$) or phosphorus pentoxide ($\\text{P}_2\\text{O}_5$) to elevate $n_1$, or with fluorine or boron to depress $n_2$, engineering profile accuracy down to nanometer radial precision."
            )
        else:
            paragraphs.append(
                "A standard communication-grade optical fiber possesses a concentric cylindrical three-layer geometry: "
                "1. **Core:** The central cylindrical dielectric region of radius $a$ and high refractive index $n_1$ through which optical power propagates.\n"
                "2. **Cladding:** An outer dielectric sheath of radius $b$ and lower refractive index $n_2$ that bounds the optical field and establishes total internal reflection.\n"
                "3. **Protective Buffer Coating:** A tough primary polymeric coating (such as UV-cured acrylate) of diameter $\\sim 250\\text{ }\\mu\\text{m}$ providing mechanical flexibility, abrasion resistance, and moisture protection."
            )
            paragraphs.append(
                "Standard telecommunication fibers maintain an industry-standard outer cladding diameter of $2b = 125\\text{ }\\mu\\text{m}$. "
                "In single-mode fibers, the central core diameter is made extremely small ($2a \\approx 8-10\\text{ }\\mu\\text{m}$) to permit only the fundamental $\\text{HE}_{11}$ mode to propagate. "
                "In multi-mode fibers, the core diameter is substantially larger ($2a = 50\\text{ }\\mu\\text{m}$ or $62.5\\text{ }\\mu\\text{m}$), supporting hundreds of propagating spatial modes."
            )
            paragraphs.append(
                "The core-cladding boundary must maintain atomic smoothness to minimize optical scattering losses. "
                "Any surface irregularities or radial micro-deviations at the boundary scatter guided photons into lossy radiation modes, increasing transmission attenuation."
            )

    # Topic 3: Acceptance Angle and Numerical Aperture
    elif "acceptance angle" in t_low or "numerical aperture" in t_low:
        if "numerical aperture" in s_low or "derivation" in s_low:
            paragraphs.append(
                "Numerical Aperture (NA) is a dimensionless optical figure of merit that characterizes the light-gathering capacity of an optical fiber. "
                "To derive NA, consider a meridional light ray entering the flat input face of a fiber from an external medium of refractive index $n_0$ (typically air, $n_0 \\approx 1.0$) at an incident angle $\\theta_0$."
            )
            paragraphs.append(
                "Applying Snell's law at the entrance face yields: $n_0 \\sin\\theta_0 = n_1 \\sin\\theta_r = n_1 \\cos\\phi$, where $\\phi = 90^\\circ - \\theta_r$ is the angle of incidence at the core-cladding interface. "
                "For the ray to be guided by total internal reflection along the core, $\\phi$ must equal or exceed the critical angle $\\phi_c$, which requires $\\sin\\phi \\ge \\sin\\phi_c = n_2 / n_1$. "
                "Substituting $\\cos\\phi = \\sqrt{1 - \\sin^2\\phi} \\le \\sqrt{1 - (n_2/n_1)^2}$ yields the maximum entrance acceptance angle $\\theta_a$:\n\n"
                "$$n_0 \\sin\\theta_a = n_1 \\sqrt{1 - \\frac{n_2^2}{n_1^2}} = \\sqrt{n_1^2 - n_2^2}$$\n\n"
                "In air ($n_0 = 1$), the Numerical Aperture is defined identically as:\n\n"
                "$$\\text{NA} = \\sin\\theta_a = \\sqrt{n_1^2 - n_2^2} = n_1 \\sqrt{2\\Delta}$$\n\n"
                "where $\\Delta = (n_1 - n_2) / n_1$ is the relative refractive index difference."
            )
            paragraphs.append(
                "The numerical aperture dictates the coupling efficiency between external optical sources (such as LEDs or semiconductor laser diodes) and the fiber core. "
                "While a large NA enhances optical capture from divergent LEDs, it increases modal dispersion by expanding the range of allowable ray propagation angles, demanding an engineering trade-off between power coupling and transmission bandwidth."
            )
        else:
            paragraphs.append(
                "The acceptance angle $\\theta_a$ defines the maximum half-angle of the spatial acceptance cone entering the fiber face within which incident light rays are captured and guided by total internal reflection. "
                "Any light ray launched outside this conical boundary strikes the core-cladding interface at an angle less than the critical angle $\\phi_c$, refracting into the cladding where it is absorbed or lost to radiation."
            )
            paragraphs.append(
                "The geometry of the acceptance cone forms a three-dimensional solid acceptance angle $\\Omega = \\pi \\sin^2\\theta_a = \\pi (\\text{NA})^2$. "
                "For a typical communication fiber with $n_1 = 1.48$ and $n_2 = 1.46$, $\\text{NA} \\approx \\sqrt{(1.48)^2 - (1.46)^2} \\approx 0.24$, corresponding to an acceptance half-angle in air of $\\theta_a = \\arcsin(0.24) \\approx 14^\\circ$."
            )
            paragraphs.append(
                "Light launched inside this acceptance cone forms propagating bound modes, while skew rays—rays that do not intersect the fiber axis—propagate in helical paths around the core. "
                "Precision optical connectors and lens systems are designed to match numerical apertures between transmitter sources and fiber cores to minimize insertion loss."
            )

    # Topic 4: Step-Index and Graded-Index Fibers
    elif "step-index and graded-index" in t_low or ("step-index" in t_low and "graded-index" in t_low):
        if "graded-index" in s_low or "modal dispersion" in s_low:
            paragraphs.append(
                "Graded-Index (GRIN) fibers were engineered specifically to overcome the severe intermodal dispersion that limits the bandwidth of step-index multi-mode fibers. "
                "In a GRIN fiber, the refractive index decreases smoothly and continuously from a maximum value $n_1$ on the central axis to $n_2$ at the core-cladding boundary."
            )
            paragraphs.append(
                "Because optical phase velocity is inversely proportional to refractive index ($v = c / n(r)$), light rays that travel off-axis follow curved, sinusoidal trajectories into lower-index peripheral regions where they propagate at higher speeds. "
                "Although off-axis higher-order modes travel longer physical path lengths, their higher average velocity compensates for the distance, allowing all spatial modes to arrive at the fiber terminus at nearly the exact same time."
            )
            paragraphs.append(
                "When the profile parameter is tuned to the optimal parabolic value $\\alpha = 2(1 - \\Delta)$, intermodal pulse broadening collapses from $\\Delta t \\approx \\frac{L n_1}{c}\\Delta$ (in step-index) down to $\\Delta t \\approx \\frac{L n_1}{2c}\\Delta^2$. "
                "Because $\\Delta \\approx 0.01$, this quadratic reduction suppresses modal dispersion by a factor of hundreds, elevating multi-mode fiber bandwidth-distance products from $20\\text{ MHz}\\cdot\\text{km}$ to over $2\\text{ GHz}\\cdot\\text{km}$."
            )
        else:
            paragraphs.append(
                "Step-index fibers feature a uniform, constant refractive index $n_1$ throughout the entire core, with an abrupt step discontinuity at the core-cladding boundary down to cladding index $n_2$. "
                "Light rays inside a step-index fiber travel along straight-line zig-zag paths, reflecting specularly from the boundary."
            )
            paragraphs.append(
                "In a step-index multi-mode fiber, the axial ray travels the shortest path length $L$ along the fiber axis in transit time $t_{min} = L / v = L n_1 / c$. "
                "In contrast, the most oblique ray propagating at the critical angle $\\phi_c$ travels a longer path length $L / \\sin\\phi_c = L n_1 / n_2$, requiring transit time $t_{max} = L n_1^2 / (c n_2)$. "
                "The resulting intermodal time delay difference per unit length is formulated as:\n\n"
                "$$\\Delta t_{step} = t_{max} - t_{min} = \\frac{L n_1}{c} \\left( \\frac{n_1 - n_2}{n_2} \\right) \\approx \\frac{L n_1}{c} \\Delta$$\n\n"
                "For typical silica fiber parameters, this intermodal delay is approximately $50\\text{ ns/km}$, causing severe digital pulse broadening that restricts data rates over kilometer spans."
            )
            paragraphs.append(
                "Despite their bandwidth limitations, step-index multi-mode fibers remain popular for short-distance illumination, industrial process sensors, and low-cost local networks because their large core diameters ($200-1000\\text{ }\\mu\\text{m}$) enable simple connectorization and high power-handling capacity."
            )

    # Topic 5: Single Mode and Multi Mode Fibers
    elif "single mode and multi mode" in t_low or ("single mode" in t_low and "multi mode" in t_low):
        if "cutoff" in s_low:
            paragraphs.append(
                "The cutoff wavelength $\\lambda_c$ is the minimum operating wavelength below which an optical fiber ceases to be single-mode and begins to support higher-order spatial modes (such as $\\text{TE}_{01}, \\text{TM}_{01}, \\text{HE}_{21}$). "
                "For wavelengths longer than $\\lambda_c$ ($\\lambda > \\lambda_c$), only the fundamental $\\text{HE}_{11}$ (or $\\text{LP}_{01}$) spatial mode can propagate."
            )
            paragraphs.append(
                "The cutoff condition occurs precisely when the normalized frequency parameter $V$ equals the first zero of the Bessel function boundary condition, $V_c = 2.40483$. "
                "Setting $V = 2.405$ in the normalized frequency formula yields the analytical expression for cutoff wavelength:\n\n"
                "$$\\lambda_c = \\frac{2\\pi a}{2.405} \\text{NA} = \\frac{2\\pi a}{2.405} \\sqrt{n_1^2 - n_2^2}$$\n\n"
                "For wavelengths shorter than $\\lambda_c$, higher-order modes propagate, introducing modal noise and intermodal dispersion."
            )
            paragraphs.append(
                "In commercial single-mode telecommunication fibers (such as ITU-T G.652 standard fiber), the cable cutoff wavelength is engineered to fall between $1180\\text{ nm}$ and $1260\\text{ nm}$. "
                "This ensures strictly single-mode operation across the primary optical transmission bands: the O-band ($1260-1360\\text{ nm}$) and C-band ($1530-1565\\text{ nm}$)."
            )
        else:
            paragraphs.append(
                "The normalized frequency parameter $V$ (commonly called the $V$-number) is a fundamental dimensionless quantity that governs the modal properties of an optical fiber. "
                "It combines the physical core radius $a$, operating wavelength $\\lambda$, and refractive indices into a single parameter:\n\n"
                "$$V = \\frac{2\\pi a}{\\lambda} \\sqrt{n_1^2 - n_2^2} = \\frac{2\\pi a}{\\lambda} \\text{NA}$$\n\n"
                "The value of $V$ dictates the total number of bound spatial electromagnetic modes supported by the fiber."
            )
            paragraphs.append(
                "For a step-index fiber, the total number of guided modes $M$ when $V \\gg 1$ is approximated as $M \\approx V^2 / 2$, whereas for a graded-index parabolic fiber, $M \\approx V^2 / 4$. "
                "Single-mode guidance occurs when $V < 2.405$. Under this condition, all higher-order modes are cut off, and only the two orthogonal polarizations of the fundamental $\\text{LP}_{01}$ mode propagate."
            )
            paragraphs.append(
                "Multi-mode fibers operate with large $V$-numbers ($V > 20$), propagating hundreds of distinct transverse modes. "
                "While multi-mode fibers simplify optical coupling from inexpensive LEDs, single-mode fibers ($V < 2.405$) eliminate intermodal dispersion entirely, making single-mode glass fiber the universal choice for long-haul and high-bandwidth telecommunications."
            )

    # Topic 6: Fiber Attenuation
    elif "attenuation" in t_low:
        if "rayleigh" in s_low or "scattering" in s_low:
            paragraphs.append(
                "Rayleigh scattering represents the intrinsic, unavoidable physical lower limit of attenuation in optical silica fibers. "
                "It arises from microscopic, sub-wavelength thermodynamic density fluctuations frozen into the amorphous glass matrix during cooling from the molten state at temperatures near the glass transition temperature ($T_g \\sim 1400\\text{ K}$)."
            )
            paragraphs.append(
                "These frozen density variations create localized refractive index fluctuations that scatter propagating electromagnetic waves isotropically into radiation modes. "
                "Rayleigh scattering loss $\\alpha_R$ exhibits a powerful inverse fourth-power dependence on optical wavelength:\n\n"
                "$$\\alpha_R \\propto \\frac{1}{\\lambda^4}$$\n\n"
                "The Rayleigh scattering attenuation coefficient is formulated as $\\alpha_R = \\frac{8\\pi^3}{3\\lambda^4} (n^8 p^2) k_B T_f \\beta_T$, where $p$ is the photoelastic coefficient and $\\beta_T$ is isothermal compressibility."
            )
            paragraphs.append(
                "Because Rayleigh scattering decreases drastically as wavelength increases, attenuation drops from $\\sim 2.5\\text{ dB/km}$ at $850\\text{ nm}$ down to $\\sim 0.16\\text{ dB/km}$ at $1550\\text{ nm}$. "
                "This $\\lambda^{-4}$ relationship explains why long-haul telecommunication systems operate predominantly in the infrared C-band ($1550\\text{ nm}$), where silica glass reaches its fundamental transparency maximum."
            )
        else:
            paragraphs.append(
                "Attenuation in optical fibers quantifies the reduction of optical signal power as light propagates through the waveguide. "
                "It is expressed logarithmically in decibels per kilometer ($\\text{dB/km}$) as:\n\n"
                "$$\\alpha = \\frac{10}{L} \\log_{10}\\left(\\frac{P_{in}}{P_{out}}\\right)$$\n\n"
                "where $P_{in}$ is optical power launched into the fiber, $P_{out}$ is transmitted power exiting after distance $L$ kilometers."
            )
            paragraphs.append(
                "Fiber attenuation originates from three principal loss mechanisms: "
                "1. **Material Absorption:** Both intrinsic electronic bandgap absorption in the ultraviolet and multiphonon vibrational absorption in the far-infrared ($> 1.6\\text{ }\\mu\\text{m}$), plus extrinsic absorption caused by transition metal impurities ($\text{Fe}^{2+}, \text{Cu}^{2+}$) and hydroxyl ($\text{OH}^-$) ions.\n"
                "2. **Linear Scattering:** Predominantly Rayleigh scattering from thermodynamic density fluctuations.\n"
                "3. **Geometric Bending Losses:** Radiation losses caused by macroscopic bends (macrobending) or microscopic local axis deviations (microbending) that force guided modes past the critical angle."
            )
            paragraphs.append(
                "Hydroxyl ion ($\text{OH}^-$) contamination causes strong absorption resonance peaks near $950\\text{ nm}, 1240\\text{ nm}$, and $1383\\text{ nm}$ (the 'water peak'). "
                "Modern chemical dehydration techniques reduce $\text{OH}^-$ impurity concentrations below one part per billion, producing 'zero water peak' (ZWP) fibers (ITU-T G.652.D) that open the entire optical spectrum from $1260\\text{ nm}$ to $1625\\text{ nm}$ for data transmission."
            )

    # Topic 7: Intermodal Dispersion
    elif "intermodal dispersion" in t_low or ("dispersion" in t_low and "intermodal" in t_low):
        if "material dispersion" in s_low or "chromatic" in s_low:
            paragraphs.append(
                "Material dispersion is an intrinsic chromatic dispersion mechanism arising from the nonlinear dependence of the glass refractive index $n(\\lambda)$ on optical wavelength. "
                "Because different spectral components of an optical pulse travel at different group velocities $v_g = c / n_g$, finite optical source linewidths cause temporal pulse spreading."
            )
            paragraphs.append(
                "The group index $n_g$ is defined as $n_g = n - \\lambda \\frac{dn}{d\\lambda}$. The material dispersion parameter $D_{mat}$ is formulated as:\n\n"
                "$$D_{mat} = -\\frac{\\lambda}{c} \\frac{d^2 n}{d\\lambda^2}$$\n\n"
                "expressed in picoseconds per nanometer-kilometer ($\\text{ps}/(\\text{nm}\\cdot\\text{km})$). "
                "For pure silica glass, the second derivative $\\frac{d^2 n}{d\\lambda^2}$ passes through zero at the material zero-dispersion wavelength $\\lambda_{ZD} \\approx 1270\\text{ nm}$."
            )
            paragraphs.append(
                "Combining material dispersion with waveguide dispersion yields the total chromatic dispersion $D = D_{mat} + D_{wg}$. "
                "By engineering core-cladding index profiles, dispersion-shifted fibers (ITU-T G.653) shift the zero-dispersion wavelength to $1550\\text{ nm}$ to coincide with the minimum attenuation window, maximizing transmission distance without electronic repeaters."
            )
        else:
            paragraphs.append(
                "Dispersion in optical fibers is the physical phenomenon where an optical pulse broadens temporally as it propagates along the fiber length. "
                "Pulse broadening causes adjacent digital pulses to overlap—a degradation known as Inter-Symbol Interference (ISI)—which degrades bit-error rates and imposes an upper limit on transmission bit rates."
            )
            paragraphs.append(
                "Intermodal (modal) dispersion occurs exclusively in multi-mode fibers, where different transverse spatial modes travel along paths with different group velocities. "
                "In a step-index multi-mode fiber of length $L$, the total time delay spread between the fastest (axial) mode and slowest (critical angle) mode is:\n\n"
                "$$\\Delta t_{modal} \\approx \\frac{L n_1}{c} \\Delta$$\n\n"
                "For a fiber with $n_1 = 1.48$ and $\\Delta = 0.01$, modal dispersion broadens pulses by $\\sim 50\\text{ ns}$ per kilometer, capping the maximum data rate at roughly $10\\text{ Mbps}$ over $1\\text{ km}$."
            )
            paragraphs.append(
                "Because single-mode fibers permit only the fundamental $\\text{LP}_{01}$ mode to propagate, intermodal dispersion is identically zero ($D_{modal} = 0$). "
                "Consequently, the information carrying capacity of single-mode systems is bounded only by chromatic dispersion and polarization mode dispersion, enabling data rates exceeding $400\\text{ Gbps}$ per wavelength."
            )

    # Topic 8: Optical Fiber Communications
    elif "communications" in t_low or ("fiber" in t_low and "transmitter" in t_low) or ("fiber" in t_low and "receiver" in t_low):
        if "receiver" in s_low or "photodetector" in s_low:
            paragraphs.append(
                "The optical receiver subsystem converts attenuated optical signal pulses emerging from the fiber back into electrical bit streams with maximum signal-to-noise ratio (SNR). "
                "The central optoelectronic component is a semiconductor photodetector—either a PIN photodiode or an Avalanche Photodiode (APD)."
            )
            paragraphs.append(
                "Photodetectors operate via the internal photoelectric effect, where absorbed incident photons generate electron-hole pairs across a reverse-biased depletion region. "
                "Key performance metrics include responsivity $\\mathcal{R} = \\frac{\\eta q}{h\\nu}$ (in A/W, where $\\eta$ is quantum efficiency), response bandwidth, and dark current. "
                "In an APD, high reverse bias induces internal avalanche multiplication of carriers via impact ionization, providing internal photocurrent gain ($M = 10-100$) that boosts receiver sensitivity for long-haul detection."
            )
            paragraphs.append(
                "Following photodetection, a Transimpedance Amplifier (TIA) converts the microscopic photocurrent into a stable voltage, followed by a linear equalizer, clock and data recovery (CDR) circuitry, and decision threshold comparators that reconstruct the clean digital bit stream. Receiver performance is verified experimentally using eye diagram pattern analysis, measuring eye opening height and jitter width to guarantee bit-error-rates better than $10^{-12}$ under high data traffic."
            )
        else:
            paragraphs.append(
                "The optical transmitter subsystem generates, modulates, and launches optical carrier signals into the fiber waveguide. "
                "The primary optical sources are Light Emitting Diodes (LEDs) and Semiconductor Laser Diodes (LDs), operating in the infrared transmission windows."
            )
            paragraphs.append(
                "LEDs provide incoherent, broad-spectrum light (spectral width $\\Delta\\lambda \\sim 30-50\\text{ nm}$) with modest optical powers (sub-milliwatt), making them suitable for low-cost, short-range local networks. "
                "In contrast, laser diodes—such as Distributed Feedback (DFB) lasers—provide highly coherent, narrow-linewidth emission ($\\Delta\\lambda < 0.1\\text{ nm}$) with high output powers ($10-100\\text{ mW}$) and gigahertz modulation bandwidths."
            )
            paragraphs.append(
                "Modern optical communication systems employ advanced modulation formats, such as Quadrature Phase Shift Keying (QPSK) and 16-QAM combined with coherent optical detection. "
                "Coherent receivers mix the incoming signal with a local oscillator laser, enabling detection of both optical amplitude and phase to transmit data at hundreds of gigabits per second per wavelength. Optical transmitters employ distributed feedback (DFB) grating structures that suppress side-mode emission, ensuring high side-mode suppression ratios (SMSR $> 40\text{ dB}$) and preventing dynamic wavelength chirp during modulation."
            )

    # Topic 9: Fiber Optic Sensors
    elif "sensor" in t_low:
        if "extrinsic" in s_low:
            paragraphs.append(
                "Extrinsic (or hybrid) fiber optic sensors use the optical fiber strictly as an unperturbed transmission channel to guide light to and from an external sensing transducer region. "
                "The physical parameter being measured alters the light beam outside the fiber core before light is re-coupled into a collection fiber."
            )
            paragraphs.append(
                "Common extrinsic sensor designs include optical pyrometers, reflection-based displacement sensors, and photoelastic pressure cells. "
                "For example, in a fiber optic reflection sensor, light launched from an emitter fiber reflects from a moving diaphragm onto an adjacent receiver fiber; displacement changes modulate the received optical intensity, measuring pressure or vibration."
            )
            paragraphs.append(
                "Extrinsic sensors offer high geometric versatility, enabling remote measurements inside harsh, high-temperature, or chemically corrosive environments where electronic transducers would fail. "
                "Because sensing occurs externally, standard low-cost silica or polymer fibers can be used without specialty dopants."
            )
        else:
            paragraphs.append(
                "Intrinsic fiber optic sensors use the optical fiber itself as the active sensing transducer. "
                "An external physical stimulus—such as temperature, strain, pressure, or acoustic waves—directly perturbs the optical wave propagating inside the core by modifying its intensity, phase, polarization, or wavelength."
            )
            paragraphs.append(
                "A premier class of intrinsic sensors is the Fiber Bragg Grating (FBG), formed by inducing a permanent periodic modulation of the core refractive index with ultraviolet interference patterns. "
                "An FBG reflects a narrow spectral peak at the Bragg wavelength $\\lambda_B = 2 n_{eff} \\Lambda$, where $\\Lambda$ is the grating period. "
                "Applied mechanical strain $\\epsilon$ or temperature change $\\Delta T$ alters both $n_{eff}$ and $\\Lambda$, shifting the reflected wavelength according to $\\frac{\\Delta\\lambda_B}{\\lambda_B} = (1 - p_e)\\epsilon + (\\alpha_T + \\xi)\\Delta T$."
            )
            paragraphs.append(
                "Intrinsic fiber sensors are widely embedded into aircraft wings, bridges, dams, and oil pipelines for structural health monitoring. "
                "Furthermore, distributed optical sensing techniques—such as Optical Time-Domain Reflectometry (OTDR) based on Raman and Brillouin scattering—allow continuous temperature and strain mapping along fiber spans exceeding $100\\text{ km}$."
            )

    # Topic 10: Fiber Fabrication and Splicing
    elif "fabrication" in t_low or "splicing" in t_low:
        if "splicing" in s_low or "fusion" in s_low:
            paragraphs.append(
                "Fiber splicing is the permanent physical joining of two optical fiber ends to establish a continuous optical waveguide with minimum insertion loss and negligible back-reflection. "
                "The dominant technique in telecommunication engineering is fusion splicing."
            )
            paragraphs.append(
                "The fusion splicing process involves four critical procedural steps: "
                "1. **Stripping and Cleaning:** Removing the protective buffer coating and wiping the bare cladding with high-purity isopropyl alcohol.\n"
                "2. **Precision Cleaving:** Scoring and pulling the fiber using a diamond or tungsten carbide blade to produce a mirror-smooth end face with cleave angles $< 1^\\circ$.\n"
                "3. **Core Alignment:** Automated microscopic alignment using Local Injection and Detection (LID) or Profile Alignment Systems (PAS) to align fiber cores to within sub-micron tolerances.\n"
                "4. **Electric Arc Fusion:** Generating a controlled high-voltage AC electric arc between tungsten electrodes to melt and fuse the glass fiber tips together."
            )
            paragraphs.append(
                "Modern automated fusion splicers achieve splice losses under $0.02\\text{ dB}$ for single-mode fibers, with mechanical tensile strength exceeding $100\\text{ kpsi}$. "
                "Mechanical splices, which align fibers in precision V-grooves using index-matching gel, provide a portable alternative for emergency repairs, albeit with slightly higher insertion losses ($0.1-0.2\\text{ dB}$)."
            )
        else:
            paragraphs.append(
                "Fabrication of ultra-low-loss telecommunication optical fibers requires two distinct manufacturing stages: preform fabrication and fiber drawing. "
                "A preform is a large, high-purity glass rod (typically $1-2\\text{ meters}$ long and $2-5\\text{ cm}$ in diameter) that embodies the precise core-cladding geometry and refractive index profile of the desired fiber on an expanded macroscopic scale."
            )
            paragraphs.append(
                "Preforms are fabricated through Chemical Vapor Deposition (CVD) processes, such as Modified Chemical Vapor Deposition (MCVD), Outside Vapor Deposition (OVD), or Vapor Axial Deposition (VAD). "
                "High-purity gaseous reagents—silicon tetrachloride ($\\text{SiCl}_4$), germanium tetrachloride ($\\text{GeCl}_4$), and oxygen—react at high temperatures ($> 1600^\\circ\\text{C}$) to form fine silica soot: $\\text{SiCl}_4 + \\text{O}_2 \\to \\text{SiO}_2 + 2\\text{Cl}_2$. "
                "The soot deposits in concentric layers inside or upon a silica substrate tube and is sintered into bubble-free vitreous glass."
            )
            paragraphs.append(
                "During fiber drawing, the preform is mounted at the top of a multi-story drawing tower and lowered into a high-temperature graphite furnace ($2000-2200^\\circ\\text{C}$). "
                "The softened glass tip draws down under gravity into a thin fiber filament. Laser micrometers monitor diameter in a high-speed feedback loop to hold the $125\\text{ }\\mu\\text{m}$ diameter to within $\\pm 0.5\\text{ }\\mu\\text{m}$, while polymer buffer coatings are applied and UV-cured before spooling."
            )

    # Topic 11: Modern Photonic Crystal Fibers
    elif "photonic crystal" in t_low or "pcf" in t_low:
        if "guidance" in s_low or "single-mode" in s_low:
            paragraphs.append(
                "Photonic Crystal Fibers (PCFs) exhibit extraordinary optical waveguiding phenomena unobtainable in conventional step-index fibers, most notably endlessly single-mode guidance. "
                "In a solid-core PCF, light is guided within a solid silica core surrounded by a cladding containing a hexagonal lattice of microscopic air holes with diameter $d$ and hole pitch $\\Lambda$."
            )
            paragraphs.append(
                "The effective refractive index of the microstructured cladding $n_{clad}(\\lambda)$ is strongly wavelength-dependent. "
                "At short optical wavelengths, light fields are strongly concentrated in the high-index silica bridges between air holes, causing $n_{clad}$ to rise and approach the core index $n_{core}$. "
                "Consequently, the normalized frequency parameter $V_{eff} = \\frac{2\\pi \\Lambda}{\\lambda}\\sqrt{n_{core}^2 - n_{clad}^2}$ remains asymptotically constant as $\\lambda \\to 0$. "
                "When the structural ratio satisfies $d / \\Lambda \\le 0.43$, $V_{eff}$ never exceeds the single-mode cutoff threshold ($V_{eff} < \\pi$), ensuring endlessly single-mode operation across all wavelengths from the ultraviolet to the far-infrared."
            )
            paragraphs.append(
                "In hollow-core Photonic Bandgap Fibers (HC-PBGFs), light is guided inside an empty air channel by a photonic bandgap cladding that forbids photon propagation at specific frequencies. "
                "Because $> 99\\%$ of optical power propagates in air rather than glass, hollow-core PCFs eliminate silica absorption losses, achieve power thresholds thousands of times higher, and reduce optical latency to the speed of light in vacuum."
            )
        else:
            paragraphs.append(
                "Photonic Crystal Fibers (PCFs), also termed microstructured or holey fibers, represent a revolutionary paradigm shift in optical waveguide engineering. "
                "Invented by Philip Russell in 1996, PCFs are fabricated from a single material (pure fused silica) containing a two-dimensional periodic array of microscopic air channels running along the entire length of the fiber."
            )
            paragraphs.append(
                "PCFs guide light via two distinct physical mechanisms: "
                "1. **Modified Total Internal Reflection (Solid-Core PCF):** A solid silica core is surrounded by an air-silica cladding. Because the average effective index of the perforated cladding is lower than the solid core, light is guided via total internal reflection.\n"
                "2. **Photonic Bandgap Guidance (Hollow-Core PCF):** A hollow air core is surrounded by a periodic photonic crystal cladding that acts as a multi-dimensional Bragg reflector, trapping light inside the lower-index air core."
            )
            paragraphs.append(
                "Fabrication of PCFs utilizes the stack-and-draw technique, where capillary silica tubes and solid rods are manually or robotically stacked in hexagonal arrays, fused, and drawn down in multiple stages on a drawing tower. "
                "PCFs enable unprecedented dispersion engineering, immense nonlinear supercontinuum generation spanning white-light spectra, and high-power laser delivery without dielectric breakdown."
            )

    # Fallback / General Fiber Optics
    else:
        paragraphs.append(
            f"Optical fiber technology forms the physical backbone of global telecommunications and modern optical instrumentation. "
            f"In the analysis of {topic}, examining {subtopic} highlights the principles of dielectric waveguiding, modal dispersion, and attenuation management."
        )
        paragraphs.append(
            "These concepts govern high-capacity transoceanic communication networks, high-sensitivity distributed optical sensors, and advanced photonic integrated circuits. "
            "Waveguide propagation parameters dictate the modal capacity, chromatic dispersion, and optical attenuation across standard telecommunication spectral windows."
        )
        paragraphs.append(
            "Rigorous analysis reveals that dielectric waveguiding principles remain robust across linear and non-linear regimes, "
            "providing the indispensable analytical framework for modern optical communication and optoelectronic engineering."
        )

    return paragraphs



def generate_em_relativity_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Electromagnetism and Relativity topics with rigorous pedagogical depth."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    # Topic 1: Gauss Law in Electrostatics
    if "gauss law in electrostatics" in t_low or ("gauss" in t_low and "electrostatic" in t_low):
        if "differential" in s_low or "divergence" in s_low:
            paragraphs.append(
                "To derive the differential form of Gauss's law from its integral formulation, consider an arbitrary closed volume $V$ bounded by closed surface $S$ containing continuous charge density distribution $\\rho(\\mathbf{r})$. "
                "Gauss's law in integral form states that the net outward electric flux equals total enclosed charge divided by permittivity:\n\n"
                "$$\\oiint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{1}{\\epsilon_0} \\iiint_V \\rho(\\mathbf{r}) dV$$"
            )
            paragraphs.append(
                "Applying Gauss's divergence theorem from vector calculus transforms the closed surface integral into a volume integral of field divergence:\n\n"
                "$$\\oiint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\iiint_V (\\nabla \\cdot \\mathbf{E}) dV$$\n\n"
                "Equating both volume integrals yields:\n\n"
                "$$\\iiint_V \\left( \\nabla \\cdot \\mathbf{E} - \\frac{\\rho}{\\epsilon_0} \\right) dV = 0$$\n\n"
                "Because this relationship must hold for an arbitrary integration volume $V$, the integrand must vanish identically everywhere, establishing the differential form of Gauss's law (the first Maxwell equation):\n\n"
                "$$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}$$\n\n"
                "In dielectric media with macroscopic polarization $\\mathbf{P}$, the law generalizes using the electric displacement field $\\mathbf{D} = \\epsilon_0 \\mathbf{E} + \\mathbf{P}$ to $\\nabla \\cdot \\mathbf{D} = \\rho_f$, where $\\rho_f$ is free charge density."
            )
            paragraphs.append(
                "This fundamental field equation establishes that electric charges act as local scalar sources (positive divergence) or sinks (negative divergence) of the electrostatic field. "
                "In electrostatic regions free of electric charge ($\\rho = 0$), the divergence vanishes ($\\nabla \\cdot \\mathbf{E} = 0$), demonstrating that electric field lines are continuous and neither originate nor terminate in empty space."
            )
        else:
            paragraphs.append(
                "Gauss's law in electrostatics relates the spatial distribution of electric charge to the resulting electrostatic field. "
                "Electric flux $\\Phi_E$ across an oriented differential surface element $d\\mathbf{A} = \\mathbf{\\hat{n}} dA$ is defined as the scalar product integral $\\Phi_E = \\iint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\iint_S E \\cos\\theta dA$."
            )
            paragraphs.append(
                "According to Gauss's flux theorem, the net electric flux passing outward through any closed Gaussian surface $S$ enclosing net electric charge $Q_{enc}$ is formulated as:\n\n"
                "$$\\oiint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{Q_{enc}}{\\epsilon_0}$$\n\n"
                "where $\\epsilon_0 = 8.854 \\times 10^{-12}\\text{ F/m}$ is the vacuum permittivity. "
                "Gauss's law is mathematically equivalent to Coulomb's inverse-square force law, but possesses far greater geometric power and analytical elegance."
            )
            paragraphs.append(
                "Gauss's law provides an exceptionally powerful analytical tool for calculating electric fields around systems exhibiting high geometric symmetry—such as spherical charge distributions, infinite line charges, and planar charge sheets—without evaluating complex Coulomb force integrals. "
                "It proves that inside any hollow electrostatic conductor, the electric field is identically zero ($E = 0$), establishing the physical principle of electrostatic shielding (Faraday cages)."
            )

    # Topic 2: Gauss Law in Magnetism
    elif "gauss law in magnetism" in t_low or ("gauss" in t_low and "magnetism" in t_low):
        if "potential" in s_low or "vector" in s_low:
            paragraphs.append(
                "In vector calculus, a fundamental identity dictates that the divergence of the curl of any twice-differentiable vector field $\\mathbf{A}$ is identically zero: $\\nabla \\cdot (\\nabla \\times \\mathbf{A}) \\equiv 0$. "
                "Because magnetic field $\\mathbf{B}$ has vanishing divergence everywhere ($\\nabla \\cdot \\mathbf{B} = 0$), Helmholtz's theorem guarantees that $\\mathbf{B}$ can be expressed as the curl of a magnetic vector potential $\\mathbf{A}$:\n\n"
                "$$\\mathbf{B} = \\nabla \\times \\mathbf{A}$$"
            )
            paragraphs.append(
                "The magnetic vector potential $\\mathbf{A}$ possesses a gauge freedom: adding the gradient of an arbitrary scalar field $\\nabla \\lambda$ leaves $\\mathbf{B}$ completely invariant ($\\nabla \\times (\\mathbf{A} + \\nabla \\lambda) = \\nabla \\times \\mathbf{A} = \\mathbf{B}$). "
                "In magnetostatics, adopting the Coulomb gauge condition $\\nabla \\cdot \\mathbf{A} = 0$ simplifies Ampere's law into a vector Poisson equation $\\nabla^2 \\mathbf{A} = -\\mu_0 \\mathbf{J}$, with solution $\\mathbf{A}(\\mathbf{r}) = \\frac{\\mu_0}{4\\pi}\\iiint \\frac{\\mathbf{J}(\\mathbf{r}')}{|\\mathbf{r} - \\mathbf{r}'|} d^3r'$. "
                "The magnetic flux $\\Phi_B$ through an open surface $S$ bounded by contour $C$ becomes $\\Phi_B = \\iint_S (\\nabla \\times \\mathbf{A}) \\cdot d\\mathbf{A} = \\oint_C \\mathbf{A} \\cdot d\\mathbf{l}$ by Stokes' theorem."
            )
            paragraphs.append(
                "The vector potential is of vital physical significance in quantum mechanics. "
                "In the celebrated Aharonov-Bohm effect, charged particles moving through regions where magnetic field $\\mathbf{B} = 0$ but vector potential $\\mathbf{A} \\neq 0$ experience measurable quantum phase shifts, proving that $\\mathbf{A}$ is a fundamental physical field rather than a mere mathematical convenience."
            )
        else:
            paragraphs.append(
                "Gauss's law in magnetism represents the fundamental empirical fact that isolated magnetic charges (magnetic monopoles) do not exist in classical physics. "
                "Unlike electric charges which exist as isolated positive and negative monopoles, magnetic poles invariably occur as equal and opposite dipole pairs (North and South)."
            )
            paragraphs.append(
                "In integral form, the total outward magnetic flux through any closed Gaussian surface $S$ is identically zero:\n\n"
                "$$\\oiint_S \\mathbf{B} \\cdot d\\mathbf{A} = 0$$\n\n"
                "Applying Gauss's divergence theorem translates this directly into the differential form (the second Maxwell equation):\n\n"
                "$$\\nabla \\cdot \\mathbf{B} = 0$$\n\n"
                "This condition signifies that magnetic field lines have neither points of divergence (sources) nor points of convergence (sinks)."
            )
            paragraphs.append(
                "Because magnetic field lines have zero divergence, they form continuous closed loops without beginning or end. "
                "If magnetic monopoles with magnetic charge density $\\rho_m$ were ever discovered, Maxwell's second equation would modify to $\\nabla \\cdot \\mathbf{B} = \\mu_0 \\rho_m$, as proposed by Paul Dirac in his quantum mechanical monopole theory."
            )

    # Topic 3: Faraday Law of Induction
    elif "faraday" in t_low:
        if "differential" in s_low or "curl" in s_low:
            paragraphs.append(
                "Faraday's law of induction in integral form states that the electromotive force $\\mathcal{E}$ induced around an arbitrary closed stationary contour $C$ bounding open surface $S$ is proportional to the negative rate of change of magnetic flux:\n\n"
                "$$\\mathcal{E} = \\oint_C \\mathbf{E} \\cdot d\\mathbf{l} = -\\frac{d\\Phi_B}{dt} = -\\frac{d}{dt} \\iint_S \\mathbf{B} \\cdot d\\mathbf{A}$$"
            )
            paragraphs.append(
                "For a stationary contour, the time derivative passes inside the surface integral as a partial derivative: $-\\iint_S \\frac{\\partial \\mathbf{B}}{\\partial t} \\cdot d\\mathbf{A}$. "
                "Applying Stokes' theorem from vector calculus transforms the closed line integral into a surface integral of the curl of the electric field:\n\n"
                "$$\\oint_C \\mathbf{E} \\cdot d\\mathbf{l} = \\iint_S (\\nabla \\times \\mathbf{E}) \\cdot d\\mathbf{A}$$\n\n"
                "Equating both surface integrals yields:\n\n"
                "$$\\iint_S \\left( \\nabla \\times \\mathbf{E} + \\frac{\\partial \\mathbf{B}}{\\partial t} \\right) \\cdot d\\mathbf{A} = 0$$\n\n"
                "Because this relationship holds for an arbitrary surface $S$, the integrand must vanish everywhere, establishing the differential form of Faraday's law (the third Maxwell equation):\n\n"
                "$$\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$$"
            )
            paragraphs.append(
                "This equation represents a profound departure from electrostatics. In electrostatics, $\\nabla \\times \\mathbf{E} = 0$, meaning electric fields are conservative and derivable from a scalar potential ($\\mathbf{E} = -\\nabla V$). "
                "In electrodynamics, time-varying magnetic fields generate non-conservative, rotational electric fields whose work along a closed path does not vanish."
            )
        else:
            paragraphs.append(
                "Discovered empirically by Michael Faraday in 1831, electromagnetic induction is the physical phenomenon whereby a time-varying magnetic flux induces an electromotive force (emf) in an electric circuit. "
                "It serves as the governing operating principle behind all electrical generators, transformers, inductors, and induction motors."
            )
            paragraphs.append(
                "Faraday's law in integral form is formulated mathematically as:\n\n"
                "$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt} = -\\frac{d}{dt} \\iint_S \\mathbf{B} \\cdot d\\mathbf{A}$$\n\n"
                "The negative sign embodies Lenz's law, which states that the induced current flows in such a direction that its secondary magnetic field opposes the original change in magnetic flux that produced it. "
                "Lenz's law is a direct consequence of the conservation of energy: if the induced field aided the flux change, a perpetual energy multiplication would occur."
            )
            paragraphs.append(
                "Induced emf can arise via two distinct physical mechanisms: "
                "1. **Transformer emf:** A stationary circuit exposed to a time-varying magnetic field ($\\partial \\mathbf{B}/\\partial t$).\n"
                "2. **Motional emf:** A physical conductor moving through a static magnetic field with velocity $\\mathbf{v}$, where the Lorentz force $\\mathbf{F} = q(\\mathbf{v} \\times \\mathbf{B})$ drives charge carriers along the conductor."
            )

    # Topic 4: Ampere-Maxwell Law
    elif "ampere" in t_low or "displacement current" in t_low:
        if "density" in s_low or "displacement" in s_low:
            paragraphs.append(
                "To resolve the mathematical inconsistency between Ampere's circuital law and charge conservation, James Clerk Maxwell analyzed the continuity equation of electric charge:\n\n"
                "$$\\nabla \\cdot \\mathbf{J} + \\frac{\\partial \\rho}{\\partial t} = 0$$\n\n"
                "Taking the divergence of the classical Ampere law $\\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J}$ yields zero on the left side due to the vector identity $\\nabla \\cdot (\\nabla \\times \\mathbf{B}) \\equiv 0$. "
                "However, the right side gives $\\mu_0 (\\nabla \\cdot \\mathbf{J}) = -\\mu_0 \\frac{\\partial \\rho}{\\partial t}$, which is non-zero in non-steady circuits."
            )
            paragraphs.append(
                "Maxwell recognized that Gauss's law $\\rho = \\epsilon_0 (\\nabla \\cdot \\mathbf{E})$ allowed replacing the charge density derivative:\n\n"
                "$$\\frac{\\partial \\rho}{\\partial t} = \\frac{\\partial}{\\partial t} [\\epsilon_0 (\\nabla \\cdot \\mathbf{E})] = \\nabla \\cdot \\left( \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t} \\right)$$\n\n"
                "Substituting this into the continuity equation gave $\\nabla \\cdot \\left( \\mathbf{J} + \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t} \\right) = 0$. "
                "Maxwell defined the displacement current density $\\mathbf{J}_d$ as:\n\n"
                "$$\\mathbf{J}_d = \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$$\n\n"
                "Adding $\\mathbf{J}_d$ to the conduction current $\\mathbf{J}$ produced the completed Ampere-Maxwell equation (the fourth Maxwell equation):\n\n"
                "$$\\nabla \\times \\mathbf{B} = \\mu_0 \\left( \\mathbf{J} + \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t} \\right)$$"
            )
            paragraphs.append(
                "The addition of displacement current was a monumental stroke of theoretical genius. "
                "It established electromagnetic symmetry: just as Faraday discovered that a changing magnetic field produces an electric field, Maxwell proved that a changing electric field produces a magnetic field. "
                "This mutual generation permits self-sustaining electromagnetic wave propagation through empty space."
            )
        else:
            paragraphs.append(
                "Ampere's classical circuital law states that the line integral of magnetic field $\\mathbf{B}$ around any closed contour $C$ equals $\\mu_0$ times the net conduction current $I_{enc}$ penetrating surface $S$ bounded by $C$: $\\oint_C \\mathbf{B} \\cdot d\\mathbf{l} = \\mu_0 I_{enc}$."
            )
            paragraphs.append(
                "In 1861, Maxwell demonstrated that classical Ampere's law fails catastrophically for time-varying circuits, such as an AC circuit charging a parallel-plate capacitor. "
                "If an open surface $S_1$ spanning contour $C$ passes through the connecting wire, conduction current $I$ penetrates $S_1$. "
                "However, if a balloon-shaped surface $S_2$ spanning the same contour $C$ passes between the capacitor plates, zero conduction current penetrates $S_2$ because the gap contains only vacuum or dielectric."
            )
            paragraphs.append(
                "To restore physical continuity, Maxwell postulated the existence of a 'displacement current' $I_d = \\epsilon_0 \\frac{d\\Phi_E}{dt}$ flowing across the capacitor dielectric gap. "
                "Between the capacitor plates, the changing electric field creates exactly the same total displacement current as the conduction current in the connecting wires ($I_d = I$), ensuring that $\\oint_C \\mathbf{B} \\cdot d\\mathbf{l}$ is identical for any surface bounded by $C$."
            )

    # Topic 5: Maxwell Equations in Free Space
    elif "maxwell equations in free space" in t_low or ("maxwell" in t_low and "free space" in t_low):
        if "wave equation" in s_low or "dielectric" in s_low:
            paragraphs.append(
                "In source-free vacuum (free space), charge density $\\rho = 0$ and current density $\\mathbf{J} = 0$. "
                "The four Maxwell equations reduce to:\n\n"
                "1. $\\nabla \\cdot \\mathbf{E} = 0$\n"
                "2. $\\nabla \\cdot \\mathbf{B} = 0$\n"
                "3. $\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$\n"
                "4. $\\nabla \\times \\mathbf{B} = \\mu_0 \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$"
            )
            paragraphs.append(
                "To derive the electromagnetic wave equation, take the curl of Faraday's law:\n\n"
                "$$\\nabla \\times (\\nabla \\times \\mathbf{E}) = -\\nabla \\times \\left(\\frac{\\partial \\mathbf{B}}{\\partial t}\\right) = -\\frac{\\partial}{\\partial t}(\\nabla \\times \\mathbf{B})$$\n\n"
                "Applying the vector identity $\\nabla \\times (\\nabla \\times \\mathbf{E}) = \\nabla(\\nabla \\cdot \\mathbf{E}) - \\nabla^2 \\mathbf{E}$ and substituting $\\nabla \\cdot \\mathbf{E} = 0$ and the fourth equation yields:\n\n"
                "$$-\\nabla^2 \\mathbf{E} = -\\mu_0 \\epsilon_0 \\frac{\\partial^2 \\mathbf{E}}{\\partial t^2} \\implies \\nabla^2 \\mathbf{E} = \\mu_0 \\epsilon_0 \\frac{\\partial^2 \\mathbf{E}}{\\partial t^2}$$\n\n"
                "Taking the curl of the fourth equation analogously yields the wave equation for magnetic field: $\\nabla^2 \\mathbf{B} = \\mu_0 \\epsilon_0 \\frac{\\partial^2 \\mathbf{B}}{\\partial t^2}$."
            )
            paragraphs.append(
                "Comparing this with the canonical three-dimensional wave equation $\\nabla^2 \\psi = \\frac{1}{v^2} \\frac{\\partial^2 \\psi}{\\partial t^2}$ reveals that electromagnetic disturbances propagate as transverse waves with propagation velocity:\n\n"
                "$$c = \\frac{1}{\\sqrt{\\mu_0 \\epsilon_0}} = \\frac{1}{\\sqrt{(4\\pi \\times 10^{-7})(8.854 \\times 10^{-12})}} \\approx 2.998 \\times 10^8\\text{ m/s}$$\n\n"
                "Maxwell's triumphant derivation proved that light is an electromagnetic wave, unifying electricity, magnetism, and optics into a single physical discipline."
            )
        else:
            paragraphs.append(
                "Maxwell's four equations represent the complete, unified theoretical framework of classical electrodynamics. "
                "In free space, in the absence of free electric charges and currents, the equations describe the mutual dynamic coupling between electric and magnetic fields in vacuum."
            )
            paragraphs.append(
                "The four fundamental equations in differential form are: "
                "1. $\\nabla \\cdot \\mathbf{E} = 0$ (No scalar electric sources in vacuum).\n"
                "2. $\\nabla \\cdot \\mathbf{B} = 0$ (Absence of magnetic monopoles).\n"
                "3. $\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$ (Time-varying magnetic flux induces electric curl).\n"
                "4. $\\nabla \\times \\mathbf{B} = \\mu_0 \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$ (Time-varying electric flux induces magnetic curl)."
            )
            paragraphs.append(
                "In linear, isotropic dielectric media characterized by permittivity $\\epsilon = \\epsilon_r \\epsilon_0$ and permeability $\\mu = \\mu_r \\mu_0$, the speed of electromagnetic waves decreases to $v = 1 / \\sqrt{\\mu\\epsilon} = c / n$, where $n = \\sqrt{\\epsilon_r \\mu_r}$ is the optical refractive index of the medium. "
                "This relation provides the electromagnetic foundation for Snell's law, Fresnel reflection, and optical waveguide propagation."
            )

    # Topic 6: Electromagnetic Wave Propagation
    elif "electromagnetic wave propagation" in t_low or ("propagation" in t_low and "transverse" in t_low):
        if "impedance" in s_low or "vacuum" in s_low:
            paragraphs.append(
                "The intrinsic impedance (wave impedance) of a medium quantifies the ratio of transverse electric field amplitude to transverse magnetic field amplitude for a propagating electromagnetic plane wave. "
                "For a monochromatic plane wave propagating along the $+z$ direction with electric field $\\mathbf{E} = E_0 \\cos(kz - \\omega t)\\mathbf{\\hat{x}}$, Faraday's law dictates $\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$."
            )
            paragraphs.append(
                "Evaluating the curl gives $\\frac{\\partial E_x}{\\partial z}\\mathbf{\\hat{y}} = -k E_0 \\sin(kz - \\omega t)\\mathbf{\\hat{y}} = -\\frac{\\partial B_y}{\\partial t}\\mathbf{\\hat{y}}$. "
                "Integrating with respect to time yields $B_y = \\frac{k}{\\omega} E_0 \\cos(kz - \\omega t) = \\frac{1}{c} E_x$. "
                "Relating magnetic field $\\mathbf{B}$ to magnetic intensity $\\mathbf{H} = \\mathbf{B} / \\mu_0$ defines the intrinsic impedance of free space $\\eta_0$:\n\n"
                "$$\\eta_0 = \\frac{E_x}{H_y} = \\frac{E_0}{B_0 / \\mu_0} = \\mu_0 c = \\sqrt{\\frac{\\mu_0}{\\epsilon_0}}$$\n\n"
                "Substituting $\\mu_0 = 4\\pi \\times 10^{-7}\\text{ H/m}$ and $\\epsilon_0 = 8.854 \\times 10^{-12}\\text{ F/m}$ yields the exact impedance:\n\n"
                "$$\\eta_0 = \\sqrt{\\frac{4\\pi \\times 10^{-7}}{8.854 \\times 10^{-12}}} \\approx 376.73\\text{ }\\Omega \\approx 120\\pi\\text{ }\\Omega$$"
            )
            paragraphs.append(
                "The intrinsic impedance $\\eta_0 \\approx 377\\text{ }\\Omega$ plays an analogous role in electrodynamics to acoustic impedance in acoustics and characteristic transmission line impedance in electrical engineering. "
                "Impedance matching between different dielectric media governs transmission and reflection coefficients at optical boundaries and antenna radiation efficiency."
            )
        else:
            paragraphs.append(
                "Electromagnetic waves in free space and homogeneous isotropic dielectrics are transverse waves (TEM waves). "
                "This means that both the electric field vector $\\mathbf{E}$ and the magnetic field vector $\\mathbf{B}$ oscillate perpendicular to each other and perpendicular to the direction of wave propagation vector $\\mathbf{k}$."
            )
            paragraphs.append(
                "This transverse character is a direct mathematical consequence of the zero divergence conditions in free space: "
                "$\\nabla \\cdot \\mathbf{E} = i \\mathbf{k} \\cdot \\mathbf{E} = 0$ and $\\nabla \\cdot \\mathbf{B} = i \\mathbf{k} \\cdot \\mathbf{B} = 0$. "
                "Because the dot product of wavevector $\\mathbf{k}$ with field vectors vanishes, neither $\\mathbf{E}$ nor $\\mathbf{B}$ can possess longitudinal components along the propagation axis in unbounded free space."
            )
            paragraphs.append(
                "Furthermore, $\\mathbf{E}$ and $\\mathbf{B}$ are in phase in free space, reaching their maximum, minimum, and zero values simultaneously. "
                "The three vectors form a mutually orthogonal right-handed triad: $\\mathbf{\\hat{E}} \\times \\mathbf{\\hat{B}} = \\mathbf{\\hat{k}}$, dictating the directional flow of electromagnetic energy."
            )

    # Topic 7: Poynting Theorem
    elif "poynting" in t_low:
        if "energy density" in s_low or "power flow" in s_low:
            paragraphs.append(
                "Poynting's theorem represents the work-energy theorem of classical electrodynamics, formulating the conservation of energy for combined electromagnetic fields and charged matter. "
                "The instantaneous total electromagnetic energy density $u$ stored in electric and magnetic fields within a linear medium is:\n\n"
                "$$u = u_E + u_B = \\frac{1}{2} \\epsilon_0 E^2 + \\frac{1}{2\\mu_0} B^2$$\n\n"
                "In a propagating plane wave in vacuum, electric and magnetic energy densities are identically equal: $u_E = \\frac{1}{2}\\epsilon_0 E^2 = \\frac{1}{2}\\epsilon_0 (c B)^2 = \\frac{1}{2\\mu_0} B^2 = u_B$."
            )
            paragraphs.append(
                "The rate of electromagnetic energy flow per unit area across an oriented boundary surface is defined by the Poynting vector $\\mathbf{S}$:\n\n"
                "$$\\mathbf{S} = \\frac{1}{\\mu_0} (\\mathbf{E} \\times \\mathbf{B}) = \\mathbf{E} \\times \\mathbf{H}$$\n\n"
                "The magnitude of $\\mathbf{S}$ represents instantaneous power density (in $\\text{W/m}^2$). "
                "For a time-harmonic wave, the time-averaged Poynting vector $\\langle \\mathbf{S} \\rangle$ defines wave intensity $I$:\n\n"
                "$$I = \\langle S \\rangle = \\frac{1}{2} c \\epsilon_0 E_0^2 = \\frac{E_0^2}{2\\eta_0} = \\frac{E_{rms}^2}{\\eta_0}$$\n\n"
                "Poynting's theorem also demonstrates that electromagnetic waves carry linear momentum density $\\mathbf{p}_{em} = \\mathbf{S} / c^2$, exerting radiation pressure $P = I / c$ upon absorbing surfaces."
            )
            paragraphs.append(
                "Applying Poynting's theorem to closed systems proves that energy loss in electrical circuits—such as Joule heating in resistive wires—flows from surrounding electromagnetic fields into the conductor surface, completely consistent with field theory."
            )
        else:
            paragraphs.append(
                "Poynting's theorem, derived by John Henry Poynting in 1884, formulates the local conservation of energy for electrodynamic systems. "
                "To derive the theorem, consider the rate of work done by electromagnetic forces on a distribution of charges with current density $\\mathbf{J}$ in volume $V$: $\\frac{dW}{dt} = \\iiint_V (\\mathbf{J} \\cdot \\mathbf{E}) dV$."
            )
            paragraphs.append(
                "Using the Ampere-Maxwell law $\\mathbf{J} = \\frac{1}{\\mu_0}(\\nabla \\times \\mathbf{B}) - \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}$, evaluating the scalar product $\\mathbf{J} \\cdot \\mathbf{E}$ and applying the vector calculus identity $\\nabla \\cdot (\\mathbf{E} \\times \\mathbf{B}) = \\mathbf{B} \\cdot (\\nabla \\times \\mathbf{E}) - \\mathbf{E} \\cdot (\\nabla \\times \\mathbf{B})$ yields the differential form of Poynting's theorem:\n\n"
                "$$-\\frac{\\partial u}{\\partial t} = \\nabla \\cdot \\mathbf{S} + \\mathbf{J} \\cdot \\mathbf{E}$$\n\n"
                "where $u = \\frac{1}{2}\\epsilon_0 E^2 + \\frac{1}{2\\mu_0}B^2$ is total energy density, $\\mathbf{S} = \\frac{1}{\\mu_0}(\\mathbf{E} \\times \\mathbf{B})$ is the Poynting vector, and $\\mathbf{J} \\cdot \\mathbf{E}$ is the rate of mechanical energy transfer to matter."
            )
            paragraphs.append(
                "Integrating over volume $V$ bounded by surface $A$ produces the integral form: $-\\frac{d}{dt}\\iiint_V u dV = \\oiint_A \\mathbf{S} \\cdot d\\mathbf{A} + \\iiint_V (\\mathbf{J} \\cdot \\mathbf{E}) dV$. "
                "This states that the rate of decrease of electromagnetic energy inside volume $V$ equals the net outward radiant power flux escaping through boundary surface $A$ plus the work done on internal charges."
            )

    # Topic 8: Galilean Relativity Inadequacy
    elif "galilean" in t_low:
        if "michelson" in s_low or "experiment" in s_low:
            paragraphs.append(
                "The Michelson-Morley experiment of 1887 was designed to detect the motion of the Earth through the hypothesized luminiferous ether—the hypothetical mechanical medium presumed to permeate all space as the carrier of light waves. "
                "Albert Michelson and Edward Morley utilized a high-sensitivity optical interferometer mounted on a heavy granite slab floating in mercury to observe fringe shifts as the apparatus rotated."
            )
            paragraphs.append(
                "According to Galilean velocity addition, if the Earth moves through the ether with orbital velocity $v \\approx 30\\text{ km/s}$, light traveling parallel to Earth's motion should have velocity $c \\pm v$, while light traveling transversely should have velocity $\\sqrt{c^2 - v^2}$. "
                "The resulting round-trip time difference between orthogonal arms of length $L$ was predicted to produce a fringe shift upon $90^\\circ$ rotation:\n\n"
                "$$\\Delta N = \\frac{2L}{\\lambda} \\frac{v^2}{c^2}$$\n\n"
                "For $L = 11\\text{ m}$ and $\\lambda = 590\\text{ nm}$, the predicted shift was $0.4$ fringes, easily resolvable by their $0.01$ fringe sensitivity."
            )
            paragraphs.append(
                "The experiment yielded a definitive null result: no fringe shift was observed within experimental error. "
                "This monumental negative result shattered the luminiferous ether hypothesis and demonstrated that the speed of light is strictly isotropic and independent of the motion of the Earth, laying the experimental foundation for Einstein's special theory of relativity."
            )
        else:
            paragraphs.append(
                "Classical Newtonian mechanics is governed by Galilean relativity, which assumes the existence of absolute, universal time ($t' = t$) identical for all observers in relative motion. "
                "Under Galilean transformations between inertial frame $S$ and frame $S'$ moving at velocity $v$ along the $x$-axis, spatial coordinates transform as: $x' = x - vt, y' = y, z' = z$."
            )
            paragraphs.append(
                "Differentiating these transformations with respect to universal time yields the classical Galilean velocity addition rule: $u_x' = u_x - v$. "
                "While Newton's second law ($\\mathbf{F} = m\\mathbf{a}$) is invariant under Galilean transformations, Maxwell's electrodynamic equations are not. "
                "Substituting Galilean transformations into Maxwell's wave equation produces extra non-zero velocity-dependent terms, falsely predicting that the speed of light must vary depending on observer velocity."
            )
            paragraphs.append(
                "This theoretical incompatibility presented nineteenth-century physics with a profound crisis: either Maxwell's equations were incomplete, or Newtonian mechanics was flawed. "
                "Einstein recognized that the fault lay with Galilean spacetime, replacing Galilean transformations with Lorentz transformations and discarding absolute time."
            )

    # Topic 9: Postulates of Special Relativity
    elif "postulates" in t_low:
        if "constancy" in s_low or "light" in s_low:
            paragraphs.append(
                "Einstein's second postulate of special relativity—the principle of the constancy of the speed of light—states: "
                "'Light propagates through vacuum at a definite speed $c$ that is entirely independent of the state of motion of the emitting source or the observing inertial frame.' "
                "This postulate is formulated mathematically by requiring the spherical wavefront condition $x^2 + y^2 + z^2 - c^2 t^2 = 0$ to hold identically across all inertial reference frames: $x'^2 + y'^2 + z'^2 - c^2 t'^2 = 0$."
            )
            paragraphs.append(
                "This postulate directly contradicts classical Newtonian velocity addition, where an observer chasing a light wave at velocity $v$ should observe light traveling at speed $c - v$. "
                "In relativistic mechanics, regardless of how fast an observer moves toward or away from a light source, the measured speed of the photons in vacuum is always identically $c = 299,792,458\\text{ m/s}$."
            )
            paragraphs.append(
                "The constancy of $c$ forces space and time to become dynamic, observer-dependent physical quantities. "
                "To ensure that all observers measure the same speed $c = \\Delta x / \\Delta t$, spatial distance intervals and temporal duration intervals must transform simultaneously, leading inexorably to length contraction, time dilation, and the relativity of simultaneity."
            )
        else:
            paragraphs.append(
                "In June 1905, Albert Einstein published his landmark paper 'On the Electrodynamics of Moving Bodies', founding the Special Theory of Relativity upon two fundamental postulates: "
                "1. **The Principle of Relativity:** The laws of physics—including both mechanics and electromagnetism—take the identical mathematical form in all inertial reference frames.\n"
                "2. **The Constancy of the Speed of Light:** The speed of light in vacuum is an absolute universal constant $c$, identical for all inertial observers regardless of their relative motion or the motion of the source."
            )
            paragraphs.append(
                "The first postulate extends Galileo's principle of relativity from Newtonian mechanics to the entire domain of physical laws, abolishing the concept of a preferred absolute frame of rest (the ether). "
                "No physical experiment—mechanical, optical, or electromagnetic—can distinguish between an inertial frame at rest and one moving at constant velocity."
            )
            paragraphs.append(
                "Together, these two elegant postulates revolutionized our fundamental understanding of nature. "
                "They revealed that space and time cannot exist as separate absolute entities, but are united into a four-dimensional pseudo-Riemannian continuum termed Minkowski spacetime."
            )

    # Topic 10: Lorentz Transformations
    elif "lorentz" in t_low:
        if "contraction" in s_low:
            paragraphs.append(
                "Length contraction (Lorentz-FitzGerald contraction) is the relativistic physical phenomenon where the measured length of an object in motion is shorter than its proper length measured in its own rest frame. "
                "Consider a rigid rod of proper length $L_0 = x_2' - x_1'$ at rest in inertial frame $S'$ moving at velocity $v$ along the $x$-axis relative to frame $S$."
            )
            paragraphs.append(
                "To determine length $L = x_2 - x_1$ in frame $S$, an observer in $S$ must record the coordinates of both rod ends simultaneously at the identical time instant $t_1 = t_2 = t$. "
                "Applying the inverse Lorentz transformation $x' = \\gamma (x - vt)$ gives $x_2' = \\gamma (x_2 - vt)$ and $x_1' = \\gamma (x_1 - vt)$. "
                "Subtracting both equations yields:\n\n"
                "$$L_0 = x_2' - x_1' = \\gamma (x_2 - x_1) = \\gamma L$$\n\n"
                "Solving for the measured length $L$ yields the length contraction formula:\n\n"
                "$$L = \\frac{L_0}{\\gamma} = L_0 \\sqrt{1 - \\frac{v^2}{c^2}}$$"
            )
            paragraphs.append(
                "Because $\\gamma > 1$ for any non-zero velocity, $L < L_0$. Length contraction occurs strictly along the direction of relative motion, while transverse dimensions ($y, z$) remain completely unaffected ($y' = y, z' = z$). "
                "Length contraction is a genuine geometric property of spacetime measurement, directly verified in particle accelerator experiments where relativistic electron bunches compress longitudinally."
            )
        else:
            paragraphs.append(
                "The Lorentz transformations are the set of coordinate transformations that relate space and time measurements between two inertial reference frames moving at constant relative velocity, preserving the invariance of Maxwell's equations and the speed of light. "
                "Consider frame $S'$ moving at constant velocity $v$ along the common $+x$ axis relative to frame $S$, with origins coinciding at $t = t' = 0$."
            )
            paragraphs.append(
                "The relativistic space-time coordinates transform according to:\n\n"
                "$$x' = \\gamma (x - vt)$$\n\n"
                "$$y' = y$$\n\n"
                "$$z' = z$$\n\n"
                "$$t' = \\gamma \\left( t - \\frac{vx}{c^2} \\right)$$\n\n"
                "where $\\gamma$ is the dimensionless Lorentz factor defined as:\n\n"
                "$$\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}} = \\frac{1}{\\sqrt{1 - \\beta^2}}$$\n\n"
                "When $v \\ll c$, the factor $v/c \\to 0$, causing $\\gamma \\to 1$ and $vx/c^2 \\to 0$, smoothly reducing the Lorentz transformations to classical Galilean transformations."
            )
            paragraphs.append(
                "The temporal transformation $t' = \\gamma(t - vx/c^2)$ contains the critical term $-vx/c^2$, which demonstrates the relativity of simultaneity. "
                "Two spatially separated events that appear simultaneous in frame $S$ ($\\Delta t = 0$) do not occur simultaneously in moving frame $S'$ ($\\Delta t' = -\\gamma v \\Delta x / c^2 \\neq 0$)."
            )

    # Topic 11: Time Dilation and Mass-Energy Equivalence
    elif "time dilation" in t_low or "mass-energy" in t_low or "twin paradox" in t_low or "e = mc^2" in t_low:
        if "derivation" in s_low or "e = mc^2" in s_low or "mass-energy" in s_low:
            paragraphs.append(
                "To derive Einstein's mass-energy equivalence $E = mc^2$, consider the relativistic momentum of a particle of invariant rest mass $m_0$ moving at velocity $v$: $\\mathbf{p} = \\gamma m_0 \\mathbf{v} = m \\mathbf{v}$, where $m = \\gamma m_0$ is the relativistic mass. "
                "Newton's second law in relativistic mechanics states that force equals the time rate of change of momentum:\n\n"
                "$$\\mathbf{F} = \\frac{d\\mathbf{p}}{dt} = \\frac{d}{dt}(m\\mathbf{v})$$"
            )
            paragraphs.append(
                "The kinetic energy $E_k$ acquired by the particle when accelerated from rest ($v = 0$) to velocity $v$ across displacement $dx$ is the work done by the force:\n\n"
                "$$E_k = \\int_0^x F dx = \\int_0^x \\frac{d(mv)}{dt} dx = \\int_0^v v d(mv) = \\int_0^v (v^2 dm + m v dv)$$\n\n"
                "Differentiating the relativistic mass formula $m^2 c^2 - m^2 v^2 = m_0^2 c^2$ yields $2m dm c^2 - 2m dm v^2 - 2m^2 v dv = 0$, which simplifies to $c^2 dm = v^2 dm + m v dv$. "
                "Substituting this identity into the work integral gives:\n\n"
                "$$E_k = \\int_{m_0}^m c^2 dm = c^2 (m - m_0) = mc^2 - m_0 c^2$$\n\n"
                "Rearranging terms gives the total relativistic energy $E$:\n\n"
                "$$E = E_k + m_0 c^2 = mc^2 = \\gamma m_0 c^2$$\n\n"
                "where $E_0 = m_0 c^2$ represents the intrinsic rest-mass energy of the particle."
            )
            paragraphs.append(
                "The celebrated formula $E = mc^2$ establishes that mass is condensed energy. "
                "Mass-energy equivalence governs the immense energy release in nuclear fission (e.g., uranium reactors) and nuclear fusion (e.g., stellar nucleosynthesis in the Sun), where microscopic mass defects $\\Delta m$ convert directly into energetic photons and kinetic energy via $\\Delta E = \\Delta m c^2$."
            )
        else:
            paragraphs.append(
                "Time dilation is the relativistic physical phenomenon where the elapsed time between two events measured by an observer in motion is longer than the proper time interval recorded by an observer at rest with the clock. "
                "If a clock at rest in frame $S'$ records a proper time interval $\\Delta t_0 = t_2' - t_1'$ between two ticks at the same spatial coordinate $x'$, the time interval $\\Delta t = t_2 - t_1$ measured in laboratory frame $S$ is:\n\n"
                "$$\\Delta t = \\gamma \\Delta t_0 = \\frac{\\Delta t_0}{\\sqrt{1 - v^2/c^2}}$$\n\n"
                "Because $\\gamma > 1$ for all velocities $v > 0$, $\\Delta t > \\Delta t_0$, proving that moving clocks run slow."
            )
            paragraphs.append(
                "The Twin Paradox is the famous thought experiment illustrating time dilation: "
                "One twin embarks on a high-speed relativistic space journey while the other twin remains on Earth. "
                "Upon return, the traveling twin is physically younger than the Earth twin. "
                "The asymmetry resolves because the traveling twin undergoes physical acceleration and deceleration when turning around, breaking inertial symmetry and changing reference frames, which shifts the Minkowski spacetime path length (proper time $\\tau = \\int d\\tau$)."
            )
            paragraphs.append(
                "Time dilation is confirmed daily by atmospheric muon observations: "
                "Muons generated in the upper atmosphere by cosmic rays have a rest lifetime of only $\\tau_0 \\approx 2.2\\text{ }\\mu\\text{s}$, which classically allows them to travel only $\\sim 660\\text{ m}$ before decaying. "
                "Due to relativistic time dilation at $v \\approx 0.998c$ ($\\gamma \\approx 15.8$), their laboratory lifetime expands to $\\sim 35\\text{ }\\mu\\text{s}$, allowing them to easily survive the $10\\text{ km}$ journey to sea level detectors."
            )

    # Fallback / General EM & Relativity
    else:
        paragraphs.append(
            f"Electromagnetism and Special Relativity form the foundational pillar of classical field theory and relativistic mechanics. "
            f"In the analysis of {topic}, examining {subtopic} establishes the governing differential equations, field transformations, and spacetime symmetry principles."
        )
        paragraphs.append(
            "Maxwell's unification of electric and magnetic fields predicted the propagation of transverse electromagnetic waves in vacuum with intrinsic impedance $\\eta_0 \\approx 377\\text{ }\\Omega$. "
            "Einstein's relativistic spacetime geometry resolved the fundamental conflict between Maxwellian electrodynamics and Newtonian mechanics."
        )
        paragraphs.append(
            "These mathematical principles govern high-frequency microwave engineering, particle accelerators, synchrotron radiation sources, and global satellite positioning systems (GPS), "
            "providing the indispensable theoretical and practical framework for modern physical engineering."
        )

    return paragraphs



def generate_physics_numerical(topic: str, subtopic: str) -> str:
    """Generates authentic university solved numericals for physics topics."""
    comb = (topic + " " + subtopic).lower()

    if "box" in comb or "well" in comb:
        return (
            "### Solved Numerical Example\n\n"
            "**Problem:** Calculate the ground-state energy and first excited-state energy (in electron-volts) for an electron ($m_e = 9.109 \\times 10^{-31}\\text{ kg}$) confined within a one-dimensional infinite potential well of width $L = 0.2\\text{ nm}$.\n\n"
            "**Solution:**\n"
            "1. **Given Data:** Mass of electron $m = 9.109 \\times 10^{-31}\\text{ kg}$, well width $L = 0.2 \\times 10^{-9}\\text{ m}$, Planck's constant $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$.\n"
            "2. **Governing Formula:** The quantized energy levels for a 1D box are given by $E_n = \\frac{n^2 h^2}{8mL^2}$.\n"
            "3. **Substitution & Calculation:**\n"
            "$$E_1 = \\frac{(1)^2 (6.626 \\times 10^{-34})^2}{8 (9.109 \\times 10^{-31}) (0.2 \\times 10^{-9})^2} = \\frac{4.390 \\times 10^{-67}}{2.915 \\times 10^{-48}} = 1.506 \\times 10^{-19}\\text{ J}$$\n"
            "Converting to electron-volts: $E_1 = \\frac{1.506 \\times 10^{-19}\\text{ J}}{1.602 \\times 10^{-19}\\text{ J/eV}} = 9.40\\text{ eV}$.\n"
            "4. **Answer & Unit:** Ground-state energy is $9.40\\text{ eV}$ and first excited-state ($n = 2$) energy is $E_2 = 4 \\times 9.40 = 37.60\\text{ eV}$."
        )

    elif "de broglie" in comb or "wave nature" in comb or "broglie" in comb or "dual" in comb:
        return (
            "### Solved Numerical Example\n\n"
            "**Problem:** An electron is accelerated from rest through an electrostatic potential difference of $V = 100\\text{ V}$. Compute its de Broglie wavelength in angstroms and compare it to the interatomic spacing of a silicon crystal ($d \\approx 2.35\\text{ \\AA}$).\n\n"
            "**Solution:**\n"
            "1. **Given Data:** Accelerating potential $V = 100\\text{ V}$, electron mass $m_e = 9.109 \\times 10^{-31}\\text{ kg}$, charge $e = 1.602 \\times 10^{-19}\\text{ C}$.\n"
            "2. **Governing Formula:** For an electron accelerated through potential $V$, the de Broglie wavelength is $\\lambda_e = \\frac{h}{\\sqrt{2m_e e V}} = \\frac{12.27}{\\sqrt{V}}\\text{ \\AA}$.\n"
            "3. **Substitution & Calculation:**\n"
            "$$\\lambda_e = \\frac{12.27}{\\sqrt{100}} = \\frac{12.27}{10} = 1.227\\text{ \\AA} \\approx 1.23\\text{ \\AA} = 0.1227\\text{ nm}$$\n"
            "4. **Answer & Unit:** The calculated wavelength is $\\lambda = 1.227\\text{ \\AA} \\approx 1.23\\text{ \\AA}$, comparable to silicon lattice spacing ($2.35\\text{ \\AA}$)."
        )

    elif "young" in comb or "interference" in comb or "fringe" in comb:
        return (
            "### Solved Numerical Example\n\n"
            "**Problem:** In a Young's double slit experiment, monochromatic light of wavelength $\\lambda = 600\\text{ nm}$ illuminates slits separated by $d = 0.5\\text{ mm}$. If the observation screen is placed at distance $D = 1.5\\text{ m}$, calculate the fringe width $\\beta$ and the linear distance of the fourth bright fringe from the central axis.\n\n"
            "**Solution:**\n"
            "1. **Given Data:** Wavelength $\\lambda = 600 \\times 10^{-9}\\text{ m}$, slit separation $d = 0.5 \\times 10^{-3}\\text{ m}$, screen distance $D = 1.5\\text{ m}$.\n"
            "2. **Governing Formula:** Fringe width is $\\beta = \\frac{\\lambda D}{d}$, and bright fringe position is $y_n = \\frac{n \\lambda D}{d} = n \\beta$.\n"
            "3. **Substitution & Calculation:**\n"
            "$$\\beta = \\frac{(600 \\times 10^{-9}) \\times 1.5}{0.5 \\times 10^{-3}} = 1.80 \\times 10^{-3}\\text{ m} = 1.80\\text{ mm}$$\n"
            "For $n = 4$: $y_4 = 4 \\times 1.80\\text{ mm} = 7.20\\text{ mm}$.\n"
            "4. **Answer & Unit:** Fringe width is $1.80\\text{ mm}$ and fourth bright fringe is located at $7.20\\text{ mm}$."
        )

    elif "fiber" in comb or "acceptance" in comb or "numerical aperture" in comb:
        return (
            "### Solved Numerical Example\n\n"
            "**Problem:** A step-index optical fiber has a core refractive index $n_1 = 1.480$ and a cladding refractive index $n_2 = 1.465$. Compute the critical angle $\\phi_c$ at the core-cladding boundary, the Numerical Aperture (NA), and the maximum acceptance angle $\\theta_a$ in air ($n_0 = 1.0$).\n\n"
            "**Solution:**\n"
            "1. **Given Data:** Core index $n_1 = 1.480$, cladding index $n_2 = 1.465$, medium index $n_0 = 1.0$.\n"
            "2. **Governing Formula:** $\\phi_c = \\arcsin(n_2 / n_1)$, $\\text{NA} = \\sqrt{n_1^2 - n_2^2}$, and $\\theta_a = \\arcsin(\\text{NA} / n_0)$.\n"
            "3. **Substitution & Calculation:**\n"
            "$$\\phi_c = \\arcsin\\left(\\frac{1.465}{1.480}\\right) = \\arcsin(0.98986) = 81.84^\\circ$$\n"
            "$$\\text{NA} = \\sqrt{(1.480)^2 - (1.465)^2} = \\sqrt{2.1904 - 2.1462} = \\sqrt{0.0442} = 0.2102$$\n"
            "$$\\theta_a = \\arcsin(0.2102) = 12.13^\\circ$$\n"
            "4. **Answer & Unit:** $\\phi_c = 81.84^\\circ$, $\\text{NA} = 0.210$ (dimensionless), and $\\theta_a = 12.13^\\circ$."
        )

    else:
        return (
            "### Solved Numerical Example\n\n"
            "**Problem:** A spacecraft travels past an observer on Earth at relativistic velocity $v = 0.8c$. If an onboard atomic clock records an elapsed time interval of $\\Delta t_0 = 1.0\\text{ hour}$, calculate the elapsed time measured by Earth observers and the Lorentz factor $\\gamma$.\n\n"
            "**Solution:**\n"
            "1. **Given Data:** Velocity $v = 0.8c$, proper time interval $\\Delta t_0 = 1.0\\text{ hour}$, speed of light $c = 3.0 \\times 10^8\\text{ m/s}$.\n"
            "2. **Governing Formula:** Lorentz factor $\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}$, dilated time $\\Delta t = \\gamma \\Delta t_0$.\n"
            "3. **Substitution & Calculation:**\n"
            "$$\\gamma = \\frac{1}{\\sqrt{1 - (0.8)^2}} = \\frac{1}{\\sqrt{0.36}} = \\frac{1}{0.6} = 1.667$$\n"
            "$$\\Delta t = 1.667 \\times 1.0\\text{ hour} = 1.667\\text{ hours} = 1\\text{ hour } 40\\text{ minutes}$$\n"
            "4. **Answer & Unit:** Lorentz factor $\\gamma = 1.667$ (dimensionless) and dilated time interval $\\Delta t = 1.667\\text{ hours}$."
        )


def generate_physics_questions(topic: str, subtopic: str) -> str:
    """Generates authentic university conceptual and analytical review questions."""
    return (
        "### Academic Review & Conceptual Questions\n\n"
        f"1. **Conceptual Understanding:** Formulate the physical principles underlying {topic}, focusing specifically on how {subtopic} defines microscopic or macroscopic boundary behavior.\n\n"
        "2. **Mathematical Derivation:** Starting from foundational governing relations, derive the analytical expression for this topic and explain the physical significance of each constant and variable.\n\n"
        "3. **Critical Analysis:** Discuss the experimental verification milestones that validated this theory, and outline the boundary limitations where the model fails or requires relativistic/quantum corrections."
    )
