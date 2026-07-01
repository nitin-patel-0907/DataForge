import pandas as pd


def load_dataset(file):
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file)


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
