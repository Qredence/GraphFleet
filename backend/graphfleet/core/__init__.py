"""
Core functionality for GraphFleet, wrapping GraphRAG's initialization, indexing, and querying capabilities.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from graphrag.init import init_project as graphrag_init
from graphrag.index import create_index as graphrag_index
from graphrag.query import (
    query as graphrag_query,
    query_local as graphrag_query_local,
    query_global as graphrag_query_global,
    query_drift as graphrag_query_drift,
    query_dynamic as graphrag_query_dynamic,
)
from graphrag.autoprompt import create_prompts as graphrag_autoprompt

class GraphFleet:
    """Main GraphFleet class that provides access to all GraphRAG functionality."""
    
    def __init__(self, project_dir: Union[str, Path]):
        self.project_dir = Path(project_dir)
        
    @staticmethod
    def init_project(project_dir: Union[str, Path], **kwargs) -> None:
        """Initialize a new GraphFleet project."""
        graphrag_init(Path(project_dir), **kwargs)
    
    def create_index(self, **kwargs) -> None:
        """Create index for the current project."""
        graphrag_index(self.project_dir, **kwargs)
    
    def create_prompts(self, **kwargs) -> None:
        """Automatically generate prompts for the current project."""
        graphrag_autoprompt(self.project_dir, **kwargs)
    
    def query(self, query_text: str, **kwargs) -> Dict[str, Any]:
        """Standard query using GraphRAG."""
        return graphrag_query(self.project_dir, query_text, **kwargs)
    
    def query_local(self, query_text: str, **kwargs) -> Dict[str, Any]:
        """Local-focused query using GraphRAG."""
        return graphrag_query_local(self.project_dir, query_text, **kwargs)
    
    def query_global(self, query_text: str, **kwargs) -> Dict[str, Any]:
        """Global-focused query using GraphRAG."""
        return graphrag_query_global(self.project_dir, query_text, **kwargs)
    
    def query_drift(self, query_text: str, **kwargs) -> Dict[str, Any]:
        """Drift analysis query using GraphRAG."""
        return graphrag_query_drift(self.project_dir, query_text, **kwargs)
    
    def query_dynamic(self, query_text: str, **kwargs) -> Dict[str, Any]:
        """Dynamic query using GraphRAG."""
        return graphrag_query_dynamic(self.project_dir, query_text, **kwargs)
