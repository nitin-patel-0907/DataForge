import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

# Warn the user if a column has more than 50% missing values
HIGH_MISSING_THRESHOLD = 50


def assess_data_quality(df: pd.DataFrame):
    """Assess the overall quality of a dataset."""

    # ======================================================
    # Overall Assessment
    # ======================================================

    passed = True
    issues = []

    # ======================================================
    # Rule 1: Duplicate Rows
    # ======================================================

    duplicate_rows = df.duplicated().sum()

    if duplicate_rows > 0:
        passed = False

        issues.append({
            "type": "duplicate_rows",
            "severity": "warning",
            "message": f"{duplicate_rows} duplicate rows found."
        })

    # ======================================================
    # Rule 2: Constant Columns
    # Ignore completely empty columns because the validator
    # already reports them.
    # ======================================================

    constant_columns = []

    for column in df.columns:
        if (
            df[column].nunique() == 1
            and not df[column].isna().all()
        ):
            constant_columns.append(column)

    if constant_columns:
        passed = False

        issues.append({
            "type": "constant_columns",
            "severity": "warning",
            "message": (
                f"Constant columns found: "
                f"{', '.join(constant_columns)}"
            )
        })

    # ======================================================
    # Rule 3: High Missing Value Columns
    # Ignore completely empty columns because the validator
    # already reports them.
    # ======================================================

    high_missing_columns = []

    for column in df.columns:

        missing_values = df[column].isna().sum()
        missing_percentage = (
            missing_values / len(df)
        ) * 100

        if (
            missing_percentage > HIGH_MISSING_THRESHOLD
            and missing_percentage < 100
        ):
            high_missing_columns.append({
                "column": column,
                "percentage": round(missing_percentage, 2)
            })

    if high_missing_columns:
        passed = False

        message = []

        for item in high_missing_columns:
            message.append(
                f"{item['column']} ({item['percentage']}%)"
            )

        issues.append({
            "type": "high_missing_columns",
            "severity": "warning",
            "message": (
                "High missing value columns: "
                + ", ".join(message)
            )
        })

    # ======================================================
    # Return Quality Report
    # ======================================================

    return {
        "passed": passed,
        "issues": issues
    }