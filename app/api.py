from typing import Any, Dict, List, Tuple, AsyncGenerator
from fastapi import HTTPException
from app.services.search_engine import local_search_engine, global_search_engine

async def global_search(query: str) -> Tuple[str, Dict[str, List[Dict[str, Any]]]]:
    try:
        result = await global_search_engine.asearch(query)
        response = result.response
        context_data = _reformat_context_data(result.context_data)
        return response, context_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Global search error: {str(e)}")

async def global_search_streaming(query: str) -> AsyncGenerator[str, None]:
    try:
        async for token in global_search_engine.astream(query):
            yield token
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Global search streaming error: {str(e)}")

async def local_search(query: str) -> Tuple[str, Dict[str, List[Dict[str, Any]]]]:
    try:
        result = await local_search_engine.asearch(query)
        response = result.response
        context_data = _reformat_context_data(result.context_data)
        return response, context_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local search error: {str(e)}")

async def local_search_streaming(query: str) -> AsyncGenerator[str, None]:
    try:
        async for token in local_search_engine.astream(query):
            yield token
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local search streaming error: {str(e)}")

def _reformat_context_data(context_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    reformatted_data = {}
    for key, value in context_data.items():
        if hasattr(value, 'to_dict'):
            reformatted_data[key] = value.to_dict(orient='records')
        elif isinstance(value, list):
            reformatted_data[key] = value
        else:
            reformatted_data[key] = [value]
    return reformatted_data