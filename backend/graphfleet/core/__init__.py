"""
GraphFleet Core Module

This module provides the main GraphFleet class and core functionality.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import yaml

from graphfleet.core.types import (
    QueryType,
    ChunkStrategy,
    EmbeddingConfig,
    QueryConfig,
    IndexConfig,
)
from graphfleet.core.features import GraphFleetFeatures
from graphfleet.core.storage import StorageBackend

class GraphFleet:
    """Main class for GraphFleet operations."""
    
    def __init__(self, project_path: str):
        """Initialize GraphFleet.
        
        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self.storage = self._init_storage()
        self.features = GraphFleetFeatures(self.storage)
    
    @staticmethod
    async def init_project(
        project_path: str,
        **options: Any
    ) -> None:
        """Initialize a new project.
        
        Args:
            project_path: Path where the project will be initialized
            **options: Additional initialization options
            
        Raises:
            ValueError: If project path is invalid
            FileExistsError: If project already exists
        """
        path = Path(project_path)
        
        # Validate path
        if not path.parent.exists():
            raise ValueError(f"Parent directory does not exist: {path.parent}")
        
        if path.exists():
            raise FileExistsError(f"Project already exists at: {path}")
        
        # Create project structure
        path.mkdir(parents=True)
        (path / "data").mkdir()
        (path / "index").mkdir()
        (path / "config").mkdir()
        
        # Create default config
        config = {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            **options
        }
        
        with open(path / "config" / "settings.yaml", "w") as f:
            yaml.safe_dump(config, f)
    
    async def create_index(
        self,
        **options: Any
    ) -> None:
        """Create index for the current project.
        
        Args:
            **options: Additional indexing options
            
        Raises:
            ValueError: If project is not initialized
        """
        if not self._is_initialized():
            raise ValueError(f"Project not initialized at: {self.project_path}")
        
        # Get index configuration
        config = IndexConfig(**options)
        
        # Create index
        await self.storage.create_index(config)
    
    async def query(
        self,
        query_text: str,
        query_type: str = "semantic",
        **options: Any
    ) -> Dict[str, Any]:
        """Process a query.
        
        Args:
            query_text: Query to process
            query_type: Type of query to perform
            **options: Additional query options
            
        Returns:
            Dict containing query results
            
        Raises:
            ValueError: If query_type is invalid
        """
        if query_type not in QueryType.__members__:
            raise ValueError(f"Invalid query type: {query_type}")
        
        # Get query configuration
        config = QueryConfig(**options)
        
        # Process query
        if query_type == QueryType.SEMANTIC:
            return await self._semantic_search(query_text, config)
        elif query_type == QueryType.LOCAL:
            return await self._local_search(query_text, config)
        elif query_type == QueryType.GLOBAL:
            return await self._global_search(query_text, config)
        else:  # DRIFT
            return await self._drift_search(query_text, config)
    
    def _init_storage(self) -> StorageBackend:
        """Initialize storage backend.
        
        Returns:
            Storage backend instance
        """
        return StorageBackend(self.project_path)
    
    def _is_initialized(self) -> bool:
        """Check if project is initialized.
        
        Returns:
            True if project is initialized, False otherwise
        """
        return (
            self.project_path.exists()
            and (self.project_path / "data").exists()
            and (self.project_path / "index").exists()
            and (self.project_path / "config").exists()
        )
    
    async def _semantic_search(
        self,
        query_text: str,
        config: QueryConfig
    ) -> Dict[str, Any]:
        """Perform semantic search.
        
        Args:
            query_text: Query text
            config: Query configuration
            
        Returns:
            Dict containing search results
        """
        # Get query embedding
        embedding = await self.storage.get_embedding(query_text)
        
        # Search similar documents
        docs = await self.storage.search_similar(
            embedding,
            k=config.max_results,
            threshold=config.similarity_threshold
        )
        
        return {
            "query": query_text,
            "results": docs,
            "metadata": {
                "query_type": "semantic",
                "config": config.dict()
            }
        }
    
    async def _local_search(
        self,
        query_text: str,
        config: QueryConfig
    ) -> Dict[str, Any]:
        """Perform local graph search.
        
        Args:
            query_text: Query text
            config: Query configuration
            
        Returns:
            Dict containing search results
        """
        # Get query embedding
        embedding = await self.storage.get_embedding(query_text)
        
        # Get local subgraph
        subgraph = await self.storage.get_local_subgraph(
            embedding,
            max_hops=config.options.get("max_hops", 2),
            max_nodes=config.options.get("max_nodes", 100)
        )
        
        # Search in subgraph
        docs = await self.storage.search_subgraph(
            subgraph,
            embedding,
            k=config.max_results,
            threshold=config.similarity_threshold
        )
        
        return {
            "query": query_text,
            "results": docs,
            "metadata": {
                "query_type": "local",
                "config": config.dict(),
                "subgraph_size": len(subgraph)
            }
        }
    
    async def _global_search(
        self,
        query_text: str,
        config: QueryConfig
    ) -> Dict[str, Any]:
        """Perform global graph search.
        
        Args:
            query_text: Query text
            config: Query configuration
            
        Returns:
            Dict containing search results
        """
        # Get query embedding
        embedding = await self.storage.get_embedding(query_text)
        
        # Get community assignments
        communities = await self.storage.get_communities(
            level=config.options.get("community_level", 1)
        )
        
        # Search across communities
        docs = await self.storage.search_communities(
            communities,
            embedding,
            k=config.max_results,
            threshold=config.similarity_threshold
        )
        
        return {
            "query": query_text,
            "results": docs,
            "metadata": {
                "query_type": "global",
                "config": config.dict(),
                "num_communities": len(set(communities.values()))
            }
        }
    
    async def _drift_search(
        self,
        query_text: str,
        config: QueryConfig
    ) -> Dict[str, Any]:
        """Perform drift-aware search.
        
        Args:
            query_text: Query text
            config: Query configuration
            
        Returns:
            Dict containing search results
        """
        # Get query embedding
        embedding = await self.storage.get_embedding(query_text)
        
        # Get temporal data
        temporal_data = await self.storage.get_temporal_data(
            window=config.options.get("time_window", "1d")
        )
        
        # Analyze drift
        drift_results = await self.storage.analyze_temporal_drift(
            temporal_data,
            embedding,
            k=config.max_results,
            threshold=config.similarity_threshold
        )
        
        return {
            "query": query_text,
            "results": drift_results["documents"],
            "metadata": {
                "query_type": "drift",
                "config": config.dict(),
                "drift_score": drift_results["drift_score"],
                "temporal_coverage": drift_results["coverage"]
            }
        }
