from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SearchType(str, Enum):
    GLOBAL = "global"
    LOCAL = "local"
    GLOBAL_DYNAMIC = "global_dynamic"

class BaseSearchRequest(BaseModel):
    query: str = Field(..., description="The search query")
    response_type: str = Field(default="Multiple Paragraphs", description="Type of response format")

class GlobalSearchRequest(BaseSearchRequest):
    community_level: int = Field(default=2, description="Community level for global search")

class GlobalDynamicSearchRequest(BaseSearchRequest):
    pass

class LocalSearchRequest(BaseSearchRequest):
    pass

class DriftSearchRequest(BaseSearchRequest):
    time_window: str = Field(..., description="Time window for drift analysis (e.g., '7d', '30d')")
    drift_threshold: float = Field(default=0.5, description="Threshold for drift detection")

class SearchResponse(BaseModel):
    response: str
    context: Dict[str, Any]

class DriftSearchResponse(BaseModel):
    response: str
    context: Dict[str, Any]
    drift_score: float
    drift_details: Dict[str, Any]

class DocumentIngestionRequest(BaseModel):
    documents: List[str] = Field(..., description="List of document paths to ingest")
    document_type: str = Field(default="text", description="Type of documents being ingested")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata for the documents")

class DocumentIngestionResponse(BaseModel):
    success: bool
    processed_count: int
    failed_documents: List[str]
    details: Dict[str, Any]

class PromptTuningRequest(BaseModel):
    task_type: str = Field(..., description="Type of task to tune prompts for")
    sample_queries: List[str] = Field(..., description="Sample queries for tuning")
    target_metrics: List[str] = Field(default=["accuracy", "relevance"], description="Metrics to optimize for")

class PromptTuningResponse(BaseModel):
    success: bool
    tuned_prompts: Dict[str, str]
    performance_metrics: Dict[str, float]

class BuildIndexRequest(BaseModel):
    source_dir: str = Field(..., description="Source directory containing documents")
    index_type: str = Field(default="default", description="Type of index to build")

class BuildIndexResponse(BaseModel):
    workflow_results: List[Dict[str, Any]]

class HealthResponse(BaseModel):
    status: str
    version: str
    llm_model: str
    embedding_model: str
