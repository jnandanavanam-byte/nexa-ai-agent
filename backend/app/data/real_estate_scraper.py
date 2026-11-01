"""
real_estate_scraper.py
----------------------
Fetch real estate listings using Firecrawl.
"""

import os
from firecrawl import FirecrawlApp

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)


def fetch_listings(location: str):
    """
    Fetch real estate listings for a given location.
    """

    query_url_map = {
        "Dubai": "https://www.propertyfinder.ae/en/rent/dubai.html",
        "Abu Dhabi": "https://www.propertyfinder.ae/en/rent/abu-dhabi.html",
    }

    url = query_url_map.get(location)
    if not url:
        return []

    result = app.scrape_url(url)

    # Return raw page text (LLM will normalize)
    return result.get("content", "")