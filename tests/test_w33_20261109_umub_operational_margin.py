import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "analysis" / "w33_20261109_umub_operational_margin.py"
spec = importlib.util.spec_from_file_location("w33_20261109_umub_operational_margin", SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class OperationalMargins(unittest.TestCase):
    def test_positive_finite_shot_bounds(self):
        out = m.compute()
        self.assertEqual(out["status"], "PASS_CONDITIONAL_OPERATIONAL_BIAS_BOUNDS")
        self.assertEqual([r["bases"] for r in out["rows"]], [5, 8])
        self.assertAlmostEqual(out["rows"][0]["guaranteed_observed_one_outcome_bias"],
                               0.024603169919719198, places=12)
        self.assertAlmostEqual(out["rows"][1]["guaranteed_observed_one_outcome_bias"],
                               0.053095685027491, places=12)
        self.assertTrue(all(r["positive_detection_margin"] for r in out["rows"]))

    def test_zero_epsilon_and_explicit_failure_control(self):
        from fractions import Fraction
        positive = m.margin(5, Fraction(1, 9), Fraction(0), 20000, 0.01)
        failure = m.margin(5, Fraction(1, 9), Fraction(1, 10), 20000, 0.01)
        self.assertGreater(positive["guaranteed_observed_one_outcome_bias"],
                           failure["guaranteed_observed_one_outcome_bias"])
        self.assertEqual(failure["guaranteed_observed_one_outcome_bias"], 0.0)

if __name__ == "__main__":
    unittest.main()
