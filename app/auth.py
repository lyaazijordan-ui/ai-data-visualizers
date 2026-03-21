import sqlite3
import streamlit as st

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            theme TEXT DEFAULT 'plotly_dark',
            chart_color TEXT DEFAULT 'Agsunset'
        )
    ''')
    conn.commit()
    conn.close()

def signup(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success(f"User '{username}' created! You can now log in.")
        return True
    except sqlite3.IntegrityError:
        st.error("Username already exists. Try another.")
        return False
    finally:
        conn.close()

def login(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == password:
        st.session_state["username"] = username
        return True
    else:
        st.error("Login failed. Check your username/password.")
        return False

def load_user_settings(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT theme, chart_color FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return {"theme": result[0], "chart_color": result[1]}
    else:
        return {"theme": "plotly_dark", "chart_color": "Agsunset"}

def save_user_settings(username, theme=None, chart_color=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if theme:
        c.execute("UPDATE users SET theme=? WHERE username=?", (theme, username))
    if chart_color:
        c.execute("UPDATE users SET chart_color=? WHERE username=?", (chart_color, username))
    conn.commit()
    conn.close()

init_db()
