import pandas as pd
import os

def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return None


def save_user_data(email, df):
    os.makedirs("user_data", exist_ok=True)
    filepath = f"user_data/{email}.json"
    df.to_json(filepath)


def load_user_data(email):
    filepath = f"user_data/{email}.json"
    try:
        return pd.read_json(filepath)
    except:
        return None
