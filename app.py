import streamlit as st

# ==========================================================
# Import reusable business logic
# ==========================================================

from src.data_processing.loader import load_dataset
from src.data_processing.validator import validate_dataset
from src.data_processing.profiler import profile_dataset
from src.data_processing.quality import assess_data_quality
from src.visualization.charts import (create_histogram, create_boxplot)

# ==========================================================
# Page Header
# ==========================================================

st.title("📊 DataForge")

st.caption(
    "Analyze, clean, and understand your data—starting with a simple upload."
)

# ==========================================================
# File Upload
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

# ==========================================================
# Main Application
# ==========================================================

if uploaded_file is not None:

    # ------------------------------------------------------
    # Step 1: Load Dataset
    # ------------------------------------------------------

    try:
        df = load_dataset(uploaded_file)

    except ValueError as e:
        st.error(str(e))
        st.stop()

    # ------------------------------------------------------
    # Step 2: Validate Dataset
    # ------------------------------------------------------

    validation_result = validate_dataset(df)

    if not validation_result["valid"]:
        st.error(validation_result["message"])
        st.stop()

    for warning in validation_result["warnings"]:
        st.warning(warning)

    # ------------------------------------------------------
    # Step 3: Profile Dataset
    # ------------------------------------------------------

    profile = profile_dataset(df)

    # ------------------------------------------------------
    # Step 4: Assess Data Quality
    # ------------------------------------------------------

    quality_report = assess_data_quality(df)

    # ------------------------------------------------------
    # Step 5: Dataset Summary
    # ------------------------------------------------------

    st.subheader("📋 Dataset Summary")

    summary = profile["summary"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", summary["rows"])
        st.metric("Numeric Columns", summary["numeric_columns"])

    with col2:
        st.metric("Columns", summary["columns"])
        st.metric("Categorical Columns", summary["categorical_columns"])

    with col3:
        st.metric("Missing Values", summary["missing_values"])
        st.metric("Memory Usage (MB)", summary["memory_usage"])

    # ------------------------------------------------------
    # Step 6: Data Quality
    # ------------------------------------------------------

    st.subheader("🛡 Data Quality")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Quality Score",
            f"{quality_report['score']} / 100"
        )

    with col2:

        grade = quality_report["grade"]

        if grade == "Excellent":
            st.success("🟢 Excellent")

        elif grade == "Good":
            st.info("🔵 Good")

        elif grade == "Fair":
            st.warning("🟡 Fair")

        else:
            st.error("🔴 Poor")

    if quality_report["issues"]:

        st.subheader("⚠ Quality Issues")

        for issue in quality_report["issues"]:

            if issue["severity"] == "warning":
                st.warning(issue["message"])

            else:
                st.error(issue["message"])

    else:
        st.success("✅ No data quality issues detected.")

    # ------------------------------------------------------
    # Step 7: Charts
    # ------------------------------------------------------

    st.subheader("📊 Histogram")

    numeric_columns = (
        df.select_dtypes(include="number")
        .columns
    )

    if len(numeric_columns) == 0:

        st.info(
            "No numeric columns available for visualization."
        )

    else:

        selected_column = st.selectbox(
            "Select a numeric column",
            numeric_columns
        )

        histogram = create_histogram(
            df,
            selected_column
        )

        boxplot = create_boxplot(
            df,
            selected_column
        )

        st.pyplot(histogram)

        st.pyplot(boxplot)

    # ------------------------------------------------------
    # Step 7: Schema
    # ------------------------------------------------------

    st.subheader("📑 Schema")

    st.dataframe(
        profile["schema"],
        use_container_width=True
    )

    # ------------------------------------------------------
    # Step 8: Preview
    # ------------------------------------------------------

    st.subheader("👀 Dataset Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )
