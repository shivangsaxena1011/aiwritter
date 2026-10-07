from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.api.v1.books import router as books_router
from backend.app.api.v1.jobs import router as jobs_router
from backend.app.api.v1.files import router as files_router

api_v1_router = APIRouter(prefix="/v1")

@api_v1_router.get("/health", tags=["System"])
def health_check():
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

@api_v1_router.get("/live", tags=["System"])
def liveness_check():
    """Liveness probe indicating application process is alive."""
    return {"status": "alive", "version": settings.APP_VERSION}

@api_v1_router.get("/ready", tags=["System"])
def readiness_check():
    """Readiness probe verifying database connectivity and storage readiness."""
    from backend.app.core.database import SessionLocal
    from sqlalchemy import text
    db_ok = False
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_ok = True
    except Exception as e:
        db_ok = False

    return {
        "status": "ready" if db_ok else "unready",
        "database": "connected" if db_ok else "disconnected",
        "storage": settings.STORAGE_PROVIDER
    }

api_v1_router.include_router(books_router)
api_v1_router.include_router(jobs_router)
api_v1_router.include_router(files_router)
