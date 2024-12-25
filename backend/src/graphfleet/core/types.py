"""Types module for GraphFleet."""

from enum import Enum, auto
from typing import Dict, Any, Optional
from pydantic import BaseModel

class QueryType(str, Enum):
    """Types of queries supported by GraphFleet."""
    SEMANTIC = "semantic"
    LOCAL = "local"
    GLOBAL = "global"
    DRIFT = "drift"

class ChunkStrategy(str, Enum):
    """Document chunking strategies."""
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    FIXED = "fixed"
    OVERLAP = "overlap"

class EmbeddingConfig(BaseModel):
    """Configuration for embedding generation."""
    model_name: str = "text-embedding-3-large"
    batch_size: int = 32
    max_length: int = 512
    normalize: bool = True
    options: Dict[str, Any] = {}

class QueryConfig(BaseModel):
    """Configuration for query processing."""
    max_results: int = 10
    similarity_threshold: float = 0.7
    options: Dict[str, Any] = {}

class IndexConfig(BaseModel):
    """Configuration for index creation."""
    chunk_size: int = 1000
    chunk_overlap: int = 200
    chunk_strategy: ChunkStrategy = ChunkStrategy.SENTENCE
    embedding: EmbeddingConfig = EmbeddingConfig()
    options: Dict[str, Any] = {} 