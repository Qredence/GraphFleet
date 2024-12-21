"""
Type definitions for GraphFleet.
"""

from enum import Enum
from typing import TypeVar, Dict, List, Optional, Union, Any
from pydantic import BaseModel

# Type variables
T = TypeVar('T')
DocumentType = TypeVar('DocumentType', bound='Document')
ChunkType = TypeVar('ChunkType', bound='Chunk')

class QueryType(str, Enum):
    """Types of queries supported by GraphFleet."""
    STANDARD = "standard"
    LOCAL = "local"
    GLOBAL = "global"
    DRIFT = "drift"
    DYNAMIC = "dynamic"

class IndexType(str, Enum):
    """Types of indexes supported by GraphFleet."""
    LANCEDB = "lancedb"
    FAISS = "faiss"
    MILVUS = "milvus"

class RetrievalType(str, Enum):
    """Types of retrieval methods."""
    VECTOR = "vector"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    MULTIHOP = "multihop"

class Document(BaseModel):
    """Base document model."""
    id: str
    content: str
    metadata: Dict[str, Any] = {}
    embedding: Optional[List[float]] = None

class Chunk(BaseModel):
    """Document chunk model."""
    id: str
    content: str
    document_id: str
    start_idx: int
    end_idx: int
    metadata: Dict[str, Any] = {}
    embedding: Optional[List[float]] = None

class QueryResult(BaseModel):
    """Query result model."""
    result: str
    confidence: float
    sources: List[Document]
    metadata: Dict[str, Any] = {}

class IndexConfig(BaseModel):
    """Index configuration model."""
    index_type: IndexType
    dimension: int = 1536
    metric: str = "cosine"
    additional_config: Dict[str, Any] = {}

class QueryConfig(BaseModel):
    """Query configuration model."""
    query_type: QueryType = QueryType.STANDARD
    retrieval_type: RetrievalType = RetrievalType.HYBRID
    max_results: int = 10
    threshold: float = 0.7
    context_window: int = 3
    max_tokens: int = 1000
    temperature: float = 0.7
    additional_config: Dict[str, Any] = {}
