"""
Base GraphFleet implementation.
"""

from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from graphrag import GraphRAG
from graphrag.utils import load_settings

from .types import (
    Document,
    Chunk,
    QueryType,
    IndexType,
    RetrievalType,
    QueryResult,
    IndexConfig,
    QueryConfig,
)

class GraphFleet:
    """
    GraphFleet main class that wraps GraphRAG functionality with enhanced features.
    
    Args:
        project_path: Path to the project directory
        config: Optional configuration dictionary
        
    Attributes:
        project_path: Path to project directory
        graph_rag: GraphRAG instance
        config: Configuration dictionary
    """
    
    def __init__(
        self,
        project_path: Union[str, Path],
        config: Optional[Dict[str, Any]] = None
    ):
        self.project_path = Path(project_path)
        self.config = config or {}
        self._load_graphrag()
    
    @classmethod
    def init_project(
        cls,
        project_path: Union[str, Path],
        **kwargs
    ) -> "GraphFleet":
        """
        Initialize a new GraphFleet project.
        
        Args:
            project_path: Path where to create the project
            **kwargs: Additional configuration options
            
        Returns:
            GraphFleet instance
        """
        project_path = Path(project_path)
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create directory structure
        (project_path / "raw").mkdir(exist_ok=True)
        (project_path / "processed").mkdir(exist_ok=True)
        (project_path / "indexes").mkdir(exist_ok=True)
        
        # Initialize GraphRAG
        settings = load_settings()
        settings.update(kwargs)
        
        return cls(project_path, config=settings)
    
    async def create_index(
        self,
        config: Optional[IndexConfig] = None,
        **kwargs
    ) -> None:
        """
        Create or update the index.
        
        Args:
            config: Index configuration
            **kwargs: Additional indexing options
        """
        config = config or IndexConfig(**kwargs)
        await self.graph_rag.create_index(
            index_type=config.index_type.value,
            dimension=config.dimension,
            metric=config.metric,
            **config.additional_config
        )
    
    async def query(
        self,
        query_text: str,
        config: Optional[QueryConfig] = None,
        **kwargs
    ) -> QueryResult:
        """
        Process a query.
        
        Args:
            query_text: Query string
            config: Query configuration
            **kwargs: Additional query options
            
        Returns:
            Query result
        """
        config = config or QueryConfig(**kwargs)
        
        result = await self.graph_rag.query(
            query_text,
            query_type=config.query_type.value,
            retrieval_type=config.retrieval_type.value,
            max_results=config.max_results,
            threshold=config.threshold,
            context_window=config.context_window,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            **config.additional_config
        )
        
        return QueryResult(
            result=result["answer"],
            confidence=result.get("confidence", 0.0),
            sources=[Document(**doc) for doc in result.get("sources", [])],
            metadata=result.get("metadata", {})
        )
    
    def _load_graphrag(self) -> None:
        """Load and initialize GraphRAG."""
        self.graph_rag = GraphRAG(
            project_dir=str(self.project_path),
            **self.config
        )
