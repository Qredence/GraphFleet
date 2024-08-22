from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
from graphrag.config.models.graph_rag_config import GraphRagConfig

app = FastAPI()


# Pydantic models for request bodies
class SearchRequest(BaseModel):
    config: Dict[
        str, Any
    ]  # Simplified for brevity, ideally you'd define a proper config model
    nodes: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]
    community_reports: List[Dict[str, Any]]
    community_level: int
    response_type: str
    query: str


class LocalSearchRequest(SearchRequest):
    text_units: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    covariates: Optional[List[Dict[str, Any]]] = None


# Helper function to convert dict to DataFrame
def dict_to_df(data: List[Dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(data)


@app.post("/global_search")
async def api_global_search(request: SearchRequest):
    try:
        config = GraphRagConfig(
            **request.config
        )  # Assuming GraphRagConfig can be instantiated this way
        result = await global_search(
            config=config,
            nodes=dict_to_df(request.nodes),
            entities=dict_to_df(request.entities),
            community_reports=dict_to_df(request.community_reports),
            community_level=request.community_level,
            response_type=request.response_type,
            query=request.query,
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/global_search_streaming")
async def api_global_search_streaming(request: SearchRequest):
    try:
        config = GraphRagConfig(**request.config)
        result_generator = global_search_streaming(
            config=config,
            nodes=dict_to_df(request.nodes),
            entities=dict_to_df(request.entities),
            community_reports=dict_to_df(request.community_reports),
            community_level=request.community_level,
            response_type=request.response_type,
            query=request.query,
        )
        return result_generator  # FastAPI will handle the streaming
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/local_search")
async def api_local_search(request: LocalSearchRequest):
    try:
        config = GraphRagConfig(**request.config)
        result = await local_search(
            config=config,
            nodes=dict_to_df(request.nodes),
            entities=dict_to_df(request.entities),
            community_reports=dict_to_df(request.community_reports),
            text_units=dict_to_df(request.text_units),
            relationships=dict_to_df(request.relationships),
            covariates=dict_to_df(request.covariates) if request.covariates else None,
            community_level=request.community_level,
            response_type=request.response_type,
            query=request.query,
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/local_search_streaming")
async def api_local_search_streaming(request: LocalSearchRequest):
    try:
        config = GraphRagConfig(**request.config)
        result_generator = local_search_streaming(
            config=config,
            nodes=dict_to_df(request.nodes),
            entities=dict_to_df(request.entities),
            community_reports=dict_to_df(request.community_reports),
            text_units=dict_to_df(request.text_units),
            relationships=dict_to_df(request.relationships),
            covariates=dict_to_df(request.covariates) if request.covariates else None,
            community_level=request.community_level,
            response_type=request.response_type,
            query=request.query,
        )
        return result_generator  # FastAPI will handle the streaming
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Keep the original functions (global_search, global_search_streaming, local_search, local_search_streaming) as they are
