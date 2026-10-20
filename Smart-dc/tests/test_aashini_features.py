import unittest
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from warehouse.semantic_net import SemanticNet
from uncertainty.bayes_scan import probability_item_on_shelf_after_failed_scan
from uncertainty.dempster_shafer import combine_evidence
from warehouse.graph import load_warehouse
from warehouse.records import load_items, load_workers
import csv

DATA = ROOT / "data"

class AashiniFeatureTests(unittest.TestCase):
    def test_semantic_net_finds_fragile_zones(self):
        net = SemanticNet.load_csv(DATA / "relations.csv")
        self.assertTrue(net.zones_for_category("fragile"))
        self.assertIn("S1", net.objects("I001", "stored-in"))

    def test_bayes_probability_is_between_zero_and_one(self):
        p = probability_item_on_shelf_after_failed_scan()
        self.assertGreaterEqual(p, 0)
        self.assertLessEqual(p, 1)
        self.assertLess(p, 0.95)

    def test_dempster_shafer_combines_sensor_evidence(self):
        a = {"on_shelf": .7, "not_on_shelf": .1, "unknown": .2}
        b = {"on_shelf": .6, "not_on_shelf": .15, "unknown": .25}
        result = combine_evidence(a, b)
        self.assertAlmostEqual(sum(result[k] for k in ("on_shelf","not_on_shelf","unknown")), 1.0)
        self.assertGreater(result["on_shelf"], result["not_on_shelf"])

    def test_required_dataset_sizes_and_references(self):
        graph = load_warehouse(DATA / "warehouse.txt")
        items = load_items(DATA / "inventory.csv")
        workers = load_workers(DATA / "workers.csv")
        with (DATA / "test_orders.csv").open(newline="", encoding="utf-8-sig") as f:
            orders = list(csv.DictReader(f))
        self.assertGreaterEqual(len(graph.locations), 30)
        self.assertGreaterEqual(len(items), 20)
        self.assertGreaterEqual(len(workers), 6)
        self.assertEqual(len(orders), 10)
        self.assertTrue(all(i.location_id in graph.locations for i in items.values()))

if __name__ == "__main__":
    unittest.main(verbosity=2)
