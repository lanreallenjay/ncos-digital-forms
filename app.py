import streamlit as st
import pandas as pd

st.set_page_config(page_title="NCoS Digital Forms", layout="centered")

st.title("📘 Nigerian Correctional Service - Admission Register")

st.write("Fill this form to admit a new inmate.")

with st.form("admission_form"):
    name = st.text_input("Inmate Full Name")
    crime = st.text_input("Offence Committed")
    date_admitted = st.date_input("Date of Admission")
    officer = st.text_input("Admitting Officer's Name")

    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {
            "Name": name,
            "Offence": crime,
            "Date Admitted": date_admitted,
            "Admitting Officer": officer
        }
        df = pd.DataFrame([data])
        df.to_excel("admission_register.xlsx", index=False)
        st.success("Admission registered and saved successfully!")
