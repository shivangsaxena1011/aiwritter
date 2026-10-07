from backend.app.core.config import settings
from backend.app.storage.base import StorageProvider
from backend.app.storage.local import LocalStorageProvider

def get_storage_provider() -> StorageProvider:
    if settings.STORAGE_PROVIDER in ("s3", "r2"):
        from backend.app.storage.s3 import S3StorageProvider
        return S3StorageProvider()
    return LocalStorageProvider()

