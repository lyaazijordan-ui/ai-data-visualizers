# app/ai_engine.py
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def generate_chart(df, chart_type, x_col, y_col):
    """
    Generate and display a chart (line, bar, scatter) using matplotlib/seaborn.
    """
    plt.figure(figsize=(8,5))
    
    if chart_type == "Line":
        sns.lineplot(data=df, x=x_col, y=y_col)
    elif chart_type == "Bar":
        sns.barplot(data=df, x=x_col, y=y_col)
    elif chart_type == "Scatter":
        sns.scatterplot(data=df, x=x_col, y=y_col)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)