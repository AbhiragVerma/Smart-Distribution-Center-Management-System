"""Bayesian estimate that an item is on its shelf after a failed scan."""
def probability_item_on_shelf_after_failed_scan(
    prior_on_shelf=0.95,
    p_failed_scan_if_on_shelf=0.08,
    p_failed_scan_if_missing=0.90,
):
    """
    P(OnShelf | FailedScan) = P(Failed|OnShelf)P(OnShelf) /
      [P(Failed|OnShelf)P(OnShelf) + P(Failed|Missing)P(Missing)].
    Inputs are probabilities in [0, 1].
    """
    values = (prior_on_shelf, p_failed_scan_if_on_shelf, p_failed_scan_if_missing)
    if any(not 0 <= x <= 1 for x in values):
        raise ValueError("All probabilities must be between 0 and 1.")
    numerator = p_failed_scan_if_on_shelf * prior_on_shelf
    denominator = numerator + p_failed_scan_if_missing * (1 - prior_on_shelf)
    if denominator == 0:
        raise ValueError("Evidence has zero probability under the supplied model.")
    return numerator / denominator

def assess_scan(item_id, prior=0.95, failed_scan=True):
    if not failed_scan:
        return {"item_id": item_id, "status": "scan successful",
                "probability_on_shelf": prior}
    p = probability_item_on_shelf_after_failed_scan(prior)
    return {"item_id": item_id, "status": "failed scan",
            "probability_on_shelf": p,
            "recommendation": "verify manually" if p < 0.8 else "rescan item"}

if __name__ == "__main__":
    result = assess_scan("I001")
    print(f"Item: {result['item_id']}")
    print(f"Probability item is still on shelf after failed scan: "
          f"{result['probability_on_shelf']:.2%}")
    print("Recommendation:", result["recommendation"])
