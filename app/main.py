from fastapi import FastAPI
from app.routers import search

app = FastAPI(title="GraphFleet API")

app.include_router(search.router, prefix="/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Welcome to GraphFleet API"}