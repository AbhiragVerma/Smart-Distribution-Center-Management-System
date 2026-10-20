"""Semantic network for warehouse items, categories, and zones."""
from pathlib import Path
import csv

class SemanticNet:
    def __init__(self):
        self.relations = []  # (subject, relation, object)

    def add(self, subject, relation, obj):
        triple = (subject.strip(), relation.strip().lower(), obj.strip())
        if triple not in self.relations:
            self.relations.append(triple)

    @classmethod
    def load_csv(cls, filename):
        net = cls()
        with Path(filename).open(newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                net.add(row["subject"], row["relation"], row["object"])
        return net

    def objects(self, subject, relation):
        return sorted({o for s, r, o in self.relations
                       if s == subject and r == relation.lower()})

    def subjects(self, relation, obj):
        return sorted({s for s, r, o in self.relations
                       if r == relation.lower() and o == obj})

    def zones_for_category(self, category):
        """Return zones storing items that are-a category (including subcategories)."""
        categories = {category}
        changed = True
        while changed:
            changed = False
            for s, r, o in self.relations:
                if r == "is-a" and o in categories and s not in categories:
                    categories.add(s)
                    changed = True
        item_ids = set()
        for s, r, o in self.relations:
            if r == "is-a" and o in categories:
                item_ids.add(s)
        locations = set()
        for item in item_ids:
            locations.update(self.objects(item, "stored-in"))
        zones = set()
        for location in locations:
            zones.update(self.objects(location, "located-in"))
        return sorted(zones)

    def query(self, question):
        """Small natural-language query handler for the required demo questions."""
        q = question.lower().strip().rstrip("?")
        if "fragile" in q and ("zone" in q or "where" in q):
            return self.zones_for_category("fragile")
        if q.startswith("where is "):
            item = question.strip().rstrip("?")[9:].strip()
            return self.objects(item, "stored-in")
        if q.startswith("what is "):
            item = question.strip().rstrip("?")[8:].strip()
            return self.objects(item, "is-a")
        return []

if __name__ == "__main__":
    data = Path(__file__).parent.parent / "data" / "relations.csv"
    net = SemanticNet.load_csv(data)
    print("Zones holding fragile items:", net.zones_for_category("fragile"))
    print("Where is I001?", net.objects("I001", "stored-in"))
