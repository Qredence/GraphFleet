from pydantic_settings import BaseSettings
from enum import Enum

class StorageBackend(str, Enum):
    LOCAL = "local"
    S3 = "s3"
    AZURE = "azure"

class Settings(BaseSettings):
    API_VERSION: str = "0.1.0"
    ALLOWED_ORIGINS: list[str] = ["*"]  # Update this with specific origins in production
    STORAGE_BACKEND: StorageBackend = StorageBackend.LOCAL
    LOG_LEVEL: str = "INFO"
    # Add other configuration settings here

settings = Settings()