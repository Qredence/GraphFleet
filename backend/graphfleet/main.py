"""GraphFleet FastAPI application."""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, Any

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

from utils.cache import get_cache, set_cache

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
    """Local search within a specific community with optimized GraphRAG features"""
    if not settings.azure_openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="Azure OpenAI API key not configured",
        )

    try:
        # Initialize cache
        cache_key = f"local_search_{request.query}_{request.response_type}"
        cached_response = await get_cache(cache_key)
        if cached_response:
            return cached_response

        # Load required data with error handling
        try:
            dfs = load_dataframes(settings.base_dir)
        except Exception as e:
            logger.error(f"Failed to load dataframes: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to load required data",
            )
        
        # Create GraphRAG config with optimized settings
        config = GraphRagConfig(
            api_key=settings.azure_openai_api_key,
            api_base=settings.azure_openai_api_base,
            api_version=settings.azure_openai_api_version,
            llm=llm,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            embedding_model=settings.embedding_model,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            top_k=5,  # Number of relevant chunks to consider
            similarity_threshold=0.7,  # Minimum similarity score
        )

        # Validate input data
        if not all(key in dfs for key in ["nodes", "entities", "community_reports", "text_units", "relationships", "covariates"]):
            raise ValueError("Missing required dataframes")

        # Perform local search with enhanced features
        response = await graphrag_local_search(
            config=config,
            nodes=dfs["nodes"],
            entities=dfs["entities"],
            community_reports=dfs["community_reports"],
            text_units=dfs["text_units"],
            relationships=dfs["relationships"],
            covariates=dfs["covariates"],
            community_level=request.community_level or 1,
            response_type=request.response_type,
            query=request.query,
            use_graph_context=True,  # Enable graph context for better results
            rerank_results=True,  # Enable result reranking
            max_hops=2,  # Maximum graph traversal distance
        )

        # Cache successful response
        await set_cache(cache_key, response, ttl=3600)  # Cache for 1 hour

        return response
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Local search error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during local search",
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
