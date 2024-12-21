"""
Pydantic models for GraphFleet API requests and responses.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

class QueryType(str, Enum):
    """Types of queries supported by GraphFleet."""
    STANDARD = "standard"
    LOCAL = "local"
    GLOBAL = "global"
    DRIFT = "drift"
    DYNAMIC = "dynamic"

class BaseRequest(BaseModel):
    """Base request model with project path."""
    project_path: str = Field(..., description="Path to the project directory")
    options: Dict[str, Any] = Field(default_factory=dict, description="Additional options")

class QueryRequest(BaseRequest):
    """Query request model."""
    query_text: str = Field(..., description="The query text to process")
    query_type: QueryType = Field(default=QueryType.STANDARD, description="Type of query to perform")

class BatchQueryRequest(BaseRequest):
    """Batch query request model."""
    queries: List[str] = Field(..., description="List of queries to process")
    query_type: QueryType = Field(default=QueryType.STANDARD, description="Type of query to perform")
    batch_size: int = Field(default=5, description="Number of queries to process simultaneously")

class QueryAnalysisRequest(BaseRequest):
    """Query analysis request model."""
    query_text: str = Field(..., description="The query text to analyze")

class InitRequest(BaseRequest):
    """Project initialization request model."""
    project_name: str = Field(..., description="Name of the project to initialize")

class IndexRequest(BaseRequest):
    """Index creation request model."""
    pass

class AutoPromptRequest(BaseRequest):
    """Auto-prompt generation request model."""
    pass

class QueryResponse(BaseModel):
    """Query response model."""
    result: Dict[str, Any] = Field(..., description="Query result")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the query")

class ConfidenceScores(BaseModel):
    """Confidence score statistics."""
    mean: float
    std: float
    min: float
    max: float

class SourceDiversity(BaseModel):
    """Source diversity statistics."""
    total_sources: int
    unique_sources: int
    source_distribution: Dict[str, int]

class ContextAnalysis(BaseModel):
    """Context analysis statistics."""
    context_lengths: List[int]
    avg_context_length: float
    total_context_used: int

class CommunityStats(BaseModel):
    """Community statistics."""
    total_communities: int
    size_distribution: Dict[str, int]
    avg_size: float
    max_size: int
    min_size: int

class EmbeddingStats(BaseModel):
    """Embedding space statistics."""
    dimension: int
    mean_norm: float
    std_norm: float

class GraphStats(BaseModel):
    """Knowledge graph statistics."""
    node_count: int
    edge_count: int
    community_stats: CommunityStats
    embedding_stats: EmbeddingStats
