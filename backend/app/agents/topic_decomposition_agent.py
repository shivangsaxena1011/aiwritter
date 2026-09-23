"""
TopicDecompositionAgent — Decomposes Major Topics into pedagogically structured,
subject-aware sections. Adapts structure specifically for Physics, Engineering,
Mathematics, Computer Science, or General Sciences.
"""

import logging
from typing import Dict, Any, List, Optional
from backend.app.agents.base import BaseAgent, AgentContext, AgentResult
from backend.app.services.ai.base import AIProvider

from backend.app.agents.topic_classifier import TopicTypeClassifier, TopicType
from backend.app.agents.subject_knowledge_model import SubjectKnowledgeModel

logger = logging.getLogger(__name__)

# Subject Archetype Section Blueprints
PHYSICS_BLUEPRINT = [
    "Conceptual Introduction",
    "Physical Concept and Theory",
    "Mathematical Formulation",
    "Derivation of Governing Equations",
    "Physical Interpretation",
    "Practical Applications",
    "Limitations and Boundary Conditions"
]

CS_BLUEPRINT = [
    "Conceptual Overview",
    "Formal Definition and Specifications",
    "Algorithmic Working and Data Flow",
    "Implementation and Syntax",
    "Complexity Analysis",
    "Common Pitfalls and Edge Cases",
    "Industrial Applications"
]

MATH_BLUEPRINT = [
    "Rigorous Definition",
    "Fundamental Axioms and Theorems",
    "Formal Proof and Derivation",
    "Analytical Properties",
    "Worked Mathematical Example",
    "Applications and Generalizations"
]

ENGINEERING_BLUEPRINT = [
    "Engineering Principles and Foundations",
    "Governing Equations and Physical Laws",
    "System Architecture and Component Design",
    "Operational Working Mechanism",
    "Engineering Applications and Case Studies",
    "Design Constraints and Failure Modes"
]

GENERAL_BLUEPRINT = [
    "Introduction and Foundational Concepts",
    "Theoretical Framework",
    "Analytical Formulation",
    "Practical Applications",
    "Summary and Critical Observations"
]

class TopicDecompositionAgent(BaseAgent):
    """
    Intelligently breaks down major topics into subject-specific academic sections.
    """

    def __init__(self, ai_provider: Optional[AIProvider] = None):
        super().__init__(ai_provider)

    async def run(self, context: AgentContext, topic_title: str = "", **kwargs) -> AgentResult:
        topic_info = kwargs.get("topic_info", {"title": topic_title})
        decomp = await self.decompose_topic(
            topic_title=topic_title or topic_info.get("title", ""),
            subject=context.subject or context.book_title,
            academic_level=context.academic_level,
            requires_derivation=topic_info.get("requires_derivation", False),
            requires_numericals=topic_info.get("requires_numericals", False)
        )
        return AgentResult(status="success", data=decomp)

    async def decompose_topic(
        self,
        topic_title: str,
        subject: str,
        academic_level: str = "University / Reference",
        requires_derivation: bool = False,
        requires_numericals: bool = False
    ) -> Dict[str, Any]:
        """
        Generates an intelligent, non-templated decomposition adapted to the specific subject domain.
        """
        # Attempt AI decomposition
        if self.ai:
            try:
                ai_sections = await self._decompose_with_ai(
                    topic_title, subject, academic_level, requires_derivation, requires_numericals
                )
                if ai_sections and len(ai_sections.get("sections", [])) >= 3:
                    return ai_sections
            except Exception as e:
                logger.warning(f"AI Topic Decomposition failed ({e}), using domain heuristic blueprint")

        # Deterministic domain heuristic
        return self._decompose_heuristically(topic_title, subject, requires_derivation, requires_numericals)

    async def _decompose_with_ai(
        self,
        topic_title: str,
        subject: str,
        academic_level: str,
        requires_derivation: bool,
        requires_numericals: bool
    ) -> Dict[str, Any]:
        prompt = f"""You are the TopicDecompositionAgent in an academic publishing engine.
Decompose the following major topic into a coherent, pedagogically sound sequence of sub-sections.

SUBJECT: {subject}
MAJOR TOPIC: {topic_title}
ACADEMIC LEVEL: {academic_level}
REQUIRES DERIVATION: {requires_derivation}
REQUIRES NUMERICAL EXAMPLES: {requires_numericals}

INSTRUCTIONS:
1. Do NOT blindly output generic headings. The structure MUST be tailored to whether this is Physics, Computer Science, Mathematics, Engineering, or a general science.
2. If Physics: focus on Introduction -> Physical Concept -> Mathematical Formulation -> Derivation -> Physical Interpretation -> Applications -> Limitations.
3. If Computer Science: focus on Concept -> Formal Specs -> Working / Architecture -> Implementation -> Complexity -> Real-world Applications.
4. If Mathematics: focus on Definition -> Theorems -> Proof / Derivation -> Properties -> Applications.
5. If Engineering: focus on Principles -> Governing Equations -> System Design -> Operation -> Trade-offs / Failure Modes.
6. Only include Derivation section if mathematically applicable.
7. Only include Worked Numerical Example if computational/numerical requested.

Return JSON:
{{
  "topic": "{topic_title}",
  "subject_domain": "Physics | Computer Science | Mathematics | Engineering | General Science",
  "sections": [
    {{
      "title": "Section Title",
      "purpose": "Brief description of what this section explains",
      "section_type": "concept | derivation | numerical | diagram_focus | application"
    }}
  ]
}}
"""
        return await self.ai.generate_structured(prompt)

    CANONICAL_DECOMPOSITIONS: Dict[str, List[Dict[str, str]]] = {
        "de broglie hypothesis": [
            {"title": "Historical Motivation and Inadequacy of Classical Physics", "purpose": "Classical breakdown, radiation paradoxes, and the matter-wave proposal", "section_type": "concept"},
            {"title": "The de Broglie Matter-Wave Postulate", "purpose": "Associating wave attributes with particulate matter", "section_type": "concept"},
            {"title": "Derivation of the de Broglie Wavelength", "purpose": "Analytical formulation linking momentum to wavelength", "section_type": "derivation"},
            {"title": "Phase Velocity and Group Velocity of Matter Waves", "purpose": "Propagation dynamics and wavepacket velocity matching particle motion", "section_type": "concept"},
            {"title": "Experimental Confirmation by Davisson and Germer", "purpose": "Nickel crystal electron diffraction and wavelength measurement", "section_type": "concept"},
            {"title": "Physical Interpretation and Matter Wave Limitations", "purpose": "Probability amplitude representation and relativistic constraints", "section_type": "concept"},
            {"title": "Electron Microscopy and Modern Engineering Applications", "purpose": "Sub-angstrom resolving power in TEM/SEM nanoscale instruments", "section_type": "application"}
        ],
        "particle in a 1d infinite potential well (particle in a box)": [
            {"title": "Physical Concept and Infinite Well Geometry", "purpose": "Idealized potential confinement and boundary specification", "section_type": "concept"},
            {"title": "Mathematical Formulation of Time-Independent Schrödinger Equation", "purpose": "Differential equations inside and outside the barrier", "section_type": "concept"},
            {"title": "Analytical Derivation and Boundary Conditions", "purpose": "Applying Dirichlet boundary conditions to determine spatial wave functions", "section_type": "derivation"},
            {"title": "Quantization of Energy Eigenvalues and Spatial Eigenfunctions", "purpose": "Discrete energy spectra and zero-point ground state", "section_type": "derivation"},
            {"title": "Normalization and Spatial Probability Density Distributions", "purpose": "Born postulate, probability density, and nodal structures", "section_type": "concept"},
            {"title": "Quantum Well Lasers and Nanostructure Applications", "purpose": "Engineering applications in quantum heterostructures and optoelectronics", "section_type": "application"},
            {"title": "Correspondence Principle and Classical Limit", "purpose": "High quantum number convergence to classical continuum behavior", "section_type": "concept"}
        ],
        "particle in a box": [
            {"title": "Physical Concept and Infinite Well Geometry", "purpose": "Idealized potential confinement and boundary specification", "section_type": "concept"},
            {"title": "Mathematical Formulation of Time-Independent Schrödinger Equation", "purpose": "Differential equations inside and outside the barrier", "section_type": "concept"},
            {"title": "Analytical Derivation and Boundary Conditions", "purpose": "Applying Dirichlet boundary conditions to determine spatial wave functions", "section_type": "derivation"},
            {"title": "Quantization of Energy Eigenvalues and Spatial Eigenfunctions", "purpose": "Discrete energy spectra and zero-point ground state", "section_type": "derivation"},
            {"title": "Normalization and Spatial Probability Density Distributions", "purpose": "Born postulate, probability density, and nodal structures", "section_type": "concept"},
            {"title": "Quantum Well Lasers and Nanostructure Applications", "purpose": "Engineering applications in quantum heterostructures and optoelectronics", "section_type": "application"},
            {"title": "Correspondence Principle and Classical Limit", "purpose": "High quantum number convergence to classical continuum behavior", "section_type": "concept"}
        ],
        "heisenberg uncertainty principle": [
            {"title": "Physical Concept and the Measurement Problem", "purpose": "Wavepacket dispersion and intrinsic limits on conjugate observables", "section_type": "concept"},
            {"title": "Mathematical Formulation and Wavepacket Derivation", "purpose": "Fourier analysis of wavepackets yielding Delta x Delta p >= hbar/2", "section_type": "derivation"},
            {"title": "Experimental Evidence and Single-Slit Diffraction", "purpose": "Demonstrating transverse momentum spreading upon narrow spatial confinement", "section_type": "concept"},
            {"title": "Physical Interpretation and Non-Existence of Electrons in the Nucleus", "purpose": "Consequences of zero-point energy and nuclear stability", "section_type": "concept"},
            {"title": "Quantum Limits in Precision Metrology and Sensing", "purpose": "Standard quantum limits in interferometry and nanoscale devices", "section_type": "application"}
        ],
        "introduction to quantum mechanics": [
            {"title": "Inadequacy of Classical Physics and Blackbody Radiation", "purpose": "Ultraviolet catastrophe, Planck hypothesis, and discrete energy quanta", "section_type": "concept"},
            {"title": "Photoelectric Effect and Einstein's Photon Theory", "purpose": "Particle-like light quanta, work function, and kinetic energy", "section_type": "concept"},
            {"title": "Foundational Postulates of Modern Quantum Theory", "purpose": "State vectors, wave functions, and wave-particle duality", "section_type": "concept"}
        ],
        "wave nature of particles": [
            {"title": "Historical Evolution from Radiation Duality to Matter Waves", "purpose": "Connecting optical diffraction to electron wave hypotheses", "section_type": "concept"},
            {"title": "Mathematical Expression of Matter Wavelengths", "purpose": "Relating wavelength to kinetic energy and accelerating potentials", "section_type": "concept"},
            {"title": "Davisson-Germer and Thomson Electron Diffraction", "purpose": "Experimental verification of de Broglie relations in crystals", "section_type": "concept"},
            {"title": "Wavepacket Representation and Phase vs Group Velocity", "purpose": "Wave superposition matching physical particle speed", "section_type": "derivation"},
            {"title": "Physical Interpretation and Born Probability Amplitude", "purpose": "Statistical interpretation of matter wave amplitudes", "section_type": "concept"},
            {"title": "Electron Beam Technologies in Semiconductor Metrology", "purpose": "Application in TEM, SEM, and electron beam lithography", "section_type": "application"}
        ],
        "phase velocity and group velocity": [
            {"title": "Superposition of Harmonic Waves and Wavepacket Formation", "purpose": "Phase relationships and modulating envelope dynamics", "section_type": "concept"},
            {"title": "Mathematical Derivation of Phase Velocity and Group Velocity", "purpose": "Deriving vp = omega/k and vg = d omega / dk", "section_type": "derivation"},
            {"title": "Physical Interpretation and Velocity of Matter Waves", "purpose": "Proving group velocity equals particle velocity in dispersion media", "section_type": "concept"}
        ],
        "operators": [
            {"title": "Operator Formalism in Quantum Mechanics", "purpose": "Associating physical observables with linear operators in Hilbert space", "section_type": "concept"},
            {"title": "Position, Momentum, and Hamiltonian Differential Operators", "purpose": "Exact mathematical expressions and differential definitions", "section_type": "concept"},
            {"title": "Commutator Algebra and Heisenberg Uncertainty", "purpose": "Evaluating [x, p] = i hbar and compatible vs incompatible observables", "section_type": "derivation"},
            {"title": "Hermitian Operators and Observable Conservation", "purpose": "Real eigenvalues, orthogonality, and expectation values", "section_type": "concept"}
        ],
        "eigenvalues and eigenfunctions": [
            {"title": "The Quantum Eigenvalue Equation", "purpose": "Defining A psi = a psi and physical measurement postulate", "section_type": "concept"},
            {"title": "Mathematical Derivation of Real Eigenvalues for Hermitian Operators", "purpose": "Proof that observable quantities possess strictly real eigenvalues", "section_type": "derivation"},
            {"title": "Orthogonality and Completeness of Eigenfunctions", "purpose": "Expansion of arbitrary state functions in orthonormal bases", "section_type": "concept"}
        ],
        "time-dependent schrodinger equation": [
            {"title": "Physical Motivation and Operator Formulation", "purpose": "Constructing dynamic wave equation from conservation of total energy", "section_type": "concept"},
            {"title": "Mathematical Derivation of the Time-Dependent Equation", "purpose": "Combining energy operator with Hamiltonian to yield i hbar dPsi/dt = H Psi", "section_type": "derivation"},
            {"title": "Probability Current Density and Continuity Equation", "purpose": "Proving local conservation of quantum probability", "section_type": "derivation"},
            {"title": "Physical Significance in Dynamic Quantum Systems", "purpose": "Time evolution of non-stationary states and wavepacket propagation", "section_type": "concept"}
        ],
        "time-independent schrodinger equation": [
            {"title": "Stationary States and Separation of Variables", "purpose": "Factoring space-time wave function into spatial and harmonic temporal parts", "section_type": "concept"},
            {"title": "Derivation of the Time-Independent Differential Formulation", "purpose": "Isolating energy eigenvalue equation H psi = E psi", "section_type": "derivation"},
            {"title": "Boundary Conditions for Physically Admissible Wave Functions", "purpose": "Continuity, single-valuedness, and finite integral constraints", "section_type": "concept"}
        ],
        "physical interpretation of wave function": [
            {"title": "Max Born Probability Postulate", "purpose": "Interpreting |Psi|^2 as spatial probability density", "section_type": "concept"},
            {"title": "Normalization Condition and Mathematical Rigor", "purpose": "Total unit probability integration across coordinate space", "section_type": "derivation"},
            {"title": "Wavepacket Collapse and Quantum Measurement", "purpose": "Transition from superposition to definitive eigenstate upon observation", "section_type": "concept"}
        ],
        "applications of quantum mechanics": [
            {"title": "Quantum Barrier Penetration and Tunneling Devices", "purpose": "Tunnel diodes, alpha decay, and Scanning Tunneling Microscopy (STM)", "section_type": "application"},
            {"title": "Quantum Heterostructures, Dots, and Semiconductor Devices", "purpose": "Nanoscale confinement in LEDs, quantum well lasers, and SQUIDs", "section_type": "application"}
        ]
    }

    def _decompose_heuristically(
        self,
        topic_title: str,
        subject: str,
        requires_derivation: bool,
        requires_numericals: bool
    ) -> Dict[str, Any]:
        topic_clean = topic_title.strip().lower()
        domain = SubjectKnowledgeModel.get_subject_domain(subject, topic_title).title()

        # Check canonical decompositions first
        for canonical_key, sec_list in self.CANONICAL_DECOMPOSITIONS.items():
            if canonical_key in topic_clean or topic_clean in canonical_key:
                sections = [dict(s) for s in sec_list]
                if requires_numericals and not any("numerical" in s["title"].lower() for s in sections):
                    sections.append({
                        "title": f"Worked Numerical Examples on {topic_title}",
                        "purpose": "Step-by-step verified numerical problem solutions with units",
                        "section_type": "numerical"
                    })
                return {
                    "topic": topic_title,
                    "subject_domain": domain,
                    "complexity_level": "High" if len(sections) >= 5 else "Medium",
                    "sections": sections
                }

        # Otherwise, dynamically classify topic using TopicTypeClassifier
        labels = TopicTypeClassifier.classify(topic_title, subject, requires_derivation, requires_numericals)
        pedagogical_flow = TopicTypeClassifier.get_pedagogical_structure(labels, topic_title)

        sections = []
        for step in pedagogical_flow:
            s_type = "derivation" if "derivation" in step["title"].lower() else ("application" if "application" in step["title"].lower() else ("numerical" if "numerical" in step["title"].lower() else "concept"))
            sections.append({
                "title": step["title"],
                "purpose": step["pedagogy"],
                "section_type": s_type
            })

        return {
            "topic": topic_title,
            "subject_domain": domain,
            "complexity_level": "High" if len(sections) >= 5 else ("Low" if len(sections) <= 2 else "Medium"),
            "sections": sections
        }
