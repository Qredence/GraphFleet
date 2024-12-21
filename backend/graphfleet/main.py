from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger(__name__)

from app.config import Settings, get_settings
from app.models import (
    GlobalSearchRequest,
    GlobalDynamicSearchRequest,
    LocalSearchRequest,
    DriftSearchRequest,
    DriftSearchResponse,
    SearchResponse,
    BuildIndexRequest,
    BuildIndexResponse,
    DocumentIngestionRequest,
    DocumentIngestionResponse,
    PromptTuningRequest,
    PromptTuningResponse,
    HealthResponse,
)
from app.services import (
    perform_global_search,
    perform_global_dynamic_search,
    perform_drift_search,
    tune_prompts,
    ingest_documents
)
from graphrag.api import local_search as graphrag_local_search
from graphrag.config.models.graph_rag_config import GraphRagConfig
from openai import AzureOpenAI
import pandas as pd
from pathlib import Path

app = FastAPI(title="GraphFleet API", version="1.0.0")

def get_llm(settings: Settings = Depends(get_settings)) -> AzureOpenAI:
    """Get Azure OpenAI client"""
    return AzureOpenAI(
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
        azure_endpoint=settings.azure_openai_api_base,
    )

def load_dataframes(base_dir: str):
    """Load required dataframes for search"""
    data_dir = Path(base_dir) / "data"
    
    return {
        "nodes": pd.read_parquet(data_dir / "create_final_nodes.parquet"),
        "entities": pd.read_parquet(data_dir / "create_final_entities.parquet"),
        "community_reports": pd.read_parquet(data_dir / "create_final_community_reports.parquet"),
        "text_units": pd.read_parquet(data_dir / "create_final_text_units.parquet"),
        "relationships": pd.read_parquet(data_dir / "create_final_relationships.parquet"),
        "covariates": pd.read_parquet(data_dir / "create_final_covariates.parquet"),
    }

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check(settings: Settings = Depends(get_settings)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "llm_model": settings.graphrag_llm_model,
        "embedding_model": settings.graphrag_embedding_model
    }

@app.post("/search/global", response_model=SearchResponse)
async def global_search(
    request: GlobalSearchRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Perform a global search operation using GraphRAG
    """
    if not settings.graphrag_api_key:
        raise HTTPException(status_code=500, detail="GRAPHRAG_API_KEY not set")
    
    try:
        result = await perform_global_search(
            query=request.query,
            community_level=request.community_level,
            response_type=request.response_type,
            settings=settings
        )
        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/global-dynamic", response_model=SearchResponse)
async def global_dynamic_search(
    request: GlobalDynamicSearchRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Perform a global dynamic search operation using GraphRAG
    """
    if not settings.graphrag_api_key:
        raise HTTPException(status_code=500, detail="GRAPHRAG_API_KEY not set")
    
    try:
        result = await perform_global_dynamic_search(
            query=request.query,
            response_type=request.response_type,
            settings=settings
        )
        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/local", response_model=SearchResponse)
async def local_search(
    request: LocalSearchRequest,
    settings: Settings = Depends(get_settings),
    llm: AzureOpenAI = Depends(get_llm),
):
    """Local search within a specific community"""
    if not settings.azure_openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="Azure OpenAI API key not configured",
        )

    try:
        # Load required data
        dfs = load_dataframes(settings.base_dir)
        
        # Create GraphRAG config
        config = GraphRagConfig(
            api_key=settings.azure_openai_api_key,
            api_base=settings.azure_openai_api_base,
            api_version=settings.azure_openai_api_version,
            llm=llm,
        )

        # Perform local search
        response = await graphrag_local_search(
            config=config,
            nodes=dfs["nodes"],
            entities=dfs["entities"],
            community_reports=dfs["community_reports"],
            text_units=dfs["text_units"],
            relationships=dfs["relationships"],
            covariates=dfs["covariates"],
            community_level=1,  # Default to level 1
            response_type=request.response_type,
            query=request.query,
        )

        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

@app.post("/search/drift", response_model=DriftSearchResponse)
async def drift_search(
    request: DriftSearchRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Perform a drift search operation using GraphRAG
    """
    if not settings.graphrag_api_key:
        raise HTTPException(status_code=500, detail="GRAPHRAG_API_KEY not set")
    
    try:
        result = await perform_drift_search(
            query=request.query,
            time_window=request.time_window,
            drift_threshold=request.drift_threshold,
            response_type=request.response_type,
            settings=settings
        )
        return DriftSearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/prompt/tune", response_model=PromptTuningResponse)
async def tune_prompt(
    request: PromptTuningRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Tune prompts for specific tasks
    """
    if not settings.graphrag_api_key:
        raise HTTPException(status_code=500, detail="GRAPHRAG_API_KEY not set")
    
    try:
        result = await tune_prompts(
            task_type=request.task_type,
            sample_queries=request.sample_queries,
            target_metrics=request.target_metrics,
            settings=settings
        )
        return PromptTuningResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/ingest", response_model=DocumentIngestionResponse)
async def ingest_document(
    request: DocumentIngestionRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Ingest new documents into the system
    """
    try:
        result = await ingest_documents(
            documents=request.documents,
            document_type=request.document_type,
            metadata=request.metadata or {},
            settings=settings
        )
        return DocumentIngestionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to GraphFleet API"}

@app.post("/build-index", response_model=BuildIndexResponse)
async def build_index(
    request: BuildIndexRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Build or rebuild the search index
    """
    # TODO: Implement index building logic
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/settings")
async def get_settings():
    try:
        return get_settings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
