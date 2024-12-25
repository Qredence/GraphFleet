# GraphFleet Examples

This directory contains example code demonstrating various features and use cases of GraphFleet.

## Directory Structure

```
examples/
├── basic/                  # Basic usage examples
│   ├── document_search.py  # Document indexing and search
│   └── knowledge_graph.py  # Knowledge graph creation and querying
├── advanced/              # Advanced usage examples
│   └── custom_pipeline.py # Custom processing pipelines
├── integrations/          # Integration examples
│   └── external_services.py # S3, Elasticsearch, ML models
└── performance/           # Performance optimization examples
    └── optimization.py    # Performance tuning techniques
```

## Basic Examples

### Document Search (`basic/document_search.py`)

Demonstrates basic document indexing and semantic search capabilities:
- Document indexing with metadata
- Simple semantic search
- Filtered search
- Hybrid search (semantic + keyword)

```bash
python examples/basic/document_search.py
```

### Knowledge Graph (`basic/knowledge_graph.py`)

Shows how to create and query knowledge graphs:
- Graph creation from documents
- Entity and relationship extraction
- Basic and advanced queries
- Graph analytics and visualization

```bash
python examples/basic/knowledge_graph.py
```

## Integration Examples

### External Services (`integrations/external_services.py`)

Demonstrates integration with external services:
- S3 storage backend
- Elasticsearch search engine
- HuggingFace models
- Custom processing pipelines

```bash
# First, start required services
docker-compose up -d elasticsearch redis localstack

# Then run the example
python examples/integrations/external_services.py
```

## Performance Examples

### Optimization (`performance/optimization.py`)

Shows various performance optimization techniques:
- Batch processing
- Parallel processing
- Query optimization
- Memory management
- Caching strategies
- Resource monitoring

```bash
python examples/performance/optimization.py
```

## Prerequisites

1. Install GraphFleet with all dependencies:
```bash
pip install graphfleet[all]
```

2. For integration examples, install additional dependencies:
```bash
pip install graphfleet[integrations]
```

3. For performance examples:
```bash
pip install graphfleet[performance]
```

## Configuration

Most examples use a default configuration suitable for local development. For production use, you should configure:

1. Environment variables:
```bash
export GRAPHFLEET_ENV=development
export GRAPHFLEET_DEBUG=true
```

2. Service endpoints (for integration examples):
```bash
export ELASTICSEARCH_URL=http://localhost:9200
export REDIS_URL=redis://localhost:6379
export AWS_ENDPOINT_URL=http://localhost:4566
```

## Best Practices

1. **Document Processing**
   - Use batch processing for large datasets
   - Include relevant metadata
   - Configure appropriate index settings

2. **Graph Operations**
   - Define clear node and edge types
   - Use appropriate relationship labels
   - Implement proper indexing strategies

3. **Performance**
   - Enable caching for frequent operations
   - Use batch processing when possible
   - Monitor resource usage

## Troubleshooting

### Common Issues

1. **Memory Issues**
```python
# Configure memory limits
gf.configure_memory(max_heap="4G")
```

2. **Performance Issues**
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

3. **Integration Issues**
```python
# Check service connectivity
from graphfleet.utils.health import check_services
check_services()
```

## Support

For help with the examples:
- Documentation: https://docs.graphfleet.ai
- Discord: https://discord.gg/graphfleet
- GitHub Issues: https://github.com/qredence/graphfleet/issues 