"""
Text chunking functionality for GraphFleet.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any

from graphrag.utils import split_text
from .types import Document, Chunk

class TextProcessor:
    """
    Process text documents into chunks suitable for indexing.
    
    Args:
        chunk_size: Maximum chunk size in tokens
        overlap: Number of tokens to overlap between chunks
        split_method: Method to use for splitting text
        **kwargs: Additional configuration options
    """
    
    def __init__(
        self,
        chunk_size: int = 512,
        overlap: int = 50,
        split_method: str = "markdown",
        **kwargs
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.split_method = split_method
        self.config = kwargs
    
    def process_text(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """
        Process a text string into chunks.
        
        Args:
            text: Text content to process
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of chunks
        """
        chunks = split_text(
            text,
            chunk_size=self.chunk_size,
            overlap=self.overlap,
            split_method=self.split_method
        )
        
        return [
            Chunk(
                id=f"chunk_{i}",
                content=chunk,
                document_id=metadata.get("document_id", ""),
                start_idx=i * (self.chunk_size - self.overlap),
                end_idx=(i + 1) * self.chunk_size,
                metadata=metadata or {}
            )
            for i, chunk in enumerate(chunks)
        ]
    
    def process_file(
        self,
        file_path: Path,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """
        Process a file into chunks.
        
        Args:
            file_path: Path to the file
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of chunks
        """
        with open(file_path, "r") as f:
            text = f.read()
        
        metadata = metadata or {}
        metadata["file_path"] = str(file_path)
        metadata["document_id"] = file_path.stem
        
        return self.process_text(text, metadata)
    
    def process_directory(
        self,
        dir_path: Path,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Chunk]:
        """
        Process all files in a directory.
        
        Args:
            dir_path: Path to the directory
            metadata: Optional metadata to attach to chunks
            
        Returns:
            List of chunks
        """
        chunks = []
        for file_path in dir_path.glob("**/*"):
            if file_path.is_file():
                file_metadata = metadata.copy() if metadata else {}
                file_metadata["directory"] = str(dir_path)
                chunks.extend(self.process_file(file_path, file_metadata))
        return chunks
