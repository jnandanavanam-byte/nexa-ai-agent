from datetime import date
from sqlalchemy import create_engine, insert
from app.core.db_init import customers, products, orders, engine


def seed_data():
    with engine.begin() as conn:
        # Customers
        conn.execute(insert(customers), [
            {"id": 1, "name": "Alice Johnson", "city": "Dubai"},
            {"id": 2, "name": "Rahul Mehta", "city": "Hyderabad"},
            {"id": 3, "name": "Fatima Noor", "city": "Abu Dhabi"},
        ])

        # Products
        conn.execute(insert(products), [
            {"id": 1, "name": "Laptop", "category": "Electronics", "price": 4500.0},
            {"id": 2, "name": "Smartphone", "category": "Electronics", "price": 2500.0},
            {"id": 3, "name": "Office Chair", "category": "Furniture", "price": 900.0},
        ])

        # Orders
        conn.execute(insert(orders), [
            {
                "id": 1,
                "customer_id": 1,
                "product_id": 1,
                "quantity": 1,
                "order_date": date(2026, 10, 10),
            },
            {
                "id": 2,
                "customer_id": 2,
                "product_id": 2,
                "quantity": 2,
                "order_date": date(2026, 10, 12),
            },
            {
                "id": 3,
                "customer_id": 3,
                "product_id": 3,
                "quantity": 4,
                "order_date": date(2026, 10, 15),
            },
        ])


if __name__ == "__main__":
    seed_data()
    print("✅ Sample data inserted successfully.")