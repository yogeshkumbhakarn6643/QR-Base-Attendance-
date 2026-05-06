import sqlite3
import os
import sys
import shutil

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DB_PATH = os.path.join(BASE_DIR, "mess.db")


# def get_db():
#     return sqlite3.connect(DB_PATH)


def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Running as EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as .py
        return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
DB_PATH = os.path.join(BASE_DIR, "mess.db")


def get_db():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mobile TEXT UNIQUE,
        user_type TEXT DEFAULT 'Direct Meal'
    )
    """)

    # WALLET (balance)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS wallet (
        user_id INTEGER PRIMARY KEY,
        balance REAL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # ATTENDANCE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        session TEXT,
        amount REAL,
        status TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # LEAVES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leaves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        session TEXT,          -- 'morning', 'night', or 'both'
        status TEXT DEFAULT 'pending',  -- 'pending', 'approved', 'rejected'
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # PAYMENTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        date TEXT,
        mode TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # SETTINGS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        meal_price REAL
    )
    """)

    # DEFAULT MEAL PRICE
    cur.execute("""
    INSERT OR IGNORE INTO settings (id, meal_price)
    VALUES (1, 50)
    """)

    # SYSTEM LOG (prevents double deduction)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_date TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()


def get_meal_price():
    """
    Returns the current per tiffin / plate amount from settings table.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT meal_price FROM settings WHERE id = 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    return 0  # default if not set


def backup_db():
    if not os.path.exists(DB_PATH):
        return
    backup_path = os.path.join(BASE_DIR, "mess_backup.db")
    shutil.copyfile(DB_PATH, backup_path)
