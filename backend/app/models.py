"""
GraphFleet Data Models

This module defines the Pydantic models used throughout the GraphFleet application.
These models handle data validation and serialization for API requests and responses.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime

class InitRequest(BaseModel):
    """Request model for project initialization."""
    project_path: str = Field(..., description="Path where the project will be initialized")
    options: Dict[str, Any] = Field(default_factory=dict, description="Additional initialization options")

    class Config:
        json_schema_extra = {
            "example": {
                "project_path": "/path/to/project",
                "options": {
                    "chunk_size": 1000,
                    "embedding_model": "text-embedding-3-large"
                }
            }
        }

class IndexRequest(BaseModel):
    """Request model for document indexing."""
    project_path: str = Field(..., description="Path to the project")
    options: Dict[str, Any] = Field(default_factory=dict, description="Indexing options")

    class Config:
        json_schema_extra = {
            "example": {
                "project_path": "/path/to/project",
                "options": {
                    "chunk_strategy": "sentence",
                    "chunk_overlap": 200
                }
            }
        }

class QueryRequest(BaseModel):
    """Request model for querying the knowledge graph."""
    project_path: str = Field(..., description="Path to the project")
    query_text: str = Field(..., description="Query text to process")
    query_type: str = Field(
        default="semantic",
        description="Type of query to perform",
        regex="^(semantic|local|global|drift)$"
    )
    options: Dict[str, Any] = Field(default_factory=dict, description="Query options")

    @validator("query_type")
    def validate_query_type(cls, v):
        allowed = {"semantic", "local", "global", "drift"}
        if v not in allowed:
            raise ValueError(f"query_type must be one of {allowed}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "project_path": "/path/to/project",
                "query_text": "What is GraphFleet?",
                "query_type": "semantic",
                "options": {
                    "max_results": 5,
                    "similarity_threshold": 0.7
                }
            }
        }

class BatchQueryRequest(BaseModel):
    """Request model for batch query processing."""
    project_path: str = Field(..., description="Path to the project")
    queries: List[str] = Field(..., description="List of queries to process")
    query_type: str = Field(
        default="semantic",
        description="Type of queries to perform",
        regex="^(semantic|local|global|drift)$"
    )
    batch_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of queries to process in parallel"
    )
    options: Dict[str, Any] = Field(default_factory=dict, description="Query options")

class QueryResponse(BaseModel):
    """Response model for query results."""
    result: Union[str, List[Dict[str, Any]]] = Field(..., description="Query result")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")

class GraphStats(BaseModel):
    """Model for knowledge graph statistics."""
    node_count: int = Field(..., description="Total number of nodes")
    edge_count: int = Field(..., description="Total number of edges")
    avg_degree: float = Field(..., description="Average node degree")
    density: float = Field(..., description="Graph density")
    communities: int = Field(..., description="Number of communities")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

class AutoPromptRequest(BaseModel):
    """Request model for automatic prompt generation."""
    project_path: str = Field(..., description="Path to the project")
    options: Dict[str, Any] = Field(default_factory=dict, description="Prompt generation options")

class QueryAnalysisRequest(BaseModel):
    """Request model for query analysis."""
    project_path: str = Field(..., description="Path to the project")
    query_text: str = Field(..., description="Query text to analyze")
    options: Dict[str, Any] = Field(default_factory=dict, description="Analysis options")
