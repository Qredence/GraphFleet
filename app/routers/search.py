from fastapi import APIRouter, Depends
from app.services.graphfleet import GraphFleet, get_graphfleet
from app.models import Document
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Document])
async def search(query: str, limit: int = 10, offset: int = 0, gf: GraphFleet = Depends(get_graphfleet)):
    results = gf.search(query, limit=limit, offset=offset)
    return [Document(content=doc['content'], metadata=doc['metadata']) for doc in results]