import pandas as pd

from .api_retriever import (
    fetch_openalex,
    openalex_to_records
)

from .transformer import transform_dataframe
from .validator import validate_dataframe


def openalex_pipeline(query, max_results=100):

    results = fetch_openalex(
        query=query,
        max_results=max_results
    )

    records = openalex_to_records(results)

    df = pd.DataFrame(records)

    df = transform_dataframe(
        df,
        source="openalex"
    )

    validate_dataframe(df)

    return df