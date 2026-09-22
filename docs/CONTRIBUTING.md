# Contributing to AI Book Writer v3.0

Thank you for your interest in enhancing the AI Book Writer academic publishing platform!

---

## 1. Development Environment Setup

1. **Prerequisites:**
   - Python 3.10+ (Python 3.11 recommended).
   - Git.
   - Node.js (optional, only if modifying custom web tooling).

2. **Clone and Virtual Environment:**
   ```bash
   git clone https://github.com/shivangsaxena1011/aiwritter.git
   cd aiwritter
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   Set `AI_MODE="mock"` to run offline tests without consuming Gemini API tokens.

---

## 2. Running Automated Tests

Run the full test suite with pytest:
```bash
pytest -v
```

To run a specific test module:
```bash
pytest tests/test_docx_exporter.py -v
```

---

## 3. Project Directory Layout

```
aiwritter/
├── backend/
│   ├── app/
│   │   ├── agents/          # Autonomous editorial agents
│   │   ├── api/v1/          # FastAPI versioned routes
│   │   ├── core/            # Config, database engine, security
│   │   ├── models/          # SQLAlchemy database entities
│   │   ├── schemas/         # Pydantic schemas and validation
│   │   ├── services/ai/     # Gemini & Mock provider abstractions
│   │   ├── services/document/ # DOCX & PDF generation engines
│   │   ├── storage/         # Local & Cloud storage engines
│   │   └── workers/         # Pipeline execution & Queue manager
│   ├── app.py               # Legacy WSGI/ASGI entrypoint
│   └── main.py              # Application factory & static mounts
├── frontend/                # SPA interface (HTML/CSS/JS)
├── prompts/                 # Parameterized prompt registry
├── templates/               # Word document master templates
├── tests/                   # Pytest test suite
└── docs/                    # Technical architecture & deployment guides
```

---

## 4. Modifying Prompts

All system prompts reside in `prompts/`. When modifying prompts:
- Keep parameterized placeholders enclosed in `{variable_name}`.
- Adhere to the anti-filler rules: disallow conversational fluff and enforce rigorous academic structure.
- Run `pytest tests/test_toc_parser.py` and `pytest tests/test_content_pipeline.py` after modifications.
