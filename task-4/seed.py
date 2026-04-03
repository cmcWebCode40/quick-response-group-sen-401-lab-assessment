"""Seed the SQLite database with initial inventory data."""

from app.database import engine, SessionLocal
from app.models import Base, InventoryItem

SEED_DATA = [
    {"item_name": "Wireless Mouse", "quantity": 150, "price": 12.99},
    {"item_name": "Mechanical Keyboard", "quantity": 85, "price": 49.99},
    {"item_name": "USB-C Hub", "quantity": 200, "price": 25.50},
    {"item_name": "Monitor Stand", "quantity": 60, "price": 34.75},
    {"item_name": "Webcam HD 1080p", "quantity": 120, "price": 29.99},
    {"item_name": "Noise Cancelling Headphones", "quantity": 45, "price": 89.99},
    {"item_name": "Laptop Sleeve 15 inch", "quantity": 300, "price": 15.00},
    {"item_name": "HDMI Cable 2m", "quantity": 500, "price": 7.49},
    {"item_name": "Portable SSD 1TB", "quantity": 30, "price": 79.99},
    {"item_name": "Desk Lamp LED", "quantity": 90, "price": 22.00},
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(InventoryItem).count() == 0:
        for item in SEED_DATA:
            db.add(InventoryItem(**item))
        db.commit()
        print(f"Seeded {len(SEED_DATA)} items.")
    else:
        print("Database already has data, skipping seed.")
    db.close()


if __name__ == "__main__":
    seed()
