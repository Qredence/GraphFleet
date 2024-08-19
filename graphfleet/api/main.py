from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
from .utils import (
    upload_files, 
    build_index, 
    delete_index, 
    list_indexes, 
    index_status,
    global_search, 
    global_search_streaming, 
    local_search,
    get_graph_stats, 
    save_graphml_file,
    get_report,
    get_entity,
    get_relationship,
    get_claim,
    get_text_unit
)
from .models import (
    UploadFilesRequest, 
    BuildIndexRequest,
    QueryRequest,
    SourceRequest
)

app = FastAPI()

# --- Data Management --- 

@app.post("/upload")
async def upload_files_endpoint(files: List[UploadFile] = File(...)): 
    """Uploads files to the local data directory."""
    return upload_files(files)

@app.delete("/data/{storage_name}")
async def delete_files_endpoint(storage_name: str):
    """Deletes files from the local data directory.
       Note: 'storage_name' is assumed to be a directory within the data path. 
    """
    data_dir = "data"
    dir_to_delete = os.path.join(data_dir, storage_name) 
    if os.path.exists(dir_to_delete) and os.path.isdir(dir_to_delete):
        try:
            shutil.rmtree(dir_to_delete)
            return JSONResponse(content={"message": f"Directory '{storage_name}' deleted successfully!"}, status_code=200)
        except OSError as e:
            return JSONResponse(content={"message": f"Error deleting directory: {str(e)}"}, status_code=500)
    else:
        return JSONResponse(content={"message": f"Directory '{storage_name}' not found."}, status_code=404)

@app.get("/data")
async def list_files_endpoint():
    """Lists files in the local data directory."""
    data_directory = "data/"
    try:
        files = os.listdir(data_directory)
        return JSONResponse(content={"files": files}, status_code=200)
    except FileNotFoundError:
        return JSONResponse(content={"message": f"Data directory '{data_directory}' not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": f"Error listing files: {str(e)}"}, status_code=500)

# --- Index Management --- 

@app.post("/index")
async def build_index_endpoint(request: BuildIndexRequest):
    """Builds a GraphRAG index."""
    # Assuming 'data/' is your data directory, modify if needed
    response = build_index(
        storage_name="data/",  # Pass the local data directory
        index_name=request.index_name,
        entity_extraction_prompt_filepath=request.entity_extraction_prompt_filepath,
        community_prompt_filepath=request.community_prompt_filepath,
        summarize_description_prompt_filepath=request.summarize_description_prompt_filepath 
    )
    return JSONResponse(content=response.json())

@app.delete("/index/{index_name}")
async def delete_index_endpoint(index_name: str):
    """Deletes a GraphRAG index. (Implementation needed)"""
    # TODO: Implement logic to delete the index data
    return JSONResponse(content={"message": f"Index '{index_name}' deleted (not implemented yet)"}) 

@app.get("/index")
async def list_indexes_endpoint():
    """Lists available GraphRAG indexes. (Implementation needed)"""
    # TODO: Implement logic to list existing indexes
    return JSONResponse(content={"index_name": ["index1", "index2"]}) # Placeholder

@app.get("/index/status/{index_name}")
async def index_status_endpoint(index_name: str):
    """Gets the status of a GraphRAG index. (Implementation needed)"""
    # TODO: Implement logic to get index status 
    return JSONResponse(content={"status": "Unknown (not implemented yet)"}) # This line should be indented!


# --- Querying --- 

@app.post("/query/global")
async def global_search_endpoint(request: QueryRequest):
    """Performs a global search on a GraphRAG index."""
    response = global_search(
        index_name=request.index_name, 
        query=request.query
    ) 
    return JSONResponse(content=response.json())

@app.post("/query/local")
async def local_search_endpoint(request: QueryRequest):
    """Performs a local search on a GraphRAG index."""
    response = local_search(
        index_name=request.index_name, 
        query=request.query
    )
    return JSONResponse(content=response.json())

# --- (Optional) Streaming Global Search Endpoint --- 

@app.post("/experimental/query/global/streaming")
async def global_search_streaming_endpoint(request: QueryRequest):
    """Performs a streaming global search on a GraphRAG index.
       Note: You might need to adjust the `global_search_streaming`
       function in `utils.py` to be compatible with FastAPI's 
       streaming responses. 
    """
    async def stream_response():
        response = global_search_streaming(
            index_name=request.index_name,
            query=request.query
        )
        for line in response.iter_lines():
            if line:
                yield line 

    return StreamingResponse(stream_response())

# --- Graph Information --- 

@app.get("/graph/stats/{index_name}")
async def get_graph_stats_endpoint(index_name: str):
    """Retrieves statistics about a GraphRAG index."""
    response = get_graph_stats(index_name)
    return JSONResponse(content=response.json())

@app.get("/graph/graphml/{index_name}") 
async def save_graphml_file_endpoint(index_name: str):
    """Downloads a GraphRAG index as a GraphML file."""
    try:
        # Assuming save_graphml_file saves to current directory, 
        # modify if needed. 
        graphml_file_name = f"{index_name}.graphml" 
        save_graphml_file(index_name, graphml_file_name) 
        return FileResponse(graphml_file_name, 
                            media_type="application/xml", 
                            filename=graphml_file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating GraphML: {str(e)}")


# --- Source Retrieval ---

@app.get("/source/{source_type}/{index_name}/{source_id}")
async def get_source_endpoint(source_type: str, index_name: str, source_id: str):
    """Retrieves a specific source from a GraphRAG index."""
    source_functions = {
        "report": get_report,
        "entity": get_entity,
        "relationship": get_relationship,
        "claim": get_claim,
        "text": get_text_unit  
    }

    if source_type not in source_functions:
        return JSONResponse(content={"error": "Invalid source type"}, status_code=400)

    source_function = source_functions[source_type]
    response = source_function(index_name, source_id) 
    return JSONResponse(content=response.json())

# --- (Optional) Prompt Generation --- 

@app.get("/index/config/prompts")
async def generate_prompts_endpoint(storage_name: str, limit: int = 1):
    """Generates prompts for GraphRAG (Implementation needed)."""
    # TODO: Implement logic to generate prompts (refer to previous responses)
    raise HTTPException(status_code=501, detail="Prompt generation not implemented yet.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 
