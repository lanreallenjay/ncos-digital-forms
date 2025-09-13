import streamlit as st
import pandas as pd

st.set_page_config(page_title="NCoS Forms Catalogue", layout="wide")

st.title("📘 Nigerian Correctional Service - Forms & Books Catalogue")

# Load the CSV
try:
    df = pd.read_csv("forms_catalogue.csv")
except FileNotFoundError:
    st.error("forms_catalogue.csv not found in the project directory.")
    st.stop()

# Search bar
search_term = st.text_input("Search by Title or Number", "").lower()

# Filter results
filtered_df = df[df.apply(lambda row:
    search_term in str(row["Title"]).lower() or
    search_term in str(row["Number"]).lower(), axis=1)]

# Display table
st.dataframe(filtered_df, use_container_width=True)
