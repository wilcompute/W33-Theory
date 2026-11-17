"""Independent SO(5)/SU5 physical context-selector and 5-front regression."""
import math,sys,unittest
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261117_SU5_adjoint_vacuum_selection as su
import toe_20261117_SUSY_SU5_Fflat_vacuum_competition as sy
import toe_20261117_rank2_projector_dynamic_portal as pr
import toe_20261117_E6_A5_KK_projected_minmax as e6
import toe_20261117_M5_X8_qutrit_minimax as m5

class AdjointShape(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.a=su.quartic_extrema();cls.l=su.landau_potential()
    def test_exact_global_ratio(self):
        self.assertEqual(self.a["exact_critical_point_classification"]["global_minimum_Q"],"7/30")
    def test_exact_global_max(self):
        self.assertEqual(self.a["exact_critical_point_classification"]["global_maximum_Q"],"13/20")
    def test_three_root_saddle(self):
        self.assertEqual(self.a["exact_critical_point_classification"]["three_distinct_eigenvalues_Q_by_partition"],{"3_1_1":"1/2","2_2_1":"1/4"})
    def test_hessian_positive(self):
        self.assertTrue(self.a["all_local_shape_eigenvalues_positive"])
    def test_SU3_tangent(self):
        self.assertEqual(self.a["angular_constrained_hessian_eigenvalues"]["SU3_traceless_2_modes"],"2/3")
    def test_SU2_tangent(self):
        self.assertEqual(self.a["angular_constrained_hessian_eigenvalues"]["SU2_traceless_1_mode"],"8/3")
    def test_massive_gauge_bosons(self):
        self.assertEqual(self.l["broken_generator_count"],12)
    def test_positive_kappa_selects_3plus2(self):
        x=self.l["example"]
        self.assertLess(x["energy_SU3_SU2_U1"],x["energy_SU4_U1"])
    def test_multistart(self):
        v=su.optimize_restarts(restarts=12)
        self.assertTrue(v["all_restarts_reached_7_over_30"])

class PhysicalGaugeVsGlobal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=su.contextual_orbits()
    def test_A5_global_orbit(self):
        self.assertEqual((self.z["A5_order"],self.z["distinct_unordered_two_subsets"]),(60,10))
    def test_10_per_sign(self):
        self.assertEqual(self.z["Z2_even_potential_3plus2_diagonal_minima"],20)
    def test_gauge_equivalence(self):
        self.assertIn("gauge-equivalent",self.z["SU5_gauge_orbit_statement"])
    def test_global_domain_caveat(self):
        self.assertIn("genuinely global",self.z["global_discrete_case"])
    def test_Z2_sign_warning(self):
        self.assertIn("NOT conjugate",self.z["Z2_warning"])
    def test_full_80_seeds(self):
        self.assertTrue(su.verify()["numerical_multistart_stress"]["all_restarts_reached_7_over_30"])

class RelativePortal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=pr.verify()
    def test_portal_3plus2(self):
        self.assertEqual(self.z["normalized_eigenvalues"],"(2,2,2,-3,-3)/sqrt(30)")
    def test_rank2_var_principle(self):
        self.assertIn("sqrt(6/5)",self.z["Cauchy_Schwarz_theorem"])
    def test_no_TrPhi4_needed(self):
        self.assertEqual(self.z["fixed_norm_quartic_ratio"],"7/30 arises without a TrPhi4 term")
    def test_gap(self):
        self.assertGreater(self.z["relative_orientation_gap"],0)
    def test_sign_bias(self):
        self.assertGreater(self.z["opposite_sign_relaxed_Q_energy_penalty"],0)
    def test_radial_root(self):
        self.assertGreater(self.z["reference_parameters"]["selected_radial_norm"],1.2)
    def test_conditional_pinning(self):
        self.assertIn("strong-pinning",self.z["rank2_pinning_effective_potential"])
    def test_gauge_invariant(self):
        self.assertIn("RELATIVE",self.z["physically_distinct_vs_gauge"])
    def test_cauchy_example(self):
        self.assertEqual(self.z["random_traceless_matrix_controls"],120)

class SUSYVacuum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=sy.verify()
    def test_three_Fflat_branches(self):
        self.assertEqual(len(set(x["TrPhi2"] for x in self.z["Fflat_branches"]["branches"])),2)
    def test_fterms_zero(self):
        self.assertTrue(all(x["VF"]==0 for x in self.z["Fflat_branches"]["branches"]))
    def test_D_terms_zero(self):
        self.assertTrue(all(x["D_flat_if_Hermitian"] for x in self.z["Fflat_branches"]["branches"]))
    def test_rigid_zero_energy(self):
        self.assertIn("degenerate",self.z["Fflat_branches"]["no_unique_SUSY_vacuum"])
    def test_soft_SM_preferred_first_order(self):
        self.assertTrue(self.z["soft_first_order"]["prefers_SM_over_SU4_and_origin_at_first_order"])
    def test_soft_gap_coefficient(self):
        self.assertIn("250",self.z["soft_first_order"]["energy_SM_minus_SU4"])
    def test_supergravity_caveat(self):
        self.assertIn("Kähler",self.z["Fflat_branches"]["SUGRA_warning"])

class WiderFiveFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=e6.verify();cls.b=m5.verify()
    def test_A5_transitive(self):
        self.assertTrue(self.a["A5_E6_context"]["entire_context_orbit_transitive"])
    def test_A5_no_unique_selection(self):
        self.assertIn("cannot",self.a["A5_E6_context"]["invariant_selection_no_go"])
    def test_KK_minmax_off_block(self):
        self.assertIn("regardless",self.a["KK_projected_minmax"]["theorem"])
    def test_M5_wedge_no_charge_claim(self):
        self.assertIn("no proof",self.b["M5_flux_wedge"]["critical_caveat"])
    def test_X8_reflection_scope(self):
        self.assertIn("externally homogeneous",self.b["X8_selection"]["consequence"])
    def test_fourMUB_minimax(self):
        self.assertEqual(self.b["qutrit_basis_optimality"]["calibrated_null"],.51)
    def test_fourMUB_uniform_optimal(self):
        self.assertIn("Uniform",self.b["qutrit_basis_optimality"]["uniform_optimality"])
    def test_herald_prebasis(self):
        self.assertIn("BEFORE",self.b["qutrit_basis_optimality"]["pre_setting_herald_loophole_safe_theorem"])
import toe_20261117_E6_adjoint_invariant_shape_obstruction as e6inv

class E6InvariantObstruction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=e6inv.verify()
    def test_cartan_six(self):
        self.assertEqual(self.z["Cartan_dimension"],6)
    def test_cubic_zero(self):
        self.assertIn("=0",self.z["polynomial_identity_3"])
    def test_quartic_exact(self):
        self.assertIn("/12",self.z["polynomial_identity_4"])
    def test_p5_nonzero(self):
        self.assertIn("not identically",self.z["first_nontrivial_odd_trace"])
    def test_hypercharge_moments(self):
        self.assertEqual(self.z["Y_integer_weight_traces"],{"2":180,"3":0,"4":2700,"5":-4320})
    def test_degree_list(self):
        self.assertEqual(self.z["degree_list_external_group_theory"],[2,5,6,8,9,12])
    def test_no_single_adjoint_selector(self):
        self.assertIn("cannot",self.z["consequence"])
    def test_samples(self):
        self.assertEqual(len(self.z["samples"]),3)

if __name__=="__main__":unittest.main()
