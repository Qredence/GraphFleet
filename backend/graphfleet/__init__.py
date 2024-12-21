"""
GraphFleet - A Python package for graph-based RAG applications.
Built on top of GraphRAG with enhanced features and improved usability.
"""

from .core.base import GraphFleet
from .core.types import (
    QueryType,
    IndexType,
    RetrievalType,
    Document,
    Chunk,
    QueryResult,
    IndexConfig,
    QueryConfig,
)
from .indexing.chunker import TextProcessor
from .prompting.generator import PromptGenerator
from .querying.optimizer import QueryOptimizer, OptimizationResult

__version__ = "1.0.1"
__author__ = "GraphFleet Team"

__all__ = [
    "GraphFleet",
    "QueryType",
    "IndexType",
    "RetrievalType",
    "Document",
    "Chunk",
    "QueryResult",
    "IndexConfig",
    "QueryConfig",
    "TextProcessor",
    "PromptGenerator",
    "QueryOptimizer",
    "OptimizationResult",
]
