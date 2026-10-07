import os
import pytest

# Ensure tests run in test environment and use an isolated test database
os.environ["APP_ENV"] = "test"
os.environ["ALLOW_MOCK_PROVIDERS"] = "true"
TEST_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_app.db"))
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"

@pytest.fixture(autouse=True, scope="session")
def cleanup_test_database():
    yield
    for ext in ["", "-shm", "-wal"]:
        fpath = TEST_DB_PATH + ext
        if os.path.exists(fpath):
            try:
                os.remove(fpath)
            except Exception:
                pass
