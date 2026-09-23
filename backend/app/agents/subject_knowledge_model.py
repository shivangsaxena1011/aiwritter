"""
SubjectKnowledgeModel — Domain Knowledge & Pedagogical Progression Engine.
Provides domain-specific concepts, governing equations, historical context,
experimental foundations, and realistic applications across scientific disciplines.
Replaces generic content templates with genuine academic knowledge structures.
"""

from typing import Dict, Any, List, Optional
import re

class SubjectKnowledgeModel:
    """
    Understands the pedagogical and mathematical structure of university subjects.
    Maps syllabus topics to authentic theoretical principles, standard derivations,
    real experimental verifications, and legitimate engineering applications.
    """

    # Domain Knowledge Repository for Engineering Physics & Related Fields
    KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
        "quantum mechanics": {
            "canonical_principles": [
                "Wave-particle duality of matter and radiation",
                "Max Born probability interpretation of the wave function",
                "Heisenberg uncertainty principle as a fundamental quantum limit",
                "Linear superposition of quantum state vectors in Hilbert space",
                "Operator formalism and eigenvalue equations for physical observables",
                "Spatial confinement inducing discrete energy quantization"
            ],
            "canonical_equations": [
                {
                    "name": "de Broglie Wavelength",
                    "latex": "\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2mE_k}}",
                    "symbols": {"\\lambda": "de Broglie wavelength (m)", "h": "Planck constant (6.626e-34 J·s)", "p": "particle momentum (kg·m/s)", "m": "particle rest mass (kg)", "v": "velocity (m/s)", "E_k": "kinetic energy (J)"},
                    "derivation_steps": [
                        "Start from Planck-Einstein relation for photon energy: $E = h\\nu = \\frac{hc}{\\lambda}$",
                        "Recall relativistic energy-momentum relationship for a photon with zero rest mass: $E = pc$",
                        "Equate the two expressions for energy: $pc = \\frac{hc}{\\lambda} \\implies p = \\frac{h}{\\lambda}$",
                        "Invert to obtain de Broglie's wavelength postulate for radiation: $\\lambda = \\frac{h}{p}$",
                        "Hypothesize that this relationship applies universally to all material particles possessing momentum $p = mv$",
                        "Express in terms of non-relativistic kinetic energy $E_k = \\frac{p^2}{2m} \\implies p = \\sqrt{2mE_k}$, yielding $\\lambda = \\frac{h}{\\sqrt{2mE_k}}$"
                    ]
                },
                {
                    "name": "Heisenberg Uncertainty Principle",
                    "latex": "\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}",
                    "symbols": {"\\Delta x": "standard deviation / uncertainty in position (m)", "\\Delta p_x": "uncertainty in momentum along x (kg·m/s)", "\\hbar": "reduced Planck constant, h / 2pi (1.055e-34 J·s)"},
                    "derivation_steps": [
                        "Consider a localized particle described by a wavepacket composed of a Fourier spectrum of plane waves $\\psi(x) = \\int A(k)e^{ikx}dk$",
                        "Recall the fundamental wave property of Fourier transform pairs relating spatial spread $\\Delta x$ and wavenumber spread $\\Delta k$: $\\Delta x \\cdot \\Delta k \\ge \\frac{1}{2}$",
                        "Substitute de Broglie's relation relating wavenumber to momentum: $p_x = \\hbar k \\implies \\Delta p_x = \\hbar \\Delta k$",
                        "Multiply the wave inequality by $\\hbar$: $\\Delta x (\\hbar \\Delta k) \\ge \\frac{\\hbar}{2} \\implies \\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}$",
                        "Observe that this inequality represents an intrinsic property of wave mechanics rather than an experimental measurement limitation"
                    ]
                },
                {
                    "name": "Time-Dependent Schrödinger Equation",
                    "latex": "i\\hbar \\frac{\\partial \\Psi(x, t)}{\\partial t} = -\\frac{\\hbar^2}{2m} \\frac{\\partial^2 \\Psi(x, t)}{\\partial x^2} + V(x, t)\\Psi(x, t)",
                    "symbols": {"\\Psi(x, t)": "complex space-time wave function", "i": "imaginary unit (sqrt(-1))", "\\hbar": "reduced Planck constant", "m": "particle mass", "V(x, t)": "potential energy field"},
                    "derivation_steps": [
                        "Begin with the classical non-relativistic total energy expression: $E = \\frac{p^2}{2m} + V(x)$",
                        "Associate physical observables with differential quantum operators acting on state function $\\Psi$:",
                        "Energy operator: $\\hat{E} = i\\hbar \\frac{\\partial}{\\partial t}$",
                        "Momentum operator: $\\hat{p} = -i\\hbar \\frac{\\partial}{\\partial x} \\implies \\hat{p}^2 = -\\hbar^2 \\frac{\\partial^2}{\\partial x^2}$",
                        "Hamiltonian operator: $\\hat{H} = \\frac{\\hat{p}^2}{2m} + V(x) = -\\frac{\\hbar^2}{2m}\\frac{\\partial^2}{\\partial x^2} + V(x)$",
                        "Construct the operator wave equation $\\hat{E}\\Psi = \\hat{H}\\Psi$, yielding the fundamental time-dependent equation"
                    ]
                },
                {
                    "name": "Time-Independent Schrödinger Equation",
                    "latex": "-\\frac{\\hbar^2}{2m} \\frac{d^2 \\psi(x)}{dx^2} + V(x)\\psi(x) = E\\psi(x)",
                    "symbols": {"\\psi(x)": "spatial stationary state wave function", "E": "energy eigenvalue (J)", "V(x)": "time-independent potential energy"},
                    "derivation_steps": [
                        "Assume a stationary state solution using separation of variables: $\\Psi(x, t) = \\psi(x)\\phi(t)$",
                        "Substitute into time-dependent equation: $i\\hbar \\psi(x) \\frac{d\\phi(t)}{dt} = \\phi(t) \\left[ -\\frac{\\hbar^2}{2m} \\frac{d^2\\psi(x)}{dx^2} + V(x)\\psi(x) \\right]$",
                        "Divide both sides by $\\Psi(x, t) = \\psi(x)\\phi(t)$ to isolate spatial and temporal terms:",
                        "$\\frac{i\\hbar}{\\phi(t)} \\frac{d\\phi(t)}{dt} = \\frac{1}{\\psi(x)} \\left[ -\\frac{\\hbar^2}{2m}\\frac{d^2\\psi(x)}{dx^2} + V(x)\\psi(x) \\right] = E$",
                        "The separation constant $E$ represents the total energy eigenvalue of the stationary quantum state",
                        "Temporal equation integrates to $\\phi(t) = e^{-iEt/\\hbar}$, while the spatial equation yields the time-independent equation $\\hat{H}\\psi = E\\psi$"
                    ]
                },
                {
                    "name": "Particle in a 1D Infinite Potential Well (Particle in a Box)",
                    "latex": "E_n = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2} = \\frac{n^2 h^2}{8mL^2}, \\quad \\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right)",
                    "symbols": {"E_n": "quantized energy eigenvalue of n-th state", "n": "quantum number (1, 2, 3, ...)", "L": "width of the potential well (m)", "m": "particle mass (kg)", "\\psi_n(x)": "normalized spatial wave function"},
                    "derivation_steps": [
                        "Define the potential: $V(x) = 0$ for $0 < x < L$, and $V(x) = \\infty$ elsewhere. Confinement requires $\\psi(x) = 0$ for $x \\le 0$ and $x \\ge L$.",
                        "Inside the well ($V = 0$), the time-independent Schrödinger equation is: $\\frac{d^2\\psi}{dx^2} + k^2\\psi = 0$, where $k = \\frac{\\sqrt{2mE}}{\\hbar}$",
                        "Write general solution: $\\psi(x) = A\\sin(kx) + B\\cos(kx)$",
                        "Apply boundary condition at $x = 0$: $\\psi(0) = B = 0$, so $\\psi(x) = A\\sin(kx)$",
                        "Apply boundary condition at $x = L$: $\\psi(L) = A\\sin(kL) = 0$. Since $A \\ne 0$ for non-trivial states, $\\sin(kL) = 0 \\implies kL = n\\pi$ for $n = 1, 2, 3, \\dots$",
                        "Quantized wavenumbers: $k_n = \\frac{n\\pi}{L}$. Equate to energy definition: $k_n^2 = \\frac{2mE_n}{\\hbar^2} \\implies E_n = \\frac{\\hbar^2 k_n^2}{2m} = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2} = \\frac{n^2 h^2}{8mL^2}$",
                        "Normalize wave function: $\\int_0^L |\\psi_n(x)|^2 dx = A^2 \\int_0^L \\sin^2\\left(\\frac{n\\pi x}{L}\\right) dx = A^2 \\frac{L}{2} = 1 \\implies A = \\sqrt{\\frac{2}{L}}$",
                        "Final normalized eigenstates: $\\psi_n(x) = \\sqrt{\\frac{2}{L}}\\sin\\left(\\frac{n\\pi x}{L}\\right)$ with non-zero zero-point energy $E_1 = \\frac{h^2}{8mL^2}$"
                    ]
                },
                {
                    "name": "Phase Velocity and Group Velocity",
                    "latex": "v_p = \\frac{\\omega}{k}, \\quad v_g = \\frac{d\\omega}{dk} = v_p + k \\frac{dv_p}{dk}",
                    "symbols": {"v_p": "phase velocity of individual wavefront (m/s)", "v_g": "group velocity of wavepacket envelope (m/s)", "\\omega": "angular frequency (rad/s)", "k": "wavenumber (rad/m)"},
                    "derivation_steps": [
                        "Consider superposition of two harmonic waves differing slightly in frequency and wavenumber: $y_1 = A\\cos(kx - \\omega t)$, $y_2 = A\\cos((k+dk)x - (\\omega+d\\omega)t)$",
                        "Use trigonometric sum formula: $y = y_1 + y_2 = 2A\\cos\\left(\\frac{dk}{2}x - \\frac{d\\omega}{2}t\\right) \\cos(kx - \\omega t)$",
                        "The high-frequency carrier wave propagates at phase velocity $v_p = \\frac{\\omega}{k}$",
                        "The low-frequency modulating envelope propagates at group velocity $v_g = \\frac{d\\omega}{dk}$",
                        "For a de Broglie matter wave, $E = \\hbar\\omega$ and $p = \\hbar k$, so $v_g = \\frac{dE}{dp} = \\frac{d(p^2/2m)}{dp} = \\frac{p}{m} = v_{particle}$",
                        "This proves that the group velocity of the matter wave packet is identically equal to the physical particle velocity"
                    ]
                },
                {
                    "name": "Physical Interpretation of Wave Function",
                    "latex": "P(x) dx = |\\Psi(x, t)|^2 dx, \\quad \\int_{-\\infty}^{\\infty} |\\Psi(x, t)|^2 dx = 1",
                    "symbols": {"P(x)dx": "probability of finding the particle in interval [x, x+dx]", "|\\Psi|^2": "probability density (m^-1)"},
                    "derivation_steps": [
                        "Max Born (1926) interpreted the complex wave function $\\Psi(x, t)$ as a probability amplitude",
                        "The absolute square $|\\Psi|^2 = \\Psi^* \\Psi$ represents the spatial probability density of locating the particle",
                        "Total probability across all space must be identically unity (normalization condition): $\\int_{-\\infty}^\\infty |\\Psi(x, t)|^2 dx = 1$",
                        "Physical admissibility requires $\\Psi$ to be single-valued, continuous, and have continuous first spatial derivatives"
                    ]
                }
            ],
            "experimental_milestones": [
                "Davisson-Germer Experiment (1927): Electron diffraction by nickel monocrystal lattice confirming de Broglie wavelength",
                "G. P. Thomson Experiment (1927): Electron diffraction through thin gold foil producing circular diffraction rings",
                "Compton Scattering (1923): Inelastic X-ray scattering confirming photon momentum $p = h/\\lambda$",
                "Franck-Hertz Experiment (1914): Inelastic electron collisions demonstrating discrete atomic energy levels",
                "Blackbody Radiation (Planck, 1900): Quantization of energy oscillators $E = nh\\nu$",
                "Photoelectric Effect (Einstein, 1905): Particle-like photon emission $E_k = h\\nu - \\Phi$"
            ],
            "engineering_applications": [
                "Transmission Electron Microscopy (TEM) and Scanning Electron Microscopy (SEM) utilizing sub-angstrom electron wavelengths",
                "Quantum Well Lasers and Heterostructure Transistors engineered by nanoscale potential wells",
                "Resonant Tunneling Diodes and Scanning Tunneling Microscopy (STM) based on quantum barrier penetration",
                "Semiconductor Quantum Dots and Nanocrystal Displays with size-tunable bandgap fluorescence",
                "Superconducting Quantum Interference Devices (SQUIDs) for ultra-sensitive magnetometry"
            ]
        },
        "wave optics": {
            "canonical_principles": [
                "Wave superposition and spatial-temporal coherence",
                "Division of wavefront vs division of amplitude",
                "Huygens-Fresnel wave propagation principle",
                "Constructive and destructive phase interference",
                "Fraunhofer (far-field) vs Fresnel (near-field) diffraction"
            ],
            "canonical_equations": [
                {
                    "name": "Young's Double Slit Fringe Width",
                    "latex": "\\beta = \\frac{\\lambda D}{d}, \\quad I(\\theta) = I_0 \\cos^2\\left(\\frac{\\pi d \\sin\\theta}{\\lambda}\\right)",
                    "symbols": {"\\beta": "fringe width (m)", "\\lambda": "wavelength (m)", "D": "slit-to-screen distance (m)", "d": "slit separation (m)"}
                },
                {
                    "name": "Diffraction Grating Equation",
                    "latex": "(a + b) \\sin\\theta = m\\lambda",
                    "symbols": {"(a+b)": "grating element (m)", "m": "spectral order (0, 1, 2, ...)", "\\theta": "diffraction angle (rad)"}
                },
                {
                    "name": "Newton's Rings Diameter",
                    "latex": "D_n^2 = 4n\\lambda R \\quad \\text{(dark rings in reflected light)}",
                    "symbols": {"D_n": "diameter of n-th dark ring", "R": "radius of curvature of plano-convex lens", "n": "ring index"}
                }
            ],
            "experimental_milestones": [
                "Young's Double-Slit Experiment (1801): Establishing wave nature of light",
                "Newton's Rings: Demonstration of thin-film interference fringes",
                "Fraunhofer Diffraction at Single Slit: Confirmation of wave bending around obstacles"
            ],
            "engineering_applications": [
                "Optical Spectroscopy and Monochromators using diffraction gratings",
                "Anti-reflective coatings on optical lenses via thin-film destructive interference",
                "Interferometric surface roughness measurement and laser metrology",
                "Optical fiber communications wavelength division multiplexing (WDM)"
            ]
        },
        "fiber optics": {
            "canonical_principles": [
                "Total internal reflection at core-cladding dielectric interface",
                "Numerical aperture and light-gathering acceptance angle",
                "Normalized frequency (V-number) governing modal propagation",
                "Material, waveguide, and chromatic dispersion mechanisms",
                "Rayleigh scattering and attenuation mechanisms in silica fibers"
            ],
            "canonical_equations": [
                {
                    "name": "Numerical Aperture and Acceptance Angle",
                    "latex": "NA = \\sqrt{n_1^2 - n_2^2} = n_1 \\sqrt{2\\Delta}, \\quad \\theta_a = \\arcsin(NA)",
                    "symbols": {"NA": "numerical aperture", "n_1": "core refractive index", "n_2": "cladding refractive index", "\\Delta": "fractional refractive index difference", "\\theta_a": "acceptance angle"}
                },
                {
                    "name": "V-Number (Normalized Frequency)",
                    "latex": "V = \\frac{2\\pi a}{\\lambda}\\sqrt{n_1^2 - n_2^2} = \\frac{2\\pi a}{\\lambda} NA",
                    "symbols": {"V": "normalized frequency", "a": "core radius (m)", "\\lambda": "operating wavelength (m)"}
                }
            ],
            "experimental_milestones": [
                "Kao and Hockham (1966): Discovery of silica fiber loss reduction below 20 dB/km",
                "Corning Glass Works (1970): First low-loss optical fiber manufactured"
            ],
            "engineering_applications": [
                "Long-haul transoceanic optical telecommunication systems",
                "Endoscopic medical diagnostic imaging devices",
                "Fiber optic gyroscopes for inertial navigation systems",
                "Distributed temperature and acoustic fiber sensors in structural monitoring"
            ]
        },
        "lasers": {
            "canonical_principles": [
                "Stimulated absorption, spontaneous emission, and stimulated emission",
                "Einstein A and B coefficients and thermodynamic equilibrium relations",
                "Population inversion and meta-stable energy level lifetimes",
                "Three-level vs four-level laser pumping schemes",
                "Optical resonant cavity feedback and longitudinal mode selection"
            ],
            "canonical_equations": [
                {
                    "name": "Einstein Coefficients Ratio",
                    "latex": "\\frac{A_{21}}{B_{21}} = \\frac{8\\pi h \\nu^3}{c^3}, \\quad B_{12} = \\frac{g_2}{g_1} B_{21}",
                    "symbols": {"A_{21}": "Einstein coefficient for spontaneous emission", "B_{21}": "Einstein coefficient for stimulated emission", "h": "Planck constant", "\\nu": "transition frequency"}
                }
            ],
            "experimental_milestones": [
                "Maiman (1960): First operational laser utilizing synthetic ruby crystal",
                "Javan et al. (1960): Helium-Neon continuous wave gas laser"
            ],
            "engineering_applications": [
                "Precision laser cutting, welding, and additive manufacturing",
                "Fiber-optic optical transmitters in telecommunications",
                "Laser eye surgery (LASIK) and precision dermatological medicine",
                "Barcode scanners and LiDAR remote sensing systems"
            ]
        },
        "semiconductor physics": {
            "canonical_principles": [
                "Energy band formation: valence band, conduction band, and bandgap",
                "Direct vs indirect bandgap semiconductors",
                "Intrinsic vs extrinsic semiconductors: donor and acceptor doping",
                "Fermi-Dirac distribution and temperature dependence of Fermi level",
                "p-n junction depletion region, built-in potential, and forward/reverse bias"
            ],
            "canonical_equations": [
                {
                    "name": "Intrinsic Carrier Concentration",
                    "latex": "n_i = \\sqrt{N_c N_v} \\exp\\left(-\\frac{E_g}{2k_B T}\\right)",
                    "symbols": {"n_i": "intrinsic carrier concentration", "N_c, N_v": "effective density of states", "E_g": "bandgap energy", "k_B": "Boltzmann constant", "T": "temperature in Kelvin"}
                },
                {
                    "name": "Built-in Potential of p-n Junction",
                    "latex": "V_{bi} = \\frac{k_B T}{q} \\ln\\left(\\frac{N_A N_D}{n_i^2}\\right)",
                    "symbols": {"V_{bi}": "built-in potential", "N_A": "acceptor dopant density", "N_D": "donor dopant density", "q": "electron charge"}
                }
            ],
            "experimental_milestones": [
                "Bardeen, Brattain, and Shockley (1947): Invention of the point-contact bipolar transistor",
                "Esaki (1957): Discovery of electron tunneling in heavily doped p-n junctions"
            ],
            "engineering_applications": [
                "Complementary Metal-Oxide-Semiconductor (CMOS) microprocessors",
                "Photovoltaic solar cells for renewable electricity generation",
                "Light Emitting Diodes (LEDs) for energy-efficient illumination",
                "Power electronic MOSFETs and IGBTs for electric vehicles"
            ]
        }
    }

    @classmethod
    def get_subject_domain(cls, subject: str, topic: str = "") -> str:
        """Identifies the subject domain from text."""
        combined = f"{subject} {topic}".lower()
        if any(k in combined for k in ["fiber", "numerical aperture", "acceptance angle", "acceptance cone", "v-number", "step-index", "graded-index"]):
            return "fiber optics"
        if any(k in combined for k in ["laser", "population inversion", "stimulated emission", "ruby", "he-ne", "einstein coefficient"]):
            return "lasers"
        if any(k in combined for k in ["semiconductor", "fermi", "p-n junction", "bandgap", "carrier concentration", "doping", "transistor", "hall effect"]):
            return "semiconductor physics"
        if any(k in combined for k in ["quantum", "schrodinger", "de broglie", "heisenberg", "wave function", "potential well", "photoelectric"]):
            return "quantum mechanics"
        if any(k in combined for k in ["optic", "interference", "diffraction", "polarization", "fringe", "newton"]):
            return "wave optics"
        return "quantum mechanics"

    @classmethod
    def get_knowledge_for_topic(cls, topic: str, subject: str = "Engineering Physics") -> Dict[str, Any]:
        """Retrieves domain-specific knowledge records relevant to a topic."""
        domain = cls.get_subject_domain(subject, topic)
        domain_data = cls.KNOWLEDGE_BASE.get(domain, cls.KNOWLEDGE_BASE["quantum mechanics"])
        topic_lower = topic.lower()

        # Find best matching canonical equation
        matched_eqs = []
        for eq in domain_data.get("canonical_equations", []):
            eq_name = eq["name"].lower()
            if any(w in topic_lower for w in eq_name.split() if len(w) > 3) or any(w in eq_name for w in topic_lower.split() if len(w) > 3):
                matched_eqs.append(eq)

        if not matched_eqs and domain_data.get("canonical_equations"):
            matched_eqs.append(domain_data["canonical_equations"][0])

        # Filter relevant milestones
        relevant_milestones = [
            m for m in domain_data.get("experimental_milestones", [])
            if any(w in m.lower() for w in topic_lower.split() if len(w) > 4)
        ]
        if not relevant_milestones:
            relevant_milestones = domain_data.get("experimental_milestones", [])[:2]

        # Filter relevant applications
        relevant_apps = [
            a for a in domain_data.get("engineering_applications", [])
            if any(w in a.lower() for w in topic_lower.split() if len(w) > 4)
        ]
        if not relevant_apps:
            relevant_apps = domain_data.get("engineering_applications", [])[:2]

        return {
            "domain": domain,
            "principles": domain_data.get("canonical_principles", [])[:3],
            "equations": matched_eqs,
            "milestones": relevant_milestones,
            "applications": relevant_apps
        }

    @classmethod
    def generate_academic_section(
        cls,
        topic: str,
        subtopic: str,
        subject: str = "Engineering Physics",
        include_numericals: bool = False,
        include_questions: bool = False,
        requires_derivation: bool = True
    ) -> str:
        """
        Generates authentic, domain-grounded university textbook prose.
        Eliminates all generic templates, fake configurations, and unrelated diffusion equations.
        Produces rigorous, subject-specific mathematical derivations and physical insights.
        """
        combined = f"{subtopic} {topic} {subject}".lower()

        # 1. de Broglie Hypothesis / Matter Waves / Dual Nature
        if any(k in combined for k in ["de broglie", "matter wave", "wave nature of particle", "wavelength"]):
            return cls._generate_de_broglie_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 2. Particle in a 1D Box / Infinite Potential Well
        if any(k in combined for k in ["box", "well", "infinite potential", "potential well", "quantum well"]):
            return cls._generate_particle_in_box_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 3. Heisenberg Uncertainty Principle
        if any(k in combined for k in ["heisenberg", "uncertainty"]):
            return cls._generate_heisenberg_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 4. Phase Velocity and Group Velocity
        if any(k in combined for k in ["phase velocity", "group velocity", "dispersion"]):
            return cls._generate_velocity_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 5. Operators, Commutators, Eigenvalues, and Eigenfunctions
        if any(k in combined for k in ["operator", "eigenvalue", "eigenfunction", "eigenstate", "hamiltonian", "commutat"]):
            return cls._generate_operators_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 6. Schrödinger Wave Equations (Time-Dependent and Time-Independent)
        if any(k in combined for k in ["schrodinger", "time-dependent", "time-independent", "wave equation"]):
            return cls._generate_schrodinger_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 7. Physical Interpretation of Wave Function / Born Postulate
        if any(k in combined for k in ["born", "interpretation", "probability density", "normalization", "wave function"]):
            return cls._generate_wave_function_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 8. Quantum Applications / Nanotechnology
        if any(k in combined for k in ["application", "tem", "sem", "stm", "tunneling", "quantum dot", "nanotechnology"]):
            return cls._generate_quantum_apps_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 9. Optical Fibers
        if any(k in combined for k in ["fiber", "numerical aperture", "acceptance angle", "attenuation", "modal"]):
            return cls._generate_fiber_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 10. Lasers and Stimulated Emission
        if any(k in combined for k in ["laser", "einstein", "stimulated emission", "population inversion", "ruby", "he-ne"]):
            return cls._generate_laser_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 11. Wave Optics (Interference, Diffraction, Newton's Rings)
        if any(k in combined for k in ["interference", "diffraction", "newton", "slit", "grating", "polarization", "fringe"]):
            return cls._generate_wave_optics_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # 12. Semiconductor Physics
        if any(k in combined for k in ["semiconductor", "hall effect", "bandgap", "fermi", "carrier", "junction"]):
            return cls._generate_semiconductor_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

        # Default fallback: General Introduction to Quantum Mechanics
        return cls._generate_quantum_intro_section(topic, subtopic, subject, include_numericals, include_questions, requires_derivation)

    @classmethod
    def _generate_de_broglie_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "The formulation of the de Broglie hypothesis in 1924 marked one of the most profound conceptual revolutions in modern physical science. "
            "Throughout the nineteenth century, physics rested comfortably upon a strict dichotomy between localized particles governed by Newtonian mechanics and continuous electromagnetic fields described by Maxwell's electrodynamics. "
            "However, this classical paradigm proved fundamentally incapable of explaining blackbody radiation, the photoelectric effect, and the stability of atomic orbits. "
            "Recognizing that electromagnetic radiation—classically treated as continuous waves—manifests discrete particle-like packet characteristics (photons) with energy $E = h\\nu$ and momentum $p = h/\\lambda$, the French physicist Louis de Broglie postulated that nature possesses an intrinsic symmetry. "
            "He asserted that material entities such as electrons, protons, and neutrons, which had universally been categorized as discrete classical particles, must simultaneously exhibit an underlying wave character in their dynamical propagation.\n",
            "### 1. Theoretical Framework and Physical Mechanisms\n",
            "The physical essence of de Broglie's thesis lies in associating every material particle possessing mechanical momentum $p$ with a characteristic pilot wave or matter wave. "
            "Unlike classical mechanical waves (such as acoustic oscillations in fluid media) or classical electromagnetic radiation (transverse oscillations of electric and magnetic fields in free space), matter waves represent quantum probability amplitudes that dictate the spatial and temporal likelihood of locating a particle upon measurement. "
            "The fundamental connection between the corpuscular attributes of the particle (mass $m$ and velocity $v$) and the wave attributes of the pilot oscillation (frequency $\\nu$ and wavelength $\\lambda$) is bridged exclusively by Planck's constant $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$.\n",
            "The definitive experimental verification of matter waves was achieved independently in 1927 by Clinton Davisson and Lester Germer at Bell Telephone Laboratories, and by George Paget Thomson at the University of Aberdeen. "
            "Davisson and Germer directed a collimated beam of low-energy electrons toward the surface of a target nickel single crystal. "
            "By measuring the angular distribution of the scattered electrons, they detected intense peak reflections at an accelerating potential of $54\\text{ V}$ and a scattering angle of $\\theta = 50^\\circ$. "
            "Applying Bragg's diffraction law $2d\\sin\\theta = n\\lambda$ to the nickel crystal lattice spacing ($d = 0.091\\text{ nm}$), they deduced an electron wavelength of $0.165\\text{ nm}$, in extraordinary agreement with de Broglie's theoretical prediction. "
            "Simultaneously, G. P. Thomson demonstrated that passing high-energy cathode rays through ultra-thin gold foils produced concentric circular diffraction rings identical to X-ray powder diffraction patterns, conclusively establishing the wave nature of electrons.\n",
            "### 2. Analytical Formulation and Governing Equations\n",
            "The quantitative relationship establishing the de Broglie wavelength for a non-relativistic particle of mass $m$ moving with velocity $v$ is formulated as:\n",
            "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv} = \\frac{h}{\\sqrt{2m E_k}}$$\n",
            "In this foundational expression, $\\lambda$ denotes the de Broglie wavelength in meters (m), $h$ represents Planck's constant ($6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$), $p$ is the relativistic or non-relativistic momentum (kg·m/s), and $E_k$ represents the kinetic energy of the moving particle in Joules (J).\n",
            "When a particle possessing elementary electrical charge $q$ is accelerated from rest through an electrostatic potential difference $V$ (Volts), the kinetic energy acquired equals $E_k = qV$. Substituting this electrodynamic relationship into the momentum formulation yields:\n",
            "$$\\lambda = \\frac{h}{\\sqrt{2m q V}}$$\n",
            "For an electron possessing rest mass $m_e = 9.109 \\times 10^{-31}\\text{ kg}$ and elementary charge $e = 1.602 \\times 10^{-19}\\text{ C}$, substituting these fundamental physical constants gives the practical working formula:\n",
            "$$\\lambda_e = \\sqrt{\\frac{150}{V}}\\text{ \\AA} = \\frac{1.227}{\\sqrt{V}}\\text{ nm}$$\n"
        ]

        if derivation:
            parts.extend([
                "### 3. Step-by-Step Mathematical Derivation\n",
                "The mathematical derivation of the de Broglie relationship proceeds systematically from Planck's radiation law and Einstein's special theory of relativity:\n",
                "**Step 1: Energy of a Photon.** According to the Planck-Einstein quantum hypothesis, the total energy of a photon of frequency $\\nu$ and wavelength $\\lambda$ propagating at the speed of light $c$ is:\n",
                "$$E = h\\nu = \\frac{hc}{\\lambda}$$\n",
                "**Step 2: Relativistic Momentum of a Photon.** In special relativity, the energy-momentum relationship for a massless particle ($m_0 = 0$) simplifies to $E = pc$. Equating the two independent expressions for photon energy:\n",
                "$$pc = \\frac{hc}{\\lambda} \\implies p = \\frac{h}{\\lambda}$$\n",
                "**Step 3: Inversion for de Broglie Postulate.** Solving for the wavelength associated with the momentum $p$ yields:\n",
                "$$\\lambda = \\frac{h}{p}$$\n",
                "**Step 4: Extension to Massive Material Particles.** De Broglie hypothesized that this mathematical link applies not only to electromagnetic quanta but universally to all material entities possessing mechanical momentum $p = mv$:\n",
                "$$\\lambda = \\frac{h}{mv}$$\n",
                "**Step 5: Relation to Accelerating Potential.** Expressing the non-relativistic momentum in terms of kinetic energy $E_k = \\frac{p^2}{2m}$, we have $p = \\sqrt{2mE_k}$. For a particle of charge $q$ accelerated through potential $V$, $E_k = qV$, arriving at the final closed-form relation:\n",
                "$$\\lambda = \\frac{h}{\\sqrt{2mqV}}$$\n"
            ])

        parts.extend([
            "### 4. Comparison of De Broglie Wavelengths across Physical Domains\n",
            "The table below contrasts de Broglie wavelengths across macroscopic systems and microscopic subatomic entities to illustrate why wave characteristics are observable exclusively in quantum regimes:\n",
            "| Entity / Particle | Rest Mass $m$ (kg) | Typical Velocity $v$ (m/s) | Momentum $p$ (kg·m/s) | De Broglie Wavelength $\\lambda$ | Observable Wave Effects |\n",
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n",
            "| Cricket Ball | $0.15\\text{ kg}$ | $30\\text{ m/s}$ | $4.5\\text{ kg}\\cdot\\text{m/s}$ | $1.47 \\times 10^{-34}\\text{ m}$ | Completely undetectable (unphysical) |\n",
            "| Smoke Particle | $1.0 \\times 10^{-15}\\text{ kg}$ | $0.01\\text{ m/s}$ | $1.0 \\times 10^{-17}\\text{ kg}\\cdot\\text{m/s}$ | $6.63 \\times 10^{-17}\\text{ m}$ | Far smaller than atomic dimensions |\n",
            "| Thermal Neutron | $1.675 \\times 10^{-27}\\text{ kg}$ | $2.20 \\times 10^3\\text{ m/s}$ | $3.68 \\times 10^{-24}\\text{ kg}\\cdot\\text{m/s}$ | $1.80 \\times 10^{-10}\\text{ m}$ ($1.80\\text{ \\AA}$) | Readily diffracted by crystal lattices |\n",
            "| Electron ($100\\text{ V}$) | $9.109 \\times 10^{-31}\\text{ kg}$ | $5.93 \\times 10^6\\text{ m/s}$ | $5.40 \\times 10^{-24}\\text{ kg}\\cdot\\text{m/s}$ | $1.23 \\times 10^{-10}\\text{ m}$ ($1.23\\text{ \\AA}$) | Primary basis of electron microscopy |\n",
            "\n### 5. Key Physical Characteristics and Constraints\n",
            "To correctly apply the de Broglie relationship in engineering and physical analysis, the following core physical properties must be observed:\n",
            "- **Inversely Proportional to Mass and Velocity:** The wavelength scales as $\\lambda \\propto 1/m$. As mass increases into the macroscopic domain, the wavelength shrinks below the Planck length scale, rendering quantum interference undetectable.\n",
            "- **Non-Electromagnetic Character:** Matter waves are not electromagnetic oscillations; neutral particles such as neutrons and buckyballs ($C_{60}$) exhibit identical matter wave diffraction according to their momentum.\n",
            "- **Relativistic Corrections:** When particle velocity approaches the speed of light ($v > 0.1c$), the relativistic momentum $p = \\gamma m_0 v = \\frac{m_0 v}{\\sqrt{1 - v^2/c^2}}$ must be employed.\n",
            "\n### 6. Contemporary Engineering and Scientific Applications\n",
            "The physical reality of de Broglie waves underpins essential modern technological instruments:\n",
            "1. **Transmission Electron Microscopy (TEM):** Because accelerating electrons through $100\\text{ kV}$ to $300\\text{ kV}$ yields de Broglie wavelengths on the order of picometers ($0.0037\\text{ nm}$ at $100\\text{ kV}$), TEM achieves sub-angstrom spatial resolution, allowing direct imaging of atomic columns and crystal defects.\n",
            "2. **Electron Beam Lithography (EBL):** Semiconductor foundries employ focused electron beams to fabricate sub-10 nanometer gate profiles for advanced microprocessors, completely overcoming optical diffraction limits.\n",
            "3. **Thermal Neutron Scattering:** Nuclear research reactors utilize thermal neutron diffraction to determine atomic and magnetic structures in high-temperature superconductors and biological macromolecules.\n"
        ])

        if include_num:
            parts.extend([
                "### 7. Worked Solved Numerical Problem\n",
                "**Problem Statement:** An electron is accelerated from rest through a potential difference of $150\\text{ V}$. Calculate: (a) its kinetic energy in Joules and electron-volts, (b) its de Broglie wavelength in angstroms and nanometers, and (c) the de Broglie wavelength of a $100\\text{ g}$ golf ball traveling at $20\\text{ m/s}$. Compare the two wavelengths.\n",
                "**Given Data:**\n",
                "- Accelerating potential $V = 150\\text{ V}$\n",
                "- Electron rest mass $m_e = 9.109 \\times 10^{-31}\\text{ kg}$\n",
                "- Elementary charge $e = 1.602 \\times 10^{-19}\\text{ C}$\n",
                "- Planck constant $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$\n",
                "**Governing Formula:**\n",
                "$$E_k = eV, \\quad \\lambda_e = \\frac{h}{\\sqrt{2m_e E_k}} = \\frac{1.227}{\\sqrt{V}}\\text{ nm}, \\quad \\lambda_{ball} = \\frac{h}{M V_{ball}}$$\n",
                "**Substitution:**\n",
                "$$\\lambda_e = \\frac{1.227}{\\sqrt{150}}\\text{ nm}, \\quad \\lambda_{ball} = \\frac{6.626 \\times 10^{-34}}{0.10 \\times 20}\\text{ m}$$\n",
                "**Calculation Steps:**\n",
                "1. Electron kinetic energy: $E_k = (1.602 \\times 10^{-19}\\text{ C}) \\times 150\\text{ V} = 2.403 \\times 10^{-17}\\text{ J} = 150\\text{ eV}$.\n",
                "2. Electron de Broglie wavelength:\n",
                "$$\\lambda_e = \\frac{1.227}{\\sqrt{150}} = \\frac{1.227}{12.247} = 0.1002\\text{ nm} = 1.002\\text{ \\AA}$$\n",
                "3. Golf ball de Broglie wavelength:\n",
                "$$\\lambda_{ball} = \\frac{6.626 \\times 10^{-34}}{0.10 \\times 20} = \\frac{6.626 \\times 10^{-34}}{2.0} = 3.313 \\times 10^{-34}\\text{ m}$$\n",
                "**Final Answer:**\n",
                "$$\\mathbf{\\lambda_e = 0.1002\\text{ nm} \\quad (1.002\\text{ \\AA}), \\quad \\lambda_{ball} = 3.313 \\times 10^{-34}\\text{ m}}$$\n",
                "The electron wavelength is comparable to interatomic lattice spacings in solids (~$1\\text{ \\AA}$), enabling diffraction, whereas the golf ball wavelength is $10^{-24}$ times smaller than an atomic nucleus, exhibiting zero observable wave effects.\n"
            ])

        if include_qa:
            parts.extend([
                "### 8. Review Questions and Academic Exercises\n",
                "1. *Analytical*: Derive the expression for the de Broglie wavelength of a relativistic particle having rest mass $m_0$ and kinetic energy $E_k$. Show that it reduces to $\\lambda = h/\\sqrt{2m_0 E_k}$ in the non-relativistic limit.\n",
                "2. *Conceptual*: Why did Davisson and Germer select nickel crystals rather than polycrystalline materials for their electron scattering experiment?\n",
                "3. *Applied*: Calculate the accelerating voltage required in an electron microscope to achieve a resolving power of $0.05\\text{ nm}$ (assuming the resolution equals the de Broglie wavelength).\n"
            ])

        return "\n".join(parts)

    @classmethod
    def _generate_particle_in_box_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "The model of a particle confined within a one-dimensional infinite potential well—conventionally termed a particle in a box—constitutes the quintessential paradigm in quantum wave mechanics. "
            "In classical mechanics, a particle trapped between two impenetrable rigid walls bounces back and forth indefinitely with constant speed, possessing any arbitrarily chosen continuous energy value $E \\ge 0$. "
            "Furthermore, classical physics predicts an entirely uniform spatial probability of locating the particle at any coordinate between the boundaries. "
            "In sharp contrast, applying the time-independent Schrödinger wave equation reveals that spatial boundary confinement forces the continuous de Broglie matter waves to form discrete stationary standing waves. "
            "This geometric boundary confinement naturally and inescapably discretizes the admissible physical energy eigenvalues into a quantized spectrum, while dictating non-uniform spatial probability density distributions characterized by distinct nodes and anti-nodes.\n",
            "### 1. Theoretical Framework and Physical Mechanisms\n",
            "Consider a non-relativistic quantum particle of rest mass $m$ constrained to move along the horizontal axis $x$ between rigid barriers located at $x = 0$ and $x = L$. "
            "The potential energy distribution function $V(x)$ is formally defined by the piecewise profile:\n",
            "$$V(x) = \\begin{cases} 0 & \\text{for } 0 < x < L \\\\ \\infty & \\text{for } x \\le 0 \\text{ and } x \\ge L \\end{cases}$$\n",
            "Because the potential energy is infinite outside the spatial interval $[0, L]$, the probability of finding the particle in the external regions is identically zero, requiring the wave function to vanish strictly outside: $\\psi(x) = 0$ for $x < 0$ and $x > L$. "
            "To maintain continuity of the quantum wave function across the interface, $\\psi(x)$ must satisfy the Dirichlet boundary conditions:\n",
            "$$\\psi(0) = 0 \\quad \\text{and} \\quad \\psi(L) = 0$$\n",
            "### 2. Analytical Formulation and Governing Equations\n",
            "Inside the potential well where $V(x) = 0$, the spatial state of the particle is governed by the one-dimensional stationary Schrödinger equation:\n",
            "$$-\\frac{\\hbar^2}{2m} \\frac{d^2\\psi(x)}{dx^2} = E\\psi(x) \\implies \\frac{d^2\\psi(x)}{dx^2} + k^2 \\psi(x) = 0$$\n",
            "where the wavevector propagation constant $k$ is defined by $k^2 = \\frac{2mE}{\\hbar^2}$. "
            "Solving this second-order ordinary differential equation subject to the boundary constraints yields the discrete quantized energy eigenvalues:\n",
            "$$E_n = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2} = \\frac{n^2 h^2}{8mL^2}, \\quad n = 1, 2, 3, \\dots$$\n",
            "and the normalized spatial eigenfunctions:\n",
            "$$\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right)$$\n",
            "Here, $n$ is the principal quantum number. Note that $n = 0$ is physically inadmissible because it causes the wave function $\\psi_0(x)$ to vanish identically everywhere, implying zero total probability of finding the particle anywhere in the universe.\n"
        ]

        if derivation:
            parts.extend([
                "### 3. Step-by-Step Mathematical Derivation\n",
                "The formal derivation of the energy eigenvalues and spatial wave functions proceeds systematically through the standard mathematical sequence:\n",
                "**Step 1: General Solution of Governing Differential Equation.** The general solution to the homogeneous harmonic equation $\\psi''(x) + k^2\\psi(x) = 0$ is a linear superposition of orthogonal basis functions:\n",
                "$$\\psi(x) = A\\sin(kx) + B\\cos(kx)$$\n",
                "**Step 2: Imposition of Left Boundary Condition.** Evaluating the wave function at the origin $x = 0$:\n",
                "$$\\psi(0) = A\\sin(0) + B\\cos(0) = 0 \\implies B = 0$$\n",
                "Thus, the wave function reduces to $\\psi(x) = A\\sin(kx)$.\n",
                "**Step 3: Imposition of Right Boundary Condition.** Evaluating at the opposite boundary $x = L$:\n",
                "$$\\psi(L) = A\\sin(kL) = 0$$\n",
                "To avoid the trivial non-physical solution where $A = 0$, the trigonometric argument must satisfy:\n",
                "$$kL = n\\pi \\implies k_n = \\frac{n\\pi}{L}, \\quad n = 1, 2, 3, \\dots$$\n",
                "**Step 4: Energy Eigenvalues.** Substituting $k_n$ back into the definition of total energy $E = \\frac{\\hbar^2 k^2}{2m}$:\n",
                "$$E_n = \\frac{\\hbar^2}{2m}\\left(\\frac{n\\pi}{L}\\right)^2 = \\frac{n^2 \\pi^2 \\hbar^2}{2mL^2} = \\frac{n^2 h^2}{8mL^2}$$\n",
                "**Step 5: Normalization of Eigenfunctions.** Enforcing the Born probability normalization condition $\\int_0^L |\\psi_n(x)|^2 dx = 1$:\n",
                "$$A^2 \\int_0^L \\sin^2\\left(\\frac{n\\pi x}{L}\\right) dx = A^2 \\left(\\frac{L}{2}\\right) = 1 \\implies A = \\sqrt{\\frac{2}{L}}$$\n",
                "Hence, the complete normalized spatial eigenmodes are $\\psi_n(x) = \\sqrt{\\frac{2}{L}}\\sin\\left(\\frac{n\\pi x}{L}\\right)$.\n"
            ])

        parts.extend([
            "### 4. Quantitative Properties of Bound Quantum States\n",
            "The table below details the physical and spatial characteristics of the first four quantized eigenstates in a 1D potential well:\n",
            "| Quantum Number $n$ | State Designation | Energy Eigenvalue $E_n$ | Internal Nodes | Probability at Midpoint $P(L/2)$ | Physical Behavior |\n",
            "| :--- | :--- | :--- | :--- | :--- | :--- |\n",
            "| $n = 1$ | Ground State | $E_1 = \\frac{h^2}{8mL^2}$ | $0$ | Maximum ($2/L$) | Fundamental half-wave resonance; non-zero zero-point energy |\n",
            "| $n = 2$ | First Excited State | $E_2 = 4E_1$ | $1$ (at $x = L/2$) | Node ($0$) | Particle cannot be detected at center of box |\n",
            "| $n = 3$ | Second Excited State | $E_3 = 9E_1$ | $2$ (at $L/3, 2L/3$) | Maximum ($2/L$) | Anti-node at center with two intermediate zero-crossings |\n",
            "| $n = 4$ | Third Excited State | $E_4 = 16E_1$ | $3$ | Node ($0$) | High kinetic energy standing wave with four spatial lobes |\n",
            "\n### 5. Physical Insights and Zero-Point Energy\n",
            "Crucially, the lowest possible energy state ($n = 1$), termed the ground state or zero-point energy:\n",
            "$$E_1 = \\frac{h^2}{8mL^2} > 0$$\n",
            "is strictly non-zero. A quantum particle confined within a finite spatial domain can never be brought completely to rest. "
            "This phenomenon is a direct consequence of the Heisenberg uncertainty principle: confining the particle within a maximum position uncertainty $\\Delta x \\approx L$ requires an irreducible momentum uncertainty $\\Delta p \\ge \\frac{\\hbar}{2L}$, which mandates a non-vanishing minimum kinetic energy.\n",
            "\n### 6. Contemporary Nanotechnology Applications\n",
            "While the 1D infinite well is an idealized theoretical model, modern semiconductor fabrication realizes exact physical analogues:\n",
            "1. **Semiconductor Quantum Wells:** By sandwiching an ultra-thin layer of gallium arsenide (GaAs, thickness $\\sim 5\\text{ nm}$) between wider bandgap layers of aluminum gallium arsenide (AlGaAs), engineers fabricate nanoscale potential wells that confine conduction electrons in one dimension. This forms the basis of high-efficiency quantum well diode lasers used in fiber-optic communications.\n",
            "2. **Quantum Dots (Artificial Atoms):** Confining electrons in all three dimensions produces quantum dots. By tuning the box width $L$, the emission wavelength can be tuned continuously across the visible spectrum, powering quantum dot television displays (QLED) and fluorescent biological markers.\n"
        ])

        if include_num:
            parts.extend([
                "### 7. Worked Solved Numerical Problem\n",
                "**Problem Statement:** An electron is confined within a one-dimensional infinite potential well of width $L = 1.0\\text{ nm} = 1.0 \\times 10^{-9}\\text{ m}$. Calculate: (a) the ground state energy $E_1$ in Joules and electron-volts ($\text{eV}$), (b) the first excited state energy $E_2$, and (c) the wavelength of the photon emitted when the electron transitions from $n = 2$ to $n = 1$.\n",
                "**Given Data:**\n",
                "- Domain width $L = 1.0 \\times 10^{-9}\\text{ m}$\n",
                "- Electron mass $m_e = 9.109 \\times 10^{-31}\\text{ kg}$\n",
                "- Planck constant $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$\n",
                "- Speed of light $c = 3.0 \\times 10^8\\text{ m/s}$\n",
                "**Governing Formula:**\n",
                "$$E_n = \\frac{n^2 h^2}{8m_e L^2}, \\quad \\Delta E = E_2 - E_1 = 3E_1, \\quad \\lambda = \\frac{hc}{\\Delta E}$$\n",
                "**Substitution:**\n",
                "$$E_1 = \\frac{(6.626 \\times 10^{-34})^2}{8 \\times (9.109 \\times 10^{-31}) \\times (1.0 \\times 10^{-9})^2}$$\n",
                "**Calculation Steps:**\n",
                "1. Ground state energy $E_1$:\n",
                "$$E_1 = \\frac{(6.626 \\times 10^{-34})^2}{8 \\times (9.109 \\times 10^{-31}) \\times (1.0 \\times 10^{-9})^2} = \\frac{4.390 \\times 10^{-67}}{7.287 \\times 10^{-48}} = 6.025 \\times 10^{-20}\\text{ J}$$\n",
                "$$E_1 = \\frac{6.025 \\times 10^{-20}}{1.602 \\times 10^{-19}} = 0.3761\\text{ eV}$$\n",
                "2. First excited state energy $E_2$:\n",
                "$$E_2 = 2^2 \\times E_1 = 4 \\times 0.3761\\text{ eV} = 1.5044\\text{ eV} \\quad (2.410 \\times 10^{-19}\\text{ J})$$\n",
                "3. Energy difference and transition wavelength:\n",
                "$$\\Delta E = E_2 - E_1 = 1.5044 - 0.3761 = 1.1283\\text{ eV} = 1.8075 \\times 10^{-19}\\text{ J}$$\n",
                "$$\\lambda = \\frac{(6.626 \\times 10^{-34}) \\times (3.0 \\times 10^8)}{1.8075 \\times 10^{-19}} = 1.0997 \\times 10^{-6}\\text{ m} = 1099.7\\text{ nm}$$\n",
                "**Final Answer:**\n",
                "$$\\mathbf{E_1 = 0.376\\text{ eV}, \\quad E_2 = 1.504\\text{ eV}, \\quad \\lambda = 1100\\text{ nm} \\quad (\\text{Near Infrared})}$$\n"
            ])

        if include_qa:
            parts.extend([
                "### 8. Review Questions and Academic Exercises\n",
                "1. *Analytical*: Calculate the probability of finding a particle in the central third of an infinite potential well (i.e. from $x = L/3$ to $x = 2L/3$) in its ground state ($n=1$).\n",
                "2. *Conceptual*: Explain why the quantum number $n = 0$ is rejected for a particle in an infinite box, whereas $n = 0$ is physically valid for a harmonic oscillator.\n",
                "3. *Applied*: How does increasing the width of a semiconductor quantum well from $2\\text{ nm}$ to $10\\text{ nm}$ alter the emission wavelength of a laser fabricated from that well?\n"
            ])

        return "\n".join(parts)

    @classmethod
    def _generate_heisenberg_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "Formulated by Werner Heisenberg in 1927, the Uncertainty Principle establishes a fundamental epistemological and physical boundary upon the precision with which conjugate physical observables can be simultaneously determined. "
            "In classical deterministic mechanics, knowing the exact position $\\mathbf{r}(t)$ and momentum $\\mathbf{p}(t)$ of a particle at any initial instant completely defines its entire past and future trajectory through Hamilton's equations of motion. "
            "However, in quantum mechanics, material entities are described by spatially distributed wavepackets rather than localized point masses. "
            "Because localized wavepackets are constructed by superposing a continuous spectrum of Fourier plane wave harmonics, narrowing the spatial wavepacket envelope $\\Delta x$ inevitably broadens the spectrum of constituent wavenumbers $\\Delta k$, and consequently broadens the uncertainty in physical momentum $\\Delta p = \\hbar \\Delta k$. "
            "Thus, the uncertainty principle is not a flaw in experimental metrology or measurement instrumentation; it is an intrinsic mathematical property of Fourier transform pairs governing all wave phenomena in nature.\n",
            "### 1. Theoretical Framework and Mathematical Statement\n",
            "For any pair of canonically conjugate quantum mechanical observables represented by operators $\\hat{A}$ and $\\hat{B}$ that do not commute ($[\\hat{A}, \\hat{B}] \\ne 0$), the Robertson-Schrödinger theorem establishes that the product of their standard deviations satisfies:\n",
            "$$\\sigma_A \\sigma_B \\ge \\frac{1}{2} |\\langle [\\hat{A}, \\hat{B}] \\rangle|$$\n",
            "For the canonical position operator $\\hat{x} = x$ and momentum operator $\\hat{p}_x = -i\\hbar \\frac{\\partial}{\\partial x}$, their fundamental commutator is $[\\hat{x}, \\hat{p}_x] = i\\hbar$. "
            "Substituting this commutation relationship into the uncertainty theorem yields Heisenberg's famous position-momentum uncertainty relation:\n",
            "$$\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}$$\n",
            "where $\\hbar = \\frac{h}{2\\pi} = 1.0546 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ is the reduced Planck constant.\n",
            "Similarly, the conjugate relationship between total energy and temporal duration is captured by the energy-time uncertainty relation:\n",
            "$$\\Delta E \\cdot \\Delta t \\ge \\frac{\\hbar}{2}$$\n",
            "Here, $\\Delta t$ represents the characteristic lifetime or coherence duration of a quantum state, and $\\Delta E$ signifies the fundamental uncertainty (natural line width) in its energy level.\n"
        ]

        if derivation:
            parts.extend([
                "### 2. Step-by-Step Derivation from Fourier Wavepacket Analysis\n",
                "**Step 1: Wavepacket Formulation.** A localized one-dimensional matter wave packet is represented by the inverse Fourier integral of spatial plane waves:\n",
                "$$\\psi(x) = \\frac{1}{\\sqrt{2\\pi}} \\int_{-\\infty}^{\\infty} A(k) e^{ikx} dk$$\n",
                "where $A(k)$ is the spectral amplitude in wavenumber space $k$.\n",
                "**Step 2: Fourier Bandwidth Theorem.** Standard harmonic analysis demonstrates that for any Fourier transform pair, the product of the spatial root-mean-square width $\\Delta x$ and the wavenumber spectral width $\\Delta k$ satisfies the rigorous inequality:\n",
                "$$\\Delta x \\cdot \\Delta k \\ge \\frac{1}{2}$$\n",
                "(with equality holding uniquely for Gaussian wavepackets).\n",
                "**Step 3: Introduction of de Broglie Momentum.** According to de Broglie's hypothesis, the momentum of a quantum particle relates to its wavenumber by $p_x = \\hbar k$. Taking the differential uncertainty:\n",
                "$$\\Delta p_x = \\hbar \\Delta k \\implies \\Delta k = \\frac{\\Delta p_x}{\\hbar}$$\n",
                "**Step 4: Substitution into Bandwidth Inequality.** Substituting $\\Delta k$ into the Fourier inequality:\n",
                "$$\\Delta x \\cdot \\left(\\frac{\\Delta p_x}{\\hbar}\\right) \\ge \\frac{1}{2} \\implies \\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}$$\n",
                "This completes the mathematical proof, confirming that quantum uncertainty is an immediate consequence of the wave nature of matter.\n"
            ])

        parts.extend([
            "### 3. Physical Applications: Non-Existence of Electrons in the Nucleus\n",
            "A celebrated application of the uncertainty principle is proving that electrons cannot reside permanently within the atomic nucleus. "
            "Experimental nuclear scattering indicates that atomic nuclei possess radii on the order of $R \\approx 10^{-14}\\text{ m}$. "
            "If an electron were confined inside the nucleus, its maximum spatial uncertainty would be $\\Delta x \\approx 2R = 2 \\times 10^{-14}\\text{ m}$. "
            "Applying the uncertainty principle yields a minimum momentum uncertainty:\n",
            "$$\\Delta p \\ge \\frac{\\hbar}{2\\Delta x} = \\frac{1.055 \\times 10^{-34}}{2 \\times (2 \\times 10^{-14})} \\approx 2.64 \\times 10^{-21}\\text{ kg}\\cdot\\text{m/s}$$\n",
            "Because this momentum is highly relativistic, we evaluate the kinetic energy using $E \\approx pc \\approx (2.64 \\times 10^{-21}) \\times (3.0 \\times 10^8) = 7.92 \\times 10^{-13}\\text{ J} \\approx 4.95\\text{ MeV} \\approx 20\\text{ MeV}$. "
            "Experimental observations of beta decay reveal electron energies rarely exceeding $2\\text{ to }3\\text{ MeV}$, conclusively proving that electrons do not pre-exist inside the nucleus but are created dynamically at the instant of nuclear decay.\n"
        ])

        if include_num:
            parts.extend([
                "### 4. Worked Solved Numerical Problem\n",
                "**Problem Statement:** An excited atomic energy state has an average lifetime of $\\tau = 1.0 \\times 10^{-8}\\text{ s}$. Calculate: (a) the minimum uncertainty in the energy of this excited state in Joules and $\\text{eV}$, and (b) the fractional frequency line width $\\Delta \\nu / \\nu_0$ for an emitted spectral line of wavelength $\\lambda_0 = 600\\text{ nm}$.\n",
                "**Given Data:**\n",
                "- State lifetime $\\Delta t = 1.0 \\times 10^{-8}\\text{ s}$\n",
                "- Transition wavelength $\\lambda_0 = 600\\text{ nm} = 6.0 \\times 10^{-7}\\text{ m}$\n",
                "- Reduced Planck constant $\\hbar = 1.055 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$\n",
                "- Speed of light $c = 3.0 \\times 10^8\\text{ m/s}$\n",
                "**Governing Formulas:**\n",
                "$$\\Delta E \\ge \\frac{\\hbar}{2\\Delta t}, \\quad \\Delta E = h \\Delta \\nu = \\frac{\\hbar}{2\\Delta t} \\implies \\Delta \\nu = \\frac{1}{4\\pi \\Delta t}, \\quad \\nu_0 = \\frac{c}{\\lambda_0}$$\n",
                "**Calculation Steps:**\n",
                "1. Minimum energy uncertainty:\n",
                "$$\\Delta E = \\frac{1.055 \\times 10^{-34}}{2 \\times (1.0 \\times 10^{-8})} = 5.275 \\times 10^{-27}\\text{ J}$$\n",
                "$$\\Delta E = \\frac{5.275 \\times 10^{-27}}{1.602 \\times 10^{-19}} = 3.293 \\times 10^{-8}\\text{ eV}$$\n",
                "2. Natural frequency width:\n",
                "$$\\Delta \\nu = \\frac{1}{4\\pi \\times 1.0 \\times 10^{-8}} = 7.958 \\times 10^6\\text{ Hz} = 7.96\\text{ MHz}$$\n",
                "3. Transition frequency:\n",
                "$$\\nu_0 = \\frac{3.0 \\times 10^8}{6.0 \\times 10^{-7}} = 5.0 \\times 10^{14}\\text{ Hz}$$\n",
                "$$\\frac{\\Delta \\nu}{\\nu_0} = \\frac{7.958 \\times 10^6}{5.0 \\times 10^{14}} = 1.59 \\times 10^{-8}$$\n",
                "**Final Answer:**\n",
                "$$\\mathbf{\\Delta E = 3.29 \\times 10^{-8}\\text{ eV}, \\quad \\Delta \\nu = 7.96\\text{ MHz}, \\quad \\frac{\\Delta \\nu}{\\nu_0} = 1.59 \\times 10^{-8}}$$\n"
            ])

        if include_qa:
            parts.extend([
                "### 5. Review Questions and Academic Exercises\n",
                "1. *Analytical*: If the position of an electron is measured to an accuracy of $0.01\\text{ nm}$, compute the minimum uncertainty in its velocity. Compare this with its orbital speed in a Bohr orbit.\n",
                "2. *Conceptual*: Explain why the uncertainty principle does not prevent the simultaneous measurement of the position and velocity of a macroscopic automobile.\n"
            ])

        return "\n".join(parts)

    @classmethod
    def _generate_velocity_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "In wave physics, a single monochromatic harmonic wave extends infinitely throughout space and time, propagating with a single well-defined phase velocity $v_p = \\omega/k$. "
            "However, an infinite plane wave conveys no localized signal and cannot represent a localized physical particle. "
            "To represent a physical particle in quantum mechanics, one must construct a spatially confined wavepacket through the linear superposition of multiple plane waves possessing a continuous band of frequencies and wavenumbers. "
            "When such a wavepacket propagates through a dispersive medium, the individual harmonic wavefronts travel at the phase velocity, while the overall modulating envelope travels at the group velocity $v_g = d\\omega/dk$. "
            "A profound triumph of quantum mechanics is demonstrating that the group velocity of a de Broglie matter wavepacket identically matches the classical physical velocity of the particle.\n",
            "### 1. Analytical Formulations and Governing Relationships\n",
            "The phase velocity $v_p$ and group velocity $v_g$ are formally defined by:\n",
            "$$v_p = \\frac{\\omega}{k}, \\quad v_g = \\frac{d\\omega}{dk}$$\n",
            "where $\\omega = 2\\pi \\nu$ is the angular frequency (rad/s) and $k = 2\\pi / \\lambda$ is the wavenumber (rad/m). "
            "Using the product rule on $\\omega = k v_p$, the group velocity can be expressed in terms of phase velocity and wavelength dispersion (Rayleigh's formula):\n",
            "$$v_g = \\frac{d(k v_p)}{dk} = v_p + k \\frac{dv_p}{dk} = v_p - \\lambda \\frac{dv_p}{d\\lambda}$$\n"
        ]

        if derivation:
            parts.extend([
                "### 2. Derivation Proving Group Velocity Equals Particle Velocity\n",
                "**Step 1: Quantum Energy and Momentum.** According to the fundamental quantum relations, total particle energy $E$ and momentum $p$ correspond to:\n",
                "$$E = \\hbar \\omega, \\quad p = \\hbar k$$\n",
                "**Step 2: Group Velocity in Energy-Momentum Space.** Expressing $v_g$ in terms of $E$ and $p$:\n",
                "$$v_g = \\frac{d\\omega}{dk} = \\frac{d(\\hbar\\omega)}{d(\\hbar k)} = \\frac{dE}{dp}$$\n",
                "**Step 3: Non-Relativistic Evaluation.** For a non-relativistic particle of mass $m$, $E = \\frac{p^2}{2m}$. Differentiating with respect to momentum:\n",
                "$$v_g = \\frac{d}{dp}\\left(\\frac{p^2}{2m}\\right) = \\frac{2p}{2m} = \\frac{p}{m} = v_{\\text{particle}}$$\n",
                "**Step 4: Relativistic Evaluation.** In special relativity, $E^2 = p^2 c^2 + m_0^2 c^4$. Differentiating implicitly with respect to $p$:\n",
                "$$2E \\frac{dE}{dp} = 2p c^2 \\implies v_g = \\frac{dE}{dp} = \\frac{pc^2}{E}$$\n",
                "Since $E = \\gamma m_0 c^2$ and $p = \\gamma m_0 v$, we find:\n",
                "$$v_g = \\frac{(\\gamma m_0 v) c^2}{\\gamma m_0 c^2} = v$$\n",
                "Thus, in both relativistic and non-relativistic regimes, the group velocity of the quantum wavepacket identically equals the physical particle velocity.\n"
            ])

        parts.extend([
            "### 3. Comparison of Phase Velocity and Group Velocity in Dispersive Media\n",
            "| Propagation Regime | Mathematical Condition | Phase Velocity vs Group Velocity | Physical Manifestation |\n",
            "| :--- | :--- | :--- | :--- |\n",
            "| Non-Dispersive (Vacuum EM) | $\\frac{dv_p}{d\\lambda} = 0$ | $v_g = v_p = c$ | Light pulses propagate without distortion or spreading |\n",
            "| Normal Dispersion (Glass, Water) | $\\frac{dv_p}{d\\lambda} > 0$ | $v_g < v_p$ | Blue light propagates slower than red light; pulse broadens |\n",
            "| Anomalous Dispersion | $\\frac{dv_p}{d\\lambda} < 0$ | $v_g > v_p$ | Occurs near atomic absorption resonance bands |\n",
            "| De Broglie Wave (Non-relativistic) | $\\omega = \\frac{\\hbar k^2}{2m}$ | $v_p = \\frac{v}{2}, \\quad v_g = v$ | Phase velocity is half of particle velocity; envelope tracks particle |\n"
        ])

        return "\n".join(parts)

    @classmethod
    def _generate_schrodinger_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "Formulated by Erwin Schrödinger in 1926, the Schrödinger wave equation serves as the fundamental equation of motion in non-relativistic quantum mechanics, occupying a role analogous to Newton's second law in classical mechanics. "
            "Whereas Newton's mechanics determines the precise temporal trajectory of a point particle through vector forces, the Schrödinger equation determines the continuous temporal evolution and spatial distribution of the complex wave function $\\Psi(\\mathbf{r}, t)$. "
            "By associating physical observables with linear differential operators acting upon state functions, Schrödinger transformed the abstract matrix mechanics of Heisenberg into an accessible partial differential boundary-value problem.\n",
            "### 1. Analytical Formulations and Governing Equations\n",
            "The general one-dimensional **Time-Dependent Schrödinger Equation (TDSE)** governing the dynamical evolution of a quantum state in an arbitrary potential field $V(x, t)$ is:\n",
            "$$i\\hbar \\frac{\\partial \\Psi(x, t)}{\\partial t} = -\\frac{\\hbar^2}{2m} \\frac{\\partial^2 \\Psi(x, t)}{\\partial x^2} + V(x, t)\\Psi(x, t)$$\n",
            "where $i = \\sqrt{-1}$ is the imaginary unit, $\\hbar = h/2\\pi$ is the reduced Planck constant, and $m$ is the particle mass. "
            "In compact operator notation, the equation is written as $\\hat{E}\\Psi = \\hat{H}\\Psi$, where $\\hat{H} = -\\frac{\\hbar^2}{2m}\\nabla^2 + V$ is the Hamiltonian operator.\n",
            "When the potential energy is independent of time ($V = V(x)$), the system possesses stationary states. Using separation of variables $\\Psi(x, t) = \\psi(x) e^{-iEt/\\hbar}$, the equation reduces to the **Time-Independent Schrödinger Equation (TISE)**:\n",
            "$$-\\frac{\\hbar^2}{2m} \\frac{d^2 \\psi(x)}{dx^2} + V(x)\\psi(x) = E\\psi(x)$$\n",
            "where $E$ represents the energy eigenvalue of the stationary state.\n"
        ]

        if derivation:
            parts.extend([
                "### 2. Step-by-Step Derivation of Time-Independent Equation\n",
                "**Step 1: Separation of Variables.** Assume the full wave function factors into spatial and temporal components:\n",
                "$$\\Psi(x, t) = \\psi(x) \\phi(t)$$\n",
                "**Step 2: Substitution into TDSE.** Substituting into the time-dependent equation:\n",
                "$$i\\hbar \\psi(x) \\frac{d\\phi(t)}{dt} = -\\frac{\\hbar^2}{2m}\\phi(t)\\frac{d^2\\psi(x)}{dx^2} + V(x)\\psi(x)\\phi(t)$$\n",
                "**Step 3: Separation of Coordinates.** Dividing both sides by $\\Psi(x, t) = \\psi(x)\\phi(t)$:\n",
                "$$\\frac{i\\hbar}{\\phi(t)} \\frac{d\\phi(t)}{dt} = \\frac{1}{\\psi(x)} \\left[ -\\frac{\\hbar^2}{2m} \\frac{d^2\\psi(x)}{dx^2} + V(x)\\psi(x) \\right]$$\n",
                "Because the left side depends purely on $t$ while the right side depends purely on $x$, both sides must independently equal a common separation constant $E$.\n",
                "**Step 4: Spatial Equation.** Equating the spatial side to $E$ yields the TISE:\n",
                "$$-\\frac{\\hbar^2}{2m} \\frac{d^2\\psi(x)}{dx^2} + V(x)\\psi(x) = E\\psi(x)$$\n",
                "**Step 5: Temporal Solution.** Integrating the temporal equation $\\frac{d\\phi}{\\phi} = -\\frac{iE}{\\hbar} dt$ gives $\\phi(t) = e^{-iEt/\\hbar}$, establishing that stationary state probability densities $|\\Psi(x, t)|^2 = |\\psi(x)|^2$ are strictly static in time.\n"
            ])

        parts.extend([
            "### 3. Probability Conservation and Continuity Equation\n",
            "A vital requirement for physical consistency is that total probability is conserved over time. From the Schrödinger equation, one derives the probability continuity equation:\n",
            "$$\\frac{\\partial P}{\\partial t} + \\nabla \\cdot \\mathbf{J} = 0$$\n",
            "where $P(\\mathbf{r}, t) = |\\Psi(\\mathbf{r}, t)|^2$ is the probability density and $\\mathbf{J}$ is the probability current density vector:\n",
            "$$\\mathbf{J} = \\frac{\\hbar}{2mi}\\left( \\Psi^* \\nabla\\Psi - \\Psi \\nabla\\Psi^* \\right)$$\n",
            "This continuity equation guarantees that quantum probability flows through space like an incompressible fluid without leaking, ensuring that the normalization $\\int |\\Psi|^2 d^3r = 1$ remains preserved for all time.\n"
        ])

        return "\n".join(parts)

    @classmethod
    def _generate_operators_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "In classical mechanics, physical observables such as position, momentum, energy, and angular momentum are treated as ordinary continuous scalar or vector variables. "
            "In quantum mechanics, according to the Dirac-von Neumann axiomatic formulation, every physically measurable observable is associated with a linear Hermitian operator acting on a state vector in Hilbert space. "
            "When an experimental measurement of an observable $\\hat{A}$ is performed on a quantum system, the only possible measurement outcomes are the discrete or continuous eigenvalues $a_n$ satisfying the eigenvalue equation $\\hat{A}\\psi_n = a_n \\psi_n$.\n",
            "### 1. Canonical Quantum Operators\n",
            "The table below catalogues the fundamental quantum mechanical operators in one-dimensional coordinate representation:\n",
            "| Observable | Classical Variable | Quantum Operator Symbol | Coordinate Representation Formula | Commutation Property |\n",
            "| :--- | :--- | :--- | :--- | :--- |\n",
            "| Position | $x$ | $\\hat{x}$ | $x$ | Commutes with functions of position |\n",
            "| Linear Momentum | $p_x$ | $\\hat{p}_x$ | $-i\\hbar \\frac{\\partial}{\\partial x}$ | $[\\hat{x}, \\hat{p}_x] = i\\hbar$ |\n",
            "| Kinetic Energy | $T$ | $\\hat{T}$ | $-\\frac{\\hbar^2}{2m} \\frac{\\partial^2}{\\partial x^2}$ | Constructed from $\\hat{p}_x^2 / 2m$ |\n",
            "| Potential Energy | $V(x)$ | $\\hat{V}$ | $V(x)$ | Multiplication operator |\n",
            "| Total Energy (Hamiltonian) | $H$ | $\\hat{H}$ | $-\\frac{\\hbar^2}{2m} \\frac{\\partial^2}{\\partial x^2} + V(x)$ | Dictates stationary energy states |\n",
            "| Angular Momentum | $L_z$ | $\\hat{L}_z$ | $-i\\hbar \\frac{\\partial}{\\partial \\phi}$ | $[\\hat{L}_x, \\hat{L}_y] = i\\hbar \\hat{L}_z$ |\n",
            "\n### 2. Mathematical Properties of Hermitian Operators\n",
            "An operator $\\hat{A}$ is formally defined as Hermitian if it equals its Hermitian adjoint: $\\hat{A} = \\hat{A}^\\dagger$, meaning that for any square-integrable wave functions $\\psi_1$ and $\\psi_2$:\n",
            "$$\\int_{-\\infty}^\\infty \\psi_1^* (\\hat{A} \\psi_2) dx = \\int_{-\\infty}^\\infty (\\hat{A} \\psi_1)^* \\psi_2 dx$$\n",
            "Hermitian operators possess two vital mathematical properties indispensable to physical reality:\n",
            "1. **Real Eigenvalues:** All eigenvalues of a Hermitian operator are strictly real numbers, guaranteeing that physical measurement outcomes are real observables rather than complex quantities.\n",
            "2. **Orthogonality of Eigenstates:** Eigenfunctions corresponding to distinct non-degenerate eigenvalues are mutually orthogonal: $\\int \\psi_m^* \\psi_n dx = \\delta_{mn}$.\n"
        ]
        return "\n".join(parts)

    @classmethod
    def _generate_wave_function_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "In 1926, Max Born proposed the statistical probability interpretation of the quantum mechanical wave function $\\Psi(\\mathbf{r}, t)$, a breakthrough for which he was awarded the 1954 Nobel Prize in Physics. "
            "Born recognized that while the wave function itself is a complex quantity ($\\\\Psi \\in \\mathbb{C}$) and cannot be directly detected by physical probes, its absolute square possesses direct physical reality. "
            "Specifically, the quantity $P(\\mathbf{r}, t) = |\\Psi(\\mathbf{r}, t)|^2 = \\Psi^* \\Psi$ represents the spatial probability density of locating the particle at position $\\mathbf{r}$ at time $t$.\n",
            "### 1. Mathematical Formulation and Normalization\n",
            "The probability $dP$ of finding a particle within an infinitesimal volume element $d^3r = dx\\,dy\\,dz$ centered at coordinates $(x, y, z)$ is:\n",
            "$$dP = |\\Psi(x, y, z, t)|^2 dx\\,dy\\,dz$$\n",
            "Because the particle must exist somewhere within the universe with absolute certainty (100% probability), any physically admissible wave function must satisfy the total normalization condition:\n",
            "$$\\int_{-\\infty}^{\\infty} \\int_{-\\infty}^{\\infty} \\int_{-\\infty}^{\\infty} |\\Psi(x, y, z, t)|^2 dx\\,dy\\,dz = 1$$\n",
            "### 2. Standard Boundary Conditions for Admissible Wave Functions\n",
            "To be physically admissible as a legitimate quantum state, a candidate wave function $\\Psi$ must satisfy four rigorous Dirichlet-Neumann conditions:\n",
            "- **Single-Valued:** $\\Psi(x)$ must possess only one value at each point in space, preventing ambiguous probabilities.\n",
            "- **Continuous:** $\\Psi(x)$ must be continuous across all spatial domains, preventing unphysical infinite forces.\n",
            "- **Continuous First Spatial Derivative:** $\\frac{\\partial \\Psi}{\\partial x}$ must be continuous wherever the potential energy $V(x)$ is finite, ensuring finite kinetic energy.\n",
            "- **Square-Integrable:** $\\int |\\Psi|^2 dx < \\infty$, ensuring the state can be normalized to unity.\n"
        ]
        return "\n".join(parts)

    @classmethod
    def _generate_quantum_apps_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Engineering Applications of Quantum Mechanics\n",
            "The principles of quantum mechanics provide the technological foundation for modern electronics, photonics, and nanoscale metrology. "
            "By engineering wave function confinement, tunneling barriers, and quantized energy states, contemporary engineers design devices that perform operations impossible within the constraints of classical physics.\n",
            "### 1. Survey of Primary Quantum Technologies\n",
            "| Technology | Quantum Mechanism | Operational Principle | Technological Impact |\n",
            "| :--- | :--- | :--- | :--- |\n",
            "| Scanning Tunneling Microscope (STM) | Quantum Barrier Penetration | Electrons tunnel through vacuum gap ($I \\propto e^{-2\\kappa d}$) | Atomic-resolution surface imaging and atom manipulation |\n",
            "| Transmission Electron Microscope (TEM) | De Broglie Matter Waves | High-voltage electron beam ($\\lambda \\sim 0.003\\text{ nm}$) | Sub-angstrom structural analysis of materials and viruses |\n",
            "| Quantum Well Diode Lasers | 1D Spatial Confinement | 2D electron density of states in nanoscale GaAs wells | High-efficiency optical sources for fiber telecommunications |\n",
            "| Semiconductor Quantum Dots | 3D Spatial Confinement | Discrete atomic-like energy levels tuned by nanocrystal size | Ultra-pure color displays (QLED) and biomedical markers |\n",
            "| SQUIDs (Superconducting Quantum Interference) | Josephson Junction Tunneling | Magnetic flux quantization in superconducting rings | Ultra-sensitive detection of neural magnetic fields |\n",
            "\n### 2. Engineering Analysis of Quantum Tunneling in STM\n",
            "In classical mechanics, a particle of energy $E$ encountering a potential barrier of height $V_0 > E$ is strictly reflected. "
            "In quantum mechanics, the wave function decays exponentially inside the classically forbidden region: $\\psi(x) \\propto e^{-\\kappa x}$, where $\\kappa = \\frac{\\sqrt{2m(V_0 - E)}}{\\hbar}$. "
            "For a barrier of width $d$, the transmission tunneling probability is $T \\approx e^{-2\\kappa d}$. "
            "Because the tunneling current in an STM scales exponentially with tip-to-sample distance $d$, a change in separation of merely $0.1\\text{ nm}$ (one atomic diameter) alters the tunneling current by a full order of magnitude (~$1000\\%$). "
            "This extreme spatial sensitivity enables the STM to resolve individual atoms on conductive surfaces.\n"
        ]
        return "\n".join(parts)

    @classmethod
    def _generate_fiber_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "Optical fibers serve as the physical backbone of global telecommunications, enabling high-bandwidth transmission of optical data signals across intercontinental distances. "
            "The foundational principle governing wave propagation in optical dielectric waveguides is total internal reflection (TIR) occurring at the cylindrical interface between an inner high-index core ($n_1$) and an outer lower-index cladding ($n_2$).\n",
            "### 1. Analytical Formulations and Governing Parameters\n",
            "The light-gathering capability of an optical fiber is characterized by its **Numerical Aperture (NA)** and maximum **Acceptance Angle ($\\theta_a$)**:\n",
            "$$\\text{NA} = \\sin\\theta_a = \\sqrt{n_1^2 - n_2^2} = n_1 \\sqrt{2\\Delta}$$\n",
            "where $\\Delta = \\frac{n_1 - n_2}{n_1} \\approx \\frac{n_1^2 - n_2^2}{2n_1^2}$ is the fractional refractive index contrast.\n",
            "The number of guided modes propagating through a step-index fiber is governed by the dimensionless **Normalized Frequency (V-number)**:\n",
            "$$V = \\frac{2\\pi a}{\\lambda} \\text{NA} = \\frac{2\\pi a}{\\lambda}\\sqrt{n_1^2 - n_2^2}$$\n",
            "where $a$ is the core radius and $\\lambda$ is the operating optical wavelength. When $V < 2.405$, the fiber operates in single-mode regime ($HE_{11}$ mode only), eliminating intermodal dispersion entirely.\n"
        ]
        return "\n".join(parts)

    @classmethod
    def _generate_laser_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "The acronym LASER stands for Light Amplification by Stimulated Emission of Radiation. "
            "Unlike conventional incandescent or fluorescent thermal sources that emit incoherent light through spontaneous emission, lasers produce highly monochromatic, spatially and temporally coherent, directional, and high-intensity beams. "
            "To achieve laser oscillation, three fundamental physical conditions must be fulfilled: (1) an active gain medium possessing metastable energy states, (2) a pumping mechanism to achieve population inversion ($N_2 > N_1$), and (3) an optical feedback resonator cavity.\n",
            "### 1. Einstein Coefficients and Radiative Transition Rates\n",
            "In 1917, Albert Einstein showed that radiative atomic transitions involve three competing mechanisms: stimulated absorption, spontaneous emission, and stimulated emission. "
            "In thermodynamic equilibrium with a blackbody radiation field of spectral density $\\rho(\\nu)$, the ratio of Einstein coefficients satisfies:\n",
            "$$\\frac{A_{21}}{B_{21}} = \\frac{8\\pi h \\nu^3}{c^3}, \\quad B_{12} = \\frac{g_2}{g_1} B_{21}$$\n",
            "Because the spontaneous-to-stimulated emission ratio scales with the cube of the transition frequency ($\\nu^3$), achieving population inversion and sustained laser action becomes progressively more demanding at optical, ultraviolet, and X-ray frequencies compared to microwave regimes (masers).\n"
        ]
        return "\n".join(parts)

    @classmethod
    def _generate_wave_optics_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "Wave optics investigates optical phenomena where the finite wavelength of electromagnetic radiation cannot be neglected, invalidating ray optics approximations. "
            "The primary phenomena include interference (the redistribution of light energy resulting from the superposition of two or more mutually coherent waves) and diffraction (the bending and spreading of wavefronts around geometric obstacles).\n",
            "### 1. Analytical Formulations of Interference and Newton's Rings\n",
            "In thin-film interference by division of amplitude, Stokes' treatment establishes that reflection at an optically denser medium introduces a phase shift of $\\pi$ radians, equivalent to a path difference of $\\lambda/2$. "
            "The net path difference for a film of thickness $t$ and refractive index $\\mu$ at refraction angle $r$ is:\n",
            "$$\\Delta = 2\\mu t \\cos r - \\frac{\\lambda}{2}$$\n",
            "For Newton's rings formed by a plano-convex lens of radius of curvature $R$, the dark fringe diameters in reflected light satisfy:\n",
            "$$D_n^2 = 4n\\lambda R \\implies D_n = 2\\sqrt{n\\lambda R}$$\n",
            "confirming that ring diameter scales proportionally to $\\sqrt{n}$, causing interference fringes to crowd closer together at larger radii.\n"
        ]
        return "\n".join(parts)

    @classmethod
    def _generate_semiconductor_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "Semiconductor physics explores the electrical and optical properties of materials whose conductivity lies between metals and insulators. "
            "In crystalline solids, the periodic potential of atomic nuclei splits discrete atomic states into continuous valence and conduction energy bands separated by a forbidden energy bandgap $E_g$.\n",
            "### 1. Carrier Concentration and Hall Effect Formulations\n",
            "In an intrinsic semiconductor, electron concentration $n$ equals hole concentration $p = n_i$, governed by:\n",
            "$$n_i = \\sqrt{N_c N_v} \\exp\\left(-\\frac{E_g}{2k_B T}\\right)$$\n",
            "When a current $I$ flows longitudinally through a semiconductor specimen in a transverse magnetic field $B_z$, the Lorentz force deflects charge carriers, creating a measurable transverse **Hall Voltage**:\n",
            "$$V_H = \\frac{R_H I B_z}{w} = -\\frac{I B_z}{n e w}$$\n",
            "where $R_H = -1/ne$ is the Hall coefficient and $w$ is the specimen thickness. Measuring the sign and magnitude of $V_H$ reveals whether the semiconductor is n-type or p-type and quantifies majority carrier density.\n"
        ]
        return "\n".join(parts)

    @classmethod
    def _generate_quantum_intro_section(cls, topic: str, subtopic: str, subject: str, include_num: bool, include_qa: bool, derivation: bool) -> str:
        parts = [
            f"### Foundations and Scope of {subtopic}\n",
            "The transition from nineteenth-century classical physics to quantum mechanics was necessitated by catastrophic failures in classical models when confronted with atomic-scale phenomena. "
            "Classical electromagnetic theory and statistical thermodynamics predicted that a blackbody cavity would emit infinite power at ultraviolet frequencies—a dilemma known as the ultraviolet catastrophe. "
            "In 1900, Max Planck resolved this crisis by proposing that energy exchange between cavity oscillators and radiation fields occurs in discrete packets or quanta: $E = nh\\nu$, introducing the fundamental quantum of action $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$.\n",
            "### 1. Historical Breakdown of Classical Mechanics\n",
            "Four crucial experimental discoveries exposed the fundamental limitations of classical continuum mechanics:\n",
            "1. **Blackbody Radiation Spectrum:** Rayleigh-Jeans classical law $u(\\nu)d\\nu = \\frac{8\\pi \\nu^2}{c^3}k_B T d\\nu$ diverged at high frequencies. Planck's quantum distribution matched experimental measurements perfectly across all spectral bands.\n",
            "2. **Photoelectric Effect:** Heinrich Hertz and Philipp Lenard observed electron emission governed instantaneously by light frequency rather than light intensity, explained by Albert Einstein (1905) through light quanta (photons) with energy $E = h\\nu$.\n",
            "3. **Discrete Atomic Line Spectra:** Rutherford's planetary atomic model predicted orbital electrons would continuously radiate energy and spiral into the nucleus within $10^{-11}\\text{ s}$. Niels Bohr (1913) postulated stationary orbits with quantized angular momentum $L = n\\hbar$.\n",
            "4. **Compton Scattering (1923):** Arthur Compton demonstrated that X-rays scattered from electrons experience a wavelength increase $\\Delta \\lambda = \\frac{h}{m_0 c}(1 - \\cos\\theta)$, proving photons carry discrete relativistic momentum $p = h/\\lambda$.\n",
            "\n### 2. The Postulates of Modern Quantum Mechanics\n",
            "Modern quantum theory formalizes these discoveries into an axiomatic framework:\n",
            "- **Postulate 1 (State Function):** The complete physical state of a system is represented by a normalized complex wave function $\\Psi(\\mathbf{r}, t)$ residing in a Hilbert space.\n",
            "- **Postulate 2 (Observables):** Every measurable physical observable corresponds to a linear Hermitian operator.\n",
            "- **Postulate 3 (Eigenvalues):** The only measurable values of an observable $\\hat{A}$ are its eigenvalues $a_n$ from $\\hat{A}\\psi_n = a_n\\psi_n$.\n",
            "- **Postulate 4 (Born Rule):** The probability of measuring eigenvalue $a_n$ is $|\\langle \\psi_n | \\Psi \\rangle|^2$.\n",
            "- **Postulate 5 (Time Evolution):** The state evolves continuously according to the time-dependent Schrödinger equation $i\\hbar \\frac{\\partial \\Psi}{\\partial t} = \\hat{H}\\Psi$.\n"
        ]
        return "\n".join(parts)

