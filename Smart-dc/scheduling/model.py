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
    Load scheduling worker information.

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

            workers.append(
                Worker(
                    row["worker_id"],
                    zones,
                    slots
                )
            )

    return workers


def load_orders(filename):
    """
    Load scheduling orders.

    CSV format:
    order_id,zone
    O1,A
    O2,B
    O3,C
    """

    orders = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            orders.append(
                Order(
                    row["order_id"],
                    row["zone"]
                )
            )

    return orders


def build_domains(orders, workers):
    """
    Build possible (worker, time-slot) assignments
    for every order.
    """

    domains = {}

    for order in orders:
        domains[order.order_id] = []

        for worker in workers:

            # Worker must be allowed in order's zone
            if order.zone not in worker.zones:
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
    if order.zone not in worker.zones:
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


if __name__ == "__main__":

    workers = load_workers("../data/scheduling_workers.csv")
    orders = load_orders("../data/scheduling_orders.csv")

    domains = build_domains(orders, workers)

    for order_id, domain in domains.items():
        print(order_id, ":", domain)