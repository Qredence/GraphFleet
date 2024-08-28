import pandas as pd
import tiktoken
from graphrag.query.structured_search.local_search.mixed_context import LocalSearchMixedContext
from graphrag.query.llm.oai.embedding import OpenAIEmbedding
from graphrag.query.context_builder.entity_extraction import EntityVectorStoreKey
from graphrag.vector_stores.lancedb import LanceDBVectorStore
from graphrag.query.llm.oai.typing import OpenaiApiType
from app.config import settings
from app.utils.data_processing import (
    process_entities,
    process_relationships,
    process_covariates,
    process_reports,
    process_text_units,
    store_embeddings,
)

def create_context_builder():
    # Load data
    entity_df = pd.read_parquet(f"{settings.INPUT_DIR}/create_final_nodes.parquet")
    entity_embedding_df = pd.read_parquet(f"{settings.INPUT_DIR}/create_final_entities.parquet")
    relationship_df = pd.read_parquet(f"{settings.INPUT_DIR}/create_final_relationships.parquet")
    covariate_df = pd.read_parquet(f"{settings.INPUT_DIR}/create_final_covariates.parquet")
    report_df = pd.read_parquet(f"{settings.INPUT_DIR}/create_final_community_reports.parquet")
    text_unit_df = pd.read_parquet(f"{settings.INPUT_DIR}/create_final_text_units.parquet")

    # Process data
    entities = process_entities(entity_df, entity_embedding_df, settings.COMMUNITY_LEVEL)
    relationships = process_relationships(relationship_df)
    claims = process_covariates(covariate_df)
    reports = process_reports(report_df, entity_df, settings.COMMUNITY_LEVEL)
    text_units = process_text_units(text_unit_df)

    # Set up embedding store
    description_embedding_store = LanceDBVectorStore(collection_name="entity_description_embeddings")
    description_embedding_store.connect(db_uri=settings.LANCEDB_URI)
    entity_description_embeddings = store_embeddings(entities, description_embedding_store)

    # Create text embedder
    text_embedder = OpenAIEmbedding(
        api_key=settings.API_KEY,
        api_base=settings.API_BASE,
        api_version=settings.API_VERSION,
        api_type=OpenaiApiType.AzureOpenAI,
        model=settings.EMBEDDING_MODEL,
        deployment_name=settings.EMBEDDING_MODEL,
        max_retries=20,
    )

    # Create token encoder
    token_encoder = tiktoken.get_encoding("cl100k_base")

    return LocalSearchMixedContext(
        community_reports=reports,
        text_units=text_units,
        entities=entities,
        relationships=relationships,
        covariates={"claims": claims},
        entity_text_embeddings=description_embedding_store,
        embedding_vectorstore_key=EntityVectorStoreKey.ID,
        text_embedder=text_embedder,
        token_encoder=token_encoder,
    )