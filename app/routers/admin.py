from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.indexer import run_indexer, run_prompt_tuning

router = APIRouter()

@router.post("/index")
async def trigger_indexing(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(run_indexer)
        return {"message": "Indexing process started in the background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start indexing process: {str(e)}")

@router.post("/prompt-tune")
async def trigger_prompt_tuning(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(run_prompt_tuning)
        return {"message": "Prompt tuning process started in the background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start prompt tuning process: {str(e)}")