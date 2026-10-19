import heapq

from .warehouse import (
    WAREHOUSE_GRID,
    CELL_SIZE_METERS,
    is_walkable,
    location_to_cell,
)

from .heuristics import manhattan_distance


DIRECTIONS = [
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1),   # right
]


def reconstruct_path(parent, goal):
    """
    Reconstruct the path from start to goal.
    """

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path


def greedy_best_first(grid, start, goal):
    """
    Greedy Best-First Search.

    Uses only the heuristic:

        f(n) = h(n)

    where h(n) is Manhattan distance to the goal.

    Returns:
        {
            "path": [...],
            "cost": ...,
            "nodes_expanded": ...
        }
    """

    # Check start and goal
    if not is_walkable(start):
        return {
            "path": [],
            "cost": float("inf"),
            "nodes_expanded": 0,
        }

    if not is_walkable(goal):
        return {
            "path": [],
            "cost": float("inf"),
            "nodes_expanded": 0,
        }

    if start == goal:
        return {
            "path": [start],
            "cost": 0,
            "nodes_expanded": 1,
        }

    # Priority queue:
    # (heuristic, tie_breaker, node)
    open_list = []

    counter = 0

    start_h = manhattan_distance(start, goal)

    heapq.heappush(
        open_list,
        (start_h, counter, start)
    )

    visited = {start}

    parent = {
        start: None
    }

    nodes_expanded = 0

    while open_list:

        _, _, current = heapq.heappop(open_list)

        nodes_expanded += 1

        # Goal reached
        if current == goal:

            path = reconstruct_path(
                parent,
                goal
            )

            cost = (len(path) - 1) * CELL_SIZE_METERS

            return {
                "path": path,
                "cost": cost,
                "nodes_expanded": nodes_expanded,
            }

        # Explore neighbours
        for dr, dc in DIRECTIONS:

            neighbour = (
                current[0] + dr,
                current[1] + dc,
            )

            if not is_walkable(neighbour):
                continue

            if neighbour in visited:
                continue

            visited.add(neighbour)

            parent[neighbour] = current

            counter += 1

            heuristic = manhattan_distance(
                neighbour,
                goal
            )

            heapq.heappush(
                open_list,
                (
                    heuristic,
                    counter,
                    neighbour
                )
            )

    # No route found
    return {
        "path": [],
        "cost": float("inf"),
        "nodes_expanded": nodes_expanded,
    }


def greedy_locations(start_location, goal_location):
    """
    Run Greedy Best-First Search using
    warehouse location names.

    Example:
        greedy_locations("P1", "S9")
    """

    start = location_to_cell(start_location)
    goal = location_to_cell(goal_location)

    return greedy_best_first(
        WAREHOUSE_GRID,
        start,
        goal,
    )