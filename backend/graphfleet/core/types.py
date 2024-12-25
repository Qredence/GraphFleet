"""
GraphFleet Core Types

This module defines the core types and configurations used throughout GraphFleet.
"""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel

class IndexType(str, Enum):
    FAISS = "faiss"
    LANCEDB = "lancedb"
    ANNOY = "annoy"

class RetrievalType(str, Enum):
    SIMILARITY = "similarity"
    HYBRID = "hybrid"
    SEMANTIC = "semantic"

class QueryType(str, Enum):
    RAG = "rag"
    DIRECT = "direct"
    GRAPH = "graph"

class Document(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any] = {}
    embedding: Optional[List[float]] = None

class Chunk(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = {}
    embedding: Optional[List[float]] = None
    document_id: str

class IndexConfig(BaseModel):
    index_type: IndexType = IndexType.LANCEDB
    dimension: int = 1536
    metric: str = "cosine"
    additional_config: Dict[str, Any] = {}

class QueryConfig(BaseModel):
    query_type: QueryType = QueryType.RAG
    retrieval_type: RetrievalType = RetrievalType.HYBRID
    max_results: int = 5
    threshold: float = 0.7
    context_window: int = 2000
    max_tokens: int = 500
    temperature: float = 0.7
    additional_config: Dict[str, Any] = {}

class QueryResult(BaseModel):
    result: str
    confidence: float = 0.0
    sources: List[Document] = []
    metadata: Dict[str, Any] = {}
