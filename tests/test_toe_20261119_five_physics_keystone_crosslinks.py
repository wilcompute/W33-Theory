"""Five TOE fronts and two cross-front mathematical falsifiers regression."""
import sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_handlebody_W7_topological_trilemma as t
import toe_20261119_source_two_ten_localized_flavor_sieve as f
import toe_20261119_SU5_brane_projector_two_loop_RGE as g
import toe_20261119_BDG4_Rao_Blackwell_smearing as c
import toe_20261119_five_qubit_photon_erasure_concatenation as p

class FivePhysicsKeystones(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t=t.run()
        cls.f=f.run()
        cls.g=g.run()
        cls.c=c.run()
        cls.p=p.run()

    def test_topology_C7_exact_primitive_unit_checks(self):
        self.assertEqual(len(self.t["exact_inverse_certificates_zk_minus_one"]),6)
        self.assertIn("z**6",self.t["C7_polynomial"])
    def test_topology_unique_spinor_character(self):
        self.assertEqual(self.t["unique_intrinsic_16_line_character_all_weights_nontrivial"],5)
        self.assertEqual(len(self.t["all_16_weight_total_characters"]),16)
        self.assertTrue(all(x!=0 for x in self.t["all_16_weight_total_characters"]))
    def test_topology_exact_three_per_SM_component_no_H2_mirrors(self):
        self.assertEqual(self.t["16_local_system_betti"],[0,48,0,0])
        self.assertEqual(self.t["three_equal_components_per_SM_weight"],3)
    def test_topology_adjoint_exotic_cost(self):
        self.assertEqual(self.t["Spin10_adjoint_W7_invariant_dimension"],13)
        self.assertEqual(self.t["Spin10_adjoint_W7_broken_dimension"],32)
        self.assertEqual(self.t["at_least_unbroken_gauge_adjoint_chiral_candidates"],52)
        self.assertEqual(self.t["total_adjoint_H1_chiral_candidates"],148)
    def test_nonmirror_W7_flat_character_blocks_up_yukawa_without_local_defect(self):
        self.assertEqual(self.t["uniform_flat_character_up_Higgs_5_weak"],3)
        self.assertEqual(self.t["uniform_flat_character_down_Higgs_bar5_weak"],4)
        self.assertEqual(self.t["uniform_up_Yukawa_total_flat_character_mod7"],6)
        self.assertEqual(self.t["uniform_down_Yukawa_total_flat_character_mod7"],0)
        self.assertEqual(self.t["additional_singlet_flat_character_needed_for_up"],1)
        self.assertTrue(self.t["trivial_character_spurion_cannot_complete_up_flat_invariant"])
    def test_topology_bulk_Yukawa_cup_no_go(self):
        self.assertEqual(self.t["absolute_H2_of_handlebody_for_any_flat_local_system"],0)
        self.assertIn("zero",self.t["bulk_H1_cup_H1_and_all_absolute_triple_cups"])
    def test_lens_punctures_keep_at_least_one_mirror(self):
        for a in self.t["lens_spherical_defect_index3_mirror_comparison"]:
            self.assertEqual(a["index"],3)
            self.assertGreaterEqual(a["twisted_H2_mirror"],1)
    def test_S3_invariant_flavor_has_double_eigenvalue(self):
        self.assertEqual(self.t["S3_invariant_Yukawa_eigenvalues"],["a+2b","a-b","a-b"])
        self.assertEqual(self.t["S3_invariant_two_Yukawa_commutator"],0)
    def test_S3_requires_dynamical_geometry_selector(self):
        self.assertIn("distinguish",self.t["flavor_escape"])
    def test_flavor_exact_twelve_minimal_U1_spurion_operators(self):
        self.assertEqual(len(self.f["complete_12_charge_neutral_entries"]),12)
        self.assertEqual(self.f["not_gauge_allowed_or_degree_limit"],[])
        self.assertEqual(self.f["source_10_fields"],["10_34","10_24"])
    def test_flavor_gaussian_overlap_normalized_and_positive(self):
        for a in self.f["complete_12_charge_neutral_entries"]:
            self.assertGreater(a["gaussian_overlap"],0)
            self.assertGreater(a["positive_effective_coupling"],0)
    def test_flavor_both_Yukawa_matrices_nondegenerate(self):
        self.assertEqual(np.linalg.matrix_rank(np.asarray(self.f["light_Yu"])),3)
        self.assertEqual(np.linalg.matrix_rank(np.asarray(self.f["light_Yd"])),3)
    def test_flavor_two_sources_have_nonzero_CKM_while_one_does_not(self):
        self.assertGreater(self.f["noncommuting_quark_mass_matrices_frobenius_norm"],1e-8)
        self.assertTrue(self.f["one_source_ten_alone_commutes_and_has_trivial_CKM"])
    def test_flavor_toy_CKM_is_not_observed_real_world(self):
        self.assertGreater(np.max(np.abs(np.asarray(self.f["abs_CKM_in_toy_model_with_low_to_high_eigenvalue_order"])-
                                        np.eye(3))),.8)
        self.assertIn("No 7D G2 overlap",self.f["strong_scope"])
    def test_SU5_octet_boundary_projector_is_exact_rank_eight(self):
        b=self.g["gauge_boundary"]
        self.assertEqual((b["SM_octet_rank"],b["SM_weak_triplet_rank"]),(8,3))
        self.assertGreater(b["SU5_non_covariance_witness_norm"],.01)
        self.assertLess(b["SM_covariance_witness_norm"],1e-12)
    def test_two_loop_doublet_trace_matrix_exact(self):
        self.assertEqual(self.g["N1_two_loop_extra_doublet_B"],
            [["9/25","9/5","0"],["3/5","7","0"],["0","0","0"]])
    def test_two_loop_triplet_trace_matrix_exact(self):
        self.assertEqual(self.g["N1_two_loop_extra_triplet_B"],
            [["8/75","0","32/15"],["0","0","0"],["4/15","0","34/3"]])
    def test_two_loop_full_multiplet_universal_one_loop(self):
        self.assertEqual(self.g["extra_complete_SU5_5_b"],["1","1","1"])
    def test_two_loop_GUT_scenarios_all_integrated_finite(self):
        self.assertEqual(len(self.g["scenarios"]),5)
        for a in self.g["scenarios"]:
            self.assertTrue(np.isfinite(a["alpha_inverse_at_MU"]).all())
            self.assertTrue(np.isfinite(a["unification_mismatch_at_MU_12_13_23"]).all())
    def test_triplet_proton_enhancement_is_ratio_not_absolute_prediction(self):
        self.assertEqual(self.g["colored_triplet_d5_proton_rate_relative_if_mass_1e14_vs_1e16"],10000.)
        self.assertIn("NOT a direct",self.g["illustrative_proton_decay_experimental_reference"])
    def test_causal_exact_thinning_identity(self):
        for eps in (.2,.5,.8,1.):
            for n in (0,1,2,3,5,9,17,24):
                from math import comb
                direct=sum(c.weights[k]*comb(n,k)*eps**k*(1-eps)**(n-k)
                           for k in range(min(3,n)+1))
                self.assertAlmostEqual(direct,c.smooth_weight(n,eps),places=10)
    def test_causal_rho_parent_samples_and_effective_density(self):
        self.assertEqual(len(self.c["sample_results"]),6)
        for x in self.c["sample_results"]:
            self.assertAlmostEqual(x["effective_density"],
                x["parent_sprinkling_density"]*x["retention_eps"])
    def test_causal_variance_exact_theorem_and_MC(self):
        self.assertIn("Var(B_smoothed",self.c["Rao_Blackwell_theorem"])
        for x in self.c["sample_results"]:
            if x["retention_eps"]<1:
                self.assertLess(x["variance_ratio_smooth_over_independent_sharp"],.12)
    def test_causal_method_has_nonlocality_tradeoff(self):
        self.assertIn("not a proof",self.c["scope"].lower())
    def test_photon_perfect_code_and_all_3_erasure_subset_failure(self):
        self.assertTrue(self.p["independent_all_ten_three_erasure_logical_support_failures_verified"])
        self.assertEqual(self.p["nontrivial_erasure_threshold"],.5)
    def test_photon_erasure_recursion_exact(self):
        self.assertEqual(self.p["exact_level_map"].split("=")[1].split(" ")[0],
                         "10p^3-15p^4+6p^5")
        self.assertAlmostEqual(p.logical_failure(.1),.00856,places=12)
    def test_photon_independent_fifty_qubits_required_level_two(self):
        x=self.p["resource_scenarios"][0]
        self.assertEqual(x["minimal_levels_certified_by_union_bound"],2)
        self.assertEqual(x["total_physical_photonic_qubits"],1250)
    def test_photon_thousand_qubits_deep_erasure_correction(self):
        x=self.p["resource_scenarios"][1]
        self.assertEqual(x["minimal_levels_certified_by_union_bound"],3)
        self.assertEqual(x["total_physical_photonic_qubits"],125000)
        self.assertLess(x["total_error_union_upper_bound"],1e-6)
    def test_photon_below_eta_half_threshold_has_no_concatenation_gain(self):
        x=self.p["resource_scenarios"][-1]
        self.assertIsNone(x["minimal_levels_certified_by_union_bound"])
        self.assertIn("not derived",self.p["no_ft_gate_escape"])
    def test_five_physics_fronts_do_not_claim_TOE(self):
        self.assertIn("not proven",self.t["scope"])
        self.assertIn("No actual",self.g["limitations"])
        self.assertIn("No",self.p["scope"])

if __name__=="__main__":unittest.main()
