# AIWritter — Testing & Verification Guide

AIWritter maintains a comprehensive automated test suite guaranteeing stability, mathematical correctness, document typography compliance, and security defenses.

---

## 1. Test Suite Architecture

The test suite covers unit logic, integration boundaries, security protections, and full end-to-end publishing pipelines.

| Test Module | Focus Area | Key Verifications |
|-------------|------------|-------------------|
| `tests/test_api.py` | FastAPI REST & SSE Endpoints | Health check, cost estimation, book CRUD, job dispatch/cancellation, legacy endpoints. |
| `tests/test_content_pipeline.py` | Content Agents & Editorial Logic | ContentWriter drafting, context continuity tracking, review scoring rubric, consistency auditor. |
| `tests/test_diagram_and_images.py` | Visuals & Technical Schematics | Monochrome prompt enforcement, Matplotlib deterministic plot generation, chapter-aware captions. |
| `tests/test_document_validation_and_quality.py` | Document Quality Assurance | Programmatic DOCX validation, typography checks, equation detection, table compliance. |
| `tests/test_docx_exporter.py` | Word Document Assembly | Times New Roman typography, 1.5 line spacing, Justified alignment, native XML tables, OMML display math. |
| `tests/test_e2e_publishing_pipeline.py` | Full Pipeline Orchestrator | Complete 14-stage execution, asset persistence, database state transitions, quality report generation. |
| `tests/test_file_security.py` | Storage & Path Defenses | Directory traversal prevention, safe filename sanitation, storage key integrity. |
| `tests/test_job_state.py` | Concurrency & Job Queues | Async job queue lifecycle, state transitions (CREATED → RUNNING → COMPLETED). |
| `tests/test_omml_and_math.py` | Mathematical Engines | LaTeX to OMML XML translation, balanced brace radicals, MathValidator canonical structure, arithmetic sanity. |
| `tests/test_research_and_originality.py` | Research & Anti-Plagiarism | Academic source gathering, IEEE/APA bibliographies, prompt injection fencing, 6-gram originality audit. |
| `tests/test_syllabus_analysis_agent.py` | Syllabus Extraction | Unstructured course parsing, subject/domain classification, zero topic omission. |
| `tests/test_toc_parser.py` | TOC Normalization | Hierarchical outline extraction, roman/numeric unit identification. |
| `tests/test_validation.py` | Request & Model Validation | Input schema validation, bounds checking, parameter sanitization. |

---

## 2. Running the Tests

Ensure your Python virtual environment is activated:

```powershell
# Run the complete test suite
.\venv\Scripts\python.exe -m pytest -v

# Run a specific test module
.\venv\Scripts\python.exe -m pytest tests/test_omml_and_math.py -v

# Run with test coverage report
.\venv\Scripts\python.exe -m pytest --cov=backend/app tests/
```

---

## 3. Testing with Mock vs. Live Providers

### Offline / Mock Testing (Default)
Tests run deterministically without internet access or API keys by utilizing `MockProvider` and `MockResearchProvider`:
- Zero API latency.
- Completely predictable structured responses.
- Guaranteed offline test repeatability.

### Live Gemini Testing
To execute verification against live Gemini models:
1. Ensure your `.env` contains a valid `GEMINI_API_KEY`.
2. Set `AI_MODE=gemini` in `.env`.
3. Set `GEMINI_TEXT_MODEL=gemini-2.5-flash` and `GEMINI_IMAGE_MODEL=imagen-3.0-generate-002`.

---

## 4. Continuous Integration (CI) Guidelines

In CI environments (e.g. GitHub Actions):
- Run tests on Ubuntu and Windows runners.
- Matplotlib must execute in headless mode using `matplotlib.use("Agg")` (already configured in codebase).
- Ensure Python version is $\ge 3.10$.
