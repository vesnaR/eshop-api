
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ai_service import get_ai_response
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = get_ai_response(request.question)
        return ChatResponse(answer=answer)
    except Exception:
        logger.exception("AI assistant request failed")
        raise HTTPException(
            status_code=500,
            detail="AI assistant is temporarily unavailable",
        )
