import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "AI Book Writer"
    APP_VERSION: str = "3.0.0"
    APP_ENV: str = Field(default="development", description="development | production | test")
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./app.db",
        description="Database connection string (SQLite for local, PostgreSQL for production)"
    )

    # Queue & Cache
    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis connection URL for distributed worker queue"
    )

    # AI Configuration
    AI_MODE: str = Field(default="gemini", description="gemini | mock")
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    TEXT_MODEL: str = "gemini-2.5-flash"
    STRUCTURED_MODEL: str = "gemini-2.5-flash"
    IMAGE_MODEL: str = "imagen-3.0-generate-002"

    # Storage
    STORAGE_PROVIDER: str = Field(default="local", description="local | s3 | r2")
    STORAGE_LOCAL_DIR: str = Field(default="./output")
    STORAGE_BUCKET: Optional[str] = None
    STORAGE_ACCESS_KEY: Optional[str] = None
    STORAGE_SECRET_KEY: Optional[str] = None
    STORAGE_ENDPOINT_URL: Optional[str] = None

    # Pipeline & Concurrency
    MAX_CONCURRENT_JOBS: int = 3
    MAX_BOOK_WORDS: int = 300000
    SECTION_RETRY_LIMIT: int = 3
    AI_TIMEOUT_SECONDS: float = 120.0

    # Security
    CORS_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str = "dev-secret-key-change-in-production-123456789"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
