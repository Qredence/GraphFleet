"""
GraphFleet Configuration Module

This module handles configuration settings for the GraphFleet application.
It loads settings from environment variables and configuration files.
"""

from typing import Dict, Any, Optional
from pydantic import BaseSettings, Field
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "GraphFleet"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A powerful graph-based knowledge management system"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # GraphFleet Core Settings
    DEFAULT_CHUNK_SIZE: int = Field(1000, ge=100, le=5000)
    DEFAULT_CHUNK_OVERLAP: int = Field(200, ge=0, le=1000)
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-large"
    DEFAULT_QUERY_MODEL: str = "gpt-4"
    
    # Database Settings
    DATABASE_URL: Optional[str] = None
    
    # Cache Settings
    REDIS_URL: Optional[str] = None
    CACHE_TTL: int = 3600  # 1 hour
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security Settings
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Default Query Settings
    DEFAULT_QUERY_TYPE: str = "semantic"
    MAX_BATCH_SIZE: int = 100
    DEFAULT_SIMILARITY_THRESHOLD: float = Field(0.7, ge=0.0, le=1.0)
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

class QueryConfig:
    """Configuration for different query types."""
    
    SEMANTIC: Dict[str, Any] = {
        "max_results": 10,
        "similarity_threshold": 0.7,
        "rerank": True
    }
    
    LOCAL: Dict[str, Any] = {
        "max_hops": 2,
        "max_nodes": 100,
        "prune_threshold": 0.5
    }
    
    GLOBAL: Dict[str, Any] = {
        "community_level": 1,
        "min_community_size": 5,
        "merge_threshold": 0.3
    }
    
    DRIFT: Dict[str, Any] = {
        "time_window": "1d",
        "min_change": 0.1,
        "smoothing": 0.2
    }

class IndexConfig:
    """Configuration for document indexing."""
    
    CHUNK_STRATEGIES = {
        "sentence": {
            "min_length": 100,
            "max_length": 1000,
            "overlap": 0.2
        },
        "fixed": {
            "chunk_size": 1000,
            "overlap": 200
        },
        "semantic": {
            "min_semantic_size": 0.8,
            "max_semantic_size": 1.2,
            "overlap_strategy": "adaptive"
        }
    }
    
    EMBEDDING_CONFIGS = {
        "text-embedding-3-large": {
            "dimension": 3072,
            "normalize": True,
            "batch_size": 32
        },
        "text-embedding-3-small": {
            "dimension": 1536,
            "normalize": True,
            "batch_size": 64
        }
    }

@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings.
    
    Returns:
        Settings object containing application configuration
    """
    return Settings()

def get_query_config(query_type: str) -> Dict[str, Any]:
    """Get configuration for a specific query type.
    
    Args:
        query_type: Type of query (semantic, local, global, drift)
        
    Returns:
        Dict containing query configuration
        
    Raises:
        ValueError: If query_type is invalid
    """
    config_map = {
        "semantic": QueryConfig.SEMANTIC,
        "local": QueryConfig.LOCAL,
        "global": QueryConfig.GLOBAL,
        "drift": QueryConfig.DRIFT
    }
    
    if query_type not in config_map:
        raise ValueError(f"Invalid query type: {query_type}")
    
    return config_map[query_type]

def get_index_config(
    chunk_strategy: str = "sentence",
    embedding_model: str = "text-embedding-3-large"
) -> Dict[str, Any]:
    """Get configuration for document indexing.
    
    Args:
        chunk_strategy: Strategy for chunking documents
        embedding_model: Model for generating embeddings
        
    Returns:
        Dict containing indexing configuration
        
    Raises:
        ValueError: If chunk_strategy or embedding_model is invalid
    """
    if chunk_strategy not in IndexConfig.CHUNK_STRATEGIES:
        raise ValueError(f"Invalid chunk strategy: {chunk_strategy}")
    
    if embedding_model not in IndexConfig.EMBEDDING_CONFIGS:
        raise ValueError(f"Invalid embedding model: {embedding_model}")
    
    return {
        "chunk_config": IndexConfig.CHUNK_STRATEGIES[chunk_strategy],
        "embedding_config": IndexConfig.EMBEDDING_CONFIGS[embedding_model]
    }
