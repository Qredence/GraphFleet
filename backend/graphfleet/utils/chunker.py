"""Text chunking utilities for GraphFleet."""
from typing import List, Optional
import re

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200,
    min_chunk_size: int = 100,
    max_chunk_size: int = 2000,
    chunk_strategy: str = "sentence"
) -> List[str]:
    """
    Chunk text into smaller pieces with overlap.
    
    Args:
        text: Text to chunk
        chunk_size: Target size of each chunk
        overlap: Number of characters to overlap between chunks
        min_chunk_size: Minimum chunk size
        max_chunk_size: Maximum chunk size
        chunk_strategy: Chunking strategy ("sentence" or "word")
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
        
    if chunk_strategy == "sentence":
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            if current_size + sentence_size > max_chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_size
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
                
            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                # Keep last few sentences for overlap
                overlap_size = 0
                overlap_chunk = []
                for s in reversed(current_chunk):
                    s_size = len(s)
                    if overlap_size + s_size > overlap:
                        break
                    overlap_chunk.insert(0, s)
                    overlap_size += s_size
                current_chunk = overlap_chunk
                current_size = overlap_size
                
        if current_chunk and current_size >= min_chunk_size:
            chunks.append(" ".join(current_chunk))
            
    else:  # word-based chunking
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            
            if current_size + word_size > max_chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
                
            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                # Keep last few words for overlap
                overlap_size = 0
                overlap_chunk = []
                for w in reversed(current_chunk):
                    w_size = len(w) + 1
                    if overlap_size + w_size > overlap:
                        break
                    overlap_chunk.insert(0, w)
                    overlap_size += w_size
                current_chunk = overlap_chunk
                current_size = overlap_size
                
        if current_chunk and current_size >= min_chunk_size:
            chunks.append(" ".join(current_chunk))
            
    return chunks 