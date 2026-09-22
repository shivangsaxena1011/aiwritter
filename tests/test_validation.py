import pytest
from pydantic import ValidationError
from backend.app.schemas import (
    CreateBookRequest, TableOfContentsSchema, UnitSchema, TopicSchema,
    EstimationResponse
)
from backend.app.agents.chapter_depth_controller import ChapterDepthController

def test_valid_toc_schema():
    toc = TableOfContentsSchema(
        units=[
            UnitSchema(
                name="Unit 1: Fundamentals",
                topics=[
                    TopicSchema(
                        name="Core Theory",
                        subtopics=["Subtopic 1", "Subtopic 2"]
                    )
                ]
            )
        ]
    )
    assert len(toc.units) == 1
    assert toc.units[0].topics[0].subtopics == ["Subtopic 1", "Subtopic 2"]

def test_create_book_request_validation():
    toc = TableOfContentsSchema(
        units=[
            UnitSchema(
                name="Unit 1",
                topics=[
                    TopicSchema(name="Topic 1", subtopics=["Subtopic 1"])
                ]
            )
        ]
    )
    req = CreateBookRequest(
        title="Valid Textbook Title",
        academic_level="Graduate",
        writing_depth="Detailed",
        toc=toc
    )
    assert req.title == "Valid Textbook Title"
    assert req.writing_depth == "Detailed"

def test_create_book_missing_title_raises():
    with pytest.raises(ValidationError):
        CreateBookRequest(
            title="",  # missing/empty
            toc=TableOfContentsSchema(units=[])
        )

def test_chapter_depth_controller_tiers():
    profiles = ["Concise", "Standard", "Detailed", "Deep Academic", "Reference"]
    for tier in profiles:
        p = ChapterDepthController.get_profile(tier)
        assert p is not None
        assert "target_words" in p
        assert p["target_words"] >= 500
        assert "min_words" in p
        assert "max_tokens" in p
        assert "instruction" in p

def test_chapter_depth_fallback():
    p = ChapterDepthController.get_profile("NonExistentTier")
    assert p["target_words"] == 2800  # Default to Detailed (2800 words)
