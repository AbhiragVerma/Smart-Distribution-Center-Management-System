from collections import deque


def is_valid_state(state, total_workers, total_robots):
    """
    Check whether a state satisfies the safety constraints.

    State format:
    (workers_left, robots_left, lift_position)

    Lift position:
    0 = Left floor
    1 = Right floor
    """

    workers_left, robots_left, lift_position = state

    workers_right = total_workers - workers_left
    robots_right = total_robots - robots_left

    # Counts must remain within valid limits
    if not (0 <= workers_left <= total_workers):
        return False

    if not (0 <= robots_left <= total_robots):
        return False

    # Check the left floor
    if workers_left > 0 and robots_left > workers_left:
        return False

    # Check the right floor
    if workers_right > 0 and robots_right > workers_right:
        return False

    return True


def get_next_states(state, total_workers, total_robots):
    """
    Generate all valid states reachable in one lift journey.
    """

    workers_left, robots_left, lift_position = state

    # The lift can carry one or two people
    possible_moves = [
        (1, 0),  # One worker
        (2, 0),  # Two workers
        (0, 1),  # One robot
        (0, 2),  # Two robots
        (1, 1)   # One worker and one robot
    ]

    next_states = []

    for workers, robots in possible_moves:

        if lift_position == 0:
            # Move people from left to right
            new_state = (
                workers_left - workers,
                robots_left - robots,
                1
            )

        else:
            # Move people from right to left
            new_state = (
                workers_left + workers,
                robots_left + robots,
                0
            )

        # Validate the state and lift capacity
        if workers + robots > 2:
            continue

        if is_valid_state(
            new_state,
            total_workers,
            total_robots
        ):
            next_states.append(
                (new_state, workers, robots)
            )

    return next_states


def solve_lift_transfer(total_workers=3, total_robots=3):
    """
    Find the minimum number of lift journeys using BFS.
    """

    start = (total_workers, total_robots, 0)
    goal = (0, 0, 1)

    if not is_valid_state(start, total_workers, total_robots):
        print("The initial state is invalid.")
        return

    if not is_valid_state(goal, total_workers, total_robots):
        print("The goal state is invalid.")
        return

    # Queue entries contain the current state and its path
    queue = deque([(start, [])])

    # Prevent revisiting states
    visited = {start}

    while queue:

        current_state, path = queue.popleft()

        # Check whether everyone reached the right floor
        if current_state == goal:
            print("\nLift Transfer Solution")
            print("----------------------")
            print(f"Minimum lift journeys: {len(path)}")
            print()

            print(
                f"Start: {total_workers} workers and "
                f"{total_robots} robots on the left floor."
            )

            for step, move in enumerate(path, start=1):
                workers, robots, direction = move

                if direction == 0:
                    destination = "Left -> Right"
                else:
                    destination = "Right -> Left"

                print(
                    f"Journey {step}: {workers} worker(s), "
                    f"{robots} robot(s), {destination}"
                )

            print("\nAll workers and robots reached the right floor.")
            return

        # Explore all valid next states
        for next_state, workers, robots in get_next_states(
            current_state,
            total_workers,
            total_robots
        ):

            if next_state not in visited:
                visited.add(next_state)

                # Store the journey with the path
                direction = current_state[2]

                new_path = path + [
                    (workers, robots, direction)
                ]

                queue.append((next_state, new_path))

    print("No valid solution exists for these numbers.")


if __name__ == "__main__":
    solve_lift_transfer(3, 3)