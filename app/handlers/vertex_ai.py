from fastapi import APIRouter, Query, HTTPException
from typing import Dict
import os
import vertexai
from vertexai.language_models import ChatModel
import logging

router = APIRouter()

# Optional: Add logger for visibility in Cloud Run logs
logger = logging.getLogger("uvicorn.error")

@router.get("/ask", response_model=Dict[str, str])
async def ask(query: str = Query(..., description="The question to ask the AI model")) -> Dict[str, str]:
    try:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "astral-outpost-460600-p3")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-south1")
        
        # Log startup for debugging
        logger.info(f"Initializing Vertex AI for project={project_id} location={location}")
        
        vertexai.init(project=project_id, location=location)
        chat_model = ChatModel.from_pretrained("chat-bison@001")
        chat = chat_model.start_chat()
        response = chat.send_message(query)
        
        return {
            "query": query,
            "response": response.text
        }

    except Exception as e:
        logger.error(f"Vertex AI chat failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )
