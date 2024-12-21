"""
GraphFleet indexing module that extends GraphRAG indexing functionality.
"""

from typing import Any, Dict

from graphrag.index.create_pipeline_config import create_pipeline_config as graphrag_create_pipeline_config

def create_pipeline_config(config: Dict[str, Any]):
    """
    Create a pipeline configuration from the provided config dictionary.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Pipeline configuration object
    """
    return graphrag_create_pipeline_config(config)
