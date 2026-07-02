import streamlit as st

# ==========================================================
# Import reusable business logic
# ==========================================================

from src.data_processing.loader import (
    load_dataset
)

from src.data_processing.validator import (
    validate_dataset,
)

from src.data_processing.profiler import profile_dataset

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

    # Fatal validation errors
    if not validation_result["valid"]:
        st.error(validation_result["message"])
        st.stop()

    # Non-fatal validation warnings
    for warning in validation_result["warnings"]:
        st.warning(warning)

    # ------------------------------------------------------
    # Step 3: Dataset Information
    # ------------------------------------------------------

    profile = profile_dataset(df)

    # ------------------------------------------------------
    # Step 3: Dataset Summary
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
    # Step 4: Schema
    # ------------------------------------------------------

    st.subheader("📑 Schema")

    st.dataframe(
        profile["schema"],
        use_container_width=True,
    )

    # ------------------------------------------------------
    # Step 5: Preview
    # ------------------------------------------------------

    st.subheader("👀 Preview")

    st.dataframe(
        df.head(),
        use_container_width=True,
    )
