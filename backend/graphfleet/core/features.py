"""
GraphFleet Core Features

This module provides the core functionality for GraphFleet operations,
including graph analysis, search, and drift detection.
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime

import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from graphfleet.core.types import (
    QueryType,
    ChunkStrategy,
    EmbeddingConfig,
    QueryConfig,
    IndexConfig,
    GraphStats,
    SearchResult,
    DriftAnalysis,
)

class GraphFleetFeatures:
    """Core features for graph operations and analysis."""
    
    def __init__(self, storage):
        """Initialize GraphFleet features.
        
        Args:
            storage: Storage backend instance
        """
        self.storage = storage
        self.graph = nx.Graph()
        self._load_graph()
    
    def _load_graph(self) -> None:
        """Load the knowledge graph from storage."""
        # Load nodes and edges from storage
        nodes = self.storage.get_nodes()
        edges = self.storage.get_edges()
        
        # Build networkx graph
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
    
    async def batch_query(
        self,
        queries: List[str],
        query_type: str = "semantic",
        batch_size: int = 10,
        **options: Any
    ) -> List[Dict[str, Any]]:
        """Process multiple queries in batch.
        
        Args:
            queries: List of queries to process
            query_type: Type of queries to perform
            batch_size: Number of queries to process in parallel
            **options: Additional query options
            
        Returns:
            List of query results
            
        Raises:
            ValueError: If query_type is invalid
        """
        if query_type not in QueryType.__members__:
            raise ValueError(f"Invalid query type: {query_type}")
        
        # Process queries in batches
        results = []
        for i in range(0, len(queries), batch_size):
            batch = queries[i:i + batch_size]
            batch_results = await self._process_batch(
                batch,
                query_type,
                **options
            )
            results.extend(batch_results)
        
        return results
    
    async def knowledge_graph_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge graph.
        
        Returns:
            Dict containing graph statistics
        """
        stats = {
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "avg_degree": float(
                2 * self.graph.number_of_edges()
            ) / self.graph.number_of_nodes(),
            "density": nx.density(self.graph),
            "communities": len(list(nx.community.greedy_modularity_communities(self.graph))),
            "updated_at": datetime.now().isoformat()
        }
        return stats
    
    async def analyze_drift(
        self,
        query: str,
        window_size: int = 100
    ) -> DriftAnalysis:
        """Analyze concept drift over time.
        
        Args:
            query: Query for drift analysis
            window_size: Size of the analysis window
            
        Returns:
            DriftAnalysis object with results
        """
        # Get temporal embeddings
        embeddings = await self.storage.get_temporal_embeddings(
            query,
            window_size
        )
        
        if not embeddings:
            return DriftAnalysis(
                query=query,
                window_size=window_size,
                drift_score=0.0,
                trends=[],
                metadata={"error": "No temporal data available"}
            )
        
        # Calculate drift scores
        scores = []
        for i in range(len(embeddings) - 1):
            similarity = cosine_similarity(
                embeddings[i].reshape(1, -1),
                embeddings[i + 1].reshape(1, -1)
            )[0][0]
            scores.append(1 - similarity)
        
        # Calculate overall drift score
        drift_score = np.mean(scores) if scores else 0.0
        
        # Get timestamps
        timestamps = await self.storage.get_temporal_timestamps(
            query,
            window_size
        )
        
        # Build trends
        trends = [
            {
                "timestamp": ts.isoformat(),
                "score": score
            }
            for ts, score in zip(timestamps, scores)
        ]
        
        return DriftAnalysis(
            query=query,
            window_size=window_size,
            drift_score=float(drift_score),
            trends=trends,
            metadata={
                "method": "cosine_similarity",
                "num_points": len(scores)
            }
        )
    
    async def _process_batch(
        self,
        queries: List[str],
        query_type: str,
        **options: Any
    ) -> List[Dict[str, Any]]:
        """Process a batch of queries.
        
        Args:
            queries: List of queries to process
            query_type: Type of queries to perform
            **options: Additional query options
            
        Returns:
            List of query results
        """
        # Get query embeddings
        embeddings = await self.storage.get_embeddings(queries)
        
        # Process based on query type
        if query_type == QueryType.SEMANTIC:
            return await self._semantic_search_batch(
                queries,
                embeddings,
                **options
            )
        elif query_type == QueryType.LOCAL:
            return await self._local_search_batch(
                queries,
                embeddings,
                **options
            )
        elif query_type == QueryType.GLOBAL:
            return await self._global_search_batch(
                queries,
                embeddings,
                **options
            )
        else:  # DRIFT
            return await self._drift_search_batch(
                queries,
                embeddings,
                **options
            )
    
    async def _semantic_search_batch(
        self,
        queries: List[str],
        embeddings: np.ndarray,
        **options: Any
    ) -> List[Dict[str, Any]]:
        """Perform semantic search for a batch of queries.
        
        Args:
            queries: List of queries
            embeddings: Query embeddings
            **options: Search options
            
        Returns:
            List of search results
        """
        k = options.get("k", 10)
        threshold = options.get("threshold", 0.5)
        
        results = []
        for query, embedding in zip(queries, embeddings):
            # Get similar documents
            docs = await self.storage.search_similar(
                embedding,
                k=k,
                threshold=threshold
            )
            
            # Format results
            query_results = [
                SearchResult(
                    id=doc["id"],
                    score=float(doc["score"]),
                    content=doc["content"],
                    metadata=doc.get("metadata", {})
                )
                for doc in docs
            ]
            
            results.append({
                "query": query,
                "results": [result.dict() for result in query_results],
                "metadata": {
                    "k": k,
                    "threshold": threshold
                }
            })
        
        return results
