"""
TopicTypeClassifier — Multi-label classification for academic syllabus topics.
Assigns pedagogical classifications to steer content structuring organically
rather than forcing rigid template structures.
"""

from typing import List, Set, Dict, Any
from enum import Enum

class TopicType(str, Enum):
    CONCEPTUAL = "CONCEPTUAL"
    DEFINITIONAL = "DEFINITIONAL"
    LAW_OR_PRINCIPLE = "LAW_OR_PRINCIPLE"
    DERIVATION_HEAVY = "DERIVATION_HEAVY"
    MATHEMATICAL = "MATHEMATICAL"
    EXPERIMENTAL = "EXPERIMENTAL"
    APPARATUS = "APPARATUS"
    PROCESS = "PROCESS"
    ALGORITHM = "ALGORITHM"
    SYSTEM_ARCHITECTURE = "SYSTEM_ARCHITECTURE"
    COMPARATIVE = "COMPARATIVE"
    APPLICATION = "APPLICATION"
    NUMERICAL = "NUMERICAL"
    HISTORICAL = "HISTORICAL"
    MIXED = "MIXED"

class TopicTypeClassifier:
    """
    Classifies topics based on domain keywords and academic requirements.
    """

    def __init__(self, ai_provider: Any = None):
        self.ai = ai_provider

    def classify_topic(
        self,
        topic_title: str,
        subject: str = "",
        requires_derivation: bool = False,
        requires_numericals: bool = False
    ) -> Dict[str, Any]:
        """Instance method returning topic types and recommended pedagogical structure."""
        types = self.classify(topic_title, subject, requires_derivation, requires_numericals)
        structure = self.get_pedagogical_structure(types, topic_title)
        return {
            "topic": topic_title,
            "topic_types": types,
            "recommended_sections": structure
        }

    def generate_pedagogical_structure(
        self,
        topic_title: str,
        subject: str = "",
        requires_derivation: bool = False,
        requires_numericals: bool = False
    ) -> Dict[str, Any]:
        """Generates dynamic pedagogical structure."""
        return self.classify_topic(topic_title, subject, requires_derivation, requires_numericals)

    @classmethod
    def classify(
        cls,
        topic_title: str,
        subject: str = "",
        requires_derivation: bool = False,
        requires_numericals: bool = False
    ) -> List[TopicType]:
        """Returns assigned TopicType labels for a given topic."""
        text = f"{subject} {topic_title}".lower()
        labels: Set[TopicType] = set()

        # Derivation Heavy & Mathematical
        if requires_derivation or any(w in text for w in ["schrodinger", "derivation", "derive", "equation", "proof", "box", "well", "formulation", "theorem", "eigenvalue"]):
            labels.add(TopicType.DERIVATION_HEAVY)
            labels.add(TopicType.MATHEMATICAL)

        # Law or Principle
        if any(w in text for w in ["hypothesis", "principle", "law", "postulate", "axiom", "theorem", "rule"]):
            labels.add(TopicType.LAW_OR_PRINCIPLE)
            labels.add(TopicType.CONCEPTUAL)

        # Historical / Experimental
        if any(w in text for w in ["introduction", "history", "evolution", "discovery", "inadequacy", "early", "origin"]):
            labels.add(TopicType.HISTORICAL)
        if any(w in text for w in ["experiment", "davisson", "germer", "thomson", "newton's ring", "double slit", "observation", "verification", "measurement"]):
            labels.add(TopicType.EXPERIMENTAL)

        # Apparatus
        if any(w in text for w in ["apparatus", "laser", "interferometer", "microscope", "grating", "diode", "transistor", "fiber structure", "device"]):
            labels.add(TopicType.APPARATUS)

        # Application
        if any(w in text for w in ["application", "implementation", "technology", "industrial", "device", "metrology", "use", "engineering"]):
            labels.add(TopicType.APPLICATION)

        # Comparative
        if any(w in text for w in ["difference", "distinction", "comparison", "vs", "versus", "comparison between"]):
            labels.add(TopicType.COMPARATIVE)

        # Process / Algorithm
        if any(w in text for w in ["process", "algorithm", "cycle", "method", "procedure", "pumping", "propagation"]):
            labels.add(TopicType.PROCESS)

        # Numerical
        if requires_numericals or any(w in text for w in ["numerical", "problem", "calculation", "worked example"]):
            labels.add(TopicType.NUMERICAL)

        # Default fallback
        if not labels:
            labels.add(TopicType.CONCEPTUAL)
            labels.add(TopicType.DEFINITIONAL)
        elif len(labels) == 1:
            labels.add(TopicType.CONCEPTUAL)

        return sorted(list(labels), key=lambda x: x.value)

    @classmethod
    def get_pedagogical_structure(cls, labels: List[TopicType], topic_title: str) -> List[Dict[str, str]]:
        """
        Dynamically recommends section flow based on topic classifications.
        Never outputs generic boilerplate titles.
        """
        sections: List[Dict[str, str]] = []
        lbl_set = set(labels)

        # 1. Historical or Conceptual Foundation
        if TopicType.HISTORICAL in lbl_set or TopicType.LAW_OR_PRINCIPLE in lbl_set:
            sections.append({
                "title": f"Historical Motivation and Physical Foundations of {topic_title}",
                "pedagogy": "Establish classical limits and experimental catalyst"
            })
        else:
            sections.append({
                "title": f"Physical Concept and Fundamental Principles of {topic_title}",
                "pedagogy": "Clear operational definition and underlying physical intuition"
            })

        # 2. Mathematical Formulation / Derivation
        if TopicType.DERIVATION_HEAVY in lbl_set or TopicType.MATHEMATICAL in lbl_set:
            sections.append({
                "title": f"Mathematical Formulation and Governing Equations of {topic_title}",
                "pedagogy": "Differential equations, operators, and coordinate assumptions"
            })
            sections.append({
                "title": f"Analytical Derivation and Boundary Conditions for {topic_title}",
                "pedagogy": "Step-by-step rigorous proof leading to closed-form solution"
            })
            sections.append({
                "title": f"Physical Interpretation of Solutions and Eigenstates in {topic_title}",
                "pedagogy": "Significance of eigenvalues, quantization, and probability profiles"
            })
        elif TopicType.LAW_OR_PRINCIPLE in lbl_set:
            sections.append({
                "title": f"Mathematical Expression and Governing Relations of {topic_title}",
                "pedagogy": "Formal statement of equation with full symbol definitions"
            })

        # 3. Experimental Evidence / Apparatus
        if TopicType.EXPERIMENTAL in lbl_set or TopicType.APPARATUS in lbl_set or TopicType.LAW_OR_PRINCIPLE in lbl_set:
            sections.append({
                "title": f"Experimental Verification and Laboratory Evidence for {topic_title}",
                "pedagogy": "Key historical experiments and measured confirmation"
            })

        # 4. Modern Applications
        if TopicType.APPLICATION in lbl_set or not any(s["title"].startswith("Experimental") for s in sections):
            sections.append({
                "title": f"Contemporary Engineering and Technological Applications of {topic_title}",
                "pedagogy": "Practical devices, instrumentation, and industrial relevance"
            })

        # 5. Limitations / Validity
        sections.append({
            "title": f"Physical Limitations, Assumptions, and Boundary Scope of {topic_title}",
            "pedagogy": "Domain of applicability, non-relativistic limits, and failure modes"
        })

        # 6. Numericals if enabled
        if TopicType.NUMERICAL in lbl_set:
            sections.append({
                "title": f"Worked Numerical Examples on {topic_title}",
                "pedagogy": "Step-by-step problem solving with given, formula, and units"
            })

        return sections
