from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
import time
import logging

logger = logging.getLogger(__name__)

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Request to {request.url.path} took {process_time:.2f} seconds")
        return response