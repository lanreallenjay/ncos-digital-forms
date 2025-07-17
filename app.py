import streamlit as st
import pandas as pd
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="NCoS Forms Catalogue", layout="wide")
st.title("📘 Nigerian Correctional Service - Forms & Books Catalogue")

# Load the CSV
csv_file = "forms_catalogue.csv"
if not os.path.exists(csv_file):
    st.error("❌ forms_catalogue.csv not found in the directory.")
    st.stop()

df = pd.read_csv(csv_file)

# --- Browse Catalogue ---
st.subheader("📂 Browse Catalogue")
search_term = st.text_input("Search by Title or Number", "").lower()

filtered_df = df[df.apply(lambda row:
    search_term in str(row["Title"]).lower() or
    search_term in str(row["Number"]).lower(), axis=1)]

# --- Display each form entry as a clickable expander ---
for index, row in filtered_df.iterrows():
    with st.expander(f"{row['Number']}: {row['Title']}"):
        if pd.notna(row['Description']) and row['Description'].strip():
            st.markdown(row['Description'])
        else:
            if st.button("✨ Generate AI Description", key=f"gen_{index}"):
                try:
                    prompt = f"Write a clear and concise description of this Nigerian Correctional Service form or book: '{row['Title']}'"
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    ai_description = response["choices"][0]["message"]["content"]
                    df.at[index, "Description"] = ai_description
                    df.to_csv(csv_file, index=False)
                    st.success("✅ AI-generated description saved.")
                    st.markdown(ai_description)
                except Exception as e:
                    st.error(f"❌ Error during AI generation: {e}")
