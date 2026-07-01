import pandas as pd


def validate_dataset(df: pd.DataFrame):
    """
    Validate the uploaded dataset.

    Returns:
        dict: Validation result containing:
            - valid (bool): Whether the dataset passed validation.
            - message (str | None): Error message for fatal validation failures.
            - warnings (list): Non-fatal validation warnings.
    """

    warnings = []

    # ==========================================================
    # Validation 1: Dataset contains no rows
    # ==========================================================
    if df.empty:
        return {
            "valid": False,
            "message": "The uploaded dataset is empty.",
            "warnings": []
        }

    # ==========================================================
    # Validation 2: Detect completely empty columns
    # ==========================================================
    empty_columns = []

    for column in df.columns:
        if df[column].isna().all():
            empty_columns.append(column)

    if empty_columns:
        warnings.append(
            f"Completely empty columns: {', '.join(empty_columns)}"
        )

    # ==========================================================
    # Validation passed
    # ==========================================================
    return {
        "valid": True,
        "message": None,
        "warnings": warnings
    }