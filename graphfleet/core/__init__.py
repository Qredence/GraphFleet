from pathlib import Path
from typing import Dict, List, Optional, Union, AsyncGenerator
import os
from dotenv import load_dotenv
import pandas as pd

from graphrag.api.index import build_index, create_pipeline_config, GraphRagConfig
from graphrag.api.query import (
    global_search,
    global_search_streaming,
    local_search,
    local_search_streaming,
)
from graphrag.config.models.input_config import InputConfig
from graphrag.config.models.llm_parameters import LLMParameters
from graphrag.config.models.text_embedding_config import TextEmbeddingConfig
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class Document(BaseModel):
    id: str
    title: str
    content: str
    metadata: Optional[Dict] = None

class GraphFleet:
    def __init__(self, project_dir: Union[str, Path]):
        self.project_dir = Path(project_dir)
        
        # Get Azure OpenAI configuration
        api_key = os.getenv("GRAPHRAG_API_KEY")
        if not api_key:
            raise ValueError("GRAPHRAG_API_KEY environment variable must be set")
        
        # Configure LLM for Azure OpenAI
        llm_config = LLMParameters(
            api_key=api_key,
            type="azure_openai_chat",
            model=os.getenv("GRAPHRAG_LLM_MODEL", "gpt-4o-mini"),
            api_base=os.getenv("GRAPHRAG_API_BASE"),
            api_version=os.getenv("GRAPHRAG_API_VERSION"),
            deployment_name=os.getenv("GRAPHRAG_DEPLOYMENT_NAME")
        )
        
        self.config = GraphRagConfig(
            project_dir=str(self.project_dir),
            skip_workflows=["compute_communities", "create_final_community_reports"],
            input=InputConfig(
                type="file",
                file_type="text",
                base_dir=str(self.project_dir / "input"),
                file_pattern=".*\\.txt$"
            ),
            llm=llm_config,
            embeddings=TextEmbeddingConfig(
                llm=LLMParameters(
                    api_key=os.getenv("GRAPHRAG_EMBEDDING_KEY"),
                    type="azure_openai_embedding",
                    model=os.getenv("GRAPHRAG_EMBEDDING_MODEL", "text-embedding-3-large"),
                    api_base=os.getenv("GRAPHRAG_EMBEDDING_ENDPOINT"),
                    deployment_name=os.getenv("GRAPHRAG_EMBEDDING_DEPLOYMENT_NAME")
                )
            )
        )
        
    @staticmethod
    def init_project(project_dir: Union[str, Path]) -> None:
        """Initialize a new GraphFleet project directory."""
        project_dir = Path(project_dir)
        project_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize required subdirectories
        (project_dir / "input").mkdir(exist_ok=True)
        (project_dir / "index").mkdir(exist_ok=True)
        (project_dir / "cache").mkdir(exist_ok=True)
        
    async def add_document(self, doc_path: Union[str, Path]) -> None:
        """Add a document to the knowledge base."""
        doc_path = Path(doc_path)
        if not doc_path.exists():
            raise FileNotFoundError(f"Document not found: {doc_path}")
            
        # Read and process document
        content = doc_path.read_text()
        doc = Document(
            id=str(doc_path),
            title=doc_path.name,
            content=content
        )
        
        # Copy document to input directory
        input_dir = self.project_dir / "input"
        input_path = input_dir / doc_path.name
        input_path.write_text(content)
        
        # Add to GraphRAG indexer
        await build_index(
            config=self.config,
            run_id=doc.id
        )
        
    async def search(self, query: str, **kwargs) -> List[Dict]:
        """Search the knowledge base using natural language."""
        # Create DataFrames with required columns
        nodes_df = pd.DataFrame({
            'id': [],
            'name': [],
            'type': [],
            'level': [],
            'community': [],
            'content': []
        })
        
        entities_df = pd.DataFrame({
            'id': [],
            'name': [],
            'type': [],
            'level': [],
            'community': []
        })
        
        communities_df = pd.DataFrame({
            'id': [],
            'name': [],
            'level': [],
            'parent_id': []
        })
        
        community_reports_df = pd.DataFrame({
            'id': [],
            'name': [],
            'level': [],
            'parent_id': [],
            'content': []
        })
        
        results = await global_search(
            query=query,
            config=self.config,
            nodes=nodes_df,
            entities=entities_df,
            communities=communities_df,
            community_reports=community_reports_df,
            community_level=0,  # Start at top level
            dynamic_community_selection=False,  # Don't dynamically select communities
            response_type="text",  # Return text responses
            **kwargs
        )
        return results
        
    async def search_streaming(self, query: str, **kwargs) -> AsyncGenerator[str, None]:
        """Search the knowledge base using natural language with streaming responses."""
        # Create DataFrames with required columns
        nodes_df = pd.DataFrame({
            'id': [],
            'name': [],
            'type': [],
            'level': [],
            'community': [],
            'content': []
        })
        
        entities_df = pd.DataFrame({
            'id': [],
            'name': [],
            'type': [],
            'level': [],
            'community': []
        })
        
        communities_df = pd.DataFrame({
            'id': [],
            'name': [],
            'level': [],
            'parent_id': []
        })
        
        community_reports_df = pd.DataFrame({
            'id': [],
            'name': [],
            'level': [],
            'parent_id': [],
            'content': []
        })
        
        async for result in global_search_streaming(
            query=query,
            config=self.config,
            nodes=nodes_df,
            entities=entities_df,
            communities=communities_df,
            community_reports=community_reports_df,
            community_level=0,  # Start at top level
            dynamic_community_selection=False,  # Don't dynamically select communities
            response_type="text",  # Return text responses
            **kwargs
        ):
            yield result
        
    async def find_similar(self, doc_id: str, **kwargs) -> List[Dict]:
        """Find documents similar to the given document."""
        results = await local_search(
            query_id=doc_id,
            config=self.config,
            **kwargs
        )
        return results
        
    async def find_similar_streaming(self, doc_id: str, **kwargs) -> AsyncGenerator[str, None]:
        """Find documents similar to the given document with streaming responses."""
        async for result in local_search_streaming(
            query_id=doc_id,
            config=self.config,
            **kwargs
        ):
            yield result
