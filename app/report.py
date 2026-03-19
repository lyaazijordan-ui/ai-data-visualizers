# app/report.py
from fpdf import FPDF
import pandas as pd
import streamlit as st

def generate_pdf(df):
    """
    Generate a simple PDF report from the DataFrame.
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "AI Data Visualization Report", ln=True, align="C")
        
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        
        # Add table headers
        col_names = df.columns.tolist()
        for col in col_names:
            pdf.cell(40, 10, col, 1)
        pdf.ln()
        
        # Add table rows (first 10 rows)
        for i in range(min(10, len(df))):
            for col in col_names:
                pdf.cell(40, 10, str(df[col].iloc[i]), 1)
            pdf.ln()
        
        # Save PDF to disk
        pdf_file = "report.pdf"
        pdf.output(pdf_file)
        
        st.success(f"PDF generated: {pdf_file}")
        st.download_button(label="Download PDF", data=open(pdf_file, "rb"), file_name="report.pdf")
    except Exception as e:
        st.error(f"Error generating PDF: {e}")