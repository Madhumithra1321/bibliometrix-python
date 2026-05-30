from .schema import (
    MANDATORY_COLUMNS,
    MULTI_VALUE_COLUMNS
)


def validate_columns(df):
    """
    Ensure all required columns exist.
    """

    missing = [
        col
        for col in MANDATORY_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing mandatory columns: {missing}"
        )

    return True


def validate_nulls(df):
    """
    Ensure no null values remain.
    """

    if df.isnull().values.any():
        raise ValueError(
            "Dataset contains null values."
        )

    return True


def validate_multivalue_types(df):
    """
    Ensure multivalue columns contain lists.
    """

    for col in MULTI_VALUE_COLUMNS:

        if col not in df.columns:
            continue

        for value in df[col]:

            if not isinstance(value, list):
                raise TypeError(
                    f"{col} contains non-list value."
                )

    return True


def validate_dataframe(df):
    """
    Full validation pipeline.
    """

    validate_columns(df)
    validate_nulls(df)
    validate_multivalue_types(df)

    return True