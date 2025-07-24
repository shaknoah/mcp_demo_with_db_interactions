# init_db.py

import sqlite3
import random
from faker import Faker

fake = Faker()

NUM_CUSTOMERS = 1000
NUM_STORES = 50
NUM_ITEMS = 500
NUM_TRANSACTIONS = 10000
NUM_EMPLOYEES = 200
NUM_CATEGORIES = 20

def init_db():
    conn = sqlite3.connect("mall.db")
    cur = conn.cursor()

    # 1. Categories
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    # 2. Customers
    cur.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')

    # 3. Stores
    cur.execute('''
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT
        )
    ''')

    # 4. Items
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')

    # 5. Employees
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT,
            store_id INTEGER,
            FOREIGN KEY (store_id) REFERENCES stores(id)
        )
    ''')

    # 6. Transactions
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            store_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (store_id) REFERENCES stores(id),
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    ''')

    # Generate and insert data
    print("Generating categories...")
    categories = set()
    while len(categories) < NUM_CATEGORIES:
        categories.add(fake.word().capitalize())
    categories = list(categories)

    cur.executemany("INSERT INTO categories (name) VALUES (?)", [(cat,) for cat in categories])

    print("Generating customers...")
    customers = []
    for i in range(NUM_CUSTOMERS):
        cid = f"CUST{i:04d}"
        customers.append((cid, fake.name(), fake.email(), fake.phone_number()))
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)

    print("Generating stores...")
    stores = [(fake.company(), fake.address()) for _ in range(NUM_STORES)]
    cur.executemany("INSERT INTO stores (name, location) VALUES (?, ?)", stores)

    print("Generating items...")
    items = [(fake.word().capitalize(), random.randint(1, NUM_CATEGORIES), round(random.uniform(10, 500), 2)) for _ in range(NUM_ITEMS)]
    cur.executemany("INSERT INTO items (name, category_id, price) VALUES (?, ?, ?)", items)

    print("Generating employees...")
    employees = [(fake.name(), random.choice(["Manager", "Sales", "Support"]), random.randint(1, NUM_STORES)) for _ in range(NUM_EMPLOYEES)]
    cur.executemany("INSERT INTO employees (name, role, store_id) VALUES (?, ?, ?)", employees)

    print("Generating transactions (this may take a while)...")
    transactions = []
    for _ in range(NUM_TRANSACTIONS):
        customer_id = random.choice(customers)[0]
        store_id = random.randint(1, NUM_STORES)
        item_id = random.randint(1, NUM_ITEMS)
        quantity = random.randint(1, 5)
        timestamp = fake.date_time_this_year().isoformat()
        transactions.append((customer_id, store_id, item_id, quantity, timestamp))
    cur.executemany('''
        INSERT INTO transactions (customer_id, store_id, item_id, quantity, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', transactions)

    conn.commit()
    conn.close()
    print("Database created with over 10,000 transactions.")

if __name__ == "__main__":
    init_db()
