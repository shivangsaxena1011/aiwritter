# AIWritter — Agentic Academic Book Publishing Platform

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Google Gemini](https://img.shields.io/badge/Gemini%202.5-Flash%20%2F%20Pro-8E75C2.svg)](https://ai.google.dev/)
[![Imagen 3](https://img.shields.io/badge/Imagen%203-Enabled-blue.svg)](https://cloud.google.com/vertex-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Autonomous multi-agent publishing platform transforming university syllabi, course outlines, and research topics into complete, publication-grade Microsoft Word (`.docx`) textbooks. Features native OMML mathematical typesetting, academic black-and-white schematics, rigorous peer review, and automated quality validation.**

---

## 🌟 Key Capabilities & Architectural Innovations

- **🤖 15 Autonomous Domain Agents:** Specialized multi-agent publishing team including:
  - `SyllabusAnalysisAgent` (Zero topic omission parser & domain classification)
  - `TopicDecompositionAgent` (Physics, CS, Math, Engineering blueprints)
  - `ResearchAgent` (IEEE/APA bibliography management, 6-gram originality audit)
  - `ContentPlanningAgent` (Pedagogical roadmaps, learning outcomes)
  - `ContentWriterAgent` (Paragraph-first academic prose, anti-AI cliché filters)
  - `DerivationAgent` (Formal mathematical proof structures)
  - `DiagramPromptAgent`, `DiagramPlannerAgent`, & `DiagramGeneratorAgent` (Monochrome line art & chapter-aware captions)
  - `ContentReviewAgent` (Multi-dimensional 100-point rubric, automatic rewrite loops)
  - `FactCheckAgent` & `BookConsistencyAgent` (Claim auditing, cross-chapter terminology memory)
  - `DocumentStructureAgent`, `DOCXExportEngine`, & `DocumentValidationAgent` (Canonical textbook layout, native OMML, and automated DOCX inspection)
- **📐 Native Word OMML Equations:** Converts LaTeX equations directly into Microsoft Word OMML XML elements (`<m:oMathPara>`, `<m:f>`, `<m:rad>`, `<m:sSup>`). Equations are crisp, vectorized, and editable in Microsoft Word with Cambria Math.
- **📊 Publication-Grade Typography & Tables:** Strict adherence to academic standards: Times New Roman, 12pt body, 1.5 line spacing, Justified alignment, 1-inch margins, running headers, and native XML tables with dark slate headers (`#1E293B`) and zebra striping.
- **📈 Black-and-White Academic Schematics:** Automatically generates high-contrast technical line art using **Google Imagen 3** or deterministic **Matplotlib** scientific plots, with resilient multi-tier fallback to styled academic callouts.
- **🔄 Durable Job Engine & Partial Recovery:** Background worker queue backed by SQLite or PostgreSQL. Checkpoints completed sections to disk and database—if interrupted, generation resumes seamlessly without lost progress.
- **🔍 Automated Quality Reports:** Emits `document_quality_report.json` auditing font compliance, line spacing, margins, OMML display equations, table shading, and syllabus coverage.
- **🔒 Zero-Credential Persistence:** Gemini API keys are held strictly in runtime memory, never written to disk, database, or browser `localStorage`.

---

## 🏛️ System Architecture

```text
USER / BROWSER CLIENT
  │
  ▼
SYLLABUS / TOPIC INPUT (with Academic Toggles)
  │
  ▼
SYLLABUS ANALYSIS AGENT (Zero-Omission Parsing)
  │
  ▼
TOPIC DECOMPOSITION AGENT (Domain Blueprints: Physics, CS, Math, Engineering)
  │
  ▼
CONTENT PLANNING AGENT (Pedagogical Roadmaps & Outcomes)
  │
  ├──► WEB RESEARCH AGENT (Data Fencing, Citations & IEEE/APA Bibliography)
  │
  ▼
CONTENT WRITER & DERIVATION AGENTS (Paragraph-First Prose, Anti-AI Filter)
  │
  ├──► DIAGRAM SYSTEM (Monochrome Line Art / Matplotlib Plots, Chapter Captions)
  │
  ▼
EDITORIAL REVIEW & FACT-CHECK AGENTS (5-Dimension Rubric, Rewrite Loops)
  │
  ▼
BOOK CONSISTENCY AGENT (Terminology & Notation Continuity)
  │
  ▼
DOCUMENT STRUCTURE & DOCX EXPORT ENGINE (Times New Roman, 1.5 Spacing, OMML)
  │
  ▼
DOCUMENT VALIDATION AGENT (Automated XML & Typography Compliance Report)
  │
  ▼
PRODUCTION MICROSOFT WORD TEXTBOOK (.docx) + QUALITY REPORT
```

---

## ⚡ Quick Start

### 1. Windows (One-Click)
Simply double-click:
```cmd
Double-Click-To-Run.bat
```
This automatically initializes the Python virtual environment, installs dependencies, creates data folders, and launches your browser to `http://127.0.0.1:8000`.

### 2. Linux / macOS
```bash
chmod +x run.sh
./run.sh
```

### 3. Docker Compose
```bash
docker-compose up -d --build
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🛠️ Configuration & Deployment

Copy the configuration template:
```bash
cp .env.example .env
```

### Key Configuration Variables:
```env
# AI Provider Configuration
AI_MODE=gemini                          # gemini or mock
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_TEXT_MODEL=gemini-2.5-flash
GEMINI_IMAGE_MODEL=imagen-3.0-generate-002
MAX_CONTENT_REVIEW_RETRIES=2

# Database & Storage
DATABASE_URL=sqlite:///./data/aiwriter.db  # or postgresql+psycopg2://...
STORAGE_TYPE=local                      # local, s3, gcs
STORAGE_LOCAL_DIR=./output
```

---

## 🧪 Comprehensive Automated Test & Regression Suite

AIWritter features a comprehensive **104-test automated suite** and a dedicated **20-point historical defect regression suite** verifying all mathematical engines, multi-agent pipelines, document typography, and security boundaries:

```powershell
# Run complete test suite (104 tests)
.\.venv\Scripts\python.exe -m pytest -v

# Run 20 historical defect regressions
.\.venv\Scripts\python.exe -m pytest tests/test_defect_regressions.py -v

# Run 3-tier production benchmark verification
.\.venv\Scripts\python.exe scripts/run_final_production_benchmarks.py --audit-only
```

### Verified Benchmark Levels:
1. **Level 1 (Micro Benchmark):** 1 Chapter, 5 Topics, 27 Sections, 37 OMML equations, 1,805 words (`artifacts/final_micro_benchmark.docx`) — **PASSED (0 blocking issues)**.
2. **Level 2 (Quantum Mechanics):** 1 Chapter, 12 Topics, 61 Sections, 39 OMML equations, 4 tables, 7 figures, 3,133 words (`artifacts/final_quantum_mechanics_benchmark.docx`) — **PASSED (0 blocking issues)**.
3. **Level 3 (Full 5-Chapter B.Tech):** 5 Chapters, 53 Topics, 106 Sections, 22 OMML equations, 3 tables, 7 figures, 5,536 words (`artifacts/final_full_btech_benchmark.docx`) — **PASSED (0 blocking issues)**.

### Test Coverage Highlights:
- `test_defect_regressions.py`: 20 / 20 regression tests guaranteeing prevention of preamble pollution, duplicate headings, repetitive table generation, raw LaTeX leaks, and false count reconciliation.
- `test_omml_and_math.py`: OMML XML conversion, nested radicals (`\sqrt{\frac{2}{L}}`), canonical numerical structure, and arithmetic sanity checks.
- `test_research_and_originality.py`: Academic research gathering, IEEE/APA references, prompt injection data fencing, and 6-gram originality audit.
- `test_diagram_and_images.py`: Academic monochrome prompt enforcement, Matplotlib technical schematics, and chapter-aware captions (`Figure X.Y`).
- `test_document_validation_and_quality.py`: Programmatic `.docx` validation of font family, line spacing, margins, OMML equations, and table formatting.
- `test_e2e_publishing_pipeline.py`: Complete 14-stage end-to-end publishing pipeline execution and asset persistence.
- `test_file_security.py`: Path traversal defenses, key isolation, safe filename sanitization.

---

## 📚 Technical Documentation

Explore the comprehensive engineering documentation in the [`docs/`](docs/) directory:

- [**System Architecture**](docs/ARCHITECTURE.md): Multi-agent pipeline overview, component interaction, and deployment modes.
- [**Agent Catalog & Specifications**](docs/AGENTS.md): Detailed specifications for all 15 publishing agents.
- [**Mathematical & OMML Engine**](docs/MATH_RENDERING.md): Native Word OMML XML generation, balanced-brace parsing, and numerical problem validation.
- [**Document Engine & Typography**](docs/DOCUMENT_ENGINE.md): Times New Roman standards, 1.5 line spacing, Justified alignment, and native XML tables.
- [**Academic Research Pipeline**](docs/RESEARCH_PIPELINE.md): Data fencing, prompt injection defenses, IEEE/APA bibliographies, and originality auditing.
- [**Diagram & Image Generation**](docs/IMAGE_GENERATION.md): Monochrome line art standards, Imagen 3, Matplotlib plotting, and chapter-aware captions.
- [**REST API Specification**](docs/API.md): Full OpenAPI reference for `/api/v1/` endpoints and SSE streams.
- [**Database Schema & Data Layer**](docs/DATABASE.md): SQLAlchemy 2.0 models, ER diagrams, and partial recovery storage.
- [**Testing & Verification Guide**](docs/TESTING.md): Test suite architecture, pytest commands, and verification protocols.
- [**Deployment Guide**](docs/DEPLOYMENT.md): Step-by-step instructions for local standalone and cloud production setups.
- [**Security & Privacy**](docs/SECURITY.md): Path traversal defenses, API key isolation, and prompt fencing.
- [**Troubleshooting FAQ**](docs/TROUBLESHOOTING.md): Operational solutions for API rate limits, OMML equations, and database concurrency.

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.
