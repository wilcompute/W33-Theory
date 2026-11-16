"""Cross-front regression against prior committed M, IIB, E6, qutrit models."""
import importlib.util
import math
import unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/"analysis"/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

r4=load("r4","toe_20261116_R4_threshold_spinor_modes.py")
tK=load("tk","toe_20261116_twisted_K_AHSS_extensions.py")
e6=load("e6_h","toe_20261116_E6_cubic_hessian_center.py")
mub=load("mub","toe_20261116_qutrit_four_MUB_experiment.py")
prior=load("prev_e6","toe_20261116_e6_trinification_cubic_flat_branches.py")
kgysin=load("prev_k","toe_20261116_iib_K_gysin_ring.py")

class HigherDerivativeAndSpin(unittest.TestCase):
    def test_coefficient_exact(self):
        row=r4.correction_threshold(100000)
        self.assertAlmostEqual(float(row["large_N_coefficient_Ccrit"]),3645*math.pi**2/4,places=8)
        self.assertGreater(float(row["ratio_to_asymptotic"]),.9999)
    def test_prior_flux_verifier_agrees(self):
        for n in (10,100,1000):
            r=r4.correction_threshold(n)
            self.assertGreater(float(r["homogeneous_BF_gap"]),0)
            self.assertLess(float(r["required_dimensionless_correction_coefficient_C"]),3645*math.pi**2/4)
    def test_spinor_modes(self):
        self.assertEqual([n for n in range(1,17) if r4.spinor_deck_table(n)["surviving_cover_Killing_spinor_mode"]],[1,2])
        self.assertEqual(r4.spinor_deck_table(4)["lifts"][1]["invariant_mode_residues_mod_N"],[2])
    def test_characteristic_background_scope(self):
        d=r4.curvature_characteristic_control()
        self.assertEqual(d["X8_of_background"],"0")
        self.assertIn("does not imply",d["C3_X8_action_quadratic_warning"])

class TwistedAHSS(unittest.TestCase):
    def test_zero_twist_matches_prior(self):
        for p,q in ((3,0),(3,3),(4,4),(1,1)):
            r=tK.page(p,q,0);prior_row=kgysin.k_gysin(p,q)
            self.assertEqual(r["gcd"],prior_row["gcd"])
            self.assertEqual(r["K1_exact"],"Z^2")
    def test_nonzero_twist_associated_graded(self):
        for p,q,k in ((3,3,2),(1,1,3),(6,10,-4),(3,0,1)):
            r=tK.page(p,q,k)
            self.assertEqual(r["K0_finite_order"],math.gcd(p,q)**2)
            self.assertEqual(r["K1_finite_order"],abs(k)**2)
    def test_primitive_extension_resolved(self):
        self.assertEqual(tK.page(1,1,3)["K1_exact"],"Z_3 + Z_3")
        self.assertEqual(tK.page(1,1,2)["K0_exact"],"0")
    def test_nonprimitive_extension_not_fabricated(self):
        self.assertNotIn("K0_exact",tK.page(3,3,2))
        self.assertNotIn("K1_exact",tK.page(3,3,2))

class CubicHessian(unittest.TestCase):
    def test_exact_spectrum(self):
        for s in (1,2,7):
            h=e6.real_singlet_hessian(s)
            self.assertEqual(h["canonically_normalized_F_scalar_mass2"],[0,9*s*s,9*s*s])
            self.assertEqual(prior.scalar_triad(s,s,s)["F_norm_squared"],0)
    def test_invariant_monomials(self):
        self.assertTrue(e6.allowed_monomial("ABC"))
        self.assertTrue(e6.allowed_monomial("AAA"))
        for x in "ABC":
            for y in "ABC":
                self.assertFalse(e6.allowed_monomial(x+y))
    def test_manifest_singlet_modulus(self):
        self.assertEqual(e6.real_singlet_hessian(3)["H_det"],0)
        self.assertEqual(e6.real_singlet_hessian(3)["H_trace"],54)

class OpticalQutrit(unittest.TestCase):
    def test_mub_operator_identity(self):
        self.assertLess(mub.mubs_identity_error(),1e-12)
    def test_entanglement_boundary(self):
        self.assertFalse(mub.model(F(1,4))["entanglement_certified_by_4MUB_ideal_mean"])
        self.assertTrue(mub.model(F(2,5))["entanglement_certified_by_4MUB_ideal_mean"])
        self.assertFalse(mub.model(F(1,2))["entanglement_certified_by_2MUB_ideal_mean"])
    def test_hoeffding_plans(self):
        self.assertEqual(mub.shots_for_power(F(3,4))["shots_per_MUB"],16)
        self.assertEqual(mub.shots_for_power(F(3,5))["shots_per_MUB"],31)
        self.assertFalse(mub.shots_for_power(F(1,4))["certifiable_with_4MUB"])
    def test_fidelity_reconstruction(self):
        for v in (F(0),F(1,4),F(2,5),F(3,4),F(1)):
            m=mub.model(v)
            self.assertEqual(F(m["Bell_fidelity"]),(F(m["sum_4MUB_matching"])-1)/3)

if __name__=="__main__":
    unittest.main()
