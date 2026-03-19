# app/data_engine.py
import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    """
    Load CSV file into a pandas DataFrame.
    """
    try:
        df = pd.read_csv(uploaded_file)
        st.success("CSV loaded successfully!")
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None