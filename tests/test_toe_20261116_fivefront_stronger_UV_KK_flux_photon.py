"""Regression for five new TOE research fronts plus prior verified controls."""
from pathlib import Path
import importlib.util,math,unittest
import sympy as S
ROOT=Path(__file__).resolve().parents[1]/"analysis"
def load(name,filename):
    sp=importlib.util.spec_from_file_location(name,ROOT/filename)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
e6=load("e6_3fam","toe_20261116_SU5_adjoint_three_family_spectral.py")
flux=load("gradedflux","toe_20261116_M5_graded_G4_wedge_complex.py")
eft=load("cusp","toe_20261116_M5_probe_cusp_BF_suppression.py")
opt=load("optical","toe_20261116_qutrit_F3_optical_budget.py")
old=load("qutritseq","toe_20261116_qutrit_anytime_eprocess.py")
old_e6=load("e6cubic","toe_20261116_E6_Yukawa_superpotential_flat.py")
jordan=load("jordan_stu","toe_20261116_STU_Jordan_24missing.py")

class SU5E6Checks(unittest.TestCase):
    def test_exact_stationary_and_spectrum(self):
        x=e6.su5_adjoint_spectral()
        self.assertEqual(x["F_term_linearization_rank"],12)
        self.assertEqual(x["Hessian_eigenvalues_lambda_v_1"],{"0":12,"+5":8,"-5":3,"-1":1})
        self.assertTrue(x["previous_3_complex_Cartan_moduli_lifted"])
    def test_characteristic(self):
        x=e6.su5_adjoint_spectral()
        self.assertEqual(x["traces_1_to_5"],{"1":0,"2":30,"3":-30,"4":210,"5":-390})
        self.assertIn("t**5",x["characteristic_polynomial"])
    def test_critical_uv_caveat(self):
        self.assertIn("no degree-3",e6.su5_adjoint_spectral()["IMPORTANT_UV_CAVEAT"])
    def test_three_families(self):
        x=e6.three_family_cubic()
        self.assertEqual(x["mass_matrix_rank"],30)
        self.assertEqual(x["remaining_kernel"],51)
    def test_one_family_source(self):
        self.assertEqual(old_e6.mass_hessian(1,2).rank(),10)
    def test_prior_superpotential_F_D(self):
        self.assertTrue(old_e6.flat_superpotential_control()["not_isolated"])

class GradedFluxChecks(unittest.TestCase):
    def test_all_graded_maps(self):
        x=flux.case(6,6,6)
        self.assertEqual(x["smith_invariants"],{"H0_H4":[6],"H1_H5":[6,6],"H2_H6":[6]})
    def test_coprime_mixed_flux(self):
        x=flux.case(100,101,100)
        self.assertEqual(x["smith_invariants"],{"H0_H4":[1],"H1_H5":[100,100],"H2_H6":[1]})
    def test_horizontal_zero(self):
        x=flux.case(0,6,6)
        self.assertEqual(x["smith_invariants"],{"H0_H4":[6],"H1_H5":[],"H2_H6":[6]})
    def test_Kunneth_ranks(self):
        x=flux.verify()
        self.assertEqual(x["cohomology_betti_numbers"],{str(i):v for i,v in enumerate((1,2,3,4,3,2,1))})
    def test_form_sign(self):
        self.assertEqual(flux.product_form(("a",),("x",)),(1,("x","a")))
        self.assertEqual(flux.product_form(("b",),("a",)),(-1,("a","b")))

class CuspAndProbeChecks(unittest.TestCase):
    def test_exact_expansion_parameters(self):
        x=eft.case(10000,100)
        self.assertAlmostEqual(x["torus_8derivative_parameter"],4*math.pi*100**3/(3*10000**2))
        self.assertAlmostEqual(x["sphere_8derivative_parameter"],32/(3*math.pi**2*10000**2))
    def test_largeN_probe(self):
        x=eft.case(1000,1,2)
        self.assertAlmostEqual(x["M5_to_bulk_characteristic_action_ratio"],32*math.pi**2/(9*1000))
    def test_cusp_breaks_control(self):
        y=10**(6*2/3)
        x=eft.case(10**6,y)
        self.assertAlmostEqual(x["torus_8derivative_parameter"],4*math.pi/3,places=10)
    def test_number_of_unstable_harmonics(self):
        a=eft.case(10**6,10)
        b=eft.case(10**6,1000)
        self.assertGreater(b["at_least_this_many_signed_classical_unstable_long_cycle_modes"],a["at_least_this_many_signed_classical_unstable_long_cycle_modes"])
    def test_full(self):
        self.assertTrue(eft.verify()["status"].startswith("PASS"))

class OpticalHardwareChecks(unittest.TestCase):
    def test_MUB_4projectors(self):
        x=opt.mub_identity()
        self.assertLess(x["operator_max_norm_residual"],1e-12)
    def test_three_coupler_analyzer(self):
        x=opt.mub_identity()["F3_analzyer_Reck_couplers"]
        self.assertEqual(x["couplers"],3)
        self.assertLess(x["reconstruction_max_error"],1e-12)
    def test_Bell_isotropic(self):
        x=opt.case(.75,0,1,1,1,1,eps=0)
        self.assertAlmostEqual(x["matched_probability_given_perfect_detection"],(1+2*.75)/3)
    def test_phase_noise_reduces(self):
        a=opt.case(.75,0,1,1,1,1)
        b=opt.case(.75,.4,1,1,1,1)
        self.assertGreater(a["Bell_fidelity"],b["Bell_fidelity"])
    def test_good_vs_bad_detection(self):
        x=opt.verify()
        self.assertTrue(x["example_feasible"]["detectable_with_positive_asymptotic_gap"])
        self.assertFalse(x["example_not_feasible"]["detectable_with_positive_asymptotic_gap"])
    def test_product_efficiency(self):
        x=opt.case(.75,0,.85,.85,.8,1)
        self.assertAlmostEqual(x["total_eventready_pair_detection"],.85**2*.8)
    def test_witness_sequential(self):
        p=old.verify()
        self.assertTrue(p["simulated_examples"]["coherent_drift"]["reject_at_alpha"])
        self.assertFalse(p["simulated_examples"]["adaptive_separable"]["reject_at_alpha"])

if __name__=="__main__":unittest.main()
