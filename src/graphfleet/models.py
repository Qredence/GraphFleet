from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Document(BaseModel):
    content: str
    metadata: Dict[str, Any]

class IndexRequest(BaseModel):
    documents: List[Document]

class QueryRequest(BaseModel):
    question: str
    method: str = Field(default="global", pattern="^(global|local)$")

class SearchRequest(BaseModel):
    query: str
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class ReleaseNotesRequest(BaseModel):
    version: str
    changes: List[str]