import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator, field_validator
import json

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
    AI_PROVIDER: str = Field(default="gemini", description="gemini | mock")
    ALLOW_MOCK_PROVIDERS: bool = Field(
        default=False,
        description="Whether mock AI or research providers are permitted. Strictly forbidden in production."
    )
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_BACKUP_KEYS: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_TEXT_MODEL: Optional[str] = None
    GEMINI_IMAGE_MODEL: Optional[str] = None
    TEXT_MODEL: str = "gemini-3.8-flash"
    STRUCTURED_MODEL: str = "gemini-3.8-flash"
    IMAGE_MODEL: str = "imagen-3.0-generate-002"

    @property
    def effective_text_model(self) -> str:
        return self.GEMINI_TEXT_MODEL or self.TEXT_MODEL

    @property
    def effective_image_model(self) -> str:
        return self.GEMINI_IMAGE_MODEL or self.IMAGE_MODEL

    @property
    def all_gemini_keys(self) -> List[str]:
        keys = []
        if self.GEMINI_API_KEY:
            for k in self.GEMINI_API_KEY.replace("\n", ",").split(","):
                k = k.strip()
                if k and k not in keys:
                    keys.append(k)
        if self.GEMINI_BACKUP_KEYS:
            for k in self.GEMINI_BACKUP_KEYS.replace("\n", ",").split(","):
                k = k.strip()
                if k and k not in keys:
                    keys.append(k)
        return keys

    # Storage
    STORAGE_PROVIDER: str = Field(default="local", description="local | s3 | r2")
    STORAGE_TYPE: Optional[str] = Field(default=None, description="Alias for STORAGE_PROVIDER")
    STORAGE_LOCAL_DIR: str = Field(default="./output")
    STORAGE_BUCKET: Optional[str] = None
    STORAGE_ACCESS_KEY: Optional[str] = None
    STORAGE_SECRET_KEY: Optional[str] = None
    STORAGE_ENDPOINT_URL: Optional[str] = None

    # Pipeline & Concurrency
    MAX_CONCURRENT_JOBS: int = 3
    MAX_BOOK_WORDS: int = 300000
    SECTION_RETRY_LIMIT: int = 3
    MAX_CONTENT_REVIEW_RETRIES: int = 2
    AI_TIMEOUT_SECONDS: float = 120.0

    # Security & Auth
    CORS_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str = "dev-secret-key-change-in-production-123456789"
    AUTH_REQUIRED: bool = Field(default=False, description="Whether private endpoints require authentication token")
    API_AUTH_SECRET: Optional[str] = Field(default=None, description="Shared bearer token or API key for private endpoint authentication")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    EXPENSIVE_ENDPOINT_LIMIT_PER_MINUTE: int = 20

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    @model_validator(mode="after")
    def validate_production_guards(self) -> "Settings":
        if self.STORAGE_TYPE and not self.STORAGE_PROVIDER:
            self.STORAGE_PROVIDER = self.STORAGE_TYPE
        elif self.STORAGE_TYPE and self.STORAGE_PROVIDER == "local":
            self.STORAGE_PROVIDER = self.STORAGE_TYPE

        if self.APP_ENV == "production":
            if self.ALLOW_MOCK_PROVIDERS:
                raise ValueError("ALLOW_MOCK_PROVIDERS cannot be True in production environment.")
            if self.AI_MODE == "mock":
                raise ValueError("AI_MODE='mock' is strictly prohibited in production environment.")
            if not self.API_AUTH_SECRET and self.AUTH_REQUIRED:
                raise ValueError("API_AUTH_SECRET must be configured when AUTH_REQUIRED=True in production.")
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
