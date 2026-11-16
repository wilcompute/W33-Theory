import importlib.util
from pathlib import Path
import unittest

P=Path(__file__).resolve().parents[1]/"analysis"/"toe_20261116_iib_K_gysin_ring.py"
spec=importlib.util.spec_from_file_location("kgysin",P)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class KTheoryRing(unittest.TestCase):
    def test_all_cases(self):
        self.assertTrue(mod.verify()["status"].startswith("PASS"))
    def test_gcd_does_not_fix_ring(self):
        a=mod.k_gysin(3,0);b=mod.k_gysin(3,3)
        self.assertEqual(a["K0_additive"],b["K0_additive"])
        self.assertEqual(a["K1_additive"],b["K1_additive"])
        self.assertEqual(a["u_square_coefficient_mod_g"],0)
        self.assertEqual(b["u_square_coefficient_mod_g"],2)
    def test_even_spins_not_automatically_susy(self):
        self.assertTrue(mod.quotient_spin_lifts(2)["some_cover_Killing_spinor_survives"])
        self.assertFalse(mod.quotient_spin_lifts(4)["some_cover_Killing_spinor_survives"])
        self.assertEqual(mod.k_gysin(4,4)["spin_structure_count"],2)
    def test_signs_endpoints(self):
        for p,q in [(-3,-3),(0,7),(5,0),(6,-10)]:
            r=mod.k_gysin(p,q)
            self.assertEqual(r["gysin_nonzero_smith_factors"],[r["gcd"]]*2)
if __name__=="__main__":unittest.main()
