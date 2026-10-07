import csv


class Order:
    def __init__(self, order_id, zone):
        self.order_id = order_id
        self.zone = zone


class Worker:
    def __init__(self, worker_id, zones, available_slots):
        self.worker_id = worker_id
        self.zones = zones
        self.available_slots = available_slots


def load_workers(filename):
    """
    Load worker information from workers.csv.

    CSV format:
    worker_id,allowed_zones,free_slots
    W1,A|B,9-10|10-11
    W2,B|C,10-11|11-12
    W3,A|C,9-10|11-12
    """

    workers = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            zones = row["allowed_zones"].split("|")
            slots = row["free_slots"].split("|")

            worker = Worker(
                row["worker_id"],
                zones,
                slots
            )

            workers.append(worker)

    return workers

def load_orders(filename):
    orders = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            order = Order(
                row["order_id"],
                row["zone"]
            )

            orders.append(order)

    return orders


def build_domains(orders, workers):
    """
    Build the domain of possible assignments for every order.

    Each domain value is:
        (worker_id, time_slot)

    A worker can be included only if they are
    allowed to work in the order's zone.
    """

    domains = {}

    for order in orders:
        domains[order.order_id] = []

        for worker in workers:

            # Zone constraint
            if order.zone not in worker.zones:
                continue

            # Add every available time slot
            for slot in worker.available_slots:
                domains[order.order_id].append(
                    (worker.worker_id, slot)
                )

    return domains


def is_valid_assignment(order, assignment, current_schedule, workers):
    """
    Check whether an assignment is valid.

    Conditions:
    1. Worker must be allowed to work in the order's zone.
    2. Worker must actually be available in that time slot.
    3. Worker cannot handle two orders in the same time slot.
    """

    worker_id, time_slot = assignment

    # Find the worker
    worker = None

    for w in workers:
        if w.worker_id == worker_id:
            worker = w
            break

    # Worker does not exist
    if worker is None:
        return False

    # Zone constraint
    if order.zone not in worker.zones:
        return False

    # Availability constraint
    if time_slot not in worker.available_slots:
        return False

    # Worker cannot handle two orders simultaneously
    for assigned_order, assigned_assignment in current_schedule.items():

        assigned_worker, assigned_slot = assigned_assignment

        if assigned_worker == worker_id and assigned_slot == time_slot:
            return False

    return True

if __name__ == "__main__":

    workers = load_workers("../data/workers.csv")

    orders = [
        Order("O1", "A"),
        Order("O2", "B"),
        Order("O3", "C")
    ]

    domains = build_domains(orders, workers)

    for order_id, domain in domains.items():
        print(order_id, ":", domain)