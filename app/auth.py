import streamlit as st
import requests
import json

# ========================
# SUPABASE CONFIG
# ========================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

AUTH_URL = f"{SUPABASE_URL}/auth/v1"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json"
}

# ========================
# LOGIN FUNCTION
# ========================
def login(email: str, password: str) -> bool:
    if not email or not password:
        st.warning("Enter both email and password")
        return False
    payload = json.dumps({"email": email, "password": password})
    try:
        response = requests.post(f"{AUTH_URL}/token", headers=HEADERS, data=payload)
        data = response.json()
        if response.status_code == 200 and "access_token" in data:
            st.session_state["user"] = email
            st.session_state["access_token"] = data["access_token"]
            return True
        else:
            st.error(data.get("error_description") or data.get("error") or "Login failed")
            return False
    except Exception as e:
        st.error(f"Login error: {e}")
        return False

# ========================
# LOGOUT FUNCTION
# ========================
def logout():
    for key in ["user", "access_token", "authenticated"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Logged out successfully")
