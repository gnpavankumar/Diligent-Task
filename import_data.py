from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = Path("ecommerce.db")
DATA_DIR = Path("data")

SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        city TEXT,
        signup_date TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        total_amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS shipments (
        shipment_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        shipment_date TEXT NOT NULL,
        delivery_status TEXT NOT NULL,
        courier TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
    """,
]


CSV_MAPPING = {
    "customers": DATA_DIR / "customers.csv",
    "products": DATA_DIR / "products.csv",
    "orders": DATA_DIR / "orders.csv",
    "order_items": DATA_DIR / "order_items.csv",
    "shipments": DATA_DIR / "shipments.csv",
}


def main() -> None:
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR.resolve()}")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for statement in SCHEMA_STATEMENTS:
            cursor.execute(statement)
        conn.commit()

        for table, csv_path in CSV_MAPPING.items():
            if not csv_path.exists():
                raise FileNotFoundError(f"CSV file missing for table '{table}': {csv_path}")

            df = pd.read_csv(csv_path)
            cursor.execute(f"DELETE FROM {table}")
            conn.commit()

            df.to_sql(table, conn, if_exists="append", index=False)

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            (row_count,) = cursor.fetchone()
            if row_count != len(df):
                raise RuntimeError(
                    f"Row count mismatch for table '{table}': inserted {row_count}, expected {len(df)}"
                )

    print("Data imported successfully")


if __name__ == "__main__":
    main()

