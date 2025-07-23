import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("bill_db.sqlite")
cursor = conn.cursor()

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
)
""")

# Create bills table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    total REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create bill_items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bill_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bill_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY(bill_id) REFERENCES bills(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

# Insert some products only if not already present
cursor.execute("SELECT COUNT(*) FROM products")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", [
        ('Apple', 0.5),
        ('Banana', 0.3),
        ('Orange', 0.7)
    ])

conn.commit()
conn.close()

print("Database and tables created successfully.")
