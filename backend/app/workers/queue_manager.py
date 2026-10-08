import asyncio
import logging
import threading
from typing import Optional, Dict, Set
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import SessionLocal
from backend.app.models import GenerationJob, GenerationEvent
from backend.app.services.ai import get_ai_provider
from backend.app.workers.pipeline import BookGenerationPipeline

logger = logging.getLogger(__name__)

class JobQueueManager:
    """
    Manages job scheduling, concurrency throttling, cancellation, and execution.
    Features:
    - Loop-isolated semaphores preventing cross-event-loop deadlocks.
    - Immediate cancellation flags and task cancellation to eliminate race conditions.
    - Server startup recovery to ensure no jobs remain stuck in non-terminal states.
    - Partial checkpoint recovery allowing retries of FAILED, CANCELLED, or PARTIAL jobs.
    - Optional Redis queue dispatch when REDIS_URL is configured.
    """

    def __init__(self):
        self._loop_semaphores: Dict[asyncio.AbstractEventLoop, asyncio.Semaphore] = {}
        self._lock = threading.Lock()
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self._cancelled_jobs: Set[str] = set()

    def _get_semaphore(self) -> asyncio.Semaphore:
        """Retrieves or creates concurrency semaphore bound strictly to the current running event loop."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop_policy().get_event_loop()

        with self._lock:
            # Clean up closed loops
            self._loop_semaphores = {l: s for l, s in self._loop_semaphores.items() if not l.is_closed()}
            if loop not in self._loop_semaphores:
                self._loop_semaphores[loop] = asyncio.Semaphore(settings.MAX_CONCURRENT_JOBS)
            return self._loop_semaphores[loop]

    def is_job_cancelled(self, job_id: str) -> bool:
        """Checks if job has been flagged for cancellation in memory."""
        return job_id in self._cancelled_jobs

    def enqueue_job(self, job_id: str, api_key: Optional[str] = None):
        """Dispatches job to persistent worker."""
        # Optional Redis queue dispatch if REDIS_URL is configured
        if settings.REDIS_URL:
            try:
                import redis
                r = redis.from_url(settings.REDIS_URL)
                import json
                r.lpush("aiwritter:jobs:queue", json.dumps({"job_id": job_id, "api_key": api_key}))
                logger.info(f"Dispatched job {job_id} to Redis queue.")
                return
            except Exception as e:
                logger.warning(f"Redis queue dispatch failed ({e}). Falling back to in-process worker pool.")

        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(self._worker_wrapper(job_id, api_key))
            with self._lock:
                self.active_tasks[job_id] = task
            task.add_done_callback(lambda t: self._cleanup_task(job_id))
        except RuntimeError:
            # Fallback when running from synchronous context or test runner
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    task = new_loop.create_task(self._worker_wrapper(job_id, api_key))
                    with self._lock:
                        self.active_tasks[job_id] = task
                    try:
                        new_loop.run_until_complete(task)
                    except asyncio.CancelledError:
                        pass
                except Exception as e:
                    logger.warning(f"Worker thread error for job {job_id}: {e}")
                finally:
                    self._cleanup_task(job_id)
                    new_loop.close()

            t = threading.Thread(target=run_in_thread, daemon=True)
            t.start()

    def _cleanup_task(self, job_id: str):
        with self._lock:
            self.active_tasks.pop(job_id, None)
            self._cancelled_jobs.discard(job_id)

    async def _worker_wrapper(self, job_id: str, api_key: Optional[str] = None):
        semaphore = self._get_semaphore()
        async with semaphore:
            db = SessionLocal()
            try:
                # Re-check cancellation before starting
                if self.is_job_cancelled(job_id):
                    logger.info(f"Job {job_id} was cancelled before worker execution began.")
                    return

                ai_provider = get_ai_provider(api_key=api_key)
                pipeline = BookGenerationPipeline(job_id=job_id, db=db, ai_provider=ai_provider)
                await pipeline.execute()
            except asyncio.CancelledError:
                logger.info(f"Worker task cancelled for job {job_id}")
                try:
                    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
                    if job and job.status not in ["COMPLETED", "PARTIAL", "FAILED"]:
                        job.status = "CANCELLED"
                        job.current_stage = "Cancelled"
                        job.updated_at = datetime.now(timezone.utc)
                        db.commit()
                except Exception as e:
                    logger.error(f"Error marking job cancelled in DB: {e}")
            except Exception as e:
                logger.error(f"Worker execution failed for job {job_id}: {e}")
                try:
                    job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
                    if job and job.status not in ["COMPLETED", "PARTIAL", "CANCELLED"]:
                        job.status = "FAILED"
                        job.error = str(e)
                        job.updated_at = datetime.now(timezone.utc)
                        db.commit()
                except Exception as commit_err:
                    logger.error(f"Error updating job failure status in DB: {commit_err}")
            finally:
                db.close()
                self._cleanup_task(job_id)

    def cancel_job(self, job_id: str, db: Session) -> bool:
        """
        Marks job as cancelled in database, flags memory token, and cancels running task.
        Guarantees no race condition: if job has already reached a terminal state, returns False.
        """
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        if not job:
            return False

        terminal_states = {"COMPLETED", "PARTIAL", "FAILED", "CANCELLED"}
        if job.status in terminal_states:
            return False

        # Mark in DB
        job.status = "CANCELLED"
        job.current_stage = "Cancelled"
        job.updated_at = datetime.now(timezone.utc)

        cancel_event = GenerationEvent(
            job_id=job_id,
            event_type="warning",
            message="Generation job cancelled by user.",
            progress=job.progress
        )
        db.add(cancel_event)
        db.commit()

        # Flag cancellation in memory immediately
        with self._lock:
            self._cancelled_jobs.add(job_id)
            task = self.active_tasks.get(job_id)
            if task and not task.done():
                task.cancel()

        return True

    def retry_job(self, job_id: str, db: Session, api_key: Optional[str] = None) -> bool:
        """
        Resets failed, cancelled, or partial job and resumes generation via checkpoint recovery.
        """
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        if not job or job.status not in ["FAILED", "CANCELLED", "PARTIAL"]:
            return False

        with self._lock:
            self._cancelled_jobs.discard(job_id)

        job.status = "RETRYING"
        job.current_stage = "Queued for retry"
        job.error = None
        job.updated_at = datetime.now(timezone.utc)
        db.commit()

        self.enqueue_job(job_id, api_key=api_key)
        return True

    def recover_interrupted_jobs(self, db: Session) -> int:
        """
        Startup recovery: Finds jobs stuck in non-terminal states from a previous server run
        and transitions them to FAILED so they can be retried cleanly.
        """
        non_terminal = ["QUEUED", "PLANNING", "RUNNING", "DRAFTING", "PROCESSING", "RETRYING"]
        stuck_jobs = db.query(GenerationJob).filter(GenerationJob.status.in_(non_terminal)).all()
        recovered_count = 0

        for job in stuck_jobs:
            job.status = "FAILED"
            job.error = "Job interrupted by server restart. You can retry this job to resume from saved section checkpoints."
            job.updated_at = datetime.now(timezone.utc)
            db.add(GenerationEvent(
                job_id=job.id,
                event_type="error",
                message="Job marked failed due to server restart.",
                progress=job.progress
            ))
            recovered_count += 1

        if recovered_count > 0:
            db.commit()
            logger.warning(f"Recovered {recovered_count} interrupted jobs stuck in non-terminal states.")

        return recovered_count

queue_manager = JobQueueManager()
