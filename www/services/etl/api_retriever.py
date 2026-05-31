import requests
import time


OPENALEX_URL = "https://api.openalex.org/works"


def fetch_openalex(query, max_results=100):

    results = []
    per_page = 25
    page = 1
    retries = 3

    while len(results) < max_results:

        params = {
            "search": query,
            "per-page": per_page,
            "page": page
        }

        success = False

        for attempt in range(retries):

            try:

                response = requests.get(
                    OPENALEX_URL,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

                works = data.get("results", [])

                if not works:
                    return results[:max_results]

                results.extend(works)

                success = True

                break

            except requests.exceptions.RequestException:

                time.sleep(2)

        if not success:
            break

        page += 1

        time.sleep(1)

    return results[:max_results]


def openalex_to_records(results):

    records = []

    for work in results:

        authors = [
            a.get("author", {}).get("display_name", "")
            for a in work.get("authorships", [])
        ]

        affiliations = []

        for a in work.get("authorships", []):
            for inst in a.get("institutions", []):
                name = inst.get("display_name", "")
                if name:
                    affiliations.append(name)

        keywords = [
            k.get("display_name", "")
            for k in work.get("keywords", [])
        ]

        concepts = [
            c.get("display_name", "")
            for c in work.get("concepts", [])
        ]

        record = {
            "DB": "OPENALEX",
            "UT": work.get("id", ""),
            "DI": work.get("doi", ""),
            "TI": work.get("title", ""),
            "PY": work.get("publication_year", ""),
            "AB": str(work.get("abstract_inverted_index", {})),
            "TC": work.get("cited_by_count", 0),
            "CR": work.get("referenced_works", []),
            "SO": work.get("display_name", ""),
            "SR": work.get("display_name", ""),
            "AU": authors,
            "AF": authors,
            "DE": keywords,
            "ID": concepts,
            "C1": affiliations,
            "DT": work.get("type", ""),
            "LA": work.get("language", ""),
            "RP": authors[0] if authors else ""
        }

        records.append(record)

    return records