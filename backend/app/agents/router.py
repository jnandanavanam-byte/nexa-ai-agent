"""
router.py
---------
Intent classification router for Nexa AI.
"""

from app.core.llm import local_llm


def route_intent(user_message: str) -> str:
    prompt = f"""
Classify the following user request into ONE category.

Categories:
- sql
- real_estate
- general_chat

Return ONLY the category name.

User message:
{user_message}

Category:
"""

    response = local_llm(prompt).strip().lower()

    if "sql" in response:
        return "sql"
    if "real" in response or "estate" in response or "property" in response:
        return "real_estate"

    return "general_chat"