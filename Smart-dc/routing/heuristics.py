"""
Heuristic functions used by the routing algorithms.
"""

from routing.warehouse import CELL_SIZE_METERS


def manhattan_distance(current, goal):
    """
    Calculate Manhattan distance between two grid cells.

    Manhattan distance:

        h(n) = |row1-row2| + |column1-column2|

    Since each grid cell represents 5 metres, the result is
    converted into metres.
    """

    row1, col1 = current
    row2, col2 = goal

    distance_in_cells = (
        abs(row1 - row2)
        +
        abs(col1 - col2)
    )

    return distance_in_cells * CELL_SIZE_METERS