"""
Configuration settings for GraphFleet FastAPI application.
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    project_name: str = "GraphFleet"
    version: str = "1.0.0"
    
    # GraphFleet settings
    project_dir: Path = Path("./data/graphfleet")
    openai_api_key: Optional[str] = None
    
    # CORS settings
    cors_origins: list[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()