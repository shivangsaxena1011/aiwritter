import os
import logging
from typing import Optional
from backend.app.core.config import settings
from backend.app.storage.base import StorageProvider

logger = logging.getLogger(__name__)

class S3StorageProvider(StorageProvider):
    """
    Production-grade S3 / Cloudflare R2 Storage Provider.
    Implements durable cloud object storage with local cache for fast retrieval.
    """

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        local_cache_dir: Optional[str] = None
    ):
        self.bucket = bucket_name or settings.STORAGE_BUCKET or "aiwritter-artifacts"
        self.access_key = access_key or settings.STORAGE_ACCESS_KEY
        self.secret_key = secret_key or settings.STORAGE_SECRET_KEY
        self.endpoint_url = endpoint_url or settings.STORAGE_ENDPOINT_URL
        self.local_cache_dir = os.path.abspath(local_cache_dir or settings.STORAGE_LOCAL_DIR)
        os.makedirs(self.local_cache_dir, exist_ok=True)
        self._s3_client = None

    @property
    def s3_client(self):
        if self._s3_client is None:
            try:
                import boto3
                kwargs = {
                    "aws_access_key_id": self.access_key,
                    "aws_secret_access_key": self.secret_key,
                }
                if self.endpoint_url:
                    kwargs["endpoint_url"] = self.endpoint_url
                self._s3_client = boto3.client("s3", **kwargs)
            except ImportError:
                logger.warning("boto3 is not installed. S3StorageProvider will operate in cache-only fallback mode.")
                self._s3_client = None
        return self._s3_client

    def save_file(self, source_path: str, storage_key: str) -> str:
        from backend.app.core.security import validate_safe_path
        cache_dest = validate_safe_path(self.local_cache_dir, storage_key)
        os.makedirs(os.path.dirname(cache_dest), exist_ok=True)
        if os.path.abspath(source_path) != os.path.abspath(cache_dest):
            import shutil
            shutil.copy2(source_path, cache_dest)

        client = self.s3_client
        if client:
            import time
            last_err = None
            retries = 3
            backoff = 1.0
            for attempt in range(retries):
                try:
                    client.upload_file(source_path, self.bucket, storage_key)
                    if self.endpoint_url:
                        return f"{self.endpoint_url.rstrip('/')}/{self.bucket}/{storage_key}"
                    return f"https://{self.bucket}.s3.amazonaws.com/{storage_key}"
                except Exception as e:
                    last_err = e
                    logger.warning(f"S3 upload attempt {attempt+1}/{retries} failed for {storage_key}: {e}")
                    if attempt < retries - 1:
                        time.sleep(backoff)
                        backoff *= 2.0

            logger.error(f"All {retries} S3 upload attempts failed for {storage_key} to bucket {self.bucket}: {last_err}")
            if settings.APP_ENV == "production" and settings.STORAGE_PROVIDER in ("s3", "r2"):
                raise RuntimeError(f"Cloud storage upload failed for {storage_key}: {last_err}")

        return f"/api/v1/files/{storage_key}"

    def get_file_path(self, storage_key: str) -> str:
        from backend.app.core.security import validate_safe_path
        cache_path = validate_safe_path(self.local_cache_dir, storage_key)
        if os.path.exists(cache_path):
            return cache_path

        client = self.s3_client
        if client:
            import time
            retries = 3
            backoff = 1.0
            for attempt in range(retries):
                try:
                    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
                    client.download_file(self.bucket, storage_key, cache_path)
                    return cache_path
                except Exception as e:
                    logger.warning(f"S3 download attempt {attempt+1}/{retries} failed for {storage_key}: {e}")
                    if attempt < retries - 1:
                        time.sleep(backoff)
                        backoff *= 2.0

        return cache_path

    @property
    def local_dir(self) -> str:
        return self.local_cache_dir
