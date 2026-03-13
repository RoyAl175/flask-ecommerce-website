import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
product TEXT,
price INTEGER
)
""")

conn.commit()
conn.close()

print("Orders table created")