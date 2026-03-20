import streamlit as st
from auth import login, logout
from data_engine import load_data, save_user_data, load_user_data
from ai_engine import generate_chart, generate_insights
from report import generate_pdf

st.set_page_config(page_title="AI Data Visualizer", layout="wide")

# LOGIN
if not login():
    st.stop()

st.sidebar.title("Menu")

if st.sidebar.button("Logout"):
    logout()

st.title("🚀 AI Data Visualizer")

# LOAD SAVED DATA
saved_df = load_user_data(st.session_state.user_email)
if saved_df is not None:
    st.session_state["df"] = saved_df
    st.success("Loaded saved data")

# TABS
tab1, tab2, tab3, tab4 = st.tabs(
    ["📁 Data", "📊 Charts", "🤖 AI Insights", "📄 Report"]
)

# 📁 DATA TAB
with tab1:
    uploaded_file = st.file_uploader("Upload CSV", type="csv")

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            st.session_state["df"] = df
            st.dataframe(df)

            if st.button("Save Data"):
                save_user_data(st.session_state.user_email, df)
                st.success("Data saved!")

# 📊 CHART TAB
with tab2:
    df = st.session_state.get("df")

    if df is not None:
        col1, col2 = st.columns(2)

        with col1:
            x = st.selectbox("X-axis", df.columns)
            y = st.selectbox("Y-axis", df.columns)
            chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Scatter"])

        with col2:
            if st.button("Generate Chart"):
                generate_chart(df, chart_type, x, y)
    else:
        st.warning("Upload data first")

# 🤖 AI INSIGHTS TAB
with tab3:
    df = st.session_state.get("df")

    if df is not None:
        if st.button("Generate AI Insights"):
            insights = generate_insights(df)
            st.write(insights)
    else:
        st.warning("Upload data first")

# 📄 REPORT TAB
with tab4:
    df = st.session_state.get("df")

    if df is not None:
        generate_pdf(df)
    else:
        st.warning("Upload data first")
