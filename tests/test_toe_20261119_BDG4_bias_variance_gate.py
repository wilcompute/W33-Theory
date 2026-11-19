"""Finite-cone exact BDG4 constant-field continuum bias/variance tradeoff."""
import sys,unittest,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_BDG4_bias_variance_gate as b
class CausalBiasVarianceGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.a=b.run()
    def test_six_fixed_parent_epsilon_scenarios(self):
        self.assertEqual(len(self.a["rows"]),6)
    def test_finite_volume_expected_constant_bias_nonzero(self):
        for r in self.a["rows"]:
            self.assertGreater(abs(r["exact_finite_volume_mean_bias_from_quadrature"]),.4)
    def test_analytic_mean_and_MonteCarlo_compatible_with_standard_error(self):
        for r in self.a["rows"]:
            self.assertLess(r["absolute_mean_disagreement_in_SE"],4)
    def test_smearing_reduces_constant_field_derived_MSE(self):
        for key in ("100.0","200.0"):
            self.assertEqual(self.a["best_per_parent_density"][key]["epsilon_best_of_tested_three"],.2)
            self.assertLess(self.a["best_per_parent_density"][key]["MSE_ratio_best_over_sharp"],.001)
    def test_no_general_field_or_quantum_gravity_claim(self):
        self.assertIn("not generic smooth fields",self.a["limits"])
if __name__=="__main__":unittest.main()
