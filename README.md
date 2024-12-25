# GraphFleet

A powerful graph-based knowledge management and query system.

## Features

- Project initialization and management
- Advanced document indexing
- Semantic search capabilities
- Custom query pipelines
- Knowledge graph analytics
- Concept drift analysis
- Batch processing support

## Project Structure

```
graphfleet/
├── backend/                 # Backend service
│   ├── app/                # Main application code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core business logic
│   │   ├── models/        # Data models
│   │   └── utils/         # Utility functions
│   ├── graphfleet/        # GraphFleet core library
│   ├── tests/             # Backend tests
│   └── templates/         # Template files
├── frontend/              # Frontend application
│   ├── src/              # Source code
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── utils/        # Utility functions
│   └── public/           # Static assets
├── shared/               # Shared utilities
├── scripts/              # Development scripts
└── examples/             # Example code and notebooks
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/graphfleet.git
cd graphfleet
```

2. Set up the backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Docker Development

```bash
docker-compose up
```

## API Documentation

The API documentation is available at `/docs` when running the backend server.

Key endpoints:
- `/v1/init` - Initialize a new project
- `/v1/index` - Create document index
- `/v1/query` - Process queries
- `/v1/semantic-search` - Perform semantic search
- `/v1/custom-pipeline` - Run custom query pipelines

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Security

For security concerns, please refer to our [Security Policy](SECURITY.md).
