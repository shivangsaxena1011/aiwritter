from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class GraphNode:
    node_id: str
    node_type: str  # Chapter, Topic, Subtopic, Concept, Equation, Definition, Experiment, Application, Example, Diagram, Source, Terminology
    name: str
    topic_id: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    relation: str  # PREREQUISITE_OF, EXPLAINS, DERIVES, APPLIES, EXTENDS, CONTRASTS, REFERENCES, ILLUSTRATES
    data: Dict[str, Any] = field(default_factory=dict)


class BookKnowledgeGraph:
    """Directed Knowledge Graph tracking pedagogical structure, concept ownership, and dependency order."""

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []
        self._introduced_concepts: Dict[str, str] = {}  # concept_name -> topic_id
        self._derived_equations: Dict[str, str] = {}    # equation_name -> topic_id
        self._established_experiments: Dict[str, str] = {}  # experiment_name -> topic_id
        self._established_terms: Dict[str, str] = {}    # term_name -> topic_id

    def add_node(self, node_id: str, node_type: str, name: str, topic_id: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> GraphNode:
        node = GraphNode(node_id=node_id, node_type=node_type, name=name, topic_id=topic_id, data=data or {})
        self.nodes[node_id] = node
        return node

    def add_edge(self, source_id: str, target_id: str, relation: str, data: Optional[Dict[str, Any]] = None):
        self.edges.append(GraphEdge(source_id=source_id, target_id=target_id, relation=relation, data=data or {}))

    def is_concept_introduced(self, concept_name: str) -> bool:
        c_clean = concept_name.lower().strip()
        return c_clean in self._introduced_concepts

    def get_concept_owner(self, concept_name: str) -> Optional[str]:
        return self._introduced_concepts.get(concept_name.lower().strip())

    def record_concept_introduction(self, concept_name: str, topic_id: str):
        c_clean = concept_name.lower().strip()
        if c_clean not in self._introduced_concepts:
            self._introduced_concepts[c_clean] = topic_id

    def is_equation_derived(self, equation_name: str) -> bool:
        e_clean = equation_name.lower().strip()
        return e_clean in self._derived_equations

    def get_equation_owner(self, equation_name: str) -> Optional[str]:
        return self._derived_equations.get(equation_name.lower().strip())

    def record_equation_derivation(self, equation_name: str, topic_id: str):
        e_clean = equation_name.lower().strip()
        if e_clean not in self._derived_equations:
            self._derived_equations[e_clean] = topic_id

    def is_experiment_established(self, experiment_name: str) -> bool:
        exp_clean = experiment_name.lower().strip()
        return exp_clean in self._established_experiments

    def record_experiment_established(self, experiment_name: str, topic_id: str):
        exp_clean = experiment_name.lower().strip()
        if exp_clean not in self._established_experiments:
            self._established_experiments[exp_clean] = topic_id

    def get_context_delta(self, topic_id: str, required_concepts: List[str], required_equations: List[str]) -> Dict[str, Any]:
        """Calculates what has already been introduced vs what is genuinely new for this topic."""
        already_covered_concepts = [c for c in required_concepts if self.is_concept_introduced(c)]
        new_concepts = [c for c in required_concepts if not self.is_concept_introduced(c)]
        already_derived_equations = [e for e in required_equations if self.is_equation_derived(e)]
        new_equations_to_derive = [e for e in required_equations if not self.is_equation_derived(e)]

        return {
            "already_covered_concepts": already_covered_concepts,
            "new_concepts": new_concepts,
            "already_derived_equations": already_derived_equations,
            "new_equations_to_derive": new_equations_to_derive,
            "total_introduced_so_far": len(self._introduced_concepts)
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "introduced_concepts_count": len(self._introduced_concepts),
            "derived_equations_count": len(self._derived_equations),
            "established_experiments_count": len(self._established_experiments)
        }
