from typing import Dict, Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.config import Settings, get_settings
from app.services.prompt_tune import PromptTuneService
from app.api.deps import get_prompt_tune_service

router = APIRouter()

class PromptTuneRequest(BaseModel):
    root_dir: str
    config: Dict[str, any]
    no_entity_types: bool = False
    output_dir: Optional[str] = None

class PromptTuneResponse(BaseModel):
    prompts: Dict[str, str]

@router.post("/tune", response_model=PromptTuneResponse)
async def tune_prompts(
    request: PromptTuneRequest,
    settings: Settings = Depends(get_settings),
    prompt_tune_service: PromptTuneService = Depends(get_prompt_tune_service),
) -> PromptTuneResponse:
    """Tune prompts for different components of the system."""
    try:
        root_dir = Path(request.root_dir)
        output_dir = Path(request.output_dir) if request.output_dir else None
        
        prompts = await prompt_tune_service.tune_prompts(
            root_dir=root_dir,
            config=request.config,
            no_entity_types=request.no_entity_types,
            output_dir=output_dir,
        )
        
        return PromptTuneResponse(prompts=prompts)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to tune prompts: {str(e)}",
        )
