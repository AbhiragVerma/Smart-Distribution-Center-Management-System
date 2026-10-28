
import time

from model import (
    load_workers,
    load_orders,
    build_domains
)

from solver import find_schedule
from solver_mrv import find_schedule_mrv


def run_comparison():
    workers = load_workers("../data/scheduling_workers.csv")
    orders = load_orders("../data/scheduling_orders.csv")
    domains = build_domains(orders, workers)

    # Plain backtracking
    start = time.perf_counter()

    plain_result = find_schedule(
        orders, domains, workers
    )

    plain_time = time.perf_counter() - start

    # MRV + forward checking
    start = time.perf_counter()

    mrv_result = find_schedule_mrv(
        orders, domains, workers
    )

    mrv_time = time.perf_counter() - start

    print("\n========== SCHEDULER COMPARISON ==========")

    print("\nPlain Backtracking")
    print("Success:", plain_result["success"])
    print("Backtracks:", plain_result["backtracks"])
    print(f"Execution time: {plain_time:.8f} seconds")

    print("\nMRV + Forward Checking")
    print("Success:", mrv_result["success"])
    print("Backtracks:", mrv_result["backtracks"])
    print(f"Execution time: {mrv_time:.8f} seconds")

    print("\n========== PERFORMANCE SUMMARY ==========")

    if plain_result["backtracks"] > 0:
        reduction = (
            (plain_result["backtracks"] -
             mrv_result["backtracks"])
            / plain_result["backtracks"]
        ) * 100

        print(f"Backtrack reduction: {reduction:.2f}%")
    else:
        print("Plain solver made no backtracking attempts.")

    if plain_time > 0:
        speedup = plain_time / max(mrv_time, 1e-12)
        print(f"Time speedup ratio: {speedup:.2f}x")

    print("\n==========================================")


if __name__ == "__main__":
    run_comparison()
