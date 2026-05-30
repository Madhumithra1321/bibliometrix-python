"""
Dispatcher for selecting mappings
based on source database.
"""

from .mappings import (
    SCOPUS_MAPPING,
    DIMENSIONS_MAPPING,
    PUBMED_MAPPING,
    OPENALEX_MAPPING
)


def get_mapping(source: str):
    source = source.upper()

    if source == "SCOPUS":
        return SCOPUS_MAPPING

    if source == "DIMENSIONS":
        return DIMENSIONS_MAPPING

    if source == "PUBMED":
        return PUBMED_MAPPING

    if source == "OPENALEX":
        return OPENALEX_MAPPING

    raise ValueError(f"Unsupported source: {source}")