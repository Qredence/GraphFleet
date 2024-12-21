"""
GraphFleet storage module that extends GraphRAG storage functionality.
"""

from graphrag.storage import create_storage as graphrag_create_storage
from graphrag.storage.base import BaseStorage

def create_storage(storage_config) -> BaseStorage:
    """
    Create a storage instance based on the provided configuration.
    This is a wrapper around GraphRAG's storage creation that allows for
    additional customization and features specific to GraphFleet.

    Args:
        storage_config: Configuration for the storage system

    Returns:
        BaseStorage: A storage instance
    """
    # For now, we're directly using GraphRAG's storage creation
    # In the future, we can add custom storage types or additional configuration here
    return graphrag_create_storage(storage_config)
