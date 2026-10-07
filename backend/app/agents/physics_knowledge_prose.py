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

    # Priority 1: Particle in a 1D Box / Potential Well
    if "box" in t_low or "well" in t_low:
        if any(k in s_low for k in ["physical model", "boundary condition", "model", "setup", "potential"]):
            paragraphs.append(
                "Consider a non-relativistic quantum particle of mass $m$ confined within a one-dimensional infinite potential well defined by: "
                "$V(x) = 0$ for $0 < x < L$, and $V(x) = \\infty$ for $x \\le 0$ and $x \\ge L$. "
                "Because the potential barrier is infinitely impenetrable outside the well, the particle has zero probability of penetrating the walls, "
                "mandating rigid Dirichlet boundary conditions: $\\psi(0) = 0$ and $\\psi(L) = 0$. "
                "Within the interior interval $0 < x < L$, the time-independent Schrödinger equation simplifies to $\\frac{d^2\\psi}{dx^2} + k^2\\psi = 0$, where wavenumber $k = \\frac{\\sqrt{2mE}}{\\hbar}$."
            )
            paragraphs.append(
                "The general mathematical solution inside the infinite potential well is $\\psi(x) = A\\sin(kx) + B\\cos(kx)$. "
                "Applying the boundary condition at the left boundary wall ($x = 0$) requires $\\psi(0) = B = 0$, reducing the physical spatial state to a pure sinusoidal oscillation $\\psi(x) = A\\sin(kx)$. "
                "At the right boundary wall ($x = L$), wave function continuity mandates $\\psi(L) = A\\sin(kL) = 0$. "
                "For physically non-trivial states ($A \\ne 0$), the spatial argument must satisfy the discrete constraint $kL = n\\pi$, establishing discrete wavenumber quantization $k_n = \\frac{n\\pi}{L}$ for integer quantum numbers $n = 1, 2, 3, \\dots$."
            )
        elif any(k in s_low for k in ["energy", "eigenvalue", "derivation", "normalization", "wave function"]) or requires_derivation:
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
        else:
            paragraphs.append(
                "The one-dimensional infinite potential well provides an essential pedagogical model demonstrating how spatial boundary constraints induce discrete energy quantization. "
                "Classically, a point particle bouncing elastically between rigid walls may assume any continuous energy value, and its probability density "
                "remains strictly uniform throughout the enclosure. In contrast, quantum wave mechanics establishes standing matter waves with spatial nodes "
                "where the probability density $P_n(x) = |\\psi_n(x)|^2$ vanishes entirely."
            )
            paragraphs.append(
                "For even quantum numbers ($n = 2, 4, \\dots$), a central nodal plane exists at the geometric midpoint $x = L/2$. "
                "The particle possesses zero probability of being detected at the well center, yet transitions dynamically across the enclosure, "
                "providing an unmistakable demonstration of the non-classical nature of quantum wave interference."
            )

    # Priority 2: de Broglie Hypothesis / Matter Waves
    elif "de broglie" in t_low or "broglie" in t_low:
        if any(k in s_low for k in ["dual nature", "davisson", "germer", "experiment", "verification"]):
            paragraphs.append(
                "In 1924, French physicist Louis de Broglie formulated his revolutionary de Broglie hypothesis, establishing the dual nature of matter: "
                "material particles such as electrons possess an intrinsic wave character governed by the fundamental matter wavelength relation:\n\n"
                "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2m E_k}}$$\n\n"
                "where $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ represents Planck's constant, $p$ is momentum, and $E_k$ is kinetic energy. "
                "For a charged particle carrying elementary charge $e$ accelerated from rest through an electric potential difference $V$, the acquired kinetic energy equals $E_k = eV$. "
                "Substituting the electron mass $m_e = 9.109 \\times 10^{-31}\\text{ kg}$ and elementary charge $e = 1.602 \\times 10^{-19}\\text{ C}$ yields the canonical engineering relation:\n\n"
                "$$\\lambda_e = \\frac{1.227}{\\sqrt{V}}\\text{ nm} = \\frac{12.27}{\\sqrt{V}}\\text{ \\AA}$$\n\n"
                "For accelerating voltages between 50 V and 150 V, electron matter wavelengths span $0.1\\text{ to }0.17\\text{ nm}$, which is precisely commensurate with interatomic crystal lattice constants."
            )
            paragraphs.append(
                "The definitive empirical confirmation of matter waves was achieved in 1927 by Clinton Davisson and Lester Germer at Bell Telephone Laboratories. "
                "Their experimental apparatus directed a collimated beam of electrons accelerated through potential difference $V = 54\\text{ V}$ normally onto the surface of a target nickel single crystal. "
                "Davisson and Germer observed a prominent scattering intensity peak at an azimuth angle of $\\phi = 50^\\circ$. "
                "Treating the nickel single crystal as a three-dimensional diffraction grating with lattice interplanar spacing $d = 0.091\\text{ nm}$, "
                "they applied Bragg's diffraction law $2d\\sin\\theta = n\\lambda$ to the glancing angle $\\theta = 90^\\circ - 50^\\circ/2 = 65^\\circ$ (or surface planes $D\\sin\\phi = n\\lambda$ where $D = 0.215\\text{ nm}$):\n\n"
                "$$\\lambda_{exp} = D \\sin(50^\\circ) = (0.215\\text{ nm})(0.766) = 0.165\\text{ nm}$$\n\n"
                "Comparing this empirical measurement against de Broglie's theoretical prediction $\\lambda = \\frac{1.227}{\\sqrt{54}}\\text{ nm} = 0.167\\text{ nm}$ revealed extraordinary agreement within 1.2%, "
                "conclusively establishing that moving electrons exhibit authentic spatial wave diffraction and constructive interference."
            )
        elif any(k in s_low for k in ["relation", "wavelength", "derivation", "formula", "momentum"]) or requires_derivation:
            paragraphs.append(
                "To derive the matter wavelength relation, Louis de Broglie began from Einstein's relativistic energy relation for a zero rest-mass photon: $E = pc$, where $p$ is momentum. "
                "Equating this expression to Planck's quantum energy equation $E = h\\nu = \\frac{hc}{\\lambda}$ yields $pc = \\frac{hc}{\\lambda} \\implies p = \\frac{h}{\\lambda}$."
            )
            paragraphs.append(
                "De Broglie boldly postulated that this momentum-wavelength inversion applies universally to any material particle of rest mass $m$ traveling with physical velocity $v$:\n\n"
                "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2m E_k}}$$\n\n"
                "where $E_k = \\frac{1}{2}mv^2$ represents the non-relativistic kinetic energy. "
                "For a charged particle carrying electrostatic charge $q$ accelerated from rest across an electric potential difference $V$, the work done by the field equals the acquired kinetic energy $E_k = qV$. "
                "Substituting this into the matter wave relation yields the fundamental accelerating-voltage expression:\n\n"
                "$$\\lambda = \\frac{h}{\\sqrt{2m q V}}$$\n\n"
                "Specializing this formula to an electron with rest mass $m_e = 9.109 \\times 10^{-31}\\text{ kg}$ and elementary charge $e = 1.602 \\times 10^{-19}\\text{ C}$ produces the canonical engineering relation:\n\n"
                "$$\\lambda_e = \\frac{6.626 \\times 10^{-34}}{\\sqrt{2 \\times (9.109 \\times 10^{-31}) \\times (1.602 \\times 10^{-19}) \\times V}} = \\frac{1.227}{\\sqrt{V}}\\text{ nm} = \\frac{12.27}{\\sqrt{V}}\\text{ \\AA}$$\n\n"
                "For accelerating voltages between 50 V and 150 V, electron matter wavelengths span $0.1\\text{ to }0.17\\text{ nm}$, which is precisely commensurate with interatomic crystal lattice constants."
            )
        else:
            paragraphs.append(
                "Matter waves, or de Broglie waves, possess fundamental physical characteristics that distinguish them sharply from classical acoustic or electromagnetic waves. "
                "First, matter waves are not mechanical elastic disturbances propagating through an elastic medium, nor are they transverse vector oscillations of electromagnetic fields. "
                "Instead, as Max Born demonstrated, matter waves represent complex probability amplitude fields whose modulus squared $|\\Psi(\\mathbf{r}, t)|^2$ dictates the spatial probability density "
                "of finding the particle within a differential volume element $d^3r$."
            )
            paragraphs.append(
                "Second, the matter wavelength associated with macroscopic bodies is exceedingly small due to the infinitesimal magnitude of Planck's constant $h \\approx 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$. "
                "For instance, a 100-gram projectile traveling at 100 m/s exhibits a de Broglie wavelength on the order of $\\lambda = 10^{-34}\\text{ m}$, which is approximately twenty orders of magnitude smaller "
                "than the diameter of an atomic nucleus, rendering quantum interference utterly unobservable in everyday classical mechanics. "
                "Only in the microscopic atomic and subatomic domain do matter waves manifest measurable diffraction patterns, underpinning modern technologies such as transmission electron microscopy."
            )

    # Priority 3: Wave Nature of Particles / Duality
    elif "wave nature" in t_low or "matter wave" in t_low:
        if any(k in s_low for k in ["davisson", "germer", "experiment"]):
            paragraphs.append(
                "The definitive empirical confirmation of matter waves was achieved in 1927 by Clinton Davisson and Lester Germer at Bell Telephone Laboratories. "
                "Their experimental apparatus consisted of a heated tungsten filament electron gun inside a high-vacuum chamber, an accelerating electrostatic anode, "
                "and an oriented target nickel single crystal. A collimated beam of electrons accelerated through potential difference $V$ was directed normally onto the target, "
                "and the spatial distribution of elastically scattered electrons was recorded using a movable electrostatic Faraday collector connected to a sensitive galvanometer."
            )
            paragraphs.append(
                "Davisson and Germer observed that for an accelerating potential of $V = 54\\text{ V}$, a prominent scattering intensity peak emerged at an azimuth angle of $\\phi = 50^\\circ$. "
                "Treating the target single crystal as a three-dimensional diffraction grating with Bragg lattice interplanar spacing $d = 0.091\\text{ nm}$, "
                "they applied Bragg's diffraction law $2d\\sin\\theta = n\\lambda$ to the glancing angle $\\theta = 90^\\circ - 50^\\circ/2 = 65^\\circ$ (or equivalently across surface planes $D\\sin\\phi = n\\lambda$ where $D = 0.215\\text{ nm}$):\n\n"
                "$$\\lambda_{exp} = D \\sin(50^\\circ) = (0.215\\text{ nm})(0.766) = 0.165\\text{ nm}$$\n\n"
                "Comparing this measurement against de Broglie's theoretical prediction $\\lambda = \\frac{1.227}{\\sqrt{54}}\\text{ nm} = 0.167\\text{ nm}$ revealed extraordinary agreement within 1.2%, "
                "conclusively establishing that moving electrons possess an authentic spatial wave character governed by diffraction and constructive interference."
            )
        else:
            paragraphs.append(
                "Wave-particle duality represents the foundational principle asserting that physical entities exhibit both corpuscular and wave characteristics "
                "depending upon the nature of the experimental apparatus used to observe them. In classical macroscopic physics, mass particles possess definite coordinates $\\mathbf{r}(t)$ "
                "and momenta $\\mathbf{p}(t)$ that trace out continuous deterministic trajectories through phase space. "
                "Waves, conversely, are extended spatial disturbances characterized by wavelength $\\lambda$, frequency $\\nu$, phase velocity $v_p$, and the capacity for mutual superposition, "
                "diffraction, and constructive or destructive interference."
            )
            paragraphs.append(
                "In quantum theory, radiation and material particles are unified under a common mathematical description. "
                "When radiation propagates through space or interacts with apertures comparable in dimension to its wavelength, it manifests wave phenomena such as interference and diffraction. "
                "However, when exchanging energy and momentum with matter during atomic absorption, photo-emission, or Compton scattering, radiation acts as an ensemble of localized photons. "
                "Conversely, electrons, protons, and neutrons propagate as coherent matter waves described by complex probability amplitudes, but deposit discrete localized charge and mass upon detection screens."
            )

    # Priority 4: Phase Velocity and Group Velocity
    elif "phase" in t_low or "group" in t_low or "velocity" in t_low:
        if "group" in s_low or "packet" in s_low:
            paragraphs.append(
                "Because a purely monochromatic infinite plane wave $\\psi(x, t) = A e^{i(kx - \\omega t)}$ extends uniformly from $-\\infty$ to $+\\infty$, "
                "it provides zero spatial localization and cannot represent a physical particle confined within a finite region of space. "
                "To represent a localized particle, quantum mechanics employs a wave packet synthesized from a continuous Fourier superposition of plane waves "
                "spanning a narrow spectrum of frequencies $\\omega(k)$ and wavenumbers $k$:\n\n"
                "$$\\Psi(x, t) = \\frac{1}{\\sqrt{2\\pi}} \\int_{-\\infty}^{\\infty} A(k) e^{i(kx - \\omega(k) t)} dk$$"
            )
            paragraphs.append(
                "By expanding the dispersion relation $\\omega(k)$ in a Taylor series about the central wavenumber $k_0$, $\\omega(k) \\approx \\omega_0 + \\left(\\frac{d\\omega}{dk}\\right)_{k_0}(k - k_0)$, "
                "the wavepacket resolves into a high-frequency carrier wave modulated by a slowly varying spatial envelope. "
                "The modulation envelope propagates at the group velocity $v_g = \\frac{d\\omega}{dk}$. "
                "Using the de Broglie quantum relations $E = \\hbar\\omega$ and $p = \\hbar k$, we evaluate the group velocity directly:\n\n"
                "$$v_g = \\frac{d\\omega}{dk} = \\frac{d(E/\\hbar)}{d(p/\\hbar)} = \\frac{dE}{dp}$$\n\n"
                "For a non-relativistic classical particle of mass $m$ with kinetic energy $E = \\frac{p^2}{2m}$, differentiating yields $v_g = \\frac{d}{dp}\\left(\\frac{p^2}{2m}\\right) = \\frac{p}{m} = v_{particle}$. "
                "In relativistic mechanics where $E^2 = p^2 c^2 + m_0^2 c^4$, implicit differentiation yields $2E \\frac{dE}{dp} = 2pc^2 \\implies v_g = \\frac{pc^2}{E} = \\frac{(\\gamma m_0 v)c^2}{\\gamma m_0 c^2} = v_{particle}$. "
                "This fundamental mathematical identity proves that the group velocity of the quantum wavepacket envelope identically equals the physical translational velocity of the material particle."
            )
        else:
            paragraphs.append(
                "When harmonic waves propagate through any physical medium, phase velocity $v_p$ defines the speed at which individual surfaces of constant phase (wavefronts) advance. "
                "For an individual plane wave component described by harmonic function $\\cos(kx - \\omega t)$, setting the phase argument constant ($kx - \\omega t = \\text{const}$) "
                "and taking the time derivative yields the canonical phase velocity definition: $v_p = \\frac{\\omega}{k} = \\nu \\lambda$."
            )
            paragraphs.append(
                "For a de Broglie matter wave in vacuum, substituting Einstein's total energy $E = mc^2 = \\hbar\\omega$ and momentum $p = mv = \\hbar k$ produces a startling classical paradox:\n\n"
                "$$v_p = \\frac{\\omega}{k} = \\frac{E}{p} = \\frac{mc^2}{mv} = \\frac{c^2}{v}$$\n\n"
                "Because physical particle velocities are strictly subluminal ($v < c$), the phase velocity of a matter wave is strictly superluminal ($v_p > c$). "
                "This superluminal velocity does not violate Einstein's special relativity because an individual monochromatic wavefront of infinite extent carries zero localized energy or physical signal. "
                "The relationship between group velocity and phase velocity is governed by Rayleigh's dispersion formula: $v_g = v_p + k\\frac{dv_p}{dk} = v_p - \\lambda \\frac{dv_p}{d\\lambda}$. "
                "In non-dispersive media $dv_p/d\\lambda = 0$, so $v_g = v_p$; however, matter waves in vacuum are inherently dispersive ($v_p = v/2$ non-relativistically), mandating wavepacket analysis."
            )

    # Priority 5: Heisenberg Uncertainty Principle
    elif "uncertainty" in t_low or "heisenberg" in t_low:
        if "implication" in s_low or "physical" in s_low or "consequence" in s_low:
            paragraphs.append(
                "The Heisenberg uncertainty principle entails profound physical implications that permanently dismantle classical determinism in the microscopic realm. "
                "In classical mechanics, Laplace determinism asserted that precise knowledge of initial coordinates $\\mathbf{r}(0)$ and velocities $\\mathbf{v}(0)$ "
                "uniquely determines the entire future and past trajectories of a physical system. "
                "In quantum mechanics, because canonically conjugate operators do not commute ($[\\hat{x}, \\hat{p}_x] = i\\hbar$), it is mathematically impossible "
                "to simultaneously prepare a quantum state with vanishing variances in both coordinate and momentum."
            )
            paragraphs.append(
                "A foundational physical consequence is the impossibility of an electron residing permanently inside an atomic nucleus. "
                "Because atomic nuclei have characteristic radii of $R \\approx 10^{-14}\\text{ m}$, any electron confined within a nucleus would have a maximum position uncertainty "
                "$\\Delta x \\approx 2 \\times 10^{-14}\\text{ m}$. Applying the uncertainty relation yields a minimum momentum uncertainty $\\Delta p \\ge \\frac{\\hbar}{2\\Delta x} \\approx 2.64 \\times 10^{-21}\\text{ kg}\\cdot\\text{m/s}$. "
                "Evaluating the corresponding relativistic kinetic energy $E \\approx pc$ reveals an energy exceeding $15\\text{ to }20\\text{ MeV}$. "
                "Because beta-decay emission energies rarely exceed $2\\text{ to }3\\text{ MeV}$, electrons cannot pre-exist within the nucleus as constituent entities, "
                "demonstrating that beta particles are synthesized dynamically at the instant of radioactive decay."
            )
        else:
            paragraphs.append(
                "Formulated by Werner Heisenberg in 1927, the uncertainty principle represents an inherent mathematical property of wave mechanics rather than a limitation of measurement technology. "
                "Any localized spatial state is represented by a wavepacket synthesized from a continuous Fourier superposition of plane waves: $\\psi(x) = \\frac{1}{\\sqrt{2\\pi}}\\int A(k)e^{ikx}dk$. "
                "According to the classical Fourier bandwidth theorem, the effective spatial width $\\Delta x$ and the wavenumber spread $\\Delta k$ satisfy the reciprocal inequality "
                "$\\Delta x \\cdot \\Delta k \\ge \\frac{1}{2}$."
            )
            paragraphs.append(
                "Multiplying this fundamental wave inequality by the reduced Planck constant $\\hbar$ and identifying the physical particle momentum as $p_x = \\hbar k$ "
                "yields the celebrated Heisenberg position-momentum uncertainty relation:\n\n"
                "$$\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}$$\n\n"
                "where $\\hbar = \\frac{h}{2\\pi} \\approx 1.055 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$. "
                "In general operator theory, the Robertson-Schrödinger theorem establishes that for any two observable Hermitian operators $\\hat{A}$ and $\\hat{B}$, "
                "their standard deviations satisfy $\\Delta A \\cdot \\Delta B \\ge \\frac{1}{2}|\\langle [\\hat{A}, \\hat{B}] \\rangle|$. "
                "Similarly, the conjugate relationship between energy and time is bounded by $\\Delta E \\cdot \\Delta t \\ge \\frac{\\hbar}{2}$, which governs the natural spectral linewidth "
                "$\\Delta \\nu \\ge \\frac{1}{4\\pi \\tau}$ of excited atomic states with finite radiative lifetime $\\tau$."
            )

    # Priority 6: Linear Operators in Quantum Mechanics
    elif "operator" in t_low:
        if "hamiltonian" in s_low or "momentum" in s_low or "linear" in s_low:
            paragraphs.append(
                "In quantum mechanics, physical observables are mapped exclusively to linear differential or matrix operators acting on state functions in Hilbert space. "
                "Under the Dirac-von Neumann coordinate representation, the classical spatial coordinate $x$ maps to the multiplicative operator $\\hat{x} = x$, "
                "while the linear momentum $p_x$ is represented by the spatial gradient operator:\n\n"
                "$$\\hat{p}_x = -i\\hbar \\frac{\\partial}{\\partial x}$$\n\n"
                "The kinetic energy operator is constructed by squaring the momentum operator: $\\hat{T} = \\frac{\\hat{p}_x^2}{2m} = -\\frac{\\hbar^2}{2m} \\frac{\\partial^2}{\\partial x^2}$."
            )
            paragraphs.append(
                "The total energy observable corresponds to the Hamiltonian operator $\\hat{H}$, which sums the kinetic and potential energy operators:\n\n"
                "$$\\hat{H} = \\hat{T} + \\hat{V} = -\\frac{\\hbar^2}{2m}\\nabla^2 + V(\\mathbf{r}, t)$$\n\n"
                "Evaluating the commutator between the fundamental position and momentum operators across an arbitrary test wave function $\\psi(x)$ demonstrates that:\n\n"
                "$$[\\hat{x}, \\hat{p}_x]\\psi = x\\left(-i\\hbar \\frac{\\partial \\psi}{\\partial x}\\right) - \\left(-i\\hbar \\frac{\\partial(x\\psi)}{\\partial x}\\right) = -i\\hbar x\\frac{\\partial\\psi}{\\partial x} + i\\hbar x\\frac{\\partial\\psi}{\\partial x} + i\\hbar\\psi = i\\hbar\\psi$$\n\n"
                "Because $[\\hat{x}, \\hat{p}_x] = i\\hbar \\ne 0$, position and momentum are mutually non-commuting, incompatible observables, mathematically generating the Heisenberg uncertainty relation."
            )
        else:
            paragraphs.append(
                "An operator $\\hat{A}$ in quantum mechanics is defined as an operational rule that transforms a state vector $\\psi$ into another vector $\\psi'$. "
                "Physical consistency requires operators representing observables to satisfy linearity: $\\hat{A}(c_1\\psi_1 + c_2\\psi_2) = c_1\\hat{A}\\psi_1 + c_2\\hat{A}\\psi_2$ for any complex scalars $c_1, c_2$. "
                "Furthermore, because the expectation value $\\langle A \\rangle = \\int \\psi^* \\hat{A} \\psi dx$ corresponds to the statistical mean of actual experimental meter readings, "
                "expectation values must be strictly real numbers ($\\langle A \\rangle^* = \\langle A \\rangle$)."
            )
            paragraphs.append(
                "This physical reality mandate requires observable operators to be Hermitian (self-adjoint), satisfying the inner-product condition "
                "$\\langle \\psi_1 | \\hat{A} \\psi_2 \\rangle = \\langle \\hat{A} \\psi_1 | \\psi_2 \\rangle$, or in integral notation: "
                "$\\int \\psi_1^* (\\hat{A}\\psi_2) dx = \\int (\\hat{A}\\psi_1)^* \\psi_2 dx$. "
                "According to Ehrenfest's theorem, the time rate of change of an expectation value is governed by $\\frac{d\\langle A \\rangle}{dt} = \\frac{i}{\\hbar}\\langle [\\hat{H}, \\hat{A}] \\rangle + \\langle \\frac{\\partial\\hat{A}}{\\partial t}\\rangle$. "
                "Consequently, any observable whose operator commutes with the Hamiltonian and lacks explicit time dependence represents a strictly conserved physical quantity."
            )

    # Priority 7: Eigenvalues and Eigenfunctions
    elif "eigen" in t_low:
        if "orthogonality" in s_low or requires_derivation:
            paragraphs.append(
                "The mathematical proof establishing that eigenfunctions corresponding to distinct eigenvalues of a Hermitian operator are mutually orthogonal proceeds as follows. "
                "Let $\\hat{A}$ be a Hermitian operator with two eigenstates $\\psi_m$ and $\\psi_n$ satisfying the eigenvalue equations "
                "$\\hat{A}\\psi_m = a_m\\psi_m$ and $\\hat{A}\\psi_n = a_n\\psi_n$, where $a_m$ and $a_n$ are distinct real eigenvalues ($a_m \\ne a_n$). "
                "Evaluating the inner product $\\int \\psi_m^* (\\hat{A}\\psi_n) dx = a_n \\int \\psi_m^* \\psi_n dx$."
            )
            paragraphs.append(
                "Applying the definition of operator Hermiticity, the left-hand integral can be rewritten as $\\int (\\hat{A}\\psi_m)^* \\psi_n dx = \\int (a_m\\psi_m)^* \\psi_n dx = a_m \\int \\psi_m^* \\psi_n dx$, "
                "since the eigenvalue $a_m$ is guaranteed to be real ($a_m^* = a_m$). "
                "Subtracting the two inner product relations yields:\n\n"
                "$$(a_m - a_n) \\int_{-\\infty}^\\infty \\psi_m^*(x) \\psi_n(x) dx = 0$$\n\n"
                "Because we stipulated that $a_m \\ne a_n$, the scalar factor $(a_m - a_n)$ is non-zero, requiring that the spatial integral vanish identically:\n\n"
                "$$\\int_{-\\infty}^\\infty \\psi_m^*(x) \\psi_n(x) dx = 0 \\quad \\text{for } m \\ne n$$\n\n"
                "Combined with unit normalization $\\int |\\psi_n|^2 dx = 1$, the eigenstates satisfy the orthonormality relation $\\int \\psi_m^* \\psi_n dx = \\delta_{mn}$, "
                "forming a complete basis spanning the entire Hilbert space."
            )
        else:
            paragraphs.append(
                "The quantum eigenvalue equation $\\hat{A}\\psi_n = a_n\\psi_n$ represents the central measurement postulate of quantum mechanics. "
                "When an operator $\\hat{A}$ acts upon a special state function $\\psi_n$ (an eigenfunction), it reproduces the same state function scaled by a numerical constant $a_n$ (the eigenvalue). "
                "According to the Dirac-von Neumann measurement postulate, the only allowable outcomes of a physical measurement of observable $A$ are the discrete eigenvalues $a_n$ of its operator $\\hat{A}$."
            )
            paragraphs.append(
                "When a quantum system is prepared in an arbitrary normalized state $\\Psi(x)$, the completeness of the orthonormal eigenbasis $\\{\\psi_n\\}$ allows $\\Psi$ to be expanded uniquely as "
                "$\\Psi(x) = \\sum_{n} c_n \\psi_n(x)$, where the expansion coefficients are given by the projection inner product $c_n = \\int \\psi_n^*(x) \\Psi(x) dx$. "
                "The probability of obtaining measurement result $a_n$ is given by Born's rule: $P(a_n) = |c_n|^2 = |\\langle \\psi_n | \\Psi \\rangle|^2$. "
                "Immediately following the measurement, the state function collapses instantaneously from the superposition $\\Psi$ into the specific eigenstate $\\psi_n$ corresponding to the detected eigenvalue."
            )

    # Priority 8: Time-Dependent Schrödinger Equation
    elif "time-dependent" in t_low or "tdse" in t_low:
        if "continuity" in s_low or "current" in s_low:
            paragraphs.append(
                "The Time-Dependent Schrödinger Equation guarantees the local conservation of probability throughout space, which is formalized by the quantum continuity equation. "
                "Starting from the TDSE $i\\hbar \\frac{\\partial\\Psi}{\\partial t} = -\\frac{\\hbar^2}{2m}\\nabla^2\\Psi + V\\Psi$ and its complex conjugate "
                "$-i\\hbar \\frac{\\partial\\Psi^*}{\\partial t} = -\\frac{\\hbar^2}{2m}\\nabla^2\\Psi^* + V\\Psi^*$ (for real potential $V$), "
                "we evaluate the time derivative of the probability density $P(\\mathbf{r}, t) = \\Psi^*\\Psi$:\n\n"
                "$$\\frac{\\partial P}{\\partial t} = \\Psi^* \\frac{\\partial\\Psi}{\\partial t} + \\Psi \\frac{\\partial\\Psi^*}{\\partial t} = \\frac{1}{i\\hbar}\\left[ \\Psi^*\\left(-\\frac{\\hbar^2}{2m}\\nabla^2\\Psi + V\\Psi\\right) - \\Psi\\left(-\\frac{\\hbar^2}{2m}\\nabla^2\\Psi^* + V\\Psi^*\\right) \\right]$$"
            )
            paragraphs.append(
                "The potential energy terms $V|\\Psi|^2$ cancel identically, leaving $\\frac{\\partial P}{\\partial t} = -\\frac{\\hbar}{2mi} [\\Psi^*\\nabla^2\\Psi - \\Psi\\nabla^2\\Psi^*] = -\\nabla \\cdot \\left[ \\frac{\\hbar}{2mi}(\\Psi^*\\nabla\\Psi - \\Psi\\nabla\\Psi^*) \\right]$. "
                "By defining the probability current density vector $\\mathbf{J}(\\mathbf{r}, t)$ as:\n\n"
                "$$\\mathbf{J}(\\mathbf{r}, t) = \\frac{\\hbar}{2mi}\\left( \\Psi^* \\nabla\\Psi - \\Psi \\nabla\\Psi^* \\right) = \\frac{\\hbar}{m}\\text{Im}(\\Psi^* \\nabla\\Psi)$$\n\n"
                "we obtain the exact differential continuity equation:\n\n"
                "$$\\frac{\\partial P}{\\partial t} + \\nabla \\cdot \\mathbf{J} = 0$$\n\n"
                "Integrating this equation over all space and applying Gauss's divergence theorem confirms that the total integrated probability $\\int_{-\\infty}^\\infty |\\Psi|^2 d^3r = 1$ is rigorously conserved in time."
            )
        else:
            paragraphs.append(
                "In 1926, Erwin Schrödinger published his wave equation, which governs the dynamical time evolution of non-relativistic quantum states. "
                "To formulate the wave equation, Schrödinger sought a linear partial differential equation consistent with de Broglie's relations $E = \\hbar\\omega$ and $p = \\hbar k$, "
                "and with the classical total energy conservation relation $E = \\frac{p^2}{2m} + V(x, t)$."
            )
            paragraphs.append(
                "Associating physical observables with differential operators—specifically the energy operator $\\hat{E} = i\\hbar \\frac{\\partial}{\\partial t}$ and momentum operator $\\hat{p} = -i\\hbar \\nabla$—the "
                "Hamiltonian operator becomes $\\hat{H} = -\\frac{\\hbar^2}{2m}\\nabla^2 + V(\\mathbf{r}, t)$. "
                "Equating $\\hat{E}\\Psi = \\hat{H}\\Psi$ produces the canonical Time-Dependent Schrödinger Equation (TDSE):\n\n"
                "$$i\\hbar \\frac{\\partial \\Psi(\\mathbf{r}, t)}{\\partial t} = -\\frac{\\hbar^2}{2m}\\nabla^2\\Psi(\\mathbf{r}, t) + V(\\mathbf{r}, t)\\Psi(\\mathbf{r}, t)$$\n\n"
                "Because the time derivative appears to first order, specifying an initial wave function $\\Psi(\\mathbf{r}, 0)$ uniquely and deterministically fixes the state vector at all subsequent times $t > 0$ "
                "via the unitary time-evolution operator $\\hat{U}(t, 0) = \\exp(-i\\hat{H}t/\\hbar)$."
            )

    # Priority 9: Time-Independent Schrödinger Equation / Stationary States
    elif "time-independent" in t_low or "tise" in t_low or "stationary" in t_low:
        if "separation" in s_low or requires_derivation:
            paragraphs.append(
                "When the external potential energy field is stationary in time ($V(\\mathbf{r}, t) = V(\\mathbf{r})$), the partial differential TDSE can be separated into spatial and temporal components "
                "using the method of separation of variables. Assuming a product solution of the form $\\Psi(\\mathbf{r}, t) = \\psi(\\mathbf{r}) \\phi(t)$, "
                "substituting into the TDSE yields:\n\n"
                "$$i\\hbar \\psi(\\mathbf{r}) \\frac{d\\phi(t)}{dt} = \\phi(t) \\left[ -\\frac{\\hbar^2}{2m}\\nabla^2\\psi(\\mathbf{r}) + V(\\mathbf{r})\\psi(\\mathbf{r}) \\right]$$"
            )
            paragraphs.append(
                "Dividing both sides by $\\Psi(\\mathbf{r}, t) = \\psi(\\mathbf{r})\\phi(t)$ isolates the purely temporal function on the left and the purely spatial function on the right:\n\n"
                "$$\\frac{i\\hbar}{\\phi(t)} \\frac{d\\phi(t)}{dt} = \\frac{1}{\\psi(\\mathbf{r})} \\left[ -\\frac{\\hbar^2}{2m}\\nabla^2\\psi(\\mathbf{r}) + V(\\mathbf{r})\\psi(\\mathbf{r}) \\right] = E$$\n\n"
                "Because the left side depends solely on $t$ and the right side solely on $\\mathbf{r}$, both must equal a common separation constant $E$, representing the total energy eigenvalue. "
                "The temporal equation integrates immediately to $\\phi(t) = \\exp(-iEt/\\hbar)$, while the spatial equation yields the Time-Independent Schrödinger Equation (TISE):\n\n"
                "$$-\\frac{\\hbar^2}{2m}\\nabla^2\\psi(\\mathbf{r}) + V(\\mathbf{r})\\psi(\\mathbf{r}) = E\\psi(\\mathbf{r}) \\implies \\hat{H}\\psi = E\\psi$$\n\n"
                "The spatial eigenfunctions $\\psi_n(\\mathbf{r})$ determine the stationary wave functions whose probability densities $|\\Psi(\\mathbf{r}, t)|^2 = |\\psi(\\mathbf{r})|^2$ remain strictly time-invariant."
            )
        else:
            paragraphs.append(
                "Stationary states in quantum mechanics correspond to solutions of the time-independent Schrödinger equation possessing definite energy eigenvalues $E_n$. "
                "The complete space-time wave function for a stationary state is given by $\\Psi_n(\\mathbf{r}, t) = \\psi_n(\\mathbf{r}) e^{-iE_n t / \\hbar}$. "
                "Evaluating the spatial probability density reveals that the complex temporal exponential phase cancels identically: "
                "$P(\\mathbf{r}, t) = |\\Psi_n(\\mathbf{r}, t)|^2 = \\psi_n^*(\\mathbf{r}) e^{iE_n t / \\hbar} \\psi_n(\\mathbf{r}) e^{-iE_n t / \\hbar} = |\\psi_n(\\mathbf{r})|^2$."
            )
            paragraphs.append(
                "Because the probability density is entirely independent of time, all expectation values of time-independent observables $\\langle A \\rangle = \\int \\Psi_n^* \\hat{A} \\Psi_n d^3r = \\int \\psi_n^* \\hat{A} \\psi_n d^3r$ "
                "remain strictly constant in stationary states. "
                "Furthermore, to qualify as physically admissible stationary states, solutions $\\psi(\\mathbf{r})$ must satisfy the standard Dirichlet-Neumann boundary conditions: "
                "the wave function must be single-valued, continuous everywhere, possess continuous first derivatives wherever $V(\\mathbf{r})$ is finite, and be square-integrable over all space."
            )

    # Priority 10: Introduction / Planck / Blackbody Radiation
    elif "intro" in t_low or "planck" in t_low or "blackbody" in t_low or "photoelectric" in t_low:
        if "planck" in s_low or "blackbody" in s_low or "postulate" in s_low:
            paragraphs.append(
                "The conceptual genesis of quantum theory was precipitated by the spectacular breakdown of nineteenth-century classical physics "
                "when applied to thermal cavity radiation. Classical electrodynamics and the equipartition theorem, formulated by Rayleigh and Jeans, "
                "predicted that the spectral energy density of a blackbody cavity should scale as $u(\\nu)d\\nu = \\frac{8\\pi\\nu^2}{c^3} k_B T d\\nu$. "
                "This classical distribution diverged catastrophically at high ultraviolet frequencies—a dilemma historically termed the 'ultraviolet catastrophe'—and "
                "implied the physically absurd result that any thermal cavity should radiate infinite energy."
            )
            paragraphs.append(
                "In December 1900, Max Planck resolved this crisis by introducing a radical mathematical hypothesis: physical material oscillators "
                "lining the cavity walls cannot absorb or emit radiant energy continuously. Instead, atomic oscillators exchange energy exclusively in discrete, "
                "indivisible energy packets termed quanta, governed by the Planck postulate:\n\n"
                "$$E = n h \\nu = n \\hbar \\omega, \\quad n = 0, 1, 2, \\dots$$\n\n"
                "where $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ represents Planck's constant and $\\nu$ denotes the oscillation frequency. "
                "By replacing the continuous Boltzmann integral over phase space with a discrete sum over quantized states, Planck evaluated the average oscillator energy as "
                "$\\langle E \\rangle = \\frac{\\sum_{n=0}^\\infty n h\\nu e^{-n h\\nu / k_B T}}{\\sum_{n=0}^\\infty e^{-n h\\nu / k_B T}} = \\frac{h\\nu}{e^{h\\nu / k_B T} - 1}$, "
                "directly yielding the celebrated Planck radiation distribution:\n\n"
                "$$u(\\nu)d\\nu = \\frac{8\\pi h \\nu^3}{c^3} \\frac{1}{e^{h\\nu / k_B T} - 1} d\\nu$$\n\n"
                "In the low-frequency limit ($h\\nu \\ll k_B T$), expanding the exponential $e^{h\\nu/k_BT} \\approx 1 + h\\nu/k_BT$ smoothly recovers the Rayleigh-Jeans law, "
                "while in the high-frequency regime ($h\\nu \\gg k_B T$), the exponential term dominates and produces Wien's displacement distribution, establishing quantum physics."
            )
        else:
            paragraphs.append(
                "The classical worldview developed throughout the seventeenth through nineteenth centuries rested upon two immutable pillars: "
                "Newtonian particle mechanics, which governed localized discrete bodies possessing definite spatial trajectories, and Maxwellian electrodynamics, "
                "which described continuous electromagnetic wave propagation across space. "
                "However, by the turn of the twentieth century, pioneering experiments probing atomic and subatomic phenomena revealed that this rigid classical dichotomy "
                "was fundamentally untenable. Phenomenological anomalies such as blackbody spectral distribution, the photoelectric effect, and discrete atomic emission spectra "
                "demanded a revolutionary framework capable of unifying discrete corpuscular behaviors with continuous wave dynamics."
            )
            paragraphs.append(
                "In 1905, Albert Einstein extended Planck's radiation hypothesis by postulating that electromagnetic radiation does not merely exchange energy in discrete amounts "
                "at cavity walls, but propagates through vacuum as localized packets of energy, later termed photons. "
                "When a monochromatic photon of energy $h\\nu$ strikes a metallic surface, its energy is transferred instantaneously to an electron, satisfying the Einstein photoelectric equation "
                "$h\\nu = W_0 + \\frac{1}{2}m v_{max}^2$, where $W_0 = h\\nu_0$ is the characteristic work function of the material. "
                "This insight proved that light manifests localized particle-like momentum $p = h/\\lambda$, initiating the profound paradigm shift toward modern quantum mechanics."
            )

    # Priority 11: Applications / Tunneling
    elif "tunnel" in t_low or "barrier" in t_low or "application" in t_low:
        paragraphs.append(
            "Quantum tunneling represents one of the most striking physical departures from classical mechanics, wherein a microscopic particle possesses a finite, "
            "non-zero transmission probability across a potential energy barrier whose height $V_0$ strictly exceeds the total energy $E$ of the particle ($E < V_0$). "
            "In classical mechanics, a particle encountering a potential hill higher than its total energy is completely reflected because the kinetic energy would become negative ($T = E - V_0 < 0$). "
            "In quantum mechanics, solving the time-independent Schrödinger equation across a finite barrier of thickness $a$ reveals that the wave function decays exponentially as an evanescent wave "
            "$\\psi(x) \\propto e^{-\\kappa x}$ inside the barrier, where the attenuation constant is $\\kappa = \\frac{\\sqrt{2m(V_0 - E)}}{\\hbar}$."
        )
        paragraphs.append(
            "Matching wave functions and their spatial derivatives at both barrier interfaces yields the celebrated transmission coefficient (tunneling probability):\n\n"
            "$$T \\approx 16 \\frac{E}{V_0} \\left(1 - \\frac{E}{V_0}\\right) e^{-2\\kappa a} = 16 \\frac{E}{V_0} \\left(1 - \\frac{E}{V_0}\\right) \\exp\\left( -\\frac{2a}{\\hbar} \\sqrt{2m(V_0 - E)} \\right)$$\n\n"
            "Because the transmission coefficient decays exponentially with barrier width $a$, tunneling is exquisitely sensitive to sub-angstrom spatial variations. "
            "This physical principle forms the operational foundation of the Scanning Tunneling Microscope (STM), developed by Gerd Binnig and Heinrich Rohrer, "
            "which measures tunneling current variations between an atom-sharp metallic tip and a conducting surface to achieve atomic-resolution surface topography."
        )

    # Fallback: check subtopic keywords or generate authentic quantum prose
    else:
        if "box" in s_low or "well" in s_low:
            return generate_quantum_prose("Particle in a 1D Box", subtopic, requires_derivation)
        elif "broglie" in s_low or "matter wave" in s_low:
            return generate_quantum_prose("de Broglie Hypothesis", subtopic, requires_derivation)
        elif "uncertainty" in s_low or "heisenberg" in s_low:
            return generate_quantum_prose("Heisenberg Uncertainty Principle", subtopic, requires_derivation)
        elif "operator" in s_low or "eigen" in s_low:
            return generate_quantum_prose("Operators in Quantum Mechanics", subtopic, requires_derivation)
        else:
            paragraphs.append(
                f"The theoretical analysis of {subtopic} within {topic} occupies a central role in modern quantum physics. "
                "Microscopic physical systems are described by state functions $\\Psi(\\mathbf{r}, t)$ evolving in complex Hilbert space, "
                "where dynamical observables correspond to linear Hermitian operators satisfying canonical commutation relations."
            )
            paragraphs.append(
                "By solving the governing wave equations subject to physical Dirichlet-Neumann boundary conditions, "
                "the discrete eigenvalue spectrum and stationary eigenfunctions can be derived analytically. "
                "These foundational quantum mechanical principles provide the quantitative framework for modern solid-state electronics, "
                "quantum optics, and nanoscale device engineering."
            )

    return paragraphs

    return paragraphs


def generate_wave_optics_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Wave Optics topics."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    if "intro" in t_low or "theory of light" in s_low or "huygens" in s_low:
        if "huygens" in s_low:
            paragraphs.append(
                "In 1678, Christian Huygens proposed the wave theory of light, establishing the geometric wave construction principle that bears his name. "
                "Huygens' principle asserts that every point on an advancing primary wavefront acts as a fresh source of secondary spherical wavelets "
                "that spread out in all directions with the characteristic phase velocity of the wave in that medium. "
                "The new position of the wavefront at any subsequent instant is defined by the geometric forward envelope (tangential surface) touching all these secondary wavelets."
            )
            paragraphs.append(
                "Applying Huygens' wave construction to a plane wavefront incident obliquely upon a plane boundary between two media of refractive indices "
                "$n_1$ and $n_2$ rigorously derives the fundamental laws of geometric optics from wave principles. "
                "Let a plane wavefront $AB$ strike the interface at angle of incidence $i$. As point $B$ travels distance $BC = v_1 t$ in medium 1, "
                "the secondary wavelet from point $A$ expands across distance $AD = v_2 t$ in medium 2. "
                "Drawing tangent $CD$ defines the refracted wavefront. From the geometry of right triangles $\\Delta ABC$ and $\\Delta ADC$ with common hypotenuse $AC$:\n\n"
                "$$\\sin i = \\frac{BC}{AC} = \\frac{v_1 t}{AC}, \\quad \\sin r = \\frac{AD}{AC} = \\frac{v_2 t}{AC}$$\n\n"
                "Dividing the two relations yields Snell's law of refraction:\n\n"
                "$$\\frac{\\sin i}{\\sin r} = \\frac{v_1}{v_2} = \\frac{c / n_1}{c / n_2} = \\frac{n_2}{n_1} = \\mu$$\n\n"
                "This wave-theoretical derivation demonstrated that light travels slower in optically denser media ($v_2 < v_1$ when $n_2 > n_1$), "
                "directly contradicting Newton's corpuscular model which had incorrectly predicted faster velocities in denser media."
            )
        else:
            paragraphs.append(
                "The historical development of optical physics witnessed a protracted debate between Isaac Newton's corpuscular theory "
                "and Christian Huygens' wave theory. Newton posited that light consists of microscopic material corpuscles emitted by luminous bodies, "
                "which explained rectilinear propagation and sharp geometric shadows. However, the corpuscular theory struggled to explain partial reflection, "
                "refraction into denser media without acceleration, and the non-scattering crossing of light beams."
            )
            paragraphs.append(
                "The wave theory emerged triumphant in the early nineteenth century through the pioneering experiments of Thomas Young and Augustin-Jean Fresnel. "
                "Fresnel synthesized Huygens' wavelet construction with the principle of mutual wave interference, creating the Huygens-Fresnel wave theory. "
                "This unified framework proved that light propagation is governed by harmonic scalar and vector fields, and that classical rectilinear propagation "
                "is merely an asymptotic limiting case when the optical aperture dimensions are vastly larger than the optical wavelength ($\\lambda \\ll D$)."
            )

    elif "interference" in t_low or "superposition" in s_low or "conditions" in s_low:
        if "superposition" in s_low or requires_derivation:
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
        else:
            paragraphs.append(
                "To observe stable, high-contrast, stationary optical interference fringes, the interfering light waves must satisfy four rigorous conditions: "
                "1. **Coherence:** The phase difference $\\delta$ between the interfering sources must remain strictly invariant over the observation time interval. "
                "Independent thermal light sources undergo random phase jumps every $10^{-9}\\text{ to }10^{-10}\\text{ seconds}$, causing rapid intensity fluctuations that average out to uniform illumination $I = I_1 + I_2$ unless derived from a common wavefront or laser oscillator."
            )
            paragraphs.append(
                "2. **Monochromaticity:** The light sources must emit radiation over a vanishingly narrow frequency band $\\Delta\\nu \\approx 0$. If polychromatic white light is used, "
                "different spectral wavelengths produce overlapping fringe patterns of varying spatial widths, washing out the pattern after only a few central colored fringes.\n"
                "3. **Equal or Comparable Amplitudes:** High fringe contrast (visibility $V = \\frac{I_{max} - I_{min}}{I_{max} + I_{min}}$) requires $a_1 \\approx a_2$. When amplitudes are equal, $I_{min} = 0$ and fringe visibility reaches unity ($V = 1$).\n"
                "4. **State of Polarization:** The interfering waves must oscillate in identical states of polarization. As established by the Fresnel-Arago laws, light waves polarized in mutually orthogonal planes cannot interfere to produce spatial intensity modulation."
            )

    elif "coherent" in t_low or "coherence" in s_low:
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
                "remains mutually coherent only if the path difference from opposite edges of the source to the aperture points is less than half a wavelength: "
                "$w \\cdot \\frac{d}{D} \\le \\frac{\\lambda}{2}$."
            )
            paragraphs.append(
                "This geometric constraint defines the spatial coherence width $l_s = \\frac{\\lambda D}{2w} = \\frac{\\lambda}{2\\theta}$, "
                "where $\\theta = w/D$ is the angular subtense of the luminous source. "
                "In optical system design, creating coherent secondary sources from thermal emitters requires either division of wavefront "
                "(as in Young's double slit or Fresnel biprism, where two parts of the same wavefront are isolated within the spatial coherence width) "
                "or division of amplitude (as in thin films, Michelson interferometers, or Newton's rings, where partial reflection splits the wave amplitude uniformly across the entire beam)."
            )

    elif "young" in t_low or "double slit" in t_low or "fringe width" in s_low:
        if "derivation" in s_low or "fringe" in s_low or requires_derivation:
            paragraphs.append(
                "In 1801, Thomas Young performed the double-slit experiment that provided the first incontrovertible proof of the wave nature of light. "
                "Consider a monochromatic light source of wavelength $\\lambda$ incident on two narrow parallel slits $S_1$ and $S_2$ separated by a small distance $d$. "
                "The light diffracted by the two slits propagates toward an observation screen placed at a parallel distance $D$ (where $D \\gg d$)."
            )
            paragraphs.append(
                "Let $P$ be a point on the observation screen located at vertical distance $y$ from the central axis. "
                "The path difference $\\Delta$ between the waves arriving at $P$ from slits $S_1$ and $S_2$ is geometrically expressed as:\n\n"
                "$$\\Delta = S_2 P - S_1 P = \\sqrt{D^2 + (y + d/2)^2} - \\sqrt{D^2 + (y - d/2)^2}$$\n\n"
                "Applying the binomial expansion for $D \\gg y$ and $D \\gg d$ simplifies the path difference to the standard approximation:\n\n"
                "$$\\Delta = d \\sin\\theta \\approx d \\tan\\theta = \\frac{y d}{D}$$\n\n"
                "For constructive interference (bright fringes), the path difference must equal an integer number of wavelengths: "
                "$\\Delta = \\frac{y_n d}{D} = n\\lambda \\implies y_n = \\frac{n\\lambda D}{d}$ for $n = 0, \\pm 1, \\pm 2, \\dots$. "
                "For destructive interference (dark fringes), the path difference must equal an odd half-integral number of wavelengths: "
                "$\\Delta = \\frac{y_n' d}{D} = (2n - 1)\\frac{\\lambda}{2} \\implies y_n' = \\left(n - \\frac{1}{2}\\right)\\frac{\\lambda D}{d}$."
            )
            paragraphs.append(
                "The fringe width $\\beta$ is defined as the spatial separation between any two consecutive bright or dark fringes:\n\n"
                "$$\\beta = y_{n+1} - y_n = \\frac{(n+1)\\lambda D}{d} - \\frac{n\\lambda D}{d} = \\frac{\\lambda D}{d}$$\n\n"
                "This fundamental formula demonstrates that fringe spacing $\\beta$ is directly proportional to wavelength $\\lambda$ and screen distance $D$, "
                "and inversely proportional to slit separation $d$. Because all fringe widths are identical, Young's double slit produces an equidistant, "
                "alternating array of bright and dark rectilinear bands across the screen."
            )
        else:
            paragraphs.append(
                "The experimental setup of Young's double-slit experiment was brilliantly designed to overcome the spatial incoherence of thermal light sources. "
                "A primary pinhole slit $S_0$ is illuminated by a monochromatic source, creating a diverging cylindrical wavefront of high spatial coherence. "
                "This single wavefront falls symmetrically upon two closely spaced parallel slits $S_1$ and $S_2$, ensuring that any microscopic phase fluctuations "
                "in the primary emitter affect both secondary slits identically, maintaining a strictly locked phase relationship $\\delta = 0$ between them."
            )
            paragraphs.append(
                "The resulting interference pattern observed on the screen displays high fringe contrast in the central region, "
                "governed by the intensity distribution $I(y) = I_0 \\cos^2\\left(\\frac{\\pi d y}{\\lambda D}\\right)$. "
                "When finite slit widths $a$ are taken into account, the pure two-beam interference pattern is modulated by a single-slit Fraunhofer diffraction envelope "
                "$\\left(\\frac{\\sin\\alpha}{\\alpha}\\right)^2$, causing fringe intensities to decay with distance from the central axis and producing missing orders "
                "wherever an interference maximum coincides with a diffraction minimum ($d/a = n/m$)."
            )

    elif "thin film" in t_low or "reflected" in s_low or "transmitted" in s_low:
        if "reflected" in s_low or requires_derivation:
            paragraphs.append(
                "Interference in thin films occurs by division of amplitude when an incident light wave strikes a parallel-sided transparent film "
                "of thickness $t$ and refractive index $\\mu$. At the upper interface, part of the wave is reflected into the original medium while the remainder "
                "is refracted into the dielectric film at angle of refraction $r$. At the lower interface, the wave undergoes internal reflection, returning to the upper surface "
                "and emerging back into the original medium parallel to the first reflected ray."
            )
            paragraphs.append(
                "The geometric optical path difference $\\Delta$ between the two reflected rays is evaluated as:\n\n"
                "$$\\Delta = \\mu(AB + BC) - AD = 2\\mu t\\cos r$$\n\n"
                "Crucially, according to Stokes' relations and electromagnetic boundary conditions, when a light wave reflects off the interface of an optically denser medium "
                "($n_{film} > n_{air}$), the reflected electric field undergoes an abrupt phase change of $\\pi$ radians, which corresponds to an additional effective optical path difference of $\\lambda/2$. "
                "The total effective path difference in reflected light is therefore:\n\n"
                "$$\\Delta_{eff} = 2\\mu t\\cos r - \\frac{\\lambda}{2}$$\n\n"
                "Enforcing the conditions for constructive and destructive interference yields:\n"
                "- **Constructive Interference (Bright Film):** $2\\mu t\\cos r - \\frac{\\lambda}{2} = n\\lambda \\implies 2\\mu t\\cos r = \\left(n + \\frac{1}{2}\\right)\\lambda = (2n + 1)\\frac{\\lambda}{2}$\n"
                "- **Destructive Interference (Dark Film):** $2\\mu t\\cos r - \\frac{\\lambda}{2} = \\left(n - \\frac{1}{2}\\right)\\lambda \\implies 2\\mu t\\cos r = n\\lambda$"
            )
        else:
            paragraphs.append(
                "In transmitted light, the interfering rays emerging from the bottom interface undergo internal reflections exclusively at boundaries with rarer media, "
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

    elif "newton" in t_low or "ring" in t_low:
        if "measurement" in s_low or "diameter" in s_low or requires_derivation:
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
                "This formula allows high-precision experimental determination of the optical wavelength $\\lambda$. "
                "Furthermore, if a liquid of refractive index $\\mu$ is introduced between the lens and plate, the path difference becomes $2\\mu t + \\lambda/2$, "
                "compressing the ring diameters according to $D_n^2 = \\frac{4n\\lambda R}{\\mu}$, allowing precision measurement of liquid refractive index as $\\mu = \\frac{(D_{n+p}^2 - D_n^2)_{air}}{(D_{n+p}^2 - D_n^2)_{liquid}}$."
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

    elif "fraunhofer" in t_low or "diffraction" in t_low or "single slit" in s_low:
        if "intensity" in s_low or "single slit" in s_low or requires_derivation:
            paragraphs.append(
                "Fraunhofer diffraction represents far-field wave diffraction where both the incident wavefront and the diffracted wavefront are effectively planar, "
                "which is realized experimentally by placing collimating and focusing lenses before and after the diffracting aperture. "
                "Consider a monochromatic plane wave of wavelength $\\lambda$ incident normally upon a long rectangular slit of width $a$. "
                "According to Huygens' principle, the slit aperture acts as a continuous line of secondary wavelet sources of infinitesimal width $dx$."
            )
            paragraphs.append(
                "For light diffracted at an angle $\\theta$, the phase difference between wavelets emerging from the edge $x=0$ and a point at coordinate $x$ is "
                "$\\phi(x) = \\frac{2\\pi}{\\lambda} x \\sin\\theta$. "
                "Integrating the secondary wavelet amplitudes across the full slit width from $x = -a/2$ to $x = +a/2$ yields the total complex electric field amplitude:\n\n"
                "$$E(\\theta) = \\int_{-a/2}^{a/2} \\frac{E_0}{a} e^{i \\frac{2\\pi}{\\lambda} x \\sin\\theta} dx = E_0 \\frac{\\sin\\alpha}{\\alpha}$$\n\n"
                "where the phase parameter $\\alpha$ is defined as $\\alpha = \\frac{\\pi a \\sin\\theta}{\\lambda}$. "
                "Squaring the field amplitude yields the celebrated single-slit Fraunhofer diffraction intensity distribution:\n\n"
                "$$I(\\theta) = I_0 \\left( \\frac{\\sin\\alpha}{\\alpha} \\right)^2$$\n\n"
                "The central maximum occurs at $\\theta = 0$ (where $\\lim_{\\alpha \\to 0} \\frac{\\sin\\alpha}{\\alpha} = 1$), producing peak intensity $I_0$. "
                "Diffraction minima occur wherever $\\sin\\alpha = 0$ with $\\alpha \\ne 0$, which mandates $\\alpha = m\\pi \\implies a \\sin\\theta = m\\lambda$ for $m = \\pm 1, \\pm 2, \\dots$. "
                "The angular half-width of the central maximum is $\\theta_1 \\approx \\frac{\\lambda}{a}$, giving a total angular spread of $2\\lambda/a$. "
                "Secondary maxima occur at transcendental roots of $\\tan\\alpha = \\alpha$ (at $\\alpha \\approx \\pm 1.43\\pi, \\pm 2.46\\pi$), "
                "possessing drastically reduced intensities of $I_1 \\approx 0.047 I_0$ (4.7%) and $I_2 \\approx 0.016 I_0$ (1.6%)."
            )
        else:
            paragraphs.append(
                "Diffraction is the fundamental wave phenomenon whereby light bends around obstacles or spreads beyond geometric shadow boundaries. "
                "Optical diffraction is categorized into two regimes: Fresnel (near-field) diffraction, where the source and screen are at finite distances from the aperture, "
                "producing curved wavefronts and complex mathematical Fresnel integrals; and Fraunhofer (far-field) diffraction, where incident and observed wavefronts are strictly planar."
            )
            paragraphs.append(
                "The physical intensity profile of Fraunhofer single-slit diffraction illustrates the reciprocal relationship between aperture dimension and wave spreading. "
                "As the slit width $a$ is narrowed toward the wavelength $\\lambda$, the angular spread of the central maximum $\\theta \\approx \\lambda/a$ expands dramatically, "
                "eventually spreading light across the entire half-space. Conversely, when $a \\gg \\lambda$, the diffraction spread shrinks to zero, "
                "recovering classical geometric optics with sharp shadow boundaries."
            )

    elif "grating" in t_low or "dispersive" in s_low or "grating equation" in s_low:
        if "equation" in s_low or "dispersive" in s_low or requires_derivation:
            paragraphs.append(
                "A plane transmission diffraction grating consists of an array of a large number $N$ of parallel, equidistant, closely spaced transparent slits "
                "separated by opaque ruling lines. Let $a$ represent the width of each transparent slit and $b$ the width of each opaque ruling. "
                "The distance between centers of adjacent slits, $(a + b)$, is called the grating element or grating pitch."
            )
            paragraphs.append(
                "When a plane monochromatic wave of wavelength $\\lambda$ strikes the grating at normal incidence, each slit diffracts light into secondary wavelets. "
                "The path difference between corresponding wavelets emerging from adjacent slits at diffraction angle $\\theta$ is $\\Delta = (a + b)\\sin\\theta$. "
                "For waves from all $N$ slits to interfere constructively, this path difference must equal an integral number of wavelengths, "
                "establishing the fundamental grating equation:\n\n"
                "$$(a + b) \\sin\\theta = n \\lambda, \\quad n = 0, \\pm 1, \\pm 2, \\dots$$\n\n"
                "where $n$ represents the spectral order. The zero-th order ($n=0$) corresponds to undeviated light where all wavelengths overlap at $\\theta = 0$. "
                "For higher orders ($n \\ge 1$), diffracted angles depend on wavelength, dispersing composite light into its constituent spectral lines."
            )
            paragraphs.append(
                "The angular dispersive power $\\frac{d\\theta}{d\\lambda}$ measures the rate of angular separation per unit wavelength change. "
                "Differentiating the grating equation $(a + b)\\cos\\theta d\\theta = n d\\lambda$ yields:\n\n"
                "$$\\frac{d\\theta}{d\\lambda} = \\frac{n}{(a + b) \\cos\\theta}$$\n\n"
                "This demonstrates that angular dispersion is directly proportional to spectral order $n$ and inversely proportional to grating element $(a+b)$. "
                "A grating with 15,000 lines per inch exhibits an extremely small grating element $(a+b) \\approx 1.69\\,\\mu\\text{m}$, producing powerful dispersion "
                "that separates closely spaced spectral doublets such as the sodium D-lines (589.0 nm and 589.6 nm)."
            )
        else:
            paragraphs.append(
                "The diffraction pattern produced by an $N$-slit grating is mathematically described by the product of a single-slit diffraction envelope and an $N$-slit interference factor: "
                "$I(\\theta) = I_0 \\left(\\frac{\\sin\\alpha}{\\alpha}\\right)^2 \\left(\\frac{\\sin(N\\beta)}{\\sin\\beta}\\right)^2$, "
                "where $\\alpha = \\frac{\\pi a \\sin\\theta}{\\lambda}$ and $\\beta = \\frac{\\pi(a+b)\\sin\\theta}{\\lambda}$."
            )
            paragraphs.append(
                "Between any two principal maxima, there exist $(N - 1)$ diffraction minima and $(N - 2)$ faint secondary maxima. "
                "Because modern spectroscopic gratings contain tens of thousands of rulings ($N \\sim 10^4\\text{ to }10^5$), the principal maxima become exceptionally sharp, "
                "narrow, and intensely luminous spikes, while secondary maxima are suppressed below measurable detection thresholds. "
                "Furthermore, if a principal maximum condition $(a+b)\\sin\\theta = n\\lambda$ coincides with a single-slit diffraction minimum $a\\sin\\theta = m\\lambda$, "
                "that spectral order vanishes completely from the spectrum, producing a missing order defined by $\\frac{a+b}{a} = \\frac{n}{m}$."
            )

    elif "resolving" in t_low or "rayleigh" in s_low:
        if "rayleigh" in s_low or requires_derivation:
            paragraphs.append(
                "Lord Rayleigh formulated the criterion governing the physical limit of resolution for optical instruments forming diffraction patterns. "
                "According to the Rayleigh criterion, two closely spaced spectral lines of wavelengths $\\lambda$ and $\\lambda + d\\lambda$ are considered just resolved "
                "when the principal maximum of the diffraction pattern of one wavelength falls exactly upon the first diffraction minimum of the adjacent wavelength."
            )
            paragraphs.append(
                "For a diffraction grating with $N$ rulings in order $n$, the principal maximum for wavelength $\\lambda + d\\lambda$ occurs at angle $\\theta + d\\theta$ "
                "satisfying $(a+b)\\sin(\\theta + d\\theta) = n(\\lambda + d\\lambda)$. "
                "The first minimum adjacent to the $n$-th principal maximum for wavelength $\\lambda$ occurs when the path difference across the entire grating width $N(a+b)$ "
                "equals $N n \\lambda + \\lambda$, so $(a+b)\\sin(\\theta + d\\theta) = n\\lambda + \\frac{\\lambda}{N}$. "
                "Equating these two expressions yields:\n\n"
                "$$n(\\lambda + d\\lambda) = n\\lambda + \\frac{\\lambda}{N} \\implies n d\\lambda = \\frac{\\lambda}{N}$$\n\n"
                "Rearranging defines the chromatic resolving power $R$ of a diffraction grating:\n\n"
                "$$R = \\frac{\\lambda}{d\\lambda} = n N$$\n\n"
                "This elegant result demonstrates that resolving power depends exclusively on the product of the spectral order $n$ and the total number of rulings $N$ "
                "illuminated by the incident beam, completely independent of the grating element $(a+b)$. "
                "To resolve the sodium doublet ($d\\lambda = 0.6\\text{ nm}$ at $\\lambda = 589.3\\text{ nm}$), the minimum required resolving power is "
                "$R = 589.3 / 0.6 \\approx 982$, which requires a minimum of $N = 491$ lines in the second order ($n=2$)."
            )
        else:
            paragraphs.append(
                "Resolving power measures the capacity of an optical system to separate images of two closely spaced point objects or spectral lines. "
                "It is inversely related to the limit of resolution: the smaller the angular or spatial separation between two just-resolvable features, "
                "the higher the resolving power of the instrument."
            )
            paragraphs.append(
                "For circular aperture instruments (such as astronomical telescopes and optical microscope objectives), the Fraunhofer diffraction pattern "
                "forms an Airy disk surrounded by concentric dark and bright rings. The first dark ring occurs at angular radius $\\theta = 1.22 \\frac{\\lambda}{D}$, "
                "where $D$ is the circular aperture diameter. Applying Rayleigh's criterion dictates that two distant stars are just resolvable if their angular separation "
                "exceeds $\\Delta\\theta = 1.22 \\frac{\\lambda}{D}$. This fundamental diffraction limit establishes why larger telescope objective diameters "
                "are mandatory for resolving fine celestial details."
            )

    elif "polarization" in t_low or "brewster" in s_low or "double refraction" in s_low:
        if "brewster" in s_low or requires_derivation:
            paragraphs.append(
                "Polarization provides unambiguous physical proof that light propagates as a transverse electromagnetic wave rather than a longitudinal acoustic wave. "
                "In unpolarized light, the electric field vector $\\mathbf{E}$ vibrates randomly in all possible directions perpendicular to the propagation axis. "
                "When light is plane-polarized (linearly polarized), the electric field is constrained to oscillate within a single fixed plane containing the propagation axis."
            )
            paragraphs.append(
                "In 1812, Sir David Brewster discovered that when unpolarized light reflects off a dielectric boundary (such as air-to-glass), the reflected light becomes "
                "100% linearly polarized at a specific angle of incidence termed Brewster's angle $\\theta_p$. "
                "Brewster determined experimentally that at this angle, the reflected ray and refracted ray are mutually perpendicular: $\\theta_p + r = 90^\\circ \\implies r = 90^\\circ - \\theta_p$."
            )
            paragraphs.append(
                "Applying Snell's law of refraction $\\frac{\\sin\\theta_p}{\\sin r} = \\mu$ and substituting $r = 90^\\circ - \\theta_p$ yields Brewster's law:\n\n"
                "$$\\frac{\\sin\\theta_p}{\\sin(90^\\circ - \\theta_p)} = \\frac{\\sin\\theta_p}{\\cos\\theta_p} = \\tan\\theta_p = \\mu$$\n\n"
                "At Brewster's angle, electrons oscillating in the dielectric medium vibrate parallel to the direction of the would-be reflected ray. "
                "Because an oscillating electric dipole radiates zero energy along its axis of vibration, the component of the electric field polarized parallel to the plane of incidence "
                "cannot be radiated into the reflected beam. Consequently, the reflected beam contains exclusively electric field vectors oscillating perpendicular to the plane of incidence (s-polarization)."
            )
        else:
            paragraphs.append(
                "Double refraction (birefringence) is an optical property exhibited by optically anisotropic crystals such as calcite ($\\text{CaCO}_3$) and quartz ($\\text{SiO}_2$). "
                "When a ray of unpolarized light enters a calcite crystal along any direction other than the optic axis, it splits into two separate refracted rays "
                "polarized in mutually orthogonal planes: the Ordinary ray (O-ray) and the Extraordinary ray (E-ray)."
            )
            paragraphs.append(
                "The O-ray obeys Snell's law of refraction in all directions, possesses a spherical wavefront, and propagates with constant velocity $v_o = c / n_o$. "
                "The E-ray violates Snell's law, possesses an ellipsoidal wavefront, and propagates with direction-dependent velocity $v_e(\\theta)$. "
                "William Nicol utilized this phenomenon to construct the Nicol prism: a calcite rhomb cut along its blunt corners, polished, and cemented back together with Canada balsam "
                "($n_{balsam} = 1.55$). Because $n_o = 1.658 > n_{balsam} > n_e = 1.486$, the O-ray strikes the balsam layer beyond its critical angle and is eliminated by total internal reflection, "
                "transmitting a pure, 100% plane-polarized E-ray. Plane-polarized light intensity transmitted through a polarizing analyzer is governed by Malus's law: $I = I_0 \\cos^2\\theta$."
            )

    else:
        paragraphs.append(
            f"The pedagogical study of {subtopic} within {topic} establishes the foundational mathematical principles of physical wave optics. "
            "By synthesizing harmonic wave propagation, electromagnetic boundary conditions, and spatial superposition, "
            "students develop a quantitative mastery of optical diffraction, interference metrology, and laser beam manipulation."
        )
        paragraphs.append(
            "These optical principles underpin contemporary high-technology industries, ranging from semiconductor photolithography and optical communications "
            "to precision laser metrology and interferometric gravitational wave observatories."
        )

    return paragraphs


def generate_laser_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Lasers topics."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    if "intro" in t_low or "characteristics" in s_low or "monochromaticity" in s_low:
        if "monochromaticity" in s_low or "coherence" in s_low:
            paragraphs.append(
                "The defining physical attribute distinguishing laser radiation from conventional thermal luminescence is its extraordinary spatial and temporal coherence. "
                "In conventional incandescent or gas discharge lamps, trillions of independent atoms undergo spontaneous radiative decay with random phase angles, "
                "producing an incoherent electromagnetic field whose spectral linewidth $\\Delta\\nu$ spans gigahertz to terahertz. "
                "The resulting coherence length $l_c = c / \\Delta\\nu$ rarely exceeds a fraction of a millimeter."
            )
            paragraphs.append(
                "In stark contrast, laser oscillators utilize stimulated emission locked within an optical resonant cavity to generate macroscopic coherence. "
                "Longitudinal cavity modes select an ultra-narrow spectral linewidth ($\\Delta\\nu < 10\\text{ kHz}$ in stabilized systems), "
                "yielding coherence lengths exceeding hundreds of kilometers. "
                "Spatial coherence across the transverse beam profile allows the entire wavefront to oscillate in unvarying phase synchrony, "
                "enabling the laser beam to propagate over vast distances with minimal diffractive divergence bounded only by the fundamental limit $\\theta \\approx 1.22 \\lambda / D$."
            )
        else:
            paragraphs.append(
                "The acronym LASER stands for 'Light Amplification by Stimulated Emission of Radiation'. "
                "Coined by Gordon Gould in 1957, it encapsulates the quantum mechanical process by which coherent electromagnetic radiation "
                "is generated and amplified through stimulated atomic transitions. "
                "Laser beams possess four quintessential characteristics that render them indispensable across modern science and engineering: "
                "extreme monochromaticity, high degree of spatial and temporal coherence, exceptional directionality (low divergence), and colossal brightness or radiance."
            )
            paragraphs.append(
                "Because a laser concentrates optical power into a nearly diffraction-limited spatial beam mode (typically $\\text{TEM}_{00}$), "
                "its focused power density can exceed $10^{15}\\text{ W/cm}^2$—many orders of magnitude brighter than the surface of the sun. "
                "This immense energy concentration underpins laser materials processing, non-linear optics, high-harmonic generation, "
                "and inertial confinement nuclear fusion research."
            )

    elif "spontaneous emission" in t_low or "lifetime" in s_low:
        if "lifetime" in s_low or requires_derivation:
            paragraphs.append(
                "Spontaneous emission is a probabilistic quantum decay mechanism wherein an atom in an excited electronic state $E_2$ "
                "transitions autonomously to a lower energy state $E_1$ without any external radiative perturbation. "
                "The emitted photon carries energy matching the Bohr transition rule $h\\nu = E_2 - E_1$, but its propagation direction, "
                "polarization state, and phase angle are completely random and uncorrelated."
            )
            paragraphs.append(
                "The rate of spontaneous decay is directly proportional to the instantaneous population density $N_2$ of the excited state:\n\n"
                "$$-\\left(\\frac{dN_2}{dt}\\right)_{spont} = A_{21} N_2$$\n\n"
                "where $A_{21}$ is the Einstein coefficient for spontaneous emission (having dimensions of $\\text{s}^{-1}$). "
                "Integrating this first-order differential equation yields exponential population decay:\n\n"
                "$$N_2(t) = N_2(0) e^{-A_{21} t} = N_2(0) e^{-t / \\tau_{sp}}$$\n\n"
                "where $\\tau_{sp} = \\frac{1}{A_{21}}$ represents the spontaneous radiative lifetime of the excited state. "
                "For conventional dipole-allowed atomic transitions, $\\tau_{sp} \\sim 10^{-8}\\text{ s}$ (10 nanoseconds), "
                "which causes rapid de-excitation and broad natural spectral linewidths."
            )
        else:
            paragraphs.append(
                "From the viewpoint of quantum electrodynamics, spontaneous emission is not truly an uncaused event; "
                "rather, it is stimulated by vacuum zero-point fluctuations of the quantized electromagnetic field. "
                "Even in a total vacuum at absolute zero temperature, the ground state of the electromagnetic field possesses a non-zero zero-point energy $\\frac{1}{2}\\hbar\\omega$ per mode, "
                "which perturbs the atomic dipole and induces spontaneous radiative transitions."
            )
            paragraphs.append(
                "Because each atom decays independently with a random phase, light generated exclusively by spontaneous emission "
                "(such as fluorescent tubes, LED lamps, and thermal flames) is spatially and temporally incoherent. "
                "In laser systems, spontaneous emission provides the initial seed photons required to initiate oscillation, "
                "but excessive spontaneous emission during steady-state lasing acts as an unwanted noise source that dissipates pump energy."
            )

    elif "stimulated emission" in t_low or "coherent multiplication" in s_low or "transition probability" in s_low:
        if "coherent" in s_low or requires_derivation:
            paragraphs.append(
                "Stimulated emission represents the fundamental physical mechanism that enables optical amplification. "
                "In 1917, Albert Einstein predicted that when an incident photon possessing resonant energy $h\\nu = E_2 - E_1$ "
                "encounters an atom already residing in excited state $E_2$, the electromagnetic field of the photon forces the atomic dipole "
                "to oscillate in phase with the incoming wave, stimulating a downward transition to ground state $E_1$."
            )
            paragraphs.append(
                "The stimulated transition emits a second photon that is an exact quantum replica of the incident photon: "
                "it possesses identically equal frequency $\\nu$, identical phase $\\phi$, identical propagation direction $\\mathbf{k}$, "
                "and identical polarization vector $\\hat{\\epsilon}$. "
                "The transition rate for stimulated emission is proportional to both the excited state population $N_2$ and the spectral radiation energy density $\\rho(\\nu)$:\n\n"
                "$$-\\left(\\frac{dN_2}{dt}\\right)_{stim} = B_{21} N_2 \\rho(\\nu)$$\n\n"
                "where $B_{21}$ is the Einstein coefficient for stimulated emission. "
                "Because one incident photon yields two identical coherent photons, repeated stimulated emissions within an inverted medium "
                "produce an exponential cascade of coherent photons, establishing macroscopic optical amplification."
            )
        else:
            paragraphs.append(
                "Stimulated emission is the quantum basis of optical gain. "
                "Consider an electromagnetic wave of intensity $I_\\nu$ propagating through an active medium along the $z$-axis. "
                "The incremental change in intensity across differential distance $dz$ balances stimulated emission gain against absorption loss:\n\n"
                "$$\\frac{dI_\\nu}{dz} = \\sigma_{21}(\\nu) \\left( N_2 - \\frac{g_2}{g_1} N_1 \\right) I_\\nu = \\gamma(\\nu) I_\\nu$$\n\n"
                "where $\\sigma_{21}(\\nu)$ is the transition cross-section, $g_1, g_2$ are level statistical degeneracies, "
                "and $\\gamma(\\nu)$ is the net optical gain coefficient. "
                "If the excited state population dominates such that $N_2 > \\frac{g_2}{g_1} N_1$, the gain coefficient is positive ($\\gamma > 0$), "
                "producing exponential optical growth $I(z) = I_0 e^{\\gamma z}$ and enabling lasing action."
            )

    elif "absorption" in t_low or "induced transitions" in s_low or "cross section" in s_low:
        paragraphs.append(
            "Stimulated absorption is the quantum process wherein an atom in a lower energy state $E_1$ absorbs an incident photon "
            "of resonant energy $h\\nu = E_2 - E_1$, elevating an electron to the excited state $E_2$. "
            "The rate of stimulated absorption is governed by the lower state population $N_1$, the radiation energy density $\\rho(\\nu)$, "
            "and the Einstein absorption coefficient $B_{12}$:\n\n"
            "$$\\left(\\frac{dN_1}{dt}\\right)_{abs} = -B_{12} N_1 \\rho(\\nu)$$"
        )
        paragraphs.append(
            "Macroscopically, stimulated absorption attenuates light propagating through a medium in accordance with the Beer-Lambert law. "
            "The attenuation across optical distance $z$ is expressed as $I(z) = I_0 e^{-\\alpha(\\nu) z}$, "
            "where the absorption coefficient $\\alpha(\\nu) = \\sigma_{12}(\\nu)(N_1 - \\frac{g_1}{g_2} N_2)$ depends directly on the net unexcited ground state density. "
            "In any unpumped thermal medium, absorption inevitably overwhelms stimulated emission, requiring active population inversion to achieve net transmission gain."
        )

    elif "population inversion" in t_low or "boltzmann" in s_low or "pumping" in s_low:
        if "boltzmann" in s_low or requires_derivation:
            paragraphs.append(
                "In any thermodynamic system at thermal equilibrium at absolute temperature $T$, the relative population distribution "
                "between two discrete energy levels $E_1$ and $E_2$ ($E_2 > E_1$) is strictly governed by Maxwell-Boltzmann statistics:\n\n"
                "$$\\frac{N_2}{N_1} = \\frac{g_2}{g_1} e^{-(E_2 - E_1) / k_B T} = \\frac{g_2}{g_1} e^{-h\\nu / k_B T}$$\n\n"
                "where $k_B = 1.381 \\times 10^{-23}\\text{ J/K}$ is the Boltzmann constant. "
                "For optical frequencies where transition energy $\\Delta E = h\\nu \\approx 2\\text{ eV}$ (such as visible red at 600 nm) "
                "and at room temperature $T = 300\\text{ K}$ (where thermal energy $k_B T \\approx 0.0259\\text{ eV}$), "
                "the exponential ratio evaluates to:\n\n"
                "$$\\frac{N_2}{N_1} \\approx e^{-2 / 0.0259} = e^{-77.2} \\approx 10^{-34}$$\n\n"
                "This vanishingly small ratio proves that at thermal equilibrium, excited atomic states are virtually empty. "
                "Because absorption rate $B_{12}N_1\\rho$ exceeds stimulated emission rate $B_{21}N_2\\rho$ by thirty-four orders of magnitude, "
                "incident resonant light is overwhelmingly absorbed, rendering optical amplification completely impossible under equilibrium conditions."
            )
        else:
            paragraphs.append(
                "Population inversion defines a highly non-equilibrium thermodynamic state in which the population of an upper energy level "
                "exceeds that of a lower energy level ($N_2 > N_1$). "
                "Under population inversion, the stimulated emission rate exceeds the absorption rate, converting the attenuating medium "
                "into an active coherent optical amplifier."
            )
            paragraphs.append(
                "Achieving population inversion requires external energy injection, termed pumping. "
                "Crucially, steady-state population inversion is mathematically impossible in a simple two-level atomic system "
                "because optical pumping stimulates absorption and downward emission at identical rates ($B_{12} = B_{21}$), "
                "saturating the population at equal densities ($N_1 = N_2$) where net gain vanishes. "
                "Practical lasers therefore mandate three-level or four-level systems utilizing optical pumping (xenon flash lamps), "
                "electrical discharge excitation (gas collision ionization), or direct carrier injection across degenerate semiconductor p-n junctions."
            )

    elif "metastable" in t_low or "lasing action" in s_low:
        paragraphs.append(
            "A metastable state is an excited electronic energy state possessing an unusually prolonged radiative lifetime compared to normal atomic states. "
            "While typical dipole-allowed atomic transitions decay spontaneously within $\\tau \\sim 10^{-8}\\text{ s}$, "
            "metastable states exhibit radiative lifetimes spanning $10^{-4}\\text{ s}$ to over $10^{-2}\\text{ s}$ (milliseconds). "
            "This prolonged stability arises from quantum mechanical dipole selection rules: optical transitions from metastable states "
            "to lower levels violate electric dipole selection rules (such as $\\Delta L = \\pm 1$ or spin conservation $\\Delta S = 0$), "
            "rendering spontaneous decay forbidden to first order."
        )
        paragraphs.append(
            "Metastable states are the indispensable prerequisite for lasing action in three-level and four-level systems. "
            "When pump energy excites atoms to higher, short-lived pump bands ($E_3$), they decay non-radiatively via fast phonon emission "
            "($\\tau_{32} \\sim 10^{-11}\\text{ s}$) into the intermediate metastable state ($E_2$). "
            "Because atoms enter the metastable state millions of times faster than they can leave it via spontaneous decay, "
            "a massive atomic backlog accumulates in level $E_2$, successfully establishing the population inversion $N_2 > N_1$ required for stimulated amplification."
        )

    elif "einstein coefficient" in t_low or "ratio" in s_low or "coefficients" in t_low:
        if "ratio" in s_low or requires_derivation:
            paragraphs.append(
                "In 1917, Albert Einstein derived the thermodynamic relations governing radiative transitions between atomic states $E_1$ and $E_2$ "
                "by considering an atomic gas enclosed in a cavity at thermodynamic equilibrium with thermal radiation at temperature $T$. "
                "Under steady-state equilibrium, the rate of upward transitions (absorption) must identically equal the sum of downward transitions "
                "(spontaneous plus stimulated emission):\n\n"
                "$$B_{12} N_1 \\rho(\\nu) = A_{21} N_2 + B_{21} N_2 \\rho(\\nu)$$"
            )
            paragraphs.append(
                "Rearranging this detailed balance equation to isolate the radiation energy density $\\rho(\\nu)$ yields:\n\n"
                "$$\\rho(\\nu) = \\frac{A_{21} N_2}{B_{12} N_1 - B_{21} N_2} = \\frac{A_{21} / B_{21}}{\\frac{B_{12}}{B_{21}} \\frac{N_1}{N_2} - 1}$$\n\n"
                "Substituting the Boltzmann population ratio $\\frac{N_1}{N_2} = \\frac{g_1}{g_2} e^{h\\nu / k_B T}$ into the expression gives:\n\n"
                "$$\\rho(\\nu) = \\frac{A_{21} / B_{21}}{\\frac{g_1 B_{12}}{g_2 B_{21}} e^{h\\nu / k_B T} - 1}$$\n\n"
                "Comparing this thermodynamic formula with Planck's empirical radiation distribution $\\rho(\\nu) = \\frac{8\\pi h\\nu^3}{c^3} \\frac{1}{e^{h\\nu / k_B T} - 1}$, "
                "both expressions must hold identically for all frequencies and temperatures, dictating the two fundamental Einstein relations:\n\n"
                "$$g_1 B_{12} = g_2 B_{21} \\quad \\text{and} \\quad \\frac{A_{21}}{B_{21}} = \\frac{8\\pi h \\nu^3}{c^3}$$\n\n"
                "The first relation establishes that the probabilities for stimulated absorption and stimulated emission are intrinsically equal. "
                "The second relation reveals that the ratio of spontaneous to stimulated emission rates scales cubically with frequency ($\\propto \\nu^3$). "
                "This $\\nu^3$ dependence explains why stimulated emission lasers are readily realized in microwave (masers) and visible domains, "
                "whereas constructing ultraviolet and X-ray lasers requires exponentially higher pump power densities to overcome rapid spontaneous decay."
            )
        else:
            paragraphs.append(
                "Einstein's transition coefficients establish the thermodynamic bridge between microscopic quantum electrodynamics "
                "and macroscopic radiation transport. Coefficient $A_{21}$ governs spontaneous emission, $B_{21}$ dictates stimulated emission, "
                "and $B_{12}$ controls stimulated absorption. "
                "Together, they satisfy the universal proportionality $\\frac{A_{21}}{B_{21}} = \\frac{8\\pi h\\nu^3}{c^3}$, "
                "proving that spontaneous and stimulated transitions are fundamentally intertwined aspects of electromagnetic radiation."
            )

    elif "ruby" in t_low:
        paragraphs.append(
            "The ruby laser, constructed in May 1960 by Theodore Maiman at Hughes Research Laboratories, was the world's first operational laser. "
            "It is a solid-state, three-level pulsed laser system. The active gain medium is a synthetic single-crystal corundum rod of aluminum oxide "
            "($\\text{Al}_2\\text{O}_3$) doped with approximately $0.05\\%$ by weight of trivalent chromium ions ($\\text{Cr}^{3+}$). "
            "The optical pump source is a high-intensity helical xenon flashlamp coiled around the ruby rod and powered by a high-voltage capacitor bank."
        )
        paragraphs.append(
            "The three-level energy scheme operates as follows: chromium ions residing in ground state $E_1$ ($^4A_2$) absorb green (550 nm) and blue (400 nm) "
            "pump photons, exciting them to broad pump absorption bands $E_3$ ($^4F_1, ^4F_2$). "
            "Within picoseconds ($10^{-11}\\text{ s}$), excited ions undergo rapid non-radiative phonon relaxation, dumping lattice heat and transitioning "
            "into the metastable doublet level $E_2$ ($^2E$). Because the metastable state has a long lifetime of $\\tau \\approx 3\\text{ ms}$, "
            "intense optical pumping transfers more than 50% of all chromium ions from $E_1$ to $E_2$, achieving population inversion $N_2 > N_1$."
        )
        paragraphs.append(
            "Optical feedback is provided by polished flat end-facets of the ruby rod: one end is coated for 100% reflectance, while the opposite output facet "
            "is coated for 90% reflectance, forming a Fabry-Perot resonator. Stimulated emission occurs between the metastable level $E_2$ and ground state $E_1$, "
            "emitting high-energy pulses of deep crimson red light at wavelength $\\lambda = 694.3\\text{ nm}$ with pulse powers reaching megawatts."
        )

    elif "he-ne" in t_low or "helium-neon" in t_low:
        paragraphs.append(
            "Invented in 1960 by Ali Javan, William Bennett, and Donald Herriott at Bell Laboratories, the Helium-Neon (He-Ne) laser "
            "was the first continuous-wave (CW) gas laser. It is a four-level laser system consisting of an active gas mixture of approximately "
            "10 parts helium to 1 part neon enclosed within a narrow quartz capillary tube at a total pressure of about $1\\text{ torr}$. "
            "The tube ends are sealed with optical windows set at Brewster's angle $\\theta_p \\approx 56^\\circ$ to eliminate reflection loss and produce 100% plane-polarized output."
        )
        paragraphs.append(
            "The pumping mechanism utilizes an electric glow discharge produced by a high DC voltage ($1\\text{ to }2\\text{ kV}$). "
            "Energetic electrons in the discharge collide inelastically with helium atoms, exciting them to metastable singlet $2^1S_0$ and triplet $2^3S_1$ states. "
            "Because helium's $2^1S$ and $2^3S$ levels happen to align almost perfectly in energy with neon's $3s$ and $2s$ states ($20.61\\text{ eV}$ and $19.82\\text{ eV}$), "
            "resonant atom-atom collision transfer excites neon atoms with high efficiency while dropping helium atoms back to the ground state."
        )
        paragraphs.append(
            "This creates strong population inversion between neon's $3s$ excited state and its lower $2p$ level. "
            "Stimulated radiative transitions from $3s_2 \\to 2p_4$ generate the classic bright red laser beam at wavelength $\\lambda = 632.8\\text{ nm}$ "
            "(with secondary infrared laser transitions available at $1.15\\,\\mu\\text{m}$ and $3.39\\,\\mu\\text{m}$). "
            "Neon atoms in the $2p$ state decay rapidly via spontaneous emission ($10^{-8}\\text{ s}$) to the $1s$ level, and subsequent non-radiative wall collisions "
            "depopulate the $1s$ level back to the ground state, preventing bottleneck accumulation and sustaining continuous-wave lasing."
        )

    elif "semiconductor" in t_low or "diode laser" in t_low:
        paragraphs.append(
            "Semiconductor diode lasers represent the most compact, efficient, and ubiquitous class of lasers in contemporary optoelectronics. "
            "They operate via direct electrical carrier injection across a heavily doped degenerate $p^+$-$n^+$ junction fabricated from direct bandgap semiconductors "
            "such as gallium arsenide ($\\text{GaAs}$) or indium gallium arsenide phosphide ($\\text{InGaAsP}$). "
            "Degenerate doping positions the quasi-Fermi level $E_{Fc}$ inside the conduction band on the n-side and $E_{Fv}$ inside the valence band on the p-side."
        )
        paragraphs.append(
            "Applying a forward bias voltage $V$ satisfying $qV > E_g$ injects high densities of electrons and holes simultaneously into the narrow "
            "active depletion region ($d \\sim 0.1\\,\\mu\\text{m}$). This establishes population inversion, satisfying the Bernard-Duraffourg lasing condition:\n\n"
            "$$E_{Fc} - E_{Fv} > h\\nu > E_g$$\n\n"
            "Stimulated electron-hole recombination across the bandgap emits coherent photons with energy $h\\nu \\approx E_g$. "
            "Because the refractive index of GaAs is exceptionally high ($n \\approx 3.6$), naturally cleaved crystal facet interfaces act as Fresnel reflectors "
            "with reflectance $R = \\left(\\frac{n-1}{n+1}\\right)^2 \\approx 32\\%$, forming an optical resonant cavity without external mirrors. "
            "Above threshold current density $J_{th}$, emission transitions from broad LED spontaneous recombination to intense, monochromatic stimulated lasing."
        )

    elif "application" in t_low or "industrial" in t_low or "medical" in t_low:
        paragraphs.append(
            "The engineering applications of lasers span virtually every domain of modern technology: "
            "1. **Industrial Manufacturing:** High-power $\\text{CO}_2$ ($10.6\\,\\mu\\text{m}$) and fiber lasers (Nd:YAG, $1.064\\,\\mu\\text{m}$) deliver kilowatt power densities "
            "for high-speed precision metal cutting, deep-penetration keyhole welding, surface hardening, and selective laser melting (SLM) additive manufacturing.\n"
            "2. **Optical Telecommunications:** Distributed feedback (DFB) semiconductor diode lasers operating at $1550\\text{ nm}$ provide coherent light carriers "
            "modulated at over 100 Gbps across global transoceanic optical fiber networks."
        )
        paragraphs.append(
            "3. **Medical and Surgical Therapeutics:** Excimer lasers ($193\\text{ nm}$) perform LASIK corneal photo-refractive ablation with sub-micron precision without thermal tissue damage; "
            "argon and Nd:YAG lasers photocoagulate retinal tears in ophthalmology and ablate arterial plaques in cardiology.\n"
            "4. **Scientific Metrology:** Frequency comb lasers enable optical atomic clocks with fractional frequency inaccuracies below $10^{-18}$, "
            "while kilometer-scale Fabry-Perot laser interferometers (LIGO) measure sub-nuclear spacetime strains ($10^{-21}$) from gravitational waves."
        )

    else:
        paragraphs.append(
            f"The pedagogical study of {subtopic} within {topic} provides essential insights into quantum optics and laser engineering. "
            "By synthesizing thermodynamic radiative transition probabilities with resonant cavity electrodynamics, "
            "students develop a quantitative mastery of coherent optical generation, gain saturation, and beam propagation."
        )
        paragraphs.append(
            "These principles form the foundation for contemporary photonics, optical quantum computing, and high-precision metrology."
        )

    return paragraphs


def generate_fiber_optics_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Fiber Optics topics."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    if "intro" in t_low or "guidance" in s_low or "total internal" in s_low:
        if "total internal" in s_low or requires_derivation:
            paragraphs.append(
                "An optical fiber is a cylindrical dielectric waveguide designed to transmit optical energy across long distances "
                "with minimal attenuation. The fundamental physical mechanism governing light guidance is Total Internal Reflection (TIR) "
                "at the interface between an inner dielectric core of refractive index $n_1$ and an outer cladding layer of lower refractive index $n_2$ ($n_1 > n_2$)."
            )
            paragraphs.append(
                "According to Snell's law of refraction, a light ray propagating in the core incident upon the core-cladding boundary at angle $\\phi$ "
                "refracts into the cladding at angle $\\theta_r$ according to $n_1 \\sin\\phi = n_2 \\sin\\theta_r$. "
                "As the angle of incidence $\\phi$ increases, the angle of refraction $\\theta_r$ reaches $90^\\circ$ at the critical angle $\\phi_c$:\n\n"
                "$$\\sin\\phi_c = \\frac{n_2}{n_1} \\implies \\phi_c = \\arcsin\\left(\\frac{n_2}{n_1}\\right)$$\n\n"
                "For any ray incident at an angle exceeding the critical angle ($\\phi > \\phi_c$), no light penetrates into the cladding as a propagating wave; "
                "the entire optical power is 100% internally reflected back into the core. "
                "Repeated successive total internal reflections trap the optical beam within the core, guiding it along straight or bent paths without radiative leakage."
            )
        else:
            paragraphs.append(
                "Optical fibers have revolutionized global telecommunications, completely supplanting legacy copper coaxial cables and microwave links. "
                "Optical fibers offer several transformative engineering advantages: "
                "1. **Enormous Bandwidth:** Operating at near-infrared optical carrier frequencies ($\\sim 200\\text{ THz}$) provides theoretical transmission capacities exceeding tens of terabits per second per fiber.\n"
                "2. **Ultra-Low Attenuation:** Modern silica glass fibers achieve losses as low as $0.18\\text{ dB/km}$ at $1550\\text{ nm}$, enabling signal propagation across repeaterless spans exceeding 100 kilometers."
            )
            paragraphs.append(
                "3. **Electromagnetic Immunity:** Because optical fibers are manufactured from dielectric silica glass ($\\text{SiO}_2$), they are entirely immune to electromagnetic interference (EMI), radio frequency interference (RFI), and high-voltage lightning surges.\n"
                "4. **Compact Form Factor and Lightweight:** A standard optical fiber has a glass diameter of only $125\\,\\mu\\text{m}$, allowing high-density cables containing hundreds of fibers to be installed in existing ducts.\n"
                "5. **High Signal Security:** Fiber waveguides radiate zero electromagnetic leakage, preventing inductive wiretapping."
            )

    elif "structure" in t_low or "geometry" in s_low or "profile" in s_low:
        if "profile" in s_low:
            paragraphs.append(
                "The optical characteristics of an optical fiber are governed by its radial refractive index profile $n(r)$. "
                "The core exhibits maximum refractive index $n_1$ along the central axis, while the cladding maintains a lower refractive index $n_2$. "
                "The fractional refractive index difference $\\Delta$ is defined as:\n\n"
                "$$\\Delta = \\frac{n_1 - n_2}{n_1} \\approx \\frac{n_1^2 - n_2^2}{2n_1^2}$$\n\n"
                "In standard silica telecommunication fibers, $\\Delta$ typically ranges between $0.1\\%$ and $1.0\\%$ ($0.001 \\le \\Delta \\le 0.01$)."
            )
            paragraphs.append(
                "Fibers are broadly classified into two categories based on their refractive index distribution: "
                "1. **Step-Index Fibers:** The refractive index remains completely uniform throughout the core ($n(r) = n_1$ for $r \\le a$) "
                "and drops discontinuously in an abrupt step to $n_2$ at the core-cladding interface ($r = a$).\n"
                "2. **Graded-Index (GRIN) Fibers:** The refractive index decreases continuously as a smooth function of radial distance $r$, "
                "typically following a power-law profile $n(r) = n_1 \\sqrt{1 - 2\\Delta(r/a)^\\alpha}$, where $\\alpha$ is the profile grading exponent. "
                "A parabolic profile with $\\alpha \\approx 2$ optimizes modal transit times, drastically suppressing intermodal pulse broadening."
            )
        else:
            paragraphs.append(
                "A standard optical fiber consists of three concentric geometric layers: "
                "1. **Core:** The innermost cylindrical region of radius $a$ fabricated from ultra-pure fused silica glass ($\\text{SiO}_2$) "
                "doped with refractive-index-raising dopants such as germanium dioxide ($\\text{GeO}_2$) or phosphorus pentoxide ($\\text{P}_2\\text{O}_5$). "
                "Core diameters range from $8\\text{ to }10\\,\\mu\\text{m}$ in single-mode fibers to $50\\text{ to }62.5\\,\\mu\\text{m}$ in multimode fibers."
            )
            paragraphs.append(
                "2. **Cladding:** A surrounding glass cylinder of outer diameter $125\\,\\mu\\text{m}$ manufactured from pure silica or silica down-doped with fluorine ($\\text{F}$). "
                "The cladding serves to confine optical power within the core, support the evanescent electromagnetic wave, and shield the core interface from surface contaminants.\n"
                "3. **Primary Buffer Jacket:** An outer dual-layer polymer coating (typically UV-cured acrylate, outer diameter $250\\,\\mu\\text{m}$) "
                "that provides mechanical strength, moisture protection, and cushioning against microbending losses during cabling and installation."
            )

    elif "acceptance" in t_low or "numerical aperture" in t_low or "critical angle" in s_low:
        if "derivation" in s_low or "numerical aperture" in s_low or requires_derivation:
            paragraphs.append(
                "Consider an optical fiber with core refractive index $n_1$ and cladding refractive index $n_2$ immersed in an external launching medium "
                "(such as air) of refractive index $n_0 \\approx 1.0$. A light ray enters the flat launching end-face of the fiber at angle of incidence $\\theta_0$, "
                "refracts into the core at angle $r$, and strikes the core-cladding interface at angle of incidence $\\phi = 90^\\circ - r$."
            )
            paragraphs.append(
                "Applying Snell's law at the entrance end-face yields $n_0 \\sin\\theta_0 = n_1 \\sin r = n_1 \\sin(90^\\circ - \\phi) = n_1 \\cos\\phi$. "
                "For the ray to be guided along the fiber, it must undergo total internal reflection at the core-cladding interface, "
                "which requires $\\phi \\ge \\phi_c$, or equivalently $\\sin\\phi \\ge \\sin\\phi_c = \\frac{n_2}{n_1}$. "
                "The limiting condition $\\phi = \\phi_c$ dictates $\\cos\\phi = \\sqrt{1 - \\sin^2\\phi_c} = \\sqrt{1 - (n_2/n_1)^2} = \\frac{\\sqrt{n_1^2 - n_2^2}}{n_1}$."
            )
            paragraphs.append(
                "Substituting this into the entrance Snell relation gives the maximum launch angle $\\theta_a$ (termed the acceptance angle):\n\n"
                "$$n_0 \\sin\\theta_a = n_1 \\left( \\frac{\\sqrt{n_1^2 - n_2^2}}{n_1} \\right) = \\sqrt{n_1^2 - n_2^2}$$\n\n"
                "For launching from air where $n_0 = 1$, the acceptance angle $\\theta_a$ and the Numerical Aperture (NA) are defined as:\n\n"
                "$$\\text{NA} = \\sin\\theta_a = \\sqrt{n_1^2 - n_2^2} = n_1 \\sqrt{2\\Delta}$$\n\n"
                "$$\\theta_a = \\arcsin(\\text{NA}) = \\arcsin\\left(\\sqrt{n_1^2 - n_2^2}\\right)$$\n\n"
                "The Numerical Aperture is a dimensionless figure of merit that quantifies the light-gathering capacity of the fiber. "
                "Rays launched within the conical solid angle of semi-apex angle $\\theta_a$ (the acceptance cone) undergo total internal reflection "
                "and propagate through the fiber, whereas rays entering outside the cone refract into the cladding and are lost."
            )
        else:
            paragraphs.append(
                "The acceptance angle and numerical aperture govern optical coupling efficiency from emitters (such as laser diodes or LEDs) into optical fibers. "
                "A large numerical aperture ($\text{NA} \\approx 0.3\\text{ to }0.5$) provides a wide acceptance cone, enabling high-efficiency coupling "
                "from broad, incoherent LED emitters. However, higher NA fibers require higher core doping levels, which increase Rayleigh scattering attenuation."
            )
            paragraphs.append(
                "In high-speed telecommunications, single-mode fibers are engineered with a small numerical aperture ($\text{NA} \\approx 0.10\\text{ to }0.14$), "
                "corresponding to an acceptance angle of only $\\theta_a \\approx 6^\\circ\\text{ to }8^\\circ$. "
                "This narrow acceptance cone requires precision laser alignment and micro-optic lens coupling, "
                "but ensures low modal dispersion, narrow chromatic pulse spreading, and superior transmission bandwidths."
            )

    elif "step-index" in t_low or "graded-index" in t_low:
        if "graded" in s_low or "modal" in s_low or requires_derivation:
            paragraphs.append(
                "In multimode step-index fibers, optical pulses suffer severe intermodal dispersion because different spatial modes travel along different ray paths. "
                "An axial ray traveling directly along the center line covers distance $L$ in transit time $t_{min} = \\frac{L}{v_1} = \\frac{L n_1}{c}$. "
                "The highest-order mode traveling at the critical angle $\\phi_c$ covers a longer zig-zag path of length $L / \\sin\\phi_c = L (n_1 / n_2)$, "
                "requiring transit time $t_{max} = \\frac{L (n_1 / n_2)}{c / n_1} = \\frac{L n_1^2}{c n_2}$."
            )
            paragraphs.append(
                "The resulting intermodal pulse broadening $\\Delta\\tau_{step}$ across fiber length $L$ is given by:\n\n"
                "$$\\Delta\\tau_{step} = t_{max} - t_{min} = \\frac{L n_1}{c} \\left( \\frac{n_1}{n_2} - 1 \\right) = \\frac{L n_1}{c} \\left( \\frac{n_1 - n_2}{n_2} \\right) \\approx \\frac{L n_1 \\Delta}{c}$$\n\n"
                "For typical parameters ($n_1 = 1.5, \\Delta = 0.01$), the pulse spread is approximately $\\Delta\\tau / L \\approx 50\\text{ ns/km}$, "
                "severely restricting the bandwidth-distance product to approximately $20\\text{ MHz}\\cdot\\text{km}$."
            )
            paragraphs.append(
                "Graded-Index (GRIN) fibers solve this limitation by employing a parabolic core refractive index profile: $n(r) = n_1 [1 - 2\\Delta(r/a)^2]^{1/2}$. "
                "In a GRIN fiber, light rays do not travel in straight zig-zag lines, but follow smooth helical, sinusoidal trajectories. "
                "Higher-order rays traveling longer trajectories spend most of their transit in the outer peripheral regions of the core where the refractive index is lower. "
                "Because local phase velocity $v(r) = c / n(r)$ increases in lower-index regions, the higher speed along longer peripheral paths precisely compensates "
                "for the shorter paths traveled by axial rays. This self-equalizing mechanism reduces intermodal dispersion to $\\Delta\\tau_{grin} \\approx \\frac{L n_1 \\Delta^2}{8c}$, "
                "improving transmission bandwidth by three orders of magnitude ($1\\text{ to }3\\text{ GHz}\\cdot\\text{km}$)."
            )
        else:
            paragraphs.append(
                "Step-index and graded-index fibers represent two fundamentally distinct waveguide designs for optical communication. "
                "Multimode step-index fibers feature large core diameters ($100\\text{ to }200\\,\\mu\\text{m}$) and are easy to manufacture, terminate, and splice. "
                "They are predominantly employed in short-reach, cost-sensitive links such as automotive data buses, industrial automation controls, "
                "and medical illumination endoscopy where high bandwidth is not required."
            )
            paragraphs.append(
                "Graded-index fibers, with standardized core diameters of $50\\,\\mu\\text{m}$ (OM3, OM4) and $62.5\\,\\mu\\text{m}$ (OM1), "
                "are engineered specifically for enterprise local area networks (LANs) and intra-datacenter optical interconnects. "
                "When paired with $850\\text{ nm}$ vertical-cavity surface-emitting lasers (VCSELs), graded-index multimode fibers reliably support "
                "data rates of $10\\text{ to }100\\text{ Gbps}$ across campus distances of up to 550 meters."
            )

    elif "single mode" in t_low or "multi mode" in t_low or "v-number" in s_low or "cutoff" in s_low:
        if "v-number" in s_low or "cutoff" in s_low or requires_derivation:
            paragraphs.append(
                "The electromagnetic modal propagation characteristics of a step-index optical fiber are governed by Maxwell's wave equations, "
                "which reduce to Bessel differential equations whose eigenvalue solutions define discrete propagating modes. "
                "The number of guided modes is dictated by a dimensionless parameter known as the normalized frequency or $V$-number:\n\n"
                "$$V = \\frac{2\\pi a}{\\lambda} \\sqrt{n_1^2 - n_2^2} = \\frac{2\\pi a}{\\lambda} \\text{NA} = \\frac{2\\pi a}{\\lambda} n_1 \\sqrt{2\\Delta}$$\n\n"
                "where $a$ is the core radius, $\\lambda$ is the operating free-space wavelength, and $\\text{NA}$ is the numerical aperture."
            )
            paragraphs.append(
                "In a multimode fiber where $V \\gg 1$, the total number of guided spatial modes $M$ supported by a step-index fiber is approximately:\n\n"
                "$$M_{step} \\approx \\frac{V^2}{2}, \\quad M_{graded} \\approx \\frac{V^2}{4}$$\n\n"
                "For a single-mode fiber (SMF), the core diameter is made so small that all higher-order modes are cut off, leaving only the fundamental "
                "doubly-degenerate hybrid $\\text{HE}_{11}$ mode (or $\\text{LP}_{01}$ linearly polarized mode) able to propagate. "
                "The mathematical condition for single-mode operation requires the $V$-number to remain below the first root of the Bessel function $J_0$:\n\n"
                "$$V \\le 2.405$$\n\n"
                "This single-mode cutoff threshold dictates the cutoff wavelength $\\lambda_c$:\n\n"
                "$$\\lambda_c = \\frac{2\\pi a}{2.405} \\text{NA} = \\frac{2\\pi a}{2.405} \\sqrt{n_1^2 - n_2^2}$$\n\n"
                "For wavelengths longer than cutoff ($\\lambda > \\lambda_c$), the fiber operates strictly in single-mode regime. "
                "Because single-mode fibers support only one spatial mode, intermodal dispersion is identically zero, making SMF the exclusive transmission medium "
                "for long-haul terrestrial and transoceanic telecommunication networks."
            )
        else:
            paragraphs.append(
                "Comparing single-mode and multimode fibers illustrates the core trade-offs of optical network design. "
                "Multimode fibers (MMF) possess large cores ($50\\,\\mu\\text{m}$), allowing them to support hundreds of guided modes ($M \\sim 500$). "
                "This large core allows relaxed connector alignment tolerances ($\\pm 5\\,\\mu\\text{m}$) and inexpensive LED/VCSEL light sources, "
                "making MMF cost-effective for short distances, despite being limited by intermodal dispersion."
            )
            paragraphs.append(
                "Single-mode fibers (SMF) feature microscopic cores ($8.2\\text{ to }9.0\\,\\mu\\text{m}$ in standard ITU-T G.652 fiber) "
                "that demand sub-micron connector alignment tolerances and precision laser transmitters. "
                "However, eliminating intermodal dispersion allows single-mode fiber to achieve virtually limitless bandwidth, "
                "bounded only by chromatic dispersion and fiber non-linearities, supporting petabit-per-second capacities across thousands of kilometers."
            )

    elif "attenuation" in t_low or "absorption" in s_low or "rayleigh" in s_low:
        paragraphs.append(
            "Optical fiber attenuation represents the loss of optical signal power as light propagates through the waveguide. "
            "Attenuation is quantified by the attenuation coefficient $\\alpha$ in decibels per kilometer ($\\text{dB/km}$):\n\n"
            "$$\\alpha = \\frac{10}{L} \\log_{10}\\left(\\frac{P_{in}}{P_{out}}\\right)$$\n\n"
            "where $P_{in}$ and $P_{out}$ are input and output optical powers across fiber length $L$. "
            "Fiber loss arises from three primary mechanisms: intrinsic material absorption, extrinsic impurity absorption, and Rayleigh scattering."
        )
        paragraphs.append(
            "1. **Rayleigh Scattering:** Rayleigh scattering is the dominant intrinsic loss mechanism in silica fibers. "
            "It is caused by microscopic, sub-wavelength thermodynamic density and compositional fluctuations frozen into the glass matrix during molten drawing. "
            "Rayleigh scattering loss scales inversely with the fourth power of wavelength: $\\alpha_R \\propto \\frac{1}{\\lambda^4}$. "
            "Because of this $\\lambda^{-4}$ dependence, scattering loss drops precipitously from $2.5\\text{ dB/km}$ at $850\\text{ nm}$ down to $0.15\\text{ dB/km}$ at $1550\\text{ nm}$."
        )
        paragraphs.append(
            "2. **Intrinsic and Extrinsic Absorption:** At short wavelengths ($\\lambda < 0.4\\,\\mu\\text{m}$), intrinsic electronic bandgap absorption dominates. "
            "At long infrared wavelengths ($\\lambda > 1.6\\,\\mu\\text{m}$), molecular silicon-oxygen (Si-O) vibrational phonon absorption causes rapid attenuation. "
            "Extrinsic absorption is caused by trace metallic ions and residual hydroxyl ($\\text{OH}^-$) radical impurities, which produce strong absorption peaks "
            "at $950\\text{ nm}$, $1240\\text{ nm}$, and especially the notorious 'water peak' at $1383\\text{ nm}$. "
            "Modern 'low-water-peak' fibers (ITU-T G.652.D) eliminate OH contamination, opening the entire spectrum from $1260\\text{ nm}$ to $1625\\text{ nm}$ for wavelength division multiplexing (WDM)."
        )

    elif "dispersion" in t_low or "pulse broadening" in s_low or "material" in s_low:
        paragraphs.append(
            "Dispersion is the optical phenomenon wherein an optical pulse broadens temporally as it propagates along a fiber, "
            "causing neighboring pulses to overlap and induce Intersymbol Interference (ISI), which severely constrains maximum transmission bit rates. "
            "In single-mode fibers where intermodal dispersion is absent, pulse broadening is governed by chromatic (intramodal) dispersion $D$, "
            "measured in $\\text{ps}/(\\text{nm}\\cdot\\text{km})$:\n\n"
            "$$D = D_{mat} + D_{wg} = -\\frac{\\lambda}{c} \\frac{d^2 n_1}{d\\lambda^2} - \\frac{n_1 \\Delta}{c\\lambda} V \\frac{d^2(Vb)}{dV^2}$$\n\n"
            "Chromatic dispersion consists of two components: Material Dispersion $D_{mat}$ and Waveguide Dispersion $D_{wg}$."
        )
        paragraphs.append(
            "Material dispersion arises because the refractive index $n(\\lambda)$ of fused silica varies non-linearly with optical wavelength, "
            "causing different spectral components of a modulated laser pulse to travel at different group velocities $v_g(\\lambda)$. "
            "Waveguide dispersion arises because the spatial distribution of the fundamental mode between core and cladding shifts with wavelength: "
            "longer wavelengths penetrate deeper into the lower-index cladding, traveling faster. "
            "In standard silica fiber (G.652), material dispersion passes through zero at $\\lambda_0 \\approx 1310\\text{ nm}$ (the zero-dispersion wavelength). "
            "By engineering the core refractive index profile, waveguide dispersion can be tailored to cancel material dispersion at $1550\\text{ nm}$, "
            "creating Dispersion-Shifted Fiber (DSF, G.653) and Non-Zero Dispersion-Shifted Fiber (NZDSF, G.655) optimized for amplified WDM systems."
        )

    elif "communications" in t_low or "transmitter" in s_low or "receiver" in s_low:
        paragraphs.append(
            "An optical fiber communication link consists of three core subsystems: "
            "1. **Optical Transmitter:** Converts electrical data signals into modulated optical pulses using direct modulation of semiconductor lasers "
            "or external Mach-Zehnder lithium niobate ($\\text{LiNbO}_3$) electro-optic modulators, operating across ITU telecom windows (C-band: $1530\\text{--}1565\\text{ nm}$).\n"
            "2. **Optical Transmission Medium:** Single-mode optical fiber spans interspersed with Erbium-Doped Fiber Amplifiers (EDFA) "
            "that provide all-optical gain without requiring electrical conversion, enabling transoceanic transmission."
        )
        paragraphs.append(
            "3. **Optical Receiver:** Demultiplexes wavelength channels and converts optical pulses back into electrical signals using high-speed photodetectors: "
            "PIN photodiodes (for cost-effective, high-linearity detection) or Avalanche Photodiodes (APD, utilizing internal avalanche multiplication gain "
            "for high-sensitivity long-reach links), followed by transimpedance amplifiers (TIA) and clock-and-data recovery (CDR) electronics."
        )

    elif "sensors" in t_low or "intrinsic" in s_low or "extrinsic" in s_low:
        paragraphs.append(
            "Fiber optic sensors utilize optical fibers to measure physical quantities such as strain, temperature, pressure, acoustic vibration, and rotation. "
            "Fiber sensors are classified into two broad categories: "
            "1. **Intrinsic Sensors:** The optical fiber itself acts as the active sensing transducer. An external physical perturbation modulates the intensity, "
            "phase, polarization, or wavelength of the guided optical wave propagating inside the fiber core.\n"
            "A prominent example is the Fiber Bragg Grating (FBG) sensor, where periodic ultraviolet laser modulation of core refractive index reflects "
            "a specific Bragg wavelength $\\lambda_B = 2 n_{eff} \\Lambda$. Mechanical strain $\\epsilon$ or temperature change $\\Delta T$ expands the grating pitch $\\Lambda$, "
            "shifting the reflected wavelength according to $\\frac{\\Delta\\lambda_B}{\\lambda_B} = (1 - p_e)\\epsilon + (\\alpha_T + \\xi)\\Delta T$, enabling multiplexed structural health monitoring."
        )
        paragraphs.append(
            "2. **Extrinsic Sensors:** The optical fiber serves exclusively as a light transmission channel to carry optical signals to and from an external sensing transducer head.\n"
            "3. **Fiber Optic Gyroscopes (FOG):** Based on the relativistic Sagnac effect, two counter-propagating laser waves traverse a multi-kilometer fiber coil. "
            "Rotational angular velocity $\\Omega$ creates an optical path difference that produces a measurable interference phase shift "
            "$\\Delta\\Phi_S = \\frac{8\\pi A N}{\\lambda c} \\Omega$, providing drift-free inertial navigation for aerospace and defense systems."
        )

    elif "fabrication" in t_low or "splicing" in t_low or "drawing" in s_low:
        paragraphs.append(
            "Manufacturing modern telecommunication optical fibers is a precision two-step process: preform fabrication followed by fiber drawing. "
            "Optical preforms (cylindrical glass rods of diameter $20\\text{ to }50\\text{ mm}$) are fabricated using Chemical Vapor Deposition (CVD) processes, "
            "such as Modified Chemical Vapor Deposition (MCVD), Outside Vapor Deposition (OVD), or Vapor Axial Deposition (VAD). "
            "In MCVD, gaseous silicon tetrachloride ($\\text{SiCl}_4$) and germanium tetrachloride ($\\text{GeCl}_4$) react with oxygen inside a rotating silica substrate tube "
            "at $1600^\\circ\\text{C}$, depositing ultra-pure glassy soot layers that are vitrified into the high-index core before collapsing into a solid preform rod."
        )
        paragraphs.append(
            "The completed preform is mounted atop a multi-story fiber drawing tower and lowered into a high-temperature graphite furnace ($2000^\\circ\\text{C}$). "
            "The molten glass tip necks down into a microscopic fiber drawn at speeds exceeding $20\\text{ m/s}$. "
            "Non-contact laser gauges monitor the $125.0 \\pm 0.5\\,\\mu\\text{m}$ cladding diameter in real time, and dual polymer coating dies apply the protective acrylate jacket.\n\n"
            "Permanent fiber joining is performed via electric arc fusion splicing. "
            "Fiber ends are stripped, cleaved flat to within $0.5^\\circ$, aligned using microscopic core Profile Alignment Systems (PAS), "
            "and melted together by a controlled electric arc discharge, achieving joint insertion losses below $0.02\\text{ dB}$."
        )

    elif "photonic crystal" in t_low or "microstructured" in s_low:
        paragraphs.append(
            "Photonic Crystal Fibers (PCFs), or microstructured optical fibers, represent an advanced class of optical waveguides developed in the late 1990s. "
            "Unlike conventional doped-silica fibers, PCFs are manufactured from a single pure silica material containing a periodic two-dimensional lattice "
            "of microscopic air channels running along the entire length of the fiber cladding parallel to the central optical axis."
        )
        paragraphs.append(
            "PCFs operate via two distinct wave guidance mechanisms: "
            "1. **Modified Total Internal Reflection (Solid-Core PCF):** A missing central air hole forms a solid silica core surrounded by an air-hole cladding. "
            "Because the air-silica cladding has an effective refractive index $n_{eff} < n_{silica}$, light is guided by total internal reflection. "
            "Remarkably, because the effective cladding index increases at shorter wavelengths, the $V$-number parameter remains below $2.405$ across all frequencies, "
            "producing 'endlessly single-mode' operation from deep ultraviolet to mid-infrared.\n"
            "2. **Photonic Bandgap Guidance (Hollow-Core PCF):** Light is confined within a hollow air or gas core by coherent Bragg scattering from the surrounding periodic hole lattice, "
            "allowing high-power laser transmission without silica damage, minimal non-linear distortion, and light propagation at 99.7% of $c$."
        )

    else:
        paragraphs.append(
            f"The pedagogical study of {subtopic} within {topic} provides essential foundations in modern optical waveguide theory and photonics. "
            "By synthesizing dielectric electromagnetic boundary value problems with optical dispersion and attenuation mechanisms, "
            "students develop a quantitative mastery of optical transmission engineering."
        )
        paragraphs.append(
            "These waveguide principles power modern global Internet backbones, datacenter optical interconnects, and advanced sensor telemetry."
        )

    return paragraphs


def generate_em_relativity_prose(topic: str, subtopic: str, requires_derivation: bool = False) -> List[str]:
    """Generates authentic university prose for Electromagnetism & Relativity topics."""
    t_low = topic.lower()
    s_low = subtopic.lower()
    paragraphs = []

    if "gauss law in electrostatics" in t_low or "electric flux" in s_low or "differential form of gauss law" in s_low:
        if "differential" in s_low or requires_derivation:
            paragraphs.append(
                "Gauss's law in electrostatics relates the distribution of electric charge to the resulting electric field. "
                "In integral form, Gauss's law states that the net outward electric flux $\\Phi_E$ passing through any closed Gaussian surface $S$ "
                "is directly proportional to the total net enclosed electric charge $Q_{enc}$:\n\n"
                "$$\\Phi_E = \\oiint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{Q_{enc}}{\\epsilon_0} = \\frac{1}{\\epsilon_0} \\iiint_V \\rho(\\mathbf{r}) dV$$\n\n"
                "where $\\epsilon_0 = 8.854 \\times 10^{-12}\\text{ F/m}$ is the permittivity of free space and $\\rho(\\mathbf{r})$ is the continuous volume charge density."
            )
            paragraphs.append(
                "To derive the differential form of Gauss's law, we apply Gauss's divergence theorem to the closed surface integral of the electric field vector, "
                "transforming it into a volume integral of the divergence of $\\mathbf{E}$ across the enclosed volume $V$:\n\n"
                "$$\\oiint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\iiint_V (\\nabla \\cdot \\mathbf{E}) dV$$\n\n"
                "Equating this to the enclosed charge integral yields:\n\n"
                "$$\\iiint_V (\\nabla \\cdot \\mathbf{E}) dV = \\iiint_V \\frac{\\rho}{\\epsilon_0} dV \\implies \\iiint_V \\left( \\nabla \\cdot \\mathbf{E} - \\frac{\\rho}{\\epsilon_0} \\right) dV = 0$$\n\n"
                "Because this equality must hold identically for any arbitrary enclosed volume $V$, the integrand itself must vanish everywhere, "
                "establishing the first Maxwell equation in differential form:\n\n"
                "$$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\epsilon_0}$$\n\n"
                "This fundamental field equation dictates that positive electric charges act as divergent sources of electric flux lines, "
                "while negative electric charges act as convergent sinks, establishing the monopolar character of electrostatic charge."
            )
        else:
            paragraphs.append(
                "Electric flux $\\Phi_E$ quantifies the total number of electric field lines penetrating a given surface element. "
                "For a flat surface of vector area $\\mathbf{A}$ oriented in a uniform electric field $\\mathbf{E}$, flux is defined by the dot product "
                "$\\Phi_E = \\mathbf{E} \\cdot \\mathbf{A} = E A \\cos\\theta$, where $\\theta$ is the angle between the electric field and the surface normal. "
                "For curved surfaces and non-uniform fields, the flux is generalized to the surface integral $\\Phi_E = \\iint \\mathbf{E} \\cdot d\\mathbf{A}$."
            )
            paragraphs.append(
                "Gauss's law serves as a powerful analytical tool for determining electric fields in configurations possessing high geometric symmetry "
                "(spherical, cylindrical, or planar). By constructing a Gaussian surface conforming to the coordinate symmetry of the source, "
                "the electric field magnitude remains constant across the surface and can be factored out of the integral, "
                "enabling direct algebraic computation of field strengths without complex multi-variable Coulomb integrations."
            )

    elif "gauss law in magnetism" in t_low or "magnetic monopoles" in s_low or "vector potential" in s_low:
        if "vector potential" in s_low or requires_derivation:
            paragraphs.append(
                "Gauss's law for magnetism represents the empirical observation that isolated magnetic charges (magnetic monopoles) do not exist in nature. "
                "In integral form, the total outward magnetic flux passing through any arbitrary closed Gaussian surface $S$ is identically zero:\n\n"
                "$$\\Phi_B = \\oiint_S \\mathbf{B} \\cdot d\\mathbf{A} = 0$$\n\n"
                "Applying the divergence theorem transforms the surface integral into a volume integral:\n\n"
                "$$\\oiint_S \\mathbf{B} \\cdot d\\mathbf{A} = \\iiint_V (\\nabla \\cdot \\mathbf{B}) dV = 0 \\implies \\nabla \\cdot \\mathbf{B} = 0$$"
            )
            paragraphs.append(
                "The vanishing divergence of the magnetic B-field has a profound mathematical consequence in vector calculus. "
                "According to Helmholtz's theorem, any divergence-free (solenoidal) vector field can be expressed identically as the curl "
                "of another vector field. Using the vector identity $\\nabla \\cdot (\\nabla \\times \\mathbf{A}) \\equiv 0$, the condition $\\nabla \\cdot \\mathbf{B} = 0$ "
                "proves that the magnetic field $\\mathbf{B}$ can always be derived from a magnetic vector potential $\\mathbf{A}$:\n\n"
                "$$\\mathbf{B} = \\nabla \\times \\mathbf{A}$$\n\n"
                "Under the standard Coulomb gauge condition $\\nabla \\cdot \\mathbf{A} = 0$, Ampere's law reduces to the vector Poisson equation "
                "$\\nabla^2 \\mathbf{A} = -\\mu_0 \\mathbf{J}$, whose solution directly facilitates calculating complex magnetic fields from distributed current densities."
            )
        else:
            paragraphs.append(
                "The physical implication of Gauss's law for magnetism is that magnetic field lines possess neither starting points nor terminating points; "
                "they form continuous, unbroken closed loops throughout space. "
                "Every north magnetic pole is inextricably paired with a south magnetic pole of equal and opposite strength, forming an intrinsic magnetic dipole. "
                "Even if a macroscopic bar magnet is fractured into atomic pieces, each fragment remains a complete dipole with north and south poles."
            )

    elif "faraday" in t_low or "electromotive force" in s_low or "induction" in t_low:
        if "differential" in s_low or requires_derivation:
            paragraphs.append(
                "Michael Faraday's law of electromagnetic induction states that whenever the magnetic flux linking a closed conducting circuit changes with time, "
                "an electromotive force (emf) $\\mathcal{E}$ is induced in the circuit proportional to the time rate of change of magnetic flux:\n\n"
                "$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt} = -\\frac{d}{dt} \\iint_S \\mathbf{B} \\cdot d\\mathbf{A}$$\n\n"
                "The negative sign embodies Lenz's law, enforcing conservation of energy: the induced current flows in such a direction "
                "that its own magnetic field opposes the original change in magnetic flux that produced it."
            )
            paragraphs.append(
                "By definition, electromotive force around a closed contour $C$ is the line integral of the induced electric field: "
                "$\\mathcal{E} = \\oint_C \\mathbf{E} \\cdot d\\mathbf{l}$. "
                "Equating this to Faraday's flux relation yields $\\oint_C \\mathbf{E} \\cdot d\\mathbf{l} = -\\iint_S \\frac{\\partial \\mathbf{B}}{\\partial t} \\cdot d\\mathbf{A}$. "
                "Applying Stokes' curl theorem transforms the contour line integral into a surface integral:\n\n"
                "$$\\oint_C \\mathbf{E} \\cdot d\\mathbf{l} = \\iint_S (\\nabla \\times \\mathbf{E}) \\cdot d\\mathbf{A}$$\n\n"
                "Equating both surface integrals yields the differential form of Faraday's law (the third Maxwell equation):\n\n"
                "$$\\iint_S \\left( \\nabla \\times \\mathbf{E} + \\frac{\\partial \\mathbf{B}}{\\partial t} \\right) \\cdot d\\mathbf{A} = 0 \\implies \\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$$\n\n"
                "This fundamental equation reveals that a time-varying magnetic field induces a non-conservative, circulating electric field whose curl does not vanish, "
                "overturning the electrostatic condition $\\nabla \\times \\mathbf{E} = 0$."
            )
        else:
            paragraphs.append(
                "Faraday's discovery of electromagnetic induction represents the technological cornerstone of modern electric power infrastructure. "
                "Whenever a conductor translates through a magnetic field or rotates within a flux gradient, magnetic Lorentz forces "
                "$\\mathbf{F} = q(\\mathbf{v} \\times \\mathbf{B})$ drive mobile charge carriers along the conductor, generating motional electromotive force."
            )
            paragraphs.append(
                "This principle drives electric alternators, high-efficiency transformers, and induction motors. "
                "In high-frequency electronics, time-varying magnetic fields induce circulating eddy currents in metallic cores, "
                "requiring laminated silicon steel sheets or ferrite ceramics to minimize resistive Joulean heating losses."
            )

    elif "ampere-maxwell" in t_low or "displacement current" in s_low or "inadequacy" in s_low:
        if "displacement" in s_low or "inadequacy" in s_low or requires_derivation:
            paragraphs.append(
                "In classical magnetostatics, Ampere's circuital law was formulated in differential form as $\\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J}$. "
                "In 1861, James Clerk Maxwell recognized that this formulation was mathematically flawed and physically incomplete for time-dependent fields. "
                "Taking the divergence of both sides of Ampere's law, the vector identity dictating that the divergence of any curl is identically zero requires:\n\n"
                "$$\\nabla \\cdot (\\nabla \\times \\mathbf{B}) \\equiv 0 \\implies \\mu_0 (\\nabla \\cdot \\mathbf{J}) = 0 \\implies \\nabla \\cdot \\mathbf{J} = 0$$"
            )
            paragraphs.append(
                "However, the fundamental law of conservation of electric charge is expressed by the continuity equation:\n\n"
                "$$\\nabla \\cdot \\mathbf{J} + \\frac{\\partial\\rho}{\\partial t} = 0 \\implies \\nabla \\cdot \\mathbf{J} = -\\frac{\\partial\\rho}{\\partial t}$$\n\n"
                "For time-dependent fields where charge density changes ($\\\\partial\\rho/\\partial t \\ne 0$, such as charging a capacitor), "
                "$\\nabla \\cdot \\mathbf{J} \\ne 0$, creating a severe mathematical contradiction. "
                "To resolve this, Maxwell substituted Gauss's law $\\rho = \\epsilon_0 (\\nabla \\cdot \\mathbf{E})$ into the continuity equation:\n\n"
                "$$\\nabla \\cdot \\mathbf{J} = -\\frac{\\partial}{\\partial t}(\\epsilon_0 \\nabla \\cdot \\mathbf{E}) = -\\nabla \\cdot \\left( \\epsilon_0 \\frac{\\partial\\mathbf{E}}{\\partial t} \\right) \\implies \\nabla \\cdot \\left( \\mathbf{J} + \\epsilon_0 \\frac{\\partial\\mathbf{E}}{\\partial t} \\right) = 0$$"
            )
            paragraphs.append(
                "Maxwell identified the term $\\mathbf{J}_d = \\epsilon_0 \\frac{\\partial\\mathbf{E}}{\\partial t}$ as the displacement current density. "
                "Adding this displacement current to the physical conduction current density yields the complete Ampere-Maxwell law:\n\n"
                "$$\\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J} + \\mu_0 \\epsilon_0 \\frac{\\partial\\mathbf{E}}{\\partial t}$$\n\n"
                "Displacement current does not represent the physical motion of electric charges; rather, it is a time-varying electric field "
                "acting as a dynamical source that generates magnetic fields, ensuring complete continuity of total current across capacitor dielectric gaps."
            )
        else:
            paragraphs.append(
                "The classic physical illustration of displacement current is the charging of a parallel-plate capacitor. "
                "While current flows along the conducting wire as conduction current $I_c = dq/dt$, no physical electrons bridge the insulating dielectric gap between plates. "
                "Yet, a magnetic field is observed experimentally encircling the gap between the plates."
            )
            paragraphs.append(
                "As charge accumulates on the plates, the time-varying electric field between the plates $E(t) = \\frac{q(t)}{\\epsilon_0 A}$ creates displacement current "
                "$I_d = \\epsilon_0 \\frac{\\partial E}{\\partial t} A = \\frac{dq}{dt} = I_c$. "
                "The displacement current across the gap identically equals the conduction current in the external leads, "
                "preserving current continuity and completing Maxwell's unification of electromagnetism."
            )

    elif "maxwell equations in free space" in t_low or "four equations" in s_low or "wave equation" in s_low:
        if "wave equation" in s_low or requires_derivation:
            paragraphs.append(
                "In source-free vacuum where charge density $\\rho = 0$ and conduction current density $\\mathbf{J} = 0$, "
                "the unified Maxwell equations reduce to four coupled partial differential field equations:\n\n"
                "1. $\\nabla \\cdot \\mathbf{E} = 0$\n"
                "2. $\\nabla \\cdot \\mathbf{B} = 0$\n"
                "3. $\\nabla \\times \\mathbf{E} = -\\frac{\\partial\\mathbf{B}}{\\partial t}$\n"
                "4. $\\nabla \\times \\mathbf{B} = \\mu_0 \\epsilon_0 \\frac{\\partial\\mathbf{E}}{\\partial t}$"
            )
            paragraphs.append(
                "To decouple these equations and derive the electromagnetic wave equation, we take the curl of Faraday's law:\n\n"
                "$$\\nabla \\times (\\nabla \\times \\mathbf{E}) = \\nabla \\times \\left( -\\frac{\\partial\\mathbf{B}}{\\partial t} \\right) = -\\frac{\\partial}{\\partial t}(\\nabla \\times \\mathbf{B})$$\n\n"
                "Applying the vector Laplacian identity $\\nabla \\times (\\nabla \\times \\mathbf{E}) = \\nabla(\\nabla \\cdot \\mathbf{E}) - \\nabla^2 \\mathbf{E}$, "
                "and substituting $\\nabla \\cdot \\mathbf{E} = 0$ alongside Ampere-Maxwell's vacuum equation $\\nabla \\times \\mathbf{B} = \\mu_0\\epsilon_0 \\frac{\\partial\\mathbf{E}}{\\partial t}$:\n\n"
                "$$-\\nabla^2 \\mathbf{E} = -\\mu_0\\epsilon_0 \\frac{\\partial^2 \\mathbf{E}}{\\partial t^2} \\implies \\nabla^2 \\mathbf{E} - \\mu_0\\epsilon_0 \\frac{\\partial^2 \\mathbf{E}}{\\partial t^2} = 0$$\n\n"
                "Taking the curl of the fourth equation analogously yields the identical wave equation for the magnetic field:\n\n"
                "$$\\nabla^2 \\mathbf{B} - \\mu_0\\epsilon_0 \\frac{\\partial^2 \\mathbf{B}}{\\partial t^2} = 0$$\n\n"
                "Comparing these results with the standard classical 3D wave equation $\\nabla^2 \\psi - \\frac{1}{v^2}\\frac{\\partial^2\\psi}{\\partial t^2} = 0$ "
                "demonstrates that time-varying electric and magnetic fields self-sustain and propagate through vacuum as transverse electromagnetic waves at speed:\n\n"
                "$$c = \\frac{1}{\\sqrt{\\mu_0 \\epsilon_0}} = \\frac{1}{\\sqrt{(4\\pi \\times 10^{-7}) \\times (8.854 \\times 10^{-12})}} = 2.998 \\times 10^8\\text{ m/s}$$\n\n"
                "Maxwell's theoretical calculation matched the experimentally measured speed of light with remarkable precision, "
                "leading to the monumental revelation that light is itself an electromagnetic wave."
            )
        else:
            paragraphs.append(
                "The four Maxwell equations encapsulate the complete classical theory of electricity, magnetism, and optics into a unified mathematical framework. "
                "They describe how electric charges generate electric fields (Gauss 1), how magnetic fields form continuous closed loops without monopoles (Gauss 2), "
                "how changing magnetic fields generate electric fields (Faraday), and how both electric currents and changing electric fields generate magnetic fields (Ampere-Maxwell)."
            )

    elif "electromagnetic wave propagation" in t_low or "transverse" in s_low or "impedance" in s_low:
        if "impedance" in s_low or requires_derivation:
            paragraphs.append(
                "Consider a monochromatic plane electromagnetic wave propagating along the $+z$ direction in vacuum, described by: "
                "$\\mathbf{E}(z, t) = E_0 \\cos(kz - \\omega t) \\hat{x}$ and $\\mathbf{B}(z, t) = B_0 \\cos(kz - \\omega t) \\hat{y}$. "
                "Substituting into Faraday's law $\\nabla \\times \\mathbf{E} = -\\frac{\\partial\\mathbf{B}}{\\partial t}$ yields "
                "$\\frac{\\partial E_x}{\\partial z} = -\\frac{\\partial B_y}{\\partial t} \\implies -k E_0 \\sin(kz - \\omega t) = -\\omega B_0 \\sin(kz - \\omega t)$."
            )
            paragraphs.append(
                "Equating coefficients gives the fundamental relation between electric and magnetic amplitudes: $E_0 = \\frac{\\omega}{k} B_0 = c B_0$. "
                "Expressing the magnetic field in terms of magnetic field intensity $\\mathbf{H} = \\frac{\\mathbf{B}}{\\mu_0}$, "
                "the ratio of the electric field to the magnetic field intensity defines the intrinsic wave impedance of free space $\\eta_0$:\n\n"
                "$$\\eta_0 = \\frac{E}{H} = \\frac{E}{B / \\mu_0} = \\mu_0 \\left(\\frac{E}{B}\\right) = \\mu_0 c = \\mu_0 \\frac{1}{\\sqrt{\\mu_0 \\epsilon_0}} = \\sqrt{\\frac{\\mu_0}{\\epsilon_0}}$$\n\n"
                "Substituting standard free-space constants yields the exact value:\n\n"
                "$$\\eta_0 = \\sqrt{\\frac{4\\pi \\times 10^{-7}\\text{ H/m}}{8.854 \\times 10^{-12}\\text{ F/m}}} \\approx 376.73\\ \\Omega \\approx 120\\pi\\ \\Omega$$\n\n"
                "Furthermore, evaluating total instantaneous energy density $u = \\frac{1}{2}\\epsilon_0 E^2 + \\frac{1}{2\\mu_0} B^2$ reveals that "
                "$\\frac{1}{2\\mu_0} B^2 = \\frac{1}{2\\mu_0}\\left(\\frac{E}{c}\\right)^2 = \\frac{1}{2\\mu_0}\\frac{E^2}{1/(\\mu_0\\epsilon_0)} = \\frac{1}{2}\\epsilon_0 E^2$, "
                "proving that electromagnetic energy is partitioned exactly equally between electric and magnetic field components."
            )
        else:
            paragraphs.append(
                "Electromagnetic waves in free space are strictly transverse in character. "
                "Evaluating the divergence equations $\\nabla \\cdot \\mathbf{E} = 0$ and $\\nabla \\cdot \\mathbf{B} = 0$ for plane waves with wavevector $\\mathbf{k}$ "
                "yields $\\mathbf{k} \\cdot \\mathbf{E} = 0$ and $\\mathbf{k} \\cdot \\mathbf{B} = 0$, "
                "proving that neither field has a longitudinal component along the direction of propagation."
            )
            paragraphs.append(
                "Furthermore, the cross-product relation $\\mathbf{k} \\times \\mathbf{E} = \\omega \\mathbf{B}$ establishes that the electric field $\\mathbf{E}$, "
                "magnetic field $\\mathbf{B}$, and propagation vector $\\mathbf{k}$ form a mutually orthogonal right-handed Cartesian triad $(\\mathbf{E} \\perp \\mathbf{B} \\perp \\mathbf{k})$. "
                "Both field vectors oscillate in temporal and spatial phase, reaching their respective positive maxima, zero nodes, and negative peaks simultaneously."
            )

    elif "poynting" in t_low:
        if "vector" in s_low or "derivation" in s_low or requires_derivation:
            paragraphs.append(
                "Poynting's theorem represents the fundamental conservation of energy principle for electromagnetic fields interacting with matter. "
                "The rate of work done by electromagnetic forces on charges contained within volume $V$ is given by the Lorentz power integral $\\iiint_V (\\mathbf{J} \\cdot \\mathbf{E}) dV$."
            )
            paragraphs.append(
                "Using the vector calculus identity $\\nabla \\cdot (\\mathbf{E} \\times \\mathbf{H}) = \\mathbf{H} \\cdot (\\nabla \\times \\mathbf{E}) - \\mathbf{E} \\cdot (\\nabla \\times \\mathbf{H})$, "
                "we substitute Maxwell's curl equations $\\nabla \\times \\mathbf{E} = -\\frac{\\partial\\mathbf{B}}{\\partial t}$ and $\\nabla \\times \\mathbf{H} = \\mathbf{J} + \\frac{\\partial\\mathbf{D}}{\\partial t}$:\n\n"
                "$$\\nabla \\cdot (\\mathbf{E} \\times \\mathbf{H}) = \\mathbf{H} \\cdot \\left(-\\frac{\\partial\\mathbf{B}}{\\partial t}\\right) - \\mathbf{E} \\cdot \\left(\\mathbf{J} + \\frac{\\partial\\mathbf{D}}{\\partial t}\\right) = -\\mathbf{J} \\cdot \\mathbf{E} - \\left( \\mathbf{E} \\cdot \\frac{\\partial\\mathbf{D}}{\\partial t} + \\mathbf{H} \\cdot \\frac{\\partial\\mathbf{B}}{\\partial t} \\right)$$\n\n"
                "Recognizing the total electromagnetic energy density $u = \\frac{1}{2}\\epsilon_0 E^2 + \\frac{1}{2}\\mu_0 H^2 = \\frac{1}{2}(\\mathbf{E}\\cdot\\mathbf{D} + \\mathbf{H}\\cdot\\mathbf{B})$, "
                "its time derivative is $\\frac{\\partial u}{\\partial t} = \\mathbf{E} \\cdot \\frac{\\partial\\mathbf{D}}{\\partial t} + \\mathbf{H} \\cdot \\frac{\\partial\\mathbf{B}}{\\partial t}$."
            )
            paragraphs.append(
                "Defining the Poynting vector $\\mathbf{S}$ as:\n\n"
                "$$\\mathbf{S} = \\mathbf{E} \\times \\mathbf{H} = \\frac{1}{\\mu_0} (\\mathbf{E} \\times \\mathbf{B})$$\n\n"
                "we obtain Poynting's theorem in differential form:\n\n"
                "$$\\nabla \\cdot \\mathbf{S} + \\frac{\\partial u}{\\partial t} = -\\mathbf{J} \\cdot \\mathbf{E}$$\n\n"
                "In this continuity equation, $\\mathbf{S}$ represents the instantaneous power flux density (measured in $\\text{W/m}^2$), "
                "$\\frac{\\partial u}{\\partial t}$ represents the time rate of field energy storage, and $-\\mathbf{J}\\cdot\\mathbf{E}$ accounts for Joulean dissipation. "
                "For harmonic plane waves, the time-averaged Poynting vector gives the radiant intensity: $\\langle \\mathbf{S} \\rangle = \\frac{1}{2} \\frac{E_0^2}{\\eta_0} \\hat{k}$."
            )
        else:
            paragraphs.append(
                "The Poynting vector $\\mathbf{S} = \\mathbf{E} \\times \\mathbf{H}$ dictates the directional transport of electromagnetic power across space. "
                "Remarkably, Poynting's theorem applies to both propagating waves and steady-state DC electric circuits. "
                "In a DC coaxial cable carrying direct current, the Poynting vector points parallel to the cable axis through the insulating dielectric, "
                "proving that electrical energy flows through the surrounding electromagnetic fields rather than through the copper conductors themselves."
            )

    elif "galilean" in t_low or "michelson" in s_low or "ether" in s_low:
        paragraphs.append(
            "Classical Newtonian mechanics rested upon Galilean relativity, which assumed absolute Euclidean space and universal, uniform time $t' = t$. "
            "For two inertial reference frames $S$ and $S'$ with $S'$ translating at constant velocity $v$ along the $x$-axis, "
            "the Galilean coordinate transformations are given by: $x' = x - vt, y' = y, z' = z, t' = t$. "
            "Differentiating yields the classical velocity addition rule: $u_x' = u_x - v$. "
            "While Newton's laws of motion $\\mathbf{F} = m\\mathbf{a}$ remain invariant under Galilean transformations, "
            "Maxwell's electromagnetic wave equations change form, predicting that the speed of light should depend on frame velocity as $c' = c \\pm v$."
        )
        paragraphs.append(
            "To resolve this conflict, nineteenth-century physicists posited the existence of an all-pervading luminiferous ether. "
            "In 1887, Albert Michelson and Edward Morley conducted their celebrated optical interferometry experiment at Case School of Applied Science. "
            "Their apparatus split a light beam into mutually perpendicular arms of equal length $L$, reflecting them back to produce interference fringes. "
            "If Earth traveled through stationary ether at orbital velocity $v \\approx 30\\text{ km/s}$, rotating the apparatus by $90^\\circ$ should have produced "
            "a measurable fringe shift $\\Delta N = \\frac{2L}{\\lambda}\\frac{v^2}{c^2} \\approx 0.4\\text{ fringes}$."
        )
        paragraphs.append(
            "The experiment yielded an unambiguous null result: the observed fringe shift was consistently less than 0.005 fringes. "
            "This historic null result decisively demolished the luminiferous ether hypothesis, proving that the speed of light is an absolute constant "
            "independent of the motion of the observer or source, and precipitating Einstein's special theory of relativity."
        )

    elif "postulates" in t_low or "constancy of speed of light" in s_low:
        paragraphs.append(
            "In June 1905, Albert Einstein resolved the conflict between Newtonian mechanics and Maxwellian electrodynamics "
            "by formulating the Special Theory of Relativity upon two revolutionary axiomatic postulates: "
            "1. **The Principle of Relativity:** The laws of physics—encompassing both mechanics and electrodynamics—assume identical mathematical form "
            "in all inertial reference frames. There is no preferred or absolute state of rest in the universe.\n"
            "2. **The Constancy of the Speed of Light:** The speed of light in vacuum is an absolute universal constant $c = 2.99792458 \\times 10^8\\text{ m/s}$ "
            "in all inertial frames of reference, completely independent of the translational motion of the emitting source or the observing detector."
        )
        paragraphs.append(
            "Einstein's second postulate directly demolished the classical concept of absolute Newtonian time. "
            "A radical consequence is the Relativity of Simultaneity: two spatially separated events that are judged to occur simultaneously "
            "in reference frame $S$ are not simultaneous when viewed from another inertial frame $S'$ moving relative to $S$. "
            "Time is not an independent universal scalar, but a relative coordinate interwoven with spatial coordinates into a four-dimensional spacetime continuum."
        )

    elif "lorentz" in t_low or "length contraction" in s_low:
        if "derivation" in s_low or "transformation" in s_low or requires_derivation:
            paragraphs.append(
                "To satisfy Einstein's postulates, coordinate transformations between inertial frames $S$ and $S'$ (moving at velocity $v$ along $x$) "
                "must preserve the invariance of the spherical light wavefront equation: $x^2 + y^2 + z^2 - c^2 t^2 = 0 \\iff x'^2 + y'^2 + z'^2 - c^2 t'^2 = 0$. "
                "Assuming a linear transformation $x' = \\gamma(x - vt)$ and $x = \\gamma(x' + vt')$, and demanding light speed invariance $x = ct \\implies x' = ct'$, "
                "we evaluate $ct' = \\gamma(ct - vt) = \\gamma t(c - v)$ and $ct = \\gamma(ct' + vt') = \\gamma t'(c + v)$."
            )
            paragraphs.append(
                "Multiplying the two relations yields $c^2 = \\gamma^2 (c^2 - v^2) \\implies \\gamma^2 = \\frac{1}{1 - v^2/c^2}$. "
                "This defines the celebrated relativistic Lorentz factor:\n\n"
                "$$\\gamma = \\frac{1}{\\sqrt{1 - v^2 / c^2}} = \\frac{1}{\\sqrt{1 - \\beta^2}}$$\n\n"
                "Substituting $\\gamma$ into the coordinate expressions establishes the Lorentz Transformations:\n\n"
                "$$x' = \\gamma(x - vt), \\quad y' = y, \\quad z' = z, \\quad t' = \\gamma\\left(t - \\frac{vx}{c^2}\\right)$$\n\n"
                "In the non-relativistic limit where $v \\ll c$, $\\beta \\to 0$ and $\\gamma \\to 1$, smoothly recovering classical Galilean transformations."
            )
            paragraphs.append(
                "A foundational consequence of the Lorentz transformations is relativistic Length Contraction. "
                "Let a rod be at rest in frame $S_0$ with proper length $L_0 = x_2 - x_1$. An observer in frame $S'$ moving with velocity $v$ "
                "measures the rod ends simultaneously at time $t_1' = t_2'$. "
                "Applying $x_2 - x_1 = \\gamma(x_2' - x_1')$ yields:\n\n"
                "$$L = x_2' - x_1' = \\frac{x_2 - x_1}{\\gamma} = L_0 \\sqrt{1 - \\frac{v^2}{c^2}}$$\n\n"
                "A physical body appears contracted along the direction of its relative motion by factor $\\sqrt{1 - v^2/c^2}$, "
                "while transverse dimensions remain completely unaltered."
            )
        else:
            paragraphs.append(
                "The Lorentz transformations replaced Galilean relativity, providing the true mathematical geometry of spacetime. "
                "They demonstrate that space and time cannot be treated as separate entities; rather, any change in inertial reference frame "
                "rotates spatial and temporal coordinates into one another via hyperbolic rotations in four-dimensional Minkowski spacetime."
            )

    elif "time dilation" in t_low or "mass-energy" in t_low or "e = mc" in s_low or "twin paradox" in s_low:
        if "derivation" in s_low or "mass-energy" in s_low or requires_derivation:
            paragraphs.append(
                "Consider a clock at rest in frame $S_0$ that measures a proper time interval $\\Delta t_0 = t_2 - t_1$ between two ticks at the same spatial point ($x_1 = x_2$). "
                "For an observer in frame $S'$ moving at velocity $v$, the time interval between these two events is governed by the Lorentz transformation "
                "$t' = \\gamma(t - vx/c^2)$:\n\n"
                "$$\\Delta t = t_2' - t_1' = \\gamma(t_2 - t_1) = \\frac{\\Delta t_0}{\\sqrt{1 - v^2 / c^2}}$$\n\n"
                "Because $\\gamma > 1$ for any non-zero velocity, $\\Delta t > \\Delta t_0$. "
                "This phenomenon is relativistic Time Dilation: a moving clock ticks slower than an identical clock at rest. "
                "Empirical proof is provided by atmospheric cosmic-ray muons: although muons possess a rest-frame lifetime of only $\\tau_0 = 2.2\\,\\mu\\text{s}$, "
                "their relativistic speed ($v = 0.998c, \\gamma \\approx 15.8$) dilates their laboratory lifetime to $\\tau = 35\\,\\mu\\text{s}$, "
                "allowing them to traverse the entire 10-kilometer atmosphere and be detected at sea level."
            )
            paragraphs.append(
                "In relativistic dynamics, momentum is generalized to preserve conservation laws: $\\mathbf{p} = \\gamma m_0 \\mathbf{v}$. "
                "The kinetic energy acquired by a particle accelerated from rest by force $\\mathbf{F}$ is given by the relativistic work-energy theorem:\n\n"
                "$$E_k = \\int_0^x F dx = \\int_0^p v dp = \\int_0^v v \\frac{d(\\gamma m_0 v)}{dt} dt = \\gamma m_0 c^2 - m_0 c^2$$\n\n"
                "Einstein identified the total relativistic energy $E$ as the sum of kinetic energy and rest-mass energy $E_0 = m_0 c^2$:\n\n"
                "$$E = E_k + m_0 c^2 = \\gamma m_0 c^2 = \\frac{m_0 c^2}{\\sqrt{1 - v^2 / c^2}}$$\n\n"
                "Squaring $E = \\gamma m_0 c^2$ and relativistic momentum $p = \\gamma m_0 v$ derives the fundamental relativistic energy-momentum invariant:\n\n"
                "$$E^2 = p^2 c^2 + m_0^2 c^4$$\n\n"
                "This formula $E = mc^2$ establishes the profound equivalence of mass and energy, proving that rest mass is a colossal reservoir of dormant energy, "
                "which powers stellar nuclear fusion, atomic reactors, and relativistic particle accelerators."
            )
        else:
            paragraphs.append(
                "The celebrated Twin Paradox considers one twin traveling on a near-light-speed rocket voyage to a distant star while the other remains on Earth. "
                "Because each observes the other in relative motion, special relativistic time dilation seems to present a paradox: which twin is younger upon return? "
                "The paradox is resolved by recognizing that the two frames are not symmetric. The earthbound twin remains in a single inertial frame, "
                "whereas the traveling twin must decelerate, turn around, and accelerate back to Earth, traversing non-inertial reference frames. "
                "Applying general relativity or calculating worldline proper time integrals $\\tau = \\int \\sqrt{1 - v^2(t)/c^2} dt$ "
                "proves that the traveling twin returns measurably and physically younger."
            )

    else:
        paragraphs.append(
            f"The pedagogical study of {subtopic} within {topic} establishes the foundations of classical electrodynamics and special relativity. "
            "By synthesizing vector calculus, field flux invariants, and spacetime Lorentz transformations, "
            "students develop a quantitative mastery of electromagnetic propagation and high-velocity physical dynamics."
        )
        paragraphs.append(
            "These principles underpin relativistic particle accelerators, satellite GPS timing corrections, and modern electrodynamic engineering."
        )

    return paragraphs


def generate_physics_numerical(topic: str, subtopic: str) -> str:
    """Generates authentic university solved numerical problems matched to topic."""
    t_low = topic.lower()

    if any(k in t_low for k in ["interference", "optics", "young", "thin film", "fringe", "newton"]):
        return (
            "### Solved Numerical Example\n\n"
            "**Problem Statement:** In a Newton's rings experiment, the diameter of the 10th dark ring is $0.50\\text{ cm}$ "
            "and that of the 2nd dark ring is $0.22\\text{ cm}$. If the radius of curvature of the plano-convex lens is $100\\text{ cm}$, "
            "calculate the wavelength of the monochromatic light source used.\n\n"
            "**Given Data:**\n"
            "- Diameter of 10th dark ring: $D_{10} = 0.50\\text{ cm} = 5.0 \\times 10^{-3}\\text{ m}$\n"
            "- Diameter of 2nd dark ring: $D_2 = 0.22\\text{ cm} = 2.2 \\times 10^{-3}\\text{ m}$\n"
            "- Difference in ring orders: $p = 10 - 2 = 8$\n"
            "- Radius of curvature of lens: $R = 100\\text{ cm} = 1.0\\text{ m}$\n\n"
            "**Governing Formula:**\n"
            "$$\\lambda = \\frac{D_{n+p}^2 - D_n^2}{4 p R}$$\n\n"
            "**Substitution and Calculation:**\n"
            "$$D_{10}^2 = (5.0 \\times 10^{-3})^2 = 25.0 \\times 10^{-6}\\text{ m}^2$$\n"
            "$$D_2^2 = (2.2 \\times 10^{-3})^2 = 4.84 \\times 10^{-6}\\text{ m}^2$$\n"
            "$$D_{10}^2 - D_2^2 = 25.0 \\times 10^{-6} - 4.84 \\times 10^{-6} = 20.16 \\times 10^{-6}\\text{ m}^2$$\n"
            "$$\\lambda = \\frac{20.16 \\times 10^{-6}}{4 \\times 8 \\times 1.0} = \\frac{20.16 \\times 10^{-6}}{32} = 6.30 \\times 10^{-7}\\text{ m}$$\n\n"
            "**Final Answer with Units:**\n"
            "$$\\lambda = 630\\text{ nm} = 6300\\text{ \\AA}$$\n\n"
            "**Physical Interpretation:** The calculated wavelength matches standard red-orange laser illumination, "
            "confirming that differential ring diameters accurately extract optical wavelengths independent of central contact imperfections."
        )

    elif any(k in t_low for k in ["laser", "emission", "ruby", "he-ne", "einstein", "population"]):
        return (
            "### Solved Numerical Example\n\n"
            "**Problem Statement:** A Helium-Neon laser emits continuous-wave radiation at $\\lambda = 632.8\\text{ nm}$ with an output power of $5.0\\text{ mW}$. "
            "Calculate (a) the energy of each emitted photon in electron-volts, and (b) the number of photons emitted per second.\n\n"
            "**Given Data:**\n"
            "- Wavelength: $\\lambda = 632.8\\text{ nm} = 6.328 \\times 10^{-7}\\text{ m}$\n"
            "- Output power: $P = 5.0\\text{ mW} = 5.0 \\times 10^{-3}\\text{ W}$\n"
            "- Planck constant: $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$\n"
            "- Speed of light: $c = 3.0 \\times 10^8\\text{ m/s}$\n"
            "- Elementary charge: $e = 1.602 \\times 10^{-19}\\text{ J/eV}$\n\n"
            "**Governing Formulas:**\n"
            "$$E_{photon} = \\frac{hc}{\\lambda}, \\quad N = \\frac{P}{E_{photon}}$$\n\n"
            "**Substitution and Calculation:**\n"
            "$$E_{photon} = \\frac{(6.626 \\times 10^{-34}) \\times (3.0 \\times 10^8)}{6.328 \\times 10^{-7}} = \\frac{1.9878 \\times 10^{-25}}{6.328 \\times 10^{-7}} = 3.141 \\times 10^{-19}\\text{ J}$$\n"
            "$$E_{photon} = \\frac{3.141 \\times 10^{-19}\\text{ J}}{1.602 \\times 10^{-19}\\text{ J/eV}} = 1.961\\text{ eV}$$\n"
            "$$N = \\frac{5.0 \\times 10^{-3}\\text{ J/s}}{3.141 \\times 10^{-19}\\text{ J/photon}} = 1.592 \\times 10^{16}\\text{ photons/s}$$\n\n"
            "**Final Answer with Units:**\n"
            "$$E_{photon} = 1.96\\text{ eV}, \\quad N = 1.59 \\times 10^{16}\\text{ photons/s}$$\n\n"
            "**Physical Interpretation:** Each neon atom releases approximately $1.96\\text{ eV}$ during the $3s \\to 2p$ laser transition, "
            "delivering over $1.5 \\times 10^{16}$ synchronized, coherent photons per second to sustain steady CW optical power."
        )

    elif any(k in t_low for k in ["fiber", "numerical aperture", "acceptance", "step-index", "graded-index", "v-number"]):
        return (
            "### Solved Numerical Example\n\n"
            "**Problem Statement:** An optical step-index fiber has a core refractive index $n_1 = 1.50$ and a cladding refractive index $n_2 = 1.48$. "
            "Calculate (a) the critical angle at the core-cladding boundary, (b) the numerical aperture (NA), and (c) the maximum acceptance angle in air.\n\n"
            "**Given Data:**\n"
            "- Core refractive index: $n_1 = 1.50$\n"
            "- Cladding refractive index: $n_2 = 1.48$\n"
            "- Launching medium (air): $n_0 = 1.00$\n\n"
            "**Governing Formulas:**\n"
            "$$\\phi_c = \\arcsin\\left(\\frac{n_2}{n_1}\\right), \\quad \\text{NA} = \\sqrt{n_1^2 - n_2^2}, \\quad \\theta_a = \\arcsin(\\text{NA})$$\n\n"
            "**Substitution and Calculation:**\n"
            "$$\\phi_c = \\arcsin\\left(\\frac{1.48}{1.50}\\right) = \\arcsin(0.9867) = 80.64^\\circ$$\n"
            "$$\\text{NA} = \\sqrt{(1.50)^2 - (1.48)^2} = \\sqrt{2.25 - 2.1904} = \\sqrt{0.0596} = 0.2441$$\n"
            "$$\\theta_a = \\arcsin(0.2441) = 14.13^\\circ$$\n\n"
            "**Final Answer with Units:**\n"
            "$$\\phi_c = 80.6^\\circ, \\quad \\text{NA} = 0.244, \\quad \\theta_a = 14.1^\\circ$$\n\n"
            "**Physical Interpretation:** Rays entering the fiber core within an acceptance cone of semi-apex angle $14.1^\\circ$ strike the cladding "
            "at angles exceeding $80.6^\\circ$, ensuring total internal reflection and guided optical transmission."
        )

    elif any(k in t_low for k in ["relativity", "lorentz", "dilation", "contraction", "poynting", "maxwell"]):
        return (
            "### Solved Numerical Example\n\n"
            "**Problem Statement:** A subatomic particle moves with velocity $v = 0.8c$ relative to the laboratory frame. "
            "If its proper lifetime is $\\tau_0 = 2.0 \\times 10^{-8}\\text{ s}$, calculate (a) its dilated lifetime as measured by a laboratory observer, "
            "and (b) the distance it travels in the laboratory before decaying.\n\n"
            "**Given Data:**\n"
            "- Velocity: $v = 0.8c = 0.8 \\times (3.0 \\times 10^8\\text{ m/s}) = 2.4 \\times 10^8\\text{ m/s}$\n"
            "- Proper lifetime: $\\tau_0 = 2.0 \\times 10^{-8}\\text{ s}$\n\n"
            "**Governing Formulas:**\n"
            "$$\\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}, \\quad \\Delta t = \\gamma \\tau_0, \\quad d = v \\Delta t$$\n\n"
            "**Substitution and Calculation:**\n"
            "$$\\gamma = \\frac{1}{\\sqrt{1 - (0.8)^2}} = \\frac{1}{\\sqrt{1 - 0.64}} = \\frac{1}{\\sqrt{0.36}} = \\frac{1}{0.6} = 1.667$$\n"
            "$$\\Delta t = 1.667 \\times (2.0 \\times 10^{-8}\\text{ s}) = 3.333 \\times 10^{-8}\\text{ s}$$\n"
            "$$d = (2.4 \\times 10^8\\text{ m/s}) \\times (3.333 \\times 10^{-8}\\text{ s}) = 8.0\\text{ m}$$\n\n"
            "**Final Answer with Units:**\n"
            "$$\\Delta t = 3.33 \\times 10^{-8}\\text{ s}, \\quad d = 8.00\\text{ m}$$\n\n"
            "**Physical Interpretation:** Time dilation extends the particle's laboratory lifetime by 66.7%, "
            "allowing it to travel 8.0 meters in the laboratory compared to only 4.8 meters predicted by non-relativistic classical mechanics."
        )

    else:
        # Quantum numerical default
        return (
            "### Solved Numerical Example\n\n"
            "**Problem Statement:** Calculate the de Broglie wavelength associated with an electron accelerated from rest across an electrostatic potential difference of $V = 100\\text{ V}$.\n\n"
            "**Given Data:**\n"
            "- Accelerating potential difference: $V = 100\\text{ V}$\n"
            "- Electron rest mass: $m_e = 9.109 \\times 10^{-31}\\text{ kg}$\n"
            "- Elementary charge: $e = 1.602 \\times 10^{-19}\\text{ C}$\n"
            "- Planck constant: $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$\n\n"
            "**Governing Formula:**\n"
            "$$\\lambda = \\frac{h}{\\sqrt{2m_e e V}} = \\frac{1.227}{\\sqrt{V}}\\text{ nm}$$\n\n"
            "**Substitution and Calculation:**\n"
            "$$\\lambda = \\frac{1.227}{\\sqrt{100}} = \\frac{1.227}{10} = 0.1227\\text{ nm} = 1.227\\text{ \\AA}$$\n\n"
            "**Final Answer with Units:**\n"
            "$$\\lambda = 0.123\\text{ nm} = 1.23\\text{ \\AA}$$\n\n"
            "**Physical Interpretation:** The calculated wavelength matches interatomic crystal spacing, "
            "explaining why electron beams readily undergo Bragg diffraction in solid-state lattices."
        )


def generate_physics_questions(topic: str, subtopic: str) -> str:
    """Generates authentic university conceptual review questions matched to topic."""
    return (
        "### Academic Review & Conceptual Questions\n\n"
        f"1. **Conceptual Understanding:** Explain the fundamental physical mechanism of {subtopic} within the domain of {topic}. What key assumptions underpin its theoretical formulation?\n\n"
        f"2. **Analytical Derivation:** Formulate the step-by-step mathematical derivation governing {subtopic}, clearly defining all boundary constraints and conservation laws.\n\n"
        f"3. **Physical Interpretation:** Contrast the classical macroscopic behavior with the underlying wave/field phenomena that emerge in {topic}.\n\n"
        f"4. **Engineering Application:** How are the governing principles of {subtopic} applied in modern high-precision engineering, photonics, or nanoscale devices?"
    )
