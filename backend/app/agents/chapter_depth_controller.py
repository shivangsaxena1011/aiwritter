from typing import Dict, Any

class ChapterDepthController:
    """Controls section length, target words, and model token budgets."""

    DEPTH_PROFILES: Dict[str, Dict[str, Any]] = {
        "Concise": {
            "target_words": 750,
            "min_words": 500,
            "max_words": 1000,
            "max_tokens": 4000,
            "instruction": "Provide a high-density, focused synthesis suitable for quick reference or survey review."
        },
        "Standard": {
            "target_words": 1500,
            "min_words": 1000,
            "max_words": 2000,
            "max_tokens": 6000,
            "instruction": "Provide balanced academic coverage with core theory, basic derivations, and foundational examples."
        },
        "Detailed": {
            "target_words": 2800,
            "min_words": 2000,
            "max_words": 3500,
            "max_tokens": 10000,
            "instruction": "Provide comprehensive university-level coverage with in-depth derivations, worked numerical examples, and comparison tables."
        },
        "Deep Academic": {
            "target_words": 4200,
            "min_words": 3500,
            "max_words": 5000,
            "max_tokens": 14000,
            "instruction": "Deliver exhaustive graduate-level treatment with historical depth, mathematical proofs, industrial case studies, and advanced review questions."
        },
        "Reference": {
            "target_words": 5500,
            "min_words": 5000,
            "max_words": 7500,
            "max_tokens": 16000,
            "instruction": "Deliver an authoritative, encyclopedic reference chapter with exhaustive analysis, comprehensive taxonomies, and multi-step empirical derivations."
        }
    }

    @classmethod
    def get_profile(cls, depth_level: str) -> Dict[str, Any]:
        return cls.DEPTH_PROFILES.get(depth_level, cls.DEPTH_PROFILES["Detailed"])
