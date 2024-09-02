from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict  # Updated import
from app.services.question_generator import create_question_generator
from app.services.search_engine import create_search_engines, LocalSearchWrapper, GlobalSearchWrapper
from app.routers import search
import pandas as pd
import logging
import numpy as np
from app.utils import convert_numpy
from app.api import _reformat_context_data
import sentry_sdk

app = FastAPI()


sentry_sdk.init(
    dsn="https://741dc950f3465d2db0b8f869832dabc0@o4507875835314176.ingest.de.sentry.io/4507875863429200",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="GraphFleet API")

class SearchQuery(BaseModel):
    query: str

@app.post("/search/local")
async def local_search(search_query: SearchQuery):
    try:
        logger.debug(f"Received local search query: {search_query.query}")
        
        search_engines = create_search_engines()
        logger.debug("Search engines created successfully")
        
        local_search_engine = search_engines[0]
        logger.debug("Local search engine retrieved")
        
        logger.debug("Starting local search")
        result = await local_search_engine.asearch(search_query.query)
        logger.debug("Local search completed")
        
        logger.debug(f"Raw context_data keys: {result.context_data.keys()}")
        for key, value in result.context_data.items():
            logger.debug(f"Key: {key}, Type: {type(value)}")
        
        logger.debug("Starting context data reformatting")
        context_data = _reformat_context_data(result.context_data)
        logger.debug(f"Context data reformatted: {list(context_data.keys())}")
        
        logger.debug("Preparing response data")
        response_data = {
            "response": result.response,
            "context_data": context_data,
            "reports_head": context_data.get("reports", [])[:5] if "reports" in context_data else []
        }
        logger.debug("Response data prepared")
        
        return response_data
    except Exception as e:
        logger.error(f"Error in local_search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred during local search: {str(e)}")

@app.post("/search/global")
async def global_search(search_query: SearchQuery):
    search_engines = create_search_engines()
    global_search_engine = search_engines[1]
    try:
        logger.debug(f"Received global search query: {search_query.query}")
        result = await global_search_engine.asearch(search_query.query)
        context_data = _reformat_context_data(result.context_data)
        logger.debug(f"Context data reformatted: {list(context_data.keys())}")
        
        total_report_count = len(context_data.get("reports", []))
        filtered_report_count = len(context_data.get("reports", []))
        
        logger.debug("Global search completed successfully")
        return {
            "response": result.response,
            "context_data": context_data,
            "reports_head": context_data.get("reports", [])[:5] if "reports" in context_data else [],
            "total_report_count": total_report_count,
            "filtered_report_count": filtered_report_count,
            "reports": context_data.get("reports", [])
        }
    except Exception as e:
        logger.error(f"Error in global_search: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred during global search: {str(e)}")

@app.post("/search/local/stream")
async def local_search_stream(search_query: SearchQuery):
    search_engines = create_search_engines()
    local_search_engine = search_engines[0]
    try:
        async def stream_generator():
            async for chunk in local_search_engine.astream(search_query.query):
                yield f"data: {chunk}\n\n"
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/global/stream")
async def global_search_stream(search_query: SearchQuery):
    search_engines = create_search_engines()
    global_search_engine = search_engines[1]
    try:
        async def stream_generator():
            async for chunk in global_search_engine.astream(search_query.query):
                yield f"data: {chunk}\n\n"
        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_questions")
async def generate_questions(search_query: SearchQuery):
    question_generator = create_question_generator()
    try:
        result = await question_generator.agenerate(question_history=[search_query.query], context_data=None, question_count=5)
        return {"questions": result.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(search.router, prefix="/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Welcome to GraphFleet API"}


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
    return {"message": "This should never be reached"}


main = app
