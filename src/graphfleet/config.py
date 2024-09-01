import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class StorageBackend(str, Enum):
    POSTGRES = "postgres"
    MONGODB = "mongodb"
    LANCEDB = "lancedb"
    LOCAL = "local"
    NEO4J = "neo4j"


class Settings(BaseSettings):
    api_key: str
    api_base: str
    api_version: str
    deployment_name: str
    embedding_model: str
    llm_model: str
    root_path: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    genaiscript_default_model: str = "openai:gpt-4"
    azure_openai_deployment_name: str
    azure_openai_embedding_model: str
    azure_openai_llm_model: str
    azure_openai_endpoint: str
    azure_openai_api_key: str
    api_type: str = "azure_openai_chat"

    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Storage settings
    storage_backend: StorageBackend = StorageBackend.LOCAL
    storage_connection_string: str = "sqlite:///graphfleet.db"  # Default to local SQLite
    parquet_storage_path: str = "./parquet_files"

    # PostgreSQL settings
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "graphfleet"
    postgres_password: str = "graphfleet_password"
    postgres_db: str = "graphfleet_db"

    # MongoDB settings
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "graphfleet_db"

    # LanceDB settings
    lancedb_uri: str = "lancedb://localhost:8000"

    # Neo4j settings
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    @property
    def is_production(self):
        return self.environment == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()