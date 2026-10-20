"""Combine RFID and barcode evidence using Dempster-Shafer theory.

Frame of discernment: {ON_SHELF, NOT_ON_SHELF}.
Each sensor provides basic probability assignments (mass) to:
ON_SHELF, NOT_ON_SHELF, and UNKNOWN (ignorance).
"""
def combine_evidence(rfid, barcode):
    """
    Each evidence argument is a dict with keys:
      on_shelf, not_on_shelf, unknown
    Values must be non-negative and sum to 1.
    Returns combined masses and conflict K.
    """
    def validate(m, name):
        required = {"on_shelf", "not_on_shelf", "unknown"}
        if set(m) != required:
            raise ValueError(f"{name} must contain exactly {sorted(required)}")
        if any(v < 0 or v > 1 for v in m.values()):
            raise ValueError(f"{name} masses must be between 0 and 1")
        if abs(sum(m.values()) - 1.0) > 1e-9:
            raise ValueError(f"{name} masses must sum to 1")

    validate(rfid, "RFID")
    validate(barcode, "Barcode")
    a, b = rfid, barcode
    # Conflict is support for mutually exclusive singletons.
    conflict = a["on_shelf"] * b["not_on_shelf"] + a["not_on_shelf"] * b["on_shelf"]
    if 1 - conflict <= 1e-12:
        raise ValueError("Evidence is totally conflicting; Dempster's rule is undefined.")
    denom = 1 - conflict
    on = (a["on_shelf"] * b["on_shelf"] +
          a["on_shelf"] * b["unknown"] +
          a["unknown"] * b["on_shelf"]) / denom
    off = (a["not_on_shelf"] * b["not_on_shelf"] +
           a["not_on_shelf"] * b["unknown"] +
           a["unknown"] * b["not_on_shelf"]) / denom
    unknown = (a["unknown"] * b["unknown"]) / denom
    return {"on_shelf": on, "not_on_shelf": off, "unknown": unknown,
            "conflict": conflict}

if __name__ == "__main__":
    rfid = {"on_shelf": 0.70, "not_on_shelf": 0.10, "unknown": 0.20}
    barcode = {"on_shelf": 0.60, "not_on_shelf": 0.15, "unknown": 0.25}
    result = combine_evidence(rfid, barcode)
    print("Combined RFID + barcode evidence")
    for key, value in result.items():
        print(f"{key}: {value:.3f}")
