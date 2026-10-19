from model import (
    load_workers,
    load_orders,
    build_domains,
    is_valid_assignment
)


def backtrack(orders, domains, assignment, workers):
    """
    Backtracking search for a valid schedule.
    """

    # All orders assigned
    if len(assignment) == len(orders):
        return assignment.copy()

    # Select next unassigned order
    current_order = None

    for order in orders:
        if order.order_id not in assignment:
            current_order = order
            break

    # Try every possible assignment
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

            if result is not None:
                return result

            # Backtrack
            del assignment[current_order.order_id]

    return None


def find_schedule(orders, domains, workers):
    """
    Find a complete schedule using backtracking.
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

    # Orders having no possible assignments
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

    workers = load_workers("../data/scheduling_workers.csv")
    orders = load_orders("../data/scheduling_orders.csv")

    domains = build_domains(orders, workers)

    result = find_schedule(
        orders,
        domains,
        workers
    )

    if result["success"]:

        print("Schedule found:")

        for order_id, assignment in result["schedule"].items():
            print(
                order_id,
                "-> Worker:",
                assignment[0],
                ", Time:",
                assignment[1]
            )

    else:

        print("Could not create a complete schedule.")

        if result["unassigned"]:

            print("Orders that cannot be placed:")

            for order_id in result["unassigned"]:
                print("-", order_id)

        else:

            print(
                "The orders have possible assignments individually,"
            )
            print(
                "but their constraints conflict."
            )