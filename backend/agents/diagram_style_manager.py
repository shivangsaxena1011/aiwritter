import logging

logger = logging.getLogger(__name__)

class DiagramStyleManager:
    """Centralized manager for standardized, publication-quality academic diagram prompts."""
    
    CATEGORIES = {
        "architecture": ["architecture", "system", "component", "layer", "module", "stack", "structure"],
        "flowchart": ["flow", "process", "workflow", "decision", "step", "algorithm"],
        "hierarchy": ["hierarchy", "tree", "taxonomy", "class", "inheritance", "organization"],
        "cyclic": ["cycle", "loop", "lifecycle", "feedback", "recurring", "phase"],
        "conceptual": ["concept", "framework", "model", "relationship", "overview"]
    }

    def classify_topic(self, topic: str) -> str:
        topic_lower = topic.lower()
        for cat, keywords in self.CATEGORIES.items():
            if any(kw in topic_lower for kw in keywords):
                return cat
        return "conceptual"

    def get_enhanced_prompt(self, topic: str) -> str:
        category = self.classify_topic(topic)
        base = f"Clean, high-resolution vector visual diagram representing '{topic}'. "
        style_rules = (
            "White background, publication textbook quality, crisp typography, "
            "modern sleek aesthetic, no background noise, professional engineering schematic."
        )

        cat_prompts = {
            "architecture": "Structured block diagram with labeled modular components, clear borders, and directional arrows.",
            "flowchart": "Clear flowchart with start/end nodes, decision diamonds, process boxes, and aligned connector arrows.",
            "hierarchy": "Tree structure diagram with clear parent-child nodes and clean connection lines.",
            "cyclic": "Circular process diagram with numbered sequential phases and smooth clockwise arrows.",
            "conceptual": "Infographic conceptual framework showing key elements and labeled relationships."
        }

        return f"{base} {cat_prompts.get(category, cat_prompts['conceptual'])} {style_rules}"
