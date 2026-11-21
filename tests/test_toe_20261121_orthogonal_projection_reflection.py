"""Independent regression for the odd/even exceptional projection geometry."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import toe_20261121_orthogonal_projection_reflection as m


class ExceptionalProjectionTests(unittest.TestCase):
    def test_even_characteristic_nucleus(self):
        self.assertTrue(m.audit_even_two()["bijective_nucleus_projection"])

    def test_even_four_nucleus(self):
        self.assertEqual(m.audit_even_four()["null_points"], 1365)

    def test_odd_q3_exhaustive(self):
        report = m.audit_odd(3, exhaustive=True)
        self.assertEqual(report["anisotropic_centers"], {"square": 351, "nonsquare": 378})
        self.assertEqual(report["theory"]["minus"], {"tangent": 112, "double": 126, "image": 238})
        self.assertEqual(report["theory"]["plus"], {"tangent": 130, "double": 117, "image": 247})

    def test_odd_q5_generalization(self):
        report = m.audit_odd(5, exhaustive=False)
        self.assertEqual(sum(report["anisotropic_centers"].values()), 5**6)
        self.assertEqual(report["theory"]["plus"], {"tangent": 806, "double": 1550, "image": 2356})
        self.assertEqual(report["theory"]["minus"], {"tangent": 756, "double": 1575, "image": 2331})

    def test_even_and_odd_are_distinct(self):
        for p in (3, 5):
            t = m.theoretical_counts(p)
            self.assertEqual(t["plus"]["double"] + t["minus"]["double"], p**5)
            self.assertEqual(t["plus"]["image"] - t["minus"]["image"], p**2)


if __name__ == "__main__":
    unittest.main()
