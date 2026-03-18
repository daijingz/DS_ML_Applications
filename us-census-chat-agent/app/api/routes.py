from fastapi import APIRouter, Depends
from app.api.schemas import ChatRequest, ChatResponse
from app.api.deps import get_chat_service
from app.services.chat_service import ChatService

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, service: ChatService = Depends(get_chat_service)):
    result = service.handle_message(payload.message, payload.session_id)
    return ChatResponse(
        answer=result.get("answer", ""),
        sql=result.get("sql"),
        rows=result.get("rows", []),
    )