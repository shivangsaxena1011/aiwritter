# AIWritter — System Architecture

AIWritter is an autonomous, agentic academic textbook publishing platform engineered to transform raw course outlines, university syllabi, and research topics into complete, rigorous, publication-grade Microsoft Word (`.docx`) textbooks.

```
                      +---------------------------------------+
                      |       Web Client (Browser SPA)        |
                      |   Modern Glassmorphism, SSE, Controls |
                      +---------------------------------------+
                                          |
                                HTTP / SSE / REST
                                          v
+-----------------------------------------------------------------------------------+
|                            FastAPI Application (ASGI)                             |
|  - API Router (/api/v1/)                                                          |
|  - Core Security (Path traversal defenses, API sanitization)                      |
|  - Static Asset Server & SSE Event Streaming                                      |
|  - Backward Compatibility Adapter (/api/generate, /api/stream)                   |
+-----------------------------------------------------------------------------------+
       |                                          |                         |
       v                                          v                         v
+--------------+                       +--------------------+     +-------------------+
|  SQLAlchemy  |                       | Background Worker  |     |  Storage Engine   |
|  Data Layer  |                       |   Queue Manager    |     |  Local / S3 / GCS |
+--------------+                       +--------------------+     +-------------------+
  (SQLite / PG)                                   |
                                                  v
                     +---------------------------------------------+
                     |  BookGenerationOrchestrator (14-Stage DAG)  |
                     +---------------------------------------------+
                               |              |              |
                               v              v              v
                     +---------------+ +--------------+ +---------------+
                     | Agent Layer   | | AI Provider  | | Document      |
                     | - 15 Agents   | | - Gemini 2.5 | |   Engine      |
                     | - Research    | | - Imagen 3   | | - DOCX Engine |
                     | - Derivations | | - Matplotlib | | - OMML Engine |
                     | - Review Loops| | - MockProvider | - Validation  |
                     +---------------+ +--------------+ +---------------+
```

---

## 1. Core Architectural Pillars

1. **Autonomous 15-Agent Pipeline:**
   Instead of a monolithic prompt, generation is divided across 15 dedicated agents:
   - `SyllabusAnalysisAgent` & `TopicDecompositionAgent`: Comprehensive blueprinting with zero topic omission.
   - `ResearchAgent`: Authoritative academic retrieval, IEEE/APA citation management, and 6-gram originality auditing.
   - `ContentPlanningAgent` & `ContentWriterAgent`: Paragraph-first drafting, anti-AI cliché filtering, structured markdown tables.
   - `DerivationAgent`: Strict mathematical proof formulation (Starting Equation → Assumptions → Step-by-Step Transformations → Final Result).
   - `DiagramPromptAgent`, `DiagramPlannerAgent`, & `DiagramGeneratorAgent`: Monochrome academic line art, Matplotlib scientific charts, and chapter-aware numbering (`Figure X.Y`).
   - `ContentReviewAgent`, `FactCheckAgent`, & `BookConsistencyAgent`: Multi-dimensional evaluation (Depth, Pedagogy, Filler, Accuracy, Completeness), claim categorization, and cross-chapter terminology registry.
   - `DocumentStructureAgent`, `DOCXExportEngine`, & `DocumentValidationAgent`: Canonical textbook structuring, native OMML mathematical typesetting, and automated DOCX XML inspection.

2. **Durable Asynchronous Job Processing:**
   Generation jobs are durable database rows (`GenerationJob`) managed by `JobQueueManager`. Each state transition (CREATED → RUNNING → COMPLETED / PARTIAL / FAILED) is persisted to SQLite/PostgreSQL and broadcast via Server-Sent Events (SSE).

3. **Partial Recovery & Checkpointing:**
   If a network drop, API rate limit, or server interruption occurs mid-generation, completed sections (`GeneratedSection`) remain persisted. Retrying resumes from the last checkpoint without regenerating prior work.

4. **Production Document Engine:**
   - **Typography:** Strict academic standard (Times New Roman, 12pt body, 1.5 line spacing, Justified alignment, 1-inch margins).
   - **Native OMML:** Mathematical expressions are rendered as native Word OMML XML elements (`<m:oMathPara>`, `<m:f>`, `<m:rad>`, `<m:sSup>`), ensuring crisp, editable, vectorized math.
   - **Native Tables:** Formatted Word XML tables with dark headers (`#1E293B`) and zebra striping.

---

## 2. System Modules & Directory Layout

```text
ai-book-writer/
├── backend/
│   └── app/
│       ├── agents/              # 15 Specialized publishing agents
│       ├── api/v1/              # FastAPI endpoints (books, jobs, files, sse)
│       ├── core/                # Configuration, logging, security
│       ├── db/                  # SQLAlchemy session & base models
│       ├── models/              # Book, BookUnit, Topic, Subtopic, Job, ResearchSource
│       ├── services/
│       │   ├── ai/              # Gemini, Imagen 3, Mock providers
│       │   ├── document/        # DOCX engine, table styling, Word XML builder
│       │   ├── image/           # Image validation, Matplotlib plots, Imagen 3
│       │   ├── math/            # OMML engine, MathValidator, arithmetic sanity
│       │   └── research/        # WebResearch, MockResearch, prompt injection fencing
│       ├── storage/             # Local filesystem, S3, GCS storage providers
│       └── workers/             # Pipeline orchestrator, queue manager, recovery
├── docs/                        # Complete technical and operational documentation
├── frontend/                    # Dark glassmorphism single-page application
├── prompts/                     # System prompts for all agents
├── templates/                   # Word DOCX document templates
└── tests/                       # Comprehensive pytest suite (39 tests)
```

---

## 3. Dual Deployment Modes

### Mode A: Self-Contained Local (Zero Infrastructure)
- **Database:** SQLite (`data/aiwriter.db`) with Write-Ahead Logging (WAL).
- **Worker:** In-process asyncio concurrency queue.
- **Storage:** Local filesystem (`./output/`).
- **AI Mode:** Direct user API key or server-configured `GEMINI_API_KEY`.

### Mode B: Cloud Distributed (Production Grade)
- **Frontend:** Vercel edge CDN.
- **Backend / Worker:** Render / Railway / AWS ECS container.
- **Database:** Managed PostgreSQL (Supabase, Neon, AWS RDS).
- **Queue Broker:** Redis cluster for horizontal worker scaling.
- **Storage:** AWS S3 / Cloudflare R2 / Google Cloud Storage.
