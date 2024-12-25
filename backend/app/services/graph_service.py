"""
GraphFleet Service Layer

This module provides the service layer for GraphFleet operations,
handling the business logic between the API endpoints and the core library.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from graphfleet.core import GraphFleet
from graphfleet.core.features import GraphFleetFeatures
from app.models import GraphStats, QueryResponse

class GraphService:
    """Service class for handling graph operations."""
    
    def __init__(self, project_path: str):
        """Initialize the graph service.
        
        Args:
            project_path: Path to the GraphFleet project
        """
        self.project_path = project_path
        self.graph_fleet = GraphFleet(project_path)
        self.features = GraphFleetFeatures(self.graph_fleet.storage)

    async def init_project(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Initialize a new project.
        
        Args:
            options: Additional initialization options
        
        Raises:
            Exception: If project initialization fails
        """
        await GraphFleet.init_project(self.project_path, **(options or {}))

    async def create_index(self, options: Optional[Dict[str, Any]] = None) -> None:
        """Create index for the current project.
        
        Args:
            options: Additional indexing options
            
        Raises:
            Exception: If index creation fails
        """
        await self.graph_fleet.create_index(**(options or {}))

    async def query(
        self,
        query_text: str,
        query_type: str = "semantic",
        options: Optional[Dict[str, Any]] = None
    ) -> QueryResponse:
        """Process a query using the specified query type.
        
        Args:
            query_text: The query to process
            query_type: Type of query to perform
            options: Additional query options
            
        Returns:
            QueryResponse containing results and metadata
            
        Raises:
            Exception: If query processing fails
        """
        result = await self.graph_fleet.query(
            query_text,
            query_type=query_type,
            **(options or {})
        )
        
        return QueryResponse(
            result=result,
            metadata={
                "query_type": query_type,
                "options_used": options,
                "timestamp": datetime.now().isoformat()
            }
        )

    async def batch_query(
        self,
        queries: List[str],
        query_type: str = "semantic",
        batch_size: int = 10,
        options: Optional[Dict[str, Any]] = None
    ) -> List[QueryResponse]:
        """Process multiple queries in batch.
        
        Args:
            queries: List of queries to process
            query_type: Type of queries to perform
            batch_size: Number of queries to process in parallel
            options: Additional query options
            
        Returns:
            List of QueryResponse objects
            
        Raises:
            Exception: If batch processing fails
        """
        results = await self.features.batch_query(
            queries,
            query_type=query_type,
            batch_size=batch_size,
            **(options or {})
        )
        
        return [
            QueryResponse(
                result=result,
                metadata={
                    "query_type": query_type,
                    "options_used": options,
                    "timestamp": datetime.now().isoformat()
                }
            )
            for result in results
        ]

    async def get_stats(self) -> GraphStats:
        """Get statistics about the knowledge graph.
        
        Returns:
            GraphStats object containing graph statistics
            
        Raises:
            Exception: If stats collection fails
        """
        stats = await self.features.knowledge_graph_stats()
        return GraphStats(**stats)

    async def semantic_search(
        self,
        query_text: str,
        k: int = 10,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """Perform semantic search over the document collection.
        
        Args:
            query_text: Search query
            k: Number of results to return
            threshold: Similarity threshold
            
        Returns:
            Dict containing search results and metadata
            
        Raises:
            Exception: If search fails
        """
        results = await self.graph_fleet.semantic_search(
            query_text,
            k=k,
            threshold=threshold
        )
        
        return {
            "results": results,
            "metadata": {
                "k": k,
                "threshold": threshold,
                "timestamp": datetime.now().isoformat()
            }
        }

    async def analyze_drift(
        self,
        query_text: str,
        window_size: int = 100
    ) -> Dict[str, Any]:
        """Analyze concept drift in the knowledge graph.
        
        Args:
            query_text: Query for drift analysis
            window_size: Size of the analysis window
            
        Returns:
            Dict containing drift analysis results
            
        Raises:
            Exception: If analysis fails
        """
        drift_stats = await self.features.analyze_drift(
            query_text,
            window_size=window_size
        )
        
        return {
            "drift_stats": drift_stats,
            "metadata": {
                "window_size": window_size,
                "timestamp": datetime.now().isoformat()
            }
        } 