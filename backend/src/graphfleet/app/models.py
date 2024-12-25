"""Models module for GraphFleet app."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class PromptTuningRequest(BaseModel):
    """Request model for prompt tuning."""
    task_type: str
    sample_queries: List[str]
    target_metrics: List[str]
    options: Dict[str, Any] = {}

class BuildIndexRequest(BaseModel):
    """Request model for index building."""
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
    chunk_strategy: Optional[str] = None
    embedding_config: Optional[Dict[str, Any]] = None
    options: Dict[str, Any] = {} 