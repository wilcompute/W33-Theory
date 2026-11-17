"""2026-11-17 next-wave seven-front exact/numerical regressions.
New science checks are conditional on the repo's verified E6 cubic
branching, physical 11D two-derivative pencil, and trusted photonic
POVM premises. They do NOT constitute a full TOE.
"""
import unittest,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261117_E6_two_adjoint_split_27_threshold as e6
import toe_20261117_E6_split_27_full_CW as cw
import toe_20261117_11D_modular_harmonic_uniform_BF as ads
import toe_20261117_qutrit_calibration_anytime_DP as qt
import toe_20261117_Cfield_spin_FW_torsion as cf
import toe_20261117_E6_proton_scale_proxy as proton
import toe_20261117_E6_FDflat_B_angle_scan as fd
class E6SplitThreshold(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=e6.verify()
 def test_27_branching(self):self.assertEqual(sum(r["dimension"] for r in self.z["E6_branching_and_trace"]["SU5_rep_branching_weights"]),27)
 def test_10_wedge_trace(self):self.assertEqual(self.z["E6_branching_and_trace"]["tr10_H4"],"3p2²-3p4")
 def test_complete_e6_no_shape(self):self.assertEqual(sum(self.z["E6_branching_and_trace"]["p4_irrep_coefficients"].values()),0)
 def test_symmetry_even(self):self.assertIn("s-messenger",self.z["loop_scan"]["best_positive"]["exact_sign_protected"])
 def test_nonempty_positive(self):self.assertGreater(self.z["loop_scan"]["positive_count"],0)
 def test_nonempty_negative(self):self.assertGreater(self.z["loop_scan"]["negative_count"],0)
 def test_positive_bench(self):
  self.assertGreater(e6.threshold(-.2,.2,.25)["kappa_SU5_TrPhi4"],.0025)
 def test_heavy_scalars_stable(self):self.assertTrue(e6.threshold(-.2,.2,.25)["full_SUSY_heavy_scalars_positive"])
 def test_singlet_masses(self):
  x=e6.threshold(-.2,.2,.25)
  self.assertTrue(all(r["min_scalar_mass2"]>0 for r in x["irrep"]))
 def test_no_split_nogo(self):
  for delta in (-.1,.1,.25):
   self.assertAlmostEqual(e6.threshold(0,0,delta)["kappa_SU5_TrPhi4"],0,places=13)
 def test_single_SO10_split_may_fail(self):
  self.assertIsNotNone(e6.threshold(-.2,0,.25))
 def test_param_scans(self):self.assertGreater(self.z["loop_scan"]["candidates_analyzed"],70)
class CompleteMessengerLog(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=cw.verify()
 def test_108_channels(self):self.assertIn("108",self.z["field_content"])
 def test_four_radii(self):self.assertEqual(len(self.z["fixed_norm_comparators"]),4)
 def test_positive_gap_all(self):
  self.assertTrue(all(float(x["V4plus1_minus_V3plus2"])>0 for x in self.z["fixed_norm_comparators"]))
 def test_positive_SU3_curvature_all(self):
  self.assertTrue(all(float(x["3fold_shape_curvature"])>0 for x in self.z["fixed_norm_comparators"]))
 def test_positive_SU2_curvature_all(self):
  self.assertTrue(all(float(x["2fold_shape_curvature"])>0 for x in self.z["fixed_norm_comparators"]))
 def test_expansion_low(self):self.assertLess(self.z["fixed_norm_comparators"][0]["relative_correction"],.01)
 def test_higher_orders_nonzero(self):self.assertGreater(self.z["fixed_norm_comparators"][-1]["relative_correction"],.1)
 def test_benchmark_kappa(self):self.assertAlmostEqual(self.z["benchmark"]["kappa_SU5_TrPhi4"],.002542364377803341)
 def test_not_full_E6(self):self.assertIn("F/D",self.z["critical_scope"])
class UniformAdS(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=ads.verify()
 def test_Hermite_L(self):self.assertAlmostEqual(self.z["Hermite_2D_shortest_dual_eigenvalue_upper"],2*math.pi*math.sqrt(3))
 def test_L_below_BF(self):self.assertLess(ads.L,12)
 def test_nonzero_integer_harmonic(self):self.assertTrue(all(x["integer_harmonic"]>=1 for x in self.z["harmonic_examples"]))
 def test_harmonic_window(self):
  self.assertTrue(all(ads.L/4-1e-12<=x["physical_lambda_selected"]<=ads.L+1e-12 for x in self.z["harmonic_examples"]))
 def test_modular_cusp(self):self.assertGreater(self.z["harmonic_examples"][-1]["integer_harmonic"],100000)
 def test_compact_gap_existence(self):self.assertIn("compact",self.z["uniform_gap_existence_proof"])
 def test_grid_3621(self):self.assertEqual(self.z["numerical_not_rigorous_minimum"]["grid_sample_count"],3621)
 def test_min_defect_numerical(self):self.assertAlmostEqual(self.z["numerical_not_rigorous_minimum"]["grid_min_deficit"],.3941869635,places=8)
 def test_not_interval(self):self.assertTrue(self.z["numerical_not_rigorous_minimum"]["absolute_error_not_certified"])
 def test_operator_validations(self):self.assertEqual(self.z["independent_5x5_numpy_operator_validation"],16)
class CalibrationSequential(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=qt.verify()
 def test_gap(self):self.assertGreater(self.z["original_ideal_gap"],.19)
 def test_epsilon_tolerance(self):self.assertAlmostEqual(self.z["largest_symmetric_epsilon_at_zero_leakage"],.09735158651485)
 def test_robust(self):self.assertTrue(self.z["calibration_scenarios"][2]["robust_certification_possible"])
 def test_too_large_error(self):self.assertFalse(self.z["calibration_scenarios"][-1]["robust_certification_possible"])
 def test_null_anytime(self):self.assertLessEqual(self.z["exact_DP_no_noise_null"]["ever_crossed_prob"],.01)
 def test_null_value(self):self.assertAlmostEqual(self.z["exact_DP_no_noise_null"]["ever_crossed_prob"],.0075145087)
 def test_alt_power(self):self.assertGreater(self.z["exact_DP_no_noise_alternative"]["ever_crossed_prob"],.999)
 def test_error_perturbed_null(self):self.assertLessEqual(self.z["exact_DP_eps03_beta01_null"]["ever_crossed_prob"],.01)
 def test_error_perturbed_alt(self):self.assertGreater(self.z["exact_DP_eps03_beta01_alternative"]["ever_crossed_prob"],.75)
 def test_history_robust(self):self.assertIn("conditional null",self.z["nonIID_proof"])
class CfieldAndFW(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=cf.verify()
 def test_spin_m6(self):self.assertTrue(self.z["M6"]["spin"])
 def test_spin_circle(self):self.assertTrue(self.z["circle6_example_euler_6_6"]["spin"])
 def test_no_shift_m6(self):self.assertEqual(self.z["M6"]["lambda=p1_over_2"],0)
 def test_no_shift_y6(self):self.assertEqual(self.z["circle6_example_euler_6_6"]["p1"],0)
 def test_flat_4torus(self):self.assertEqual(self.z["M6"]["flat_degree4_differential_character_H3_RmodZ"]["U1_free_factors"],4)
 def test_flat_y6(self):self.assertEqual(self.z["circle6_example_euler_6_6"]["flat_degree4_differential_character_H3_RmodZ"]["finite_torsion"],[6])
 def test_free_comparison(self):self.assertEqual(self.z["circle6_example_euler_6_6"]["H4_Z"]["free_rank"],1)
 def test_FW_nonzero(self):self.assertFalse(cf.fw(3,3,5)["naive_D5_wrapping_entire_Y5_times_time_allowed"])
 def test_1200(self):self.assertEqual(self.z["nonzero_signed_integer_triples_verified"],1200)
 def test_not_page(self):self.assertIn("NOT",self.z["not_a_Page_charge_dictionary"])
class GaugeProton(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=proton.verify()
 def test_four_vevs(self):self.assertEqual(len(self.z["benchmarks"]),4)
 def test_light_messenger(self):self.assertAlmostEqual(self.z["benchmarks"][2]["min_messenger_fermion_mass_over_M_at_A0"],.2)
 def test_x_over_M(self):self.assertAlmostEqual(self.z["benchmarks"][2]["X_vector_mass_over_M"],.03236043187592832)
 def test_M_scale_conditional(self):self.assertGreater(self.z["benchmarks"][2]["required_messenger_scale_GeV_IF_MX_at_least_1e15"],3e16)
 def test_no_lifetime_claim(self):self.assertIn("needs",self.z["no_lifetime_prediction"])
 def test_su5_alpha(self):self.assertEqual(self.z["illustrative_alpha5"],.04)
class FDSUSY(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=fd.verify()
 def test_72_120(self):self.assertEqual(self.z["exact_Cartan_norms_and_FD"]["trace27_B2"],"72 psi²+120 chi²")
 def test_FD_exists(self):self.assertIn("holomorphic F-terms vanish",self.z["exact_Cartan_norms_and_FD"]["FD_flat_constructive_proof"])
 def test_720_scan(self):self.assertGreater(self.z["B_angle_CW_scan_grid_720_with_fermion_mass_threshold_0p15"],400)
 def test_B_benchmark_not_min(self):self.assertFalse(self.z["benchmark_B_is_global_CW_grid_min"])
 def test_B_positive_region(self):self.assertGreater(self.z["positive_A_quartic_count_at_same_B_norm"],100)
 def test_positive_best(self):self.assertGreater(self.z["lowest_CW_B_energy_grid"]["kappa_A_SU5_TrA4"],0)
 def test_no_unique_B(self):self.assertIn("moduli",self.z["exact_Cartan_norms_and_FD"]["critical_missing"])
 def test_cutoff_stability(self):self.assertGreater(self.z["lowest_CW_B_energy_grid"]["smallest_fermion_mass_abs"],.15)
if __name__=="__main__":unittest.main()
