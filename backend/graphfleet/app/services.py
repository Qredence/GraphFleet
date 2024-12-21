import pandas as pd
import tiktoken
from typing import Dict, Any, List
import logging
from datetime import datetime, timedelta
import os

from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.structured_search.global_search.community_context import GlobalCommunityContext
from graphrag.query.structured_search.global_search.search import GlobalSearch
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.query.indexer_adapters import (
    read_indexer_communities,
    read_indexer_entities,
    read_indexer_reports,
    read_indexer_relationships,
    read_indexer_text_units,
)
from graphrag.config.create_graphrag_config import create_graphrag_config

from .config import Settings
from .modules.drift import DriftDetector
from .modules.prompt_tuning import PromptTuner
from .modules.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initialize_llm(settings: Settings):
    """Initialize the LLM with settings"""
    try:
        logger.info(f"Initializing LLM with settings: api_base={settings.azure_openai_api_base}, deployment={settings.azure_openai_deployment}")
        llm = ChatOpenAI(
            api_key=settings.azure_openai_api_key,
            api_base=settings.azure_openai_api_base,
            api_version=settings.azure_openai_api_version,
            deployment_name=settings.azure_openai_deployment,
            api_type=OpenaiApiType.AZURE,
            max_retries=3,
            supports_json=settings.llm_supports_json
        )
        token_encoder = tiktoken.get_encoding(settings.encoding_model)
        return llm, token_encoder
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise

def load_dataframes(settings: Settings, community_level: int = 2) -> Dict[str, Any]:
    """Load all required dataframes"""
    try:
        logger.info(f"Loading dataframes from directory: {settings.output_dir}")
        
        # Check if output directory exists
        if not os.path.exists(settings.output_dir):
            logger.error(f"Output directory does not exist: {settings.output_dir}")
            raise FileNotFoundError(f"Output directory not found: {settings.output_dir}")
        
        files_to_load = {
            "communities": "create_final_communities.parquet",
            "nodes": "create_final_nodes.parquet",
            "entities": "create_final_entities.parquet",
            "reports": "create_final_community_reports.parquet",
            "relationships": "create_final_relationships.parquet",
            "text_units": "create_final_text_units.parquet"
        }
        
        # Check if all required files exist
        for name, filename in files_to_load.items():
            filepath = os.path.join(settings.output_dir, filename)
            if not os.path.exists(filepath):
                logger.error(f"Required file not found: {filepath}")
                raise FileNotFoundError(f"Required file not found: {filepath}")
            logger.debug(f"Found {name} file: {filepath}")
        
        # Load all dataframes
        community_df = pd.read_parquet(os.path.join(settings.output_dir, files_to_load["communities"]))
        entity_df = pd.read_parquet(os.path.join(settings.output_dir, files_to_load["nodes"]))
        entity_embedding_df = pd.read_parquet(os.path.join(settings.output_dir, files_to_load["entities"]))
        report_df = pd.read_parquet(os.path.join(settings.output_dir, files_to_load["reports"]))
        relationship_df = pd.read_parquet(os.path.join(settings.output_dir, files_to_load["relationships"]))
        text_unit_df = pd.read_parquet(os.path.join(settings.output_dir, files_to_load["text_units"]))
        
        logger.info("Successfully loaded all dataframes")
        
        return {
            "communities": read_indexer_communities(community_df, entity_df, report_df),
            "entities": read_indexer_entities(entity_df, entity_embedding_df, community_level),
            "reports": read_indexer_reports(report_df, entity_df, community_level),
            "relationships": read_indexer_relationships(relationship_df),
            "text_units": read_indexer_text_units(text_unit_df)
        }
    except Exception as e:
        logger.error(f"Error loading dataframes: {str(e)}")
        raise

async def perform_global_search(
    query: str,
    community_level: int,
    response_type: str,
    settings: Settings
) -> Dict[str, Any]:
    """Perform global search operation"""
    try:
        logger.info(f"Starting global search with query: {query}")
        
        config = create_graphrag_config()
        logger.debug("Created GraphRAG config")
        
        llm, token_encoder = initialize_llm(settings)
        logger.debug("Initialized LLM and token encoder")
        
        data = load_dataframes(settings, community_level=community_level)
        logger.debug("Loaded dataframes")
        
        context = GlobalCommunityContext(
            communities=data["communities"],
            entities=data["entities"],
            community_level=community_level
        )
        logger.debug("Created global search context")
        
        search = GlobalSearch(llm=llm, token_encoder=token_encoder)
        logger.debug("Created global search instance")
        
        result = await search.search(
            query=query,
            context=context,
            response_type=response_type
        )
        logger.info("Successfully completed global search")
        
        return {
            "response": result.response,
            "context": result.context_data
        }
    except Exception as e:
        logger.error(f"Global search error: {str(e)}", exc_info=True)
        raise

async def perform_global_dynamic_search(
    query: str,
    response_type: str,
    settings: Settings
) -> Dict[str, Any]:
    """Perform global dynamic search operation"""
    try:
        logger.info(f"Starting global dynamic search with query: {query}")
        
        config = create_graphrag_config()
        logger.debug("Created GraphRAG config")
        
        llm, token_encoder = initialize_llm(settings)
        logger.debug("Initialized LLM and token encoder")
        
        data = load_dataframes(settings)
        logger.debug("Loaded dataframes")
        
        context = GlobalCommunityContext(
            communities=data["communities"],
            entities=data["entities"],
            community_level=None  # Dynamic selection
        )
        logger.debug("Created global dynamic search context")
        
        search = GlobalSearch(llm=llm, token_encoder=token_encoder)
        logger.debug("Created global dynamic search instance")
        
        result = await search.search(
            query=query,
            context=context,
            response_type=response_type
        )
        logger.info("Successfully completed global dynamic search")
        
        return {
            "response": result.response,
            "context": result.context_data
        }
    except Exception as e:
        logger.error(f"Global dynamic search error: {str(e)}", exc_info=True)
        raise

async def perform_local_search(
    query: str,
    response_type: str,
    settings: Settings
) -> Dict[str, Any]:
    """Perform local search operation"""
    try:
        logger.info(f"Starting local search with query: {query}")
        
        config = create_graphrag_config()
        logger.debug("Created GraphRAG config")
        
        llm, token_encoder = initialize_llm(settings)
        logger.debug("Initialized LLM and token encoder")
        
        data = load_dataframes(settings)
        logger.debug("Loaded dataframes")
        
        context = LocalSearchMixedContext(
            entities=data["entities"],
            relationships=data["relationships"],
            text_units=data["text_units"]
        )
        logger.debug("Created local search context")
        
        search = LocalSearch(llm=llm, token_encoder=token_encoder)
        logger.debug("Created local search instance")
        
        result = await search.search(
            query=query,
            context=context,
            response_type=response_type
        )
        logger.info("Successfully completed local search")
        
        return {
            "response": result.response,
            "context": result.context_data
        }
    except Exception as e:
        logger.error(f"Local search error: {str(e)}", exc_info=True)
        raise

async def perform_drift_search(
    query: str,
    time_window: str,
    drift_threshold: float,
    response_type: str,
    settings: Settings
) -> Dict[str, Any]:
    """Perform drift search operation"""
    try:
        logger.info(f"Starting drift search with query: {query}")
        
        config = create_graphrag_config()
        logger.debug("Created GraphRAG config")
        
        llm, token_encoder = initialize_llm(settings)
        logger.debug("Initialized LLM and token encoder")
        
        data = load_dataframes(settings)
        logger.debug("Loaded dataframes")
        
        # Parse time window
        unit = time_window[-1]
        value = int(time_window[:-1])
        if unit == 'd':
            delta = timedelta(days=value)
        elif unit == 'h':
            delta = timedelta(hours=value)
        else:
            raise ValueError(f"Unsupported time window unit: {unit}")
        
        end_time = datetime.now()
        start_time = end_time - delta
        
        drift_detector = DriftDetector(
            llm=llm,
            token_encoder=token_encoder,
            threshold=drift_threshold
        )
        logger.debug("Created drift detector")
        
        drift_result = drift_detector.detect_drift(
            query=query,
            context=data,
            start_time=start_time,
            end_time=end_time
        )
        logger.info("Successfully completed drift search")
        
        return {
            "response": drift_result.response,
            "context": drift_result.context_data,
            "drift_score": drift_result.drift_score,
            "drift_details": drift_result.drift_details
        }
    except Exception as e:
        logger.error(f"Drift search error: {str(e)}", exc_info=True)
        raise

async def tune_prompts(
    task_type: str,
    sample_queries: List[str],
    target_metrics: List[str],
    settings: Settings
) -> Dict[str, Any]:
    """Perform prompt tuning"""
    try:
        logger.info(f"Starting prompt tuning with task type: {task_type}")
        
        config = create_graphrag_config()
        logger.debug("Created GraphRAG config")
        
        llm, token_encoder = initialize_llm(settings)
        logger.debug("Initialized LLM and token encoder")
        
        tuner = PromptTuner(
            llm=llm,
            token_encoder=token_encoder,
            task_type=task_type,
            target_metrics=target_metrics
        )
        logger.debug("Created prompt tuner")
        
        result = await tuner.tune(sample_queries)
        logger.info("Successfully completed prompt tuning")
        
        return {
            "success": result.success,
            "tuned_prompts": result.prompts,
            "performance_metrics": result.metrics
        }
    except Exception as e:
        logger.error(f"Prompt tuning error: {str(e)}", exc_info=True)
        raise

async def ingest_documents(
    documents: List[str],
    document_type: str,
    metadata: Dict[str, Any],
    settings: Settings
) -> Dict[str, Any]:
    """Ingest documents into the system"""
    try:
        logger.info(f"Starting document ingestion with document type: {document_type}")
        
        config = create_graphrag_config()
        logger.debug("Created GraphRAG config")
        
        processor = DocumentProcessor(
            document_type=document_type,
            output_dir=settings.output_dir
        )
        logger.debug("Created document processor")
        
        result = await processor.process_documents(
            documents=documents,
            metadata=metadata
        )
        logger.info("Successfully completed document ingestion")
        
        return {
            "success": result.success,
            "processed_count": result.processed_count,
            "failed_documents": result.failed_documents,
            "details": result.details
        }
    except Exception as e:
        logger.error(f"Document ingestion error: {str(e)}", exc_info=True)
        raise
