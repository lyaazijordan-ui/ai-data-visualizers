import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
from auth import login, logout
from db import save_data, load_data

st.set_page_config(page_title="AI Data Lab", layout="wide")

# ========================
# SIDEBAR NAVIGATION
# ========================
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

st.sidebar.title("AI Data Lab")
page = st.sidebar.radio("Navigate", ["Login", "Upload & Visualize", "Reports", "Logout"])

# ========================
# LOGIN PAGE
# ========================
if page == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(email, password):
            st.session_state["authenticated"] = True
            st.success("Logged in!")
            st.experimental_rerun()

# ========================
# LOGOUT PAGE
# ========================
elif page == "Logout":
    if st.session_state.get("authenticated"):
        logout()
        st.session_state["authenticated"] = False
        st.experimental_rerun()
    else:
        st.info("You are not logged in")

# ========================
# UPLOAD & VISUALIZE
# ========================
elif page == "Upload & Visualize":
    if not st.session_state.get("authenticated"):
        st.warning("Login first!")
    else:
        st.subheader("Upload CSV")
        uploaded_file = st.file_uploader("Choose CSV", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            save_data(st.session_state["user"], df)

            st.subheader("Select chart type")
            chart_type = st.selectbox("Chart type", ["Line", "Bar", "Scatter"])
            color_col = st.selectbox("Color column", df.columns)
            x_col = st.selectbox("X-axis", df.columns)
            y_col = st.selectbox("Y-axis", df.columns)

            if st.button("Generate Chart"):
                fig = None
                if chart_type == "Line":
                    fig = px.line(df, x=x_col, y=y_col, color=color_col,
                                  color_continuous_scale=px.colors.sequential.Agsunset,
                                  template="plotly_dark")
                elif chart_type == "Bar":
                    fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                                 color_discrete_sequence=px.colors.sequential.Agsunset,
                                 template="plotly_dark")
                elif chart_type == "Scatter":
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                     color_continuous_scale=px.colors.sequential.Agsunset,
                                     template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

                # Download chart as PNG
                buf = BytesIO()
                fig.write_image(buf, format="png")
                st.download_button("Download Chart PNG", buf, file_name="chart.png", mime="image/png")

# ========================
# REPORT PAGE
# ========================
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
