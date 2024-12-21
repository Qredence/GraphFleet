# Test Data Directory

This directory contains sample data files for testing the GraphFleet FastAPI application with Azure OpenAI integration.

## Required Files
- `nodes.parquet`: Sample nodes in the knowledge graph
- `entities.parquet`: Sample entities extracted from the documents
- `communities.parquet`: Sample community structure
- `community_reports.parquet`: Sample community reports
- `text_units.parquet`: Sample text units
- `relationships.parquet`: Sample relationships between entities

## File Structure
The test data should mirror the structure expected by the application:
```
test_data/
├── input/
│   └── (input documents)
├── output/
│   ├── nodes.parquet
│   ├── entities.parquet
│   ├── communities.parquet
│   ├── community_reports.parquet
│   ├── text_units.parquet
│   └── relationships.parquet
└── prompts/
    └── (prompt templates)
```

## Note
These files contain minimal test data and should not be used for production. Make sure to use appropriate test data that covers your use cases.
