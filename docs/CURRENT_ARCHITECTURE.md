# Current Architecture Audit — AI Book Writer (Pre-Migration)

## 1. Executive Summary

This document captures the state of the codebase prior to the architectural transformation into **AIWritter — Agentic Academic Book Publishing Engine**.

The current project is an academic textbook publishing prototype featuring a FastAPI backend, an SQLite/SQLAlchemy ORM layer, a preliminary multi-agent workflow (TOC planner, context manager, depth controller, content writer, diagram system, review agent, consistency auditor, quality controller), an in-memory/DB job queue, an initial `python-docx` export engine, and a dark glassmorphism vanilla JavaScript single-page application.

---

## 2. Frontend Architecture & State Management

### Tech Stack
- Vanilla HTML5, CSS3 (custom custom properties, CSS Grid/Flexbox, glassmorphic styling), and ES6+ JavaScript.
- No heavy frontend framework (React/Vue/Angular), reducing build complexity and bundle size.
- Font Awesome 6.4.0 (CDN) and Google Fonts (`Inter`, `JetBrains Mono`, `Outfit`).

### Key Files
- `frontend/index.html`: Multi-section single page interface containing 3 navigation steps:
  1. **Book Setup**: Metadata form (Title, Subtitle, Author, Academic Level, Writing Depth, Citation Style, API Key toggle, Diagram generation toggle), live estimation card, raw syllabus input, interactive Table of Contents tree editor (with unit/topic/subtopic add/delete/rename).
  2. **Generation**: Real-time progress bar, visual 6-stage multi-agent flow diagram, task status indicator, cancel/retry controls, and agent execution console log.
  3. **Review & Export**: Peer review quality scorecard (Academic Rigor, Completeness, Consistency, Pedagogy), stats summary, and direct `.docx` download action.
- `frontend/api.js`: Centralized REST API client (`ApiClient`) communicating with `/api/v1/` endpoints and legacy routes.
- `frontend/app.js`: State manager handling DOM events, syllabus parsing dispatch, local state syncing, dynamic Table of Contents tree rendering, live page/word count estimation, Server-Sent Events (SSE) stream subscription, and scorecard rendering.
- `frontend/style.css`: 1,200+ lines of dark-mode UI styles, CSS variables, interactive widgets, responsive layouts, and animations.

### State Management & SSE Implementation
- **Local State**: Managed in an in-memory JavaScript object with `localStorage` draft saving (`autosave-status`).
- **Live Event Streaming**: Connects via HTML5 `EventSource` to `/api/v1/jobs/{jobId}/stream`. Reconnection logic falls back to interval polling (`/api/v1/jobs/{jobId}/events?after=...`) if SSE connection disconnects or errors.

---

## 3. Backend Architecture & API Routes

### Tech Stack
- **FastAPI / Starlette**: Async ASGI web framework.
- **SQLAlchemy 2.0**: Relational ORM with connection pooling.
- **SQLite / PostgreSQL**: SQLite (`sqlite:///./app.db`) used for local development, configured for PostgreSQL in production via `DATABASE_URL`.
- **Pydantic v2**: Request/response schema validation and settings management (`pydantic-settings`).
- **python-docx**: Office Open XML document builder.
- **Matplotlib & Pillow**: Programmatic charts and image raster manipulation.
- **Google GenAI SDK (`google-genai>=1.0.0`)**: Gemini 2.5 Flash and Imagen 3 client.

### Directory Structure
```
backend/
├── agents/             # Legacy stubs (to be cleaned / redirected)
└── app/
    ├── api/v1/
    │   ├── books.py    # Book creation, TOC syllabus parsing, estimation, quality report
    │   ├── files.py    # Secure static file serving and download
    │   ├── jobs.py     # Job queue lifecycle, SSE streaming, cancellation, retry
    │   └── router.py   # API v1 router aggregator
    ├── core/
    │   ├── config.py   # Environment settings via Pydantic
    │   ├── database.py # SQLAlchemy engine, session maker, base model
    │   └── security.py # Path traversal protection, sanitize inputs, secret masking
    ├── models/
    │   └── __init__.py # SQLAlchemy models (User, Project, Book, BookUnit, BookTopic, BookSubtopic, GenerationJob, GenerationEvent, GeneratedAsset, GeneratedSection)
    ├── schemas/
    │   └── __init__.py # Pydantic schemas for request/response serialization
    ├── services/
    │   ├── ai/         # AI providers: base.py, factory.py, gemini_provider.py, mock_provider.py
    │   ├── document/   # Document builders: base.py, docx_engine.py, pdf_engine.py
    │   └── prompt_service.py # Template loader for text prompts
    ├── storage/        # Storage providers: base.py, factory.py, local.py (S3 placeholder)
    └── workers/        # Pipeline orchestration: pipeline.py, queue_manager.py
```

### Existing API Routes
- `POST /api/v1/books/parse-syllabus`: Parses raw syllabus into structured units/topics/subtopics.
- `POST /api/v1/books/estimate`: Pre-generation calculation of words, pages, duration, and AI requests.
- `POST /api/v1/books`: Creates book record and persists normalized TOC hierarchy.
- `GET  /api/v1/books/{book_id}`: Retrieves book metadata and TOC tree.
- `GET  /api/v1/books/{book_id}/quality-report`: Computes academic audit metrics.
- `POST /api/v1/jobs`: Enqueues an asynchronous generation job.
- `GET  /api/v1/jobs/{job_id}`: Retrieves job progress and status.
- `GET  /api/v1/jobs/{job_id}/stream`: SSE endpoint streaming real-time events.
- `POST /api/v1/jobs/{job_id}/cancel`: Sets job status to CANCELLED.
- `POST /api/v1/jobs/{job_id}/retry`: Resumes interrupted job from checkpoints.
- `GET  /api/v1/jobs/{job_id}/events`: Retrieves event log history.
- `GET  /api/v1/files/{filename}`: Securely downloads generated DOCX and diagram assets.
- Legacy backward-compatible endpoints:
  - `POST /api/generate`
  - `POST /api/parse-syllabus`
  - `GET  /api/stream/{task_id}`
  - `GET  /api/download/{filename}`

---

## 4. Current Agents & Pipelines

### Current Agents
1. **`TOCPlanner` (`backend/app/agents/toc_planner.py`)**:
   - Parses unstructured syllabus text using AI structured output or deterministic regex rules.
   - Normalizes units, topics, and subtopics with numerical prefixes (`Unit 1: ...`, `1.1 ...`, `1.1.1 ...`).
2. **`BookContextManager` (`backend/app/agents/book_context_manager.py`)**:
   - Tracks cross-chapter narrative memory, terminology glossary, and mathematical notation.
   - Maintains rolling chapter and topic summaries to prevent introductory redundancy.
3. **`ChapterDepthController` (`backend/app/agents/chapter_depth_controller.py`)**:
   - Maps writing depth profiles (`Concise`, `Standard`, `Detailed`, `Deep Academic`, `Reference`) to token budgets and target word counts.
4. **`ContentWriter` (`backend/app/agents/content_writer.py`)**:
   - Writes unit overviews and subtopic sections based on prompt templates.
5. **`DiagramPlanner` & `DiagramGenerator` (`backend/app/agents/diagram_system.py`)**:
   - Evaluates whether a section requires a diagram (`needs_diagram: bool`).
   - Supports Matplotlib 2D scientific plots, AI illustrations via Imagen 3 (`imagen-3.0-generate-002`), and formatted text fallback placeholders.
6. **`ReviewAgent` (`backend/app/agents/review_agent.py`)**:
   - Reviews generated text against academic criteria and determines if a rewrite is needed.
7. **`ConsistencyAuditor` (`backend/app/agents/consistency_auditor.py`)**:
   - Audits terminology and symbol usage across sections.
8. **`QualityController` (`backend/app/agents/quality_controller.py`)**:
   - Computes weighted publication quality metrics.

### Generation Pipeline
- Coordinated in `backend/app/workers/pipeline.py` via `BookGenerationPipeline.execute()`.
- Iterates synchronously over Units -> Topics -> Subtopics.
- Writes overview -> writes subtopic -> reviews -> consistency audit -> optional diagram -> persists `GeneratedSection` in SQLite/Postgres.
- Compiles sections into DOCX and finishes job.

---

## 5. Current DOCX Exporter & Template Integration

### Template System
- Base template: `templates/master_book_template.docx` (36 KB).
- Loaded by `backend/app/services/document/docx_engine.py` via `python-docx`.
- Configures margins (1.0 inch all around), default styles (Times New Roman, 11pt, dark slate color).

### Document Assembly
- Cover Page: Academic Series tag, Book Title, Subtitle, Author, Date, Page Break.
- Front Matter: Preface and Table of Contents (indented text hierarchy).
- Body Content: Markdown parsing into headings, paragraphs, bullet lists, numbered lists, code blocks, real Word tables (`add_table` with XML shading), centered figures with italicized captions, and basic `$$ ... $$` math formatting into Cambria Math runs.
- Back Matter: Academic quality scorecard table.
- Dynamic page numbering injected into footers using Word XML field `w:fldSimple` with `w:instr="PAGE"`.

---

## 6. Testing Baseline

- Pytest test suite (`tests/`):
  - `test_api.py`: 5 tests
  - `test_content_pipeline.py`: 4 tests
  - `test_docx_exporter.py`: 1 test
  - `test_file_security.py`: 4 tests
  - `test_job_state.py`: 1 test
  - `test_toc_parser.py`: 4 tests
  - `test_validation.py`: 5 tests
  - **Total**: 24 tests, 100% passing baseline in 4.03s.

---

## 7. Identified Technical Debt & Gaps vs. Target Specification

1. **Missing Specialized Agent Decomposition**:
   - No dedicated `SyllabusAnalysisAgent` with topic classification (prerequisites, required derivations, required numericals, diagrams).
   - No `TopicDecompositionAgent` with subject-specific breakdown (Physics vs. Engineering vs. Mathematics vs. Computer Science).
   - No `ResearchAgent` / `WebResearchProvider` for educational research grounding, source tracking, and originality auditing.
   - No dedicated `DerivationAgent` for step-by-step mathematical derivations.
   - No dedicated equation engine converting LaTeX/MathML into real Office Math Markup Language (OMML) equations.
   - No configurable numerical problem engine (Given, Formula, Substitution, Calculation, Answer, Unit) controlled by user settings.
   - No configurable Q&A or example switches.
   - No `DiagramPromptAgent` generating structured black-and-white academic diagram prompts.
   - No `FactCheckAgent` cross-referencing research sources.
   - No `DocumentStructureAgent`, `DocumentFormattingAgent`, or `DocumentValidationAgent` generating programmatic `document_quality_report.json` and `syllabus_coverage_report.json`.

2. **Typography & Formatting Rules**:
   - Body font in `docx_engine.py` is currently set to 11 pt with 1.15 line spacing, instead of the mandated **Times New Roman, 12 pt, 1.5 line spacing, Justified paragraph alignment**.
   - Equations are styled as plain italic text instead of proper centered OMML equations with Greek symbols and native fraction representations.

3. **Database Schema Enhancements**:
   - Missing tables/models for `ResearchSource`, `ReviewResult`, `DocumentExport`, and granular generation settings (numerical toggle, research depth, Q&A toggle, example toggle).

4. **Worker & Resilience**:
   - `BookGenerationPipeline` needs integration with the full multi-agent orchestrator (`BookGenerationOrchestrator`) supporting parallel safe execution, failure resilience per topic without failing the entire book, and full event replay.

---

## 8. Target Migration Plan

- **Phase 1**: Architecture audit & documentation (completed by this document).
- **Phase 2**: Core Data Models & Database Migrations (add `ResearchSource`, `ReviewResult`, `DocumentExport`, configuration options).
- **Phase 3**: Agent Contracts & Base Interfaces (`AgentContext`, `AgentResult`, `AIProvider`, `ResearchProvider`, `ImageGenerationProvider`).
- **Phase 4**: `SyllabusAnalysisAgent` & `TopicDecompositionAgent`.
- **Phase 5**: Web Research Engine & Plagiarism / Originality Check.
- **Phase 6**: Content Planning & Generation Agents (`ContentWriterAgent`, paragraph-first policy).
- **Phase 7**: Derivation & Mathematical Equation Engine (OMML / MathML, Greek symbols, fractions, centered derivations).
- **Phase 8**: Diagram Engine (`DiagramPlannerAgent`, `DiagramPromptAgent`, Black-and-White academic style, Matplotlib/SVG/Gemini).
- **Phase 9**: Quality, Fact Check & Consistency Agents (`ContentReviewAgent`, `FactCheckAgent`, `BookConsistencyAgent`).
- **Phase 10**: Document Engine (`DocumentStructureAgent`, `DocumentFormattingAgent`, `DOCXExportAgent`, `DocumentValidationAgent`).
- **Phase 11**: Multi-Agent Orchestrator & Durable Worker Pipeline (`BookGenerationOrchestrator`).
- **Phase 12**: API v1 & Frontend Integration (New toggles for Numericals, Q&A, Research, Diagram options, live logs, reports).
- **Phase 13**: Comprehensive Automated Testing (Syllabus, Math, Content, Images, DOCX, Jobs, Events).
- **Phase 14**: Complete Documentation Suite & Acceptance Test.
