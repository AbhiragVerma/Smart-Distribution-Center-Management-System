from copy import deepcopy
import time

from model import (
    load_workers,
    load_orders,
    build_domains,
    is_valid_assignment
)


def select_mrv_order(orders, domains, assignment, workers):
    """
    Select the unassigned order with the fewest
    currently valid assignments.
    """

    best_order = None
    best_options = None

    for order in orders:
        if order.order_id in assignment:
            continue

        # Keep only assignments that are currently valid
        valid_options = []

        for option in domains[order.order_id]:
            if is_valid_assignment(
                order,
                option,
                assignment,
                workers
            ):
                valid_options.append(option)

        # Minimum Remaining Values: choose the smallest domain
        if best_order is None or len(valid_options) < len(best_options):
            best_order = order
            best_options = valid_options

    return best_order, best_options


def forward_check(orders, domains, assignment, workers):
    """
    Remove invalid options from the domains of unassigned orders.

    Return False if any unassigned order has no valid options.
    """

    for order in orders:
        if order.order_id in assignment:
            continue

        remaining_options = []

        for option in domains[order.order_id]:
            if is_valid_assignment(
                order,
                option,
                assignment,
                workers
            ):
                remaining_options.append(option)

        domains[order.order_id] = remaining_options

        # An empty domain means this branch cannot succeed
        if not remaining_options:
            return False

    return True


def backtrack_mrv(orders, domains, assignment, workers, stats):
    """
    Solve the scheduling problem using MRV and forward checking.
    """

    # All orders have been assigned
    if len(assignment) == len(orders):
        return assignment.copy()

    # Select the order with the fewest valid options
    current_order, options = select_mrv_order(
        orders,
        domains,
        assignment,
        workers
    )

    # No valid option exists for this order
    if not options:
        stats["backtracks"] += 1
        return None

    # Try each valid assignment
    for option in options:

        assignment[current_order.order_id] = option

        # Copy domains so failed branches do not affect other branches
        new_domains = deepcopy(domains)

        # Apply forward checking
        if forward_check(
            orders,
            new_domains,
            assignment,
            workers
        ):

            result = backtrack_mrv(
                orders,
                new_domains,
                assignment,
                workers,
                stats
            )

            if result is not None:
                return result

        # Undo the assignment when the branch fails
        del assignment[current_order.order_id]

        stats["backtracks"] += 1

    return None


def find_schedule_mrv(orders, domains, workers):
    """
    Find a schedule using MRV and forward checking.
    """

    stats = {"backtracks": 0}

    solution = backtrack_mrv(
        orders,
        deepcopy(domains),
        {},
        workers,
        stats
    )

    if solution is not None:
        return {
            "success": True,
            "schedule": solution,
            "unassigned": [],
            "backtracks": stats["backtracks"]
        }

    # Identify orders that have no initial candidate assignments
    unassigned = [
        order.order_id
        for order in orders
        if not domains[order.order_id]
    ]

    return {
        "success": False,
        "schedule": {},
        "unassigned": unassigned,
        "backtracks": stats["backtracks"]
    }


if __name__ == "__main__":
    workers = load_workers("../data/scheduling_workers.csv")
    orders = load_orders("../data/scheduling_orders.csv")
    domains = build_domains(orders, workers)

    result = find_schedule_mrv(orders, domains, workers)

    if result["success"]:
        print("Schedule found using MRV + Forward Checking:\n")

        for order_id, assignment in result["schedule"].items():
            print(f"{order_id} -> {assignment}")
    else:
        print("No complete schedule could be found.")

        if result["unassigned"]:
            print("Orders with no initial assignments:")
            for order_id in result["unassigned"]:
                print("-", order_id)

    print("\nBacktracks:", result["backtracks"])