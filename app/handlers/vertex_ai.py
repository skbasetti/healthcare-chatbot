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
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        # Log startup for debugging
        logger.info(f"Initializing Vertex AI for project={project_id} location={location}")
        
        vertexai.init(project=project_id, location=location)
        
        # Fix: Use correct model name for ChatModel
        # Valid ChatModel names: "chat-bison", "chat-bison@001", "chat-bison@002"
        chat_model = ChatModel.from_pretrained("chat-bison")
        
        # Healthcare-focused context
        healthcare_context = """You are a helpful healthcare assistant for insurance and medical inquiries. 
        Provide informative, accurate responses while always reminding users to:
        1. Consult healthcare professionals for medical advice
        2. Contact their insurance provider for official coverage decisions
        3. Seek emergency care for urgent medical situations
        
        Keep responses concise, helpful, and professional."""
        
        # Start chat with healthcare context
        chat = chat_model.start_chat(
            context=healthcare_context
        )
        
        # Configure parameters for healthcare responses
        response = chat.send_message(
            query,
            temperature=0.3,  # Lower temperature for more consistent healthcare responses
            max_output_tokens=512,
            top_p=0.8,
            top_k=40
        )
        
        return {
            "query": query,
            "response": response.text,
            "model_used": "chat-bison"
        }

    except Exception as e:
        logger.error(f"Vertex AI chat failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

# Alternative endpoint using newer Generative Models (if available)
@router.get("/ask-gemini", response_model=Dict[str, str])
async def ask_gemini(query: str = Query(..., description="The question to ask the Gemini model")) -> Dict[str, str]:
    try:
        from vertexai.generative_models import GenerativeModel
        
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "astral-outpost-460600-p3")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        
        logger.info(f"Initializing Vertex AI Generative Models for project={project_id}")
        
        vertexai.init(project=project_id, location=location)
        
        # Try different Gemini models in order of preference
        model_names = ["gemini-1.0-pro", "gemini-1.5-flash", "text-bison@001"]
        
        for model_name in model_names:
            try:
                model = GenerativeModel(model_name)
                
                healthcare_prompt = f"""You are a healthcare assistant for insurance inquiries. 
                Provide helpful, accurate information while reminding users to consult healthcare professionals.
                
                User question: {query}
                
                Response:"""
                
                response = model.generate_content(healthcare_prompt)
                
                return {
                    "query": query,
                    "response": response.text,
                    "model_used": model_name
                }
                
            except Exception as model_error:
                logger.warning(f"Model {model_name} failed: {model_error}")
                continue
        
        raise Exception("No available Gemini models found")
        
    except Exception as e:
        logger.error(f"Gemini model failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request with Gemini: {str(e)}"
        )

# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "vertex-ai-handler"}