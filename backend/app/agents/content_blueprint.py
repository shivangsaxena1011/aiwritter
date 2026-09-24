from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
import uuid


class SectionPurposeType(str, Enum):
    HISTORICAL_MOTIVATION = "HISTORICAL_MOTIVATION"
    CORE_CONCEPT = "CORE_CONCEPT"
    DEFINITION = "DEFINITION"
    PHYSICAL_INTERPRETATION = "PHYSICAL_INTERPRETATION"
    MATHEMATICAL_FORMULATION = "MATHEMATICAL_FORMULATION"
    DERIVATION = "DERIVATION"
    EXPERIMENT = "EXPERIMENT"
    EXPERIMENTAL_EVIDENCE = "EXPERIMENTAL_EVIDENCE"
    COMPARISON = "COMPARISON"
    APPLICATION = "APPLICATION"
    ENGINEERING_SIGNIFICANCE = "ENGINEERING_SIGNIFICANCE"
    LIMITATION = "LIMITATION"
    EXAMPLE = "EXAMPLE"
    SUMMARY = "SUMMARY"
    TRANSITION = "TRANSITION"


@dataclass
class SectionContract:
    section_id: str
    topic_id: str
    subtopic_title: str
    purpose: SectionPurposeType
    learning_objective: str
    required_claims: List[str] = field(default_factory=list)
    required_equations: List[str] = field(default_factory=list)
    allowed_concepts: List[str] = field(default_factory=list)
    forbidden_concepts: List[str] = field(default_factory=list)
    prerequisite_context: List[str] = field(default_factory=list)
    source_ids: List[str] = field(default_factory=list)
    target_depth: str = "Detailed"
    target_word_range: Tuple[int, int] = (250, 450)
    repetition_context: Dict[str, Any] = field(default_factory=dict)
    table_required: bool = False
    diagram_required: bool = False
    diagram_type: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_id": self.section_id,
            "topic_id": self.topic_id,
            "subtopic_title": self.subtopic_title,
            "purpose": self.purpose.value,
            "learning_objective": self.learning_objective,
            "required_claims": self.required_claims,
            "required_equations": self.required_equations,
            "allowed_concepts": self.allowed_concepts,
            "forbidden_concepts": self.forbidden_concepts,
            "prerequisite_context": self.prerequisite_context,
            "target_depth": self.target_depth,
            "target_word_range": list(self.target_word_range),
            "table_required": self.table_required,
            "diagram_required": self.diagram_required,
            "diagram_type": self.diagram_type
        }


@dataclass
class TopicBoundaryContract:
    topic_id: str
    topic_title: str
    allowed_concepts: List[str] = field(default_factory=list)
    prerequisite_concepts: List[str] = field(default_factory=list)
    forbidden_concepts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "topic_title": self.topic_title,
            "allowed_concepts": self.allowed_concepts,
            "prerequisite_concepts": self.prerequisite_concepts,
            "forbidden_concepts": self.forbidden_concepts
        }


@dataclass
class ContentBlueprint:
    topic_id: str
    topic_title: str
    topic_type: str
    learning_objectives: List[str] = field(default_factory=list)
    prerequisite_topics: List[str] = field(default_factory=list)
    required_concepts: List[str] = field(default_factory=list)
    optional_concepts: List[str] = field(default_factory=list)
    excluded_concepts: List[str] = field(default_factory=list)
    historical_context_required: bool = False
    derivation_required: bool = False
    derivation_targets: List[str] = field(default_factory=list)
    experiment_required: bool = False
    experiment_targets: List[str] = field(default_factory=list)
    application_required: bool = False
    application_targets: List[str] = field(default_factory=list)
    comparison_table_required: bool = False
    diagram_required: bool = False
    diagram_targets: List[str] = field(default_factory=list)
    numerical_examples_required: bool = False
    qa_required: bool = False
    estimated_depth: str = "Detailed"
    target_word_range: Tuple[int, int] = (1200, 2000)
    section_plan: List[SectionContract] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic_id": self.topic_id,
            "topic_title": self.topic_title,
            "topic_type": self.topic_type,
            "learning_objectives": self.learning_objectives,
            "prerequisite_topics": self.prerequisite_topics,
            "required_concepts": self.required_concepts,
            "optional_concepts": self.optional_concepts,
            "excluded_concepts": self.excluded_concepts,
            "historical_context_required": self.historical_context_required,
            "derivation_required": self.derivation_required,
            "derivation_targets": self.derivation_targets,
            "experiment_required": self.experiment_required,
            "experiment_targets": self.experiment_targets,
            "application_required": self.application_required,
            "application_targets": self.application_targets,
            "comparison_table_required": self.comparison_table_required,
            "diagram_required": self.diagram_required,
            "diagram_targets": self.diagram_targets,
            "numerical_examples_required": self.numerical_examples_required,
            "qa_required": self.qa_required,
            "estimated_depth": self.estimated_depth,
            "target_word_range": list(self.target_word_range),
            "section_plan": [s.to_dict() for s in self.section_plan]
        }


class ContentBlueprintPlanner:
    """Generates rigorous, topic-specific ContentBlueprints and TopicBoundaryContracts."""

    @classmethod
    def create_blueprint(
        cls,
        topic_title: str,
        subject: str = "Engineering Physics",
        academic_level: str = "University",
        include_numericals: bool = False,
        include_questions: bool = False,
        include_diagrams: bool = True
    ) -> ContentBlueprint:
        t_clean = topic_title.lower().strip()
        t_id = str(uuid.uuid4())[:8]

        # 1. de Broglie Hypothesis
        if "de broglie" in t_clean:
            sections = [
                SectionContract(
                    section_id=f"{t_id}_1", topic_id=t_id, subtopic_title="Historical Motivation and the Postulate of Matter Waves",
                    purpose=SectionPurposeType.HISTORICAL_MOTIVATION,
                    learning_objective="Explain classical breakdown, radiation paradoxes, and the symmetry reasoning leading to matter waves.",
                    required_claims=["Radiation exhibits particle properties, so material entities must exhibit wave properties."],
                    allowed_concepts=["blackbody", "photoelectric", "matter waves", "pilot wave", "symmetry of nature"],
                    forbidden_concepts=["laser population inversion", "semiconductor band gap", "Brewster angle"]
                ),
                SectionContract(
                    section_id=f"{t_id}_2", topic_id=t_id, subtopic_title="The de Broglie Matter-Wave Postulate",
                    purpose=SectionPurposeType.CORE_CONCEPT,
                    learning_objective="Formulate de Broglie's pilot wave relation connecting particulate momentum to oscillation wavelength.",
                    required_claims=["Every moving material body has associated wave of wavelength lambda = h/p."],
                    required_equations=["\\lambda = \\frac{h}{p}", "\\lambda = \\frac{h}{mv}"],
                    allowed_concepts=["momentum", "wavelength", "Planck constant", "probability amplitude"],
                    forbidden_concepts=["laser", "semiconductor"]
                ),
                SectionContract(
                    section_id=f"{t_id}_3", topic_id=t_id, subtopic_title="Derivation of the de Broglie Wavelength",
                    purpose=SectionPurposeType.DERIVATION,
                    learning_objective="Derive lambda = h/p from photon relativity and express it in terms of electrostatic accelerating potential.",
                    required_claims=["Equating photon E = hc/lambda and E = pc yields p = h/lambda; accelerating potential V gives lambda = 1.227/sqrt(V) nm."],
                    required_equations=["\\lambda = \\frac{h}{p}", "\\lambda = \\frac{h}{\\sqrt{2mqV}}", "\\lambda_e = \\frac{1.227}{\\sqrt{V}}\\text{ nm}"],
                    allowed_concepts=["photon momentum", "special relativity", "kinetic energy", "electron accelerating potential"],
                    forbidden_concepts=["laser", "diffusion"]
                ),
                SectionContract(
                    section_id=f"{t_id}_4", topic_id=t_id, subtopic_title="Experimental Confirmation by Davisson-Germer and G. P. Thomson",
                    purpose=SectionPurposeType.EXPERIMENTAL_EVIDENCE,
                    learning_objective="Detail the nickel crystal electron diffraction experiment and transmission foil diffraction proving wave character.",
                    required_claims=["Davisson-Germer peak at 54V and 50 degrees confirmed lambda = 0.165 nm matching de Broglie theory."],
                    allowed_concepts=["nickel crystal", "Bragg law", "54 V accelerating voltage", "G. P. Thomson gold foil", "circular diffraction rings"],
                    forbidden_concepts=["laser cavity", "p-n junction"],
                    table_required=True,
                    diagram_required=include_diagrams,
                    diagram_type="apparatus diagram"
                ),
                SectionContract(
                    section_id=f"{t_id}_5", topic_id=t_id, subtopic_title="Electron Microscopy and Contemporary Nanoscale Engineering",
                    purpose=SectionPurposeType.APPLICATION,
                    learning_objective="Explain why sub-angstrom electron wavelengths enable high-resolution Transmission Electron Microscopy (TEM).",
                    required_claims=["Picometer de Broglie wavelengths of high-energy electrons overcome Abbe diffraction limits in light microscopy."],
                    allowed_concepts=["Transmission Electron Microscopy (TEM)", "Scanning Electron Microscopy (SEM)", "sub-angstrom resolution", "Abbe diffraction limit"],
                    forbidden_concepts=["laser population inversion"]
                )
            ]
            return ContentBlueprint(
                topic_id=t_id, topic_title=topic_title, topic_type="LAW_OR_PRINCIPLE",
                learning_objectives=["Understand wave-particle duality", "Derive matter-wave wavelength", "Analyze Davisson-Germer experiment"],
                prerequisite_topics=["Photoelectric Effect", "Introduction to Quantum Mechanics"],
                required_concepts=["matter waves", "de Broglie wavelength", "Davisson-Germer", "G. P. Thomson", "TEM"],
                historical_context_required=True, derivation_required=True, derivation_targets=["\\lambda = \\frac{h}{p}"],
                experiment_required=True, experiment_targets=["Davisson-Germer experiment"],
                application_required=True, application_targets=["Transmission Electron Microscopy"],
                comparison_table_required=True, diagram_required=include_diagrams, diagram_targets=["Davisson-Germer apparatus"],
                numerical_examples_required=include_numericals, qa_required=include_questions,
                section_plan=sections
            )

        # 2. Particle in a 1D Box (Infinite Potential Well)
        if "box" in t_clean or "infinite potential well" in t_clean or "potential well" in t_clean:
            sections = [
                SectionContract(
                    section_id=f"{t_id}_1", topic_id=t_id, subtopic_title="Physical Model, Infinite Well Geometry, and Boundary Constraints",
                    purpose=SectionPurposeType.CORE_CONCEPT,
                    learning_objective="Formulate the one-dimensional infinite potential well boundary-value problem.",
                    required_claims=["Impenetrable barriers require wavefunction psi(x) to vanish identically at x <= 0 and x >= L."],
                    required_equations=["V(x) = 0 \\text{ for } 0 < x < L, \\quad V(x) = \\infty \\text{ otherwise}"],
                    allowed_concepts=["infinite potential well", "boundary conditions", "wavefunction continuity", "spatial confinement"],
                    forbidden_concepts=["population inversion", "laser cavity"]
                ),
                SectionContract(
                    section_id=f"{t_id}_2", topic_id=t_id, subtopic_title="Analytical Derivation of Wavefunctions and Energy Eigenvalues",
                    purpose=SectionPurposeType.DERIVATION,
                    learning_objective="Solve the time-independent Schrödinger equation and apply boundary conditions to derive discrete energy levels.",
                    required_claims=["Boundary conditions enforce kL = n*pi, yielding quantized energy eigenvalues and sinusoidal standing waves."],
                    required_equations=["-\\frac{\\hbar^2}{2m}\\frac{d^2\\psi}{dx^2} = E\\psi", "\\psi_n(x) = \\sqrt{\\frac{2}{L}} \\sin\\left(\\frac{n\\pi x}{L}\\right)", "E_n = \\frac{n^2 h^2}{8mL^2}"],
                    allowed_concepts=["Schrodinger equation", "Dirichlet boundary conditions", "normalization", "energy quantization"],
                    forbidden_concepts=["laser", "heat diffusion"]
                ),
                SectionContract(
                    section_id=f"{t_id}_3", topic_id=t_id, subtopic_title="Physical Interpretation of Eigenstates and Zero-Point Energy",
                    purpose=SectionPurposeType.PHYSICAL_INTERPRETATION,
                    learning_objective="Explain why the ground state energy is strictly non-zero and connect it to Heisenberg uncertainty.",
                    required_claims=["The ground state n=1 possesses finite zero-point energy E1 = h^2/(8mL^2) due to spatial confinement."],
                    required_equations=["E_1 = \\frac{h^2}{8mL^2} > 0"],
                    allowed_concepts=["zero-point energy", "standing wave nodes", "probability density", "Heisenberg uncertainty principle"],
                    forbidden_concepts=["semiconductor depletion"],
                    table_required=True,
                    diagram_required=include_diagrams,
                    diagram_type="energy-level diagram"
                ),
                SectionContract(
                    section_id=f"{t_id}_4", topic_id=t_id, subtopic_title="Nanotechnology and Quantum Well Heterostructure Devices",
                    purpose=SectionPurposeType.APPLICATION,
                    learning_objective="Examine engineering applications in semiconductor quantum wells, quantum dots, and optoelectronic displays.",
                    required_claims=["Artificially engineered potential wells in semiconductor heterostructures enable tunable bandgap lasers and quantum dot displays."],
                    allowed_concepts=["quantum dots", "quantum well lasers", "nanostructures", "size-tunable emission", "QLED"],
                    forbidden_concepts=["classical fluid dynamics"]
                )
            ]
            return ContentBlueprint(
                topic_id=t_id, topic_title=topic_title, topic_type="DERIVATION_HEAVY",
                learning_objectives=["Formulate boundary conditions", "Derive quantized energies En = n^2 h^2 / 8mL^2", "Interpret zero-point energy"],
                prerequisite_topics=["Time-Independent Schrödinger Equation", "Physical Interpretation of the Wave Function"],
                required_concepts=["infinite potential well", "boundary conditions", "energy eigenvalues", "zero-point energy"],
                derivation_required=True, derivation_targets=["E_n = \\frac{n^2 h^2}{8mL^2}"],
                application_required=True, application_targets=["quantum dots", "quantum well heterostructures"],
                comparison_table_required=True, diagram_required=include_diagrams, diagram_targets=["energy-level diagram"],
                numerical_examples_required=include_numericals, qa_required=include_questions,
                section_plan=sections
            )

        # 3. Operators
        if "operator" in t_clean:
            sections = [
                SectionContract(
                    section_id=f"{t_id}_1", topic_id=t_id, subtopic_title="Motivation for Operator Formalism in Quantum Mechanics",
                    purpose=SectionPurposeType.CORE_CONCEPT,
                    learning_objective="Explain why physical observables are represented by linear operators acting on Hilbert state vectors.",
                    required_claims=["Every physically measurable observable corresponds to a linear Hermitian operator in quantum mechanics."],
                    allowed_concepts=["observables", "linear operators", "Hilbert space", "quantum state vector"],
                    forbidden_concepts=["laser", "fiber"]
                ),
                SectionContract(
                    section_id=f"{t_id}_2", topic_id=t_id, subtopic_title="Position, Momentum, and Hamiltonian Operators in Coordinate Space",
                    purpose=SectionPurposeType.MATHEMATICAL_FORMULATION,
                    learning_objective="State standard quantum operators in coordinate representation and construct the total energy Hamiltonian.",
                    required_claims=["Position is a multiplication operator, momentum is -i*hbar*d/dx, and Hamiltonian is kinetic plus potential energy."],
                    required_equations=["\\hat{x} = x", "\\hat{p}_x = -i\\hbar \\frac{\\partial}{\\partial x}", "\\hat{H} = -\\frac{\\hbar^2}{2m}\\nabla^2 + V"],
                    allowed_concepts=["coordinate representation", "momentum operator", "Hamiltonian operator"],
                    forbidden_concepts=["laser", "semiconductor"],
                    table_required=True
                ),
                SectionContract(
                    section_id=f"{t_id}_3", topic_id=t_id, subtopic_title="Commutator Algebra and Fundamental Commutation Relations",
                    purpose=SectionPurposeType.MATHEMATICAL_FORMULATION,
                    learning_objective="Evaluate commutator brackets [x, px] = i*hbar and connect non-commutativity to simultaneous measurability.",
                    required_claims=["The canonical commutator [x, px] = i*hbar proves position and momentum cannot be simultaneously known without uncertainty."],
                    required_equations=["[\\hat{A}, \\hat{B}] = \\hat{A}\\hat{B} - \\hat{B}\\hat{A}", "[\\hat{x}, \\hat{p}_x] = i\\hbar"],
                    allowed_concepts=["commutator bracket", "canonical commutation relation", "simultaneous observables"],
                    forbidden_concepts=["laser cavity"]
                ),
                SectionContract(
                    section_id=f"{t_id}_4", topic_id=t_id, subtopic_title="Hermitian Operators and Reality of Physical Eigenvalues",
                    purpose=SectionPurposeType.PHYSICAL_INTERPRETATION,
                    learning_objective="Demonstrate why operators representing physical observables must be Hermitian to ensure real expectation values.",
                    required_claims=["Hermitian operators guarantee strictly real eigenvalues and mutually orthogonal eigenfunctions."],
                    allowed_concepts=["Hermitian operator", "real eigenvalues", "expectation values", "orthogonality"],
                    forbidden_concepts=["laser"]
                )
            ]
            return ContentBlueprint(
                topic_id=t_id, topic_title=topic_title, topic_type="MATHEMATICAL",
                learning_objectives=["Understand operator representation", "Evaluate canonical commutators", "Establish Hermitian properties"],
                prerequisite_topics=["Physical Interpretation of the Wave Function"],
                required_concepts=["operators", "momentum operator", "commutator", "Hermitian"],
                comparison_table_required=True, diagram_required=False,
                numerical_examples_required=include_numericals, qa_required=include_questions,
                section_plan=sections
            )

        # 4. Heisenberg Uncertainty Principle
        if "uncertainty" in t_clean or "heisenberg" in t_clean:
            sections = [
                SectionContract(
                    section_id=f"{t_id}_1", topic_id=t_id, subtopic_title="Physical Concept and Measurement Limits in Quantum Systems",
                    purpose=SectionPurposeType.CORE_CONCEPT,
                    learning_objective="Explain why uncertainty is an intrinsic wave property rather than an experimental measurement flaw.",
                    required_claims=["Wave-particle duality inherently restricts the simultaneous localization of position and wavenumber."],
                    allowed_concepts=["wavepacket dispersion", "conjugate variables", "intrinsic quantum indeterminacy"],
                    forbidden_concepts=["laser", "fiber"]
                ),
                SectionContract(
                    section_id=f"{t_id}_2", topic_id=t_id, subtopic_title="Mathematical Formulation of Position-Momentum and Energy-Time Uncertainty",
                    purpose=SectionPurposeType.MATHEMATICAL_FORMULATION,
                    learning_objective="State the exact mathematical bounds for position-momentum and energy-time uncertainty relations.",
                    required_claims=["The product of standard deviations satisfies Delta x * Delta p >= hbar/2 and Delta E * Delta t >= hbar/2."],
                    required_equations=["\\Delta x \\cdot \\Delta p_x \\ge \\frac{\\hbar}{2}", "\\Delta E \\cdot \\Delta t \\ge \\frac{\\hbar}{2}"],
                    allowed_concepts=["position-momentum uncertainty", "energy-time uncertainty", "reduced Planck constant"],
                    forbidden_concepts=["laser population inversion"]
                ),
                SectionContract(
                    section_id=f"{t_id}_3", topic_id=t_id, subtopic_title="Gedanken Experiments: Single-Slit Diffraction and Gamma-Ray Microscope",
                    purpose=SectionPurposeType.EXPERIMENTAL_EVIDENCE,
                    learning_objective="Analyze Bohr and Heisenberg thought experiments illustrating the measurement recoil and photon momentum transfer.",
                    required_claims=["Narrowing a slit to define position Delta x causes diffraction spreading, imparting uncertain transverse momentum Delta px."],
                    allowed_concepts=["single-slit diffraction", "gamma-ray microscope", "photon recoil", "diffraction angle"],
                    forbidden_concepts=["optical resonator"],
                    diagram_required=include_diagrams,
                    diagram_type="apparatus diagram"
                ),
                SectionContract(
                    section_id=f"{t_id}_4", topic_id=t_id, subtopic_title="Physical Consequences: Non-Existence of Electrons in the Atomic Nucleus",
                    purpose=SectionPurposeType.APPLICATION,
                    learning_objective="Apply Delta x * Delta p >= hbar/2 to prove that free electrons cannot reside inside atomic nuclei.",
                    required_claims=["Confining an electron within nuclear dimensions (~10^-14 m) yields kinetic energy > 20 MeV, far exceeding observed beta decay energies (~4 MeV)."],
                    allowed_concepts=["nuclear confinement", "kinetic energy of electron", "beta decay energy limit"],
                    forbidden_concepts=["laser", "semiconductor"]
                )
            ]
            return ContentBlueprint(
                topic_id=t_id, topic_title=topic_title, topic_type="LAW_OR_PRINCIPLE",
                learning_objectives=["Understand position-momentum uncertainty", "Analyze Gedanken experiments", "Prove non-existence of electrons in nucleus"],
                prerequisite_topics=["Wave Nature of Particles", "de Broglie Hypothesis"],
                required_concepts=["Heisenberg uncertainty", "conjugate observables", "nuclear electron non-existence"],
                diagram_required=include_diagrams, diagram_targets=["single-slit diffraction wavepacket"],
                numerical_examples_required=include_numericals, qa_required=include_questions,
                section_plan=sections
            )

        # 5. Generic Default Fallback for Any Other Syllabus Topic
        sections = [
            SectionContract(
                section_id=f"{t_id}_1", topic_id=t_id, subtopic_title=f"Foundational Principles and Physical Scope of {topic_title}",
                purpose=SectionPurposeType.CORE_CONCEPT,
                learning_objective=f"Establish the physical basis, postulates, and scope of {topic_title}.",
                allowed_concepts=[topic_title.lower()],
                forbidden_concepts=["Configuration Alpha", "\\dot{S}_{gen}"]
            ),
            SectionContract(
                section_id=f"{t_id}_2", topic_id=t_id, subtopic_title=f"Mathematical Formulation and Governing Equations of {topic_title}",
                purpose=SectionPurposeType.MATHEMATICAL_FORMULATION,
                learning_objective=f"Formulate the quantitative relations, equations, and parameters governing {topic_title}.",
                allowed_concepts=[topic_title.lower()],
                forbidden_concepts=["Configuration Alpha", "\\dot{S}_{gen}"]
            ),
            SectionContract(
                section_id=f"{t_id}_3", topic_id=t_id, subtopic_title=f"Physical Interpretation and Engineering Relevance of {topic_title}",
                purpose=SectionPurposeType.APPLICATION,
                learning_objective=f"Analyze the physical consequences, experimental verification, and contemporary applications of {topic_title}.",
                allowed_concepts=[topic_title.lower()],
                forbidden_concepts=["Configuration Alpha", "\\dot{S}_{gen}"]
            )
        ]
        return ContentBlueprint(
            topic_id=t_id, topic_title=topic_title, topic_type="CONCEPTUAL",
            learning_objectives=[f"Master foundations of {topic_title}", f"Apply governing principles of {topic_title}"],
            required_concepts=[topic_title.lower()],
            numerical_examples_required=include_numericals, qa_required=include_questions,
            section_plan=sections
        )

    @classmethod
    def create_boundary_contract(cls, topic_title: str) -> TopicBoundaryContract:
        t_clean = topic_title.lower().strip()
        t_id = str(uuid.uuid4())[:8]

        allowed = [t_clean]
        prereqs = []
        forbidden = ["configuration alpha", "configuration beta", "\\dot{s}_{gen}", "dot{s}_{gen}"]

        if "photoelectric" in t_clean:
            allowed.extend(["photon", "work function", "stopping potential", "threshold frequency", "Einstein equation"])
            forbidden.extend(["population inversion", "stimulated emission", "metastable state", "optical resonator", "acceptance cone", "numerical aperture"])
        elif "de broglie" in t_clean:
            allowed.extend(["matter waves", "pilot wave", "Davisson-Germer", "G. P. Thomson", "TEM", "accelerating potential"])
            forbidden.extend(["population inversion", "optical resonator", "acceptance cone", "numerical aperture", "depletion width"])
        elif "box" in t_clean or "well" in t_clean:
            allowed.extend(["infinite potential well", "boundary conditions", "wavefunction", "quantization", "zero-point energy", "quantum dots"])
            forbidden.extend(["population inversion", "Brewster's angle", "acceptance cone", "numerical aperture"])
        elif "operator" in t_clean:
            allowed.extend(["linear operator", "commutator", "Hamiltonian", "eigenvalue", "Hermitian"])
            forbidden.extend(["population inversion", "acceptance cone", "numerical aperture", "spontaneous emission"])

        return TopicBoundaryContract(
            topic_id=t_id,
            topic_title=topic_title,
            allowed_concepts=allowed,
            prerequisite_concepts=prereqs,
            forbidden_concepts=forbidden
        )

