"""
GraphFleet Main Application

This module initializes and configures the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import router as api_v1_router
from app.core.config import get_settings
from app.core.errors import setup_exception_handlers
from app.core.logging import setup_logging
from app.middleware.request_handler import (
    RequestHandlerMiddleware,
    RateLimitMiddleware
)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    settings = get_settings()
    
    # Initialize FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    
    # Set up logging
    setup_logging()
    
    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    # Add custom middleware
    app.add_middleware(RequestHandlerMiddleware)
    app.add_middleware(
        RateLimitMiddleware,
        rate_limit=100,
        window_size=60
    )
    
    # Set up exception handlers
    setup_exception_handlers(app)
    
    # Include routers
    app.include_router(
        api_v1_router,
        prefix=settings.API_V1_STR
    )
    
    return app

app = create_app()

@app.get("/")
async def root():
    """Root endpoint that returns API information.
    
    Returns:
        Dict with API information
    """
    settings = get_settings()
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "version": get_settings().VERSION
    }