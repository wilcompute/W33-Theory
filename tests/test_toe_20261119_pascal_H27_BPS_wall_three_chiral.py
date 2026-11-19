"""Exact H27 BPS wall × Pascal gram three-family selector tests."""
import sys,unittest
from math import sqrt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_pascal_H27_BPS_wall_chiral_selector as w

class DomainwallChiralSelector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=w.run()
    def test_wall_W_second_derivative(self):
        self.assertAlmostEqual(w.Wsecond(0),0)
        self.assertAlmostEqual(w.Wsecond(1),-9)
    def test_bps_Wprime_nonnegative(self):
        for x in (.01,.1,.5,.9,.99):
            self.assertGreater(w.Wprime(x),0)
    def test_L2_exact_lambdas(self):
        vals=self.r["pascal_Gram_mass_eigenvalues_L2"]
        self.assertEqual(len(vals),4)
        self.assertAlmostEqual(vals[0],w.PHI**-4)
        self.assertAlmostEqual(vals[1],1)
        self.assertAlmostEqual(vals[2],1)
        self.assertAlmostEqual(vals[3],w.PHI**4)
    def test_open_bulk_mass_interval(self):
        lower,upper=self.r["gapped_Fredholm_L2_three_family_open_interval_m0"]
        self.assertAlmostEqual(lower,9*w.PHI**-4)
        self.assertAlmostEqual(upper,9)
        self.assertLess(lower,2)
    def test_noncritical_mass_gapped_three_chiral(self):
        for m0 in (1.4,2.,4.,7.,8.9):
            self.assertEqual(w.zero_mode_count(2,m0),3)
    def test_too_small_m0_has_four_zero_modes(self):
        self.assertEqual(w.zero_mode_count(2,1.),4)
    def test_too_large_m0_has_one_or_no_zero_modes(self):
        self.assertEqual(w.zero_mode_count(2,10.),1)
        self.assertEqual(w.zero_mode_count(2,100.),0)
    def test_gapped_selector_right_chiral_zero(self):
        self.assertEqual(self.r["normalizable_right_count_m0_2"],0)
    def test_ungapped_zero_offset_three_is_not_protected(self):
        self.assertEqual(self.r["zero_offset_L2_formal_normalizable_count"],3)
        self.assertIn("non-Fredholm",self.r["zero_offset_NOT_topologically_protected"])
    def test_beta_integral_zero_mode_normalization(self):
        self.assertIn("Beta",self.r["zero_offset_nonFredholm_norm_formula"])
        self.assertAlmostEqual(w.Wprime(.5),3*.25*(1-.125))
    def test_higher_dyadic_levels_create_additional_modes(self):
        self.assertEqual(w.zero_mode_count(1,2.),2)
        self.assertEqual(w.zero_mode_count(2,2.),3)
        self.assertGreater(w.zero_mode_count(3,2.),3)
    def test_rank_one_defect_flavor_split_preserves_three_chiral_modes(self):
        self.assertLess(self.r["rank_one_perturbation_operator_norm"],
                        self.r["strict_spectral_gap_margin_at_m0_2"])
        eig=self.r["perturbed_four_distinct_eigenvalues"]
        self.assertEqual(len(set(round(v,7) for v in eig)),4)
        self.assertEqual(self.r["perturbed_three_chiral_normalizable_count"],3)
    def test_zero_modes_are_not_charged_lepton_masses(self):
        self.assertIn("massless before Higgs",self.r["crucial_scope"])
        self.assertIn("not the physical SM family index",self.r["crucial_scope"])
    def test_two_modes_remain_degenerate(self):
        self.assertIn("two lambda1 modes",self.r["persistent_family_pair_degeneracy"])
if __name__=="__main__":unittest.main()
