import csv
from pathlib import Path

from .models import Item, Worker, Order


def load_items(filename):
    items = {}

    with Path(filename).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            item = Item(
                item_id=row["item_id"].strip(),
                name=row["name"].strip(),
                location_id=row["location_id"].strip(),
                quantity=int(row["quantity"]),
            )

            items[item.item_id] = item

    return items


def load_workers(filename):
    workers = {}

    with Path(filename).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            worker = Worker(
                worker_id=row["worker_id"].strip(),
                name=row["name"].strip(),
                zone=row["zone"].strip(),
                available=row["available"].strip().lower() == "true",
            )

            workers[worker.worker_id] = worker

    return workers


def load_orders(filename):
    orders = {}

    with Path(filename).open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            item_ids = [
                item.strip()
                for item in row["item_ids"].split("|")
                if item.strip()
            ]

            order = Order(
                order_id=row["order_id"].strip(),
                item_ids=item_ids,
                status=row["status"].strip(),
            )

            orders[order.order_id] = order

    return orders


def find_item_location(items, item_id):
    item = items.get(item_id)

    if item is None:
        return None

    return item.location_id


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "data"

    items = load_items(data_dir / "inventory.csv")
    workers = load_workers(data_dir / "workers.csv")
    orders = load_orders(data_dir / "orders.csv")

    print("ITEMS")
    print("=" * 40)

    for item in items.values():
        print(
            f"{item.item_id}: "
            f"{item.name} -> {item.location_id}, "
            f"quantity={item.quantity}"
        )

    print("\nWORKERS")
    print("=" * 40)

    for worker in workers.values():
        print(
            f"{worker.worker_id}: "
            f"{worker.name}, "
            f"{worker.zone}, "
            f"available={worker.available}"
        )

    print("\nORDERS")
    print("=" * 40)

    for order in orders.values():
        print(
            f"{order.order_id}: "
            f"{order.item_ids}, "
            f"status={order.status}"
        )

    print("\nITEM LOCATION LOOKUP")
    print("=" * 40)

    item_id = "I003"
    location = find_item_location(items, item_id)

    print(f"{item_id} is stored at {location}")