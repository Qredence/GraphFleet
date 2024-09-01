from pydantic import BaseModel, HttpUrl
from typing import Dict, Any

class QueryParams(BaseModel):
    question: str
    method: str = "global"

class Document(BaseModel):
    content: str
    metadata: Dict[str, Any]

class IndexResponse(BaseModel):
    message: str
    indexed_count: int

class PromptTuneResponse(BaseModel):
    message: str
    status: str

class MonthyRequest(BaseModel):
    url: HttpUrl
    output_format: str = "text"