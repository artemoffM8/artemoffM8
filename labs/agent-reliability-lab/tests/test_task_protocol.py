import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from task_protocol import ManifestError, load_manifest, validate_manifest

class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.base = json.loads((ROOT / "fixtures/sample_task.json").read_text())

    def test_fixture(self):
        self.assertEqual(load_manifest(ROOT / "fixtures/sample_task.json")["task_id"], "synthetic-001")

    def test_reject_extra_field(self):
        self.base["shell"] = "rm -rf /"
        with self.assertRaises(ManifestError):
            validate_manifest(self.base)

    def test_reject_path_traversal(self):
        self.base["task_id"] = "../escape"
        with self.assertRaises(ManifestError):
            validate_manifest(self.base)

    def test_reject_network(self):
        self.base["evaluation"]["network"] = "allow"
        with self.assertRaises(ManifestError):
            validate_manifest(self.base)

    def test_reject_unapproved_command(self):
        self.base["evaluation"]["test_command"] = ["bash", "-c", "echo hello"]
        with self.assertRaises(ManifestError):
            validate_manifest(self.base)

    def test_reject_over_budget(self):
        self.base["cost_limit_usd"] = 6
        with self.assertRaises(ManifestError):
            validate_manifest(self.base)

    def test_reject_over_time(self):
        self.base["time_limit_seconds"] = 7201
        with self.assertRaises(ManifestError):
            validate_manifest(self.base)

if __name__ == "__main__":
    unittest.main()
