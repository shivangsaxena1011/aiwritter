from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend.app.core.database import get_db
from backend.app.models import Book, BookUnit, BookTopic, BookSubtopic
from backend.app.schemas import (
    CreateBookRequest, ParseSyllabusRequest, ParseSyllabusResponse,
    EstimationResponse, TableOfContentsSchema
)
from backend.app.services.ai import get_ai_provider
from backend.app.agents.toc_planner import TOCPlanner
from backend.app.agents.chapter_depth_controller import ChapterDepthController

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/parse-syllabus", response_model=ParseSyllabusResponse)
async def parse_syllabus(req: ParseSyllabusRequest):
    """Parses raw text, outline, or markdown into structured Table of Contents."""
    ai_provider = get_ai_provider(api_key=req.api_key)
    planner = TOCPlanner(ai_provider)
    result = await planner.plan_toc(raw_syllabus=req.text)
    return result

@router.post("/estimate", response_model=EstimationResponse)
def estimate_book_metrics(req: CreateBookRequest):
    """Calculates pre-generation estimates for words, pages, and duration."""
    total_units = len(req.toc.units)
    total_topics = sum(len(u.topics) for u in req.toc.units)
    total_subtopics = sum(len(t.subtopics) for u in req.toc.units for t in u.topics)

    profile = ChapterDepthController.get_profile(req.writing_depth or "Detailed")
    target_words_per_section = profile["target_words"]

    estimated_words = (total_subtopics * target_words_per_section) + (total_units * 800)
    estimated_pages = max(10, estimated_words // 380)
    estimated_ai_requests = total_subtopics + total_units + 5
    estimated_image_requests = total_subtopics if req.generate_images else 0
    estimated_minutes = max(2, (total_subtopics * 15) // 60)

    return {
        "total_units": total_units,
        "total_topics": total_topics,
        "total_subtopics": total_subtopics,
        "estimated_words": estimated_words,
        "estimated_pages": estimated_pages,
        "estimated_ai_requests": estimated_ai_requests,
        "estimated_image_requests": estimated_image_requests,
        "estimated_minutes": estimated_minutes
    }

@router.post("", status_code=201)
def create_book(req: CreateBookRequest, db: Session = Depends(get_db)):
    """Saves book definition and full Table of Contents hierarchy to database."""
    book = Book(
        title=req.title.strip(),
        subtitle=req.subtitle.strip() if req.subtitle else None,
        author=req.author or "AI Academic Press",
        academic_level=req.academic_level or "University / Reference",
        target_audience=req.target_audience or "Undergraduate & Graduate",
        language=req.language or "en",
        book_metadata={
            "writing_depth": req.writing_depth or "Detailed",
            "citation_style": req.citation_style or "IEEE",
            "generate_images": req.generate_images
        }
    )
    db.add(book)
    db.flush()

    for u_idx, u in enumerate(req.toc.units, start=1):
        unit = BookUnit(book_id=book.id, position=u_idx, title=u.name)
        db.add(unit)
        db.flush()

        for t_idx, t in enumerate(u.topics, start=1):
            topic = BookTopic(unit_id=unit.id, position=t_idx, title=t.name)
            db.add(topic)
            db.flush()

            for s_idx, s in enumerate(t.subtopics, start=1):
                subtopic = BookSubtopic(topic_id=topic.id, position=s_idx, title=s)
                db.add(subtopic)

    db.commit()
    db.refresh(book)

    return {
        "id": book.id,
        "title": book.title,
        "status": book.status,
        "created_at": book.created_at
    }

@router.get("/{book_id}")
def get_book(book_id: str, db: Session = Depends(get_db)):
    """Fetches book metadata and structured Table of Contents."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    units = []
    for u in book.units:
        topics = []
        for t in u.topics:
            topics.append({
                "id": t.id,
                "name": t.title,
                "subtopics": [s.title for s in t.subtopics]
            })
        units.append({
            "id": u.id,
            "name": u.title,
            "topics": topics
        })

    return {
        "id": book.id,
        "title": book.title,
        "subtitle": book.subtitle,
        "author": book.author,
        "academic_level": book.academic_level,
        "target_audience": book.target_audience,
        "status": book.status,
        "metadata": book.book_metadata,
        "units": units
    }
