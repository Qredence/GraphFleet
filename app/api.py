from typing import Any, Dict, List, AsyncGenerator
from fastapi import HTTPException
from app.services.search_engine import (
    local_search_engine,
    global_search_engine,
)


async def global_search(query: str) -> Dict[str, Any]:
    try:
        result = await global_search_engine.asearch(query)
        return {
            "response": result.response,
            "context_data": _reformat_context_data(result.context_data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Global search error: {str(e)}")


async def global_search_streaming(query: str) -> AsyncGenerator[str, None]:
    try:
        async for chunk in global_search_engine.asearch_streaming(query):
            yield chunk
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Global search streaming error: {str(e)}"
        )
    # Add this line to ensure the function always returns an AsyncGenerator
    yield ""


async def local_search(query: str) -> Dict[str, Any]:
    try:
        result = await local_search_engine.asearch(query)
        return {
            "response": result.response,
            "context_data": _reformat_context_data(result.context_data),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Local search error: {str(e)}"
        )


async def local_search_streaming(query: str) -> AsyncGenerator[str, None]:
    try:
        async for chunk in local_search_engine.asearch_streaming(query):
            yield chunk
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Local search streaming error: {str(e)}"
            )


def _reformat_context_data(context_data: Dict[str, Any]) -> Dict[str, List[Any]]:
    return {
        key: value.to_dict(orient="records") 
        if hasattr(value, "to_dict") 
        else (value if isinstance(value, list) else [value])
        for key, value in context_data.items()
    }
