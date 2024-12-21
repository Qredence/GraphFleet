from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger()

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            # Log the error
            logger.error(
                "unhandled_error",
                error=str(e),
                error_type=type(e).__name__,
                path=request.url.path
            )
            
            # Return a JSON response with error details
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": {
                        "message": "An unexpected error occurred",
                        "type": type(e).__name__,
                        "code": "INTERNAL_SERVER_ERROR"
                    }
                }
            )
