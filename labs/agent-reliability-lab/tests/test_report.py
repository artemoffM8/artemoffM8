import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from report import summarize

class ReportTests(unittest.TestCase):
    def test_metrics(self):
        rows = [{"task_id":"t1","agent":"hermes","verified_success":True,"cost_usd":2},
                {"task_id":"t2","agent":"hermes","verified_success":False,"cost_usd":1}]
        self.assertEqual(summarize(rows)["hermes"]["success_rate"], 0.5)
        self.assertEqual(summarize(rows)["hermes"]["cost_per_verified_success_usd"], 3)

    def test_missing_cost_is_unknown(self):
        result = summarize([{"task_id":"t","agent":"codex","verified_success":True,"cost_usd":None}])
        self.assertIsNone(result["codex"]["total_cost_usd"])

    def test_no_success_no_cost_per_success(self):
        result = summarize([{"task_id":"t","agent":"codex","verified_success":False,"cost_usd":0}])
        self.assertIsNone(result["codex"]["cost_per_verified_success_usd"])

    def test_reject_duplicate(self):
        row = {"task_id":"t","agent":"hermes","verified_success":True,"cost_usd":1}
        with self.assertRaises(ValueError):
            summarize([row, row])

    def test_reject_negative_cost(self):
        with self.assertRaises(ValueError):
            summarize([{"task_id":"t","agent":"hermes","verified_success":True,"cost_usd":-1}])

    def test_reject_non_boolean_success(self):
        with self.assertRaises(ValueError):
            summarize([{"task_id":"t","agent":"hermes","verified_success":1,"cost_usd":1}])

if __name__ == "__main__":
    unittest.main()
