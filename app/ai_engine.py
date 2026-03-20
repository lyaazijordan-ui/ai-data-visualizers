import streamlit as st
import plotly.express as px

def generate_chart(df, chart_type, x, y):
    if chart_type == "Line":
        fig = px.line(df, x=x, y=y)
    elif chart_type == "Bar":
        fig = px.bar(df, x=x, y=y)
    else:
        fig = px.scatter(df, x=x, y=y)

    st.plotly_chart(fig)


def generate_insights(df):
    insights = []

    # Basic dataset info
    insights.append(f"📊 Dataset has {df.shape[0]} rows and {df.shape[1]} columns.")

    # Column types
    insights.append("\n🧾 Columns:")
    for col in df.columns:
        insights.append(f"- {col} ({df[col].dtype})")

    # Numeric analysis
    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) > 0:
        insights.append("\n📈 Numeric Insights:")
        for col in numeric_cols:
            insights.append(
                f"{col}: mean={df[col].mean():.2f}, max={df[col].max()}, min={df[col].min()}"
            )

    # Missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        insights.append("\n⚠️ Missing Values:")
        for col in missing.index:
            if missing[col] > 0:
                insights.append(f"{col}: {missing[col]} missing")

    return "\n".join(insights)
