"""Helper functions for inventory stock analysis."""

from __future__ import annotations

import statistics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inventory import InventoryItem


def total_stock_value(items: list[InventoryItem]) -> float:
    """Calculate the combined value of all items in inventory.

    Returns 0.0 when the inventory list is empty.
    """
    if not items:
        return 0.0
    return round(sum(item.stock_value for item in items), 2)


def highest_stock_item(items: list[InventoryItem]) -> InventoryItem | None:
    """Return the item with the highest total stock value.

    Returns None when the inventory list is empty.
    """
    if not items:
        return None
    return max(items, key=lambda item: item.stock_value)


def lowest_stock_item(items: list[InventoryItem]) -> InventoryItem | None:
    """Return the item with the lowest total stock value.

    Returns None when the inventory list is empty.
    """
    if not items:
        return None
    return min(items, key=lambda item: item.stock_value)


def average_item_price(items: list[InventoryItem]) -> float:
    """Calculate the average unit price across all inventory items.

    Returns 0.0 when the inventory list is empty.
    """
    if not items:
        return 0.0
    return round(sum(item.price for item in items) / len(items), 2)


def median_item_price(items: list[InventoryItem]) -> float:
    """Calculate the median unit price across all inventory items.

    Returns 0.0 when the inventory list is empty.
    """
    if not items:
        return 0.0
    return float(statistics.median(item.price for item in items))


def total_units_in_stock(items: list[InventoryItem]) -> int:
    """Return the sum of all item quantities in the inventory."""
    return sum(item.quantity for item in items)


def items_below_threshold(items: list[InventoryItem], threshold: int = 50) -> list[InventoryItem]:
    """Return items whose quantity falls below the given restock threshold."""
    return [item for item in items if item.quantity < threshold]


def items_above_threshold(items: list[InventoryItem], threshold: int = 50) -> list[InventoryItem]:
    """Return items whose quantity meets or exceeds the given threshold."""
    return [item for item in items if item.quantity >= threshold]


def sort_by_stock_value(items: list[InventoryItem], descending: bool = True) -> list[InventoryItem]:
    """Return a new list of items sorted by total stock value."""
    return sorted(items, key=lambda item: item.stock_value, reverse=descending)


def sort_by_quantity(items: list[InventoryItem], descending: bool = True) -> list[InventoryItem]:
    """Return a new list of items sorted by quantity."""
    return sorted(items, key=lambda item: item.quantity, reverse=descending)
