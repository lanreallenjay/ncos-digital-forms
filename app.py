import streamlit as st
import pandas as pd
import os

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

st.dataframe(filtered_df, use_container_width=True)

# --- Admin Login ---
st.subheader("🔐 Admin Login Required to Edit Descriptions")

# Store login state in session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    password = st.text_input("Enter admin password", type="password")
    if st.button("Login"):
        if password == "ncosadmin123":
            st.session_state.logged_in = True
            st.success("✅ Login successful. You can now edit descriptions.")
        else:
            st.error("❌ Incorrect password. Access denied.")

# --- Description Editor (Visible only if logged in) ---
if st.session_state.logged_in:
    st.subheader("📝 Edit Form Description")

    selected_title = st.selectbox("Select a Form Title to Edit", df["Title"].unique())
    form_row = df[df["Title"] == selected_title].iloc[0]
    current_desc = form_row["Description"]
    form_number = form_row["Number"]

    new_description = st.text_area("Update Description", value=current_desc, height=150)

    if st.button("💾 Save Description"):
        df.loc[df["Title"] == selected_title, "Description"] = new_description
        df.to_csv(csv_file, index=False)
        st.success(f"Description for '{selected_title}' updated successfully!")
