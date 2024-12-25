"""
Basic example demonstrating document indexing and semantic search with GraphFleet.
"""

import os
from pathlib import Path
from graphfleet import GraphFleet

# Initialize GraphFleet
gf = GraphFleet()

# Create a new project
project = gf.create_project(
    name="document-search-demo",
    description="Demo project for document search"
)

def index_documents():
    """Index sample documents."""
    # Sample documents
    documents = [
        {
            "content": """
            GraphFleet is a powerful graph-based knowledge management system.
            It provides semantic search and knowledge graph capabilities.
            """,
            "metadata": {
                "title": "About GraphFleet",
                "type": "documentation"
            }
        },
        {
            "content": """
            Machine learning models can be used for various tasks including
            classification, regression, and clustering.
            """,
            "metadata": {
                "title": "ML Overview",
                "type": "article"
            }
        },
        {
            "content": """
            Python is a versatile programming language widely used in
            data science and machine learning.
            """,
            "metadata": {
                "title": "Python Programming",
                "type": "tutorial"
            }
        }
    ]

    # Add documents to the project
    results = project.add_documents(documents)
    print(f"Indexed {len(results)} documents")
    return results

def semantic_search():
    """Perform semantic search."""
    # Simple search
    results = project.search(
        query="knowledge management systems",
        limit=2
    )
    print("\nSimple Search Results:")
    for doc in results:
        print(f"- {doc.metadata['title']}: {doc.score:.2f}")

    # Search with filters
    filtered_results = project.search(
        query="machine learning",
        filters={
            "type": "article"
        },
        limit=2
    )
    print("\nFiltered Search Results:")
    for doc in filtered_results:
        print(f"- {doc.metadata['title']}: {doc.score:.2f}")

def advanced_search():
    """Demonstrate advanced search features."""
    # Semantic search with relevance boost
    results = project.search(
        query="programming languages",
        boost_fields={
            "title": 1.5,
            "type": 1.2
        },
        limit=2
    )
    print("\nBoosted Search Results:")
    for doc in results:
        print(f"- {doc.metadata['title']}: {doc.score:.2f}")

    # Hybrid search (combining semantic and keyword search)
    hybrid_results = project.search(
        query="python data science",
        search_type="hybrid",
        weights={
            "semantic": 0.7,
            "keyword": 0.3
        },
        limit=2
    )
    print("\nHybrid Search Results:")
    for doc in hybrid_results:
        print(f"- {doc.metadata['title']}: {doc.score:.2f}")

def main():
    """Run the example."""
    print("1. Indexing documents...")
    index_documents()

    print("\n2. Basic semantic search...")
    semantic_search()

    print("\n3. Advanced search features...")
    advanced_search()

if __name__ == "__main__":
    main() 