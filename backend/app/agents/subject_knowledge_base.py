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
        if any(k in t_low for k in ["interference", "diffraction", "polarization", "optic", "newton", "young", "grating"]):
            return ["Electromagnetic wave theory", "Huygens wavelets", "Harmonic oscillation superposition", "Complex amplitudes"]
        if any(k in t_low for k in ["laser", "emission", "absorption", "population", "ruby", "he-ne"]):
            return ["Atomic energy levels", "Boltzmann distribution", "Thermodynamic equilibrium", "Resonant cavity modes"]
        if any(k in t_low for k in ["fiber", "optical fiber", "numerical aperture", "v-number", "attenuation", "dispersion"]):
            return ["Snell's law of refraction", "Dielectric boundary conditions", "Total internal reflection", "Waveguide modes"]
        if any(k in t_low for k in ["maxwell", "gauss", "faraday", "ampere", "poynting", "relativity", "lorentz", "dilation"]):
            return ["Vector calculus (gradient, divergence, curl)", "Electrostatics and magnetostatics", "Galilean transformations", "Inertial frames"]
        if "schrodinger" in t_low or "box" in t_low:
            return ["Classical wave equation", "Operator formalism", "Energy conservation", "Complex variables"]
        if "de broglie" in t_low or "uncertainty" in t_low:
            return ["Planck-Einstein relation", "Photoelectric effect", "Special relativity momentum"]
        return ["Classical Newtonian mechanics", "Electromagnetism", "Wave interference"]

    def canonical_concepts(self, topic: str) -> List[str]:
        t_low = topic.lower()
        if any(k in t_low for k in ["interference", "optic", "young", "thin film", "newton", "coherent"]):
            return ["Superposition of harmonic fields", "Division of wavefront vs amplitude", "Stokes phase change upon reflection", "Newton's rings variable air wedge", "Fringe visibility"]
        if any(k in t_low for k in ["diffraction", "grating", "resolving", "polarization", "brewster"]):
            return ["Fraunhofer far-field diffraction", "Single-slit sinc intensity envelope", "Grating principal maxima", "Rayleigh criterion for resolution", "Brewster polarizing angle"]
        if any(k in t_low for k in ["laser", "emission", "population", "ruby", "he-ne", "metastable"]):
            return ["Stimulated vs spontaneous emission", "Einstein A and B transition probabilities", "Population inversion condition", "Metastable level accumulation", "Fabry-Perot resonator feedback"]
        if any(k in t_low for k in ["fiber", "numerical aperture", "acceptance", "step-index", "graded-index", "v-number"]):
            return ["Core-cladding dielectric interface", "Critical angle for total internal reflection", "Numerical aperture and acceptance cone", "Normalized frequency V-number", "Intermodal and chromatic dispersion"]
        if any(k in t_low for k in ["maxwell", "gauss", "faraday", "ampere", "displacement", "poynting"]):
            return ["Differential Maxwell equations", "Ampere-Maxwell displacement current density", "Electromagnetic 3D wave equation", "Intrinsic vacuum wave impedance", "Poynting power flux vector"]
        if any(k in t_low for k in ["relativity", "lorentz", "dilation", "contraction", "michelson", "mass-energy"]):
            return ["Michelson-Morley null ether result", "Einstein relativity postulates", "Spacetime Lorentz transformations", "Relativistic time dilation", "Mass-energy equivalence E=mc^2"]
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
        if any(k in t_low for k in ["interference", "young", "fringe"]):
            return [{
                "name": "Young's Double Slit Fringe Width",
                "latex": "\\beta = \\frac{\\lambda D}{d}",
                "symbols": {"\\beta": "Fringe width (m)", "\\lambda": "Wavelength (m)", "D": "Slit-to-screen distance (m)", "d": "Slit separation (m)"}
            }]
        if any(k in t_low for k in ["newton", "ring"]):
            return [{
                "name": "Newton's Rings Dark Ring Diameter",
                "latex": "D_n^2 = 4n\\lambda R",
                "symbols": {"D_n": "Diameter of n-th dark ring (m)", "n": "Ring order index", "\\lambda": "Wavelength (m)", "R": "Radius of lens curvature (m)"}
            }]
        if any(k in t_low for k in ["diffraction", "grating"]):
            return [{
                "name": "Plane Diffraction Grating Equation",
                "latex": "(a + b) \\sin\\theta = n \\lambda",
                "symbols": {"(a+b)": "Grating element (m)", "\\theta": "Diffraction angle", "n": "Spectral order", "\\lambda": "Wavelength (m)"}
            }]
        if any(k in t_low for k in ["polarization", "brewster"]):
            return [{
                "name": "Brewster's Law",
                "latex": "\\tan\\theta_p = \\mu",
                "symbols": {"\\theta_p": "Brewster polarizing angle", "\\mu": "Refractive index of medium"}
            }]
        if any(k in t_low for k in ["laser", "einstein", "emission"]):
            return [{
                "name": "Einstein Transition Coefficients Ratio",
                "latex": "\\frac{A_{21}}{B_{21}} = \\frac{8\\pi h \\nu^3}{c^3}",
                "symbols": {"A_{21}": "Spontaneous emission coefficient (s^-1)", "B_{21}": "Stimulated emission coefficient", "h": "Planck constant", "\\nu": "Transition frequency (Hz)", "c": "Speed of light (m/s)"}
            }]
        if any(k in t_low for k in ["fiber", "numerical aperture", "acceptance"]):
            return [{
                "name": "Fiber Numerical Aperture & Acceptance Angle",
                "latex": "\\text{NA} = \\sqrt{n_1^2 - n_2^2} = n_1 \\sqrt{2\\Delta}, \\quad \\theta_a = \\arcsin(\\text{NA})",
                "symbols": {"\\text{NA}": "Numerical aperture", "n_1": "Core refractive index", "n_2": "Cladding refractive index", "\\Delta": "Fractional index difference", "\\theta_a": "Acceptance angle"}
            }]
        if any(k in t_low for k in ["v-number", "cutoff", "single mode"]):
            return [{
                "name": "Fiber Normalized Frequency (V-Number)",
                "latex": "V = \\frac{2\\pi a}{\\lambda} \\text{NA} = \\frac{2\\pi a}{\\lambda} \\sqrt{n_1^2 - n_2^2}",
                "symbols": {"V": "Normalized frequency parameter", "a": "Core radius (m)", "\\lambda": "Wavelength (m)", "\\text{NA}": "Numerical aperture"}
            }]
        if any(k in t_low for k in ["ampere", "displacement", "maxwell"]):
            return [{
                "name": "Ampere-Maxwell Equation with Displacement Current",
                "latex": "\\nabla \\times \\mathbf{B} = \\mu_0 \\mathbf{J} + \\mu_0 \\epsilon_0 \\frac{\\partial \\mathbf{E}}{\\partial t}",
                "symbols": {"\\mathbf{B}": "Magnetic flux density (T)", "\\mu_0": "Permeability of vacuum", "\\mathbf{J}": "Conduction current density", "\\epsilon_0": "Permittivity of vacuum", "\\mathbf{E}": "Electric field (V/m)"}
            }]
        if any(k in t_low for k in ["wave equation", "propagation", "impedance"]):
            return [{
                "name": "Electromagnetic Wave Equation in Vacuum",
                "latex": "\\nabla^2 \\mathbf{E} - \\mu_0\\epsilon_0 \\frac{\\partial^2 \\mathbf{E}}{\\partial t^2} = 0, \\quad c = \\frac{1}{\\sqrt{\\mu_0\\epsilon_0}}",
                "symbols": {"\\mathbf{E}": "Electric field vector", "c": "Speed of light (2.998e8 m/s)", "\\mu_0": "Vacuum permeability", "\\epsilon_0": "Vacuum permittivity"}
            }]
        if any(k in t_low for k in ["poynting"]):
            return [{
                "name": "Poynting Vector & Power Density",
                "latex": "\\mathbf{S} = \\frac{1}{\\mu_0} (\\mathbf{E} \\times \\mathbf{B}), \\quad \\nabla \\cdot \\mathbf{S} + \\frac{\\partial u}{\\partial t} = -\\mathbf{J}\\cdot\\mathbf{E}",
                "symbols": {"\\mathbf{S}": "Poynting power flux vector (W/m^2)", "u": "EM energy density (J/m^3)", "\\mathbf{E}": "Electric field", "\\mathbf{B}": "Magnetic field"}
            }]
        if any(k in t_low for k in ["lorentz", "relativity", "transformation"]):
            return [{
                "name": "Lorentz Space-Time Transformations",
                "latex": "x' = \\gamma(x - vt), \\quad t' = \\gamma\\left(t - \\frac{vx}{c^2}\\right), \\quad \\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}",
                "symbols": {"\\gamma": "Lorentz factor", "v": "Relative velocity (m/s)", "c": "Speed of light (m/s)", "x, t": "Laboratory coordinates", "x', t'": "Moving frame coordinates"}
            }]
        if any(k in t_low for k in ["dilation", "contraction", "mass-energy", "e = mc"]):
            return [{
                "name": "Relativistic Energy-Momentum Relation",
                "latex": "E = \\gamma m_0 c^2, \\quad E^2 = p^2 c^2 + m_0^2 c^4",
                "symbols": {"E": "Total relativistic energy (J)", "m_0": "Rest mass (kg)", "p": "Relativistic momentum (kg·m/s)", "c": "Speed of light (m/s)"}
            }]
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
        t_low = topic.lower()
        if any(k in t_low for k in ["interference", "young", "fringe", "newton"]):
            return [{
                "name": "Newton's Rings Fringe Interferometry (Newton, 1704)",
                "setup": "Plano-convex lens of radius R placed on optical flat plate illuminated by monochromatic sodium light.",
                "observation": "Concentric alternating circular dark and bright fringes with dark central contact spot.",
                "conclusion": "Accurately measures optical wavelength from diameter squared difference (D_{n+p}^2 - D_n^2 = 4p lambda R)."
            }]
        if any(k in t_low for k in ["diffraction", "grating", "resolving"]):
            return [{
                "name": "Diffraction Grating Spectrometry",
                "setup": "Collimated spectrometer directed at transmission diffraction grating with 15,000 lines/inch.",
                "observation": "Discrete sharp spectral orders diffracted according to (a+b)sin theta = n lambda.",
                "conclusion": "Resolves close sodium D-line doublet (589.0 nm and 589.6 nm) with high chromatic resolving power."
            }]
        if any(k in t_low for k in ["laser", "ruby", "he-ne"]):
            return [{
                "name": "Maiman Synthetic Ruby Laser Oscillation (1960)",
                "setup": "Synthetic Al2O3:Cr3+ cylindrical rod pumped by helical xenon flashtube inside Fabry-Perot cavity.",
                "observation": "Intense coherent deep-crimson pulse emitted at 694.3 nm with milliradian divergence.",
                "conclusion": "First empirical demonstration of optical amplification by stimulated emission of radiation."
            }]
        if any(k in t_low for k in ["fiber", "attenuation", "numerical aperture"]):
            return [{
                "name": "Fiber Optic Numerical Aperture Profile Measurement",
                "setup": "He-Ne laser launched into optical fiber end-face with far-field angular scanning detector.",
                "observation": "Output cone divergence angle measured in far-field matching NA = sin(theta_a) = sqrt(n1^2 - n2^2).",
                "conclusion": "Confirms light guidance boundary governed by critical total internal reflection."
            }]
        if any(k in t_low for k in ["michelson", "relativity", "ether", "lorentz"]):
            return [{
                "name": "Michelson-Morley Ether Drift Interferometry (1887)",
                "setup": "Orthogonal equal-arm optical interferometer floating on mercury pool rotating through 360 degrees.",
                "observation": "Zero fringe shift observed (fringe shift < 0.005 fringes against 0.4 theoretical prediction).",
                "conclusion": "Disproved luminiferous ether hypothesis and established universal constancy of speed of light."
            }]
        return [{
            "name": "Davisson-Germer Electron Diffraction (1927)",
            "setup": "Collimated low-energy electron beam impinging on nickel target single crystal.",
            "observation": "Constructive interference peak observed at 54 V accelerating potential and 50 degree scattering angle.",
            "conclusion": "Deduced electron wavelength of 0.165 nm matching de Broglie theoretical prediction within 1%."
        }]

    def application_patterns(self, topic: str) -> List[Dict[str, Any]]:
        t_low = topic.lower()
        if any(k in t_low for k in ["interference", "thin film", "optics"]):
            return [{
                "device": "Anti-Reflective Optical Dielectric Coating",
                "mechanism": "Quarter-wave MgF2 thin film destructive interference suppresses surface reflection below 0.1%.",
                "impact": "Crucial for high-efficiency camera optics, solar photovoltaic cells, and laser optics."
            }]
        if any(k in t_low for k in ["laser", "he-ne", "ruby", "semiconductor"]):
            return [{
                "device": "Semiconductor Distributed Feedback (DFB) Telecom Laser",
                "mechanism": "Stimulated electron-hole recombination in InGaAsP quantum wells with Bragg grating cavity feedback.",
                "impact": "Powers high-speed transoceanic optical telecommunication networks operating at 1550 nm."
            }]
        if any(k in t_low for k in ["fiber", "optical fiber", "sensor"]):
            return [{
                "device": "Fiber Bragg Grating (FBG) Structural Sensor",
                "mechanism": "Periodic core index modulation reflects narrow Bragg wavelength shifting with strain and temperature.",
                "impact": "Enables distributed real-time structural health monitoring in bridges, aircraft, and oil pipelines."
            }]
        if any(k in t_low for k in ["relativity", "lorentz", "dilation"]):
            return [{
                "device": "Global Positioning System (GPS) Satellite Constellation",
                "mechanism": "Atomic clocks account for relativistic time dilation (-7 us/day) and gravitational blueshift (+45 us/day).",
                "impact": "Enables worldwide sub-meter precision geospatial navigation."
            }]
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
            "k_B": "Boltzmann constant (1.381 x 10^-23 J/K)",
            "c": "Speed of light in vacuum (2.998 x 10^8 m/s)",
            "\\epsilon_0": "Permittivity of free space (8.854 x 10^-12 F/m)",
            "\\mu_0": "Permeability of free space (4pi x 10^-7 H/m)"
        }

    def generate_section_prose(
        self,
        topic: str,
        subtopic: str,
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = False
    ) -> str:
        from backend.app.agents.physics_knowledge_prose import (
            generate_quantum_prose,
            generate_wave_optics_prose,
            generate_laser_prose,
            generate_fiber_optics_prose,
            generate_em_relativity_prose,
            generate_physics_numerical,
            generate_physics_questions
        )

        t_low = topic.lower()

        if any(k in t_low for k in ["interference", "diffraction", "polarization", "optic", "fringe", "newton", "young", "coherent", "thin film", "grating", "resolving", "brewster"]):
            paragraphs = generate_wave_optics_prose(topic, subtopic, requires_derivation)
        elif any(k in t_low for k in ["laser", "emission", "absorption", "population inversion", "metastable", "einstein coefficient", "ruby", "he-ne"]):
            paragraphs = generate_laser_prose(topic, subtopic, requires_derivation)
        elif any(k in t_low for k in ["fiber", "optical fiber", "numerical aperture", "acceptance", "step-index", "graded-index", "v-number", "attenuation", "dispersion", "splicing", "photonic crystal"]):
            paragraphs = generate_fiber_optics_prose(topic, subtopic, requires_derivation)
        elif any(k in t_low for k in ["maxwell", "gauss", "faraday", "ampere", "displacement current", "poynting", "relativity", "galilean", "lorentz", "dilation", "contraction", "electromagnetism"]):
            paragraphs = generate_em_relativity_prose(topic, subtopic, requires_derivation)
        else:
            paragraphs = generate_quantum_prose(topic, subtopic, requires_derivation)

        if include_numericals:
            paragraphs.append(generate_physics_numerical(topic, subtopic))
        if include_questions:
            paragraphs.append(generate_physics_questions(topic, subtopic))

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
