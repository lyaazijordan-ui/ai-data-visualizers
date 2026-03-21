import streamlit as st
from db import save_user, load_user

def signup(username, password):
    existing = load_user(username)
    if existing:
        st.error("Username already exists!")
        return False
    save_user(username, password)
    st.success("Account created!")
    return True

def login(username, password):
    user = load_user(username)
    if user and user[1] == password:
        st.session_state["username"] = username
        st.session_state["theme"] = user[2]
        st.session_state["chart_color"] = user[3]
        return True
    st.error("Login failed!")
    return False
