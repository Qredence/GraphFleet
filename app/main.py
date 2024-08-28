from fastapi import FastAPI
from app.routers import search

app = FastAPI(title="GraphRAG API")

app.include_router(search.router, prefix="/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "Welcome to GraphRAG API"}