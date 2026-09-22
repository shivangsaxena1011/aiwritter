# AI Book Writer v3.0 — Agentic Academic Publishing Platform

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Google Gemini](https://img.shields.io/badge/Gemini%202.5-Flash%20%2F%20Pro-8E75C2.svg)](https://ai.google.dev/)
[![Imagen 3](https://img.shields.io/badge/Imagen%203-Enabled-blue.svg)](https://cloud.google.com/vertex-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Autonomous AI-powered platform for generating university-grade academic textbooks (300+ pages) from syllabi or raw outlines, featuring multi-agent editorial review, Imagen 3 & Matplotlib scientific diagrams, and native Word `.docx` formatting.**

---

## 🌟 Key Highlights & Innovations in v3.0

- **🤖 8 Autonomous Domain Agents:** Full editorial team including `TOCPlanner`, `BookContextManager`, `ChapterDepthController`, `ContentWriter`, `DiagramSystem`, `ReviewAgent` (1–100 rubric), `ConsistencyAuditor`, and `QualityController`.
- **📊 Real Native Word Tables:** Converts markdown tables into true Word XML tables (`<w:tbl>`) with colored headers and alternating zebra row striping—never raw markdown text blocks.
- **📈 Scientific Diagrams:** Automatically balances between **Google Imagen 3** photorealistic illustrations and **Matplotlib** technical graphs (polarization curves, distributions, state diagrams).
- **🔄 Durable Job Engine & Partial Recovery:** Background worker queue backed by SQLite or PostgreSQL. If a network blip occurs, the pipeline checkpoints to disk and resumes from the exact section without regenerating previous chapters.
- **⚡ Pre-Generation Live Estimator:** Real-time computation of total word count, page count (~380 words/page), generation duration, and diagram counts as you edit the outline or adjust depth levels.
- **🎨 Dark Glassmorphic Interface:** Futuristic glassmorphic cards, glowing orbs, interactive tree editor, live progress bar, and real-time console log with Server-Sent Events (SSE).
- **🔒 Zero-Credential Persistence:** Gemini API keys are held strictly in runtime memory, never written to disk, database, or browser `localStorage`.

---

## 🏛️ System Architecture

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
|  - API Router (/api/v1/books, /api/v1/jobs, /api/v1/files)                       |
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

## 🛠️ Configuration & Deployment Modes

Copy the configuration template:
```bash
cp .env.example .env
```

### Mode A: Local Standalone (Default)
- **Database:** SQLite (`data/aiwriter.db`) with Write-Ahead Logging (WAL).
- **Worker:** In-process asyncio semaphore queue.
- **Storage:** Local filesystem (`./output/`).

### Mode B: Cloud Distributed (Production)
- **Frontend:** Deployed to Vercel via included `vercel.json`.
- **Backend & Worker:** Deployed on Render, Railway, or AWS ECS.
- **Database:** Managed PostgreSQL (`DATABASE_URL="postgresql+psycopg2://..."`).
- **Distributed Queue:** Redis (`REDIS_URL="redis://..."`).
- **Storage:** S3 / Cloudflare R2 / GCS (`STORAGE_TYPE="s3"`).

---

## 🧪 Automated Test Suite

AI Book Writer comes with a comprehensive **24-test suite** covering all critical subsystems:

```bash
# Run full test suite
pytest -v
```

### Verified Test Categories:
- `test_api.py`: FastAPI endpoints, health check, job dispatch, legacy compatibility.
- `test_content_pipeline.py`: Agent orchestration, context continuity, review scoring, consistency audits.
- `test_docx_exporter.py`: Production Word exporter, master template integration, native table rendering.
- `test_file_security.py`: Path traversal protection, safe slugification, API key masking.
- `test_job_state.py`: Job state machine transitions (`QUEUED` -> `GENERATING` -> `CANCELLED` -> `RETRYING`).
- `test_toc_parser.py`: Regex syllabus parsing, markdown heading parsing, AI planning fallback.
- `test_validation.py`: Pydantic schema validation, depth controller profiles.

---

## 📚 Technical Documentation

Comprehensive architectural and engineering guides are available in the [`docs/`](docs/) directory:

- [**System Architecture**](docs/ARCHITECTURE.md): Component interactions, data flow, dual-mode deployment.
- [**REST API Specification**](docs/API.md): Full OpenAPI reference for `/api/v1/` and SSE streaming endpoints.
- [**AI Pipeline & Agents**](docs/AI_PIPELINE.md): Multi-agent orchestration, prompt registry, depth controller.
- [**Generation Pipeline**](docs/GENERATION_PIPELINE.md): 14-stage DAG execution sequence and partial recovery.
- [**Database & Schema**](docs/DATABASE.md): SQLAlchemy models, ER diagram, SQLite vs PostgreSQL.
- [**Deployment Guide**](docs/DEPLOYMENT.md): Step-by-step instructions for local and cloud production setups.
- [**Security & Privacy**](docs/SECURITY.md): Path traversal defense, key isolation, schema validation.
- [**Contributing Guide**](docs/CONTRIBUTING.md): Code style, adding agents, running test suites.
- [**Troubleshooting FAQ**](docs/TROUBLESHOOTING.md): Rate limits, template recovery, error handling.

---

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.
