import pandas as pd


def assess_data_quality(df: pd.DataFrame):
    """Assess the overall quality of a dataset."""

    duplicate_rows = df.duplicated().sum()

    issues = []
    passed = True

    if duplicate_rows > 0:
        passed = False
        issues.append({
            "type": "duplicate_rows",
            "severity": "warning",
            "message": f"{duplicate_rows} duplicate rows found."})

    constant_columns = []

    for column in df.columns:
        if df[column].nunique() == 1:
            constant_columns.append(column)

    if constant_columns:
        passed = False
        issues.append({
            "type": "constant_columns",
            "severity": "warning",
            "message": ", ".join(constant_columns)
        })

    return {
        "passed": passed,
        "issues": issues
    }
