"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field, field_validator


class InventoryItemBase(BaseModel):
    item_name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., gt=0)

    @field_validator("item_name")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Item name must not be blank")
        return stripped


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemResponse(InventoryItemBase):
    id: int
    stock_value: float

    model_config = {"from_attributes": True}
