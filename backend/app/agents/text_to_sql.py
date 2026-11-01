import re

from sqlalchemy import text
from app.core.db_schema import get_schema_description
from app.core.db_init import engine


def extract_sql(llm_response: str) -> str:
    """
    Extract the complete SELECT statement from an LLM response.
    """
    response = re.sub(r"```(?:sql)?", "", llm_response, flags=re.IGNORECASE)
    select_match = re.search(r"\bSELECT\b", response, flags=re.IGNORECASE)
    if select_match:
        sql = response[select_match.start():]
        explanation_match = re.search(
            r"\n\s*(?:Explanation|Reasoning)\s*:",
            sql,
            flags=re.IGNORECASE,
        )
        if explanation_match:
            sql = sql[:explanation_match.start()]

        sql = sql.strip().rstrip(";").strip()
        if sql:
            return f"{sql};"

    raise ValueError("No SELECT statement found in LLM response.")


def is_safe_sql(sql: str) -> bool:
    sql_upper = sql.strip().upper()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False

    # Must contain FROM
    if " FROM " not in sql_upper:
        return False

    # Disallow dangerous keywords
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]
    if any(word in sql_upper for word in forbidden):
        return False

    return True


def execute_sql(sql: str):
    if not is_safe_sql(sql):
        raise ValueError("Unsafe SQL query detected.")

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = result.keys()

    return {
        "columns": list(columns),
        "rows": [list(row) for row in rows]
    }


def normalize_prompt(prompt: str) -> str:
    """
    Groq requires clean, compact prompt strings.
    This removes indentation and blank lines safely.
    """
    return "\n".join(
        line.strip()
        for line in prompt.strip().splitlines()
        if line.strip()
    )


def text_to_sql_agent(user_question: str, llm_client) -> dict:
    schema = get_schema_description()

    prompt = f"""
You are a Text-to-SQL assistant.

=== Database Schema ===
{schema}

=== Rules ===
1. Generate only SELECT queries.
2. Use only the given schema.
3. Do not invent columns or tables.
4. Return at most 100 rows.
5. Output SQL and explanation.

=== Output Format ===
SQL:
<SQL query>

Explanation:
<brief explanation>

=== User Question ===
{user_question}
"""

    # ✅ Normalize prompt for provider compatibility
    clean_prompt = normalize_prompt(prompt)

    # ✅ Call LLM safely
    try:
        response = llm_client(clean_prompt)
    except Exception as e:
        return {
            "error": "LLM call failed",
            "details": str(e)
        }

    # ✅ Extract and validate SQL
    try:
        sql_query = extract_sql(response)
    except Exception as e:
        return {
            "error": "SQL extraction failed",
            "details": str(e),
            "llm_response": response
        }

    # ✅ Enforce LIMIT
    if "LIMIT" not in sql_query.upper():
        sql_query = sql_query.rstrip(";") + " LIMIT 100;"

    # ✅ Execute query
    try:
        data = execute_sql(sql_query)
    except Exception as e:
        return {
            "error": "SQL execution failed",
            "details": str(e),
            "sql": sql_query
        }

    # ✅ Safe explanation handling
    if "Explanation:" in response:
        explanation_text = response.split("Explanation:")[-1].strip()
    else:
        explanation_text = "SQL query generated and executed successfully."

    return {
        "sql": sql_query,
        "data": data,
        "explanation": explanation_text
    }