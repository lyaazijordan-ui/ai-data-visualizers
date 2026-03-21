import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("app_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            theme TEXT DEFAULT 'dark',
            chart_color TEXT DEFAULT 'Agsunset'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS csv_data (
            username TEXT,
            csv_content BLOB,
            PRIMARY KEY(username)
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_user(username, password, theme="dark", chart_color="Agsunset"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (username, password, theme, chart_color)
        VALUES (?, ?, ?, ?)
    """, (username, password, theme, chart_color))
    conn.commit()
    conn.close()

def load_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, theme, chart_color FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def save_csv(username, df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    cursor.execute("INSERT OR REPLACE INTO csv_data (username, csv_content) VALUES (?, ?)", (username, csv_bytes))
    conn.commit()
    conn.close()

def load_csv(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT csv_content FROM csv_data WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return pd.read_csv(pd.compat.StringIO(result[0].decode("utf-8")))
    return None
