"""
GraphFleet Quickstart Guide

This script demonstrates how to get started with GraphFleet, a powerful document 
search and analysis tool built on top of GraphRAG.

Prerequisites:
1. Install GraphFleet: `pip install graphfleet`
2. Set up your environment variables in `.env`
3. Access to example documents
"""

import asyncio
from pathlib import Path
from graphfleet.core import GraphFleet
from graphfleet.indexing import TextProcessor, GraphBuilder

async def main():
    # Set up project directory
    project_dir = Path("./data")
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create example documents
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

    # Initialize GraphFleet
    gf = GraphFleet(project_dir)
    
    # Create and save example documents
    for filename, content in example_docs.items():
        doc_path = project_dir / "input" / filename
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(content)
        await gf.add_document(doc_path)
    
    # Search the knowledge base
    query = "What are the main challenges in AI development?"
    results = await gf.search(query)
    print("\nSearch Results:")
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
