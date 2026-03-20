import streamlit as st

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = None

    if not st.session_state.logged_in:
        st.title("🔐 Login")

        email = st.text_input("Enter your email")

        if st.button("Login"):
            if email:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Logged in successfully")

        return False
    return True


def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
