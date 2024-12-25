# Getting Started with GraphFleet

This guide will help you get started with GraphFleet, from installation to your first knowledge graph.

## Prerequisites

- Python 3.10 or higher
- Node.js 18+ (for UI components)
- Docker (optional, but recommended)

## Installation

### Using pip

```bash
# Install the core package
pip install graphfleet

# Install with all optional dependencies
pip install graphfleet[all]

# Install development dependencies
pip install graphfleet[dev]
```

### Using Docker

```bash
# Pull the Docker image
docker pull qredence/graphfleet:latest

# Run the container
docker run -p 8000:8000 qredence/graphfleet:latest
```

## Quick Start

### 1. Initialize a Project

```python
from graphfleet import GraphFleet

# Create a new project
gf = GraphFleet()
project = gf.create_project(
    name="my-first-project",
    description="A sample project"
)
```

### 2. Add Documents

```python
# Add a single document
doc = project.add_document(
    content="GraphFleet is a powerful knowledge management system.",
    metadata={"title": "About GraphFleet", "type": "documentation"}
)

# Add multiple documents
docs = project.add_documents([
    {
        "content": "First document content",
        "metadata": {"title": "Doc 1"}
    },
    {
        "content": "Second document content",
        "metadata": {"title": "Doc 2"}
    }
])
```

### 3. Create Knowledge Graph

```python
# Create a graph from documents
graph = project.create_graph(
    name="knowledge-graph",
    config={
        "node_types": ["document", "entity"],
        "edge_types": ["contains", "relates_to"]
    }
)

# Build relationships
graph.build_relationships()
```

### 4. Query the Graph

```python
# Simple semantic search
results = project.search("knowledge management")

# Graph query
query = """
MATCH (d:Document)-[:CONTAINS]->(e:Entity)
WHERE e.type = 'concept'
RETURN d.title, e.name
"""
results = graph.query(query)
```

## Using the Web Interface

1. Start the server:
```bash
graphfleet serve
```

2. Open http://localhost:8000 in your browser

3. Use the UI to:
   - Create and manage projects
   - Upload and process documents
   - Visualize knowledge graphs
   - Run queries

## Common Use Cases

### 1. Document Analysis

```python
# Analyze document content
analysis = project.analyze_document(doc_id)
print(analysis.summary)
print(analysis.key_concepts)
print(analysis.sentiment)
```

### 2. Knowledge Extraction

```python
# Extract entities and relationships
entities = project.extract_entities(doc_id)
relationships = project.extract_relationships(doc_id)
```

### 3. Semantic Search

```python
# Search with filters
results = project.search(
    query="machine learning",
    filters={
        "type": "research_paper",
        "date": {"$gt": "2023-01-01"}
    }
)
```

### 4. Graph Analytics

```python
# Run graph analytics
metrics = graph.analyze()
print(metrics.centrality)
print(metrics.communities)
print(metrics.path_analysis)
```

## Configuration

### 1. Environment Variables

Create a `.env` file:
```bash
GRAPHFLEET_STORAGE=s3
GRAPHFLEET_INDEX=faiss
GRAPHFLEET_API_KEY=your_api_key
```

### 2. Custom Configuration

```python
config = {
    "storage": {
        "backend": "s3",
        "bucket": "my-bucket"
    },
    "index": {
        "type": "faiss",
        "dimension": 768
    },
    "processing": {
        "batch_size": 1000,
        "workers": 4
    }
}

gf = GraphFleet(config=config)
```

## Best Practices

1. **Document Processing**
   - Use batch processing for large datasets
   - Include relevant metadata
   - Maintain consistent document structure

2. **Graph Management**
   - Define clear node and edge types
   - Use meaningful relationship labels
   - Regularly update graph indices

3. **Query Optimization**
   - Use appropriate filters
   - Limit result sets
   - Cache frequent queries

## Next Steps

- Explore the [API Documentation](../api/README.md)
- Read the [Architecture Overview](../architecture/README.md)
- Join our [Discord Community](https://discord.gg/graphfleet)
- Check out [Example Projects](../../examples/)

## Troubleshooting

### Common Issues

1. **Installation Problems**
   ```bash
   # Update pip
   pip install --upgrade pip
   
   # Install system dependencies
   apt-get install python3-dev
   ```

2. **Performance Issues**
   ```python
   # Enable performance logging
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Memory Issues**
   ```python
   # Configure memory limits
   project.configure(memory_limit="8G")
   ```

### Getting Help

- Check our [FAQ](https://docs.graphfleet.ai/faq)
- Report issues on [GitHub](https://github.com/qredence/graphfleet/issues)
- Contact support at support@graphfleet.ai 