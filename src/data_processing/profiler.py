import pandas as pd
from pandas.api.types import is_numeric_dtype


def profile_dataset(df: pd.DataFrame):
    """Generate a complete profile for the dataset."""

    # Calculate reusable statistics
    missing_values = df.isna().sum()
    unique_values = df.nunique()

    # Count numeric columns
    numeric_count = 0
    for column in df.columns:
        if is_numeric_dtype(df[column]):
            numeric_count += 1

    # Store detailed profile for each column
    column_profiles = {}

    for column in df.columns:

        # Check if the current column is numeric
        is_numeric = is_numeric_dtype(df[column])

        if is_numeric:
            mean_value = df[column].mean()
            median_value = df[column].median()
            std_value = df[column].std()
            min_value = df[column].min()
            max_value = df[column].max()
        else:
            mean_value = None
            median_value = None
            std_value = None
            min_value = None
            max_value = None

        # Save statistics for the current column
        column_profiles[column] = {
            "missing": missing_values[column],
            "unique": unique_values[column],
            "mean": mean_value,
            "median": median_value,
            "std": std_value,
            "min": min_value,
            "max": max_value,
        }

    # Dataset summary
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_columns": numeric_count,
        "categorical_columns": len(df.columns) - numeric_count,
        "missing_values": int(missing_values.sum()),
        "memory_usage": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            2
        ),
    }

    # Schema table
    schema = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing": missing_values.values,
        "Unique": unique_values.values,
        "Mean": [
            column_profiles[col]["mean"] for col in df.columns
        ],
        "Median": [
            column_profiles[col]["median"] for col in df.columns
        ],
        "Std": [
            column_profiles[col]["std"] for col in df.columns
        ],
        "Min": [
            column_profiles[col]["min"] for col in df.columns
        ],
        "Max": [
            column_profiles[col]["max"] for col in df.columns
        ],
    })

    # Return the complete dataset profile
    return {
        "shape": df.shape,
        "summary": summary,
        "schema": schema,
        "column_profiles": column_profiles,
    }
