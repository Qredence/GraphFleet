import os
import pandas as pd
import tiktoken
from fastapi import HTTPException
from graphrag.query.structured_search.local_search.search import (
    LocalSearch as OriginalLocalSearch
)
from graphrag.query.structured_search.global_search.search import (
    GlobalSearch as OriginalGlobalSearch
)
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.llm.oai.typing import OpenaiApiType
from graphrag.query.context_builder.entity_extraction import (
    EntityVectorStoreKey
)
from graphrag.query.structured_search.global_search.community_context import (
    GlobalCommunityContext
)
from app.utils import create_context_builder
from app.config import settings
from app.utils.data_processing import (
    read_indexer_entities,
    read_indexer_reports
)
import asyncio
import logging

logger = logging.getLogger(__name__)

class LocalSearchWrapper(OriginalLocalSearch):
    async def astream(self, query: str):
        result = await self.asearch(query)
        response = result.response
        # Simulate streaming by yielding chunks of the response
        chunk_size = 10  # Adjust this value to control the streaming speed
        response_chars = list(response)
        for i in range(0, len(response_chars), chunk_size):
            yield ''.join(str(char) for char in response_chars[i:i+chunk_size])
            await asyncio.sleep(0.1)  # Add a small delay between chunks


class GlobalSearchWrapper(OriginalGlobalSearch):
    async def astream(self, query: str):
        result = await self.asearch(query)
        response = result.response
        # Simulate streaming by yielding chunks of the response
        chunk_size = 10  # Adjust this value to control the streaming speed
        response_chars = list(response)
        for i in range(0, len(response_chars), chunk_size):
            yield ''.join(str(char) for char in response_chars[i:i+chunk_size])
            await asyncio.sleep(0.1)  # Add a small delay between chunks


def create_search_engines():
    try:
        logger.debug("Starting create_search_engines")
        
        # Check if the directory exists
        if not os.path.exists(settings.INPUT_DIR):
            logger.error(f"Directory not found: {settings.INPUT_DIR}")
            raise FileNotFoundError(f"Directory not found: {settings.INPUT_DIR}")

        # List of required files
        required_files = [
            "create_final_nodes.parquet",
            "create_final_community_reports.parquet",
            "create_final_entities.parquet"
        ]

        # Check if all required files exist
        for file in required_files:
            file_path = os.path.join(settings.INPUT_DIR, file)
            if not os.path.exists(file_path):
                logger.error(f"Required file not found: {file_path}")
                raise FileNotFoundError(f"Required file not found: {file_path}")

        logger.debug("All required files found")

        # If all checks pass, proceed with loading the data
        entity_df = pd.read_parquet(
            f"{settings.INPUT_DIR}/create_final_nodes.parquet")
        logger.debug(f"Loaded entity_df: {entity_df.shape}")
        
        report_df = pd.read_parquet(
            f"{settings.INPUT_DIR}/create_final_community_reports.parquet")
        logger.debug(f"Loaded report_df: {report_df.shape}")
        
        entity_embedding_df = pd.read_parquet(
            f"{settings.INPUT_DIR}/create_final_entities.parquet")
        logger.debug(f"Loaded entity_embedding_df: {entity_embedding_df.shape}")

        reports = read_indexer_reports(
            report_df, entity_df, settings.COMMUNITY_LEVEL)
        logger.debug(f"Processed reports: {len(reports)}")
        
        entities = read_indexer_entities(
            entity_df, entity_embedding_df, settings.COMMUNITY_LEVEL)
        logger.debug(f"Processed entities: {len(entities)}")

        llm = ChatOpenAI(
            api_key=settings.API_KEY,
            api_base=settings.API_BASE,
            api_version=settings.API_VERSION,
            model=settings.LLM_MODEL,
            api_type=OpenaiApiType.AzureOpenAI,
            max_retries=20,
        )

        token_encoder = tiktoken.get_encoding("cl100k_base")

        local_context_builder = create_context_builder()
        local_context_params = {
            "text_unit_prop": 0.5,
            "community_prop": 0.1,
            "conversation_history_max_turns": 5,
            "conversation_history_user_turns_only": True,
            "top_k_mapped_entities": 10,
            "top_k_relationships": 10,
            "include_entity_rank": True,
            "include_relationship_weight": True,
            "include_community_rank": False,
            "return_candidate_context": False,
            "embedding_vectorstore_key": EntityVectorStoreKey.ID,
            "max_tokens": settings.MAX_TOKENS,
        }

        local_search = LocalSearchWrapper(
            llm=llm,
            context_builder=local_context_builder,
            token_encoder=token_encoder,
            llm_params={"max_tokens": 2000, "temperature": 0.0},
            context_builder_params=local_context_params,
            response_type="multiple paragraphs",
        )

        global_context_builder = GlobalCommunityContext(
            community_reports=reports,
            entities=entities,
            token_encoder=token_encoder,
        )

        global_context_params = {
            "use_community_summary": False,
            "shuffle_data": True,
            "include_community_rank": True,
            "min_community_rank": 0,
            "community_rank_name": "rank",
            "include_community_weight": True,
            "community_weight_name": "occurrence weight",
            "normalize_community_weight": True,
            "max_tokens": settings.MAX_TOKENS,
            "context_name": "Reports",
        }

        global_search = GlobalSearchWrapper(
            llm=llm,
            context_builder=global_context_builder,
            token_encoder=token_encoder,
            max_data_tokens=settings.MAX_TOKENS,
            map_llm_params={
                "max_tokens": 1000,
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            },
            reduce_llm_params={"max_tokens": 2000, "temperature": 0.0},
            allow_general_knowledge=True,
            json_mode=True,
            context_builder_params=global_context_params,
            concurrent_coroutines=32,
            response_type="multiple paragraphs",
        )

        logger.debug("Search engines created successfully")
        return [local_search, global_search]

    except Exception as e:
        logger.error(f"Error in create_search_engines: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error creating search engines: {str(e)}"
        )


local_search_engine, global_search_engine = create_search_engines()
