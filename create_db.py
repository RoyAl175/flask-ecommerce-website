import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE products (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
price INTEGER,
image TEXT
)
""")

cursor.execute("""
INSERT INTO products (name,price,image)
VALUES
('Laptop',60000,'laptop.jpg'),
('Mobile',20000,'mobile.jpg'),
('Headphones',2000,'headphones.jpg')
""")

conn.commit()

conn.close()

print("Database created successfully")