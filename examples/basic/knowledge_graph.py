"""
Basic example demonstrating knowledge graph creation and querying with GraphFleet.
"""

from graphfleet import GraphFleet

# Initialize GraphFleet
gf = GraphFleet()

# Create a new project
project = gf.create_project(
    name="knowledge-graph-demo",
    description="Demo project for knowledge graphs"
)

def create_graph():
    """Create a knowledge graph from documents."""
    # Sample documents about machine learning
    documents = [
        {
            "content": """
            Neural networks are a fundamental concept in deep learning.
            They consist of layers of neurons that process information.
            Convolutional Neural Networks (CNNs) are particularly effective
            for image processing tasks.
            """,
            "metadata": {
                "title": "Neural Networks",
                "author": "John Smith"
            }
        },
        {
            "content": """
            Deep learning is a subset of machine learning that uses neural networks
            with multiple layers. It has revolutionized fields like computer vision
            and natural language processing.
            """,
            "metadata": {
                "title": "Deep Learning Overview",
                "author": "Jane Doe"
            }
        }
    ]

    # Add documents
    docs = project.add_documents(documents)

    # Create graph
    graph = project.create_graph(
        name="ml-knowledge-graph",
        config={
            "node_types": ["Document", "Concept", "Author"],
            "edge_types": ["CONTAINS", "RELATES_TO", "AUTHORED_BY"]
        }
    )

    # Extract entities and relationships
    graph.extract_knowledge(docs)
    print("Created knowledge graph")
    return graph

def basic_queries(graph):
    """Demonstrate basic graph queries."""
    # Find all concepts related to neural networks
    results = graph.query("""
        MATCH (c:Concept)-[:RELATES_TO]->(n:Concept)
        WHERE n.name CONTAINS 'neural network'
        RETURN c.name, n.name
    """)
    print("\nConcepts related to neural networks:")
    for result in results:
        print(f"- {result['c.name']} -> {result['n.name']}")

    # Find documents by author
    author_docs = graph.query("""
        MATCH (d:Document)-[:AUTHORED_BY]->(a:Author)
        WHERE a.name = 'John Smith'
        RETURN d.title
    """)
    print("\nDocuments by John Smith:")
    for doc in author_docs:
        print(f"- {doc['d.title']}")

def advanced_queries(graph):
    """Demonstrate advanced graph queries."""
    # Find concept relationships with path analysis
    paths = graph.query("""
        MATCH path = (c1:Concept)-[:RELATES_TO*1..3]->(c2:Concept)
        WHERE c1.name CONTAINS 'deep learning'
        RETURN path
    """)
    print("\nConcept paths from 'deep learning':")
    for path in paths:
        print(f"- Path: {path}")

    # Find common concepts between documents
    common_concepts = graph.query("""
        MATCH (d1:Document)-[:CONTAINS]->(c:Concept)<-[:CONTAINS]-(d2:Document)
        WHERE d1.title <> d2.title
        RETURN d1.title, d2.title, collect(c.name) as common_concepts
    """)
    print("\nCommon concepts between documents:")
    for result in common_concepts:
        print(f"- {result['d1.title']} & {result['d2.title']}: {result['common_concepts']}")

def analyze_graph(graph):
    """Perform graph analytics."""
    # Calculate centrality
    centrality = graph.analyze_centrality(
        node_type="Concept",
        algorithm="pagerank"
    )
    print("\nTop concepts by centrality:")
    for concept, score in centrality[:5]:
        print(f"- {concept}: {score:.2f}")

    # Find communities
    communities = graph.detect_communities(
        node_type="Concept",
        algorithm="louvain"
    )
    print("\nConcept communities:")
    for i, community in enumerate(communities[:3]):
        print(f"Community {i + 1}: {', '.join(community)}")

def visualize_graph(graph):
    """Visualize the knowledge graph."""
    graph.visualize(
        output_file="knowledge_graph.html",
        config={
            "layout": "force",
            "node_size": "degree",
            "edge_width": "weight"
        }
    )
    print("\nGraph visualization saved to 'knowledge_graph.html'")

def main():
    """Run the example."""
    print("1. Creating knowledge graph...")
    graph = create_graph()

    print("\n2. Running basic queries...")
    basic_queries(graph)

    print("\n3. Running advanced queries...")
    advanced_queries(graph)

    print("\n4. Analyzing graph...")
    analyze_graph(graph)

    print("\n5. Visualizing graph...")
    visualize_graph(graph)

if __name__ == "__main__":
    main() 