# auth.py
import streamlit as st
from app.db import load_data, save_data

USERS_KEY = "users_data"

def signup(username, password):
    users = st.session_state.get(USERS_KEY, {})
    if username in users:
        return False
    users[username] = {"password": password, "settings": {"theme":"plotly_dark", "chart_color":"Agsunset"}}
    st.session_state[USERS_KEY] = users
    save_data(USERS_KEY, users)
    return True

def login(username, password):
    users = st.session_state.get(USERS_KEY, {})
    if username in users and users[username]["password"] == password:
        return True
    return False

def load_user_settings(username):
    users = st.session_state.get(USERS_KEY, {})
    if username in users:
        return users[username].get("settings", {})
    return {}

def save_user_settings(username, theme, chart_color):
    users = st.session_state.get(USERS_KEY, {})
    if username in users:
        users[username]["settings"] = {"theme": theme, "chart_color": chart_color}
        st.session_state[USERS_KEY] = users
        save_data(USERS_KEY, users)
