from exa_py import Exa
import requests
import os

exa = Exa()


def web_search(query: str) -> list[dict]:
    """Search the web via Exa and return simplified results."""
    try:
        results = exa.search_and_contents(query, num_results=5)
        return [{"title": r.title, "url": r.url, "text": r.text} for r in results.results]
    except ValueError as e:
        # Exa's SDK raises ValueError for non-2xx API responses (bad key, rate limit, etc.)
        return [{"error": f"Exa API error: {e!s}"}]
    except requests.exceptions.RequestException as e:
        # Network-level failures — timeout, DNS, connection refused
        return [{"error": f"Network error contacting Exa: {e!s}"}]
