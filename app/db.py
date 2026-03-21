import pandas as pd
import requests
import json
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

TABLE_NAME = "user_data"

def save_data(user_email, df: pd.DataFrame):
    records = df.to_dict(orient="records")
    payload = [{"user": user_email, "data": json.dumps(records)}]
    response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}", headers=HEADERS, json=payload)
    if response.status_code in [200, 201]:
        return True
    else:
        st.error(f"Save failed: {response.text}")
        return False

def load_data(user_email):
    params = {"user": f"eq.{user_email}"}
    response = requests.get(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}", headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            records = json.loads(data[0]["data"])
            df = pd.DataFrame(records)
            return df
    return None
