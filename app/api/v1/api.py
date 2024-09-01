from fastapi import APIRouter
from app.api.v1 import endpoints, graphfleet

api_router = APIRouter()

api_router.include_router(endpoints.router, prefix="/endpoints", tags=["endpoints"])
api_router.include_router(graphfleet.router, prefix="/graphfleet", tags=["graphfleet"])
# Add other v1 routers here