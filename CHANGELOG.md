# Changelog — AIWritter

All notable changes to the AIWritter autonomous academic book publishing platform will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0-PROD] — 2026-10-07

### Production Release Candidate Acceptance & Hardening

#### Added
- **Independent Artifact Truth Engine (`IndependentArtifactAuditor`):** Standalone Word DOCX verification engine that directly reopens rendered `.docx` packages from disk, parses `<w:p>`, `<w:tbl>`, `<m:oMath>`, and `<a:blip>`, and strictly enforces authentic 3-way count reconciliation (`planned == assembled == rendered_docx`).
- **3-Tier Comprehensive Benchmark Verification Suite:**
  - **Level 1 (Micro Benchmark):** 1 Chapter, 5 Topics, 27 Sections, 37 OMML equations, 1,805 words (`artifacts/final_micro_benchmark.docx`) — **PASSED (0 blocking issues)**.
  - **Level 2 (Quantum Mechanics):** 1 Chapter, 12 Topics, 61 Sections, 39 OMML equations, 4 tables, 7 figures, 3,133 words (`artifacts/final_quantum_mechanics_benchmark.docx`) — **PASSED (0 blocking issues)**.
  - **Level 3 (Full 5-Chapter B.Tech):** 5 Chapters, 53 Topics, 106 Sections, 22 OMML equations, 3 tables, 7 figures, 5,536 words (`artifacts/final_full_btech_benchmark.docx`) — **PASSED (0 blocking issues)**.
- **Multi-Domain Pedagogical Knowledge Base (`SubjectKnowledgeBase`):** Extensible domain intelligence framework providing authentic academic equations, concepts, experiments, and terminology rules across 6 disciplines:
  - Engineering Physics
  - Mathematics
  - Computer Science
  - Electronics & Electrical Engineering
  - Mechanical Engineering
  - Generic Technical Systems
- **Historical Defect Regression Suite (`tests/test_defect_regressions.py`):** 20 automated regression tests verifying permanent resolution of preamble promotion, duplicate headings, repetitive table generation, raw LaTeX leaks, and false count matches.
- **Fail-Fast Security & Configuration Guards:**
  - Added `ALLOW_MOCK_PROVIDERS: bool = False` guard in `Settings`.
  - Added startup assertions in `main.py` lifespan: rejects mock provider selection when `APP_ENV=production`.
  - Added write permission probe for local and cloud storage targets.
- **Alembic Database Migration Baseline:** Initial schema migration (`alembic/versions/12754522d378_initial_schema.py`) generating DDL for all 13 core relational tables (`users`, `projects`, `books`, `book_units`, `book_topics`, `book_subtopics`, `generation_jobs`, `generation_events`, `generated_assets`, `generated_sections`, `research_sources`, `review_results`, `document_exports`).
- **Complete Test Data Cleanup Infrastructure (`scripts/clean_test_data.py`):** Purges Categories C, E, and F while strictly protecting Categories A (User Data: 0 deleted) and B (Production Templates).

#### Changed
- Consolidated pipeline orchestrator around `BookAssemblyModel` intermediate representation.
- Completely removed client-side API key inputs from frontend web UI (`index.html`, `app.js`). All secrets managed exclusively via server `.env`.
- Updated `.gitignore` to ignore SQLite WAL (`*.db-wal`) and shared memory (`*.db-shm`) lock files.
- Upgraded test suite from 39 to 104 unit/integration tests with 100% pass rate.

#### Fixed
- Fixed table duplication by introducing cryptographic SHA-256 table markdown hashing in `TablePlanner`.
- Fixed figure caption semantic verification in `IndependentArtifactAuditor` to evaluate both parent topic and subtopic titles.
- Eliminated canned, robotic introductory sentences across subject knowledge generation models.

---

## [2.2.0] — 2026-10-07
- Introduced `FinalDocxAuditor` and initial OpenXML inspection.
- Implemented `BookAssemblyModel` dataclass hierarchy.
- Added OMML mathematical fraction and nested radical support.

## [2.1.0] — 2026-10-07
- Added `RepetitionDetector2` sentence-level duplicate detection.
- Introduced `ConceptOwnershipRegistry` to prevent cross-chapter topic contamination.
- Added `TablePlanner` pedagogical necessity evaluation.

## [2.0.0] — 2026-10-07
- Transitioned to durable job worker queue with SQLite/PostgreSQL persistence.
- Added Server-Sent Events (SSE) streaming for real-time progress updates.
- Integrated Crossref REST API and Wikipedia for academic citations.

## [1.0.0] — 2026-10-06
- Initial release of AIWritter prototype.
