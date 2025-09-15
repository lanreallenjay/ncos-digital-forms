import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Must call set_page_config before other Streamlit calls that produce output
st.set_page_config(page_title="NCoS Forms Catalogue", layout="wide")
st.title("📘 Nigerian Correctional Service - Forms & Books Catalogue")

# Load local .env (for local development)
load_dotenv()

# Prefer Streamlit secrets, fallback to local environment
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("No OPENAI_API_KEY found. Add it to Streamlit secrets (recommended) or local .env.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

csv_file = "forms_catalogue.csv"

# Load CSV
if not os.path.exists(csv_file):
    st.error("❌ forms_catalogue.csv not found in the directory.")
    st.stop()

df = pd.read_csv(csv_file)

# Search
search_term = st.text_input("🔍 Search by Title or Number", "").lower()

filtered_df = df[df.apply(lambda row:
    search_term in str(row["Title"]).lower() or
    search_term in str(row["Number"]).lower(), axis=1)]

# Table
st.subheader("📋 Forms & Books List")

for _, row in filtered_df.iterrows():
    st.markdown(f"### {row['Number']}. {row['Title']}")
    with st.expander("🔎 Click to View or Generate Description", expanded=False):
        current_description = row["Description"]
        st.markdown(f"**Current Description:** {current_description if pd.notna(current_description) and current_description.strip() else '*No description yet.*'}")

        if st.button(f"✨ Generate Description for '{row['Title']}'", key=row['Number']):
            try:
                prompt = f"Provide a professional, one-sentence description of the correctional form titled: '{row['Title']}'"
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                generated = response.choices[0].message.content.strip()
                df.loc[df["Title"] == row["Title"], "Description"] = generated
                df.to_csv(csv_file, index=False)
                st.success("✅ Description generated and saved!")
                st.markdown(f"**New Description:** {generated}")
            except Exception as e:
                st.error(f"❌ Error during AI generation: {e}")
