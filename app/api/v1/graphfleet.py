from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from typing import List
from app.models import QueryParams, Document, IndexResponse, MonthyRequest
from app.services.graphfleet import GraphFleet, get_graphfleet
import logging
import json
from app.exceptions import CustomException

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/query", response_model=dict)
async def query(params: QueryParams, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        answer, confidence = gf.query(params.question, method=params.method)
        return {"answer": answer, "confidence": confidence}
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/index", response_model=IndexResponse)
async def index(file: UploadFile = File(...), gf: GraphFleet = Depends(get_graphfleet)):
    try:
        contents = await file.read()
        documents = json.loads(contents.decode('utf-8'))
        indexed_count = gf.index_documents(documents)
        return IndexResponse(message="Documents indexed successfully", indexed_count=indexed_count)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search", response_model=List[Document])
async def search(query: str, limit: int = 10, offset: int = 0, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        results = gf.search(query, limit=limit, offset=offset)
        return [Document(content=doc['content'], metadata=doc['metadata']) for doc in results]
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/monthy-scrape", response_model=dict)
async def monthy_scrape(request: MonthyRequest, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        result = gf.monthy_scrape(str(request.url), request.output_format)
        return {"content": result}
    except CustomException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ask-monty", response_model=dict)
async def ask_monty(request: str, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        result = gf.ask_monty(request)
        return {"response": result}
    except CustomException as e:
        logger.error(f"CustomException in ask_monty: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in ask_monty: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Add other endpoints as needed