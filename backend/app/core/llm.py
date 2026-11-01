"""
llm.py
------
Local LLM integration using Ollama with Google Gemma 4 E4B.

Responsibilities:
- Low-level LLM invocation (Ollama)
- SQL-oriented prompting (stateless)
- General chat prompting WITH conversation memory
"""

import requests
from app.core.memory import get_history, add_message

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma4:e4b"


# --------------------------------------------------
# Core LLM call (no assumptions about the task)
# --------------------------------------------------
def _call_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180  # needed for cold starts / large models
    )
    response.raise_for_status()

    return response.json()["response"].strip()


# --------------------------------------------------
# Text-to-SQL LLM (STRICT, STATELESS)
# --------------------------------------------------
def local_llm(prompt: str) -> str:
    """
    LLM call intended for Text-to-SQL and other
    structured, stateless tasks.
    """
    sql_prompt = f"""
You are a precise Text-to-SQL assistant.

Rules:
- Use ONLY the provided database schema.
- Generate ONLY a valid SQL SELECT statement.
- Do not explain the SQL.
- Do not include markdown.
- Do not invent tables or columns.

Task:
{prompt}
"""
    return _call_ollama(sql_prompt)


# --------------------------------------------------
# General Chat LLM WITH Memory
# --------------------------------------------------
def general_chat_with_memory(message: str) -> str:
    """
    Conversational LLM with short-term memory.
    Used for:
    - Explanations
    - Follow-up questions
    - Voice responses
    """

    history = get_history()

    history_text = "\n".join(
        f"{item['role'].capitalize()}: {item['content']}"
        for item in history
    )

    chat_prompt = f"""
You are a helpful, clear, and concise assistant.

Conversation so far:
{history_text}

User:
{message}

Assistant:
"""

    response = _call_ollama(chat_prompt)

    # Update memory AFTER response is generated
    add_message("user", message)
    add_message("assistant", response)

    return response
