from model import (
    load_workers,
    load_orders,
    build_domains,
    is_valid_assignment
)


def backtrack(orders, domains, assignment, workers):
    """
    Backtracking search for a valid schedule.

    Returns:
        A complete assignment if one exists.
        None if no valid schedule can be found.
    """

    # Base case:
    # All orders have been assigned
    if len(assignment) == len(orders):
        return assignment.copy()

    # Find the next unassigned order
    current_order = None

    for order in orders:
        if order.order_id not in assignment:
            current_order = order
            break

    # Try every possible worker/time-slot assignment
    for option in domains[current_order.order_id]:

        if is_valid_assignment(
            current_order,
            option,
            assignment,
            workers
        ):
            # Choose
            assignment[current_order.order_id] = option

            # Explore
            result = backtrack(
                orders,
                domains,
                assignment,
                workers
            )

            # If successful, return the solution
            if result is not None:
                return result

            # Backtrack
            del assignment[current_order.order_id]

    # No option worked
    return None

def find_schedule(orders, domains, workers):
    """
    Find a complete schedule using backtracking.

    Returns:
        A dictionary containing the result of the scheduling process.
    """

    solution = backtrack(
        orders,
        domains,
        {},
        workers
    )

    if solution is not None:
        return {
            "success": True,
            "schedule": solution,
            "unassigned": []
        }

    # Find orders with no possible assignments
    unassigned = []

    for order in orders:
        if not domains[order.order_id]:
            unassigned.append(order.order_id)

    return {
        "success": False,
        "schedule": {},
        "unassigned": unassigned
    }

def find_schedule(orders, domains, workers):
    """
    Find a complete schedule.

    Returns a dictionary containing:
        success    -> whether all orders were scheduled
        schedule   -> successful assignments
        unassigned -> orders that could not be placed
    """

    solution = backtrack(
        orders,
        domains,
        {},
        workers
    )

    if solution is not None:
        return {
            "success": True,
            "schedule": solution,
            "unassigned": []
        }

    # Find orders that have no possible assignments
    unassigned = []

    for order in orders:
        if not domains[order.order_id]:
            unassigned.append(order.order_id)

    return {
        "success": False,
        "schedule": {},
        "unassigned": unassigned
    }


if __name__ == "__main__":

    workers = load_workers("../data/workers.csv")
    orders = load_orders("../data/orders.csv")

    domains = build_domains(orders, workers)

    result = find_schedule(
        orders,
        domains,
        workers
    )

    if result["success"]:

        print("Schedule found:")

        for order_id, assignment in result["schedule"].items():
            print(order_id, "->", assignment)

    else:

        print("Could not create a complete schedule.")

        if result["unassigned"]:
            print("Orders that cannot be placed:")

            for order_id in result["unassigned"]:
                print("-", order_id)

        else:
            print("The orders have possible assignments individually,")
            print("but their constraints conflict.")