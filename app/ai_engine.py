import plotly.express as px
import pandas as pd

def generate_chart(df, chart_type, x, y):
    template = "plotly_dark"

    if chart_type == "Line":
        return px.line(df, x=x, y=y, template=template)
    elif chart_type == "Bar":
        return px.bar(df, x=x, y=y, template=template)
    elif chart_type == "Scatter":
        return px.scatter(df, x=x, y=y, template=template)
    elif chart_type == "Histogram":
        return px.histogram(df, x=x, template=template)
    elif chart_type == "Box":
        return px.box(df, x=x, y=y, template=template)
    elif chart_type == "Area":
        return px.area(df, x=x, y=y, template=template)
    else:
        return px.pie(df, names=x, values=y)


def generate_insights(df):
    insights = []

    insights.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    num = df.select_dtypes(include="number")

    if not num.empty:
        for col in num.columns:
            insights.append(f"{col}: mean={num[col].mean():.2f}")

    return "\n".join(insights)


def ask_data(df, question):
    q = question.lower()

    if "highest" in q or "max" in q:
        col = df.select_dtypes(include="number").columns[0]
        return f"Highest {col}: {df[col].max()}"

    if "average" in q:
        col = df.select_dtypes(include="number").columns[0]
        return f"Average {col}: {df[col].mean():.2f}"

    return "Try asking about highest or average values."
