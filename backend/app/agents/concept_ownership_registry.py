from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConceptRecord:
    concept_id: str
    name: str
    primary_topic: str
    secondary_topics: List[str] = field(default_factory=list)
    canonical_explanation: str = ""
    canonical_equation: str = ""
    allowed_reuse_mode: str = "SUMMARY"  # FULL (only in primary_topic), SUMMARY, REFERENCE, EQUATION_ONLY, NONE


@dataclass
class EquationRecord:
    equation_id: str
    name: str
    latex: str
    primary_topic: str
    derivation_owner_topic: str
    symbols: Dict[str, str] = field(default_factory=dict)
    canonical_status: str = "canonical"


class ConceptOwnershipRegistry:
    """Enforces strict ownership for each major concept and prevents full regeneration in secondary topics."""

    def __init__(self):
        self.concepts: Dict[str, ConceptRecord] = {}
        self.equations: Dict[str, EquationRecord] = {}
        self._concept_usage_counts: Dict[str, Dict[str, int]] = {}  # concept_name -> {topic: count}

    def register_concept(
        self,
        concept_id: str,
        name: str,
        primary_topic: str,
        secondary_topics: Optional[List[str]] = None,
        canonical_explanation: str = "",
        canonical_equation: str = "",
        allowed_reuse_mode: str = "SUMMARY"
    ) -> ConceptRecord:
        record = ConceptRecord(
            concept_id=concept_id,
            name=name,
            primary_topic=primary_topic,
            secondary_topics=secondary_topics or [],
            canonical_explanation=canonical_explanation,
            canonical_equation=canonical_equation,
            allowed_reuse_mode=allowed_reuse_mode
        )
        self.concepts[name.lower().strip()] = record
        return record

    def register_equation(
        self,
        equation_id: str,
        name: str,
        latex: str,
        primary_topic: str,
        derivation_owner_topic: str,
        symbols: Optional[Dict[str, str]] = None
    ) -> EquationRecord:
        record = EquationRecord(
            equation_id=equation_id,
            name=name,
            latex=latex,
            primary_topic=primary_topic,
            derivation_owner_topic=derivation_owner_topic,
            symbols=symbols or {}
        )
        self.equations[name.lower().strip()] = record
        return record

    def get_concept_policy(self, concept_name: str, current_topic: str) -> Dict[str, Any]:
        """Returns the permitted explanation mode for this concept in the current topic."""
        c_clean = concept_name.lower().strip()
        rec = self.concepts.get(c_clean)
        if not rec:
            return {"mode": "FULL", "is_owner": True, "record": None}

        is_owner = (rec.primary_topic.lower().strip() == current_topic.lower().strip())
        if is_owner:
            return {"mode": "FULL", "is_owner": True, "record": rec}
        else:
            return {"mode": rec.allowed_reuse_mode, "is_owner": False, "record": rec}

    def can_derive_equation(self, equation_name: str, current_topic: str) -> bool:
        """Derivations are strictly permitted only in the derivation owner topic."""
        e_clean = equation_name.lower().strip()
        rec = self.equations.get(e_clean)
        if not rec:
            return True
        return rec.derivation_owner_topic.lower().strip() == current_topic.lower().strip()

    def record_usage(self, concept_name: str, topic: str):
        c_clean = concept_name.lower().strip()
        if c_clean not in self._concept_usage_counts:
            self._concept_usage_counts[c_clean] = {}
        self._concept_usage_counts[c_clean][topic] = self._concept_usage_counts[c_clean].get(topic, 0) + 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_registered_concepts": len(self.concepts),
            "total_registered_equations": len(self.equations),
            "concepts": {k: {"primary_owner": v.primary_topic, "reuse_mode": v.allowed_reuse_mode} for k, v in self.concepts.items()}
        }


class ExampleRegistry:
    """Tracks worked examples and numerical parameters to prevent repetitive parameter reuse."""

    def __init__(self):
        self.registered_examples: List[Dict[str, Any]] = []

    def register_example(self, topic: str, example_type: str, parameters: Dict[str, Any], description: str):
        self.registered_examples.append({
            "topic": topic,
            "example_type": example_type,
            "parameters": parameters,
            "description": description
        })

    def is_similar_example_used(self, example_type: str, parameters: Dict[str, Any]) -> bool:
        for ex in self.registered_examples:
            if ex["example_type"] == example_type:
                # check overlap of parameter values
                overlap = sum(1 for k, v in parameters.items() if ex["parameters"].get(k) == v)
                if overlap >= 2:
                    return True
        return False


class AnalogyRegistry:
    """Tracks conceptual analogies to prevent spreading generic analogies throughout the book."""

    def __init__(self, max_reuse: int = 1):
        self.analogies: Dict[str, int] = {}
        self.max_reuse = max_reuse

    def register_analogy(self, analogy_key: str, topic: str) -> bool:
        """Returns True if analogy can be used, False if it exceeds max_reuse."""
        k_clean = analogy_key.lower().strip()
        count = self.analogies.get(k_clean, 0)
        if count >= self.max_reuse:
            return False
        self.analogies[k_clean] = count + 1
        return True
