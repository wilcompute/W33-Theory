"""Regression for eight independently constructed Nov17/18 research
frontiers: E6 rank/quantum pinning/UV beta, certified 11D BF, C-field
linking, nonuniform qutrit MUB, and two 11-cell/Klein orbit bridges.
"""
from pathlib import Path
import unittest,sys,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261117_E6_rank_two_singlet_Balignment_completion as rank
import toe_20261117_E6_B_Fterm_pinning_CW_response as pin
import toe_20261117_E6_UV_perturbativity_beta as uv
import toe_20261117_11D_certified_uniform_Rayleigh_BF_0p05 as ads
import toe_20261117_Cfield_integral_torsion_linking as link
import toe_20261117_qutrit_nonuniform_MUB_loss as qutrit
import toe_20261117_11cell_Klein_equivariant_orbit_bridge as klein
import toe_20261117_11cell_Klein_660flag_bifactor as bipair
class E6Rank(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=rank.verify()
 def test_stabilizers(self):self.assertEqual(list(self.z["Lie_algebra_dims"].values()),[78,24,12])
 def test_charge_matrix(self):self.assertEqual(self.z["singlet_charge_matrix_integer_Nc_S"],[[1,-5],[4,0]])
 def test_exact_det(self):self.assertEqual(self.z["singlet_charge_det"],20)
 def test_Btarget(self):self.assertEqual(self.z["B_eigenvalue_constraints"]["unique_psi"],"-1/5")
 def test_Bchi(self):self.assertEqual(self.z["B_eigenvalue_constraints"]["unique_chi"],"1/5")
 def test_u1_mass_positive(self):self.assertGreater(min(self.z["gauge_mass2_eigenvalues_per_g2v2_canonical_27_trace"]),0)
 def test_naive_Z20_not_physical(self):self.assertIn("covering",self.z["global_discrete_WARNING"])
 def test_superpotential_is_EFT(self):self.assertIn("1/Lambda",self.z["EFT_dimension"])
 def test_flat(self):self.assertIn("F=0 and D=0",self.z["FD_flat_exists"])
class E6PinnedCW(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=pin.verify()
 def test_nonzero_grad(self):self.assertGreater(abs(self.z["unpinned_CW_gradient_at_benchmark"][1]),.9)
 def test_pinhessian(self):self.assertGreater(min(self.z["pinned_tree_Hessian_eigenvalues_at_stiff_0p1"]),0)
 def test_nine_couplings(self):self.assertEqual(len(self.z["one_loop_local_minima"]),9)
 def test_stiff_restores_sign(self):
  self.assertLess(self.z["one_loop_local_minima"][0]["remaining_SU5_shape_kappa"],0)
  self.assertGreater(self.z["one_loop_local_minima"][-1]["remaining_SU5_shape_kappa"],0)
 def test_too_light_at_one(self):self.assertLess(self.z["one_loop_local_minima"][5]["minimum_heavy_messenger_fermion_mass"],.15)
 def test_heavy_at_two(self):self.assertGreater(self.z["one_loop_local_minima"][6]["minimum_heavy_messenger_fermion_mass"],.15)
 def test_massfloor_root(self):self.assertAlmostEqual(self.z["pin_mass_floor_threshold"]["pin_stiffness_at_benchmark_mass_floor_0p15"],1.90698666498,places=4)
 def test_no_global_proof(self):self.assertIn("not a global E6 scalar",self.z["scope"])
class E6UV(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=uv.verify()
 def test_beta_33(self):self.assertEqual(self.z["N1_SUSY_one_loop_beta_b"],33)
 def test_alpha0(self):self.assertEqual(self.z["UV_example_alpha_at_messenger_scale"],.04)
 def test_pole(self):self.assertAlmostEqual(self.z["landau_pole_ratio"],116.7446264161288,places=6)
 def test_M1e16_nonpert(self):self.assertTrue(self.z["benchmarks"][0]["one_loop_landau_pole_below_planck"])
 def test_M3e16_latepole(self):self.assertFalse(self.z["benchmarks"][2]["one_loop_landau_pole_below_planck"])
 def test_alpha_high(self):self.assertGreater(self.z["benchmarks"][2]["alpha_at_planck_one_loop"],.3)
 def test_threshold_caveat(self):self.assertIn("CONDITIONAL",self.z["interpretation"])
class AdSBF(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=ads.verify()
 def test_exact_factor(self):self.assertIn("sqrt(3)",self.z["analytic_certificate"]["exact_Rayleigh_negative_gap_factorization"])
 def test_ratio(self):self.assertGreater(self.z["analytic_certificate"]["certified_decimal_BF_gap_lower"],.05)
 def test_simple(self):self.assertIn("0.05",self.z["analytic_certificate"]["claimed_strict_simple_BF_gap_lower"])
 def test_numerical(self):self.assertGreater(self.z["numerical_crosschecks"]["smallest_sample_Rayleigh_gap"],.38)
 def test_eigen_bound(self):self.assertGreaterEqual(self.z["numerical_crosschecks"]["largest_exact_lowest_eigen_gap_minus_Rayleigh"],0)
 def test_number_samples(self):self.assertEqual(self.z["numerical_crosschecks"]["independent_samples"],513)
 def test_scope(self):self.assertIn("two-derivative",self.z["physical_scope"])
 def test_no_R4_claim(self):self.assertIn("No full 11D corrected action",self.z["physical_scope"])
class FlatC(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=link.verify()
 def test_1200(self):self.assertEqual(self.z["integer_signed_triples_checked"],1200)
 def test_g6(self):self.assertEqual(self.z["original_e6_example_6_6"]["g"],6)
 def test_g5(self):self.assertEqual(self.z["Tdual_5_minus5"]["g"],5)
 def test_pairing(self):self.assertEqual(self.z["original_e6_example_6_6"]["unit_linking_fraction"],"1/6")
 def test_non_degenerate(self):self.assertEqual(link.torsion(3,3)["Tor_H4"],"Z_3")
 def test_dual_is_not_Page(self):self.assertIn("NOT",self.z["physical_warning"])
 def test_no_flux_torsion(self):self.assertIn("quantum Page charges",self.z["physical_warning"])
class Qutrit(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=qutrit.verify()
 def test_random(self):self.assertEqual(self.z["random_products_checked"],1500)
 def test_equalities(self):self.assertEqual(len(self.z["independent_equality_checks"]),18)
 def test_tight(self):self.assertIn("equality",self.z["tight_bound"])
 def test_nonuniform(self):self.assertGreater(self.z["nonuniform_calibrated_examples"][1]["robust_positive_gap"],.15)
 def test_null(self):self.assertLessEqual(self.z["exact_sequential_null_first_crossing_500"]["ever_crossed_prob"],.01)
 def test_power(self):self.assertGreater(self.z["exact_sequential_alternative_first_crossing_500"]["ever_crossed_prob"],.99)
 def test_no_hardware(self):self.assertIn("Experimental",self.z["scope"])
 def test_inverse_weighting(self):self.assertIn("small",self.z["loss_unbiasing"])
class KleinNoGo(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=klein.verify()
 def test_order(self):self.assertEqual(self.z["G_order"],660)
 def test_sylow_12(self):self.assertEqual(self.z["C11_sylow_subgroups"],12)
 def test_pair_generation(self):self.assertEqual(self.z["distinct_sylow_pairs_generate_full_G"],66)
 def test_A5_no_fixed(self):self.assertEqual(self.z["A5_trivial_multiplicity"],0)
 def test_A5_irrep(self):self.assertEqual(self.z["A5_character_inner_product_self"],1)
 def test_60(self):self.assertEqual(self.z["distinct_fixed_lines_on_Klein_cubic"],60)
 def test_11(self):self.assertEqual(self.z["G_orbit_11cell_vertices"],11)
 def test_no_direct_vertex_map(self):self.assertIn("IMPOSSIBLE",self.z["vertex_equivariant_map_to_projective_Klein"])
class KleinFlagBijection(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.z=bipair.verify()
 def test_A5(self):self.assertEqual(self.z["generated_A5_order"],60)
 def test_C11(self):self.assertEqual(self.z["generated_C11_order"],11)
 def test_intersection(self):self.assertEqual(self.z["intersection_size"],1)
 def test_order2(self):self.assertEqual(bipair.order(tuple(self.z["explicit_A5_generator_order2"])),2)
 def test_order3(self):self.assertEqual(bipair.order(tuple(self.z["explicit_A5_generator_order3"])),3)
 def test_order5(self):self.assertEqual(self.z["generator_product_order5"],5)
 def test_complete_660(self):self.assertEqual(len(self.z["explicit_flag_table"]),660)
 def test_11x60(self):self.assertEqual(self.z["full_11x60_pairs"],660)
 def test_row(self):self.assertEqual(len(self.z["matrix_entry_flag_index"]),11)
 def test_col(self):self.assertEqual(len(self.z["matrix_entry_flag_index"][0]),60)
 def test_unique(self):self.assertEqual(len(set(x for row in self.z["matrix_entry_flag_index"] for x in row)),660)
 def test_no_incidence_claim(self):self.assertIn("does not prove incidence",self.z["geometry_limit"])
if __name__=="__main__":unittest.main()
