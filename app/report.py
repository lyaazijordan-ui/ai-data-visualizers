from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import streamlit as st

def generate_pdf(df):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("AI Data Report", styles["Title"]))
    content.append(Paragraph(df.head().to_string(), styles["Normal"]))

    doc.build(content)

    with open("report.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="report.pdf")
