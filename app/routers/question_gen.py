from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.api import generate_questions

router = APIRouter()

class QuestionGenRequest(BaseModel):
    question_history: List[str]
    question_count: int = 5

class QuestionGenResponse(BaseModel):
    questions: List[str]

@router.post("/generate_questions", response_model=QuestionGenResponse)
async def api_generate_questions(request: QuestionGenRequest):
    questions = await generate_questions(request.question_history, request.question_count)
    return QuestionGenResponse(questions=questions)