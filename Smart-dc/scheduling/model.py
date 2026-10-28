import csv

LOCATION_TO_ZONE = {
    "S1": "A",
    "S2": "A",
    "S3": "A",
    "S4": "B",
    "S5": "B",
    "S6": "B",
    "S7": "C",
    "S8": "C",
    "S9": "C",
    "L01": "A",
    "L02": "A",
    "L03": "A",
    "L04": "A",
    "L05": "B",
    "L06": "B",
    "L07": "B",
    "L08": "B",
    "L09": "C",
    "L10": "C",
}


def load_inventory(filename):
    inventory = {}

    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            inventory[row["item_id"]] = row["location_id"]

    return inventory

class Order:
    def __init__(self, order_id, zones):
        self.order_id = order_id
        self.zones = set(zones)


class Worker:
    def __init__(self, worker_id, zones, available_slots):
        self.worker_id = worker_id
        self.zones = zones
        self.available_slots = available_slots


# def load_workers(filename):
#     """
#     Load scheduling worker information.

#     CSV format:
#     worker_id,allowed_zones,free_slots
#     W1,A|B,9-10|10-11
#     W2,B|C,10-11|11-12
#     W3,A|C,9-10|11-12
#     """

#     workers = []

#     with open(filename, newline="") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             zones = row["allowed_zones"].split("|")
#             slots = row["free_slots"].split("|")

#             workers.append(
#                 Worker(
#                     row["worker_id"],
#                     zones,
#                     slots
#                 )
#             )

#     return workers


def load_workers(filename):
    workers = []

    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            zones = [
                zone.strip()
                for zone in row["allowed_zones"].split("|")
                if zone.strip()
            ]

            slots = [
                slot.strip()
                for slot in row["free_slots"].split("|")
                if slot.strip()
            ]

            workers.append(
                Worker(row["worker_id"], zones, slots)
            )

    return workers



# def load_orders(filename):
#     """
#     Load scheduling orders.

#     CSV format:
#     order_id,zone
#     O1,A
#     O2,B
#     O3,C
#     """

#     orders = []

#     with open(filename, newline="") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             orders.append(
#                 Order(
#                     row["order_id"],
#                     row["zone"]
#                 )
#             )

#     return orders

# def load_workers(filename):
#     workers = []

#     with open(filename, newline="", encoding="utf-8-sig") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             worker = Worker(
#                 row["worker_id"],
#                 [row["zone"].replace("Zone-", "")],
#                 ["9-10", "10-11", "11-12"]
#                 if row["available"].strip().lower() == "true"
#                 else []
#             )

#             workers.append(worker)

#     return workers

def build_domains(orders, workers):
    domains = {}

    for order in orders:
        domains[order.order_id] = []

        for worker in workers:
            if not order.zones.issubset(set(worker.zones)):
                continue

            for slot in worker.available_slots:
                domains[order.order_id].append(
                    (worker.worker_id, slot)
                )

    return domains


def is_valid_assignment(order, assignment, current_schedule, workers):
    """
    Check zone, availability and worker/time-slot constraints.
    """

    worker_id, time_slot = assignment

    worker = None

    for w in workers:
        if w.worker_id == worker_id:
            worker = w
            break

    if worker is None:
        return False

    # Zone constraint
    if not order.zones.issubset(set(worker.zones)):
    
        return False

    # Availability constraint
    if time_slot not in worker.available_slots:
        return False

    # Same worker cannot handle two orders
    # in the same time slot.
    for assigned_assignment in current_schedule.values():

        assigned_worker, assigned_slot = assigned_assignment

        if (
            assigned_worker == worker_id
            and assigned_slot == time_slot
        ):
            return False

    return True

# def load_orders(filename):
#     orders = []

#     with open(filename, newline="", encoding="utf-8-sig") as file:
#         reader = csv.DictReader(file)

#         for index, row in enumerate(reader):
#             # Temporary zone assignment for testing the scheduling solver.
#             # The current orders.csv contains item IDs, not order zones.
#             zone = chr(ord("A") + index % 4)

#             order = Order(row["order_id"], zone)
#             orders.append(order)

#     return orders


# def load_orders(filename, inventory_filename="../data/inventory.csv"):
#     inventory = load_inventory(inventory_filename)
#     orders = []

#     with open(filename, newline="", encoding="utf-8-sig") as file:
#         reader = csv.DictReader(file)

#         for row in reader:
#             item_ids = row["item_ids"].split("|")
#             zones = set()

#             for item_id in item_ids:
#                 item_id = item_id.strip()

#                 if item_id not in inventory:
#                     raise ValueError(
#                         f"Item {item_id} not found in inventory"
#                     )

#                 location = inventory[item_id]

#                 if location not in LOCATION_TO_ZONE:
#                     raise ValueError(
#                         f"No zone mapping defined for location {location}"
#                     )

#                 zones.add(LOCATION_TO_ZONE[location])

#             orders.append(Order(row["order_id"], zones))

#     return orders


def load_orders(filename):
    orders = []

    with open(filename, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            zone = row["zone"].strip()
            order = Order(row["order_id"], [zone])
            orders.append(order)

    return orders


if __name__ == "__main__":

    workers = load_workers("../data/scheduling_workers.csv")
    orders = load_orders("../data/scheduling_orders.csv")

    domains = build_domains(orders, workers)

    for order_id, domain in domains.items():
        print(order_id, ":", domain)