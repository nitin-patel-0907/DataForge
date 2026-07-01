import streamlit as st
from src.data_processing.loader import load_dataset, get_dataset_info

st.title("DataForge")
st.caption("Upload a CSV file to preview its structure and metadata.")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = load_dataset(uploaded_file)
    info = get_dataset_info(df)
    
    st.subheader("Dataset Information")

    st.write(f"**Rows:** {info['shape'][0]}")
    st.write(f"**Columns:** {info['shape'][1]}")

    st.subheader("Schema")
    st.dataframe(info["schema"], use_container_width=True)

    st.subheader("Preview")
    st.dataframe(df.head())