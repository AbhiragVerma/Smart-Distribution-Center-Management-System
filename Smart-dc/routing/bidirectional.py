from collections import deque

from .warehouse import (
    WAREHOUSE_GRID,
    CELL_SIZE_METERS,
    is_walkable,
    location_to_cell,
)


DIRECTIONS = [
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1),   # right
]


def reconstruct_path(parent_forward, parent_backward, meeting):
    """
    Reconstruct the complete path from start to goal
    using the meeting point of the two searches.
    """

    # Build start -> meeting path
    forward_path = []
    current = meeting

    while current is not None:
        forward_path.append(current)
        current = parent_forward.get(current)

    forward_path.reverse()

    # Build meeting -> goal path
    backward_path = []
    current = parent_backward.get(meeting)

    while current is not None:
        backward_path.append(current)
        current = parent_backward.get(current)

    return forward_path + backward_path


def _expand_layer(
    queue,
    visited,
    parent,
    other_visited,
):
    """
    Expand one complete BFS layer.

    Returns:
        meeting_node, nodes_expanded
    """

    layer_size = len(queue)
    nodes_expanded = 0

    for _ in range(layer_size):
        current = queue.popleft()
        nodes_expanded += 1

        for dr, dc in DIRECTIONS:
            neighbour = (
                current[0] + dr,
                current[1] + dc,
            )

            # Your warehouse.py uses is_walkable(cell),
            # not is_walkable(grid, cell).
            if not is_walkable(neighbour):
                continue

            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = current
            queue.append(neighbour)

            # The two searches have met.
            if neighbour in other_visited:
                return neighbour, nodes_expanded

    return None, nodes_expanded


def bidirectional(grid, start, goal):
    """
    Bidirectional BFS search.

    Searches simultaneously from the start and goal.

    Returns:
        {
            "path": [...],
            "cost": ...,
            "nodes_expanded": ...
        }
    """

    # Check whether start is valid.
    if not is_walkable(start):
        return {
            "path": [],
            "cost": float("inf"),
            "nodes_expanded": 0,
        }

    # Check whether goal is valid.
    if not is_walkable(goal):
        return {
            "path": [],
            "cost": float("inf"),
            "nodes_expanded": 0,
        }

    # Start and goal are the same location.
    if start == goal:
        return {
            "path": [start],
            "cost": 0,
            "nodes_expanded": 1,
        }

    # -------------------------------------------------
    # Forward BFS
    # -------------------------------------------------

    forward_queue = deque([start])
    forward_visited = {start}
    forward_parent = {
        start: None
    }

    # -------------------------------------------------
    # Backward BFS
    # -------------------------------------------------

    backward_queue = deque([goal])
    backward_visited = {goal}
    backward_parent = {
        goal: None
    }

    nodes_expanded = 0

    # -------------------------------------------------
    # Search from both directions
    # -------------------------------------------------

    while forward_queue and backward_queue:

        # Expand one layer from the START side.
        meeting, expanded = _expand_layer(
            forward_queue,
            forward_visited,
            forward_parent,
            backward_visited,
        )

        nodes_expanded += expanded

        if meeting is not None:
            path = reconstruct_path(
                forward_parent,
                backward_parent,
                meeting,
            )

            cost = (len(path) - 1) * CELL_SIZE_METERS

            return {
                "path": path,
                "cost": cost,
                "nodes_expanded": nodes_expanded,
            }

        # Expand one layer from the GOAL side.
        meeting, expanded = _expand_layer(
            backward_queue,
            backward_visited,
            backward_parent,
            forward_visited,
        )

        nodes_expanded += expanded

        if meeting is not None:
            path = reconstruct_path(
                forward_parent,
                backward_parent,
                meeting,
            )

            cost = (len(path) - 1) * CELL_SIZE_METERS

            return {
                "path": path,
                "cost": cost,
                "nodes_expanded": nodes_expanded,
            }

    # -------------------------------------------------
    # No route found
    # -------------------------------------------------

    return {
        "path": [],
        "cost": float("inf"),
        "nodes_expanded": nodes_expanded,
    }


def bidirectional_locations(start_location, goal_location):
    """
    Run bidirectional search using warehouse location names.

    Example:
        bidirectional_locations("P1", "S9")
    """

    start = location_to_cell(start_location)
    goal = location_to_cell(goal_location)

    return bidirectional(
        WAREHOUSE_GRID,
        start,
        goal,
    )