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

    # Production environment security assertions
    if settings.APP_ENV == "production":
        if settings.SECRET_KEY == "dev-secret-key-change-in-production-123456789":
            logger.warning("CRITICAL SECURITY ADVISORY: Default SECRET_KEY in production. Set a random SECRET_KEY in .env.")
        if settings.ALLOW_MOCK_PROVIDERS:
            raise RuntimeError("FATAL: ALLOW_MOCK_PROVIDERS is True in production mode.")
        if settings.AI_MODE == "mock":
            raise RuntimeError("FATAL: AI_MODE='mock' is prohibited in production mode.")

    init_db()
    os.makedirs(settings.STORAGE_LOCAL_DIR, exist_ok=True)

    # Recover any interrupted jobs left in non-terminal states from prior crashes
    from backend.app.core.database import SessionLocal
    from backend.app.workers.queue_manager import queue_manager
    try:
        with SessionLocal() as recovery_db:
            queue_manager.recover_interrupted_jobs(recovery_db)
    except Exception as rec_err:
        logger.error(f"Failed to run startup job recovery: {rec_err}")

    # Verify write permissions to storage directory
    test_probe = os.path.join(settings.STORAGE_LOCAL_DIR, ".write_probe")
    try:
        with open(test_probe, "w") as f:
            f.write("ok")
        os.remove(test_probe)
    except Exception as e:
        logger.error(f"Failed to verify storage directory write permissions: {e}")
        if settings.APP_ENV == "production":
            raise RuntimeError(f"Storage directory not writable: {e}")

    yield
    logger.info("Shutting down AI Book Writer...")

app = FastAPI(
    title="AIWritter — Agentic Academic Book Publishing Engine",
    version=settings.APP_VERSION,
    description="Production-grade agentic academic textbook publishing engine with multi-stage agents, derivations, educational research, durable jobs, and native Word export.",
    lifespan=lifespan
)

# CORS Security: wildcard '*' cannot be combined with allow_credentials=True in standard CORS
cors_origins = settings.CORS_ORIGINS
allow_creds = True
if "*" in cors_origins or cors_origins == ["*"]:
    allow_creds = False
    if settings.APP_ENV == "production":
        logger.warning("CORS wildcard origin configured in production without credentials.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_creds,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Root Health, Liveness, and Readiness probes
@app.get("/health", tags=["System"])
def root_health():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "env": settings.APP_ENV,
        "ai_mode": settings.AI_MODE,
        "text_model": settings.effective_text_model,
        "image_model": settings.effective_image_model,
        "storage": settings.STORAGE_PROVIDER
    }

@app.get("/live", tags=["System"])
def root_live():
    return {"status": "alive", "version": settings.APP_VERSION}

@app.get("/ready", tags=["System"])
def root_ready(db: Session = Depends(get_db)):
    from sqlalchemy import text
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    return {
        "status": "ready" if db_ok else "unready",
        "database": "connected" if db_ok else "disconnected",
        "storage": settings.STORAGE_PROVIDER
    }

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
    from backend.app.core.security import validate_safe_path
    try:
        file_path = validate_safe_path(frontend_dir, file_name)
    except Exception:
        return RedirectResponse(url="/")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        from fastapi.responses import FileResponse
        return FileResponse(file_path)
    return RedirectResponse(url="/")
