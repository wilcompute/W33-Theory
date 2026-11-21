"""Regression for the exact octonionic-reflection incidence obstruction."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import toe_20261121_octonionic_reflection_line_test as m


class HexagonReflectionTests(unittest.TestCase):
    def test_all_729_nonsingular_centers(self):
        result = m.run(write=False)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["anisotropic_centers_checked"], 729)
        self.assertEqual(result["classes"][0]["surviving_lines"], 28)
        self.assertEqual(result["classes"][1]["surviving_lines"], 52)


if __name__ == "__main__":
    unittest.main()
