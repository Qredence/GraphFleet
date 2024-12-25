"""
GraphFleet - A powerful graph-based knowledge management and query system.

This package provides tools for building and querying knowledge graphs,
with features for semantic search, concept drift analysis, and more.
"""

__version__ = "0.7.0"
__author__ = "GraphFleet Team"
__email__ = "team@graphfleet.io"

from graphfleet.core import GraphFleet
from graphfleet.core.features import GraphFleetFeatures
from graphfleet.core.types import (
    QueryType,
    ChunkStrategy,
    EmbeddingConfig,
    QueryConfig,
    IndexConfig,
)

__all__ = [
    "GraphFleet",
    "GraphFleetFeatures",
    "QueryType",
    "ChunkStrategy",
    "EmbeddingConfig",
    "QueryConfig",
    "IndexConfig",
] 