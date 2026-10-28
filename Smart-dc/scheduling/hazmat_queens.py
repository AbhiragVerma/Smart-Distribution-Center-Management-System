def is_safe(board, row, col, n):
    """
    Check whether a pallet can be placed safely
    at the given row and column.
    """

    # Check the same column in previous rows
    for i in range(row):
        if board[i] == col:
            return False

    # Check the upper-left diagonal
    i = row - 1
    j = col - 1

    while i >= 0 and j >= 0:
        if board[i] == j:
            return False

        i -= 1
        j -= 1

    # Check the upper-right diagonal
    i = row - 1
    j = col + 1

    while i >= 0 and j < n:
        if board[i] == j:
            return False

        i -= 1
        j += 1

    return True


def solve_queens(board, row, n):
    """
    Place one pallet in each row using backtracking.
    """

    # Base case: all pallets have been placed
    if row == n:
        return True

    # Try every column in the current row
    for col in range(n):

        if is_safe(board, row, col, n):

            # Place the pallet
            board[row] = col

            # Recursively place the next pallet
            if solve_queens(board, row + 1, n):
                return True

            # Backtrack: remove the pallet
            board[row] = -1

    return False


def print_board(board, n):
    """
    Display the rack and pallet positions.
    """

    for row in range(n):
        for col in range(n):
            if board[row] == col:
                print(" Q ", end="")
            else:
                print(" . ", end="")

        print()


def solve_hazmat_queens(n):
    """
    Solve the hazardous-pallet placement problem.
    """

    if n < 1:
        print("Rack size must be at least 1.")
        return

    board = [-1] * n

    print(f"\nHazardous-Pallet Placement: {n}x{n} Rack")

    if solve_queens(board, 0, n):
        print("\nSafe pallet arrangement found:\n")
        print_board(board, n)
    else:
        print(f"\nNo valid arrangement exists for N = {n}.")


if __name__ == "__main__":
    n = int(input("Enter rack size N: "))
    solve_hazmat_queens(n)