"""
GraphFleet storage utilities that extend GraphRAG storage functionality.
"""

from typing import Any

from graphrag.utils.storage import (
    load_table_from_storage as graphrag_load_table,
    write_table_to_storage as graphrag_write_table,
)
from graphrag.storage.base import BaseStorage

async def load_table_from_storage(filename: str, storage: BaseStorage) -> Any:
    """
    Load a table from storage.
    
    Args:
        filename: Name of the file to load
        storage: Storage instance to load from
        
    Returns:
        Loaded table data
    """
    return await graphrag_load_table(filename, storage)

async def write_table_to_storage(table: Any, filename: str, storage: BaseStorage) -> None:
    """
    Write a table to storage.
    
    Args:
        table: Table data to write
        filename: Name of the file to write to
        storage: Storage instance to write to
    """
    await graphrag_write_table(table, filename, storage)
