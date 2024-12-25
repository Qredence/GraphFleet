"""
GraphFleet Storage Backend

This module provides the storage backend for GraphFleet operations.
It handles data persistence, indexing, and retrieval.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import networkx as nx
import pandas as pd

from graphfleet.core.types import (
    IndexConfig,
    SearchResult,
    DriftAnalysis,
)

class StorageBackend:
    """Storage backend for GraphFleet."""
    
    def __init__(self, project_path: Path):
        """Initialize storage backend.
        
        Args:
            project_path: Path to project directory
        """
        self.project_path = project_path
        self.data_dir = project_path / "data"
        self.index_dir = project_path / "index"
        self.config_dir = project_path / "config"
        
        # Load components
        self._load_components()
    
    def _load_components(self) -> None:
        """Load storage components."""
        # Load embedding model
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-mpnet-base-v2"
        )
        
        # Load index if exists
        index_path = self.index_dir / "faiss.index"
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
        else:
            self.index = None
        
        # Load graph if exists
        graph_path = self.data_dir / "graph.gpickle"
        if graph_path.exists():
            self.graph = nx.read_gpickle(graph_path)
        else:
            self.graph = nx.Graph()
        
        # Load document store
        docs_path = self.data_dir / "documents.parquet"
        if docs_path.exists():
            self.documents = pd.read_parquet(docs_path)
        else:
            self.documents = pd.DataFrame(
                columns=["id", "content", "embedding", "metadata"]
            )
    
    async def create_index(self, config: IndexConfig) -> None:
        """Create search index.
        
        Args:
            config: Index configuration
        """
        # Initialize FAISS index
        dimension = config.embedding_config.dimension
        self.index = faiss.IndexFlatIP(dimension)
        
        # Add existing documents
        if not self.documents.empty:
            embeddings = np.stack(self.documents["embedding"].values)
            self.index.add(embeddings)
        
        # Save index
        faiss.write_index(
            self.index,
            str(self.index_dir / "faiss.index")
        )
    
    async def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Text embedding
        """
        return self.embedding_model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    
    async def search_similar(
        self,
        embedding: np.ndarray,
        k: int = 10,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Search for similar documents.
        
        Args:
            embedding: Query embedding
            k: Number of results
            threshold: Similarity threshold
            
        Returns:
            List of similar documents
        """
        if self.index is None:
            return []
        
        # Search index
        scores, indices = self.index.search(
            embedding.reshape(1, -1),
            k
        )
        
        # Filter by threshold
        mask = scores[0] >= threshold
        indices = indices[0][mask]
        scores = scores[0][mask]
        
        # Get documents
        results = []
        for idx, score in zip(indices, scores):
            doc = self.documents.iloc[idx]
            results.append({
                "id": doc["id"],
                "score": float(score),
                "content": doc["content"],
                "metadata": doc["metadata"]
            })
        
        return results
    
    async def get_local_subgraph(
        self,
        embedding: np.ndarray,
        max_hops: int = 2,
        max_nodes: int = 100
    ) -> nx.Graph:
        """Get local subgraph around query.
        
        Args:
            embedding: Query embedding
            max_hops: Maximum number of hops
            max_nodes: Maximum number of nodes
            
        Returns:
            Local subgraph
        """
        # Find nearest node
        scores, indices = self.index.search(
            embedding.reshape(1, -1),
            1
        )
        start_node = self.documents.iloc[indices[0][0]]["id"]
        
        # Get ego network
        subgraph = nx.ego_graph(
            self.graph,
            start_node,
            radius=max_hops,
            undirected=True
        )
        
        # Limit size
        if len(subgraph) > max_nodes:
            nodes = list(subgraph.nodes())[:max_nodes]
            subgraph = subgraph.subgraph(nodes)
        
        return subgraph
    
    async def search_subgraph(
        self,
        subgraph: nx.Graph,
        embedding: np.ndarray,
        k: int = 10,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Search within subgraph.
        
        Args:
            subgraph: Graph to search in
            embedding: Query embedding
            k: Number of results
            threshold: Similarity threshold
            
        Returns:
            List of search results
        """
        # Get node embeddings
        node_ids = list(subgraph.nodes())
        mask = self.documents["id"].isin(node_ids)
        embeddings = np.stack(self.documents[mask]["embedding"].values)
        
        # Calculate similarities
        similarities = np.dot(embeddings, embedding)
        
        # Get top k
        indices = np.argsort(similarities)[-k:][::-1]
        mask = similarities[indices] >= threshold
        indices = indices[mask]
        
        # Get documents
        results = []
        for idx in indices:
            doc = self.documents[mask].iloc[idx]
            results.append({
                "id": doc["id"],
                "score": float(similarities[idx]),
                "content": doc["content"],
                "metadata": doc["metadata"]
            })
        
        return results
    
    async def get_communities(
        self,
        level: int = 1
    ) -> Dict[str, int]:
        """Get community assignments.
        
        Args:
            level: Community hierarchy level
            
        Returns:
            Dict mapping node IDs to community IDs
        """
        # Get communities
        communities = list(
            nx.community.louvain_communities(
                self.graph,
                resolution=1.0 / level
            )
        )
        
        # Create mapping
        assignments = {}
        for i, community in enumerate(communities):
            for node in community:
                assignments[node] = i
        
        return assignments
    
    async def search_communities(
        self,
        communities: Dict[str, int],
        embedding: np.ndarray,
        k: int = 10,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Search across communities.
        
        Args:
            communities: Community assignments
            embedding: Query embedding
            k: Number of results
            threshold: Similarity threshold
            
        Returns:
            List of search results
        """
        results = []
        
        # Search in each community
        for community_id in set(communities.values()):
            # Get community nodes
            node_ids = [
                node
                for node, comm in communities.items()
                if comm == community_id
            ]
            
            # Get embeddings
            mask = self.documents["id"].isin(node_ids)
            embeddings = np.stack(self.documents[mask]["embedding"].values)
            
            # Calculate similarities
            similarities = np.dot(embeddings, embedding)
            
            # Get top results
            indices = np.argsort(similarities)[-k:][::-1]
            mask = similarities[indices] >= threshold
            indices = indices[mask]
            
            # Add documents
            for idx in indices:
                doc = self.documents[mask].iloc[idx]
                results.append({
                    "id": doc["id"],
                    "score": float(similarities[idx]),
                    "content": doc["content"],
                    "metadata": {
                        **doc["metadata"],
                        "community_id": community_id
                    }
                })
        
        # Sort by score and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:k]
    
    async def get_temporal_data(
        self,
        window: str = "1d"
    ) -> pd.DataFrame:
        """Get temporal document data.
        
        Args:
            window: Time window (e.g., "1d", "7d")
            
        Returns:
            DataFrame with temporal data
        """
        # Parse window
        unit = window[-1]
        value = int(window[:-1])
        
        # Get cutoff time
        now = pd.Timestamp.now()
        if unit == "d":
            cutoff = now - pd.Timedelta(days=value)
        elif unit == "h":
            cutoff = now - pd.Timedelta(hours=value)
        else:
            raise ValueError(f"Invalid time window: {window}")
        
        # Filter documents
        mask = pd.to_datetime(
            self.documents["metadata"].apply(
                lambda x: x.get("timestamp")
            )
        ) >= cutoff
        
        return self.documents[mask]
    
    async def analyze_temporal_drift(
        self,
        temporal_data: pd.DataFrame,
        embedding: np.ndarray,
        k: int = 10,
        threshold: float = 0.5
    ) -> Dict[str, Any]:
        """Analyze temporal drift.
        
        Args:
            temporal_data: Temporal document data
            embedding: Query embedding
            k: Number of results
            threshold: Similarity threshold
            
        Returns:
            Dict with drift analysis results
        """
        if temporal_data.empty:
            return {
                "documents": [],
                "drift_score": 0.0,
                "coverage": 0.0
            }
        
        # Get embeddings
        embeddings = np.stack(temporal_data["embedding"].values)
        
        # Calculate similarities
        similarities = np.dot(embeddings, embedding)
        
        # Get drift score
        drift_score = 1.0 - np.mean(similarities)
        
        # Get top results
        indices = np.argsort(similarities)[-k:][::-1]
        mask = similarities[indices] >= threshold
        indices = indices[mask]
        
        # Get documents
        documents = []
        for idx in indices:
            doc = temporal_data.iloc[idx]
            documents.append({
                "id": doc["id"],
                "score": float(similarities[idx]),
                "content": doc["content"],
                "metadata": doc["metadata"]
            })
        
        return {
            "documents": documents,
            "drift_score": float(drift_score),
            "coverage": len(temporal_data) / len(self.documents)
        } 