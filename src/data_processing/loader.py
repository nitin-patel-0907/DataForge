import pandas as pd
from pandas.errors import EmptyDataError


def load_dataset(file):
    """Load a CSV file into a pandas DataFrame."""

    try:
        return pd.read_csv(file)

    except EmptyDataError:
        raise ValueError("The uploaded file is empty.")


def get_dataset_info(df):
    """Return basic information about a dataset."""
    schema = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })
    return {
        "shape": df.shape,
        "schema": schema,
    }
