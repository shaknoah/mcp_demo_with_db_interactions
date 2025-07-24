import sqlite3

DB_PATH = "/Users/shaknoah/Documents/mcp/db_ineraction_project/mall.db"

def run_query(query: str, params: tuple = ()):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

def top_customers_by_spending(limit=5):
    print("\n🔹 Top 5 Customers by Total Spending:")
    query = """
        SELECT c.id, c.name, ROUND(SUM(i.price * t.quantity), 2) AS total_spent
        FROM transactions t
        JOIN items i ON t.item_id = i.id
        JOIN customers c ON t.customer_id = c.id
        GROUP BY t.customer_id
        ORDER BY total_spent DESC
        LIMIT ?;
    """
    results = run_query(query, (limit,))
    for cid, name, total in results:
        print(f" - {name} ({cid}): ₹{total}")

def most_purchased_item():
    print("\n🔹 Most Purchased Item (by quantity):")
    query = """
        SELECT i.name, SUM(t.quantity) AS total_qty
        FROM transactions t
        JOIN items i ON t.item_id = i.id
        GROUP BY t.item_id
        ORDER BY total_qty DESC
        LIMIT 1;
    """
    item, qty = run_query(query)[0]
    print(f" - {item}: {qty} units sold")

def highest_revenue_store():
    print("\n🔹 Store with Highest Revenue:")
    query = """
        SELECT s.name, ROUND(SUM(i.price * t.quantity), 2) AS revenue
        FROM transactions t
        JOIN items i ON t.item_id = i.id
        JOIN stores s ON t.store_id = s.id
        GROUP BY t.store_id
        ORDER BY revenue DESC
        LIMIT 1;
    """
    store, revenue = run_query(query)[0]
    print(f" - {store}: ₹{revenue}")

def category_sales_summary():
    print("\n🔹 Category-wise Quantity and Revenue:")
    query = """
        SELECT cat.name, SUM(t.quantity) AS total_qty, ROUND(SUM(i.price * t.quantity), 2) AS revenue
        FROM transactions t
        JOIN items i ON t.item_id = i.id
        JOIN categories cat ON i.category_id = cat.id
        GROUP BY i.category_id
        ORDER BY revenue DESC;
    """
    results = run_query(query)
    for cat, qty, rev in results:
        print(f" - {cat}: {qty} units, ₹{rev}")

def customer_total_spending(customer_id="CUST0420"):
    print(f"\n🔹 Total Spending for Customer {customer_id}:")
    query = """
        SELECT ROUND(SUM(i.price * t.quantity), 2) AS total_spent
        FROM transactions t
        JOIN items i ON t.item_id = i.id
        WHERE t.customer_id = ?;
    """
    result = run_query(query, (customer_id,))
    total = result[0][0] if result and result[0][0] else 0
    print(f" - ₹{total}")

if __name__ == "__main__":
    top_customers_by_spending()
    most_purchased_item()
    highest_revenue_store()
    category_sales_summary()
    customer_total_spending("CUST0420")
