"""Gate useful-output scope separately from acceptance of the clean input."""
from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from w33_three_copy_output_rank_audit import logical_qubits, verify


class OutputRankTests(unittest.TestCase):
    def test_full_search_retains_no_logical_qubits(self):
        result = verify()
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(all(result["checks"].values()))
        path = Path(__file__).resolve().parents[1] / "analysis" / "w33_three_copy_output_rank_audit_certificate.json"
        self.assertEqual(json.loads(json.dumps(result)), json.loads(path.read_text()))

    def test_rank_is_computed_and_invalid_generators_are_rejected(self):
        self.assertEqual(logical_qubits([], 6), 6)
        z = [[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        x = [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(logical_qubits([z]), 5)
        with self.assertRaises(ValueError):
            logical_qubits([z, z])
        with self.assertRaises(ValueError):
            logical_qubits([z, x])


if __name__ == "__main__":
    unittest.main()
