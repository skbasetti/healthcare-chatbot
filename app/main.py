from fastapi import FastAPI
# Corrected import statement:
from app.handlers import claims, benefits, vertex_ai

app = FastAPI(title="Healthcare Chatbot API") # Added a title for good measure

# Register API routers
app.include_router(claims.router, tags=["Claims"]) # Added tags for better OpenAPI docs
app.include_router(benefits.router, tags=["Benefits"])
app.include_router(vertex_ai.router, tags=["Vertex AI Gemini"]) # Router for /ask-gemini

@app.get("/health")
async def health(): # Changed to async def, good practice in FastAPI
    return {"status": "healthy", "service": "main-api"} # Made health check more informative

@app.get("/")
async def root(): # Changed to async def
    return {"message": "Welcome to the Healthcare Chatbot API. Visit /docs for API documentation."}

# You can also add a basic health check for the root if you want
# or serve your API documentation (FastAPI does this by default at /docs and /redoc)