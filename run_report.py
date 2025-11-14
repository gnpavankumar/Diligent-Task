from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd


DB_PATH = Path("ecommerce.db")

REPORT_SQL = """
SELECT
  c.name AS customer_name,
  o.order_id,
  o.order_date,
  p.product_name,
  oi.quantity,
  o.total_amount,
  s.delivery_status
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
JOIN shipments AS s ON s.order_id = o.order_id
ORDER BY o.order_date DESC
"""


def main() -> None:
    if not DB_PATH.exists():
        print(f"SQLite database not found at {DB_PATH.resolve()}", file=sys.stderr)
        sys.exit(1)

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(REPORT_SQL, conn)

    pd.options.display.max_rows = 20
    pd.options.display.max_columns = None

    if df.empty:
        print("No rows returned by the report.")
    else:
        print(df)


if __name__ == "__main__":
    main()

