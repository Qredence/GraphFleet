from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
from functools import lru_cache
from datetime import timedelta
from pathlib import Path
from typing import List

from passlib.context import CryptContext


class Settings(BaseSettings):
    PROJECT_NAME: str = "GraphFleet"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER", ""),
            path=f"/{values.get('POSTGRES_DB', '')}",
        )

    # GraphRAG settings
    GRAPHRAG_INPUT_DIR: str = "data"
    GRAPHRAG_COMMUNITY_LEVEL: int = 2
    GRAPHRAG_MAX_CONCURRENT_REQUESTS: int = 1

    # LLM settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 1000
    OPENAI_TEMPERATURE: float = 0.7

    # Embedding settings
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Authentication settings
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    admin_username: str
    admin_password_hash: str

    # Security settings
    allowed_hosts: List[str] = ["*"]
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    reload: bool = True

    # Logging settings
    log_level: str = "INFO"

    class Config:
        case_sensitive = True
        env_file = ".env"

    def get_jwt_settings(self) -> dict:
        """Get JWT settings."""
        return {
            "secret_key": self.jwt_secret_key,
            "algorithm": self.jwt_algorithm,
            "expire_minutes": self.access_token_expire_minutes,
        }

    def get_cors_settings(self) -> dict:
        """Get CORS settings."""
        return {
            "allow_origins": self.cors_origins,
            "allow_credentials": self.cors_allow_credentials,
            "allow_methods": self.cors_allow_methods,
            "allow_headers": self.cors_allow_headers,
        }

    def get_server_settings(self) -> dict:
        """Get server settings."""
        return {
            "host": self.host,
            "port": self.port,
            "workers": self.workers,
            "reload": self.reload,
        }


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Get password hash."""
    return pwd_context.hash(password)


settings = get_settings()
