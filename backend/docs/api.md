# GraphFleet API Documentation

## Overview

GraphFleet provides a FastAPI-based REST API for managing and querying graph-based RAG applications. This document describes all available endpoints and their usage.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

No authentication required. The API is open for use.

## Endpoints

### Document Management

#### Add Documents
```http
POST /documents/add
```

Add documents to the project.

**Request Body:**
```json
{
  "project_path": "string",
  "documents": [
    {
      "content": "string",
      "metadata": {
        "key": "value"
      }
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "document_ids": ["string"],
  "message": "string"
}
```

### Indexing

#### Create Index
```http
POST /index/create
```

Create or update the index.

**Request Body:**
```json
{
  "project_path": "string",
  "index_type": "lancedb",
  "dimension": 1536,
  "metric": "cosine",
  "config": {
    "key": "value"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "string"
}
```

### Querying

#### Standard Query
```http
POST /query
```

Process a standard query.

**Request Body:**
```json
{
  "project_path": "string",
  "query_text": "string",
  "query_type": "standard",
  "config": {
    "max_results": 10,
    "threshold": 0.7,
    "context_window": 3
  }
}
```

**Response:**
```json
{
  "result": "string",
  "confidence": 0.95,
  "sources": [
    {
      "id": "string",
      "content": "string",
      "metadata": {}
    }
  ]
}
```

#### Batch Query
```http
POST /query/batch
```

Process multiple queries.

**Request Body:**
```json
{
  "project_path": "string",
  "queries": ["string"],
  "batch_size": 5,
  "config": {
    "max_results": 10,
    "threshold": 0.7
  }
}
```

**Response:**
```json
{
  "results": [
    {
      "query": "string",
      "result": "string",
      "confidence": 0.95,
      "sources": []
    }
  ]
}
```

### Advanced Features

#### Custom Pipeline
```http
POST /query/custom
```

Run a custom query pipeline.

**Request Body:**
```json
{
  "project_path": "string",
  "query_text": "string",
  "pipeline_type": "hybrid",
  "config": {
    "local_weight": 0.7,
    "global_weight": 0.3
  }
}
```

**Response:**
```json
{
  "result": "string",
  "confidence": 0.95,
  "sources": [],
  "pipeline_info": {
    "steps": [],
    "metrics": {}
  }
}
```

#### Query Analysis
```http
POST /query/analyze
```

Analyze query results.

**Request Body:**
```json
{
  "project_path": "string",
  "query_text": "string",
  "metrics": ["relevance", "coherence"]
}
```

**Response:**
```json
{
  "scores": {
    "relevance": 0.9,
    "coherence": 0.85
  },
  "suggestions": ["string"]
}
```

### Templates

#### List Templates
```http
GET /templates
```

List available templates.

**Response:**
```json
{
  "templates": [
    {
      "name": "string",
      "description": "string",
      "version": "string"
    }
  ]
}
```

#### Add Template
```http
POST /templates/add
```

Add a new template.

**Request Body:**
```json
{
  "name": "string",
  "template": "string",
  "metadata": {
    "description": "string",
    "version": "string"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "string"
}
```

## Error Handling

All endpoints return standard error responses:

```json
{
  "error": true,
  "message": "string",
  "details": {}
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

- Default: 100 requests per minute
- Batch endpoints: 20 requests per minute

## Examples

### Python

```python
import requests

# Standard query
response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "project_path": "./data",
        "query_text": "What is AI?",
        "query_type": "standard"
    }
)

# Custom pipeline
response = requests.post(
    "http://localhost:8000/api/v1/query/custom",
    json={
        "project_path": "./data",
        "query_text": "How do neural networks work?",
        "pipeline_type": "hybrid",
        "config": {
            "local_weight": 0.7,
            "global_weight": 0.3
        }
    }
)
```

### cURL

```bash
# Standard query
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "./data",
    "query_text": "What is AI?",
    "query_type": "standard"
  }'

# List templates
curl "http://localhost:8000/api/v1/templates"
