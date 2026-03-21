# db.py
import streamlit as st
import json
import os

def get_db_file(key):
    return f"db_{key}.json"

def save_data(key, data):
    file = get_db_file(key)
    with open(file, "w") as f:
        json.dump(data, f)

def load_data(key):
    file = get_db_file(key)
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}
