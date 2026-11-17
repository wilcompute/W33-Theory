"""Regression: five TOE physics fronts and one independent extra branch."""
import importlib.util,math,unittest
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def load(n,p):
    s=importlib.util.spec_from_file_location(n,ROOT/p)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
e6=load("vece6","toe_20261116_E6_Yukawa_superpotential_flat.py")
kk=load("kk2","toe_20261116_KK_secondorder_geometry_mixing.py")
cs=load("mcs","toe_20261116_M5_STU_Chern_Simons_lattice.py")
r4=load("geom8","toe_20261116_11D_R4_invariants_firewall.py")
qr=load("qrev","toe_20261116_qutrit_anytime_eprocess.py")
old_e6=load("olde6","toe_20261116_E6_full_cubic_SM_stabilizer.py")
old_q=load("oldq","toe_20261116_qutrit_randomized_memory_drift.py")

class CubicMassAndFflat(unittest.TestCase):
    def test_full_cert(self):
        self.assertTrue(e6.verify()["status"].startswith("PASS"))
    def test_rank10_for_linear_combos(self):
        for a,b in ((1,0),(0,1),(1,2),(1,sp.I)):
            M=e6.mass_hessian(a,b)
            self.assertEqual(M.rank(),10)
            self.assertEqual(M.nullspace().__len__(),17)
    def test_nonzero_singular_masses(self):
        for a,b in ((2,0),(1,1+sp.I)):
            M=e6.mass_hessian(a,b)
            self.assertEqual((M.conjugate().T*M).eigenvals(),
                             {0:17,sp.expand(sp.conjugate(a)*a+sp.conjugate(b)*b):10})
    def test_vectorlike_doublet_triplet(self):
        x=e6.mass_hessian(1,1)
        self.assertEqual([x[:9,:9].rank(),x[9:18,18:27].rank(),x[18:27,9:18].rank()],[4,3,3])
    def test_exact_polarized_F(self):
        self.assertTrue(e6.flat_superpotential_control()["not_isolated"])
    def test_adjoint_moduli(self):
        a=e6.cartan_five_invariant()
        self.assertEqual(a["unlifted_complex_SU5_Cartan_moduli_at_least"],3)
        self.assertEqual(a["quadratic_vs_fifth_Cartan_gradient_rank"],2)
    def test_prior_SM_stabilizer(self):
        x=old_e6.verify()
        self.assertEqual((x["E6_Lie_dim"],x["surviving_SU5_Lie_dim"],x["SM_Lie_dim"]),(78,24,12))

class NearEqualGeometry(unittest.TestCase):
    def test_exact_coefficients(self):
        x=kk.symbolic()
        self.assertEqual(x["eta_coefficients"],["3/2","-3/4","-12","147/8"])
        self.assertEqual(x["lambda_coefficients_over_pi"],["3","-3/2","-57/8","183/16"])
    def test_mass_proxy_coefficient(self):
        self.assertAlmostEqual(kk.symbolic()["proxy_second_order_coefficient_numeric"],-7.6221129337592535)
    def test_sign_of_unknown_mixing(self):
        r=kk.physical_mixing_obstruction()["counterexamples"]
        self.assertLess(r[0]["second_order_shift_at_t_0p01"],0)
        self.assertGreater(r[1]["second_order_shift_at_t_0p01"],0)
    def test_cert(self):
        self.assertTrue(kk.verify()["status"].startswith("PASS"))

class TopologyFluxPairing(unittest.TestCase):
    def test_triple_intersection(self):
        x=cs.intersection_certificate()
        self.assertEqual(len(x["nonzero_triple_intersections"]),6)
        self.assertEqual(x["volume_cubic"],"(1/6) integral J^3 = a*b*c")
    def test_flux_gcd_distinction(self):
        self.assertEqual(cs.flux_pairing(5,6,6)["Smith_invariant"],1)
        self.assertEqual(cs.flux_pairing(6,6,6)["Smith_invariant"],6)
    def test_no_false_physical_BF(self):
        self.assertIn("not certified",cs.flux_pairing(5,6,6)["physical_caveat"])
    def test_cert(self):
        self.assertTrue(cs.verify()["status"].startswith("PASS"))

class CurvatureControls(unittest.TestCase):
    def test_scalar_invariants(self):
        x=r4.invariants(sp.Rational(1,2))
        self.assertEqual((x["R_L2"],x["Ricci_squared_L4"],x["Riemann_squared_L4"]),("4","224","328"))
    def test_reflection_anisotropy(self):
        self.assertEqual(r4.invariants(sp.Rational(1,4))["Riemann_squared_L4"],
                         r4.invariants(sp.Rational(3,4))["Riemann_squared_L4"])
    def test_pontryagin_scalar_distinction(self):
        x=r4.verify()
        self.assertEqual(x["exact_invariants"]["pointwise_X8"],"0")
        self.assertEqual(x["samples"][1]["Riemann_squared_squared_L8"],"107584")
    def test_no_claim_real_R4(self):
        self.assertTrue(r4.verify()["no_physical_eight_derivative_coefficient_computed"])

class SequentialQutrit(unittest.TestCase):
    def test_factor_valid_under_any_null(self):
        self.assertLessEqual(qr.check_factor(.51,.75,.25),1)
        self.assertAlmostEqual(qr.check_factor(.51,.75,.51),1)
    def test_fixed_likelihood_against_Bernoulli_null(self):
        run=qr.eprocess([1]*15,adaptive=False,target_q=.75,epsilon=.01)
        self.assertAlmostEqual(run["log_evidence_final"],15*math.log(.75/.51))
        self.assertTrue(run["reject_at_alpha"])
    def test_anytime_adaptive(self):
        r=qr.verify()["simulated_examples"]
        self.assertTrue(r["coherent_drift"]["reject_at_alpha"])
        self.assertFalse(r["adaptive_separable"]["reject_at_alpha"])
        self.assertFalse(r["worst_case_separable"]["reject_at_alpha"])
    def test_leakage_penalizes(self):
        outcomes=qr.synth("coherent_drift",2000,20261116)
        low=qr.eprocess(outcomes,setting_leakage_TV=0.)
        high=qr.eprocess(outcomes,setting_leakage_TV=.08)
        self.assertLessEqual(high["log_evidence_peak"],low["log_evidence_peak"]+1e-9)
    def test_null_requires_valid_q(self):
        with self.assertRaises(ValueError):qr.eprocess([1],epsilon=.6)
    def test_prior_batched_null(self):
        self.assertTrue(old_q.verify()["status"].startswith("PASS"))

if __name__=="__main__":unittest.main()
