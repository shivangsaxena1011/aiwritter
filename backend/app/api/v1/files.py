import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import validate_safe_filename
from backend.app.models import GeneratedAsset
from backend.app.storage import get_storage_provider

router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/{filename}")
def download_file(filename: str, db: Session = Depends(get_db)):
    """
    Safely downloads a generated file by verified filename or database storage key.
    Enforces strict path traversal defenses.
    """
    safe_filename = validate_safe_filename(filename)
    storage = get_storage_provider()
    local_path = storage.get_file_path(safe_filename)

    if not os.path.exists(local_path):
        # Look in database asset storage keys
        asset = db.query(GeneratedAsset).filter(GeneratedAsset.storage_key == safe_filename).first()
        if asset:
            local_path = storage.get_file_path(asset.storage_key)

    if not os.path.exists(local_path):
        raise HTTPException(status_code=404, detail="File not found")

    media_type = "application/octet-stream"
    if safe_filename.endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif safe_filename.endswith(".pdf"):
        media_type = "application/pdf"
    elif safe_filename.endswith(".png"):
        media_type = "image/png"

    return FileResponse(
        path=local_path,
        media_type=media_type,
        filename=safe_filename,
        headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'}
    )
