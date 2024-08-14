from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import shlex

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatHistory(BaseModel):
    messages: list[ChatMessage]

# In-memory storage for chat history
chat_history = []

# Allowlist of accepted search methods
ALLOWED_METHODS = ["local", "global"]

def process_query(query: str, search_method: str) -> str:
    if search_method not in ALLOWED_METHODS:
        raise HTTPException(status_code=400, detail=f"Invalid search method: {search_method}")

    cmd = [
        "python3", "-m", "graphrag.query",
        "--root", "./graphfleet",
        "--method", search_method,
    ]
    cmd.append(shlex.quote(query))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        response = output.split(f"SUCCESS: {search_method.capitalize()} Search Response:", 1)[-1].strip()
        return response
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e.stderr}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the GraphFleet API"}

@app.post("/process_local_query/")
async def process_local_query_endpoint(request: QueryRequest):
    response = process_query(request.query, "local")
    return {"response": response}

@app.post("/process_global_query/")
async def process_global_query_endpoint(request: QueryRequest):
    response = process_query(request.query, "global")
    return {"response": response}

@app.post("/add_message/")
async def add_message(message: ChatMessage):
    chat_history.append(message)
    return {"status": "Message added"}

@app.get("/get_chat_history/")
async def get_chat_history():
    return {"messages": chat_history}

@app.delete("/clear_chat_history/")
async def clear_chat_history():
    chat_history.clear()
    return {"status": "Chat history cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed port to 8001
