from pydantic import BaseModel
from typing import Any, Dict, List

class ChatResponse(BaseModel):
    answer: str
    sql: str
    rows: List[Dict[str, Any]]
    notes: List[str] = []

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None