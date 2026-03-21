# main.py# app/main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add current folder to path
from app.auth import login, signup, load_user_settings, save_user_settings
from app.db import save_data, load_data
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
import time

st.set_page_config(page_title="AI Data Dashboard", layout="wide", initial_sidebar_state="expanded")

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    st.markdown("<h2 style='text-align:center'>🌐 AI Dashboard</h2>", unsafe_allow_html=True)
    page = st.radio("Go to", ["Home", "Upload & Visualize", "Reports", "Settings", "Logout"])

# -----------------------------
# Home / Login & Signup
# -----------------------------
if page == "Home":
    st.markdown("<h1 style='text-align:center;color:#4B0082'>Welcome to AI Data Dashboard</h1>", unsafe_allow_html=True)
    choice = st.radio("Choose action", ["Login", "Sign Up"])
    username = st.text_input("Username", max_chars=20)
    password = st.text_input("Password", type="password", max_chars=50)

    if choice == "Login" and st.button("Login"):
        if login(username, password):
            st.session_state.update(load_user_settings(username))
            st.success(f"Welcome back, {username}!")
            st.stop()
        else:
            st.error("Login failed. Check username/password.")

    elif choice == "Sign Up" and st.button("Sign Up"):
        if signup(username, password):
            st.success("Sign up successful! Please log in.")
            st.stop()

# -----------------------------
# Logout
# -----------------------------
elif page == "Logout":
    if "username" in st.session_state:
        st.session_state.clear()
        st.success("Logged out")
    else:
        st.info("You are not logged in")

# -----------------------------
# Upload & Visualize
# -----------------------------
elif page == "Upload & Visualize":
    if "username" not in st.session_state:
        st.warning("Please log in first for full features")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state["current_df"] = df
    else:
        df = st.session_state.get("current_df")

    if df is not None:
        st.markdown("### 📋 Dataset Preview")
        st.dataframe(df.head(), height=250)

        st.markdown("### 📊 Dataset Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Mean Y", round(df.select_dtypes(include=np.number).mean().mean(),2))
        col4.metric("Max Y", round(df.select_dtypes(include=np.number).max().max(),2))

        st.markdown("---")
        st.subheader("Interactive Chart")
        chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])
        x_col = st.selectbox("X-axis", df.columns)
        y_col = st.selectbox("Y-axis", df.columns)
        color_col = st.selectbox("Color column (optional)", [None]+list(df.columns))
        template_theme = st.session_state.get("theme","plotly_dark")
        color_args = {"color": color_col} if color_col else {}

        steps = 30
        for i in range(steps):
            subset = df.sample(frac=min(1,(i+1)/steps))
            if chart_type=="Line":
                fig = px.line(subset, x=x_col, y=y_col, **color_args, template=template_theme)
            elif chart_type=="Bar":
                fig = px.bar(subset, x=x_col, y=y_col, **color_args, template=template_theme)
            else:
                fig = px.scatter(subset, x=x_col, y=y_col, **color_args, template=template_theme)

            fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers+lines'))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            time.sleep(0.03)

        st.download_button("Download Chart HTML", fig.to_html(), file_name="chart.html", mime="text/html")

# -----------------------------
# Reports
# -----------------------------
elif page == "Reports":
    if "username" not in st.session_state:
        st.warning("Please log in first")
    else:
        df = st.session_state.get("current_df")
        if df is not None:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()
            elements = [Paragraph("User Data Report", styles['Title'])]
            data_table = [df.columns.tolist()] + df.values.tolist()
            elements.append(Table(data_table))
            doc.build(elements)
            buffer.seek(0)
            st.download_button("Download PDF Report", buffer, file_name="report.pdf")
        else:
            st.info("No data available")

# -----------------------------
# Settings
# -----------------------------
elif page == "Settings":
    if "username" not in st.session_state:
        st.warning("Please log in first")
    else:
        st.subheader("User Settings")
        theme = st.selectbox("Theme", ["plotly_dark", "plotly_white"], index=0)
        chart_color = st.text_input("Default Chart Gradient", st.session_state.get("chart_color", "Agsunset"))
        username = st.text_input("Username", st.session_state.get("username"))
        if st.button("Save Settings"):
            st.session_state["theme"] = theme
            st.session_state["chart_color"] = chart_color
            st.session_state["username"] = username
            save_user_settings(username, theme, chart_color)
            st.success("Settings saved!")
