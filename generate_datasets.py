import csv, random, os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

os.makedirs('data', exist_ok=True)

num_customers = 80
num_products = 70
num_orders = 150

customers = []
for cid in range(1, num_customers + 1):
    customers.append({
        'customer_id': cid,
        'name': fake.name(),
        'email': fake.unique.email(),
        'phone': fake.phone_number(),
        'city': fake.city(),
        'signup_date': fake.date_between(start_date='-3y', end_date='-6m').isoformat()
    })

categories = [
    'Electronics', 'Home & Kitchen', 'Books', 'Apparel', 'Beauty',
    'Sports', 'Toys', 'Grocery', 'Automotive', 'Garden'
]

products = []
for pid in range(1, num_products + 1):
    price = round(random.uniform(5, 500), 2)
    products.append({
        'product_id': pid,
        'product_name': fake.catch_phrase(),
        'category': random.choice(categories),
        'price': price,
        'stock': random.randint(20, 500)
    })

product_price_lookup = {p['product_id']: p['price'] for p in products}

payment_methods = ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery', 'Gift Card']

orders = []
order_items = []
order_item_id_counter = 1

for oid in range(1, num_orders + 1):
    customer_id = random.randint(1, num_customers)
    order_date = fake.date_between(start_date='-18m', end_date='today')
    num_items = random.randint(1, 5)
    order_total = 0.0
    chosen_products = random.sample(range(1, num_products + 1), k=num_items)
    for prod_id in chosen_products:
        quantity = random.randint(1, 4)
        unit_price = product_price_lookup[prod_id]
        line_total = quantity * unit_price
        order_total += line_total
        order_items.append({
            'order_item_id': order_item_id_counter,
            'order_id': oid,
            'product_id': prod_id,
            'quantity': quantity,
            'unit_price': round(unit_price, 2)
        })
        order_item_id_counter += 1
    orders.append({
        'order_id': oid,
        'customer_id': customer_id,
        'order_date': order_date.isoformat(),
        'total_amount': round(order_total, 2),
        'payment_method': random.choice(payment_methods)
    })

couriers = ['DHL', 'FedEx', 'UPS', 'USPS', 'Royal Mail', 'Canada Post']
delivery_statuses = ['Pending', 'Shipped', 'In Transit', 'Out for Delivery', 'Delivered']

shipments = []
for order in orders:
    shipment_date = datetime.fromisoformat(order['order_date']) + timedelta(days=random.randint(1, 7))
    status = random.choices(
        delivery_statuses,
        weights=[0.1, 0.25, 0.25, 0.15, 0.25],
        k=1
    )[0]
    shipments.append({
        'shipment_id': order['order_id'],
        'order_id': order['order_id'],
        'shipment_date': shipment_date.date().isoformat(),
        'delivery_status': status,
        'courier': random.choice(couriers)
    })

files = [
    ('data/customers.csv', ['customer_id', 'name', 'email', 'phone', 'city', 'signup_date'], customers),
    ('data/products.csv', ['product_id', 'product_name', 'category', 'price', 'stock'], products),
    ('data/orders.csv', ['order_id', 'customer_id', 'order_date', 'total_amount', 'payment_method'], orders),
    ('data/order_items.csv', ['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price'], order_items),
    ('data/shipments.csv', ['shipment_id', 'order_id', 'shipment_date', 'delivery_status', 'courier'], shipments)
]

for path, headers, rows in files:
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

print('Generated files:')
for path, *_ in files:
    print(path)
