# app/main.py
import streamlit as st
from auth import login, logout
from data_engine import load_data
from ai_engine import generate_chart
from report import generate_pdf

st.set_page_config(page_title="AI Data Visualizer", layout="wide")

# --- LOGIN ---
if not login():
    st.stop()  # Stop here if user not logged in

st.sidebar.title("Menu")
menu = st.sidebar.radio("Select Option", ["Upload CSV", "Generate Charts", "Generate PDF", "Logout"])

# --- LOGOUT ---
if menu == "Logout":
    logout()

# --- UPLOAD CSV ---
if menu == "Upload CSV":
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            st.dataframe(df)

# --- CHARTS ---
if menu == "Generate Charts":
    if "logged_in" in st.session_state and st.session_state.logged_in:
        uploaded_file = st.file_uploader("Choose a CSV file first", type="csv", key="chart_upload")
        if uploaded_file:
            df = load_data(uploaded_file)
            if df is not None:
                st.subheader("AI Chart Generator")
                x_col = st.selectbox("X-axis", df.columns)
                y_col = st.selectbox("Y-axis", df.columns)
                chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])
                if st.button("Generate Chart"):
                    generate_chart(df, chart_type, x_col, y_col)

# --- PDF REPORT ---
if menu == "Generate PDF":
    if "logged_in" in st.session_state and st.session_state.logged_in:
        uploaded_file = st.file_uploader("Choose a CSV file first", type="csv", key="pdf_upload")
        if uploaded_file:
            df = load_data(uploaded_file)
            if df is not None:
                st.subheader("Generate PDF Report")
                generate_pdf(df)