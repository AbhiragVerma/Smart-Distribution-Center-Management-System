import time

from .bfs import bfs_locations
from .astar import astar_locations
from .dfs import dfs_locations
from .dfs import iterative_deepening_locations
from .bidirectional import bidirectional_locations
from .greedy import greedy_locations


# -------------------------------------------------
# 10 warehouse location pairs
# -------------------------------------------------

LOCATION_PAIRS = [
    ("P1", "S1"),
    ("P1", "S2"),
    ("P1", "S3"),
    ("P1", "S4"),
    ("P1", "S5"),
    ("P1", "S6"),
    ("P1", "S7"),
    ("P1", "S8"),
    ("P1", "S9"),
    ("S1", "S9"),
]


# -------------------------------------------------
# Algorithms
# -------------------------------------------------

ALGORITHMS = {
    "BFS": bfs_locations,
    "DFS": dfs_locations,
    "Iterative Deepening": iterative_deepening_locations,
    "Bidirectional": bidirectional_locations,
    "Greedy Best-First": greedy_locations,
    "A*": astar_locations,
}


def run_algorithm(algorithm, start, goal):
    """
    Run one search algorithm and measure execution time.
    """

    function = ALGORITHMS[algorithm]

    start_time = time.perf_counter()

    result = function(start, goal)

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return {
        "cost": result["cost"],
        "nodes_expanded": result["nodes_expanded"],
        "time": execution_time,
    }


def compare_all():
    """
    Compare all six search algorithms
    across all ten location pairs.
    """

    results = []

    print("=" * 100)
    print("SEARCH ALGORITHM COMPARISON")
    print("=" * 100)

    for start, goal in LOCATION_PAIRS:

        print()
        print(f"Route: {start} -> {goal}")
        print("-" * 100)

        for algorithm in ALGORITHMS:

            result = run_algorithm(
                algorithm,
                start,
                goal
            )

            results.append({
                "start": start,
                "goal": goal,
                "algorithm": algorithm,
                "cost": result["cost"],
                "nodes_expanded": result["nodes_expanded"],
                "time": result["time"],
            })

            print(
                f"{algorithm:<22}"
                f" Cost: {result['cost']:<6} "
                f"Nodes: {result['nodes_expanded']:<6} "
                f"Time: {result['time']:.8f} sec"
            )

    return results


if __name__ == "__main__":
    compare_all()