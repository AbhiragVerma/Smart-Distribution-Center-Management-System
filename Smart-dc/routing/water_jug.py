from collections import deque


def get_next_states(state, capacity_a, capacity_b):
    """
    Generate all possible states from the current state.

    State format:
        (amount_in_jug_A, amount_in_jug_B)
    """

    a, b = state

    states = []

    # 1. Fill Jug A
    states.append(
        ((capacity_a, b), "Fill Jug A")
    )

    # 2. Fill Jug B
    states.append(
        ((a, capacity_b), "Fill Jug B")
    )

    # 3. Empty Jug A
    states.append(
        ((0, b), "Empty Jug A")
    )

    # 4. Empty Jug B
    states.append(
        ((a, 0), "Empty Jug B")
    )

    # 5. Pour Jug A -> Jug B
    transfer = min(a, capacity_b - b)

    states.append(
        (
            (a - transfer, b + transfer),
            "Pour Jug A -> Jug B"
        )
    )

    # 6. Pour Jug B -> Jug A
    transfer = min(b, capacity_a - a)

    states.append(
        (
            (a + transfer, b - transfer),
            "Pour Jug B -> Jug A"
        )
    )

    return states


def water_jug_bfs(capacity_a, capacity_b, target):
    """
    Solve the Water-Jug Problem using BFS.

    Parameters:
        capacity_a: Capacity of Jug A
        capacity_b: Capacity of Jug B
        target: Required quantity

    Returns:
        {
            "path": [...],
            "steps": ...,
            "nodes_expanded": ...
        }
    """

    # Target must be possible in at least one jug.
    if target > max(capacity_a, capacity_b):
        return {
            "path": [],
            "steps": -1,
            "nodes_expanded": 0,
        }

    start = (0, 0)

    queue = deque([start])

    visited = {start}

    parent = {
        start: None
    }

    action = {}

    nodes_expanded = 0

    while queue:

        current = queue.popleft()

        nodes_expanded += 1

        a, b = current

        # Goal condition:
        # exact target exists in either jug.
        if a == target or b == target:

            path = []

            state = current

            while state is not None:

                path.append(
                    (
                        state,
                        action.get(state, "Start")
                    )
                )

                state = parent[state]

            path.reverse()

            return {
                "path": path,
                "steps": len(path) - 1,
                "nodes_expanded": nodes_expanded,
            }

        # Generate next states
        for next_state, next_action in get_next_states(
            current,
            capacity_a,
            capacity_b
        ):

            if next_state in visited:
                continue

            visited.add(next_state)

            parent[next_state] = current

            action[next_state] = next_action

            queue.append(next_state)

    # No solution exists.
    return {
        "path": [],
        "steps": -1,
        "nodes_expanded": nodes_expanded,
    }


def print_solution(capacity_a, capacity_b, target):
    """
    Print a readable Water-Jug BFS solution.
    """

    result = water_jug_bfs(
        capacity_a,
        capacity_b,
        target
    )

    print("=" * 60)
    print("WATER-JUG PROBLEM USING BFS")
    print("=" * 60)

    print(f"Jug A capacity : {capacity_a}")
    print(f"Jug B capacity : {capacity_b}")
    print(f"Target quantity : {target}")
    print()

    if not result["path"]:
        print("No solution exists.")
        print(f"Nodes expanded: {result['nodes_expanded']}")
        return

    print("Solution:")
    print("-" * 60)

    for number, (state, action) in enumerate(
        result["path"]
    ):
        print(
            f"Step {number}: "
            f"{action:<25} "
            f"State = {state}"
        )

    print("-" * 60)

    print(f"Total steps: {result['steps']}")
    print(
        f"Nodes expanded: "
        f"{result['nodes_expanded']}"
    )


if __name__ == "__main__":

    # Example:
    # 4-liter jug + 3-liter jug
    # Measure exactly 2 liters.
    print_solution(
        4,
        3,
        2
    )