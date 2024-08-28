from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.api import global_search, global_search_streaming, local_search, local_search_streaming

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

class SearchResponse(BaseModel):
    response: str
    context_data: dict

@router.post("/local", response_model=SearchResponse)
async def api_local_search(query: SearchQuery):
    response, context_data = await local_search(query.query)
    return SearchResponse(response=response, context_data=context_data)

@router.post("/global", response_model=SearchResponse)
async def api_global_search(query: SearchQuery):
    response, context_data = await global_search(query.query)
    return SearchResponse(response=response, context_data=context_data)

@router.post("/local/stream")
async def api_local_search_stream(query: SearchQuery):
    return StreamingResponse(local_search_streaming(query.query), media_type="text/event-stream")

@router.post("/global/stream")
async def api_global_search_stream(query: SearchQuery):
    return StreamingResponse(global_search_streaming(query.query), media_type="text/event-stream")