
# import sqlite3
# from typing import Any
# from mcp.server.fastmcp import FastMCP

# DB_PATH = "/Users/shaknoah/Documents/mcp/db_ineraction_project/mall.db"
# mcp = FastMCP("mall_transactions")

# def query_db(query: str, params: tuple = ()) -> list[dict[str, Any]]:
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     cur = conn.cursor()
#     cur.execute(query, params)
#     rows = cur.fetchall()
#     conn.close()
#     return [dict(row) for row in rows]

# @mcp.tool()
# async def all_transactions() -> list[dict[str, Any]]:
#     """Fetch all transactions with customer, store, item, and category details."""
#     query = """
#     SELECT 
#         t.id AS transaction_id,
#         t.timestamp,
#         t.quantity,
#         ROUND(i.price * t.quantity, 2) AS total_amount,
#         c.name AS customer_name,
#         s.name AS store_name,
#         i.name AS item_name,
#         cat.name AS category
#     FROM transactions t
#     JOIN customers c ON t.customer_id = c.id
#     JOIN stores s ON t.store_id = s.id
#     JOIN items i ON t.item_id = i.id
#     LEFT JOIN categories cat ON i.category_id = cat.id
#     ORDER BY t.timestamp DESC
#     LIMIT 30
#     """
#     return query_db(query)

# @mcp.tool()
# async def get_transaction_by_id(transaction_id: int) -> dict[str, Any]:
#     """Get a specific transaction with full details."""
#     query = """
#     SELECT 
#         t.id AS transaction_id,
#         t.timestamp,
#         t.quantity,
#         ROUND(i.price * t.quantity, 2) AS total_amount,
#         c.name AS customer_name,
#         s.name AS store_name,
#         i.name AS item_name,
#         cat.name AS category
#     FROM transactions t
#     JOIN customers c ON t.customer_id = c.id
#     JOIN stores s ON t.store_id = s.id
#     JOIN items i ON t.item_id = i.id
#     LEFT JOIN categories cat ON i.category_id = cat.id
#     WHERE t.id = ?
#     """
#     results = query_db(query, (transaction_id,))
#     return results[0] if results else {}

# @mcp.tool()
# async def get_transactions_by_store(store_name: str) -> list[dict[str, Any]]:
#     """Get all transactions for a specific store."""
#     query = """
#     SELECT 
#         t.id AS transaction_id,
#         t.timestamp,
#         t.quantity,
#         ROUND(i.price * t.quantity, 2) AS total_amount,
#         c.name AS customer_name,
#         i.name AS item_name,
#         cat.name AS category
#     FROM transactions t
#     JOIN customers c ON t.customer_id = c.id
#     JOIN stores s ON t.store_id = s.id
#     JOIN items i ON t.item_id = i.id
#     LEFT JOIN categories cat ON i.category_id = cat.id
#     WHERE s.name = ?
#     ORDER BY t.timestamp DESC
#     """
#     return query_db(query, (store_name,))

# @mcp.tool()
# async def get_customer_history(customer_id: str) -> list[dict[str, Any]]:
#     """Get all transactions by a customer ID."""
#     query = """
#     SELECT 
#         t.id AS transaction_id,
#         t.timestamp,
#         s.name AS store_name,
#         i.name AS item_name,
#         t.quantity,
#         ROUND(i.price * t.quantity, 2) AS total_amount
#     FROM transactions t
#     JOIN stores s ON t.store_id = s.id
#     JOIN items i ON t.item_id = i.id
#     WHERE t.customer_id = ?
#     ORDER BY t.timestamp DESC
#     """
#     return query_db(query, (customer_id,))

# @mcp.tool()
# async def top_selling_items(limit: int = 10) -> list[dict[str, Any]]:
#     """Return top-selling items by quantity."""
#     query = """
#     SELECT 
#         i.name AS item_name,
#         cat.name AS category,
#         SUM(t.quantity) AS total_units_sold,
#         ROUND(SUM(t.quantity * i.price), 2) AS total_revenue
#     FROM transactions t
#     JOIN items i ON t.item_id = i.id
#     LEFT JOIN categories cat ON i.category_id = cat.id
#     GROUP BY t.item_id
#     ORDER BY total_units_sold DESC
#     LIMIT ?
#     """
#     return query_db(query, (limit,))

# @mcp.tool()
# async def top_customers_by_spend(limit: int = 10) -> list[dict[str, Any]]:
#     """Return top customers based on total spending."""
#     query = """
#     SELECT 
#         c.id AS customer_id,
#         c.name AS customer_name,
#         ROUND(SUM(i.price * t.quantity), 2) AS total_spent
#     FROM transactions t
#     JOIN customers c ON t.customer_id = c.id
#     JOIN items i ON t.item_id = i.id
#     GROUP BY t.customer_id
#     ORDER BY total_spent DESC
#     LIMIT ?
#     """
#     return query_db(query, (limit,))

# @mcp.tool()
# async def daily_sales_summary(days: int = 7) -> list[dict[str, Any]]:
#     """Return total sales and transaction count per day for recent days."""
#     query = """
#     SELECT 
#         DATE(t.timestamp) AS date,
#         COUNT(*) AS transactions,
#         ROUND(SUM(i.price * t.quantity), 2) AS total_sales
#     FROM transactions t
#     JOIN items i ON t.item_id = i.id
#     WHERE DATE(t.timestamp) >= DATE('now', ? || ' days')
#     GROUP BY DATE(t.timestamp)
#     ORDER BY date DESC
#     """
#     return query_db(query, (-days,))

# @mcp.tool()
# async def category_sales_breakdown() -> list[dict[str, Any]]:
#     """Return total sales and units sold by category."""
#     query = """
#     SELECT 
#         cat.name AS category,
#         COUNT(*) AS transactions,
#         SUM(t.quantity) AS units_sold,
#         ROUND(SUM(i.price * t.quantity), 2) AS total_revenue
#     FROM transactions t
#     JOIN items i ON t.item_id = i.id
#     LEFT JOIN categories cat ON i.category_id = cat.id
#     GROUP BY cat.name
#     ORDER BY total_revenue DESC
#     """
#     return query_db(query)


# @mcp.tool()
# async def high_value_transactions(min_total: float = 1000.0) -> list[dict[str, Any]]:
#     """Return all transactions where total (price * quantity) exceeds threshold."""
#     query = """
#     SELECT 
#         t.id AS transaction_id,
#         c.name AS customer_name,
#         i.name AS item_name,
#         t.quantity,
#         ROUND(i.price * t.quantity, 2) AS total_amount,
#         t.timestamp
#     FROM transactions t
#     JOIN customers c ON t.customer_id = c.id
#     JOIN items i ON t.item_id = i.id
#     WHERE i.price * t.quantity >= ?
#     ORDER BY total_amount DESC
#     LIMIT 50
#     """
#     return query_db(query, (min_total,))

# @mcp.tool()
# async def frequent_customers(min_visits: int = 5) -> list[dict[str, Any]]:
#     """List customers who made at least N purchases."""
#     query = """
#     SELECT 
#         c.id AS customer_id,
#         c.name AS customer_name,
#         COUNT(t.id) AS transaction_count,
#         ROUND(SUM(i.price * t.quantity), 2) AS total_spent
#     FROM transactions t
#     JOIN customers c ON t.customer_id = c.id
#     JOIN items i ON t.item_id = i.id
#     GROUP BY c.id
#     HAVING transaction_count >= ?
#     ORDER BY transaction_count DESC
#     """
#     return query_db(query, (min_visits,))




# @mcp.tool()
# async def store_sales_summary(store_name: str) -> dict[str, Any]:
#     """Return total sales and number of transactions for a given store."""
#     query = """
#     SELECT 
#         COUNT(t.id) AS total_transactions,
#         SUM(t.quantity) AS total_items_sold,
#         ROUND(SUM(i.price * t.quantity), 2) AS total_sales
#     FROM transactions t
#     JOIN stores s ON t.store_id = s.id
#     JOIN items i ON t.item_id = i.id
#     WHERE s.name = ?
#     """
#     results = query_db(query, (store_name,))
#     return results[0] if results else {"message": "Store not found or no sales"}



import sqlite3
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, TextResourceContents

DB_PATH = "/Users/shaknoah/Documents/mcp/db_ineraction_project/mall.db"
mcp = FastMCP("mall_transactions")

def query_db(query: str, params: tuple = ()) -> list[dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# MCP Prompt
@mcp.prompt()
async def mall_analytics_prompt() -> str:
    """
    You are a mall transaction analytics assistant. You have access to a comprehensive database 
    of mall transactions, customers, stores, items, and categories. You can help analyze:
    
    - Transaction patterns and trends
    - Customer behavior and spending habits  
    - Store performance metrics
    - Item popularity and sales data
    - Category-wise revenue analysis
    - High-value transactions and frequent customers
    
    When analyzing data, provide clear insights, identify trends, and suggest actionable 
    business recommendations. Use the available tools to fetch relevant data and present 
    findings in an organized, business-friendly format.
    
    Always consider multiple perspectives when analyzing data:
    - Revenue impact
    - Customer satisfaction
    - Operational efficiency
    - Growth opportunities
    """

# MCP Resources
@mcp.resource("mall://database/schema")
async def database_schema() -> Resource:
    """Database schema information for the mall transactions system."""
    schema_content = """
    # Mall Transactions Database Schema
    
    ## Tables Overview
    
    ### transactions
    - id: Primary key
    - customer_id: Foreign key to customers table
    - store_id: Foreign key to stores table
    - item_id: Foreign key to items table
    - quantity: Number of items purchased
    - timestamp: Transaction date and time
    
    ### customers
    - id: Primary key
    - name: Customer name
    
    ### stores
    - id: Primary key
    - name: Store name
    
    ### items
    - id: Primary key
    - name: Item name
    - price: Item price
    - category_id: Foreign key to categories table
    
    ### categories
    - id: Primary key
    - name: Category name
    
    ## Relationships
    - Each transaction links one customer, one store, and one item
    - Items belong to categories
    - Transactions track quantity and can calculate total amount (price * quantity)
    """
    
    return Resource(
        uri="mall://database/schema",
        name="Database Schema",
        description="Complete database schema for mall transactions system",
        mimeType="text/markdown",
        text=schema_content
    )

@mcp.resource("mall://analytics/kpis")
async def key_performance_indicators() -> Resource:
    """Key Performance Indicators and metrics definitions."""
    kpi_content = """
    # Mall Analytics - Key Performance Indicators
    
    ## Revenue Metrics
    - **Total Sales**: Sum of all transaction amounts (price * quantity)
    - **Average Transaction Value**: Total sales / number of transactions
    - **Revenue per Customer**: Total sales / unique customers
    - **Revenue per Store**: Total sales by individual store
    
    ## Customer Metrics
    - **Customer Frequency**: Number of transactions per customer
    - **Customer Lifetime Value**: Total spending per customer
    - **Repeat Customer Rate**: Customers with multiple transactions
    - **High-Value Customers**: Customers exceeding spending thresholds
    
    ## Product Metrics
    - **Best Sellers**: Items with highest unit sales
    - **Revenue Leaders**: Items generating most revenue
    - **Category Performance**: Sales breakdown by product category
    - **Inventory Turnover**: Frequency of item sales
    
    ## Operational Metrics
    - **Daily Sales Trends**: Sales patterns over time
    - **Store Performance**: Comparative analysis across stores
    - **Peak Hours/Days**: Transaction timing patterns
    - **Average Items per Transaction**: Basket size analysis
    """
    
    return Resource(
        uri="mall://analytics/kpis",
        name="Key Performance Indicators",
        description="Definitions and explanations of mall analytics KPIs",
        mimeType="text/markdown",
        text=kpi_content
    )

@mcp.resource("mall://reports/templates")
async def report_templates() -> Resource:
    """Standard report templates and formats."""
    template_content = """
    # Standard Report Templates
    
    ## Executive Summary Template
    ```
    Mall Performance Summary - [Date Range]
    
    Key Metrics:
    - Total Revenue: $[amount]
    - Total Transactions: [count]
    - Average Transaction: $[amount]
    - Active Customers: [count]
    - Top Performing Store: [name]
    
    Insights:
    - [Key finding 1]
    - [Key finding 2]
    - [Key finding 3]
    
    Recommendations:
    - [Recommendation 1]
    - [Recommendation 2]
    ```
    
    ## Store Performance Template
    ```
    Store Analysis: [Store Name]
    
    Performance Metrics:
    - Total Sales: $[amount]
    - Transaction Count: [number]
    - Average Sale: $[amount]
    - Top Items: [list]
    
    Customer Analysis:
    - Unique Customers: [count]
    - Repeat Customers: [count]
    - Average Spend per Customer: $[amount]
    ```
    
    ## Customer Segmentation Template
    ```
    Customer Segment: [Segment Name]
    
    Characteristics:
    - Total Customers: [count]
    - Average Spend: $[amount]
    - Purchase Frequency: [number]
    - Preferred Categories: [list]
    
    Behavior Patterns:
    - [Pattern 1]
    - [Pattern 2]
    ```
    """
    
    return Resource(
        uri="mall://reports/templates",
        name="Report Templates",
        description="Standard templates for mall analytics reports",
        mimeType="text/markdown",
        text=template_content
    )

# Tools (from original code)
@mcp.tool()
async def all_transactions() -> list[dict[str, Any]]:
    """Fetch all transactions with customer, store, item, and category details."""
    query = """
    SELECT 
        t.id AS transaction_id,
        t.timestamp,
        t.quantity,
        ROUND(i.price * t.quantity, 2) AS total_amount,
        c.name AS customer_name,
        s.name AS store_name,
        i.name AS item_name,
        cat.name AS category
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN stores s ON t.store_id = s.id
    JOIN items i ON t.item_id = i.id
    LEFT JOIN categories cat ON i.category_id = cat.id
    ORDER BY t.timestamp DESC
    LIMIT 30
    """
    return query_db(query)

@mcp.tool()
async def get_transaction_by_id(transaction_id: int) -> dict[str, Any]:
    """Get a specific transaction with full details."""
    query = """
    SELECT 
        t.id AS transaction_id,
        t.timestamp,
        t.quantity,
        ROUND(i.price * t.quantity, 2) AS total_amount,
        c.name AS customer_name,
        s.name AS store_name,
        i.name AS item_name,
        cat.name AS category
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN stores s ON t.store_id = s.id
    JOIN items i ON t.item_id = i.id
    LEFT JOIN categories cat ON i.category_id = cat.id
    WHERE t.id = ?
    """
    results = query_db(query, (transaction_id,))
    return results[0] if results else {}

@mcp.tool()
async def get_transactions_by_store(store_name: str) -> list[dict[str, Any]]:
    """Get all transactions for a specific store."""
    query = """
    SELECT 
        t.id AS transaction_id,
        t.timestamp,
        t.quantity,
        ROUND(i.price * t.quantity, 2) AS total_amount,
        c.name AS customer_name,
        i.name AS item_name,
        cat.name AS category
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN stores s ON t.store_id = s.id
    JOIN items i ON t.item_id = i.id
    LEFT JOIN categories cat ON i.category_id = cat.id
    WHERE s.name = ?
    ORDER BY t.timestamp DESC
    """
    return query_db(query, (store_name,))

@mcp.tool()
async def get_customer_history(customer_id: str) -> list[dict[str, Any]]:
    """Get all transactions by a customer ID."""
    query = """
    SELECT 
        t.id AS transaction_id,
        t.timestamp,
        s.name AS store_name,
        i.name AS item_name,
        t.quantity,
        ROUND(i.price * t.quantity, 2) AS total_amount
    FROM transactions t
    JOIN stores s ON t.store_id = s.id
    JOIN items i ON t.item_id = i.id
    WHERE t.customer_id = ?
    ORDER BY t.timestamp DESC
    """
    return query_db(query, (customer_id,))

@mcp.tool()
async def top_selling_items(limit: int = 10) -> list[dict[str, Any]]:
    """Return top-selling items by quantity."""
    query = """
    SELECT 
        i.name AS item_name,
        cat.name AS category,
        SUM(t.quantity) AS total_units_sold,
        ROUND(SUM(t.quantity * i.price), 2) AS total_revenue
    FROM transactions t
    JOIN items i ON t.item_id = i.id
    LEFT JOIN categories cat ON i.category_id = cat.id
    GROUP BY t.item_id
    ORDER BY total_units_sold DESC
    LIMIT ?
    """
    return query_db(query, (limit,))

@mcp.tool()
async def top_customers_by_spend(limit: int = 10) -> list[dict[str, Any]]:
    """Return top customers based on total spending."""
    query = """
    SELECT 
        c.id AS customer_id,
        c.name AS customer_name,
        ROUND(SUM(i.price * t.quantity), 2) AS total_spent
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN items i ON t.item_id = i.id
    GROUP BY t.customer_id
    ORDER BY total_spent DESC
    LIMIT ?
    """
    return query_db(query, (limit,))

@mcp.tool()
async def daily_sales_summary(days: int = 7) -> list[dict[str, Any]]:
    """Return total sales and transaction count per day for recent days."""
    query = """
    SELECT 
        DATE(t.timestamp) AS date,
        COUNT(*) AS transactions,
        ROUND(SUM(i.price * t.quantity), 2) AS total_sales
    FROM transactions t
    JOIN items i ON t.item_id = i.id
    WHERE DATE(t.timestamp) >= DATE('now', ? || ' days')
    GROUP BY DATE(t.timestamp)
    ORDER BY date DESC
    """
    return query_db(query, (-days,))

@mcp.tool()
async def category_sales_breakdown() -> list[dict[str, Any]]:
    """Return total sales and units sold by category."""
    query = """
    SELECT 
        cat.name AS category,
        COUNT(*) AS transactions,
        SUM(t.quantity) AS units_sold,
        ROUND(SUM(i.price * t.quantity), 2) AS total_revenue
    FROM transactions t
    JOIN items i ON t.item_id = i.id
    LEFT JOIN categories cat ON i.category_id = cat.id
    GROUP BY cat.name
    ORDER BY total_revenue DESC
    """
    return query_db(query)

@mcp.tool()
async def high_value_transactions(min_total: float = 1000.0) -> list[dict[str, Any]]:
    """Return all transactions where total (price * quantity) exceeds threshold."""
    query = """
    SELECT 
        t.id AS transaction_id,
        c.name AS customer_name,
        i.name AS item_name,
        t.quantity,
        ROUND(i.price * t.quantity, 2) AS total_amount,
        t.timestamp
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN items i ON t.item_id = i.id
    WHERE i.price * t.quantity >= ?
    ORDER BY total_amount DESC
    LIMIT 50
    """
    return query_db(query, (min_total,))

@mcp.tool()
async def frequent_customers(min_visits: int = 5) -> list[dict[str, Any]]:
    """List customers who made at least N purchases."""
    query = """
    SELECT 
        c.id AS customer_id,
        c.name AS customer_name,
        COUNT(t.id) AS transaction_count,
        ROUND(SUM(i.price * t.quantity), 2) AS total_spent
    FROM transactions t
    JOIN customers c ON t.customer_id = c.id
    JOIN items i ON t.item_id = i.id
    GROUP BY c.id
    HAVING transaction_count >= ?
    ORDER BY transaction_count DESC
    """
    return query_db(query, (min_visits,))

@mcp.tool()
async def store_sales_summary(store_name: str) -> dict[str, Any]:
    """Return total sales and number of transactions for a given store."""
    query = """
    SELECT 
        COUNT(t.id) AS total_transactions,
        SUM(t.quantity) AS total_items_sold,
        ROUND(SUM(i.price * t.quantity), 2) AS total_sales
    FROM transactions t
    JOIN stores s ON t.store_id = s.id
    JOIN items i ON t.item_id = i.id
    WHERE s.name = ?
    """
    results = query_db(query, (store_name,))
    return results[0] if results else {"message": "Store not found or no sales"}

# Additional analytics tools
@mcp.tool()
async def monthly_trends(months: int = 6) -> list[dict[str, Any]]:
    """Analyze sales trends over the past N months."""
    query = """
    SELECT 
        strftime('%Y-%m', t.timestamp) AS month,
        COUNT(*) AS transactions,
        SUM(t.quantity) AS items_sold,
        ROUND(SUM(i.price * t.quantity), 2) AS total_sales,
        ROUND(AVG(i.price * t.quantity), 2) AS avg_transaction_value
    FROM transactions t
    JOIN items i ON t.item_id = i.id
    WHERE DATE(t.timestamp) >= DATE('now', '-' || ? || ' months')
    GROUP BY strftime('%Y-%m', t.timestamp)
    ORDER BY month DESC
    """
    return query_db(query, (months,))

@mcp.tool()
async def customer_segmentation() -> list[dict[str, Any]]:
    """Segment customers based on spending patterns."""
    query = """
    WITH customer_stats AS (
        SELECT 
            c.id,
            c.name,
            COUNT(t.id) AS transaction_count,
            ROUND(SUM(i.price * t.quantity), 2) AS total_spent,
            ROUND(AVG(i.price * t.quantity), 2) AS avg_transaction
        FROM customers c
        JOIN transactions t ON c.id = t.customer_id
        JOIN items i ON t.item_id = i.id
        GROUP BY c.id, c.name
    )
    SELECT 
        name AS customer_name,
        total_spent,
        transaction_count,
        avg_transaction,
        CASE 
            WHEN total_spent >= 5000 THEN 'VIP'
            WHEN total_spent >= 2000 THEN 'Premium'
            WHEN total_spent >= 500 THEN 'Regular'
            ELSE 'Occasional'
        END AS segment
    FROM customer_stats
    ORDER BY total_spent DESC
    """
    return query_db(query)

if __name__ == "__main__":
    mcp.run()