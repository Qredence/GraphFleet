# GraphFleet Project Structure

```
graphfleet/
├── backend/                    # FastAPI backend
│   ├── app/                   # FastAPI application
│   │   ├── api/              # API endpoints
│   │   │   └── v1/          # API v1 routes
│   │   ├── core/            # Core application code
│   │   ├── db/              # Database models
│   │   ├── middleware/      # API middleware
│   │   ├── models/          # Pydantic models
│   │   ├── schemas/         # API schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utilities
│   │
│   ├── graphfleet/          # Core package
│   │   ├── core/           # Core functionality
│   │   ├── indexing/       # Indexing functionality
│   │   ├── prompting/      # Prompt management
│   │   ├── querying/       # Query processing
│   │   └── storage/        # Storage backends
│   │
│   ├── docs/               # Backend documentation
│   ├── examples/           # Example notebooks
│   ├── templates/          # GraphRAG templates
│   └── tests/             # Backend tests
│
├── frontend/                  # Next.js frontend
│   ├── app/                  # Next.js 13+ app directory
│   │   ├── (auth)/         # Authentication routes
│   │   │   ├── login/     # Login page
│   │   │   └── signup/    # Signup page
│   │   │
│   │   ├── dashboard/     # Dashboard routes
│   │   │   ├── documents/ # Document management
│   │   │   ├── queries/   # Query interface
│   │   │   └── settings/  # User settings
│   │   │
│   │   ├── api/          # Frontend API routes
│   │   └── layout.tsx    # Root layout
│   │
│   ├── components/         # React components
│   │   ├── ui/           # UI components
│   │   ├── forms/        # Form components
│   │   └── shared/       # Shared components
│   │
│   ├── lib/               # Frontend utilities
│   │   ├── api/         # API client
│   │   ├── hooks/       # Custom hooks
│   │   └── utils/       # Helper functions
│   │
│   ├── styles/            # Global styles
│   └── types/             # TypeScript types
│
├── shared/                    # Shared code
│   ├── types/               # Shared TypeScript types
│   ├── constants/           # Shared constants
│   └── utils/              # Shared utilities
│
├── .env.example              # Example environment variables
├── docker-compose.yml        # Docker composition
├── package.json              # Root package.json
└── README.md                # Project documentation
```

## Setup Instructions

### Backend (FastAPI)

1. Create Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run backend:
```bash
uvicorn app.main:app --reload
```

### Frontend (Next.js)

1. Create Next.js project:
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --eslint
```

2. Install dependencies:
```bash
npm install @tanstack/react-query axios @headlessui/react @heroicons/react
```

3. Run frontend:
```bash
npm run dev
```

## Key Features

### Backend
- FastAPI for high-performance API
- GraphRAG integration for document processing
- Async support for better scalability
- Comprehensive API documentation

### Frontend
- Modern Next.js 13+ with App Router
- Type-safe API client
- Real-time updates with React Query
- Responsive UI with Tailwind CSS
- Dark mode support
- Authentication flow

### Shared
- Type definitions shared between frontend and backend
- Common utilities and constants
- Consistent error handling

## Development Workflow

1. Backend Development:
   - Use FastAPI's auto-reload
   - Run tests with pytest
   - Update API documentation

2. Frontend Development:
   - Use Next.js development server
   - Component development with Storybook
   - E2E testing with Cypress

3. Full Stack Development:
   - Run both servers
   - Use Docker for consistent environments
   - Share types between frontend and backend

## Deployment

1. Backend:
   - Deploy as Docker container
   - Use gunicorn for production
   - Configure CORS properly

2. Frontend:
   - Build static site with Next.js
   - Deploy to Vercel or similar
   - Configure environment variables

3. Infrastructure:
   - Use Docker Compose for local development
   - Deploy with Kubernetes for production
   - Set up CI/CD pipeline
