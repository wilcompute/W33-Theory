"""Independent checks of explicit H27 positive Einstein free cover,
E6 Hesse cubic/Higgs selection, local PW covariance and tripartite-qutrit
GHZ static three-party target. Does not claim a physical TOE."""
import unittest,sys,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_H27_Einstein_Hesse_E8_Higgs_PW_GHZ as T

class H27NewInterfaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=T.run()
        cls.g=cls.r["positive_Einstein_H27_cover"]
        cls.c=cls.r["E6_H27_Hesse_cubic"]
        cls.h=cls.r["H27_elementary_Higgs_obstruction"]
        cls.p=cls.r["PW_site_hopping_covariance"]
        cls.q=cls.r["triple_GHZ_pairwise_classical_target"]

    def test_all_27_group_matrices_have_group_law(self):
        self.assertLess(self.g["group_law_max_error"],2e-13)
    def test_group_rep_matrix_unitarity(self):
        for x in T.G:
            a=T.rep(x)
            self.assertLess(np.max(abs(a.conj().T@a-np.eye(3))),1e-12)
    def test_group_rep_det1(self):
        for x in T.G:
            self.assertLess(abs(np.linalg.det(T.rep(x))-1),1e-12)
    def test_no_fixed_point_all_26_nontrivial(self):
        self.assertEqual(sum(self.g["nonidentity_elements_covered_by_factor"].values()),26)
        self.assertGreater(self.g["minimal_moving_eigenvalue_gap"],1.7)
    def test_two_center_elements_removed_by_S5(self):
        self.assertEqual(self.g["nonidentity_elements_covered_by_factor"]["center"],2)
    def test_18_quotient_elements_removed_by_first_character(self):
        self.assertEqual(self.g["nonidentity_elements_covered_by_factor"]["first_character"],18)
    def test_six_quotient_elements_removed_by_second_character(self):
        self.assertEqual(self.g["nonidentity_elements_covered_by_factor"]["second_character"],6)
    def test_einstein_cover_dimension11(self):
        self.assertEqual(self.g["quotient_dimension"],11)
    def test_einstein_constant1(self):
        self.assertEqual(self.g["quotient_positive_Einstein_Ricci_coefficient"],1)
    def test_scalar_curvature11(self):
        self.assertEqual(self.g["quotient_scalar_curvature"],11)
    def test_quotient_pi1_H27(self):
        self.assertEqual(self.g["quotient_pi1_order"],27)
    def test_quotient_positive_volume(self):
        self.assertAlmostEqual(self.g["volume_float"],1024*math.pi**7/27,places=6)
    def test_quotient_Kunneth_betti(self):
        self.assertEqual(self.g["quotient_rational_Betti"],
                         {"0":1,"3":2,"5":1,"6":1,"8":2,"11":1})
    def test_quotient_no_real_4_or_7_flux_classes(self):
        self.assertEqual((self.g["quotient_Betti4"],self.g["quotient_Betti7"]),(0,0))
    def test_geometry_not_seven_dim_G2(self):
        self.assertIn("NOT an internal seven-manifold",self.g["physical_limit"])
    def test_geometry_norm_Ricci_flow_scale_unstable(self):
        self.assertEqual(self.g["normalized_Ricci_flow_relative_scale_linear_eigenvalues"],[2,2])
        self.assertTrue(self.g["volume_preserving_scalar_curvature_Hessian_positive"])
    def test_geometry_flow_not_physical_BF(self):
        self.assertIn("not an 11D",self.g["normalized_Ricci_flow_scope"])

    def test_hesse_degree3_monomial_count(self):
        self.assertEqual(self.c["symmetric_cubic_monomial_count"],10)
    def test_hesse_H27_symmetric_cubic_dim2(self):
        self.assertEqual(self.c["invariant_symmetric_cubic_space_dimension"],2)
    def test_hesse_projector_idempotent(self):
        self.assertLess(self.c["projector_idempotence_error"],1e-12)
    def test_hesse_explicit_basis_sum_cubes(self):
        self.assertEqual(self.c["invariant_polynomial_1"],"x^3+y^3+z^3")
    def test_hesse_explicit_basis_xyz(self):
        self.assertEqual(self.c["invariant_polynomial_2"],"x*y*z")
    def test_hesse_tensor_cube_dim3(self):
        self.assertEqual(self.c["full_tensor_cube_invariant_dimension"],3)
    def test_hesse_alternating_invariant_dim1(self):
        self.assertEqual(self.c["alternating_tensor_cube_invariant_dimension"],1)
    def test_hesse_full_SU3_symmetric_invariant_dim0(self):
        self.assertEqual(self.c["full_SU3_family_symmetric_cubic_invariant_dimension"],0)
    def test_E6_symmetric_d_SU3_epsilon_zero_for_same_chiral_field(self):
        self.assertTrue(self.c["E6_symmetric_d_times_SU3_epsilon_identical_commuting_superfield_zero"])
        self.assertLess(self.c["cubic_contraction_numerical_residual"],1e-11)
    def test_hesse_effective_cubic_only_below_SU3(self):
        self.assertIn("broken family SU3",self.c["scope"])
        self.assertFalse(self.c["UV_E8_cubic_invariant"])
    def test_hesse_two_effective_Yukawa_family_channels(self):
        self.assertEqual(self.c["low_energy_E6_times_H27_symmetric_cubic_family_channels"],2)
    def test_hesse_parameter_not_derived(self):
        self.assertIn("One complex ratio",self.c["effective_texture_moduli"])

    def test_H27_no_invariant_vector_triplet(self):
        self.assertEqual(self.h["H27_invariants_in_family3"],0)
        self.assertLess(self.h["family3_projector_max_abs"],1e-12)
    def test_H27_no_invariant_antitriplet(self):
        self.assertEqual(self.h["H27_invariants_in_family3bar"],0)
    def test_H27_one_invariant_3times3bar(self):
        self.assertEqual(self.h["H27_invariants_in_family3_tensor_3bar"],1)
        self.assertEqual(self.h["triplet_tensor_antitriplet_projector_rank"],1)
    def test_H27_no_invariant_adjoint8(self):
        self.assertEqual(self.h["H27_invariants_in_family_adjoint8"],0)
    def test_H27_78_invariant_before_W7(self):
        self.assertEqual(self.h["full_E8_adj_H27_parallel_invariant_subspace_dim"],78)
    def test_H27_14_invariant_after_c3_W7(self):
        self.assertEqual(self.h["after_order7_c3_Wilson_parallel_invariant_dim"],14)
    def test_no_elementary_27x3_parallel_Higgs(self):
        self.assertTrue(self.h["no_H27_invariant_elementary_27x3_Higgs_VEV"])
    def test_Higgs_composites_possible_not_verified(self):
        self.assertIn("composite fields",self.h["caveat"])

    def test_PW_triangle_ratio(self):
        self.assertGreater(self.p["ratio_max_min_distance"],1.13)
        self.assertLess(self.p["ratio_max_min_distance"],1.15)
    def test_PW_two_short_edges(self):
        self.assertAlmostEqual(self.p["pairwise_distances_sorted"][0],
                               self.p["pairwise_distances_sorted"][1],places=10)
    def test_PW_one_long_edge(self):
        self.assertGreater(self.p["pairwise_distances_sorted"][2],
                           self.p["pairwise_distances_sorted"][1])
    def test_PW_hopping_long_short_ratio(self):
        self.assertAlmostEqual(self.p["relative_long_edge_to_short_edge_hopping"],
                               .34797063539454,places=11)
    def test_PW_H27_shift_commutator_nonzero(self):
        self.assertGreater(self.p["commutator_X_frobenius"],.03)
    def test_PW_H27_clock_commutator_nonzero(self):
        self.assertGreater(self.p["commutator_Z_frobenius"],.10)
    def test_PW_H27_twirl_scalar_zero(self):
        self.assertLess(self.p["H27_twirl_hopping_max_abs"],1e-12)
    def test_PW_tunneling_is_toy_not_real_Dirac(self):
        self.assertIn("NOT the continuum PW",self.p["physical_scope"])

    def test_GHZ_each_pair_identical_to_classical_diagonal(self):
        self.assertLess(self.q["pairwise_reduced_density_max_error"],1e-12)
        self.assertTrue(self.q["each_pairwise_reduction_separable"])
    def test_GHZ_three_party_X_coherence_differs(self):
        self.assertEqual(self.q["GHZ_vs_classical_XXX_expectation"],[1,0])
    def test_GHZ_unique_triple_stabilizer_projector(self):
        self.assertEqual(self.q["joint_three_stabilizer_projector_rank"],1)
        self.assertTrue(self.q["P_GHZ_equals_projector_Xsum0_Z12equal_Z23equal"])
    def test_GHZ_biseparable_fidelity_bound(self):
        self.assertAlmostEqual(self.q["biseparable_fidelity_upper_bound"],1/3,places=12)
    def test_GHZ_dephased_visibility(self):
        self.assertEqual(self.q["dephased_visibility_t"],.75)
        self.assertAlmostEqual(self.q["GHZ_fidelity"],5/6,places=12)
    def test_GHZ_noisy_pairs_Z_probability(self):
        self.assertGreater(self.q["measured_equal_Z12_probability"],.98)
    def test_GHZ_noisy_triple_X_probability(self):
        self.assertGreater(self.q["measured_X_basis_three_labels_sum_mod3_zero_probability"],.80)
    def test_GHZ_three_setting_fidelity_lower(self):
        self.assertGreater(self.q["fidelity_from_three_setting_union_lower_bound"],.77)
    def test_GHZ_finite_sample_n200_per_setting(self):
        self.assertEqual(self.q["per_setting_accepted_n"],200)
        self.assertEqual(self.q["total_accepted_trials"],600)
    def test_GHZ_model_power_gt99pct(self):
        self.assertGreater(self.q["exact_IID_GHZ_model_power_under_readout"],.99)
    def test_GHZ_Hoeffding_typeI_composite(self):
        self.assertEqual(self.q["statistical_null_typeI_at_most"],.01)
    def test_GHZ_does_not_prove_process_tensor(self):
        self.assertIn("not automatically produce",self.q["scope"])
    def test_no_TOE_claim(self):
        self.assertFalse(self.r["valid_TOE"])

if __name__=="__main__":unittest.main()
