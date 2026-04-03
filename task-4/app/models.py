"""SQLAlchemy ORM model for inventory items."""

from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False)

    @property
    def stock_value(self) -> float:
        return round(self.quantity * self.price, 2)
