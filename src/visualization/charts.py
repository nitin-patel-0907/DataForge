import matplotlib.pyplot as plt
import pandas as pd


def create_histogram(df: pd.DataFrame, column: str):
    """Create a histogram for a numeric column."""

    fig, ax = plt.subplots()

    ax.hist(
        df[column],
        bins=20
    )

    ax.set_title(f"Distribution of {column}")

    ax.set_xlabel(column)

    ax.set_ylabel("Frequency")
    
    fig.tight_layout()

    return fig
