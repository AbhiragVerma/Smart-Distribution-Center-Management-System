"""
Nearest-neighbour picking order for larger orders.

Brute force becomes too slow when an order has many item locations
(10 locations already means 3,628,800 visiting orders). This file uses a
heuristic instead: from the current location, always walk to the closest
location that has not been visited yet. It is fast, but the result is not
always the cheapest order.

Syllabus topics: Module 2 - Travelling Salesperson Problem,
                 Module 1 - Heuristic.

Run on its own:   python picking/tsp_nearest.py
"""

try:                                   # imported as part of the project
    from picking.tsp_exact import (START, END, MAX_EXACT_ITEMS, PickingPlan,
                                   unique_stops, build_distance_table,
                                   tour_cost, exact_picking_order, format_plan,
                                   sample_distance)
except ImportError:                    # run directly from the picking/ folder
    from tsp_exact import (START, END, MAX_EXACT_ITEMS, PickingPlan,
                           unique_stops, build_distance_table,
                           tour_cost, exact_picking_order, format_plan,
                           sample_distance)


def nearest_neighbour_order(item_locations, distance, start=START, end=END):
    """Build a tour by always moving to the closest unvisited location."""
    stops = unique_stops(item_locations, start, end)
    table = build_distance_table([start] + stops + [end], distance)

    tour = [start]
    current = start
    remaining = list(stops)

    while remaining:
        # Closest location first. Ties are broken by name so the result is
        # the same on every run.
        nearest = min(remaining, key=lambda stop: (table[(current, stop)], stop))
        tour.append(nearest)
        remaining.remove(nearest)
        current = nearest

    tour.append(end)
    return PickingPlan(tour, tour_cost(tour, table), 1, "nearest neighbour")


def plan_picking(item_locations, distance, start=START, end=END):
    """Entry point for the rest of the system.

    Small orders get the exact answer. Larger orders use the heuristic.
    """
    stops = unique_stops(item_locations, start, end)
    if len(stops) <= MAX_EXACT_ITEMS:
        return exact_picking_order(item_locations, distance, start, end)
    return nearest_neighbour_order(item_locations, distance, start, end)


def compare(item_locations, distance, start=START, end=END):
    """Run both methods on the same order and return (exact, nearest, extra %)."""
    exact = exact_picking_order(item_locations, distance, start, end)
    nearest = nearest_neighbour_order(item_locations, distance, start, end)
    extra = 0.0
    if exact.cost > 0:
        extra = (nearest.cost - exact.cost) / exact.cost * 100
    return exact, nearest, extra


if __name__ == "__main__":
    orders = {
        "ORD101": ["S2", "S4", "S7"],
        "ORD102": ["S1", "S3", "S4", "S6", "S9"],
        "ORD103": ["S5", "S5", "S8"],
    }
    for order_id, locations in orders.items():
        exact, nearest, extra = compare(locations, sample_distance)
        print(f"{order_id}  items at {locations}")
        print(format_plan(exact))
        print(format_plan(nearest))
        print(f"{'':<18} nearest neighbour walks {extra:.1f}% further than the best order")
        print()

    big_order = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]
    plan = plan_picking(big_order, sample_distance)
    print(f"ORD104  items at {big_order}")
    print(f"{len(big_order)} locations is above the brute-force limit of "
          f"{MAX_EXACT_ITEMS}, so plan_picking uses the heuristic:")
    print(format_plan(plan))