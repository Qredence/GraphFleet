from typing import List, Dict, Optional
from pathlib import Path
import pandas as pd
from graphrag.api.index import build_index

class TextProcessor:
    """Process text documents for indexing."""
    
    def __init__(self, 
                 project_dir: Path,
                 chunk_size: int = 512,
                 overlap: int = 50,
                 split_method: str = "txt"):
        """Initialize text processor with chunking parameters.
        
        Args:
            project_dir: Root directory for the project
            chunk_size: Maximum chunk size in tokens
            overlap: Number of tokens to overlap between chunks
            split_method: Method to split text ("txt" or "md")
        """
        self.project_dir = project_dir
        self.input_dir = project_dir / "input"
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.split_method = split_method
    
    def process_document(self, file_path: Path) -> List[Dict]:
        """Process a single document into chunks.
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of dictionaries containing chunk information
        """
        content = file_path.read_text()
        
        # Simple text splitting for now
        # TODO: Implement more sophisticated chunking with tiktoken
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            chunks.append({
                "id": f"{file_path}_{i}",
                "title": f"{file_path.name} (chunk {i})",
                "content": chunk,
                "source": str(file_path)
            })
        
        return chunks
    
    def process_directory(self, directory: Path) -> List[Dict]:
        """Process all documents in a directory.
        
        Args:
            directory: Directory containing documents
            
        Returns:
            List of dictionaries containing chunk information
        """
        all_chunks = []
        for file_path in directory.glob("**/*.*"):
            if file_path.suffix.lower() in [".txt", ".md"]:
                chunks = self.process_document(file_path)
                all_chunks.extend(chunks)
        return all_chunks

class GraphBuilder:
    """Build knowledge graph from processed documents."""
    
    def __init__(self, project_dir: Path):
        """Initialize graph builder.
        
        Args:
            project_dir: Root directory for the project
        """
        self.project_dir = project_dir
        self.index_dir = project_dir / "index"
        self.index_dir.mkdir(parents=True, exist_ok=True)
    
    async def build_graph(self, documents: List[Dict], config: Dict) -> None:
        """Build knowledge graph from documents.
        
        Args:
            documents: List of document chunks
            config: Configuration for GraphRAG
        """
        # Convert documents to DataFrame
        df = pd.DataFrame(documents)
        
        # Build index using GraphRAG
        await build_index(
            config=config,
            run_id=str(self.project_dir),
            documents=df
        )
