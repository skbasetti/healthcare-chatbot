from fastapi import FastAPI
from handlers import claims, benefits, vertex_ai

app = FastAPI()

# Register API routers
app.include_router(claims.router)
app.include_router(benefits.router)
app.include_router(vertex_ai.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return {"message": "Welcome to the Health Claims API!"}