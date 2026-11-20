import duckdb
import random
from datetime import date, timedelta
from faker import Faker

# Configuration
DB_PATH = "sales.duckdb"

NUM_CUSTOMERS = 100
NUM_ORDERS = 500
MAX_ITEMS_PER_ORDER = 5


def main():
    fake = Faker()
    random.seed(42)



    # Connect to DuckDB
    con = duckdb.connect(DB_PATH)

    # --------------------------------------------------
    # 1. Create tables
    # --------------------------------------------------

    con.execute("""
        CREATE OR REPLACE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name VARCHAR,
            email VARCHAR
        )
    """)

    con.execute("""
        CREATE OR REPLACE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATE,
            notes VARCHAR,
            status VARCHAR
        )
    """)

    con.execute("""
        CREATE OR REPLACE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            unit_price DECIMAL(10, 2),
            quantity INTEGER
        )
    """)

    # --------------------------------------------------
    # 2. Populate customers
    # --------------------------------------------------

    customers = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):
        customers.append((
            customer_id,
            fake.name(),
            fake.email()
        ))

    con.executemany("""
        INSERT INTO customers
        VALUES (?, ?, ?)
    """, customers)

    # --------------------------------------------------
    # 3. Populate orders
    # --------------------------------------------------

    statuses = [
        "delivered",
        "delivered",
        "delivered",
        "shipped",
        "processing",
        "cancelled",
        "pending"
    ]

    notes_options = [
        "Leave at front door",
        "Ring the doorbell",
        "Express delivery requested",
        "Customer requested gift wrapping",
        "Deliver after 17:00",
        None,
        None
    ]

    orders = []

    start_date = date.today() - timedelta(days=365)

    for order_id in range(1, NUM_ORDERS + 1):
        customer_id = random.randint(1, NUM_CUSTOMERS)

        order_date = start_date + timedelta(
            days=random.randint(0, 365)
        )

        status = random.choice(statuses)
        notes = random.choice(notes_options)

        orders.append((
            order_id,
            customer_id,
            order_date,
            notes,
            status
        ))

    con.executemany("""
        INSERT INTO orders
        VALUES (?, ?, ?, ?, ?)
    """, orders)

    # --------------------------------------------------
    # 4. Populate order_items
    # --------------------------------------------------

    order_items = []
    order_item_id = 1

    for order_id in range(1, NUM_ORDERS + 1):

        number_of_items = random.randint(
            1,
            MAX_ITEMS_PER_ORDER
        )

        for _ in range(number_of_items):
            unit_price = round(
                random.uniform(5.00, 500.00), 2
            )

            quantity = random.randint(1, 10)

            order_items.append((
                order_item_id,
                order_id,
                unit_price,
                quantity
            ))

            order_item_id += 1

    con.executemany("""
        INSERT INTO order_items
        VALUES (?, ?, ?, ?)
    """, order_items)

    # --------------------------------------------------
    # 5. Verify data
    # --------------------------------------------------

    print("\nDatabase populated successfully!")

    for table in ["customers", "orders", "order_items"]:
        count = con.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table}: {count} records")

    delivered_count = con.execute("""
        SELECT COUNT(*)
        FROM orders
        WHERE status = 'delivered'
    """).fetchone()[0]

    print(f"\nDelivered orders: {delivered_count}")

    con.close()

if __name__ == "__main__":
    main()