import pandas as pd
from .dispatcher import get_mapping
from .schema import (
    MULTI_VALUE_COLUMNS,
    REQUIRED_COLUMNS
)

def ensure_required_columns(df):

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    return df

def split_multi_value(value):
    
    if pd.isna(value) or value == "":
        return []

    if isinstance(value, list):
        return value

    return [
        item.strip()
        for item in str(value).replace(",", ";").split(";")
        if item.strip()
    ]


def standardize_nulls(df):
    
    return df.fillna("")


def rename_columns(df, source):
    
    mapping = get_mapping(source)
    
    existing_mapping = {
        k: v
        for k, v in mapping.items()
        if k in df.columns
    }

    return df.rename(columns=existing_mapping)


def standardize_multivalue_columns(df):
    
    for col in MULTI_VALUE_COLUMNS:

        if col not in df.columns:
            continue

        df[col] = df[col].apply(split_multi_value)

    return df

def ensure_required_columns(df):

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    return df

def transform_dataframe(df, source):

    df = rename_columns(df, source)

    df = standardize_nulls(df)

    df = ensure_required_columns(df)

    df = standardize_multivalue_columns(df)

    return df