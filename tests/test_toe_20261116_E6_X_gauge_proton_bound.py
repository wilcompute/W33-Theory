"""Unit tests for separate dimension-six E6 charge-five gauge channel."""
import sys,unittest,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261116_E6_charge5_gauge_proton_bound as gx
class GaugeProton(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=gx.verify()
    def test_bound(self):
        self.assertTrue(9e-32<gx.bound()<1.1e-31)
    def test_minimum_vev(self):
        self.assertTrue(2.5e14<self.r["VEV_Y_min_GeV_AR_1_W_0p1"]<2.7e14)
    def test_gauge_mass(self):
        self.assertAlmostEqual(gx.model(1e15,g=.7)["gauge_boson_MX_GeV"],3.5e15)
    def test_proton_lifetime_fourth_power(self):
        self.assertAlmostEqual(gx.model(2e14)["single_operator_partial_lifetime_years"]/gx.model(1e14)["single_operator_partial_lifetime_years"],16)
    def test_g_cancels(self):
        self.assertAlmostEqual(gx.model(1e15,g=.1)["effective_C6_GeV_minus2"]/gx.model(1e15,g=.9)["effective_C6_GeV_minus2"],1)
    def test_triplet_filter_not_gauge_protection(self):
        self.assertIn("not this independent",self.r["physics_key_point"])
    def test_unsuppressed_weak_vev(self):
        self.assertFalse(self.r["reference_low"]["passes_single_operator_bound"])
if __name__=="__main__":unittest.main()
