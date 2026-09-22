import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Integer, Float, Text, Boolean, DateTime, ForeignKey, JSON, Index
)
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active", index=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="projects")
    books = relationship("Book", back_populates="project", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=True)
    author = Column(String(255), default="AI Academic Press")
    academic_level = Column(String(50), default="University / Reference")
    target_audience = Column(String(100), default="Undergraduate & Graduate")
    status = Column(String(50), default="draft", index=True)
    language = Column(String(20), default="en")
    book_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    project = relationship("Project", back_populates="books")
    units = relationship("BookUnit", back_populates="book", cascade="all, delete-orphan", order_by="BookUnit.position")
    jobs = relationship("GenerationJob", back_populates="book", cascade="all, delete-orphan")
    assets = relationship("GeneratedAsset", back_populates="book", cascade="all, delete-orphan")
    sections = relationship("GeneratedSection", back_populates="book", cascade="all, delete-orphan")

class BookUnit(Base):
    __tablename__ = "book_units"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False, index=True)
    position = Column(Integer, nullable=False, default=1)
    title = Column(String(255), nullable=False)

    book = relationship("Book", back_populates="units")
    topics = relationship("BookTopic", back_populates="unit", cascade="all, delete-orphan", order_by="BookTopic.position")

class BookTopic(Base):
    __tablename__ = "book_topics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    unit_id = Column(String(36), ForeignKey("book_units.id"), nullable=False, index=True)
    position = Column(Integer, nullable=False, default=1)
    title = Column(String(255), nullable=False)

    unit = relationship("BookUnit", back_populates="topics")
    subtopics = relationship("BookSubtopic", back_populates="topic", cascade="all, delete-orphan", order_by="BookSubtopic.position")

class BookSubtopic(Base):
    __tablename__ = "book_subtopics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    topic_id = Column(String(36), ForeignKey("book_topics.id"), nullable=False, index=True)
    position = Column(Integer, nullable=False, default=1)
    title = Column(String(255), nullable=False)
    status = Column(String(50), default="pending", index=True)

    topic = relationship("BookTopic", back_populates="subtopics")

class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False, index=True)
    status = Column(String(50), default="CREATED", index=True)  # CREATED, QUEUED, PLANNING, GENERATING, REVIEWING, FORMATTING, EXPORTING, COMPLETED, FAILED, CANCELLED, RETRYING
    progress = Column(Float, default=0.0)
    current_stage = Column(String(100), default="Initialization")
    current_item = Column(String(255), nullable=True)
    error = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    book = relationship("Book", back_populates="jobs")
    events = relationship("GenerationEvent", back_populates="job", cascade="all, delete-orphan", order_by="GenerationEvent.created_at")

class GenerationEvent(Base):
    __tablename__ = "generation_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    job_id = Column(String(36), ForeignKey("generation_jobs.id"), nullable=False, index=True)
    event_type = Column(String(50), default="log", index=True)  # log, progress, stage, warning, error, complete
    message = Column(Text, nullable=False)
    progress = Column(Float, nullable=True)
    event_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, index=True)

    job = relationship("GenerationJob", back_populates="events")

class GeneratedAsset(Base):
    __tablename__ = "generated_assets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False, index=True)
    job_id = Column(String(36), ForeignKey("generation_jobs.id"), nullable=True, index=True)
    type = Column(String(50), nullable=False)  # docx, pdf, image_png, diagram_svg
    storage_key = Column(String(512), nullable=False)
    url = Column(String(1024), nullable=True)
    asset_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    book = relationship("Book", back_populates="assets")

class GeneratedSection(Base):
    __tablename__ = "generated_sections"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    book_id = Column(String(36), ForeignKey("books.id"), nullable=False, index=True)
    unit_id = Column(String(36), ForeignKey("book_units.id"), nullable=True)
    topic_id = Column(String(36), ForeignKey("book_topics.id"), nullable=True)
    subtopic_id = Column(String(36), ForeignKey("book_subtopics.id"), nullable=True)
    content = Column(Text, nullable=False)
    status = Column(String(50), default="generated", index=True)  # generated, reviewed, formatted
    word_count = Column(Integer, default=0)
    review_status = Column(String(50), default="pending")
    quality_score = Column(Float, default=0.0)
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    book = relationship("Book", back_populates="sections")

Index("idx_sections_book_subtopic", GeneratedSection.book_id, GeneratedSection.subtopic_id)
