from dataclasses import dataclass
from itertools import permutations

START = "P1"          # picking station: every tour starts here
END = "D1"            # dispatch area: every tour ends here
MAX_EXACT_ITEMS = 8   # 8! = 40,320 orders. Above this, use tsp_nearest.py


@dataclass
class PickingPlan:
    order: list           # full tour, for example ["P1", "S4", "S1", "D1"]
    cost: float           # total travel distance in metres
    orders_checked: int   # how many visiting orders were evaluated
    method: str           # "exact" or "nearest neighbour"


def unique_stops(item_locations, start=START, end=END):
    """Return the locations to visit, without repeats.

    Two items on the same shelf need only one visit. The start and end points
    are dropped because the tour passes through them anyway.
    """
    stops = []
    for location in item_locations:
        if location not in stops and location != start and location != end:
            stops.append(location)
    return stops


def build_distance_table(points, distance):
    """Call distance(a, b) once for every pair of points and store the result.

    `distance` is any function that returns the travel cost from a to b.
    In the full system this is the A* route cost from routing/astar.py.
    The table is stored per direction, so one-way aisles also work.
    """
    table = {}
    for a in points:
        for b in points:
            if a == b:
                table[(a, b)] = 0
                continue
            cost = distance(a, b)
            if cost is None or cost == float("inf"):
                raise ValueError(f"No route from {a} to {b}")
            table[(a, b)] = cost
    return table


def tour_cost(tour, table):
    """Add up the cost of every leg of the tour."""
    total = 0
    for a, b in zip(tour, tour[1:]):
        total += table[(a, b)]
    return total


def exact_picking_order(item_locations, distance, start=START, end=END):
    """Try every visiting order and return the cheapest one."""
    stops = unique_stops(item_locations, start, end)
    if len(stops) > MAX_EXACT_ITEMS:
        raise ValueError(
            f"{len(stops)} locations is too many for brute force "
            f"(limit {MAX_EXACT_ITEMS}). Use nearest_neighbour_order instead."
        )

    table = build_distance_table([start] + stops + [end], distance)

    best_tour = None
    best_cost = float("inf")
    checked = 0

    for middle in permutations(stops):
        tour = [start] + list(middle) + [end]
        cost = tour_cost(tour, table)
        checked += 1
        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return PickingPlan(best_tour, best_cost, checked, "exact")


def format_plan(plan):
    """One readable line per plan, used by the demos."""
    route = " -> ".join(plan.order)
    return (f"{plan.method:<18} {route}\n"
            f"{'':<18} cost = {plan.cost} m, orders checked = {plan.orders_checked}")

SAMPLE_COORDS = {
    "P1": (20, 0),
    "D1": (0, 0),
    "S1": (5, 10),
    "S2": (15, 10),
    "S3": (25, 10),
    "S4": (35, 10),
    "S5": (5, 25),
    "S6": (15, 25),
    "S7": (25, 25),
    "S8": (35, 25),
    "S9": (45, 25),
}


def sample_distance(a, b):
    (x1, y1), (x2, y2) = SAMPLE_COORDS[a], SAMPLE_COORDS[b]
    return abs(x1 - x2) + abs(y1 - y2)


if __name__ == "__main__":
    orders = {
        "ORD101": ["S2", "S4", "S7"],
        "ORD102": ["S1", "S3", "S4", "S6", "S9"],
        "ORD103": ["S5", "S5", "S8"],          # two items on the same shelf
    }
    for order_id, locations in orders.items():
        plan = exact_picking_order(locations, sample_distance)
        print(f"{order_id}  items at {locations}")
        print(format_plan(plan))
        print()