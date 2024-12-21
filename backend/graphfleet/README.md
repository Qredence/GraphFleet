# GraphFleet API

A FastAPI-based REST API for the GraphFleet application, providing access to GraphRAG's search capabilities.

## Features

- Multiple Search Methods:
  - Global Search: Search over all AI-generated community reports
  - Local Search: Search specific entities and their relationships
  - Dynamic Global Search: Automatically selects relevant community levels
- Index Building and Management
- Settings Configuration
- CORS enabled
- Logging system

## API Endpoints

### Core Endpoints
- `GET /`: Welcome endpoint
- `GET /settings`: Retrieve application settings
- `POST /index/build`: Build a new index

### Search Endpoints
- `POST /search`: Unified search endpoint supporting multiple search types:
  - Global Search: Searches over all AI-generated community reports
  - Local Search: Combines knowledge graph data with text chunks
  - Dynamic Global Search: Automatically selects community levels

#### Search Request Format
```json
{
  "query": "Your search query",
  "search_type": "global | local | global_dynamic",
  "community_level": 2,  // Optional, default: 2
  "dynamic_community_selection": false,  // Optional, default: false
  "response_type": "Multiple Paragraphs"  // Optional, default: "Multiple Paragraphs"
}
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
GRAPHRAG_API_KEY=your_api_key
GRAPHRAG_LLM_MODEL=gpt-4  # or your preferred model
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

Create a `.env` file in the root directory with the following configurations:
```env
GRAPHRAG_API_KEY=your_api_key
GRAPHRAG_LLM_MODEL=gpt-4
