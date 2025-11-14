## Synthetic E-Commerce Data Pipeline using Cursor + SQLite

### Overview
This project demonstrates an end-to-end e-commerce workflow entirely inside the Cursor IDE. You can generate realistic synthetic datasets, ingest them into SQLite, execute analytical SQL join queries, and version everything with Git/GitHub—all from one environment.

### Tech Stack
- Python  
- Pandas  
- SQLite3  
- Cursor IDE  
- Git & GitHub  

### Project Workflow

**Step 1: Generate Synthetic E-Commerce Data**  
Prompt used inside Cursor terminal:  
```
Generate 5 synthetic e-commerce dataset CSV files with realistic sample data.
1. customers.csv:
   Columns: customer_id, name, email, phone, city, signup_date
2. products.csv:
   Columns: product_id, product_name, category, price, stock
3. orders.csv:
   Columns: order_id, customer_id, order_date, total_amount, payment_method
4. order_items.csv:
   Columns: order_item_id, order_id, product_id, quantity, unit_price
5. shipments.csv:
   Columns: shipment_id, order_id, shipment_date, delivery_status, courier

Ensure:
- At least 50 rows per file
- IDs should be consistent across files
- Use realistic values
- Export each as a separate CSV file
```
After running `python generate_datasets.py`, the CSVs are saved under `data/`.

**Step 2: Import CSVs into SQLite**  
1. Install requirements inside Cursor (`pip install faker pandas`).  
2. Run `python import_data.py` to create `ecommerce.db`, create tables (`customers`, `products`, `orders`, `order_items`, `shipments`), load the CSVs, and validate row counts.  
3. Confirm the script prints `Data imported successfully`.

**Step 3: Run SQL Join Report**  
1. Execute `python run_report.py`.  
2. The script runs the join query:
   ```
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
   ORDER BY o.order_date DESC;
   ```
3. Pandas prints the report, showing per-line item order details and delivery status.

**Step 4: Initialize Git & Commit**  
1. `git init` inside the Cursor terminal.  
2. `git add .` (include `generate_datasets.py`, `import_data.py`, `run_report.py`, `data/*.csv`, and optional `.gitignore`).  
3. `git commit -m "E-commerce synthetic data + SQLite ingestion"`.

**Step 5: Create GitHub Repo & Push**  
1. Use Cursor’s GitHub integration (Command Palette → “GitHub: Create New Repository”) to create an empty repo.  
2. Add the remote: `git remote add origin https://github.com/<user>/<repo>.git`.  
3. Ensure you’re on `main` (`git branch -M main`).  
4. `git push -u origin main` to publish the entire workflow to GitHub.

