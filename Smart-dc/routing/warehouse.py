"""
Warehouse representation for the Smart Distribution Center.

The warehouse is represented as a grid.

Each cell represents 5 metres.

'.' = free aisle / walkable location
'#' = blocked location / obstacle

Named locations:
    P1 = picking station
    D1 = dispatch area
    S1-S9 = storage locations
"""

CELL_SIZE_METERS = 5

# -------------------------------------------------------------------
# Warehouse map
# -------------------------------------------------------------------
#
# 6 rows x 10 columns
#
# '.' = walkable
# '#' = blocked
#
# The storage locations are placed on open cells.
# -------------------------------------------------------------------

WAREHOUSE_GRID = [
    list(".........."),
    list(".#..#..#.."),
    list(".........."),
    list(".#..#..#.."),
    list("..#...#..."),
    list("..........")
]


# -------------------------------------------------------------------
# Location coordinates
# -------------------------------------------------------------------
#
# Coordinates are based on the coordinates already used by the
# project's TSP module.
#
# Format:
#     location: (x, y)
#
# The routing grid uses:
#     (row, column) = (y / 5, x / 5)
# -------------------------------------------------------------------

LOCATION_COORDINATES = {

    # Picking station
    "P1": (20, 0),

    # Dispatch area
    "D1": (0, 0),

    # Storage locations
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


def location_to_cell(location):
    """
    Convert a warehouse location name into a grid cell.

    Example:

        S1 = (5, 10)

        becomes:

        (row=2, column=1)
    """

    if location not in LOCATION_COORDINATES:
        raise ValueError(
            f"Unknown warehouse location: {location}"
        )

    x, y = LOCATION_COORDINATES[location]

    row = y // CELL_SIZE_METERS
    column = x // CELL_SIZE_METERS

    return row, column


def cell_to_location(cell):
    """
    Convert a grid cell into a warehouse location name.

    Returns None if the cell is not a named location.
    """

    for location in LOCATION_COORDINATES:

        if location_to_cell(location) == cell:
            return location

    return None


def is_valid_cell(cell):
    """
    Check whether a grid cell is inside the warehouse.
    """

    row, column = cell

    rows = len(WAREHOUSE_GRID)
    columns = len(WAREHOUSE_GRID[0])

    return (
        0 <= row < rows
        and
        0 <= column < columns
    )


def is_walkable(cell):
    """
    Check whether a warehouse cell can be traversed.
    """

    if not is_valid_cell(cell):
        return False

    row, column = cell

    return WAREHOUSE_GRID[row][column] != "#"


def print_warehouse(path=None, start=None, goal=None):
    """
    Print the warehouse grid.

    If a path is supplied:
        '*' represents the calculated route.

    S = start
    G = goal
    # = obstacle
    . = free space
    """

    display = [
        row.copy()
        for row in WAREHOUSE_GRID
    ]

    if path:

        for cell in path:

            row, column = cell

            if display[row][column] == ".":
                display[row][column] = "*"

    if start is not None:

        row, column = start
        display[row][column] = "S"

    if goal is not None:

        row, column = goal
        display[row][column] = "G"

    print()

    for row in display:

        print(" ".join(row))

    print()


if __name__ == "__main__":

    print("Warehouse locations:")

    for location in LOCATION_COORDINATES:

        print(
            f"{location}: "
            f"{location_to_cell(location)}"
        )

    print()

    print_warehouse()