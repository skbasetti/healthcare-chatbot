# In your vertex_ai.py file

from fastapi import APIRouter, Query, HTTPException
from typing import Dict
import os
import vertexai
from vertexai.generative_models import GenerativeModel # Ensure this import is present
import logging

router = APIRouter()

# Optional: Add logger for visibility in Cloud Run logs
logger = logging.getLogger("uvicorn.error")

# ... (your /ask endpoint with ChatModel can remain as is if you want it as a backup or for other tests) ...

@router.get("/ask-gemini", response_model=Dict[str, str])
async def ask_gemini(query: str = Query(..., description="The question to ask the Gemini model")) -> Dict[str, str]:
    try:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "astral-outpost-460600-p3") # Ensure this is your correct project
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # Ensure this is your correct location
        
        logger.info(f"Initializing Vertex AI Generative Models for project={project_id}, location={location}")
        
        # Explicitly initialize Vertex AI. This is good practice.
        vertexai.init(project=project_id, location=location)
        
        # --- MODIFICATION FOR DEMO RELIABILITY ---
        # Pick ONE specific Gemini model that you have tested and works in your project/region.
        # Example: "gemini-1.5-flash" or "gemini-1.0-pro"
        chosen_model_name = "gemini-1.5-flash-001" # <--- *** REPLACE WITH YOUR TESTED GEMINI MODEL NAME ***
        
        logger.info(f"Attempting to use Gemini model: {chosen_model_name}")
        
        try:
            model = GenerativeModel(chosen_model_name)
            
            # Construct a clear prompt for the healthcare assistant context
            healthcare_prompt = f"""You are a healthcare assistant for insurance inquiries. 
            Provide helpful, accurate information.
            Always remind users to consult official healthcare professionals for medical advice and their insurance provider for official coverage details.
            
            User question: {query}
            
            Response:"""
            
            response = model.generate_content(healthcare_prompt)
            
            # Check if response.text is None or empty before accessing it
            response_text = ""
            if response.candidates and response.candidates[0].content.parts and response.candidates[0].content.parts[0].text:
                response_text = response.candidates[0].content.parts[0].text
            else:
                logger.warning(f"Gemini model {chosen_model_name} produced no text output for query: {query}")
                response_text = "I'm sorry, I couldn't generate a response for that query at the moment."

            return {
                "query": query,
                "response": response_text,
                "model_used": chosen_model_name
            }
            
        except Exception as model_error:
            logger.error(f"Failed to use Gemini model {chosen_model_name}: {str(model_error)}")
            # Specific error for model failure
            raise HTTPException(
                status_code=500,
                detail=f"Error interacting with the AI model ({chosen_model_name}): {str(model_error)}"
            )
        # --- END OF MODIFICATION ---
        
    except Exception as e:
        # Catch-all for other unexpected errors (e.g., initialization issues not caught above)
        logger.error(f"A general error occurred in /ask-gemini: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while processing your request: {str(e)}"
        )

# Health check endpoint (keep this as it's useful)
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "vertex-ai-handler"}