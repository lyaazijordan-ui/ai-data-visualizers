# app/auth.py
import streamlit as st

def login():
    """
    Simple login simulation for Streamlit >=1.55.
    No experimental_get_query_params or experimental_rerun used.
    """
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.user_name = None

    if not st.session_state.logged_in:
        st.warning("Simulated login. Click below to continue.")
        if st.button("Login"):
            st.session_state.logged_in = True
            st.session_state.user_email = "test@example.com"
            st.session_state.user_name = "Test User"
            # No rerun needed; Streamlit will automatically refresh widgets
        return False
    return True

def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_name = None