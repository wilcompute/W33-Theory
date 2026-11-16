import importlib.util
from pathlib import Path
from decimal import Decimal
import unittest
P=Path(__file__).resolve().parents[1]/"analysis"/"toe_20261116_near_equal_flux_BF_scaling.py"
spec=importlib.util.spec_from_file_location("nearbf",P)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class NearEqual(unittest.TestCase):
    def test_producer(self):
        self.assertTrue(mod.verify()["status"].startswith("PASS"))
    def test_asymptotic(self):
        c=mod.case(10000)
        self.assertTrue(Decimal("44.9")<Decimal(c["N_squared_times_BF_gap"])<Decimal(45))
    def test_positive_violation_and_radius_scaling(self):
        for n in (1,2,11,100,1000):
            v=mod.case(n)
            self.assertTrue(Decimal(v["BF_gap_below_minus4"])>0)
            self.assertTrue(Decimal(v["L_cubed_in_Planck_units"])>1)
    def test_equal_flux_exactly_at_BF(self):
        self.assertEqual(mod.ratio_squared(Decimal("0.5")),Decimal(1))
if __name__=="__main__":unittest.main()
