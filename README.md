# GraphFleet

GraphFleet is a powerful Python package for building graph-based RAG (Retrieval-Augmented Generation) applications. Built on top of GraphRAG with enhanced features and improved usability.

## Features

- **Advanced Document Processing**: Intelligent text chunking and document handling
- **Graph-Based Knowledge**: Leverage graph structures for better context understanding
- **Smart Prompting**: Template management and auto-prompt generation
- **Optimized Querying**: Query optimization and result evaluation
- **FastAPI Integration**: Ready-to-use API endpoints
- **Comprehensive Examples**: Jupyter notebooks demonstrating all features

## Installation

```bash
pip install graphfleet
```

## Quick Start

```python
from graphfleet import GraphFleet

# Initialize project
graph_fleet = GraphFleet.init_project("./my_project")

# Add documents
await graph_fleet.add_documents("./docs")

# Create index
await graph_fleet.create_index()

# Query
result = await graph_fleet.query("What is machine learning?")
print(result.result)
```

## Documentation

### Core Components

1. **Document Processing**
   - Text chunking with overlap
   - Metadata handling
   - Multiple file formats support

2. **Indexing**
   - Vector indexing with LanceDB
   - Graph construction
   - Custom index configurations

3. **Prompting**
   - Template management
   - Auto-prompt generation
   - Template customization

4. **Querying**
   - Multiple query types
   - Context window management
   - Query optimization
   - Result evaluation

### Example Notebooks

1. `01_quickstart.ipynb`: Basic usage and setup
2. `02_advanced_features.ipynb`: Advanced features demo
3. `03_indexing.ipynb`: Document indexing guide
4. `04_auto_prompting.ipynb`: Prompt management
5. `05_advanced_querying.ipynb`: Advanced query features

## API Reference

See [API Documentation](docs/api.md) for detailed endpoint descriptions.

## Configuration

### Environment Variables

Create a `.env` file:

```env
GRAPHFLEET_PROJECT_DIR=./data
GRAPHFLEET_INDEX_TYPE=lancedb
GRAPHFLEET_MODEL=gpt-4
GRAPHFLEET_CHUNK_SIZE=512
GRAPHFLEET_CHUNK_OVERLAP=50
```

### Project Structure

```
graphfleet/
├── app/                    # FastAPI application
├── data/                   # Data directories
├── docs/                   # Documentation
├── examples/               # Jupyter notebooks
├── graphfleet/            # Core package
├── templates/             # GraphRAG templates
└── tests/                 # Test suite
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
