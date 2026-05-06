import sqlite3

conn = sqlite3.connect("mess.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(leaves)")
columns = cur.fetchall()
for col in columns:
    print(col)

conn.close()
