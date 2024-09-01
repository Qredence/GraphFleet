from pydantic import HttpUrl
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, BackgroundTasks, APIRouter, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .graphfleet import GraphFleet
from .config import settings, StorageBackend
import json
import logging
import subprocess
import os
from .models import ReleaseNotesRequest
from .utils.exceptions import GraphFleetException, graphfleet_exception_handler
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import aioredis

app = FastAPI(title="GraphFleet API", version="0.5.35")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency to get GraphFleet instance


def get_graphfleet():
    return GraphFleet()


class QueryParams(BaseModel):
    question: str
    method: str = "global"


class Query(BaseModel):
    question: str


class Document(BaseModel):
    content: str
    metadata: dict


class IndexResponse(BaseModel):
    message: str
    indexed_count: int


class PromptTuneResponse(BaseModel):
    message: str
    status: str


def run_prompt_tune(config_path: str, root_path: str, output_path: str):
    command = [
        "python", "-m", "graphrag.prompt_tune",
        "--config", config_path,
        "--root", root_path,
        "--no-entity-types",
        "--output", output_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Error in prompt tuning: {result.stderr}")
        raise Exception("Prompt tuning failed")
    logger.info("Prompt tuning completed successfully")


@app.post("/query", response_model=dict)
async def query(params: QueryParams, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        logger.info(f"Received query: {params.question} (method: {params.method})")
        answer, confidence = gf.query(params.question, method=params.method)
        return {"answer": answer, "confidence": confidence}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/info")
async def info(gf: GraphFleet = Depends(get_graphfleet)):
    return {
        "api_base": settings.api_base,
        "api_version": settings.api_version,
        "deployment_name": settings.deployment_name,
    }


@app.post("/index", response_model=IndexResponse)
async def index(file: UploadFile = File(...), gf: GraphFleet = Depends(get_graphfleet)):
    try:
        contents = await file.read()
        documents = json.loads(contents.decode('utf-8'))
        if not isinstance(documents, list):
            raise ValueError("Uploaded file must contain a JSON array of documents")

        gf.index_documents(documents)
        logger.info(f"Indexed {len(documents)} documents")
        return IndexResponse(message="Documents indexed successfully", indexed_count=len(documents))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error indexing documents: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error indexing documents: {str(e)}")


@app.get("/visualize")
async def visualize(gf: GraphFleet = Depends(get_graphfleet)):
    try:
        gf.visualize_graph()
        return {"message": "Knowledge graph visualization saved as 'knowledge_graph.png'."}
    except Exception as e:
        logger.error(f"Error visualizing graph: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error visualizing graph: {str(e)}")


@app.get("/search", response_model=List[Document])
async def search(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    gf: GraphFleet = Depends(get_graphfleet)
):
    try:
        results = await gf.search(query, limit=limit, offset=offset)
        return [Document(content=doc['content'], metadata=doc['metadata']) for doc in results]
    except Exception as e:
        logger.error(f"Error performing search: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error performing search: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/auto-prompt-tune", response_model=PromptTuneResponse)
async def auto_prompt_tune(background_tasks: BackgroundTasks):
    try:
        config_path = os.path.join(settings.root_path, "settings.yaml")
        output_path = os.path.join(settings.root_path, "prompts")

        # Run the prompt tuning in the background
        background_tasks.add_task(run_prompt_tune, config_path,
                                  settings.root_path, output_path)

        return PromptTuneResponse(
            message="Auto prompt tuning started in the background",
            status="running"
        )
    except Exception as e:
        logger.error(f"Error starting auto prompt tune: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error starting auto prompt tune: {str(e)}")


@app.post("/index-file", response_model=IndexResponse)
async def index_file(file: UploadFile = File(...), gf: GraphFleet = Depends(get_graphfleet)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process and index the file
        gf.index_file(temp_file_path)

        # Remove the temporary file
        os.remove(temp_file_path)

        return IndexResponse(message="File indexed successfully", indexed_count=1)
    except Exception as e:
        logger.error(f"Error indexing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error indexing file: {str(e)}")


@app.post("/advanced-reasoning")
async def advanced_reasoning(question: str, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        answer = gf.advanced_reasoning(question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in advanced reasoning: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error in advanced reasoning: {str(e)}")


@app.post("/generate-release-notes")
async def generate_release_notes(request: ReleaseNotesRequest, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        notes = gf.generate_release_notes(request.version, request.changes)
        return {"release_notes": notes}
    except Exception as e:
        logger.error(f"Error generating release notes: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error generating release notes: {str(e)}")


@app.post("/web-enhanced-query")
async def web_enhanced_query(question: str, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        answer = gf.web_enhanced_query(question)
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error in web-enhanced query: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error in web-enhanced query: {str(e)}")


@app.post("/containerized-processing")
async def containerized_processing(data: dict, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        result = gf.containerized_processing(data)
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in containerized processing: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error in containerized processing: {str(e)}")


@app.post("/index-large-file")
async def index_large_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    background_tasks.add_task(process_and_index_file, temp_file_path)
    return {"message": "File indexing started in the background"}


def process_and_index_file(file_path: str):
    gf = GraphFleet()
    try:
        gf.index_file(file_path)
    finally:
        os.remove(file_path)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)


@app.get("/rate-limited-endpoint", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def rate_limited_endpoint():
    return {"message": "This endpoint is rate limited"}

v1_router = APIRouter(prefix="/v1")


@v1_router.post("/query")
async def query_v1(params: QueryParams, gf: GraphFleet = Depends(get_graphfleet)):
    # Implement v1 query logic
    try:
        answer, confidence = gf.query(params.question, method=params.method)
        return {"answer": answer, "confidence": confidence}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Add more v1 endpoints here...

app.include_router(v1_router)

app.add_exception_handler(GraphFleetException, graphfleet_exception_handler)


@app.post("/set-storage-backend")
async def set_storage_backend(backend: StorageBackend):
    settings.storage_backend = backend
    # Reinitialize GraphFleet with the new storage backend
    global gf
    gf = GraphFleet()
    return {"message": f"Storage backend set to {backend}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Add this import at the top of the file

# Add this new model


class MonthyRequest(BaseModel):
    url: HttpUrl
    output_format: str = "text"

# Add this new endpoint


@app.post("/monthy-scrape")
async def monthy_scrape(request: MonthyRequest, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        result = gf.monthy_scrape(str(request.url), request.output_format)
        return {"content": result}
    except Exception as e:
        logger.error(f"Error in Monthy scraping: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error in Monthy scraping: {str(e)}")

# Add this new endpoint


@app.post("/ask-monty")
async def ask_monty(request: str, gf: GraphFleet = Depends(get_graphfleet)):
    try:
        result = gf.ask_monty(request)
        return {"response": result}
    except Exception as e:
        logger.error(f"Error in Ask Monty: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in Ask Monty: {str(e)}")

# Example route
@app.get("/example")
async def example_route():
    return {"message": "This is an example route."}
