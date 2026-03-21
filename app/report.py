from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st

def generate_pdf(df, insights):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("AI Data Lab Report", styles["Title"]))
    content.append(Paragraph(df.head().to_string(), styles["Normal"]))
    content.append(Paragraph(insights, styles["Normal"]))

    doc.build(content)

    with open("report.pdf", "rb") as f:
        st.download_button("Download PDF", f)
