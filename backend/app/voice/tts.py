"""
tts.py
------
Text-to-Speech using pyttsx3 (Windows native).
"""

import pyttsx3
import uuid
import os

_engine = pyttsx3.init()


def text_to_speech(text: str) -> str:
    output_dir = "voice_output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")

    _engine.save_to_file(text, output_path)
    _engine.runAndWait()

    return output_path