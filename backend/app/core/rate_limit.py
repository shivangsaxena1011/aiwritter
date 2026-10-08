import time
import threading
from typing import Dict, List, Optional
from fastapi import Request, HTTPException
from backend.app.core.config import settings

class InMemoryRateLimiter:
    """
    Thread-safe in-memory sliding window rate limiter.
    Limits requests per client IP across configurable time windows.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._requests: Dict[str, List[float]] = {}
        self._last_cleanup = time.time()

    def _cleanup(self, now: float):
        if now - self._last_cleanup > 300:  # clean up every 5 minutes
            for key in list(self._requests.keys()):
                self._requests[key] = [t for t in self._requests[key] if now - t < 3600]
                if not self._requests[key]:
                    del self._requests[key]
            self._last_cleanup = now

    def check_rate_limit(self, key: str, max_requests: int, window_seconds: float) -> Optional[int]:
        """
        Checks whether key exceeds rate limit.
        Returns None if permitted, or retry_after in seconds if exceeded.
        """
        now = time.time()
        with self._lock:
            self._cleanup(now)
            cutoff = now - window_seconds
            timestamps = [t for t in self._requests.get(key, []) if t > cutoff]

            if len(timestamps) >= max_requests:
                oldest = timestamps[0]
                retry_after = max(1, int(oldest + window_seconds - now))
                return retry_after

            timestamps.append(now)
            self._requests[key] = timestamps
            return None

rate_limiter = InMemoryRateLimiter()

def rate_limit_dependency(max_requests: int = 60, window_seconds: float = 60.0):
    """Factory creating a FastAPI route dependency for rate limiting."""
    async def _dependency(request: Request):
        if not settings.RATE_LIMIT_ENABLED:
            return

        client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "127.0.0.1")
        if client_ip and "," in client_ip:
            client_ip = client_ip.split(",")[0].strip()

        key = f"{client_ip}:{request.url.path}"
        retry_after = rate_limiter.check_rate_limit(key, max_requests, window_seconds)
        if retry_after is not None:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: maximum {max_requests} requests per {int(window_seconds)}s. Try again in {retry_after}s.",
                headers={"Retry-After": str(retry_after)}
            )

    return _dependency
