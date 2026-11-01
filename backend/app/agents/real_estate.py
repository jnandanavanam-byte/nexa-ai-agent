"""
real_estate.py
---------------
LLM-powered Real Estate Agent for Nexa.
Supports live scraping with safe fallback to mock listings.
"""

import json
import re
from typing import Dict, List

from app.core.llm import local_llm
from app.data.real_estate_listings import LISTINGS
from app.data.real_estate_scraper import fetch_listings


# -------------------------
# JSON extraction helpers
# -------------------------

def extract_json_object(text: str) -> Dict:
    """
    Extract the first JSON object {...} from LLM output.
    """
    match = re.search(r"\{[\s\S]*?\}", text)
    if not match:
        raise ValueError("No JSON object found in LLM response")
    return json.loads(match.group(0))


def extract_json_array(text: str) -> List[Dict]:
    """
    Extract the first JSON array [...] from LLM output.
    """
    match = re.search(r"\[[\s\S]*?\]", text)
    if not match:
        return []
    return json.loads(match.group(0))


# -------------------------
# Listing normalization
# -------------------------

def normalize_listings(raw_text: str) -> List[Dict]:
    """
    Convert raw scraped text into structured listings using LLM.
    """
    prompt = f"""
Extract real estate listings from the text below.

Return ONLY a JSON array.
Do NOT include explanations.

Each listing must contain:
- title
- location
- property_type (apartment | villa)
- bedrooms (number)
- price (number)

Text:
{raw_text}

JSON:
"""

    response = local_llm(prompt)
    return extract_json_array(response)


# -------------------------
# Filtering logic
# -------------------------

def filter_listings(criteria: Dict, listings: List[Dict]) -> List[Dict]:
    results = []

    for item in listings:
        if criteria.get("location") and item.get("location") != criteria["location"]:
            continue

        if criteria.get("property_type") and item.get("property_type") != criteria["property_type"]:
            continue

        if criteria.get("bedrooms") and item.get("bedrooms") != criteria["bedrooms"]:
            continue

        if criteria.get("budget_max") and item.get("price") and item["price"] > criteria["budget_max"]:
            continue

        results.append(item)

    return results


# -------------------------
# Main agent
# -------------------------

def real_estate_agent(user_query: str) -> Dict:
    """
    Parse criteria using LLM, fetch live data, filter results.
    """

    prompt = f"""
You are a real estate assistant.

Return ONLY a valid JSON object.
Do NOT include explanations.

Required fields:
- location (string or null)
- property_type (apartment | villa | null)
- bedrooms (number or null)
- budget_max (number or null)
- transaction (rent | buy | null)

User query:
{user_query}

JSON:
"""

    try:
        response = local_llm(prompt)
        criteria = extract_json_object(response)
    except Exception as e:
        return {
            "agent": "real_estate",
            "criteria": {
                "location": None,
                "property_type": None,
                "bedrooms": None,
                "budget_max": None,
                "transaction": None,
            },
            "results": [],
            "error": f"Criteria extraction failed: {str(e)}",
        }

    # -------- Live scraping first --------
    listings = []
    try:
        raw_text = fetch_listings(criteria.get("location"))
        listings = normalize_listings(raw_text)
    except Exception:
        listings = []

    # -------- Fallback to mock data --------
    if not listings:
        listings = LISTINGS

    results = filter_listings(criteria, listings)

    return {
        "agent": "real_estate",
        "criteria": criteria,
        "results": results,
        "message": f"Found {len(results)} matching properties."
    }