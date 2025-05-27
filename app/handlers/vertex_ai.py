from fastapi import APIRouter, Query
import vertexai
from vertexai.language_models import ChatModel

router = APIRouter()

@router.get("/ask")
def ask(query: str = Query(...)):
    vertexai.init(project="astral-outpost-460600-p3", location="us-south1")
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat()
    response = chat.send_message(query)
    return {"query": query, "response": response.text}