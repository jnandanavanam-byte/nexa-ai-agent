from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey
)
from pathlib import Path

# --------------------------------------------------
# ✅ FIX: Use absolute path for SQLite database
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sales.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

metadata = MetaData()

# --------------------------------------------------
# Tables
# --------------------------------------------------

customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("city", String, nullable=False),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("category", String, nullable=False),
    Column("price", Float, nullable=False),
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey("customers.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("quantity", Integer, nullable=False),
    Column("order_date", Date, nullable=False),
)

# --------------------------------------------------
# DB initialization
# --------------------------------------------------

def init_db():
    metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("✅ Database schema created successfully.")