import json
import uuid
import asyncio
from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models import Book, GenerationJob, GenerationEvent, GeneratedAsset
from backend.app.schemas import JobResponse, EventResponse
from backend.app.workers.queue_manager import queue_manager

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class CreateJobRequest(BaseModel):
    book_id: str
    api_key: Optional[str] = None

@router.post("", response_model=JobResponse, status_code=201)
def create_generation_job(req: CreateJobRequest, db: Session = Depends(get_db)):
    """Creates a durable generation job and dispatches it to the background queue."""
    book = db.query(Book).filter(Book.id == req.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    job = GenerationJob(
        book_id=book.id,
        status="QUEUED",
        progress=0.0,
        current_stage="Queued in background worker",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Dispatch to worker queue
    queue_manager.enqueue_job(job.id, api_key=req.api_key)

    return _format_job_response(job, db)

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    """Fetches job status, progress, and download link."""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _format_job_response(job, db)

@router.post("/{job_id}/cancel")
def cancel_job(job_id: str, db: Session = Depends(get_db)):
    """Cancels an active generation job."""
    success = queue_manager.cancel_job(job_id, db)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel job in current state")
    return {"status": "CANCELLED", "job_id": job_id}

@router.post("/{job_id}/retry")
def retry_job(job_id: str, req: Optional[CreateJobRequest] = None, db: Session = Depends(get_db)):
    """Retries a failed or cancelled job using partial recovery."""
    api_key = req.api_key if req else None
    success = queue_manager.retry_job(job_id, db, api_key=api_key)
    if not success:
        raise HTTPException(status_code=400, detail="Job cannot be retried from its current state")
    return {"status": "RETRYING", "job_id": job_id}

@router.get("/{job_id}/events", response_model=List[EventResponse])
def get_job_events(job_id: str, after: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """
    Returns persistent events for reconnect recovery.
    Supports ?after=<iso_timestamp> to only fetch unseen events.
    """
    query = db.query(GenerationEvent).filter(GenerationEvent.job_id == job_id)
    if after:
        try:
            after_dt = datetime.fromisoformat(after.replace("Z", "+00:00"))
            query = query.filter(GenerationEvent.created_at > after_dt)
        except Exception:
            pass

    events = query.order_by(GenerationEvent.created_at.asc()).all()
    return events

@router.get("/{job_id}/stream")
async def stream_job_events(job_id: str, request: Request, db: Session = Depends(get_db)):
    """Server-Sent Events (SSE) streaming endpoint backed by database with keepalives."""
    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator():
        last_event_time = None
        while True:
            if await request.is_disconnected():
                break

            # Refresh session to see latest commits from worker
            try:
                db.commit()
            except Exception:
                pass

            # Poll events since last timestamp
            ev_query = db.query(GenerationEvent).filter(GenerationEvent.job_id == job_id)
            if last_event_time:
                ev_query = ev_query.filter(GenerationEvent.created_at > last_event_time)
            new_events = ev_query.order_by(GenerationEvent.created_at.asc()).all()

            for ev in new_events:
                last_event_time = ev.created_at
                payload = {
                    "event_id": ev.id,
                    "job_id": ev.job_id,
                    "type": ev.event_type,
                    "message": ev.message,
                    "progress": ev.progress,
                    "timestamp": ev.created_at.isoformat(),
                    "created_at": ev.created_at.isoformat(),
                    "metadata": ev.event_metadata
                }
                yield f"data: {json.dumps(payload)}\n\n"

            # Check job status
            db.expire(job)
            current_job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
            if current_job and current_job.status in ["COMPLETED", "PARTIAL", "FAILED", "CANCELLED"]:
                asset = db.query(GeneratedAsset).filter(
                    GeneratedAsset.job_id == job_id,
                    GeneratedAsset.type == "docx"
                ).first()
                final_payload = {
                    "event_id": str(uuid.uuid4()),
                    "job_id": job_id,
                    "type": "complete" if current_job.status in ["COMPLETED", "PARTIAL"] else "error",
                    "status": current_job.status,
                    "message": current_job.error or f"Pipeline finished ({current_job.status})",
                    "progress": current_job.progress,
                    "download_url": asset.url if asset else None
                }
                yield f"data: {json.dumps(final_payload)}\n\n"
                break

            # Keepalive ping every 2 seconds
            yield ": keepalive\n\n"
            await asyncio.sleep(2)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

def _format_job_response(job: GenerationJob, db: Session) -> JobResponse:
    asset = db.query(GeneratedAsset).filter(
        GeneratedAsset.job_id == job.id,
        GeneratedAsset.type == "docx"
    ).first()

    return JobResponse(
        id=job.id,
        book_id=job.book_id,
        status=job.status,
        progress=job.progress or 0.0,
        current_stage=job.current_stage or "Initializing",
        current_item=job.current_item,
        error=job.error,
        started_at=job.started_at,
        completed_at=job.completed_at,
        created_at=job.created_at,
        updated_at=job.updated_at,
        download_url=asset.url if asset else None
    )
