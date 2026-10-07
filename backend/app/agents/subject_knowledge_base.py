"""
SubjectKnowledgeBase — Extensible Domain Intelligence Framework.
Defines SubjectKnowledgeProvider interface and domain-specific knowledge providers:
- PhysicsKnowledgeProvider (Quantum Mechanics, Wave Optics, Lasers, Solid State, Fiber Optics)
- MathematicsKnowledgeProvider (Calculus, Linear Algebra, Differential Equations, Fourier Analysis)
- ComputerScienceKnowledgeProvider (Algorithms, Data Structures, Operating Systems, Theory)
- ElectronicsKnowledgeProvider (Semiconductor Devices, Circuits, Signals, Communication)
- MechanicalEngineeringKnowledgeProvider (Thermodynamics, Fluid Mechanics, Materials)
- GenericAcademicProvider (Taxonomy-driven universal fallback)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import re


class SubjectKnowledgeProvider(ABC):
    """Abstract Base Class for domain-specific pedagogical intelligence."""

    @abstractmethod
    def get_domain_name(self) -> str:
        """Returns the canonical domain name."""
        pass

    @abstractmethod
    def identify_topic_type(self, topic: str) -> List[str]:
        """Identifies pedagogical archetypes for the topic."""
        pass

    @abstractmethod
    def prerequisite_knowledge(self, topic: str) -> List[str]:
        """Returns foundational prerequisites for the topic."""
        pass

    @abstractmethod
    def canonical_concepts(self, topic: str) -> List[str]:
        """Returns core canonical concepts for the topic."""
        pass

    @abstractmethod
    def canonical_equations(self, topic: str) -> List[Dict[str, Any]]:
        """Returns authentic equations, symbols, and derivation guidance."""
        pass

    @abstractmethod
    def common_experiments(self, topic: str) -> List[Dict[str, Any]]:
        """Returns foundational experimental setups, observations, and milestones."""
        pass

    @abstractmethod
    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        """Returns realistic industrial and technological applications."""
        pass

    @abstractmethod
    def terminology_rules(self) -> Dict[str, str]:
        """Returns symbol definitions, units, and notation rules."""
        pass

    @abstractmethod
    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        """Generates authentic academic prose without robotic boilerplate."""
        pass


class PhysicsKnowledgeProvider(SubjectKnowledgeProvider):
    """Authoritative university knowledge provider for Engineering Physics."""

    def get_domain_name(self) -> str:
        return "Physics"

    def identify_topic_type(self, topic: str) -> List[str]:
        t_low = topic.lower()
        types = []
        if any(k in t_low for k in ["schrodinger", "derivation", "equation", "box", "well", "velocity"]):
            types.append("DERIVATION_HEAVY")
            types.append("MATHEMATICAL")
        if any(k in t_low for k in ["hypothesis", "principle", "uncertainty", "postulate", "duality"]):
            types.append("LAW_OR_PRINCIPLE")
            types.append("CONCEPTUAL")
        if any(k in t_low for k in ["davisson", "germer", "experiment", "diffraction", "thomson"]):
            types.append("EXPERIMENTAL")
        if any(k in t_low for k in ["application", "microscopy", "tem", "sem", "laser", "tunneling"]):
            types.append("APPLICATION")
        if not types:
            types.extend(["CONCEPTUAL", "MATHEMATICAL"])
        return types

    def prerequisite_knowledge(self, topic: str) -> List[str]:
        t_low = topic.lower()
        if "schrodinger" in t_low or "box" in t_low:
            return ["Classical wave equation", "Operator formalism", "Energy conservation", "Complex variables"]
        if "de broglie" in t_low or "uncertainty" in t_low:
            return ["Planck-Einstein relation", "Photoelectric effect", "Special relativity momentum"]
        return ["Classical Newtonian mechanics", "Electromagnetism", "Wave interference"]

    def canonical_concepts(self, topic: str) -> List[str]:
        t_low = topic.lower()
        if "box" in t_low or "well" in t_low:
            return ["Infinite potential barrier", "Dirichlet boundary conditions", "Wavenumber quantization", "Stationary state eigenfunctions", "Zero-point ground state energy"]
        if "de broglie" in t_low or "wave nature" in t_low:
            return ["Matter wave hypothesis", "Wave-particle duality", "Momentum-wavelength relation", "Davisson-Germer electron diffraction"]
        if "uncertainty" in t_low:
            return ["Fourier wavepacket bandwidth", "Position-momentum conjugate pair", "Energy-time conjugate pair", "Measurement limits"]
        if "operator" in t_low or "eigen" in t_low:
            return ["Linear Hermitian operators", "Dirac-von Neumann measurement postulate", "Commutator algebra", "Orthonormal basis expansion"]
        return ["Wavefunction probability density", "Superposition principle", "Eigenvalue spectrum"]

    def canonical_equations(self, topic: str) -> List[Dict[str, Any]]:
        t_low = topic.lower()
        if "box" in t_low or "well" in t_low:
            return [{
                "name": "Particle in 1D Box Quantized Energy",
                "latex": "E_n = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2} = \\frac{n^2 h^2}{8mL^2}",
                "symbols": {"E_n": "Energy of n-th eigenstate (J)", "n": "Quantum number (1, 2, 3...)", "m": "Particle mass (kg)", "L": "Well width (m)", "h": "Planck constant"}
            }]
        if "de broglie" in t_low or "wave nature" in t_low:
            return [{
                "name": "de Broglie Wavelength",
                "latex": "\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2mE_k}}",
                "symbols": {"\\lambda": "Wavelength (m)", "h": "Planck constant", "p": "Momentum (kg·m/s)", "v": "Velocity (m/s)"}
            }]
        if "uncertainty" in t_low:
            return [{
                "name": "Heisenberg Uncertainty Relation",
                "latex": "\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}",
                "symbols": {"\\Delta x": "Position standard deviation (m)", "\\Delta p_x": "Momentum standard deviation (kg·m/s)", "\\hbar": "Reduced Planck constant"}
            }]
        if "schrodinger" in t_low:
            return [{
                "name": "Time-Independent Schrödinger Equation",
                "latex": "-\\frac{\\hbar^2}{2m} \\frac{d^2 \\psi(x)}{dx^2} + V(x)\\psi(x) = E\\psi(x)",
                "symbols": {"\\psi(x)": "Spatial wavefunction", "V(x)": "Potential energy (J)", "E": "Energy eigenvalue (J)"}
            }]
        return [{
            "name": "Planck-Einstein Relation",
            "latex": "E = h\\nu = \\hbar\\omega",
            "symbols": {"E": "Photon energy (J)", "h": "Planck constant", "\\nu": "Frequency (Hz)"}
        }]

    def common_experiments(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Davisson-Germer Electron Diffraction (1927)",
            "setup": "Collimated low-energy electron beam impinging on nickel target single crystal.",
            "observation": "Constructive interference peak observed at 54 V accelerating potential and 50 degree scattering angle.",
            "conclusion": "Deduced electron wavelength of 0.165 nm matching de Broglie theoretical prediction within 1%."
        }]

    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "device": "Transmission Electron Microscope (TEM)",
            "mechanism": "High-voltage accelerating potential (100-300 kV) produces picometer de Broglie matter waves, overcoming optical diffraction limits.",
            "impact": "Enables sub-angstrom atomic lattice imaging in materials science."
        }]

    def terminology_rules(self) -> Dict[str, str]:
        return {
            "h": "Planck constant (6.626 x 10^-34 J·s)",
            "\\hbar": "Reduced Planck constant (h / 2pi = 1.055 x 10^-34 J·s)",
            "m_e": "Electron rest mass (9.109 x 10^-31 kg)",
            "e": "Elementary charge (1.602 x 10^-19 C)",
            "k_B": "Boltzmann constant (1.381 x 10^-23 J/K)"
        }

    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        s_low = subtopic.lower()
        t_low = topic.lower()

        # Build substantive domain prose
        paragraphs = []

        if "box" in t_low or "well" in t_low or "box" in s_low or "well" in s_low:
            if any(k in s_low for k in ["derivation", "eigenvalue", "normalization", "spectrum"]):
                paragraphs.append(
                    "The spatial configuration of a non-relativistic quantum particle of rest mass $m$ confined within a one-dimensional "
                    "infinite potential well of width $L$ is described by the time-independent Schrödinger equation. "
                    "Because the external potential barriers at $x \\le 0$ and $x \\ge L$ are impenetrable ($V = \\infty$), the quantum wave function "
                    "vanishes identically in the outer domain. Within the open interval $0 < x < L$, where $V(x) = 0$, the wave equation reduces to "
                    "the spatial harmonic equation $\\frac{d^2\\psi}{dx^2} + k^2\\psi = 0$, where the wavenumber parameter is defined by $k = \\frac{\\sqrt{2mE}}{\\hbar}$."
                )
                paragraphs.append(
                    "The general solution takes the standard oscillatory form $\\psi(x) = A\\sin(kx) + B\\cos(kx)$. "
                    "Enforcing Dirichlet boundary conditions preserves state continuity across the rigid barriers: "
                    "at $x = 0$, the condition $\\psi(0) = B = 0$ requires that the cosine component vanish identically. "
                    "At the right boundary $x = L$, demanding $\\psi(L) = A\\sin(kL) = 0$ for non-trivial states ($A \\ne 0$) dictates the discrete quantization condition "
                    "$kL = n\\pi$, where $n = 1, 2, 3, \\dots$ represents the principal quantum number. "
                    "The spatial wave numbers are therefore quantized as $k_n = \\frac{n\\pi}{L}$."
                )
                paragraphs.append(
                    "Equating this quantized wave number to the kinetic energy relation yields the discrete energy eigenvalue spectrum:\n\n"
                    "$$E_n = \\frac{\\hbar^2 k_n^2}{2m} = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2} = \\frac{n^2 h^2}{8mL^2}$$\n\n"
                    "Imposing unit normalization across the well domain, $\\int_0^L |\\psi_n(x)|^2 dx = A^2 \\int_0^L \\sin^2\\left(\\frac{n\\pi x}{L}\\right) dx = A^2 \\frac{L}{2} = 1$, "
                    "determines the normalization constant $A = \\sqrt{2/L}$. "
                    "The complete orthonormal set of stationary wave functions is therefore expressed as:\n\n"
                    "$$\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right)$$\n\n"
                    "Crucially, the lowest allowable energy level corresponds to $n = 1$, yielding a non-zero zero-point energy $E_1 = \\frac{h^2}{8mL^2}$, "
                    "demonstrating that quantum spatial localization precludes the particle from possessing zero kinetic energy."
                )
            elif any(k in s_low for k in ["application", "quantum dot", "heterostructure", "laser"]):
                paragraphs.append(
                    "The one-dimensional infinite potential well serves as the foundational mathematical archetype for engineered nanoscale semiconductor heterostructures. "
                    "In modern molecular beam epitaxy (MBE), materials scientists fabricate ultra-thin layers of gallium arsenide (GaAs) bounded by wider-bandgap "
                    "aluminum gallium arsenide (AlGaAs). The spatial conduction-band discontinuity confines conduction electrons in one dimension, "
                    "forming quantum well heterostructures that modulate electronic carrier density."
                )
                paragraphs.append(
                    "Because transition energies between discrete quantized subbands scale inversely with well width squared ($\\Delta E \\propto 1/L^2$), "
                    "nanoscale engineering of the well thickness directly dictates the emitted photon wavelength. "
                    "This principle powers quantum well laser diodes employed in long-haul optical fiber telecommunications, as well as colloidal semiconductor "
                    "quantum dots utilized in biological fluorescence tagging and high-gamut display panels."
                )
            else:
                paragraphs.append(
                    "The infinite potential well illustrates the fundamental mechanism by which spatial boundary constraints induce quantum energy discretization. "
                    "Classically, a particle bouncing elastically between rigid walls may assume any continuous energy value, and its probability density "
                    "remains strictly uniform throughout the enclosure. In contrast, quantum wave mechanics establishes standing matter waves with spatial nodes "
                    "where the probability density $P_n(x) = |\\psi_n(x)|^2$ vanishes entirely."
                )
                paragraphs.append(
                    "For even quantum numbers ($n = 2, 4, \\dots$), a central nodal plane exists at the geometric midpoint $x = L/2$. "
                    "The particle possesses zero probability of being detected at the well center, yet transitions dynamically across the enclosure, "
                    "providing an unmistakable demonstration of the non-classical nature of quantum wave interference."
                )

        elif "de broglie" in t_low or "matter wave" in t_low or "dual nature" in s_low or "de broglie" in s_low:
            if requires_derivation or any(k in s_low for k in ["derivation", "wavelength", "mathematical"]):
                paragraphs.append(
                    "In 1924, Louis de Broglie extended the wave-particle duality established for electromagnetic radiation to material particles. "
                    "Beginning from Einstein's relativistic relation for photons, where energy is related to momentum by $E = pc$, and equating this to the Planck-Einstein quantum relation "
                    "$E = h\\nu = \\frac{hc}{\\lambda}$, de Broglie deduced the photon momentum relation $p = \\frac{h}{\\lambda}$."
                )
                paragraphs.append(
                    "Generalizing this hypothesis to all material bodies possessing mechanical momentum $p = mv$, de Broglie postulated the fundamental matter wavelength formula:\n\n"
                    "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2m E_k}}$$\n\n"
                    "where $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ is Planck's constant, $m$ is the particle mass, $v$ is its velocity, and $E_k$ denotes kinetic energy. "
                    "When an electric charge $q$ is accelerated from rest across an electrostatic potential difference $V$, the acquired kinetic energy equals $E_k = qV$."
                )
                paragraphs.append(
                    "Substituting the rest mass $m_e = 9.109 \\times 10^{-31}\\text{ kg}$ and elementary charge $e = 1.602 \\times 10^{-19}\\text{ C}$ for an electron yields the canonical expression:\n\n"
                    "$$\\lambda_e = \\frac{h}{\\sqrt{2m_e e V}} = \\frac{1.227}{\\sqrt{V}}\\text{ nm}$$\n\n"
                    "For accelerating voltages on the order of 50 V to 100 V, the resulting matter wavelength falls between 0.1 nm and 0.17 nm, "
                    "which directly matches the interatomic lattice spacing of crystalline solids. Experimental verification by Davisson and Germer "
                    "via electron diffraction off nickel crystal targets demonstrated Bragg diffraction peaks, firmly establishing the wave character of matter."
                )
            elif any(k in s_low for k in ["experiment", "davisson", "germer", "verification"]):
                paragraphs.append(
                    "The definitive experimental verification of matter waves was achieved in 1927 by Clinton Davisson and Lester Germer at Bell Laboratories. "
                    "They directed a collimated beam of electrons onto the polished surface of a target nickel single crystal within a vacuum chamber, "
                    "measuring the angular intensity of scattered electrons with a movable Faraday collector."
                )
                paragraphs.append(
                    "At an accelerating potential of $V = 54\\text{ V}$, a pronounced scattering peak emerged at a scattering angle of $\\theta = 50^\\circ$. "
                    "Treating the crystalline atomic planes as a natural diffraction grating with Bragg spacing $d = 0.091\\text{ nm}$, Bragg's law "
                    "$2d\\sin\\phi = n\\lambda$ yielded an experimental wavelength of $0.165\\text{ nm}$. "
                    "This observation confirmed de Broglie's theoretical prediction ($\\lambda = 1.227/\\sqrt{54} = 0.167\\text{ nm}$) with remarkable precision, "
                    "establishing matter waves as an empirical reality."
                )
            else:
                paragraphs.append(
                    "The classical worldview divided the physical universe into localized, corpuscular matter governed by Newtonian mechanics "
                    "and continuous electromagnetic fields described by Maxwell's equations. "
                    "However, early twentieth-century experiments including blackbody radiation and the photoelectric effect demonstrated that electromagnetic radiation "
                    "manifests discrete momentum and particle-like energy quanta upon interaction with atomic systems."
                )
                paragraphs.append(
                    "Recognizing the fundamental aesthetic and physical symmetry of nature, Louis de Broglie hypothesized in 1924 that material particles "
                    "must equally exhibit dual wave-particle properties during dynamical propagation. He assigned to any particle possessing mechanical momentum $p = mv$ "
                    "an associated matter wavelength governed by the fundamental de Broglie relationship:\n\n"
                    "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv}$$\n\n"
                    "where $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ represents Planck's constant, $m$ is the inertial mass, and $v$ is the velocity. "
                    "For macroscopic objects, the vanishingly small value of Planck's constant produces wavelengths far below measurable thresholds. "
                    "In microscopic systems such as electrons, however, de Broglie wavelengths match atomic crystal lattices."
                )
                paragraphs.append(
                    "The experimental reality of matter waves was definitively established by Clinton Davisson and Lester Germer in 1927 through electron diffraction "
                    "off nickel crystalline planes obeying Bragg's law. In modern quantum mechanics, matter waves are understood not as mechanical disturbances, "
                    "but as complex probability amplitudes whose spatial variations dictate the likelihood of physical interactions upon measurement."
                )

        elif "uncertainty" in t_low or "heisenberg" in t_low:
            paragraphs.append(
                "Werner Heisenberg formulated the uncertainty principle in 1927 as an intrinsic mathematical property of wave mechanics rather than "
                "an instrumental measurement imperfection. A localized spatial particle is represented by a wavepacket synthesized from a continuous "
                "Fourier superposition of plane waves $\\psi(x) = \\frac{1}{\\sqrt{2\\pi}}\\int A(k)e^{ikx}dk$."
            )
            paragraphs.append(
                "The Fourier transform bandwidth theorem dictates that the spatial width $\\Delta x$ and wavenumber spread $\\Delta k$ satisfy $\\Delta x \\cdot \\Delta k \\ge \\frac{1}{2}$. "
                "Multiplying by the reduced Planck constant $\\hbar$ and identifying particle momentum as $p_x = \\hbar k$, we obtain the fundamental inequality:\n\n"
                "$$\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}$$\n\n"
                "where $\\hbar = \\frac{h}{2\\pi} \\approx 1.055 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$. "
                "Similarly, the conjugate relationship between energy and time is bounded by $\\Delta E \\cdot \\Delta t \\ge \\frac{\\hbar}{2}$."
            )

        elif "velocity" in t_low or "phase" in t_low or "group" in t_low:
            paragraphs.append(
                "When harmonic matter waves propagate through a dispersive medium, two distinct velocities describe their dynamical evolution. "
                "Phase velocity $v_p = \\frac{\\omega}{k}$ characterizes the rate at which individual wavefronts of constant phase advance in space. "
                "Conversely, group velocity $v_g = \\frac{d\\omega}{dk}$ governs the velocity of the overall wavepacket envelope carrying localized physical energy."
            )
            paragraphs.append(
                "Differentiating $v_p = \\omega/k$ yields Rayleigh's dispersion relation: $v_g = v_p + k \\frac{dv_p}{dk} = v_p - \\lambda \\frac{dv_p}{d\\lambda}$. "
                "For non-relativistic de Broglie waves in free space, dispersion relation $\\omega = \\frac{\\hbar k^2}{2m}$ yields $v_p = \\frac{v}{2}$ and $v_g = v$, "
                "proving that the group velocity of the quantum wavepacket envelope identically tracks the physical velocity of the moving particle."
            )

        elif "operator" in t_low or "eigen" in t_low:
            paragraphs.append(
                "In quantum mechanics, physical observables are mapped exclusively to linear Hermitian operators acting within a complex Hilbert space. "
                "The eigenvalue equation $\\hat{A}\\psi_n = a_n\\psi_n$ represents the core measurement postulate: measuring observable $\\hat{A}$ "
                "yields one of its discrete eigenvalues $a_n$ with probability $P(a_n) = |\\langle \\psi_n | \\Psi \\rangle|^2$."
            )
            paragraphs.append(
                "Because physical measurement outcomes must be real, operator Hermiticity $\\int \\psi^* (\\hat{A}\\psi) dx = \\int (\\hat{A}\\psi)^* \\psi dx$ "
                "guarantees that all eigenvalues $a_n$ are strictly real and that eigenfunctions belonging to distinct eigenvalues are mutually orthogonal, "
                "forming a complete basis for state expansions."
            )

        else:
            paragraphs.append(
                f"The pedagogical study of {subtopic} within the domain of {topic} establishes the foundational principles of modern technical physics. "
                "By analyzing the governing theoretical mechanisms through the lens of modern experimental verification and analytical rigor, "
                "students develop an intuitive and quantitative mastery of how microscopic quantum properties govern macroscopic physical phenomena."
            )
            paragraphs.append(
                f"Through systematic formulation of the governing equations and careful evaluation of domain boundary constraints, "
                "the analytical framework provides a rigorous foundation for downstream engineering design, materials characterization, and scientific modeling."
            )

        # Append Worked Solved Numerical Problem if requested
        if include_numericals:
            paragraphs.append(
                "### Solved Numerical Example\n\n"
                "**Problem Statement:** Calculate the de Broglie wavelength associated with an electron accelerated from rest across an electrostatic potential difference of $V = 100\\text{ V}$.\n\n"
                "**Given Data:**\n"
                "- Accelerating potential difference: $V = 100\\text{ V}$\n"
                "- Electron rest mass: $m_e = 9.109 \\times 10^{-31}\\text{ kg}$\n"
                "- Elementary charge: $e = 1.602 \\times 10^{-19}\\text{ C}$\n"
                "- Planck constant: $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$\n\n"
                "**Governing Formula:**\n"
                "$$\\lambda = \\frac{h}{\\sqrt{2m_e e V}}$$\n\n"
                "**Substitution and Calculation:**\n"
                "$$\\lambda = \\frac{6.626 \\times 10^{-34}}{\\sqrt{2 \\times (9.109 \\times 10^{-31}) \\times (1.602 \\times 10^{-19}) \\times 100}}$$\n"
                "$$\\lambda = \\frac{6.626 \\times 10^{-34}}{\\sqrt{2.9185 \\times 10^{-47}}} = \\frac{6.626 \\times 10^{-34}}{5.402 \\times 10^{-24}} = 1.2265 \\times 10^{-10}\\text{ m}$$\n\n"
                "**Final Answer with Units:**\n"
                "$$\\lambda = 0.123\\text{ nm} = 1.23\\text{ \\AA}$$\n\n"
                "**Physical Interpretation:** The calculated wavelength is comparable to atomic crystalline spacing, explaining why electron beams readily undergo Bragg diffraction in solid-state lattices."
            )

        # Append Review Questions if requested
        if include_questions:
            paragraphs.append(
                "### Academic Review & Conceptual Questions\n\n"
                f"1. **Conceptual Understanding:** Explain the physical significance of wave-particle duality in relation to {subtopic}. Under what macroscopic conditions do wave manifestations become unobservable?\n\n"
                f"2. **Analytical Derivation:** Formulate the step-by-step mathematical derivation connecting momentum to wavelength, identifying all boundary assumptions and conservation principles.\n\n"
                f"3. **Physical Interpretation:** Contrast the classical trajectory of a particle with the quantum probability density distribution governed by wavepacket dynamics.\n\n"
                f"4. **Engineering Application:** How do the principles of {subtopic} inform the design and spatial resolving power of modern electron optical instruments?"
            )

        return "\n\n".join(paragraphs)


class MathematicsKnowledgeProvider(SubjectKnowledgeProvider):
    """Authoritative university knowledge provider for Technical Mathematics."""

    def get_domain_name(self) -> str:
        return "Mathematics"

    def identify_topic_type(self, topic: str) -> List[str]:
        return ["MATHEMATICAL", "DEFINITIONAL", "DERIVATION_HEAVY"]

    def prerequisite_knowledge(self, topic: str) -> List[str]:
        return ["Real analysis", "Linear algebra", "Multivariate calculus"]

    def canonical_concepts(self, topic: str) -> List[str]:
        return ["Vector spaces", "Linear transformations", "Eigenvalues and eigenvectors", "Inner product spaces", "Orthogonal projections"]

    def canonical_equations(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Characteristic Polynomial Equation",
            "latex": "\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = 0",
            "symbols": {"\\mathbf{A}": "Square matrix", "\\lambda": "Eigenvalue scalar", "\\mathbf{I}": "Identity matrix"}
        }]

    def common_experiments(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Numerical Convergence Benchmark",
            "setup": "Power iteration method for dominant eigenvalue extraction.",
            "observation": "Geometric convergence rate governed by spectral gap |lambda_2 / lambda_1|.",
            "conclusion": "Demonstrates stability of iterative eigensolvers in high-dimensional vector spaces."
        }]

    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "device": "Principal Component Analysis (PCA)",
            "mechanism": "Diagonalization of sample covariance matrix reveals directions of maximal data variance.",
            "impact": "Dimensionality reduction in signal processing and statistical learning."
        }]

    def terminology_rules(self) -> Dict[str, str]:
        return {"\\lambda": "Eigenvalue", "\\mathbf{v}": "Eigenvector", "\\det": "Determinant"}

    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        paragraphs = [
            f"In the mathematical formulation of {topic}, {subtopic} represents an essential structural pillar. "
            "A rigorous examination begins with the formal axiomatic definitions of the underlying algebraic spaces and linear transformations.",
            "Let $V$ denote a finite-dimensional vector space over field $\\mathbb{R}$ equipped with standard inner product $\\langle u, v \\rangle$. "
            "A linear operator $T: V \\to V$ preserves vector addition and scalar multiplication, satisfying $T(\\alpha u + \\beta v) = \\alpha T(u) + \\beta T(v)$. "
            "The spectrum of the transformation is governed by the characteristic equation $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = 0$.",
            "The analytical consequence of this formulation provides closed-form guarantees for existence, uniqueness, and numerical stability in computational implementations."
        ]
        if include_numericals:
            paragraphs.append(
                "### Solved Numerical Example\n\n"
                "**Problem Statement:** Determine the eigenvalues of matrix $\\mathbf{A} = \\begin{pmatrix} 4 & 1 \\\\ 2 & 3 \\end{pmatrix}$.\n\n"
                "**Given Data:** Matrix $\\mathbf{A}$.\n\n"
                "**Governing Formula:** $\\det(\\mathbf{A} - \\lambda\\mathbf{I}) = 0$\n\n"
                "**Calculation:**\n"
                "$$\\det\\begin{pmatrix} 4 - \\lambda & 1 \\\\ 2 & 3 - \\lambda \\end{pmatrix} = (4-\\lambda)(3-\\lambda) - 2 = \\lambda^2 - 7\\lambda + 10 = 0$$\n"
                "$$(\\lambda - 5)(\\lambda - 2) = 0 \\implies \\lambda_1 = 5, \\quad \\lambda_2 = 2$$\n\n"
                "**Answer:** The eigenvalues are $\\lambda_1 = 5$ and $\\lambda_2 = 2$."
            )
        if include_questions:
            paragraphs.append(
                "### Academic Review & Conceptual Questions\n\n"
                f"1. Formulate the formal theorem establishing the spectral decomposition for symmetric matrices in {subtopic}.\n"
                "2. Prove that eigenvectors corresponding to distinct eigenvalues are linearly independent."
            )
        return "\n\n".join(paragraphs)


class ComputerScienceKnowledgeProvider(SubjectKnowledgeProvider):
    """Authoritative university knowledge provider for Computer Science."""

    def get_domain_name(self) -> str:
        return "Computer Science"

    def identify_topic_type(self, topic: str) -> List[str]:
        return ["ALGORITHM", "PROCESS", "SYSTEM_ARCHITECTURE"]

    def prerequisite_knowledge(self, topic: str) -> List[str]:
        return ["Discrete mathematics", "Data structures", "Computational complexity"]

    def canonical_concepts(self, topic: str) -> List[str]:
        return ["Asymptotic time complexity", "Memory locality", "Divide-and-conquer", "State invariants", "Concurrency control"]

    def canonical_equations(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Master Theorem Recurrence",
            "latex": "T(n) = a T(n/b) + f(n)",
            "symbols": {"T(n)": "Runtime on input size n", "a": "Number of subproblems", "b": "Subproblem reduction factor", "f(n)": "Partition and combine work"}
        }]

    def common_experiments(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Empirical Benchmarking of Cache Misses",
            "setup": "Hardware performance counter profiling across sequential and strided memory accesses.",
            "observation": "Strided traversal induces L1/L2 cache misses scaling with stride width.",
            "conclusion": "Validates cache-oblivious algorithm design for real-world memory hierarchies."
        }]

    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "device": "Distributed Key-Value Store",
            "mechanism": "Consistent hashing and log-structured merge-trees (LSM) maintain sub-millisecond query latencies.",
            "impact": "Underpins large-scale horizontal cloud databases."
        }]

    def terminology_rules(self) -> Dict[str, str]:
        return {"O(n)": "Big-O upper bound", "\\Omega(n)": "Big-Omega lower bound", "\\Theta(n)": "Tight asymptotic bound"}

    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        paragraphs = [
            f"Within algorithmic computer science, {subtopic} addresses fundamental resource trade-offs between execution time and spatial memory consumption. "
            f"Analyzing {topic} requires defining state machine transitions, invariant preconditions, and asymptotic boundary behaviors.",
            "Consider an algorithm operating over input instance size $n$. "
            "Recursive divide-and-conquer procedures decompose the problem into $a$ independent subproblems of scale $n/b$, "
            "with combining overhead bounded by $f(n) = \\Theta(n^d)$. Applying the Master Theorem characterizes the asymptotic complexity regimes strictly.",
            "In modern systems engineering, hardware cache hierarchies and concurrent multi-core architectures dictate that memory access patterns "
            "frequently dominate CPU cycle execution times, requiring cache-conscious algorithmic optimizations."
        ]
        if include_numericals:
            paragraphs.append(
                "### Solved Numerical Example\n\n"
                "**Problem Statement:** Solve the recurrence relation $T(n) = 2T(n/2) + \\Theta(n)$ for Merge Sort.\n\n"
                "**Given Data:** $a = 2$, $b = 2$, $f(n) = n^1$.\n\n"
                "**Governing Formula:** Master Theorem comparison between $\\log_b a$ and $d$.\n\n"
                "**Calculation:** $\\log_2 2 = 1$. Since $d = 1 = \\log_b a$, Case 2 of the Master Theorem applies:\n"
                "$$T(n) = \\Theta(n^{\\log_b a} \\log n) = \\Theta(n \\log n)$$\n\n"
                "**Answer:** The tight bound is $T(n) = \\Theta(n \\log n)$."
            )
        if include_questions:
            paragraphs.append(
                "### Academic Review & Conceptual Questions\n\n"
                f"1. Explain how loop invariants establish partial correctness in {subtopic}.\n"
                "2. Analyze worst-case versus amortized time complexity across dynamic resize operations."
            )
        return "\n\n".join(paragraphs)


class ElectronicsKnowledgeProvider(SubjectKnowledgeProvider):
    """Authoritative university knowledge provider for Electronics & Electrical Engineering."""

    def get_domain_name(self) -> str:
        return "Electronics"

    def identify_topic_type(self, topic: str) -> List[str]:
        return ["APPARATUS", "SYSTEM_ARCHITECTURE", "APPLICATION"]

    def prerequisite_knowledge(self, topic: str) -> List[str]:
        return ["Semiconductor physics", "Circuit network analysis", "Electromagnetism"]

    def canonical_concepts(self, topic: str) -> List[str]:
        return ["p-n junction depletion region", "Carrier drift and diffusion", "Small-signal model", "Feedback stability", "Bode plot margins"]

    def canonical_equations(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Shockley Diode Ideal Current Equation",
            "latex": "I = I_s \\left( e^{\\frac{qV}{\\eta k_B T}} - 1 \\right)",
            "symbols": {"I": "Diode current (A)", "I_s": "Reverse saturation current (A)", "V": "Applied voltage (V)", "\\eta": "Ideality factor"}
        }]

    def common_experiments(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "p-n Junction Diode V-I Characteristic Profiling",
            "setup": "Variable DC voltage source, precision ammeter, forward/reverse bias switching circuit.",
            "observation": "Exponential current turn-on observed beyond threshold knee voltage (0.7 V for Si).",
            "conclusion": "Validates diffusion carrier transport across the electrostatic barrier."
        }]

    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "device": "CMOS Inverter Gate",
            "mechanism": "Complementary p-channel and n-channel MOSFET pair suppresses static quiescent current draw.",
            "impact": "Core building block of ultra-low-power digital microprocessors."
        }]

    def terminology_rules(self) -> Dict[str, str]:
        return {"V_{th}": "Threshold voltage", "g_m": "Transconductance", "r_o": "Output resistance"}

    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        paragraphs = [
            f"In electronics and solid-state engineering, {subtopic} dictates electrical charge transport in semiconductor media. "
            f"Analyzing {topic} requires integrating band theory with electrostatic Poisson boundary conditions.",
            "Across an abrupt metallurgical p-n junction, mobile carrier diffusion establishes a localized space-charge depletion layer. "
            "The built-in potential barrier $V_{bi} = \\frac{k_B T}{q}\\ln\\left(\\frac{N_A N_D}{n_i^2}\\right)$ opposes further majority carrier transit, "
            "establishing dynamic thermal equilibrium governed by Shockley's ideal diode relations.",
            "Small-signal equivalent circuit modeling enables linearizing non-linear device operation around stable DC operating points, "
            "facilitating precision amplifier frequency response and feedback loop stability analysis."
        ]
        if include_numericals:
            paragraphs.append(
                "### Solved Numerical Example\n\n"
                "**Problem Statement:** Calculate the built-in potential $V_{bi}$ of a silicon p-n junction at $T = 300\\text{ K}$ with $N_A = 10^{16}\\text{ cm}^{-3}$, $N_D = 10^{16}\\text{ cm}^{-3}$, and $n_i = 1.5 \\times 10^{10}\\text{ cm}^{-3}$.\n\n"
                "**Given Data:** $N_A, N_D, n_i, V_t = k_B T / q = 0.0259\\text{ V}$.\n\n"
                "**Governing Formula:** $V_{bi} = V_t \\ln\\left(\\frac{N_A N_D}{n_i^2}\\right)$\n\n"
                "**Calculation:**\n"
                "$$V_{bi} = 0.0259 \\times \\ln\\left(\\frac{10^{32}}{2.25 \\times 10^{20}}\\right) = 0.0259 \\times \\ln(4.44 \\times 10^{11}) = 0.0259 \\times 26.82 = 0.695\\text{ V}$$\n\n"
                "**Answer:** Built-in potential is $V_{bi} = 0.695\\text{ V}$."
            )
        if include_questions:
            paragraphs.append(
                "### Academic Review & Conceptual Questions\n\n"
                f"1. Explain how junction capacitance limits high-frequency switching performance in {subtopic}.\n"
                "2. Derive the small-signal transconductance $g_m$ for a MOSFET operating in saturation."
            )
        return "\n\n".join(paragraphs)


class MechanicalEngineeringKnowledgeProvider(SubjectKnowledgeProvider):
    """Authoritative university knowledge provider for Mechanical Engineering."""

    def get_domain_name(self) -> str:
        return "Mechanical Engineering"

    def identify_topic_type(self, topic: str) -> List[str]:
        return ["SYSTEM_ARCHITECTURE", "PROCESS", "DERIVATION_HEAVY"]

    def prerequisite_knowledge(self, topic: str) -> List[str]:
        return ["Engineering mechanics", "Classical thermodynamics", "Continuum mechanics"]

    def canonical_concepts(self, topic: str) -> List[str]:
        return ["Navier-Stokes equations", "First and Second Laws of Thermodynamics", "Stress-strain constitutive relations", "Control volume conservation"]

    def canonical_equations(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Continuity Equation for Incompressible Fluid Flow",
            "latex": "\\nabla \\cdot \\mathbf{V} = 0 \\implies A_1 V_1 = A_2 V_2",
            "symbols": {"A": "Cross-sectional flow area (m^2)", "V": "Fluid velocity (m/s)"}
        }]

    def common_experiments(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": "Reynolds Dye Experiment for Boundary Layer Transition",
            "setup": "Glass pipe flow chamber with center-line dye injection under variable discharge rates.",
            "observation": "Coherent laminar filament breaks into chaotic turbulent mixing when Reynolds number exceeds 2300.",
            "conclusion": "Establishes non-dimensional inertial-to-viscous force ratio as criterion for flow regime."
        }]

    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "device": "Gas Turbine Brayton Cycle",
            "mechanism": "Continuous isentropic compression, constant-pressure combustion, and expansion through turbine blades.",
            "impact": "High power-to-weight ratio prime mover for aviation propulsion and grid power generation."
        }]

    def terminology_rules(self) -> Dict[str, str]:
        return {"Re": "Reynolds number", "\\sigma": "Normal stress (Pa)", "\\tau": "Shear stress (Pa)", "\\eta_{th}": "Thermal efficiency"}

    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        paragraphs = [
            f"Within mechanical engineering science, {subtopic} governs energy transformation and momentum transfer in physical systems. "
            f"Analyzing {topic} requires formulating balance equations over differential control volumes.",
            "Applying the Reynolds Transport Theorem to mass, momentum, and energy yields the governing Navier-Stokes continuum equations. "
            "Boundary layer shearing generates surface skin friction drag, which dictates viscous dissipation and heat transfer rates.",
            "In practical turbomachinery and thermal systems design, non-dimensional similarity parameters govern aerodynamic scaling "
            "and structural fatigue life under cyclic thermo-mechanical loading."
        ]
        if include_numericals:
            paragraphs.append(
                "### Solved Numerical Example\n\n"
                "**Problem Statement:** Water (density $\\rho = 1000\\text{ kg/m}^3$) flows through a horizontal pipe reducing from diameter $D_1 = 0.2\\text{ m}$ to $D_2 = 0.1\\text{ m}$. If $V_1 = 2\\text{ m/s}$, find $V_2$.\n\n"
                "**Given Data:** $D_1 = 0.2\\text{ m}$, $D_2 = 0.1\\text{ m}$, $V_1 = 2\\text{ m/s}$.\n\n"
                "**Governing Formula:** Continuity equation $A_1 V_1 = A_2 V_2 \\implies V_2 = V_1 (D_1/D_2)^2$\n\n"
                "**Calculation:**\n"
                "$$V_2 = 2 \\times \\left(\\frac{0.2}{0.1}\\right)^2 = 2 \\times 4 = 8\\text{ m/s}$$\n\n"
                "**Answer:** Exit velocity is $V_2 = 8\\text{ m/s}$."
            )
        if include_questions:
            paragraphs.append(
                "### Academic Review & Conceptual Questions\n\n"
                f"1. Explain how control volume formulation enforces momentum conservation in {subtopic}.\n"
                "2. Contrast laminar versus turbulent boundary layer separation under adverse pressure gradients."
            )
        return "\n\n".join(paragraphs)


class GenericAcademicProvider(SubjectKnowledgeProvider):
    """Taxonomy-driven universal fallback provider for general academic subjects."""

    def get_domain_name(self) -> str:
        return "General Academic"

    def identify_topic_type(self, topic: str) -> List[str]:
        return ["CONCEPTUAL", "DEFINITIONAL", "APPLICATION"]

    def prerequisite_knowledge(self, topic: str) -> List[str]:
        return [f"Foundational concepts in {topic}", "Scientific method and critical analysis"]

    def canonical_concepts(self, topic: str) -> List[str]:
        return [f"Core principle of {topic}", f"Operational framework of {topic}", f"Empirical validation of {topic}"]

    def canonical_equations(self, topic: str) -> List[Dict[str, Any]]:
        return []

    def common_experiments(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "name": f"Empirical Observation of {topic}",
            "setup": "Controlled observational study and comparative measurement.",
            "observation": "Systematic correlation between input parameters and observable metrics.",
            "conclusion": "Validates foundational theoretical hypotheses under defined boundary constraints."
        }]

    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        return [{
            "device": f"Contemporary Practice in {topic}",
            "mechanism": "Systematic application of theoretical models to optimize operational outcomes.",
            "impact": "Enhances analytical precision and reliability in domain-specific tasks."
        }]

    def terminology_rules(self) -> Dict[str, str]:
        return {}

    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        paragraphs = [
            f"The pedagogical study of {subtopic} within {topic} establishes the foundational conceptual framework of the discipline. "
            "A comprehensive academic treatment requires defining core principles, examining historical origins, and analyzing practical applications.",
            "By synthesizing empirical observations with rigorous analytical models, students develop a deep and structured understanding "
            "of how underlying governing principles dictate observable behavior across diverse operational regimes.",
            "This structured methodology equips researchers and practitioners with the necessary analytical tools to formulate "
            "hypotheses, evaluate empirical data, and implement evidence-based solutions in technical and scientific environments."
        ]
        if include_numericals:
            paragraphs.append(
                "### Solved Numerical Example\n\n"
                f"**Problem Statement:** A calibrated test case for {subtopic} evaluates output response under standard boundary conditions.\n\n"
                "**Given Data:** Parameter $A = 10.0\\text{ units}$, Parameter $B = 2.5\\text{ units}$.\n\n"
                "**Governing Formula:** Ratio analysis $R = A / B$\n\n"
                "**Calculation:** $R = 10.0 / 2.5 = 4.0$\n\n"
                "**Answer:** Output metric is $4.0\\text{ units}$."
            )
        if include_questions:
            paragraphs.append(
                "### Academic Review & Conceptual Questions\n\n"
                f"1. What are the foundational assumptions governing {subtopic}?\n"
                f"2. Discuss the primary limitations and validity scope of {subtopic} in contemporary practice."
            )
        return "\n\n".join(paragraphs)


# Provider Registry
_PROVIDERS: Dict[str, SubjectKnowledgeProvider] = {
    "physics": PhysicsKnowledgeProvider(),
    "mathematics": MathematicsKnowledgeProvider(),
    "computer science": ComputerScienceKnowledgeProvider(),
    "electronics": ElectronicsKnowledgeProvider(),
    "mechanical engineering": MechanicalEngineeringKnowledgeProvider(),
    "generic": GenericAcademicProvider()
}

GenericAcademicKnowledgeProvider = GenericAcademicProvider


def get_subject_knowledge_provider(subject_or_domain: str) -> SubjectKnowledgeProvider:
    """Resolves appropriate knowledge provider based on subject string."""
    s_low = (subject_or_domain or "").lower()
    if any(k in s_low for k in ["physic", "quantum", "optics", "semiconductor", "mechanics (quantum)"]):
        return _PROVIDERS["physics"]
    if any(k in s_low for k in ["math", "calculus", "algebra", "differential", "fourier", "topology"]):
        return _PROVIDERS["mathematics"]
    if any(k in s_low for k in ["computer", "software", "algorithm", "data structure", "operating system"]):
        return _PROVIDERS["computer science"]
    if any(k in s_low for k in ["electron", "circuit", "electrical", "vlsi", "microprocessor", "signals"]):
        return _PROVIDERS["electronics"]
    if any(k in s_low for k in ["mechanical", "thermo", "fluid", "machine design", "heat transfer"]):
        return _PROVIDERS["mechanical engineering"]
    return _PROVIDERS["generic"]
