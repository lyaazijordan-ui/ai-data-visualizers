from supabase import create_client
import streamlit as st
import json

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

def save_data(email, df):
    data_json = df.to_json()

    supabase.table("user_data").upsert({
        "email": email,
        "data": data_json
    }).execute()


def load_data(email):
    response = supabase.table("user_data").select("*").eq("email", email).execute()

    if response.data:
        import pandas as pd
        return pd.read_json(response.data[0]["data"])
    return None
