"""
GraphFleet FastAPI application.
"""

from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models import (
    AutoPromptRequest,
    IndexRequest,
    InitRequest,
    QueryRequest,
    QueryResponse,
    QueryType,
)
from graphfleet.core import GraphFleet

app = FastAPI(
    title="GraphFleet",
    description="GraphFleet API - Enhanced GraphRAG capabilities through FastAPI",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GraphFleet instance
graph_fleet = GraphFleet(settings.project_dir)

@app.post("/init", response_model=Dict[str, str])
async def init_project(request: InitRequest):
    """Initialize a new GraphFleet project."""
    try:
        GraphFleet.init_project(
            Path(settings.project_dir) / request.project_name,
            **request.options
        )
        return {"status": "Project initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index", response_model=Dict[str, str])
async def create_index(request: IndexRequest):
    """Create index for the current project."""
    try:
        graph_fleet.create_index(**request.options)
        return {"status": "Index created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/autoprompt", response_model=Dict[str, str])
async def create_prompts(request: AutoPromptRequest):
    """Generate prompts automatically."""
    try:
        graph_fleet.create_prompts(**request.options)
        return {"status": "Prompts generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process a query using the specified query type."""
    try:
        query_funcs = {
            QueryType.STANDARD: graph_fleet.query,
            QueryType.LOCAL: graph_fleet.query_local,
            QueryType.GLOBAL: graph_fleet.query_global,
            QueryType.DRIFT: graph_fleet.query_drift,
            QueryType.DYNAMIC: graph_fleet.query_dynamic,
        }
        
        query_func = query_funcs[request.query_type]
        result = query_func(request.query_text, **request.options)
        
        return QueryResponse(
            result=result,
            metadata={
                "query_type": request.query_type,
                "options_used": request.options,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Check API health."""
    return {"status": "healthy"}