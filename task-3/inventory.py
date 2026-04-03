"""Inventory data validated with Pydantic models."""

from pydantic import BaseModel, Field, field_validator


class InventoryItem(BaseModel):
    """A single inventory item with validated fields."""

    item_name: str = Field(..., min_length=1, description="Name of the inventory item")
    quantity: int = Field(..., ge=0, description="Number of units in stock")
    price: float = Field(..., gt=0, description="Unit price in currency")

    @field_validator("item_name")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Item name must not be blank")
        return stripped

    @property
    def stock_value(self) -> float:
        return round(self.quantity * self.price, 2)


inventory: list[InventoryItem] = [
    InventoryItem(item_name="Wireless Mouse", quantity=150, price=12.99),
    InventoryItem(item_name="Mechanical Keyboard", quantity=85, price=49.99),
    InventoryItem(item_name="USB-C Hub", quantity=200, price=25.50),
    InventoryItem(item_name="Monitor Stand", quantity=60, price=34.75),
    InventoryItem(item_name="Webcam HD 1080p", quantity=120, price=29.99),
    InventoryItem(item_name="Noise Cancelling Headphones", quantity=45, price=89.99),
    InventoryItem(item_name="Laptop Sleeve 15 inch", quantity=300, price=15.00),
    InventoryItem(item_name="HDMI Cable 2m", quantity=500, price=7.49),
    InventoryItem(item_name="Portable SSD 1TB", quantity=30, price=79.99),
    InventoryItem(item_name="Desk Lamp LED", quantity=90, price=22.00),
]
