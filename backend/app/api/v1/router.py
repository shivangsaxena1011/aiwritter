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
        "text_model": settings.TEXT_MODEL,
        "image_model": settings.IMAGE_MODEL
    }

api_v1_router.include_router(books_router)
api_v1_router.include_router(jobs_router)
api_v1_router.include_router(files_router)
