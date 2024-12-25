"""
GraphFleet API v1 Endpoints

This module contains the REST API endpoints for the GraphFleet service.
It provides functionality for:
- Project initialization and indexing
- Query processing and analysis
- Knowledge graph statistics and management
- Custom pipelines and semantic search
- Drift analysis and monitoring

All endpoints handle errors gracefully and return appropriate HTTP status codes.
"""

from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.models import (
    AutoPromptRequest,
    BatchQueryRequest,
    GraphStats,
    IndexRequest,
    InitRequest,
    QueryAnalysisRequest,
    QueryRequest,
    QueryResponse,
)
from graphfleet.core import GraphFleet
from graphfleet.core.features import GraphFleetFeatures

router = APIRouter(prefix="/v1", tags=["GraphFleet API v1"])

@router.post("/init", response_model=Dict[str, str])
async def init_project(request: InitRequest):
    """Initialize a new GraphFleet project."""
    try:
        GraphFleet.init_project(request.project_path, **request.options)
        return {"status": "Project initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/index", response_model=Dict[str, str])
async def create_index(request: IndexRequest):
    """Create index for the current project."""
    try:
        graph_fleet = GraphFleet(request.project_path)
        await graph_fleet.create_index(**request.options)
        return {"status": "Index created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/autoprompt", response_model=Dict[str, str])
async def create_prompts(request: AutoPromptRequest):
    """Generate prompts automatically."""
    try:
        graph_fleet = GraphFleet(request.project_path)
        await graph_fleet.create_prompts(**request.options)
        return {"status": "Prompts generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Process a query using the specified query type."""
    try:
        graph_fleet = GraphFleet(request.project_path)
        result = await graph_fleet.query(
            request.query_text,
            query_type=request.query_type,
            **request.options
        )
        return QueryResponse(
            result=result,
            metadata={
                "query_type": request.query_type,
                "options_used": request.options,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-query", response_model=List[QueryResponse])
async def batch_query(request: BatchQueryRequest):
    """Process multiple queries in batch."""
    try:
        graph_fleet = GraphFleet(request.project_path)
        features = GraphFleetFeatures(graph_fleet.storage)
        results = await features.batch_query(
            request.queries,
            query_type=request.query_type,
            batch_size=request.batch_size,
            **request.options
        )
        return [
            QueryResponse(
                result=result,
                metadata={
                    "query_type": request.query_type,
                    "options_used": request.options,
                }
            )
            for result in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query-analysis", response_model=Dict)
async def query_analysis(request: QueryAnalysisRequest):
    """Perform detailed analysis of query results."""
    try:
        graph_fleet = GraphFleet(request.project_path)
        features = GraphFleetFeatures(graph_fleet.storage)
        analysis = await features.query_analysis(
            request.query_text,
            **request.options
        )
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/graph-stats", response_model=GraphStats)
async def graph_stats(project_path: str):
    """Get statistics about the knowledge graph."""
    try:
        graph_fleet = GraphFleet(project_path)
        features = GraphFleetFeatures(graph_fleet.storage)
        stats = await features.knowledge_graph_stats()
        return GraphStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New Endpoints

@router.post("/custom-pipeline", response_model=Dict[str, Any])
async def custom_pipeline(
    project_path: str = Query(..., description="Path to the GraphFleet project"),
    query_text: str = Query(..., description="Query text to process"),
    local_weight: float = Query(0.7, ge=0.0, le=1.0, description="Weight for local results"),
    options: Optional[Dict[str, Any]] = None
):
    """
    Run a custom hybrid query pipeline that combines local and global search results.
    
    Args:
        project_path: Path to the GraphFleet project
        query_text: Query text to process
        local_weight: Weight given to local results (between 0 and 1)
        options: Additional options for query processing
        
    Returns:
        Dict containing combined search results and metadata
        
    Raises:
        HTTPException: If there's an error during processing
    """
    try:
        graph_fleet = GraphFleet(project_path)
        
        # Get local and global results
        local_result = await graph_fleet.query_local(
            query_text,
            **(options or {})
        )
        global_result = await graph_fleet.query_global(
            query_text,
            **(options or {})
        )
        
        # Combine results
        combined_score = {}
        for doc in local_result.get("documents", []):
            combined_score[doc["id"]] = doc["score"] * local_weight
        
        for doc in global_result.get("documents", []):
            doc_id = doc["id"]
            if doc_id in combined_score:
                combined_score[doc_id] += doc["score"] * (1 - local_weight)
            else:
                combined_score[doc_id] = doc["score"] * (1 - local_weight)
        
        sorted_results = sorted(
            combined_score.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "results": sorted_results,
            "metadata": {
                "local_weight": local_weight,
                "options_used": options,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/semantic-search", response_model=Dict[str, Any])
async def semantic_search(
    project_path: str = Query(..., description="Path to the GraphFleet project"),
    query_text: str = Query(..., description="Query text for semantic search"),
    k: int = Query(10, ge=1, le=100, description="Number of results to return"),
    threshold: float = Query(0.5, ge=0.0, le=1.0, description="Similarity threshold")
):
    """
    Perform semantic search over the document collection.
    
    Args:
        project_path: Path to the GraphFleet project
        query_text: Search query text
        k: Number of results to return
        threshold: Minimum similarity threshold
        
    Returns:
        Dict containing search results and metadata
        
    Raises:
        HTTPException: If there's an error during search
    """
    try:
        graph_fleet = GraphFleet(project_path)
        results = await graph_fleet.semantic_search(
            query_text,
            k=k,
            threshold=threshold
        )
        return {
            "results": results,
            "metadata": {
                "k": k,
                "threshold": threshold,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/drift-analysis", response_model=Dict[str, Any])
async def drift_analysis(
    project_path: str = Query(..., description="Path to the GraphFleet project"),
    query_text: str = Query(..., description="Query text for drift analysis"),
    window_size: int = Query(100, ge=10, le=1000, description="Analysis window size")
):
    """
    Analyze concept drift in the knowledge graph over time.
    
    Args:
        project_path: Path to the GraphFleet project
        query_text: Query text for analysis
        window_size: Size of the analysis window
        
    Returns:
        Dict containing drift statistics and analysis results
        
    Raises:
        HTTPException: If there's an error during analysis
    """
    try:
        graph_fleet = GraphFleet(project_path)
        features = GraphFleetFeatures(graph_fleet.storage)
        drift_stats = await features.analyze_drift(
            query_text,
            window_size=window_size
        )
        return drift_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
