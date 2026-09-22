# AI Book Writer v3.0 — System Architecture

## 1. High-Level Architecture Overview

AI Book Writer v3.0 is an agentic academic publishing platform engineered to transform raw course outlines, university syllabi, or topical prompts into 300+ page, publication-ready academic reference textbooks.

```
                      +---------------------------------------+
                      |       Web Client (Browser SPA)        |
                      |   Dark Glassmorphism, SSE, Tree Editor|
                      +---------------------------------------+
                                          |
                                HTTP / SSE / REST
                                          v
+-----------------------------------------------------------------------------------+
|                            FastAPI Application (ASGI)                             |
|  - API Router (/api/v1/)                                                          |
|  - Core Security (Path traversal defenses, API sanitization)                      |
|  - Static Asset Server                                                            |
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
                     |    BookGenerationPipeline (14-Stage DAG)    |
                     +---------------------------------------------+
                               |              |              |
                               v              v              v
                     +---------------+ +--------------+ +---------------+
                     | Agent Layer   | | AI Provider  | | Document      |
                     | - TOCPlanner  | | - Gemini 2.5 | |   Engine      |
                     | - ContextMgr  | | - Imagen 3   | | - DOCXEngine  |
                     | - DepthCtrl   | | - Matplotlib | | - Native Tabs |
                     | - Writer      | | - MockProvider | - PDF Export  |
                     | - Reviewer    | +--------------+ +---------------+
                     | - Auditor     |
                     +---------------+
```

---

## 2. Core Architectural Principles

1. **Durable Asynchronous Job Processing:**
   No book generation runs inside ephemeral HTTP request threads or process-local in-memory dictionaries (`tasks = {}`). All generation tasks are durable database rows (`GenerationJob`) managed by a concurrency-throttled queue (`JobQueueManager`), persisting progress, checkpoints, and event logs.

2. **Partial Recovery & Checkpointing:**
   If a network drop, API rate limit, or server restart interrupts a 10-chapter textbook run at section 4.2, the pipeline checkpoints completed sections (`GeneratedSection`) to disk and database. Retrying resumes from the interrupted point without regenerating prior sections.

3. **Multi-Agent Quality Loop:**
   Generation does not simply write markdown. The system runs an autonomous editorial team:
   - **TOCPlanner**: Normalizes syllabi into an academic tree structure.
   - **BookContextManager**: Propagates cross-chapter continuity, terminology, and notation.
   - **ChapterDepthController**: Enforces token budgets and depth tiers (Concise to Reference).
   - **ContentWriter**: Produces academic prose, LaTeX equations, and worked examples.
   - **DiagramSystem**: Dynamically selects between Imagen 3 and Matplotlib scientific graphs.
   - **ReviewAgent**: Evaluates against an academic rubric (1–100 score).
   - **ConsistencyAuditor**: Audits nomenclature, symbols, and acronyms across chapters.
   - **QualityController**: Emits a verifiable publication scorecard.

4. **Production Document Engine:**
   The exporter generates native Word `.docx` documents based on `templates/master_book_template.docx`. Markdown tables are converted into true Word XML tables (`<w:tbl>`) with shaded headers and alternating rows—never raw monospace markdown blocks.

---

## 3. Dual Deployment Modes

### Mode A: Self-Contained Local (Zero Infrastructure)
- **Database:** SQLite (`data/aiwriter.db`) with WAL journal mode.
- **Worker:** In-process asyncio semaphore queue.
- **Storage:** Local filesystem (`./output/`).
- **AI Mode:** Direct user API key or server `GEMINI_API_KEY`.

### Mode B: Cloud Distributed (Production Grade)
- **Frontend:** Vercel edge CDN.
- **Backend / Worker:** Render / Railway / ECS persistent service container.
- **Database:** Managed PostgreSQL (Supabase, Neon, AWS RDS).
- **Queue Broker:** Redis cluster for distributed worker scaling.
- **Storage:** S3 / Cloudflare R2 / Google Cloud Storage.
