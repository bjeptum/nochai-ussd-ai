# db.py
import sqlite3
from datetime import datetime

DATABASE = "nochai.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  location TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (session_id TEXT PRIMARY KEY,
                  phone_number TEXT,
                  step INTEGER,
                  temp_data TEXT,
                  last_seen TEXT)''')
    conn.commit()
    conn.close()
    print("Database initialized")

def add_report(location, amount, category, description):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""INSERT INTO reports 
                 (timestamp, location, amount, category, description)
                 VALUES (?, ?, ?, ?, ?)""",
              (datetime.now().isoformat(), location, amount, category, description[:500]))
    conn.commit()
    conn.close()

def get_session(session_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT session_id, phone_number, step, temp_data FROM sessions WHERE session_id=?", (session_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"session_id": row[0], "phone": row[1], "step": row[2], "temp_data": row[3]}
    return None

def update_session(session_id, phone_number, step, temp_data=None):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("""INSERT OR REPLACE INTO sessions
                 (session_id, phone_number, step, temp_data, last_seen)
                 VALUES (?, ?, ?, ?, ?)""",
              (session_id, phone_number, step, temp_data or "", now))
    conn.commit()
    conn.close()