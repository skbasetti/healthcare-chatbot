from fastapi import APIRouter, Query
from vertexai.preview.language_models import ChatModel

router = APIRouter()

@router.get("/ask")
def ask_vertex_ai(query: str):
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    chat = chat_model.start_chat()
    response = chat.send_message(query)
    return {"response": response.text}
