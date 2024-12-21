# GraphFleet Examples

This directory contains Jupyter notebooks demonstrating GraphFleet's features and capabilities.

## Prerequisites

Before running these notebooks, make sure you have:

1. Installed GraphFleet:
```bash
pip install graphfleet
```

2. Set up your environment variables in `.env`:
```env
GRAPHFLEET_PROJECT_DIR=./data
GRAPHFLEET_INDEX_TYPE=lancedb
GRAPHFLEET_MODEL=gpt-4
```

3. Clone GraphRAG example documents:
```bash
git clone https://github.com/microsoft/graphrag.git
cp -r graphrag/examples/docs/* ./data/raw/
```

## Notebooks

### 1. Quick Start (`01_quickstart.ipynb`)
- Basic project setup
- Adding documents from GraphRAG examples
- Simple queries
- Result handling

### 2. Advanced Features (`02_advanced_features.ipynb`)
- Custom pipelines
- Batch processing
- Result analysis
- Performance optimization

### 3. Indexing Guide (`03_indexing.ipynb`)
- Document preparation
- Text chunking
- Graph construction
- Vector indexing
- Index optimization

### 4. Auto-Prompting (`04_auto_prompting.ipynb`)
- Template management
- Auto-prompt generation
- Prompt tuning
- Custom templates

### 5. Advanced Querying (`05_advanced_querying.ipynb`)
- Query types
- Context window management
- Query optimization
- Advanced retrieval
- Query analysis

## Running the Notebooks

1. Start Jupyter:
```bash
jupyter lab
```

2. Open the notebooks in order (01 to 05)

3. Make sure to run the cells in sequence

## Additional Resources

- [API Documentation](../docs/api.md)
- [Advanced Features Guide](../docs/guides/advanced_features.md)
- [GraphRAG Documentation](https://microsoft.github.io/graphrag/)
