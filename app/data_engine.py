import pandas as pd
import json
import os

def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except:
        return None


def save_user_data(email, df):
    os.makedirs("user_data", exist_ok=True)
    filepath = f"user_data/{email}.json"
    with open(filepath, "w") as f:
        f.write(df.to_json())


def load_user_data(email):
    filepath = f"user_data/{email}.json"
    try:
        with open(filepath, "r") as f:
            return pd.read_json(f.read())
    except:
        return None
