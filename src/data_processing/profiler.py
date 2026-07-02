import pandas as pd


def profile_dataset(df: pd.DataFrame):
    """Generate basic profile information for a dataset."""

    # Calculate missing values once
    missing_values = df.isna().sum()

    # Calculate unique values once
    unique_values = df.nunique()

    # Build schema table
    schema = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing": missing_values.values,
        "Unique": unique_values
    })

    # Build column profiles
    column_profiles = {}

    for column in df.columns:
        column_profiles[column] = {
            "missing": missing_values[column],
            "unique": unique_values[column]
        }

    # Return complete profile
    return {
        "shape": df.shape,
        "schema": schema,
        "column_profiles": column_profiles
    }
