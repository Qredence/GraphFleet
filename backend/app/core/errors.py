"""
GraphFleet Error Handling Module

This module defines custom exceptions and error handlers for the GraphFleet application.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class GraphFleetException(Exception):
    """Base exception for GraphFleet errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class ProjectNotFoundError(GraphFleetException):
    """Raised when a project is not found."""
    
    def __init__(self, project_path: str):
        super().__init__(
            message=f"Project not found at path: {project_path}",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"project_path": project_path}
        )

class IndexNotFoundError(GraphFleetException):
    """Raised when an index is not found."""
    
    def __init__(self, project_path: str):
        super().__init__(
            message=f"Index not found for project at: {project_path}",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"project_path": project_path}
        )

class InvalidQueryTypeError(GraphFleetException):
    """Raised when an invalid query type is specified."""
    
    def __init__(self, query_type: str):
        super().__init__(
            message=f"Invalid query type: {query_type}",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"query_type": query_type}
        )

class ConfigurationError(GraphFleetException):
    """Raised when there's a configuration error."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )

async def graphfleet_exception_handler(
    request: Request,
    exc: GraphFleetException
) -> JSONResponse:
    """Handle GraphFleet exceptions.
    
    Args:
        request: FastAPI request object
        exc: GraphFleet exception
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
            "path": request.url.path
        }
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors.
    
    Args:
        request: FastAPI request object
        exc: Validation exception
        
    Returns:
        JSON response with validation error details
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "details": {
                "errors": exc.errors(),
                "body": exc.body
            },
            "path": request.url.path
        }
    )

async def http_exception_handler(
    request: Request,
    exc: HTTPException
) -> JSONResponse:
    """Handle HTTP exceptions.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": str(exc.detail),
            "path": request.url.path
        }
    )

def setup_exception_handlers(app: Any) -> None:
    """Set up exception handlers for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(GraphFleetException, graphfleet_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler) 