"""Example script demonstrating how to index a text file using GraphFleet."""
import asyncio
from pathlib import Path
from typing import List

from graphfleet import GraphFleetBase
from graphfleet.utils.chunker import chunk_text

async def index_text_file(
    file_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> None:
    """Index a text file using GraphFleet.
    
    Args:
        file_path: Path to the text file to index
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
    """
    # Initialize GraphFleet
    graph_fleet = GraphFleetBase()
    
    # Read the text file
    text = Path(file_path).read_text()
    
    # Chunk the text
    chunks = chunk_text(
        text=text,
        chunk_size=chunk_size,
        overlap=chunk_overlap,
        chunk_strategy="sentence"
    )
    
    print(f"Created {len(chunks)} chunks from text")
    
    # Index each chunk
    for i, chunk in enumerate(chunks):
        await graph_fleet.index_text(
            text=chunk,
            metadata={
                "source": file_path,
                "chunk_id": i,
                "total_chunks": len(chunks)
            }
        )
        print(f"Indexed chunk {i+1}/{len(chunks)}")
    
    print("Indexing complete!")
    
    # Example search
    query = "What is the main topic discussed in this text?"
    result = await graph_fleet.search(query)
    print(f"\nTest Query: {query}")
    print(f"Result: {result}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Index a text file using GraphFleet")
    parser.add_argument("file_path", help="Path to the text file to index")
    parser.add_argument("--chunk-size", type=int, default=1000, help="Size of text chunks")
    parser.add_argument("--chunk-overlap", type=int, default=200, help="Overlap between chunks")
    
    args = parser.parse_args()
    
    asyncio.run(index_text_file(
        file_path=args.file_path,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )) 