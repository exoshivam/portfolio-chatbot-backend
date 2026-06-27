from fastapi import APIRouter

from core.chatbot import Chatbot
from models.request import ChatRequest
from models.response import ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

chatbot = Chatbot()


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer = chatbot.chat(request.message)

    return ChatResponse(
        response=answer
    )