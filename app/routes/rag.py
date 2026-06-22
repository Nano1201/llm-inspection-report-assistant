from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import answer_question_with_rag

router = APIRouter(prefix="/rag", tags=["rag"])


class RagAskRequest(BaseModel):
    question: str
    top_k: int = 5


@router.post("/ask")
async def rag_ask(request: RagAskRequest):
    """
    Ask a question and answer it using retrieved document chunks.
    """
    result = answer_question_with_rag(
        question=request.question,
        top_k=request.top_k,
    )

    return {
        "question": request.question,
        "top_k": request.top_k,
        "answer": result["answer"],
        "sources": result["sources"],
    }