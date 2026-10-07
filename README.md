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
  - `TopicDecompositionAgent` (Normalized canonical matching for Physics, CS, Math, Engineering blueprints)
  - `ResearchAgent` (IEEE/APA bibliography management, live CrossRef/Wikipedia grounding, prompt injection defenses)
  - `ContentPlanningAgent` (Pedagogical roadmaps, learning outcomes)
  - `ContentWriterAgent` (Paragraph-first academic prose, anti-AI cliché filters)
  - `DerivationAgent` (Formal mathematical proof structures)
  - `DiagramPromptAgent`, `DiagramPlannerAgent`, & `DiagramGeneratorAgent` (Monochrome line art & chapter-aware captions)
  - `ContentReviewAgent` (Multi-dimensional 100-point rubric, automatic rewrite loops)
  - `FactCheckAgent` & `BookConsistencyAgent` (Claim auditing, cross-chapter terminology memory)
  - `DocumentStructureAgent`, `DOCXExportEngine`, & `DocumentValidationAgent` (Canonical textbook layout, native OMML, and automated DOCX inspection)
  - `IndependentArtifactAuditor` & `FinalDocxAuditor` (Direct OpenXML artifact truth verification)
- **📐 Native Word OMML Equations:** Converts LaTeX equations directly into Microsoft Word OMML XML elements (`<m:oMathPara>`, `<m:f>`, `<m:rad>`, `<m:sSup>`). Equations are crisp, vectorized, and editable in Microsoft Word with Cambria Math.
- **📊 Publication-Grade Typography & Tables:** Strict adherence to academic standards: Times New Roman, 12pt body, 1.5 line spacing, Justified alignment, 1-inch margins, running headers, and native XML tables with dark slate headers (`#1E293B`) and zebra striping.
- **📈 Black-and-White Academic Schematics:** Automatically generates high-contrast technical line art using **Google Imagen 3** or deterministic **Matplotlib** scientific plots, with resilient multi-tier fallback to styled academic callouts.
- **🔄 Durable Job Engine & Partial Recovery:** Background worker queue backed by SQLite or PostgreSQL. Checkpoints completed sections to disk and database—if interrupted, generation resumes seamlessly without lost progress.
- **🔍 Automated Quality Reports:** Emits comprehensive OpenXML audits assessing font compliance, line spacing, margins, OMML display equations, table shading, and syllabus coverage.
- **🔒 Zero-Credential Persistence:** Gemini API keys are held strictly in runtime memory, never written to disk, database, or browser `localStorage`.

---

## 🏛️ System Architecture

```text
INPUT (Topic, Course Outline, or University Syllabus)
  │
  ▼
SYLLABUS ANALYSIS & DOMAIN CLASSIFIER
  │
  ▼
TOPIC DECOMPOSITION AGENT (Canonical Hierarchy & Archetype Contracts)
  │
  ▼
CONTENT PLANNING & ROADMAP AGENT
  │
  ├──► WEB RESEARCH AGENT (Live CrossRef/Wikipedia, Data Fencing, IEEE/APA Citations)
  │
  ▼
CONTENT WRITER & DERIVATION AGENTS (Paragraph-First Prose, Solved Numericals, Q&A)
  │
  ├──► DIAGRAM SYSTEM (Monochrome Line Art / Matplotlib Plots, Chapter Captions)
  │
  ▼
EDITORIAL REVIEW & FACT-CHECK AGENTS (5-Dimension Rubric, Anti-Plagiarism)
  │
  ▼
CANONICAL BOOK ASSEMBLY MODEL (Content Orchestration 2.1)
  │
  ▼
NATIVE DOCX EXPORT ENGINE (Times New Roman 12pt, 1.5 Spacing, OMML Math)
  │
  ▼
INDEPENDENT ARTIFACT AUDITOR (Re-opens DOCX OpenXML, Validates Word Count & Equations)
  │
  ▼
PRODUCTION MICROSOFT WORD TEXTBOOK (.docx) + VERIFICATION REPORTS
```

---

## 🚀 How to Run AIWritter

### Prerequisites
- **Python 3.10 – 3.12** installed on your system.
- *(Optional)* A **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/) for live AI generation. If not provided, AIWritter includes built-in authoritative knowledge models for offline generation and testing.

---

### Method 1: Windows One-Click Launch (Easiest)
Simply double-click the included batch launcher in the project root:
```cmd
Double-Click-To-Run.bat
```
This batch file will:
1. Verify or create your Python virtual environment (`.venv`).
2. Install all required dependencies from `requirements.txt`.
3. Create all runtime directories (`output/`, `output/assets/`).
4. Initialize the database schema (`app.db`).
5. Start the FastAPI server on `http://127.0.0.1:8000`.
6. Automatically open your default web browser to the AIWritter Publishing Studio.

---

### Method 2: Manual Command Line Launch (All Platforms)

1. **Activate Virtual Environment:**
   ```powershell
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS:
   source .venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables (Optional):**
   Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
   Set your API key if using live Google Gemini:
   ```env
   GEMINI_API_KEY=AIzaSy...your_key_here
   AI_MODE=gemini
   ```

4. **Start the Web Application:**
   ```bash
   uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

5. **Open the Studio:**
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

### Method 3: Headless CLI Book Generation
To generate textbooks directly from the terminal without using the web UI:

- **Generate Full 5-Chapter University Physics Book:**
  ```powershell
  .\.venv\Scripts\python.exe scripts/generate_full_5chapter_book.py
  ```
  Generates a complete 5-chapter textbook covering Quantum Mechanics, Wave Optics, Lasers, Fiber Optics, and Electromagnetism/Relativity into `./output/`.

- **Run Multi-Tier Acceptance Benchmarks:**
  ```powershell
  .\.venv\Scripts\python.exe scripts/run_final_production_benchmarks.py
  ```

---

## 💻 Using the Web Application (3-Step Publishing Workflow)

1. **Step 1: Syllabus & Topic Definition**
   - Enter your **Book Title**, **Subtitle**, and **Author / Institution**.
   - Paste a raw university syllabus, course outline, or topic list into the input box.
   - Click **AI Parse Syllabus** to automatically decompose the syllabus into chapters, topics, and subtopics.
   - Customize academic options: Writing Depth (*Detailed*, *Standard*, *Comprehensive*), Citation Style (*IEEE*, *APA*), Solved Numericals toggle, Review Questions toggle, and Diagram generation toggle.
   - Click **Begin Book Generation**.

2. **Step 2: Live Publishing Engine & Event Stream**
   - Watch real-time multi-agent orchestration via Server-Sent Events (SSE).
   - Track live agent progress across syllabus parsing, web research, content drafting, mathematical derivations, diagram generation, peer review, and DOCX assembly.
   - Inspect console logs, word counts, and stage updates in real time.

3. **Step 3: Document Review & Download**
   - Review the final document scorecard (academic rigor, completeness, consistency, pedagogy).
   - Click **Download Completed Textbook (.docx)** to retrieve your publication-grade Microsoft Word document.

---

## 🧹 Test-Data Cleanup & Sanitization

AIWritter includes an automated data sanitization utility to ensure zero mock data, ephemeral test records, or temporary lock files pollute the production environment:

```powershell
.\.venv\Scripts\python.exe scripts/clean_test_data.py
```

This utility safely:
- Purges all test records and jobs from the SQLite database.
- Re-initializes a pristine database schema with 0 rows across all 13 production tables.
- Cleans stale test outputs and assets from `./output/`.
- Protects user templates (`templates/master_book_template.docx`) and source code.
- Generates `artifacts/test_data_cleanup_report.json` and `.md`.

---

## 🧪 Automated Test & Regression Suite

AIWritter features a **104-test automated pytest suite** and a **20-point historical defect regression suite** verifying all mathematical engines, multi-agent pipelines, document typography, and security boundaries:

```powershell
# Run the complete test suite (104 tests)
.\.venv\Scripts\python.exe -m pytest -v

# Run historical defect regressions
.\.venv\Scripts\python.exe -m pytest tests/test_defect_regressions.py -v

# Run content intelligence & quality gate tests
.\.venv\Scripts\python.exe -m pytest tests/test_content_intelligence.py -v
```

### Verified Benchmark Levels (Direct OpenXML Reconciliation):
1. **Level 1 (Micro Benchmark):** 1 Chapter, 5 Topics, 27 Sections, 98 OMML equations, 2 tables, 2 figures, 4,944 words (`artifacts/final_micro_benchmark.docx`) — **PASSED (`publication_ready = True`, 0 blocking issues)**.
2. **Level 2 (Quantum Mechanics):** 1 Chapter, 12 Topics, 61 Sections, 208 OMML equations, 4 tables, 3 figures, 9,744 words (`artifacts/final_quantum_mechanics_benchmark.docx`) — **PASSED (`publication_ready = True`, 0 blocking issues)**.
3. **Level 3 (Full 5-Chapter B.Tech Syllabus):** 5 Chapters, 53 Topics, 106 Sections, 447 OMML equations, 3 tables, 7 figures, 21,075 words (`artifacts/final_full_btech_benchmark.docx`) — **PASSED (`publication_ready = True`, 0 blocking issues)**.

---

## 📚 Technical Documentation

Explore detailed engineering documentation in the [`docs/`](docs/) directory:

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

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
