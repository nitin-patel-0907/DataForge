import pandas as pd

# ==========================================================
# Configuration
# ==========================================================

HIGH_MISSING_THRESHOLD = 50

DUPLICATE_ROWS_PENALTY = 10
CONSTANT_COLUMNS_PENALTY = 10
HIGH_MISSING_PENALTY = 20


def assess_data_quality(df: pd.DataFrame):
    """Assess the overall quality of a dataset."""

    # ======================================================
    # Overall Assessment
    # ======================================================

    passed = True
    issues = []

    score = 100

    # ======================================================
    # Rule 1: Duplicate Rows
    # ======================================================

    duplicate_rows = df.duplicated().sum()

    if duplicate_rows > 0:

        passed = False
        score -= DUPLICATE_ROWS_PENALTY

        issues.append({
            "type": "duplicate_rows",
            "severity": "warning",
            "message": f"{duplicate_rows} duplicate rows found."
        })

    # ======================================================
    # Rule 2: Constant Columns
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
        score -= CONSTANT_COLUMNS_PENALTY

        issues.append({
            "type": "constant_columns",
            "severity": "warning",
            "message": (
                "Constant columns found: "
                + ", ".join(constant_columns)
            )
        })

    # ======================================================
    # Rule 3: High Missing Value Columns
    # ======================================================

    high_missing_columns = []

    for column in df.columns:

        missing_percentage = (
            df[column].isna().sum() / len(df)
        ) * 100

        if (
            missing_percentage > HIGH_MISSING_THRESHOLD
            and missing_percentage < 100
        ):
            high_missing_columns.append(
                f"{column} ({missing_percentage:.1f}%)"
            )

    if high_missing_columns:

        passed = False
        score -= HIGH_MISSING_PENALTY

        issues.append({
            "type": "high_missing_columns",
            "severity": "warning",
            "message": (
                "High missing value columns: "
                + ", ".join(high_missing_columns)
            )
        })

    # ======================================================
    # Final Score
    # ======================================================

    score = max(score, 0)

    if score >= 90:
        grade = "Excellent"

    elif score >= 75:
        grade = "Good"

    elif score >= 60:
        grade = "Fair"

    else:
        grade = "Poor"

    # ======================================================
    # Return Report
    # ======================================================

    return {
        "passed": passed,
        "score": score,
        "grade": grade,
        "issues": issues
    }
