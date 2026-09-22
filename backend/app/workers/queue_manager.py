import asyncio
import logging
from typing import Optional, Dict
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import SessionLocal
from backend.app.models import GenerationJob
from backend.app.services.ai import get_ai_provider
from backend.app.workers.pipeline import BookGenerationPipeline

logger = logging.getLogger(__name__)

class JobQueueManager:
    """
    Manages job scheduling, concurrency throttling, and execution.
    Supports in-process async worker pool (Mode A) and Redis queue dispatch (Mode B).
    """

    def __init__(self):
        self._semaphore = None
        self.active_tasks: Dict[str, asyncio.Task] = {}

    def _get_semaphore(self):
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_JOBS)
        return self._semaphore

    def enqueue_job(self, job_id: str, api_key: Optional[str] = None):
        """Dispatches job to persistent worker."""
        try:
            loop = asyncio.get_running_loop()
            task = loop.create_task(self._worker_wrapper(job_id, api_key))
            self.active_tasks[job_id] = task
            task.add_done_callback(lambda t: self.active_tasks.pop(job_id, None))
        except RuntimeError:
            # Fallback when running from synchronous context or test runner
            import threading
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    new_loop.run_until_complete(self._worker_wrapper(job_id, api_key))
                finally:
                    new_loop.close()

            t = threading.Thread(target=run_in_thread, daemon=True)
            t.start()

    async def _worker_wrapper(self, job_id: str, api_key: Optional[str] = None):
        async with self._get_semaphore():
            db = SessionLocal()
            try:
                ai_provider = get_ai_provider(api_key=api_key)
                pipeline = BookGenerationPipeline(job_id=job_id, db=db, ai_provider=ai_provider)
                await pipeline.execute()
            except Exception as e:
                logger.error(f"Worker execution failed for job {job_id}: {e}")
            finally:
                db.close()

    def cancel_job(self, job_id: str, db: Session) -> bool:
        """Marks job as cancelled in database and flags task."""
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        if not job:
            return False

        if job.status in ["COMPLETED", "FAILED", "CANCELLED"]:
            return False

        job.status = "CANCELLED"
        job.updated_at = datetime.now(timezone.utc)
        db.commit()

        # If running in local active tasks, cancel async task
        task = self.active_tasks.get(job_id)
        if task and not task.done():
            task.cancel()

        return True

    def retry_job(self, job_id: str, db: Session, api_key: Optional[str] = None) -> bool:
        """Resets failed or cancelled job and resumes generation via partial recovery."""
        job = db.query(GenerationJob).filter(GenerationJob.id == job_id).first()
        if not job or job.status not in ["FAILED", "CANCELLED"]:
            return False

        job.status = "RETRYING"
        job.error = None
        job.updated_at = datetime.now(timezone.utc)
        db.commit()

        self.enqueue_job(job_id, api_key=api_key)
        return True

queue_manager = JobQueueManager()
