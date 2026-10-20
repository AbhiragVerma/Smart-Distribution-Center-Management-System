"""Validate Aashini's required sample data before running the demos."""
import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
from warehouse.graph import load_warehouse
from warehouse.records import load_items, load_workers

DATA = BASE / "data"

def main():
    graph = load_warehouse(DATA / "warehouse.txt")
    items = load_items(DATA / "inventory.csv")
    workers = load_workers(DATA / "workers.csv")
    with (DATA / "test_orders.csv").open(newline="", encoding="utf-8-sig") as f:
        orders = list(csv.DictReader(f))

    errors = []
    if len(graph.locations) < 30:
        errors.append(f"Expected 30+ locations, found {len(graph.locations)}")
    if len(items) < 20:
        errors.append(f"Expected 20+ inventory items, found {len(items)}")
    if len(workers) < 6:
        errors.append(f"Expected 6+ workers, found {len(workers)}")
    if len(orders) != 10:
        errors.append(f"Expected 10 test orders, found {len(orders)}")
    for item in items.values():
        if item.location_id not in graph.locations:
            errors.append(f"{item.item_id} references missing location {item.location_id}")
    for order in orders:
        for item_id in order["item_ids"].split("|"):
            if item_id and item_id not in items:
                errors.append(f"{order['order_id']} references missing item {item_id}")

    if errors:
        print("DATA LOADER CHECK: FAILED")
        for error in errors:
            print(" -", error)
        raise SystemExit(1)
    print("DATA LOADER CHECK: PASSED")
    print(f"Locations: {len(graph.locations)}")
    print(f"Inventory items: {len(items)}")
    print(f"Workers: {len(workers)}")
    print(f"Test orders: {len(orders)}")
    print("All inventory locations and test-order item IDs are valid.")

if __name__ == "__main__":
    main()
