import sqlite3

conn = sqlite3.connect("jobportal.db")
cursor = conn.cursor()

# ==============================
# USERS TABLE (STUDENTS)
# ==============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

# ==============================
# JOBS TABLE
# ==============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    location TEXT,
    description TEXT
)
""")

# ==============================
# APPLICATIONS TABLE
# ==============================
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    job_id INTEGER,
    resume TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully 🚀")