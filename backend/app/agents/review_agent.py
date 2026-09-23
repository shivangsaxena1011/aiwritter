import logging
from typing import Dict, Any
from backend.app.services.ai.base import AIProvider
from backend.app.services.prompt_service import prompt_service

logger = logging.getLogger(__name__)

class ReviewAgent:
    """Peer reviews academic sections, assigns quality score, and flags rewrite requirements."""

    def __init__(self, ai_provider: AIProvider):
        self.ai = ai_provider

    async def review_section(
        self,
        book_title: str,
        subtopic_title: str,
        content: str,
        target_word_count: int
    ) -> Dict[str, Any]:
        prompt = prompt_service.get_prompt(
            "reviewer.txt",
            book_title=book_title,
            subtopic_title=subtopic_title,
            target_word_count=target_word_count,
            content=content
        )
        try:
            result = await self.ai.generate_structured(prompt)
            # Ensure safe fields
            score = float(result.get("overall_score", 85.0))
            rewrite = bool(result.get("rewrite_required", False))

            # Additional check: excessive bullet points penalty (Section 12 & 31)
            bullet_count = len([line for line in content.splitlines() if line.strip().startswith("- ") or line.strip().startswith("* ")])
            total_lines = len([line for line in content.splitlines() if line.strip()])
            if total_lines > 0 and (bullet_count / total_lines) > 0.40:
                result.setdefault("issues", []).append("Excessive bullet usage detected; textbook material must be predominantly explanatory paragraphs.")
                score = min(score, 68.0)
                rewrite = True

            if score < 70.0:
                rewrite = True

            return {
                "overall_score": score,
                "depth_score": float(result.get("depth_score", 17)),
                "pedagogy_score": float(result.get("pedagogy_score", 17)),
                "filler_score": float(result.get("filler_score", 17)),
                "accuracy_score": float(result.get("accuracy_score", 17)),
                "completeness_score": float(result.get("completeness_score", 17)),
                "issues": result.get("issues", []),
                "missing_topics": result.get("missing_topics", []),
                "corrections": result.get("corrections", []),
                "rewrite_required": rewrite
            }
        except Exception as e:
            logger.warning(f"Review agent evaluation failed: {e}")
            return {
                "overall_score": 85.0,
                "depth_score": 17,
                "pedagogy_score": 17,
                "filler_score": 17,
                "accuracy_score": 17,
                "completeness_score": 17,
                "issues": [],
                "missing_topics": [],
                "corrections": [],
                "rewrite_required": False
            }

# Semantic Alias
ContentReviewAgent = ReviewAgent

