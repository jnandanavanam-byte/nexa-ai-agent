from fastapi import APIRouter, UploadFile, File
from app.voice.stt import speech_to_text
from app.voice.tts import text_to_speech
from app.api.chat import chat, ChatRequest

router = APIRouter()


@router.post("/voice")
async def voice_chat(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"

    with open(audio_path, "wb") as f:
        f.write(await file.read())

    # Speech → Text
    user_text = speech_to_text(audio_path)

    # Text → Agent Router → Response
    response = chat(ChatRequest(message=user_text))

    # Text → Speech
    audio_response_path = text_to_speech(
        response.get("response", "")
    )

    return {
        "recognized_text": user_text,
        "agent": response.get("agent"),
        "audio_response_path": audio_response_path
    }