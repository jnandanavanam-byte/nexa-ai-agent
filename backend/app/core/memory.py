"""
memory.py
---------
Simple in-memory conversation memory.
"""

from collections import deque
from typing import List, Dict

# Keep last N messages per session
MAX_HISTORY = 6

# For now, a single global session (can extend to per-user later)
_chat_history: deque = deque(maxlen=MAX_HISTORY)


def add_message(role: str, content: str):
    _chat_history.append({
        "role": role,
        "content": content
    })


def get_history() -> List[Dict]:
    return list(_chat_history)


def clear_history():
    _chat_history.clear()