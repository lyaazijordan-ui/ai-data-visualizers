import streamlit as st
import plotly.express as px
import os
from openai import OpenAI

# API key handling (local + cloud)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]
)


def generate_chart(df, chart_type, x, y):
    if chart_type == "Line":
        fig = px.line(df, x=x, y=y)
    elif chart_type == "Bar":
        fig = px.bar(df, x=x, y=y)
    else:
        fig = px.scatter(df, x=x, y=y)

    st.plotly_chart(fig)


def generate_insights(df):
    sample = df.head().to_string()

    prompt = f"""
    Analyze this dataset:
    {sample}

    Provide:
    - Key trends
    - Patterns
    - Insights
    - Recommendations
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
