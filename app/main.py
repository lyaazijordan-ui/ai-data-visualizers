import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
from auth import login, signup
from db import save_csv, load_csv, save_user, load_user
import time

st.set_page_config(page_title="AI Data Dashboard", layout="wide", initial_sidebar_state="collapsed")

# -----------------------------
# Sidebar + Navigation
# -----------------------------
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {background-color: #1f2c56; color: white; padding: 20px;}
    .sidebar .sidebar-content h2 {font-size: 24px;}
    .sidebar .sidebar-content input, .sidebar .sidebar-content select {margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.title("🌐 AI Dashboard")
page = st.sidebar.radio("Navigation", ["Login / Signup", "Upload & Visualize", "Reports", "Settings", "Logout"])

# -----------------------------
# Login / Signup
# -----------------------------
if page == "Login / Signup":
    st.markdown("<h1 style='text-align:center'>Welcome to AI Data Dashboard</h1>", unsafe_allow_html=True)
    choice = st.radio("Choose action", ["Login", "Sign Up"])
    username = st.text_input("Username", max_chars=20)
    password = st.text_input("Password", type="password", max_chars=50)
    if choice == "Login":
        if st.button("Login"):
            if login(username, password):
                st.success(f"Logged in as {username}")
                st.experimental_rerun()
    else:
        if st.button("Sign Up"):
            if signup(username, password):
                st.experimental_rerun()

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
        if "username" in st.session_state:
            save_csv(st.session_state["username"], df)
    else:
        df = st.session_state.get("current_df")
        if "username" in st.session_state:
            df = df or load_csv(st.session_state["username"])

    if df is not None:
        st.dataframe(df.head(), height=250)

        # -----------------------------
        # Stats Cards
        # -----------------------------
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
        
        # -----------------------------
        # Real-time animation simulation
        # -----------------------------
        steps = 30  # number of animation frames
        for i in range(steps):
            subset = df.sample(frac=min(1,(i+1)/steps))
            if chart_type=="Line":
                fig = px.line(subset, x=x_col, y=y_col, **color_args, template=template_theme)
            elif chart_type=="Bar":
                fig = px.bar(subset, x=x_col, y=y_col, **color_args, template=template_theme)
            elif chart_type=="Scatter":
                fig = px.scatter(subset, x=x_col, y=y_col, **color_args, template=template_theme)
            fig.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers+lines'))
            st.plotly_chart(fig, use_container_width=True)
            time.sleep(0.05)  # smooth animated effect

        st.download_button("Download Chart HTML", fig.to_html(), file_name="chart.html", mime="text/html")

# -----------------------------
# Reports
# -----------------------------
elif page == "Reports":
    if "username" not in st.session_state:
        st.warning("Please log in first")
    else:
        df = st.session_state.get("current_df") or load_csv(st.session_state["username"])
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
            save_user(username, "", theme=theme, chart_color=chart_color)
            st.success("Settings saved!")
