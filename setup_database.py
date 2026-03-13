import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# PRODUCTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
price INTEGER,
image TEXT,
category TEXT
)
""")

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

# ORDERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
product TEXT,
price INTEGER,
order_date TEXT
)
""")

# SAMPLE PRODUCTS
cursor.execute("SELECT COUNT(*) FROM products")

if cursor.fetchone()[0] == 0:

    products = [
        ("Laptop",60000,"laptop.jpg","Electronics"),
        ("Mobile",20000,"mobile.jpg","Electronics"),
        ("Headphones",2000,"headphones.jpg","Accessories"),
        ("Speaker",500,"speaker.jpg","Accessories"),
        ("Keyboard",800,"keyboard.jpg","Accessories"),
        ("Tablet",55000,"tab.jpg","Electronics"),
        ("Mouse",500,"mouse.jpg","Accessories"),
        ("Camera",75000,"camera.jpg","Electronics"),
        ("Power Bank",800,"power_bank.jpg","Gadgets"),
        ("Phone Case",200,"phone_case.jpg","Accessories")
    ]

    cursor.executemany(
        "INSERT INTO products (name,price,image,category) VALUES (?,?,?,?)",
        products
    )

conn.commit()
conn.close()

print("Database setup complete")