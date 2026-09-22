import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import init_db, get_db
from backend.app.api.v1.router import api_v1_router
from backend.app.api.v1.books import parse_syllabus as v1_parse_syllabus, create_book as v1_create_book
from backend.app.api.v1.jobs import create_generation_job as v1_create_job, stream_job_events as v1_stream_job
from backend.app.api.v1.files import download_file as v1_download_file
from backend.app.schemas import ParseSyllabusRequest, CreateBookRequest, TableOfContentsSchema

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ai_book_writer")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.APP_ENV} mode)...")
    init_db()
    os.makedirs(settings.STORAGE_LOCAL_DIR, exist_ok=True)
    yield
    logger.info("Shutting down AI Book Writer...")

app = FastAPI(
    title="AI Book Writer v3.0 — Academic Publishing Platform",
    version=settings.APP_VERSION,
    description="Production-grade AI textbook publishing engine with multi-stage agents, durable jobs, and DOCX/PDF export.",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1
app.include_router(api_v1_router, prefix="/api")

# =========================================================================
# Backward Compatibility Endpoints for v2 / v1 Clients
# =========================================================================
@app.post("/api/generate")
async def compat_generate(req: dict, db: Session = Depends(get_db)):
    """Translates legacy /api/generate calls into v3 durable Book & Job pipeline."""
    title = req.get("title", "Academic Textbook")
    api_key = req.get("api_key")
    toc_data = req.get("toc", {"units": []})
    generate_images = bool(req.get("generate_images", False))

    # Convert toc dict to schema
    toc_schema = TableOfContentsSchema(**toc_data)
    book_req = CreateBookRequest(
        title=title,
        api_key=api_key,
        generate_images=generate_images,
        toc=toc_schema
    )
    book_res = v1_create_book(book_req, db)
    book_id = book_res["id"]

    from backend.app.api.v1.jobs import CreateJobRequest
    job_req = CreateJobRequest(book_id=book_id, api_key=api_key)
    job_res = v1_create_job(job_req, db)

    return {"task_id": job_res.id, "book_id": book_id}

@app.post("/api/parse-syllabus")
async def compat_parse_syllabus(req: dict):
    parse_req = ParseSyllabusRequest(text=req.get("text", ""), api_key=req.get("api_key"))
    return await v1_parse_syllabus(parse_req)

@app.get("/api/stream/{task_id}")
async def compat_stream(task_id: str, request: Request, db: Session = Depends(get_db)):
    return await v1_stream_job(task_id, request, db)

@app.get("/api/download/{filename}")
def compat_download(filename: str, db: Session = Depends(get_db)):
    return v1_download_file(filename, db)

# =========================================================================
# Static Frontend Serving
# =========================================================================
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))

if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AI Book Writer v3.0</h1><p>Frontend assets not found.</p>"

@app.get("/{file_name}")
async def serve_frontend_assets(file_name: str):
    file_path = os.path.join(frontend_dir, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        from fastapi.responses import FileResponse
        return FileResponse(file_path)
    return RedirectResponse(url="/")
