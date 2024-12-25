# GraphFleet API Documentation

This document provides comprehensive documentation for GraphFleet's REST and GraphQL APIs.

## API Versions

- Current stable version: v1
- Beta version: v2 (under development)

## Authentication

All API endpoints require authentication using JWT tokens. To obtain a token:

```bash
curl -X POST https://api.graphfleet.ai/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Include the token in subsequent requests:

```bash
curl -X GET https://api.graphfleet.ai/v1/projects \
  -H "Authorization: Bearer your_token"
```

## REST API Endpoints

### Project Management

#### Create Project
```http
POST /v1/projects
```

Request body:
```json
{
  "name": "my-project",
  "description": "Project description",
  "config": {
    "storage_backend": "s3",
    "index_type": "faiss"
  }
}
```

#### List Projects
```http
GET /v1/projects
```

#### Get Project
```http
GET /v1/projects/{project_id}
```

### Document Management

#### Index Document
```http
POST /v1/projects/{project_id}/documents
```

Request body:
```json
{
  "content": "document content",
  "metadata": {
    "title": "Document Title",
    "author": "Author Name"
  }
}
```

#### Search Documents
```http
POST /v1/projects/{project_id}/search
```

Request body:
```json
{
  "query": "search query",
  "filters": {
    "author": "Author Name"
  },
  "limit": 10
}
```

### Graph Operations

#### Create Graph
```http
POST /v1/projects/{project_id}/graphs
```

Request body:
```json
{
  "name": "knowledge-graph",
  "config": {
    "node_types": ["document", "entity"],
    "edge_types": ["contains", "relates_to"]
  }
}
```

#### Query Graph
```http
POST /v1/projects/{project_id}/graphs/{graph_id}/query
```

Request body:
```json
{
  "query": "MATCH (d:Document)-[:CONTAINS]->(e:Entity) RETURN d, e",
  "parameters": {
    "limit": 100
  }
}
```

## GraphQL API

GraphFleet also provides a GraphQL API for more flexible querying.

### Endpoint
```http
POST /v1/graphql
```

### Example Queries

#### Get Project with Documents
```graphql
query {
  project(id: "project-id") {
    name
    description
    documents {
      id
      title
      content
      metadata
    }
  }
}
```

#### Search Documents with Graph Relations
```graphql
query {
  search(
    projectId: "project-id"
    query: "search query"
    limit: 10
  ) {
    documents {
      id
      title
      content
      relations {
        type
        target {
          ... on Document {
            id
            title
          }
          ... on Entity {
            id
            name
          }
        }
      }
    }
  }
}
```

## Rate Limiting

- Free tier: 1000 requests/hour
- Pro tier: 10000 requests/hour
- Enterprise tier: Custom limits

## Error Handling

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {
      "field": "Additional error details"
    }
  }
}
```

Common error codes:
- `AUTH_ERROR`: Authentication failed
- `INVALID_REQUEST`: Invalid request parameters
- `NOT_FOUND`: Resource not found
- `RATE_LIMITED`: Rate limit exceeded

## Webhooks

GraphFleet can send webhooks for various events:

```http
POST /v1/projects/{project_id}/webhooks
```

Request body:
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["document.indexed", "graph.updated"],
  "secret": "your_webhook_secret"
}
```

## SDKs

Official SDKs are available for:
- Python: [graphfleet-python](https://github.com/qredence/graphfleet-python)
- JavaScript: [graphfleet-js](https://github.com/qredence/graphfleet-js)
- Go: [graphfleet-go](https://github.com/qredence/graphfleet-go)

## API Versioning

- APIs are versioned using URL prefixes (e.g., /v1/, /v2/)
- Each version is supported for at least 12 months after deprecation notice
- Beta features are available under /v2/ with appropriate warnings

## Support

For API support:
- Email: api-support@graphfleet.ai
- Discord: [GraphFleet Community](https://discord.gg/graphfleet)
- Documentation: [docs.graphfleet.ai](https://docs.graphfleet.ai) 