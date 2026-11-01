from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.router import route_intent
from app.agents.text_to_sql import text_to_sql_agent
from app.agents.real_estate import real_estate_agent
from app.core.llm import local_llm
from app.core.llm import general_chat_with_memory

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):
    intent = route_intent(request.message)

    if intent == "sql":
        return text_to_sql_agent(request.message, local_llm)

    if intent == "real_estate":
        return real_estate_agent(request.message)

    # General chat fallback
    return {
        "agent": "general_chat",
        "response": general_chat_with_memory(request.message)
    }