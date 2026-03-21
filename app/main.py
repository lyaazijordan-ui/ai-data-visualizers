import streamlit as st
from auth import login, logout
from data_engine import load_csv
from ai_engine import generate_chart, generate_insights, ask_data
from report import generate_pdf
from db import save_data, load_data

# 🔥 APP CONFIG (IMPORTANT FOR MOBILE + WEB)
st.set_page_config(
    page_title="AI Data Lab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 CUSTOM UI (MOBILE + PREMIUM LOOK)
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
h1, h2, h3 {
    color: #38bdf8;
}
button {
    border-radius: 12px !important;
    padding: 0.5rem 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# 🔐 LOGIN
if not login():
    st.stop()

# 🧭 SIDEBAR
with st.sidebar:
    st.title("⚙️ AI Data Lab")
    if st.button("Logout"):
        logout()

# 🚀 HEADER
st.markdown("## 🚀 AI Data Lab PRO")
st.caption("Smart Data Analytics Platform")

# ☁️ LOAD DATA FROM SUPABASE
df = load_data(st.session_state.user)
if df is not None:
    st.session_state["df"] = df

# 📱 MOBILE FRIENDLY TABS
tabs = st.tabs(["📁 Data", "📊 Charts", "🤖 Insights", "📊 Dashboard", "📄 Reports"])

# =========================
# 📁 DATA TAB
# =========================
with tabs[0]:
    st.subheader("Upload Dataset")

    file = st.file_uploader("Upload CSV", type="csv")

    if file:
        df = load_csv(file)
        st.session_state["df"] = df

        st.success("Data Loaded")
        st.dataframe(df, use_container_width=True)

        if st.button("☁️ Save to Cloud"):
            save_data(st.session_state.user, df)
            st.success("Saved successfully!")

# =========================
# 📊 CHARTS TAB
# =========================
with tabs[1]:
    df = st.session_state.get("df")

    if df is not None:
        st.subheader("Generate Charts")

        col1, col2 = st.columns(2)

        with col1:
            x = st.selectbox("X-axis", df.columns)
            y = st.selectbox("Y-axis", df.columns)
            chart = st.selectbox(
                "Chart Type",
                ["Line","Bar","Scatter","Histogram","Box","Area","Pie"]
            )

        with col2:
            st.markdown("### Preview")
            if st.button("📊 Generate Chart"):
                fig = generate_chart(df, chart, x, y)
                st.plotly_chart(fig, use_container_width=True)

                # 📥 DOWNLOAD CHART
                st.download_button(
                    "📥 Download Chart (PNG)",
                    fig.to_image(format="png"),
                    file_name="chart.png"
                )
    else:
        st.warning("Upload data first")

# =========================
# 🤖 INSIGHTS TAB
# =========================
with tabs[2]:
    df = st.session_state.get("df")

    if df is not None:
        st.subheader("AI Insights")

        if st.button("🧠 Generate Insights"):
            insights = generate_insights(df)
            st.session_state["insights"] = insights

            st.text(insights)

        st.markdown("### Ask Your Data")
        question = st.text_input("Ask something about your data")

        if question:
            answer = ask_data(df, question)
            st.success(answer)
    else:
        st.warning("Upload data first")

# =========================
# 📊 DASHBOARD TAB
# =========================
with tabs[3]:
    df = st.session_state.get("df")

    if df is not None:
        st.subheader("Auto Dashboard")

        num = df.select_dtypes(include="number")

        if not num.empty:
            cols = st.columns(min(3, len(num.columns)))

            for i, col in enumerate(num.columns[:3]):
                cols[i].metric(col, round(num[col].mean(), 2))

            fig = generate_chart(df, "Line", df.columns[0], num.columns[0])
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Upload data first")

# =========================
# 📄 REPORT TAB
# =========================
with tabs[4]:
    df = st.session_state.get("df")
    insights = st.session_state.get("insights", "")

    if df is not None:
        st.subheader("Export Reports")

        generate_pdf(df, insights)

        # 📥 DOWNLOAD CSV
        st.download_button(
            "📥 Download Data (CSV)",
            df.to_csv(index=False),
            file_name="data.csv"
        )
    else:
        st.warning("Upload and analyze data first")
