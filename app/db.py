import sqlite3
import pandas as pd

DB = "data.db"

def init_data_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            username TEXT,
            name TEXT,
            csv TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_data(username, name, df):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    csv_str = df.to_csv(index=False)
    c.execute("INSERT INTO datasets (username, name, csv) VALUES (?, ?, ?)", (username, name, csv_str))
    conn.commit()
    conn.close()

def load_data(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, csv FROM datasets WHERE username=?", (username,))
    rows = c.fetchall()
    conn.close()
    return [(r[0], pd.read_csv(pd.compat.StringIO(r[1]))) for r in rows]

init_data_db()
