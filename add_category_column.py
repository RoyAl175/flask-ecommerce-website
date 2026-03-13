import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE products ADD COLUMN category TEXT")

conn.commit()
conn.close()

print("Category column added")