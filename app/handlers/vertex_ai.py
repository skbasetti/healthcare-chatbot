from fastapi import APIRouter, Query, HTTPException
from typing import Dict
import os
import vertexai
from vertexai.language_models import ChatModel
from vertexai.language_models._language_models import ChatResponse

router = APIRouter()

@router.get("/ask", response_model=Dict[str, str])
async def ask(query: str = Query(..., description="The question to ask the AI model")) -> Dict[str, str]:
    try:
        # Initialize Vertex AI with project details
        vertexai.init(
            project=os.getenv("GOOGLE_CLOUD_PROJECT", "astral-outpost-460600-p3"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-south1")
        )
        
        # Initialize chat model and get response
        chat_model = ChatModel.from_pretrained("chat-bison@001")
        chat = chat_model.start_chat()
        response: ChatResponse = chat.send_message(query)
        
        return {
            "query": query,
            "response": response.text
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )