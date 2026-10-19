"""
Depth-First Search and Iterative Deepening Search
for warehouse routing.

DFS is used as an uninformed-search method.

Iterative Deepening Search (IDS) repeatedly applies
depth-limited DFS with increasing depth limits.
"""

from routing.warehouse import (
    is_walkable,
    CELL_SIZE_METERS,
    WAREHOUSE_GRID,
    location_to_cell
)


# Same movement order used by BFS and A*
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


def dfs(grid, start, goal):
    """
    Find a route from start to goal using Depth-First Search.

    Returns
    -------
    dictionary containing:

        path
        cost
        nodes_expanded
    """

    # Stack used by DFS
    stack = [start]

    # Keep track of visited cells
    visited = {start}

    # Store predecessor of each cell
    parent = {
        start: None
    }

    nodes_expanded = 0

    while stack:

        current = stack.pop()

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
        #
        # Reverse the order when adding to the stack
        # so DFS explores directions in the same order
        # as the other routing algorithms.
        for dr, dc in reversed(DIRECTIONS):

            next_cell = (
                current[0] + dr,
                current[1] + dc
            )

            # Skip obstacles and outside cells
            if not is_walkable(next_cell):
                continue

            # Skip already visited cells
            if next_cell in visited:
                continue

            visited.add(next_cell)

            parent[next_cell] = current

            stack.append(next_cell)

    # No route exists
    return {
        "path": None,
        "cost": None,
        "nodes_expanded": nodes_expanded
    }


def _depth_limited_dfs(
    start,
    goal,
    depth_limit
):
    """
    Perform one depth-limited DFS.

    This function is used internally by iterative
    deepening search.

    Returns
    -------
    found_path:
        The path if the goal is found, otherwise None.

    nodes_expanded:
        Number of nodes expanded during this iteration.

    cutoff:
        True if the search stopped because the
        depth limit was reached.
    """

    nodes_expanded = 0

    path = [start]

    # Prevent cycles on the current DFS path
    path_set = {start}

    def search(current, depth):

        nonlocal nodes_expanded

        nodes_expanded += 1

        # Goal test
        if current == goal:
            return path.copy(), False

        # Depth limit reached
        if depth == depth_limit:
            return None, True

        cutoff_occurred = False

        for dr, dc in DIRECTIONS:

            next_cell = (
                current[0] + dr,
                current[1] + dc
            )

            # Skip obstacles and outside cells
            if not is_walkable(next_cell):
                continue

            # Avoid cycles in the current path
            if next_cell in path_set:
                continue

            path.append(next_cell)
            path_set.add(next_cell)

            result, cutoff = search(
                next_cell,
                depth + 1
            )

            if result is not None:
                return result, False

            if cutoff:
                cutoff_occurred = True

            path.pop()
            path_set.remove(next_cell)

        return None, cutoff_occurred

    found_path, cutoff = search(
        start,
        0
    )

    return (
        found_path,
        nodes_expanded,
        cutoff
    )


def iterative_deepening(
    grid,
    start,
    goal,
    max_depth=None
):
    """
    Find a route using Iterative Deepening Search.

    IDS repeatedly performs depth-limited DFS:

        depth = 0
        depth = 1
        depth = 2
        ...

    until the goal is found.

    Returns
    -------
    dictionary containing:

        path
        cost
        nodes_expanded
    """

    # Maximum possible useful depth.
    #
    # The number of cells in the grid is a safe upper
    # bound for a simple path.
    if max_depth is None:

        max_depth = (
            len(grid)
            *
            len(grid[0])
        )

    total_nodes_expanded = 0

    for depth_limit in range(
        max_depth + 1
    ):

        (
            path,
            nodes_expanded,
            cutoff
        ) = _depth_limited_dfs(
            start,
            goal,
            depth_limit
        )

        total_nodes_expanded += nodes_expanded

        # Goal found
        if path is not None:

            cost = (
                len(path) - 1
            ) * CELL_SIZE_METERS

            return {
                "path": path,
                "cost": cost,
                "nodes_expanded": total_nodes_expanded
            }

        # No cutoff means the complete state space
        # was searched and the goal does not exist.
        if not cutoff:
            break

    # No route exists
    return {
        "path": None,
        "cost": None,
        "nodes_expanded": total_nodes_expanded
    }


def dfs_locations(
    start_location,
    goal_location
):
    """
    Convenience function for DFS using location names.

    Example:

        dfs_locations("P1", "S9")
    """

    start = location_to_cell(
        start_location
    )

    goal = location_to_cell(
        goal_location
    )

    return dfs(
        WAREHOUSE_GRID,
        start,
        goal
    )


def iterative_deepening_locations(
    start_location,
    goal_location
):
    """
    Convenience function for Iterative Deepening
    using warehouse location names.

    Example:

        iterative_deepening_locations("P1", "S9")
    """

    start = location_to_cell(
        start_location
    )

    goal = location_to_cell(
        goal_location
    )

    return iterative_deepening(
        WAREHOUSE_GRID,
        start,
        goal
    )