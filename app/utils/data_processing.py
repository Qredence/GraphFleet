from typing import Dict, List
import pandas as pd
from graphrag.query.indexer_adapters import (
    read_indexer_covariates,
    read_indexer_entities,
    read_indexer_relationships,
    read_indexer_reports,
    read_indexer_text_units,
)
from graphrag.query.input.loaders.dfs import store_entity_semantic_embeddings

def process_entities(entity_df: pd.DataFrame, entity_embedding_df: pd.DataFrame, community_level: int) -> Dict:
    return read_indexer_entities(entity_df, entity_embedding_df, community_level)

def process_relationships(relationship_df: pd.DataFrame) -> List:
    return read_indexer_relationships(relationship_df)

def process_covariates(covariate_df: pd.DataFrame) -> List:
    return read_indexer_covariates(covariate_df)

def process_reports(report_df: pd.DataFrame, entity_df: pd.DataFrame, community_level: int) -> List:
    return read_indexer_reports(report_df, entity_df, community_level)

def process_text_units(text_unit_df: pd.DataFrame) -> List:
    return read_indexer_text_units(text_unit_df)

def store_embeddings(entities: Dict, vectorstore):
    return store_entity_semantic_embeddings(entities=entities, vectorstore=vectorstore)