import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import search
from app.core.config import settings
from app.middleware import CustomMiddleware
from app.exceptions import add_exception_handlers
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GraphFleet API",
    version=settings.API_VERSION,
    description="GraphFleet API for knowledge graph operations"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(CustomMiddleware)

# Add OpenTelemetry instrumentation
FastAPIInstrumentor.instrument_app(app)

# Include routers
app.include_router(search.router, prefix="/search", tags=["search"])

# Add exception handlers
add_exception_handlers(app)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again later."},
    )

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to GraphFleet API",
        "version": settings.API_VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
