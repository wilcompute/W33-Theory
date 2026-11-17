"""Regress independent E6 mirror no-go, SU5 quantum CW shape, physical
AdS BF robustness, integral twisted-K shadow, exact qutrit analyzers
and setting-aware trusted MUB witness.
"""
import unittest,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261117_E6_mirror_Z4R_no_go as uv
import toe_20261117_SU5_CW_higher_orders_shape as vac
import toe_20261117_11D_BF_eightderiv_robustness as bf
import toe_20261117_Ypq_twisted_K_AHSS as kt
import toe_20261117_qutrit_four_MUB_loss_compiler as interfer
import toe_20261117_qutrit_calibrated_loss_witness as wit
class E6(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=uv.verify()
 def test_cartan(self):self.assertEqual(self.z["group_theory"]["Cartan_dimension"],6)
 def test_cubic_invariance(self):self.assertEqual(self.z["group_theory"]["exact_45_monomial_constraints"],45)
 def test_quartic_nogo(self):self.assertIn("No directional",self.z["group_theory"]["no_go"])
 def test_odd_mirror(self):self.assertTrue(self.z["group_theory"]["mirror_odd_powers_cancel"])
 def test_yukawa_allowed(self):
  for key in ("up_Yukawa","down_Yukawa","lepton_Yukawa","Weinberg","mirror_Yukawa_p","mirror_Yukawa_m"):
   self.assertTrue(self.z["operator_symmetry"]["allowed_by_Z4R"][key])
 def test_proton_forbidden(self):
  for key in ("QQQL","UUDE","UDD","LQD","LLE","LH_u"):
   self.assertFalse(self.z["operator_symmetry"]["allowed_by_Z4R"][key])
 def test_mu_forbidden(self):self.assertFalse(self.z["operator_symmetry"]["allowed_by_Z4R"]["mu_term"])
 def test_mirror_parity_breaks(self):self.assertTrue(self.z["operator_symmetry"]["mirror_exchange"]["A78_nonzero_VEV_spontaneously_breaks_mirror_Z2"])
 def test_spurion_mu(self):self.assertTrue(self.z["operator_symmetry"]["allowed_by_Z4R"]["spurion_S2_HuHd"])
 def test_gauge_proton_not_protected(self):self.assertIn("dimension-six",self.z["operator_symmetry"]["proton_scope"])
 def test_anomaly_not_claimed(self):self.assertIn("anomaly-free",self.z["not_UV_completion"])
class QuantumVac(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=vac.verify()
 def test_quartic_positive(self):self.assertGreater(self.z["series"]["quartic_coefficient"],0)
 def test_sixth_positive(self):self.assertGreater(self.z["series"]["sixth_coefficient"],0)
 def test_eighth_negative(self):self.assertLess(self.z["series"]["eighth_coefficient"],0)
 def test_fixed_radius(self):self.assertAlmostEqual(self.z["shape"]["fixed_vev_norm"],.2)
 def test_competitor_gap(self):self.assertGreater(self.z["shape"]["4plus1_minus_3plus2"],2e-7)
 def test_series_accuracy(self):
  z=self.z["shape"];self.assertLess(abs(z["quartic_sextic_predicted_difference"]/z["4plus1_minus_3plus2"]-1),.005)
 def test_SU3_curvature(self):self.assertGreater(self.z["shape"]["SU3_shape_scalar_curvature"],0)
 def test_SU2_curvature(self):self.assertGreater(self.z["shape"]["SU2_shape_scalar_curvature"],0)
 def test_multistart(self):self.assertEqual(self.z["shape"]["multistart_trials"],64)
 def test_one_of_starts_reaches(self):self.assertGreater(self.z["shape"]["converged_to_3plus2_energy"],0)
 def test_not_full_E6(self):self.assertIn("NOT included",self.z["shape"]["important_limitation"])
class AdS(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=bf.verify()
 def test_sample_grid(self):self.assertEqual(len(self.z["BF_deficit_vs_d_at_lambda3pi"]),5)
 def test_gap_min(self):self.assertGreater(min(x["BF_deficit"] for x in self.z["BF_deficit_vs_d_at_lambda3pi"]),.88)
 def test_gap_square(self):self.assertAlmostEqual(self.z["BF_deficit_vs_d_at_lambda3pi"][0]["BF_deficit"],1.0169440813,places=8)
 def test_eight_derivative_bound(self):self.assertIn("C/N",self.z["eight_derivative_scaling_example"])
 def test_nonphys_C(self):self.assertIn("NOT computed",self.z["eight_derivative_scaling_example"])
 def test_offblock_stress(self):self.assertEqual(len(self.z["offblock_mixing_and_rankone_shift_checks"]),12)
 def test_goldstone_normalization(self):self.assertIn("gauge-compatible physical normalization",self.z["physical_limit"])
 def test_no_full_11D(self):self.assertIn("NOT known",self.z["physical_limit"])
class KCharges(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=kt.verify()
 def test_1200(self):self.assertEqual(self.z["signed_integer_triples_checked"],1200)
 def test_Gysin_smith(self):self.assertEqual(kt.untwisted(6,6)["nonzero_Smith_invariants"],[6,6])
 def test_coprime(self):self.assertEqual(kt.untwisted(5,6)["K0_Y_torsion_cyclic_orders"],[])
 def test_6_5_duality_even(self):self.assertEqual(self.z["example_euler6_6_H5"]["original"]["K_even_group_cardinality"],36)
 def test_6_5_duality_odd(self):self.assertEqual(self.z["example_euler6_6_H5"]["original"]["K_odd_group_cardinality"],25)
 def test_dual_parity(self):self.assertEqual(self.z["example_euler6_6_H5"]["Tdual"]["K_odd_group_cardinality"],36)
 def test_extensions_unresolved(self):self.assertIn("NOT a canonical",self.z["example_euler6_6_H5"]["original"]["extension_open"])
 def test_no_Page_claim(self):self.assertIn("No explicit differential",self.z["scope"])
 def test_k_nonzero(self):
  with self.assertRaises(AssertionError):kt.twisted_AHSS(6,6,0)
 def test_e_nonzero(self):
  with self.assertRaises(AssertionError):kt.untwisted(0,0)
class Photonic(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.a=interfer.verify();cls.z=wit.verify()
 def test_6_unbiased_pairs(self):self.assertEqual(self.a["basis_pairs_unbiased_verified"],6)
 def test_three_mixing(self):self.assertEqual([p["stages"] for p in self.a["per_basis_compilers"].values()],[0,3,3,3])
 def test_reconstruction(self):self.assertTrue(all(x["maximum_reconstruction_error"]<1e-12 for x in self.a["per_basis_compilers"].values()))
 def test_legacy_conservative_fails(self):
  self.assertLess(self.z["conservative_vs_calibrated_two_memory_99p5"]["expected_entangled_match"],.51)
 def test_calibrated_aware_works(self):
  x=self.z["conservative_vs_calibrated_two_memory_99p5"]
  self.assertTrue(x["expected_violation"])
  self.assertLess(x["calibrated_separable_upper"],x["expected_entangled_match"])
 def test_expected_p0(self):self.assertAlmostEqual(self.z["conservative_vs_calibrated_two_memory_99p5"]["calibrated_separable_upper"],.3053206716,places=9)
 def test_expected_p1(self):self.assertAlmostEqual(self.z["conservative_vs_calibrated_two_memory_99p5"]["expected_entangled_match"],.5000238446,places=9)
 def test_KL_heuristic(self):
  x=self.z["conservative_vs_calibrated_two_memory_99p5"]["oracle_log_evalue100_heuristic_n"]
  self.assertLess(x,60)
 def test_four_MUB_identity(self):self.assertIn("I_9",self.z["MUB_exact_2design_identity"])
 def test_separable_tight(self):self.assertIn("Equality",self.z["exact_loss_aware_separable_bound"])
 def test_random_product(self):self.assertEqual(self.z["random_product_controls"],1000)
 def test_better_with_weak_mem_if_trusted(self):self.assertTrue(self.z["weak_memory_loss_aware_case"]["expected_violation"])
 def test_error_floor_kills(self):self.assertFalse(wit.witness(calibration_error=.3)["expected_violation"])
 def test_state_independent_trust(self):self.assertIn("ALL input states",self.z["critical_measurement_assumption"])
 def test_qavg_matches_old(self):
  z=self.z["model_qb"]
  self.assertAlmostEqual((z["q_Z"]+3*z["q_each_nonZ"])/4,z["q_uniform_average"],places=12)
if __name__=="__main__":unittest.main()
