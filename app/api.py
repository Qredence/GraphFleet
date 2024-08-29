from typing import Any, Dict, List, AsyncGenerator
from fastapi import HTTPException
from app.services.search_engine import (
    local_search_engine,
    global_search_engine,
)
import logging
import numpy as np
from app.utils import convert_numpy

# ... existing imports ...

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def global_search(query: str) -> Dict[str, Any]:
    try:
        logger.debug(f"Starting global search with query: {query}")
        result = await global_search_engine.asearch(query)
        logger.debug("Global search completed successfully")
        context_data = _reformat_context_data(result.context_data)
        logger.debug(f"Context data reformatted: {list(context_data.keys())}")
        return {
            "response": result.response,
            "context_data": context_data,
        }
    except Exception as e:
        logger.error(f"Global search error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Global search error: {str(e)}"
        )


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
        logger.debug(f"Starting local search with query: {query}")
        result = await local_search_engine.asearch(query)
        logger.debug("Local search completed successfully")
        context_data = _reformat_context_data(result.context_data)
        logger.debug(f"Context data reformatted: {list(context_data.keys())}")
        return {
            "response": result.response,
            "context_data": context_data,
        }
    except Exception as e:
        logger.error(f"Local search error: {str(e)}", exc_info=True)
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
            status_code=500,
            detail=f"Local search streaming error: {str(e)}"
        )


def _reformat_context_data(context_data: Dict[str, Any]) -> Dict[str, List[Any]]:
    reformatted_data = {}
    for key, value in context_data.items():
        logger.debug(f"Processing key: {key}, Type: {type(value)}")
        try:
            if hasattr(value, "to_dict"):
                logger.debug(f"Converting {key} using to_dict method")
                reformatted_data[key] = convert_numpy(value.to_dict(orient="records"))
            elif isinstance(value, list):
                logger.debug(f"Converting {key} as list")
                reformatted_data[key] = convert_numpy(value)
            else:
                logger.debug(f"Converting {key} as single value")
                reformatted_data[key] = convert_numpy([value])
            logger.debug(f"Converted {key}, Type: {type(reformatted_data[key])}")
        except Exception as e:
            logger.error(f"Error converting {key}: {str(e)}", exc_info=True)
            reformatted_data[key] = str(value)  # Fallback to string representation
    return reformatted_data
