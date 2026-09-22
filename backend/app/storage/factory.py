from backend.app.core.config import settings
from backend.app.storage.base import StorageProvider
from backend.app.storage.local import LocalStorageProvider

def get_storage_provider() -> StorageProvider:
    # Defaults to LocalStorageProvider
    return LocalStorageProvider()
