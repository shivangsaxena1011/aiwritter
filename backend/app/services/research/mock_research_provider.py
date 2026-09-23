"""
MockResearchProvider for offline testing and deterministic evaluation.
"""

from datetime import datetime, timezone
from backend.app.services.research.base import ResearchProvider, ResearchResult, ResearchSourceData

class MockResearchProvider(ResearchProvider):
    async def conduct_research(
        self,
        topic: str,
        subject: str,
        depth: str = "Standard"
    ) -> ResearchResult:
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return ResearchResult(
            topic=topic,
            sources=[
                ResearchSourceData(
                    title=f"Academic Principles of {subject}: {topic}",
                    url="https://academic.example.edu/treatise",
                    author="Prof. A. Scholar",
                    publisher="University Press",
                    publication_date="2023",
                    accessed_date=now_str,
                    source_type="university",
                    relevance="Foundational reference",
                    key_points=[
                        f"Theoretical principles governing {topic}.",
                        "Standard notation and mathematical representations."
                    ]
                )
            ],
            research_notes=[
                f"Grounding notes for {topic}: emphasize rigorous analytical foundations.",
                "Original academic synthesis without verbatim duplication."
            ],
            originality_guidelines=[
                "Maintain complete academic originality.",
                "Independent step-by-step mathematical reasoning."
            ],
            status="success"
        )
