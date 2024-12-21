from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.core.config import Settings, get_settings
from app.services.query import QueryService
from app.schemas.search import SearchQuery, SearchResult
from app.api.deps import get_query_service

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    method: str = "global"
    streaming: bool = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None

@router.post("", response_model=SearchResult)
async def execute_query(
    request: QueryRequest,
    settings: Settings = Depends(get_settings),
    query_service: QueryService = Depends(get_query_service),
) -> SearchResult:
    """Execute a query using the specified method."""
    try:
        if request.streaming:
            return StreamingResponse(
                query_service.execute_query(
                    query=request.query,
                    method=request.method,
                    streaming=True,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                ),
                media_type="text/event-stream",
            )
        
        return await query_service.execute_query(
            query=request.query,
            method=request.method,
            streaming=False,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute query: {str(e)}",
        )
