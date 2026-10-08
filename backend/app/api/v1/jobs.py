import json
import uuid
import asyncio
from datetime import datetime, timezone
from typing import Optional, List, Set, Tuple, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from backend.app.core.database import get_db, SessionLocal
from backend.app.core.security import verify_api_auth
from backend.app.core.rate_limit import rate_limit_dependency
from backend.app.models import Book, GenerationJob, GenerationEvent, GeneratedAsset
from backend.app.schemas import JobResponse, EventResponse
from backend.app.workers.queue_manager import queue_manager

router = APIRouter(prefix="/jobs", tags=["Jobs"])

class CreateJobRequest(BaseModel):
    book_id: str = Field(..., min_length=1)
    api_key: Optional[str] = None

    @field_validator("book_id")
    @classmethod
    def validate_book_id(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("book_id cannot be blank or whitespace-only")
        return s

@router.post(
    "",
    response_model=JobResponse,
    status_code=201,
    dependencies=[Depends(rate_limit_dependency(max_requests=20, window_seconds=60.0))]
)
def create_generation_job(
    req: CreateJobRequest,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Creates a durable generation job and dispatches it to the background queue."""
    verify_api_auth(authorization=authorization, x_api_key=x_api_key)

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
def cancel_job(
    job_id: str,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Cancels an active generation job."""
    verify_api_auth(authorization=authorization, x_api_key=x_api_key)
    success = queue_manager.cancel_job(job_id, db)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot cancel job in current state")
    return {"status": "CANCELLED", "job_id": job_id}

@router.post("/{job_id}/retry")
def retry_job(
    job_id: str,
    req: Optional[CreateJobRequest] = None,
    authorization: Optional[str] = Header(None),
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Retries a failed, cancelled, or partial job using partial recovery."""
    verify_api_auth(authorization=authorization, x_api_key=x_api_key)
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

def _fetch_poll_update(job_id: str, last_time: Optional[datetime], seen_ids: Set[str]) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Runs synchronous DB polling inside a thread-safe short-lived session."""
    with SessionLocal() as db:
        ev_query = db.query(GenerationEvent).filter(GenerationEvent.job_id == job_id)
        if last_time:
            ev_query = ev_query.filter(GenerationEvent.created_at >= last_time)

        raw_events = ev_query.order_by(GenerationEvent.created_at.asc()).all()
        new_events = []
        for ev in raw_events:
            if ev.id in seen_ids:
                continue
            seen_ids.add(ev.id)
            new_events.append({
                "event_id": ev.id,
                "job_id": ev.job_id,
                "type": ev.event_type,
                "message": ev.message,
                "progress": ev.progress,
                "timestamp": ev.created_at.isoformat(),
                "created_at": ev.created_at.isoformat(),
                "metadata": ev.event_metadata or {}
            })

        # Check job terminal status
        current_job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        terminal_data = None
        if current_job and current_job.status in ["COMPLETED", "PARTIAL", "FAILED", "CANCELLED"]:
            asset = db.query(GeneratedAsset).filter(
                GeneratedAsset.job_id == job_id,
                GeneratedAsset.type == "docx"
            ).first()
            terminal_data = {
                "event_id": str(uuid.uuid4()),
                "job_id": job_id,
                "type": "complete" if current_job.status in ["COMPLETED", "PARTIAL"] else "error",
                "status": current_job.status,
                "message": current_job.error or f"Pipeline finished ({current_job.status})",
                "progress": current_job.progress,
                "download_url": asset.url if asset else None
            }

        return new_events, terminal_data

@router.get("/{job_id}/stream")
async def stream_job_events(job_id: str, request: Request):
    """
    Server-Sent Events (SSE) streaming endpoint backed by database with keepalives.
    Uses short-lived thread-pool DB sessions to prevent connection pool exhaustion,
    and deduplicated event tracking to prevent event loss or duplicate emissions.
    """
    # Initial existence check using short-lived session
    with SessionLocal() as db:
        job_exists = db.query(GenerationJob.id).filter(GenerationJob.id == job_id).first()
    if not job_exists:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator():
        last_event_time: Optional[datetime] = None
        seen_event_ids: Set[str] = set()

        while True:
            if await request.is_disconnected():
                break

            # Poll via thread-safe short-lived session without holding connection pool
            try:
                new_events, terminal_data = await asyncio.to_thread(
                    _fetch_poll_update, job_id, last_event_time, seen_event_ids
                )
            except Exception as poll_err:
                yield f": poll_error {str(poll_err)}\n\n"
                await asyncio.sleep(2)
                continue

            for payload in new_events:
                try:
                    last_event_time = datetime.fromisoformat(payload["timestamp"])
                except Exception:
                    pass
                yield f"data: {json.dumps(payload)}\n\n"

            # Prune seen_event_ids to prevent memory growth if stream runs for very long
            if len(seen_event_ids) > 10000:
                seen_event_ids.clear()

            if terminal_data:
                yield f"data: {json.dumps(terminal_data)}\n\n"
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
