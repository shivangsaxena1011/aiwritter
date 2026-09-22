from abc import ABC, abstractmethod

class StorageProvider(ABC):
    @abstractmethod
    def save_file(self, source_path: str, storage_key: str) -> str:
        """Persists file and returns accessible URL or resolved path."""
        pass

    @abstractmethod
    def get_file_path(self, storage_key: str) -> str:
        """Returns local filesystem path for serving/downloading."""
        pass
