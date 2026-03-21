import streamlit as st

def login():
    if "user" not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        st.title("🔐 AI Data Lab Login")
        email = st.text_input("Email")

        if st.button("Login"):
            if email:
                st.session_state.user = email
                st.success("Logged in")

        return False
    return True


def logout():
    st.session_state.user = None
