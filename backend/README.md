# GraphFleet

A graph-based knowledge management and query system.

## Features

- Graph-based document representation
- Auto-tuning of prompts
- Intelligent chunking and indexing
- Hybrid search capabilities

## Installation

```bash
pip install graphfleet
```

## Usage

```python
from graphfleet import GraphFleet

# Initialize GraphFleet
graph_fleet = GraphFleet("project_dir")

# Create index
await graph_fleet.create_index()

# Query
result = await graph_fleet.query(
    query_text="What are the main features?",
    query_type="semantic"
)
```

## License

MIT 