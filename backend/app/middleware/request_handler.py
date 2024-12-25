"""
GraphFleet Request Handling Middleware

This module provides middleware for handling requests in the GraphFleet application.
It includes request ID generation, logging, timing, and error handling.
"""

import time
import uuid
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.logging import get_request_logger
from app.core.errors import GraphFleetException

class RequestHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling incoming requests."""
    
    def __init__(self, app: ASGIApp):
        """Initialize the middleware.
        
        Args:
            app: ASGI application
        """
        super().__init__(app)
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process the request.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in chain
            
        Returns:
            Response object
        """
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Set up request logger
        logger = get_request_logger(
            __name__,
            request_id,
            method=request.method,
            url=str(request.url)
        )
        
        # Start timing
        start_time = time.time()
        
        try:
            # Log request
            logger.info(
                f"Incoming request: {request.method} {request.url.path}",
                extra={
                    "client_host": request.client.host if request.client else None,
                    "query_params": dict(request.query_params),
                    "headers": dict(request.headers)
                }
            )
            
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                f"Request completed: {response.status_code}",
                extra={
                    "status_code": response.status_code,
                    "duration": duration
                }
            )
            
            # Add timing header
            response.headers["X-Process-Time"] = str(duration)
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except GraphFleetException as e:
            # Log GraphFleet errors
            logger.error(
                f"GraphFleet error: {e.message}",
                extra={
                    "error_type": e.__class__.__name__,
                    "status_code": e.status_code,
                    "details": e.details
                },
                exc_info=True
            )
            raise
            
        except Exception as e:
            # Log unexpected errors
            logger.error(
                f"Unexpected error: {str(e)}",
                extra={
                    "error_type": e.__class__.__name__
                },
                exc_info=True
            )
            raise
            
        finally:
            # Always log request completion
            duration = time.time() - start_time
            logger.info(
                "Request processing completed",
                extra={"duration": duration}
            )

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests."""
    
    def __init__(
        self,
        app: ASGIApp,
        rate_limit: int = 100,
        window_size: int = 60
    ):
        """Initialize the middleware.
        
        Args:
            app: ASGI application
            rate_limit: Maximum requests per window
            window_size: Window size in seconds
        """
        super().__init__(app)
        self.rate_limit = rate_limit
        self.window_size = window_size
        self.requests = {}
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Process the request with rate limiting.
        
        Args:
            request: FastAPI request
            call_next: Next middleware in chain
            
        Returns:
            Response object
            
        Raises:
            HTTPException: If rate limit is exceeded
        """
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Clean up old requests
        current_time = time.time()
        self.requests = {
            ip: timestamps
            for ip, timestamps in self.requests.items()
            if timestamps[-1] > current_time - self.window_size
        }
        
        # Check rate limit
        if client_ip in self.requests:
            timestamps = self.requests[client_ip]
            if len(timestamps) >= self.rate_limit:
                oldest = timestamps[0]
                if current_time - oldest < self.window_size:
                    return Response(
                        content="Rate limit exceeded",
                        status_code=429,
                        headers={
                            "Retry-After": str(self.window_size),
                            "X-RateLimit-Limit": str(self.rate_limit),
                            "X-RateLimit-Reset": str(int(oldest + self.window_size))
                        }
                    )
                timestamps.pop(0)
            timestamps.append(current_time)
        else:
            self.requests[client_ip] = [current_time]
        
        return await call_next(request) 