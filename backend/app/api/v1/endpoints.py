"""
API v1 endpoints for GraphFleet.
"""

from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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

router = APIRouter()

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

@router.post("/custom-pipeline")
async def custom_pipeline(
    project_path: str,
    query_text: str,
    local_weight: float = 0.7,
    options: Optional[Dict] = None
):
    """Run a custom hybrid query pipeline."""
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

@router.post("/semantic-search")
async def semantic_search(
    project_path: str,
    query_text: str,
    k: int = 10,
    threshold: float = 0.5
):
    """Perform semantic search over the document collection."""
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

@router.post("/drift-analysis")
async def drift_analysis(
    project_path: str,
    query_text: str,
    window_size: int = 100
):
    """Analyze concept drift in the knowledge graph."""
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
