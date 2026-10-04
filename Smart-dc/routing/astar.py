"""
A* search for warehouse routing.

A* is the main cost-aware routing algorithm of the project.

Formula:

    f(n) = g(n) + h(n)

where:

    g(n) = actual cost from start to n
    h(n) = estimated cost from n to goal
"""

import heapq

from routing.heuristics import manhattan_distance

from routing.warehouse import (
    is_walkable,
    CELL_SIZE_METERS
)


DIRECTIONS = [
    (-1, 0),   # Up
    (1, 0),    # Down
    (0, -1),   # Left
    (0, 1)     # Right
]


def reconstruct_path(parent, goal):
    """
    Reconstruct the final route.
    """

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path


def astar(grid, start, goal):
    """
    Find a least-cost route using A*.

    Parameters
    ----------
    grid:
        Warehouse grid.

    start:
        Starting cell.

    goal:
        Destination cell.

    Returns
    -------
    dictionary containing:

        path
        cost
        nodes_expanded
    """

    # Priority queue.
    #
    # Each entry:
    #
    # (f_cost, g_cost, cell)
    #
    # f(n) = g(n) + h(n)
    open_list = []

    start_g = 0

    start_h = manhattan_distance(
        start,
        goal
    )

    start_f = start_g + start_h

    heapq.heappush(
        open_list,
        (
            start_f,
            start_g,
            start
        )
    )

    # Actual cost from start to each cell
    g_cost = {
        start: 0
    }

    # Used for reconstructing the final route
    parent = {
        start: None
    }

    nodes_expanded = 0

    while open_list:

        f_cost, current_g, current = heapq.heappop(
            open_list
        )

        # Ignore an outdated queue entry.
        #
        # This can happen when a better route to the
        # same cell is discovered later.
        if current_g != g_cost.get(current):
            continue

        nodes_expanded += 1

        # Goal test
        if current == goal:

            path = reconstruct_path(
                parent,
                goal
            )

            return {
                "path": path,
                "cost": g_cost[goal],
                "nodes_expanded": nodes_expanded
            }

        # Generate successor states
        for dr, dc in DIRECTIONS:

            next_cell = (
                current[0] + dr,
                current[1] + dc
            )

            # Skip obstacles and outside cells
            if not is_walkable(next_cell):
                continue

            # Every movement costs one grid cell = 5 metres
            movement_cost = CELL_SIZE_METERS

            new_g = (
                current_g
                +
                movement_cost
            )

            # Check whether this route is better
            if (
                next_cell not in g_cost
                or
                new_g < g_cost[next_cell]
            ):

                g_cost[next_cell] = new_g

                h = manhattan_distance(
                    next_cell,
                    goal
                )

                f = new_g + h

                parent[next_cell] = current

                heapq.heappush(
                    open_list,
                    (
                        f,
                        new_g,
                        next_cell
                    )
                )

    # No route exists
    return {
        "path": None,
        "cost": None,
        "nodes_expanded": nodes_expanded
    }


def astar_locations(start_location, goal_location):
    """
    Convenience function.

    Allows A* to be called using location names:

        P1
        S1
        S2
        D1
    """

    from routing.warehouse import (
        WAREHOUSE_GRID,
        location_to_cell
    )

    start = location_to_cell(
        start_location
    )

    goal = location_to_cell(
        goal_location
    )

    return astar(
        WAREHOUSE_GRID,
        start,
        goal
    )


def astar_distance(start_location, goal_location):
    """
    Return only the A* travel cost.

    This function is designed specifically to plug into
    the existing TSP code.

    Example:

        exact_picking_order(
            ["S2", "S4", "S7"],
            astar_distance
        )
    """

    result = astar_locations(
        start_location,
        goal_location
    )

    if result["cost"] is None:

        return float("inf")

    return result["cost"]