[1mdiff --git a/app.py b/app.py[m
[1mindex 3320ce8..eadcb69 100644[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@ -1,27 +1,24 @@[m
 import streamlit as st[m
 import pandas as pd[m
 [m
[31m-st.set_page_config(page_title="NCoS Digital Forms", layout="centered")[m
[32m+[m[32mst.set_page_config(page_title="NCoS Forms Catalogue", layout="wide")[m
 [m
[31m-st.title("📘 Nigerian Correctional Service - Admission Register")[m
[32m+[m[32mst.title("📘 Nigerian Correctional Service - Forms & Books Catalogue")[m
 [m
[31m-st.write("Fill this form to admit a new inmate.")[m
[32m+[m[32m# Load the CSV[m
[32m+[m[32mtry:[m
[32m+[m[32m    df = pd.read_csv("forms_catalogue.csv")[m
[32m+[m[32mexcept FileNotFoundError:[m
[32m+[m[32m    st.error("forms_catalogue.csv not found in the project directory.")[m
[32m+[m[32m    st.stop()[m
 [m
[31m-with st.form("admission_form"):[m
[31m-    name = st.text_input("Inmate Full Name")[m
[31m-    crime = st.text_input("Offence Committed")[m
[31m-    date_admitted = st.date_input("Date of Admission")[m
[31m-    officer = st.text_input("Admitting Officer's Name")[m
[32m+[m[32m# Search bar[m
[32m+[m[32msearch_term = st.text_input("Search by Title or Number", "").lower()[m
 [m
[31m-    submitted = st.form_submit_button("Submit")[m
[32m+[m[32m# Filter results[m
[32m+[m[32mfiltered_df = df[df.apply(lambda row:[m
[32m+[m[32m    search_term in str(row["Title"]).lower() or[m
[32m+[m[32m    search_term in str(row["Number"]).lower(), axis=1)][m
 [m
[31m-    if submitted:[m
[31m-        data = {[m
[31m-            "Name": name,[m
[31m-            "Offence": crime,[m
[31m-            "Date Admitted": date_admitted,[m
[31m-            "Admitting Officer": officer[m
[31m-        }[m
[31m-        df = pd.DataFrame([data])[m
[31m-        df.to_excel("admission_register.xlsx", index=False)[m
[31m-        st.success("Admission registered and saved successfully!")[m
[32m+[m[32m# Display table[m
[32m+[m[32mst.dataframe(filtered_df, use_container_width=True)[m
