import asyncio
from pathlib import Path
from graphfleet.core import GraphFleet
from graphfleet.indexing import TextProcessor, GraphBuilder

async def main():
    # Set up project directory
    project_dir = Path("./data")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    gf = GraphFleet(project_dir)
    processor = TextProcessor(
        project_dir=project_dir,
        chunk_size=512,  # Maximum chunk size in tokens
        overlap=50,      # Overlap between chunks
        split_method="txt"  # Use text-based splitting
    )
    builder = GraphBuilder(project_dir)
    
    # Create example documents
    raw_dir = project_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    example_docs = {
        "ai_challenges.txt": """
        Challenges in AI Development:
        1. Data Quality and Bias
        2. Model Interpretability
        3. Ethical Considerations
        4. Resource Requirements
        5. Safety and Security
        """,
        "machine_learning.txt": """
        Machine Learning Fundamentals:
        1. Supervised Learning
        2. Unsupervised Learning
        3. Reinforcement Learning
        4. Neural Networks
        5. Deep Learning
        """
    }
    
    # Save example documents
    for filename, content in example_docs.items():
        doc_path = raw_dir / filename
        doc_path.write_text(content)
    
    # Process documents into chunks
    chunks = processor.process_directory(raw_dir)
    print(f"Created {len(chunks)} chunks from documents")
    
    # Build knowledge graph
    config = {
        "api_key": gf.api_key,
        "api_base": gf.api_base,
        "api_version": gf.api_version,
        "deployment_name": gf.deployment_name,
        "embedding_key": gf.embedding_key,
        "embedding_endpoint": gf.embedding_endpoint,
        "embedding_deployment_name": gf.embedding_deployment_name
    }
    
    await builder.build_graph(chunks, config)
    print("Built knowledge graph from chunks")
    
    # Test search functionality
    query = "What are the main challenges in AI development?"
    results = await gf.search(query)
    print("\nSearch Results:")
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
