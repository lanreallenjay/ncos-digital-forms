import os
import json
import time
import pandas as pd
import streamlit as st
import requests

# =========================
# Page Setup
# =========================
st.set_page_config(page_title="NCoS Forms Catalogue", layout="wide")
st.title("📘 Nigerian Correctional Service - Forms & Books Catalogue")

CSV_FILE = "forms_catalogue.csv"

# =========================
# Session State
# =========================
if "ai_cache" not in st.session_state:
    st.session_state.ai_cache = {}  # {(number,title): generated_text}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# Helpers: Data I/O
# =========================
def load_catalogue(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        st.error(f"❌ `{csv_path}` not found. Please upload it to the project root.")
        st.stop()
    df = pd.read_csv(csv_path, dtype=str).fillna("")
    for col in ["Number", "Title", "Description"]:
        if col not in df.columns:
            df[col] = ""
    if "Corrected" not in df.columns:
        df["Corrected"] = ""
    return df

def save_catalogue(df: pd.DataFrame, csv_path: str = CSV_FILE):
    cols = ["Number", "Title", "Description", "Corrected"]
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    df[cols].to_csv(csv_path, index=False)

df = load_catalogue(CSV_FILE)

# =========================
# Sidebar: Admin & AI Provider
# =========================
with st.sidebar:
    st.subheader("🔐 Admin")
    if not st.session_state.logged_in:
        pwd = st.text_input("Admin password", type="password", placeholder="Enter password")
        if st.button("Login"):
            admin_password = st.secrets.get("ADMIN_PASSWORD", "ncosadmin123")
            if pwd == admin_password:
                st.session_state.logged_in = True
                st.success("✅ Logged in as Admin")
                st.rerun()
            else:
                st.error("❌ Incorrect password")
    else:
        st.success("You are logged in ✅")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    st.divider()
    st.subheader("⚙️ AI Provider")
    provider = st.radio(
        "Choose AI Provider",
        ["OpenRouter (free)", "OpenAI (paid)"],
        index=0  # default to OpenRouter
    )

# =========================
# AI Description (Provider-Aware)
# =========================
def generate_ai_description(title: str, number: str) -> str:
    prompt = (
        "You are helping catalogue official administrative forms used by the "
        "Nigerian Correctional Service (NCoS).\n"
        f"Form Number: {number}\n"
        f"Title: {title}\n\n"
        "Write a clear, neutral, 2–4 sentence description covering:\n"
        "• What the form/book is for\n"
        "• Who typically uses it\n"
        "• When or how often it is used\n"
        "Avoid sensitive data or legal advice. Keep it concise and practical."
    )

    if provider == "OpenRouter (free)":
        openrouter_key = st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        if openrouter_key:
            try:
                url = "https://openrouter.ai/api/v1/chat/completions"
                model = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
                headers = {"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant for cataloguing forms."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                }
                resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    return text if text else "❌ AI returned an empty response."
                else:
                    return f"❌ OpenRouter error: {resp.status_code} – {resp.text}"
            except Exception as e:
                return f"❌ OpenRouter exception: {e}"
        else:
            return "❌ OpenRouter API key not set."

    elif provider == "OpenAI (paid)":
        openai_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                url = "https://api.openai.com/v1/chat/completions"
                model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
                headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant for cataloguing forms."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                }
                resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    text = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    return text if text else "❌ AI returned an empty response."
                else:
                    return f"❌ OpenAI error: {resp.status_code} – {resp.text}"
            except Exception as e:
                return f"❌ OpenAI exception: {e}"
        else:
            return "❌ OpenAI API key not set."

    return "❌ No AI provider configured."

# =========================
# Browse & Generate Section
# =========================
st.subheader("📂 Browse Catalogue")
search_term = st.text_input("Search by Title or Number", "").strip().lower()

if search_term:
    filtered = df[df.apply(lambda r: search_term in r["Title"].lower() or search_term in r["Number"].lower(), axis=1)].reset_index(drop=True)
else:
    filtered = df.reset_index(drop=True)

for idx, row in filtered.iterrows():
    number, title, desc = row["Number"], row["Title"], row.get("Description", "")
    key_base = f"{number}_{title}".replace(" ", "_")

    cols = st.columns([2, 7, 3])
    with cols[0]:
        st.markdown(f"**{number}**")
    with cols[1]:
        st.markdown(title)

    with cols[2]:
        if st.button("🧠 Get Description", key=f"gen_{key_base}"):
            cache_key = (number, title)
            if cache_key in st.session_state.ai_cache:
                ai_text = st.session_state.ai_cache[cache_key]
            else:
                with st.spinner("Generating description..."):
                    ai_text = generate_ai_description(title, number)
                    st.session_state.ai_cache[cache_key] = ai_text
            st.session_state[f"show_{key_base}"] = True
            st.session_state[f"ai_text_{key_base}"] = ai_text

    show_block = st.session_state.get(f"show_{key_base}", False)
    if show_block or desc:
        with st.expander(f"Details for {number} — {title}", expanded=show_block):
            ai_text = st.session_state.get(f"ai_text_{key_base}", "").strip()
            display_text = ai_text if ai_text and not ai_text.startswith("❌") else desc

            if st.session_state.logged_in:
                edited_number = st.text_input("Form Number", value=number, key=f"num_{key_base}")
                edited_title = st.text_input("Title", value=title, key=f"title_{key_base}")
                edited_desc = st.text_area("Description", value=display_text, height=140, key=f"desc_{key_base}")

                c1, c2, c3 = st.columns([1.2, 1, 1])
                with c1:
                    if st.button("💾 Save", key=f"save_{key_base}"):
                        df.loc[(df["Number"] == number) & (df["Title"] == title), ["Number", "Title", "Description"]] = [edited_number, edited_title, edited_desc]
                        df.loc[(df["Number"] == edited_number) & (df["Title"] == edited_title), "Corrected"] = "True"
                        save_catalogue(df, CSV_FILE)
                        st.success("Saved successfully.")
                        st.session_state.ai_cache.pop((number, title), None)
                        st.session_state[f"ai_text_{key_base}"] = edited_desc
                        time.sleep(0.2)
                        st.rerun()
                with c2:
                    if st.button("↩️ Revert to Saved", key=f"revert_{key_base}"):
                        fresh = load_catalogue(CSV_FILE)
                        saved_val = fresh[(fresh["Number"] == number) & (fresh["Title"] == title)][["Number","Title","Description"]]
                        if not saved_val.empty:
                            st.session_state[f"ai_text_{key_base}"] = saved_val["Description"].iloc[0]
                        st.info("Reverted to last saved description.")
                        time.sleep(0.2)
                        st.rerun()
                with c3:
                    if st.button("🗑️ Delete Entry", key=f"del_{key_base}"):
                        st.session_state[f"confirm_del_{key_base}"] = True
                    if st.session_state.get(f"confirm_del_{key_base}", False):
                        st.warning("Are you sure? This will remove the entry permanently.")
                        cc1, cc2 = st.columns(2)
                        with cc1:
                            if st.button("Yes, delete", key=f"yes_del_{key_base}"):
                                df_drop = df[~((df["Number"] == number) & (df["Title"] == title))].copy()
                                save_catalogue(df_drop, CSV_FILE)
                                st.success("Entry deleted.")
                                time.sleep(0.2)
                                st.rerun()
                        with cc2:
                            if st.button("Cancel", key=f"cancel_del_{key_base}"):
                                st.session_state[f"confirm_del_{key_base}"] = False
                                st.rerun()
            else:
                if display_text:
                    st.write(display_text)
                elif ai_text and ai_text.startswith("❌"):
                    st.error(ai_text)
                else:
                    st.info("Click **🧠 Get Description** to generate an overview with AI.")

st.divider()

# =========================
# Admin: Add New Entry
# =========================
if st.session_state.logged_in:
    st.subheader("🛠️ Manage Catalogue (Admin)")
    with st.form("add_entry_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 5])
        with c1:
            new_number = st.text_input("Form Number (e.g., 21A)").strip()
        with c2:
            new_title = st.text_input("Title").strip()
        new_description = st.text_area("Description (optional)", height=120)
        submitted = st.form_submit_button("➕ Add Entry")
        if submitted:
            if not new_number or not new_title:
                st.error("Number and Title are required.")
            else:
                exists = df[(df["Number"] == new_number) & (df["Title"] == new_title)]
                if len(exists) > 0:
                    st.warning("An entry with the same Number and Title already exists.")
                else:
                    new_row = {
                        "Number": new_number,
                        "Title": new_title,
                        "Description": new_description,
                        "Corrected": "True" if new_description else "",
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    save_catalogue(df, CSV_FILE)
                    st.success("New entry added.")
                    time.sleep(0.2)
                    st.rerun()

# =========================
# Utilities
# =========================
st.download_button(
    "⬇️ Download Current Catalogue (CSV)",
    data=df.to_csv(index=False),
    file_name="forms_catalogue.csv",
    mime="text/csv",
)
