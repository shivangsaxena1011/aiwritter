import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)

if settings.DATABASE_URL.startswith("sqlite"):
    from sqlalchemy import event

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA busy_timeout=30000")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes database tables."""
    try:
        # Import models so Base metadata is populated
        import backend.app.models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
