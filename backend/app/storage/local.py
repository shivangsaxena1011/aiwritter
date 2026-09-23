import os
import shutil
from backend.app.core.config import settings
from backend.app.storage.base import StorageProvider

class LocalStorageProvider(StorageProvider):
    def __init__(self, base_dir: str = None):
        self.base_dir = os.path.abspath(base_dir or settings.STORAGE_LOCAL_DIR)
        os.makedirs(self.base_dir, exist_ok=True)

    def save_file(self, source_path: str, storage_key: str) -> str:
        dest_path = os.path.join(self.base_dir, storage_key)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        if os.path.abspath(source_path) != os.path.abspath(dest_path):
            shutil.copy2(source_path, dest_path)
        return f"/api/v1/files/{storage_key}"

    def get_file_path(self, storage_key: str) -> str:
        return os.path.join(self.base_dir, storage_key)

    @property
    def local_dir(self) -> str:
        return self.base_dir
