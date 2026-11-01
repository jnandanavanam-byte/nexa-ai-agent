from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.voice import router as voice_router

app = FastAPI(title="Nexa AI Assistant")
app.include_router(chat_router)
app.include_router(voice_router)

@app.get("/")
def health_check():
    return {"status": "Nexa is running"}