import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
from auth import login, logout
from db import save_data, load_data

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="AI Data Lab",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Theme toggle
# -------------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

theme_option = st.sidebar.selectbox("Theme", ["Dark", "Light"])
st.session_state["theme"] = "plotly_dark" if theme_option == "Dark" else "plotly_white"

# -------------------------
# Sidebar navigation
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

st.sidebar.title("🚀 AI Data Lab")
page = st.sidebar.radio("Navigate", ["Login", "Upload & Visualize", "Reports", "Logout"])

# -------------------------
# LOGIN PAGE
# -------------------------
if page == "Login":
    st.markdown("<h1 style='text-align:center'>Welcome to AI Data Lab</h1>", unsafe_allow_html=True)
    st.subheader("Login")
    email = st.text_input("Email", placeholder="Enter your email", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
    if st.button("Login", use_container_width=True):
        if login(email, password):
            st.session_state["authenticated"] = True
            st.success("Logged in successfully! 🚀")
            st.experimental_rerun()

# -------------------------
# LOGOUT PAGE
# -------------------------
elif page == "Logout":
    if st.session_state.get("authenticated"):
        logout()
        st.session_state["authenticated"] = False
        st.experimental_rerun()
    else:
        st.info("You are not logged in")

# -------------------------
# UPLOAD & VISUALIZE
# -------------------------
elif page == "Upload & Visualize":
    if not st.session_state.get("authenticated"):
        st.warning("Login first!")
    else:
        st.markdown("## Upload CSV and generate charts")
        uploaded_file = st.file_uploader("Choose CSV", type="csv", label_visibility="collapsed")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())

            save_data(st.session_state["user"], df)

            # Chart options
            st.subheader("Chart Settings")
            chart_type = st.selectbox("Chart type", ["Line", "Bar", "Scatter"])
            x_col = st.selectbox("X-axis", df.columns)
            y_col = st.selectbox("Y-axis", df.columns)
            color_col = st.selectbox("Color column (optional)", [None]+list(df.columns))

            # Chart generation
            st.subheader("Generated Chart")
            fig = None
            color_args = {"color": color_col} if color_col else {}
            gradient = px.colors.sequential.Agsunset

            if chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, **color_args, template=st.session_state["theme"])
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, **color_args, template=st.session_state["theme"])
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, **color_args, template=st.session_state["theme"])

            fig.update_traces(marker=dict(colorscale=gradient, showscale=True), selector=dict(mode="markers+lines"))

            # Animated update effect
            st.plotly_chart(fig, use_container_width=True, theme="streamlit", config={"displayModeBar": True})

            # Downloads
            # HTML always works
            st.download_button("Download Interactive Chart (HTML)", fig.to_html(), file_name="chart.html", mime="text/html")
            # PNG fallback
            try:
                buf = BytesIO()
                fig.write_image(buf, format="png")
                st.download_button("Download Chart PNG", buf, file_name="chart.png", mime="image/png")
            except:
                st.info("PNG download not available in cloud; use HTML download")

# -------------------------
# REPORT PAGE
# -------------------------
elif page == "Reports":
    if not st.session_state.get("authenticated"):
        st.warning("Login first!")
    else:
        df = load_data(st.session_state["user"])
        if df is not None:
            st.subheader("Download PDF Report")
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()
            elements = [Paragraph("User Data Report", styles['Title'])]
            data_table = [df.columns.tolist()] + df.values.tolist()
            elements.append(Table(data_table))
            doc.build(elements)
            buffer.seek(0)
            st.download_button("Download PDF", buffer, file_name="report.pdf")
        else:
            st.info("No data uploaded yet")
