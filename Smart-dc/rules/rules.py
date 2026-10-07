class Rule:
    """
    Represents a simple IF-THEN rule.

    condition:
        A function that receives the current facts
        and returns True or False.

    action:
        A function that receives the current facts
        and returns new facts when the rule fires.
    """

    def __init__(self, name, condition, action):
        self.name = name
        self.condition = condition
        self.action = action

    def evaluate(self, facts):
        """
        Evaluate the rule against the current facts.

        Returns:
            Dictionary containing newly generated facts
            if the rule fires, otherwise None.
        """

        if self.condition(facts):
            return self.action(facts)

        return None


# RULE 1: ORDER PRIORITY

def priority_condition(facts):
    """
    IF the order is marked as urgent
    THEN it should receive high priority.
    """

    return facts.get("urgent", False) is True


def priority_action(facts):
    """
    Set the order priority to HIGH.
    """

    return {
        "priority": "HIGH"
    }



# RULE 2: STOCK HOLD


def stock_hold_condition(facts):
    """
    IF available stock is less than the required quantity
    THEN the order should be placed on stock hold.
    """

    stock = facts.get("stock")
    required_quantity = facts.get("required_quantity")

    # Do not fire if required information is missing.
    if stock is None or required_quantity is None:
        return False

    return stock < required_quantity


def stock_hold_action(facts):
    """
    Place the order on stock hold.
    """

    return {
        "stock_hold": True
    }



# RULE 3: REORDER ALERT


def reorder_condition(facts):
    """
    IF current stock is at or below the reorder level
    THEN generate a reorder alert.
    """

    stock = facts.get("stock")
    reorder_level = facts.get("reorder_level")

    # Do not fire if required information is missing.
    if stock is None or reorder_level is None:
        return False

    return stock <= reorder_level


def reorder_action(facts):
    """
    Generate a reorder alert.
    """

    return {
        "reorder_alert": True
    }


# RULE BASE


RULES = [
    Rule(
        name="High Priority Order",
        condition=priority_condition,
        action=priority_action
    ),

    Rule(
        name="Stock Hold",
        condition=stock_hold_condition,
        action=stock_hold_action
    ),

    Rule(
        name="Reorder Alert",
        condition=reorder_condition,
        action=reorder_action
    )
]