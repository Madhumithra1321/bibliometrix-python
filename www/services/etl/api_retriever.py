import requests
import time


OPENALEX_URL = "https://api.openalex.org/works"


def fetch_openalex(query, max_results=100):

    results = []
    per_page = 25
    page = 1

    while len(results) < max_results:

        params = {
            "search": query,
            "per-page": per_page,
            "page": page
        }

        response = requests.get(
            OPENALEX_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        works = data.get("results", [])

        if not works:
            break

        results.extend(works)

        page += 1

        time.sleep(1)

    return results[:max_results]