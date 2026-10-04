"""
Breadth-First Search for warehouse routing.

BFS is used as the uninformed-search baseline for the project.
"""

from collections import deque

from routing.warehouse import (
    is_walkable,
    CELL_SIZE_METERS
)


# Four possible warehouse movements
DIRECTIONS = [
    (-1, 0),   # Up
    (1, 0),    # Down
    (0, -1),   # Left
    (0, 1)     # Right
]


def reconstruct_path(parent, goal):
    """
    Reconstruct the route from the parent dictionary.
    """

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path


def bfs(grid, start, goal):
    """
    Find a route from start to goal using BFS.

    Parameters
    ----------
    grid:
        Warehouse grid.

    start:
        Starting cell (row, column).

    goal:
        Destination cell (row, column).

    Returns
    -------
    dictionary containing:

        path
        cost
        nodes_expanded
    """

    # Queue used by BFS
    queue = deque()

    queue.append(start)

    # Keep track of visited states
    visited = {start}

    # Store the predecessor of every state
    parent = {
        start: None
    }

    nodes_expanded = 0

    while queue:

        current = queue.popleft()

        nodes_expanded += 1

        # Goal test
        if current == goal:

            path = reconstruct_path(
                parent,
                goal
            )

            cost = (
                len(path) - 1
            ) * CELL_SIZE_METERS

            return {
                "path": path,
                "cost": cost,
                "nodes_expanded": nodes_expanded
            }

        # Generate successor states
        for dr, dc in DIRECTIONS:

            next_cell = (
                current[0] + dr,
                current[1] + dc
            )

            # Check whether the cell is inside
            # the warehouse and walkable.
            #
            # We use the imported warehouse function
            # because the routing grid follows the
            # project's warehouse representation.
            if not is_walkable(next_cell):
                continue

            # Skip already visited states
            if next_cell in visited:
                continue

            visited.add(next_cell)

            parent[next_cell] = current

            queue.append(next_cell)

    # No route exists
    return {
        "path": None,
        "cost": None,
        "nodes_expanded": nodes_expanded
    }


def bfs_locations(start_location, goal_location):
    """
    Convenience function.

    Allows BFS to be called using warehouse names
    such as P1, S1, S2 and D1.
    """

    from routing.warehouse import (
        WAREHOUSE_GRID,
        location_to_cell
    )

    start = location_to_cell(start_location)
    goal = location_to_cell(goal_location)

    return bfs(
        WAREHOUSE_GRID,
        start,
        goal
    )