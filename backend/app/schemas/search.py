from typing import Dict, List, Optional, Any
from pydantic import BaseModel


class EntityInfo(BaseModel):
    id: str
    name: str
    type: str
    community_id: Optional[str] = None
    rank: Optional[float] = None


class RelationshipInfo(BaseModel):
    source_id: str
    target_id: str
    type: str
    weight: Optional[float] = None


class ContextData(BaseModel):
    entities: List[EntityInfo]
    relationships: List[RelationshipInfo]
    text_units: List[Dict[str, Any]]
    community_reports: List[Dict[str, Any]]
    claims: List[Dict[str, Any]]


class SearchResult(BaseModel):
    response: str
    context_data: ContextData
    confidence_score: float
    metadata: Dict[str, Any]


class SearchError(BaseModel):
    error: str
    details: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    result: Optional[SearchResult] = None
    error: Optional[SearchError] = None
