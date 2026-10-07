from rules import RuleEngine, RULES


facts = {
    "order_id": "O1",
    "zone": "A",
    "urgent": True,
    "stock": 3,
    "required_quantity": 5,
    "reorder_level": 4
}


engine = RuleEngine(RULES)

final_facts, fired_rules = engine.run(facts)


print("Final Facts:")
for key, value in final_facts.items():
    print(f"  {key}: {value}")

print("\nRules Fired:")
for rule in fired_rules:
    print(f"  - {rule}")