"""Main entry point — reads inventory data and displays a stock analysis report."""

from tabulate import tabulate

from inventory import inventory
from utils.helpers import (
    total_stock_value,
    highest_stock_item,
    lowest_stock_item,
    average_item_price,
    median_item_price,
    total_units_in_stock,
    items_below_threshold,
    items_above_threshold,
    sort_by_stock_value,
)

BORDER = "=" * 64
DIVIDER = "-" * 64
RESTOCK_THRESHOLD = 50


def display_summary() -> None:
    """Print high-level inventory statistics."""
    print(f"\n{DIVIDER}")
    print("  Summary Statistics")
    print(DIVIDER)

    highest = highest_stock_item(inventory)
    lowest = lowest_stock_item(inventory)

    summary_rows = [
        ["Total Items", len(inventory)],
        ["Total Units in Stock", total_units_in_stock(inventory)],
        ["Total Stock Value", f"${total_stock_value(inventory):,.2f}"],
        ["Average Unit Price", f"${average_item_price(inventory):,.2f}"],
        ["Median Unit Price", f"${median_item_price(inventory):,.2f}"],
        [
            "Highest Value Item",
            f"{highest.item_name} (${highest.stock_value:,.2f})" if highest else "N/A",
        ],
        [
            "Lowest Value Item",
            f"{lowest.item_name} (${lowest.stock_value:,.2f})" if lowest else "N/A",
        ],
    ]
    print(tabulate(summary_rows, headers=["Metric", "Value"], tablefmt="fancy_grid"))


def display_full_inventory() -> None:
    """Print every item ranked by total stock value."""
    print(f"\n{DIVIDER}")
    print("  Inventory Ranked by Stock Value (Highest → Lowest)")
    print(DIVIDER)

    ranked = sort_by_stock_value(inventory)
    rows = [
        [rank, item.item_name, item.quantity, f"${item.price:.2f}", f"${item.stock_value:,.2f}"]
        for rank, item in enumerate(ranked, start=1)
    ]
    print(
        tabulate(
            rows,
            headers=["Rank", "Item Name", "Qty", "Unit Price", "Stock Value"],
            tablefmt="fancy_grid",
            colalign=("center", "left", "center", "right", "right"),
        )
    )


def display_restock_alerts() -> None:
    """Print items that fall below the restock threshold."""
    low_stock = items_below_threshold(inventory, RESTOCK_THRESHOLD)
    print(f"\n{DIVIDER}")
    print(f"  ⚠️  Low Stock Alert (below {RESTOCK_THRESHOLD} units)")
    print(DIVIDER)

    if low_stock:
        rows = [
            [item.item_name, item.quantity, f"${item.price:.2f}", f"${item.stock_value:,.2f}"]
            for item in low_stock
        ]
        print(
            tabulate(
                rows,
                headers=["Item Name", "Qty", "Unit Price", "Stock Value"],
                tablefmt="fancy_grid",
            )
        )
    else:
        print("  All items are adequately stocked.")


def display_well_stocked() -> None:
    """Print items that meet or exceed the restock threshold."""
    well_stocked = items_above_threshold(inventory, RESTOCK_THRESHOLD)
    print(f"\n{DIVIDER}")
    print(f"  ✅  Well Stocked Items ({RESTOCK_THRESHOLD}+ units)")
    print(DIVIDER)

    if well_stocked:
        rows = [
            [item.item_name, item.quantity, f"${item.price:.2f}", f"${item.stock_value:,.2f}"]
            for item in well_stocked
        ]
        print(
            tabulate(
                rows,
                headers=["Item Name", "Qty", "Unit Price", "Stock Value"],
                tablefmt="fancy_grid",
            )
        )
    else:
        print("  No items meet the threshold.")


def main() -> None:
    """Run the full inventory analysis report."""
    print(f"\n{BORDER}")
    print("        📦  INVENTORY STOCK ANALYSIS REPORT")
    print(BORDER)

    if not inventory:
        print("\n⚠️  Inventory is empty. Nothing to analyse.")
        print(BORDER)
        return

    display_summary()
    display_full_inventory()
    display_restock_alerts()
    display_well_stocked()

    print(f"\n{BORDER}")
    print("        ✅  Report Complete")
    print(f"{BORDER}\n")


if __name__ == "__main__":
    main()
