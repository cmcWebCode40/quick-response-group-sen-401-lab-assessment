"""FastAPI REST API for inventory management."""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.models import Base, InventoryItem
from app.schemas import InventoryItemCreate, InventoryItemResponse
from seed import seed

Base.metadata.create_all(bind=engine)
seed()

api = FastAPI(title="Inventory API", version="1.0.0")


def to_response(item: InventoryItem) -> dict:
    """Convert an ORM item to a response dict with computed stock_value."""
    return {
        "id": item.id,
        "item_name": item.item_name,
        "quantity": item.quantity,
        "price": item.price,
        "stock_value": item.stock_value,
    }


@api.get("/items", response_model=list[InventoryItemResponse])
def list_items(db: Session = Depends(get_db)):
    """Return all inventory items."""
    return [to_response(i) for i in db.query(InventoryItem).all()]


@api.get("/items/{item_id}", response_model=InventoryItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Return a single inventory item by ID."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return to_response(item)


@api.post("/items", response_model=InventoryItemResponse, status_code=201)
def create_item(payload: InventoryItemCreate, db: Session = Depends(get_db)):
    """Create a new inventory item."""
    item = InventoryItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return to_response(item)


@api.put("/items/{item_id}", response_model=InventoryItemResponse)
def update_item(item_id: int, payload: InventoryItemCreate, db: Session = Depends(get_db)):
    """Update an existing inventory item."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.item_name = payload.item_name
    item.quantity = payload.quantity
    item.price = payload.price
    db.commit()
    db.refresh(item)
    return to_response(item)


@api.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an inventory item by ID."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()


@api.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Return summary statistics for all inventory items."""
    items = db.query(InventoryItem).all()
    if not items:
        return {"total_items": 0, "total_units": 0, "total_value": 0.0}
    total_units = sum(i.quantity for i in items)
    total_value = round(sum(i.stock_value for i in items), 2)
    avg_price = round(sum(i.price for i in items) / len(items), 2)
    return {
        "total_items": len(items),
        "total_units": total_units,
        "total_value": total_value,
        "average_price": avg_price,
    }
