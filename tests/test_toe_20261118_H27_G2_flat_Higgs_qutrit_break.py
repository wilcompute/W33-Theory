"""Independent checks of H27 space-form obstruction, G2 flat Dirac gap,
E8 parallel-adjoint rank, PW x triplet multiplicity and noisy SWAP break."""
import unittest,sys,math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.stats import binom
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_H27_G2_flat_Higgs_qutrit_break as T

class H27G2Memory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=T.run()
        cls.h=cls.d["finite_H27_families"]
        cls.sp=cls.d["spherical_space_form_no_go"]
        cls.g=cls.d["smooth_nearlyG2_flat_Dirac_no_go"]
        cls.e=cls.d["E8_parallel_Higgs_and_family_multiplicity"]
        cls.q=cls.d["qutrit_controlled_memory"]

    def test_H27_order(self):
        self.assertEqual(self.h["order"],27)
    def test_H27_associativity_exhaustive(self):
        G=[(a,b,c) for a in range(3) for b in range(3) for c in range(3)]
        for x in G:
            for y in G:
                for z in G:
                    self.assertEqual(T.hmul(T.hmul(x,y),z),T.hmul(x,T.hmul(y,z)))
    def test_H27_inverse_exhaustive(self):
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    g=(a,b,c)
                    self.assertEqual(T.hmul(g,T.hinv(g)),(0,0,0))
                    self.assertEqual(T.hmul(T.hinv(g),g),(0,0,0))
    def test_H27_irreducible_count(self):
        self.assertEqual(self.h["conjugacy_class_count"],11)
        self.assertEqual(len(self.h["irreducible_dimensions"]),11)
    def test_H27_irreducible_squared_dimension(self):
        self.assertEqual(self.h["sum_of_squares"],27)
    def test_H27_nontrivial_center_is_3D(self):
        self.assertEqual(self.h["irreducible_dimensions"],[1]*9+[3,3])
        self.assertTrue(self.h["all_one_dimensional_center_characters_trivial"])
    def test_H27_two_conjugate_triplets(self):
        self.assertEqual(self.h["two_nontrivial_center_characters"],["omega","omega^2"])
    def test_H27_orthogonality(self):
        self.assertLess(self.h["character_orthogonality_error"],1e-12)
    def test_H27_conjugacy_class_sizes(self):
        self.assertEqual(self.h["class_sizes"],[1,1,1]+[3]*8)
    def test_H27_irrep_already_prior(self):
        self.assertIn("already proved",self.h["prior_art"])

    def test_C3_squared_abelian_subgroup(self):
        self.assertEqual(self.sp["abelian_subgroup"],"C3 x C3")
        self.assertEqual(self.sp["subgroup_order"],9)
    def test_every_abelian_character_has_nontrivial_kernel(self):
        self.assertEqual(sorted(self.sp["all_nine_character_kernel_sizes"]),
                         [3]*8+[9])
    def test_H27_free_round_sphere_impossible(self):
        self.assertFalse(self.sp["free_orthogonal_action_on_any_round_sphere_possible"])
    def test_H27_free_topological_sphere_impossible(self):
        self.assertFalse(self.sp["free_topological_action_on_any_standard_sphere_possible"])
    def test_H27_gauge_holonomy_NOT_automatically_excluded(self):
        self.assertIn("NOT a no-go",self.sp["physical_scope"])

    def test_G2_positive_Einstein_coefficient(self):
        self.assertEqual(self.g["Ricci_coefficient"],"3*tau0^2/8")
    def test_G2_positive_scalar(self):
        self.assertEqual(self.g["scalar_curvature"],"21*tau0^2/8")
    def test_G2_flat_Dirac_square_gap(self):
        self.assertEqual(self.g["Dirac_squared_spectral_lower_bound"],
                         "21*tau0^2/32")
    def test_G2_FR_tau2L_gap(self):
        self.assertEqual(self.g["at_tau0_2_overL_Dirac_squared_L2_lower_bound"],"21/8")
    def test_G2_flat_twisted_no_zero(self):
        self.assertTrue(self.g["no_ordinary_flat_twisted_Dirac_zero_modes"])
    def test_G2_Myers_bound(self):
        self.assertEqual(self.g["Myers_at_tau0_2_overL_diameter_upper_bound"],"2*pi*L")
    def test_G2_positive_Ricci_pi1_finite(self):
        self.assertTrue(self.g["fundamental_group_finite"])
    def test_G2_real_H1_zero(self):
        self.assertTrue(self.g["real_first_cohomology_zero"])
    def test_G2_source_free_abelian_harmonic_one_form_vanishes(self):
        self.assertTrue(self.g["source_free_closed_harmonic_real_one_forms_zero"])
    def test_G2_no_overclaim_flux_coupled(self):
        self.assertIn("Does not apply",self.g["caveat"])

    def test_E8_Wilson_center_dim14(self):
        self.assertEqual(self.e["Wilson_E6_c3_unbroken_dimension"],14)
    def test_E8_Wilson_rank6_three_centers(self):
        self.assertEqual(self.e["residual_center_dimension"],3)
        self.assertEqual(self.e["residual_extra_U1_beyond_SM"],2)
    def test_E8_parallel_adjoint_cannot_fix_u1(self):
        self.assertTrue(self.e["all_globally_covariantly_parallel_adjoint_VEVs_preserve_at_least_U1_cubed"])
    def test_PW_three_modes_times_H27_three_is_nine(self):
        self.assertEqual(self.e["spatial_PW_scalar_L2_zero_modes"],3)
        self.assertEqual(self.e["independent_H27_Schrodinger_family_fiber_dim"],3)
        self.assertEqual(self.e["naive_commuting_tensored_L2_zero_modes"],9)
    def test_PW_quartic_critical_triple_non_equilateral(self):
        self.assertGreater(self.e["tilted_quartic_triangle_longest_over_shortest"],1.13)
        self.assertLess(self.e["tilted_quartic_triangle_longest_over_shortest"],1.15)
        self.assertFalse(self.e["tilted_quartic_has_euclidean_C3_rotation_permuting_sites"])
    def test_PW_geometry_recompute(self):
        p=np.array(self.e["tilted_quartic_critical_points_xy"])
        for x,y in p:
            z=complex(x,y)
            self.assertLess(abs(z.conjugate()**3-z-1),1e-9)
    def test_PW_not_claiming_physical_index(self):
        self.assertIn("conditional product",self.e["physics_limit"])

    def test_qutrit_all_3_middle_break_resets(self):
        self.assertEqual(self.q["independently_prepared_middle_reset_values"],[0,1,2])
    def test_qutrit_coherent_full_fidelity(self):
        self.assertEqual(self.q["coherent_output_fidelity"],1)
    def test_qutrit_classical_dephased_EB(self):
        self.assertAlmostEqual(self.q["dephased_environment_classical_memory_fidelity"],1/3,places=11)
    def test_qutrit_fresh_E_no_memory(self):
        self.assertAlmostEqual(self.q["no_memory_depolarized_environment_fidelity"],1/9,places=11)
    def test_qutrit_noisy_storage_fidelity(self):
        self.assertAlmostEqual(self.q["expected_return_fidelity"],7/9,places=11)
    def test_qutrit_four_MUB_match(self):
        self.assertAlmostEqual(self.q["expected_local_MUB_match"],5/6,places=11)
    def test_qutrit_MUB_two_design_identity(self):
        self.assertLess(self.q["four_MUB_2design_residual"],2e-12)
    def test_qutrit_three_time_full_CPTP(self):
        self.assertLess(self.q["exact_CPTP_output_residual_max"],1e-12)
    def test_qutrit_classical_memory_27_trial_statistical_budget(self):
        a=self.q["classical_memory_fixed_n_99pct_typeI_90pct_power"]
        self.assertEqual((a["accepted_trials"],a["min_matches"]),(27,20))
        self.assertLessEqual(a["exact_typeI"],.01)
        self.assertGreaterEqual(a["design_power"],.90)
    def test_qutrit_intrinsic_three_dim_317_budget(self):
        a=self.q["intrinsic_qutrit_fixed_n_99pct_typeI_90pct_power"]
        self.assertEqual((a["accepted_trials"],a["min_matches"]),(317,256))
        self.assertLessEqual(a["exact_typeI"],.01)
        self.assertGreaterEqual(a["design_power"],.90)
    def test_qutrit_readout_calibrated_budgets(self):
        r=self.q["detector_symmetric_ternary_error_designs"]
        self.assertEqual([x["intrinsic_SN3_99pct_90pct_power"]["accepted_trials"] for x in r],
                         [317,348,389])
    def test_qutrit_no_genuine_three_time_only_claim(self):
        self.assertIn("NOT_PROVEN",self.q["status_of_2026_Beyer_genuine_three_time_only_target"])
    def test_qutrit_no_photons_claimed(self):
        self.assertIn("No real photon",self.q["physical_limit"])
    def test_no_complete_theory_claim(self):
        self.assertTrue(self.d["no_TOE_claim"])

if __name__=="__main__":unittest.main()
