"""Regression certificates for next five W33/TOE frontiers (2026-11-19)."""
import math
import pathlib
import sys
import unittest
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_w33_logical_decoder_certificate as code
import toe_20261119_physics_followthrough as physics
import toe_20261119_w33_40_qutrit_css as prev


class FiveFrontierFollowthroughTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.C=code.certify()
        cls.P=physics.certify()

    def test_modular_middle_logical_and_orthogonality(self):
        C=self.C
        self.assertEqual(C["logical_quotient_dimension"],19)
        self.assertEqual(C["logical_Gram_rank_mod3"],19)
        self.assertEqual(C["logical_Gram_determinant_mod3"],1)
        self.assertEqual(C["logical_symmetry"]["logical_action_kernel_order"],1)

    def test_logical_point_group_faithful_action(self):
        self.assertEqual(self.C["logical_symmetry"]["generated_projective_symplectic_group_order"],25920)
        self.assertTrue(self.C["logical_symmetry"]["representation_preserves_symmetric_dot_quotient"])
        pgl=self.C["full_PGL_orthogonal_action"]
        self.assertEqual(pgl["projective_linear_group_order"],12130560)
        self.assertTrue(pgl["logical_PGL_action_faithful"])
        self.assertTrue(pgl["all_13_generators_preserve_19D_dot_Gram"])
        self.assertEqual(pgl["elementary_transvection_nilpotent_ranks"],[10,3,0])

    def test_optimal_stabilizer_basis_and_depth_graph(self):
        x=self.C["optimal_check_basis"]
        self.assertEqual((x["checks_rank_X"],x["checks_rank_Z"]),(11,10))
        self.assertEqual((x["old_check_interactions"],
                          x["proven_minimum_independent_check_interactions"]),(413,323))
        self.assertEqual(x["data_qudit_max_incidence"],9)
        self.assertEqual(x["minimum_ancilla_data_two_qudit_rounds"],18)
        self.assertEqual(x["parallel_bias_aware_decoder_syndrome_sizes_on_optimized_checks"],[81,3201])
        self.assertEqual(x["parallel_bias_aware_decoder_exact_component_patterns"],259281)
        X=prev.checks()[2][x["X_basis_closed_neighborhood_row_ids"]]
        Z=np.array(x["Z_basis_vectors"],dtype=np.int64)
        self.assertTrue(np.all((X@Z.T)%3==0))
        self.assertEqual(np.count_nonzero(X)+np.count_nonzero(Z),323)
        layers=x['explicit_collision_free_gate_layers']
        self.assertEqual(len(layers),18)
        self.assertEqual(sum(len(layer) for layer in layers),323)
        all_edges=[]
        for layer in layers:
            self.assertEqual(len({e[0] for e in layer}),len(layer))
            self.assertEqual(len({e[1] for e in layer}),len(layer))
            all_edges.extend(tuple(e) for e in layer)
        self.assertEqual(len(set(all_edges)),323)
        self.assertTrue(all(np.vstack((X,Z))[a,b]==v for a,b,v in all_edges))

    def test_classical_full_weight_enumerator_matches_existing_literature(self):
        c=self.C["optimal_check_basis"]
        h10=c["prior_classical_C10_weight_enumerator"]
        h11=c["prior_classical_C11_weight_enumerator"]
        self.assertEqual(h10["18"],1560)
        self.assertEqual(h11["13"],80)
        self.assertEqual(sum(h10.values()),3**10)
        self.assertEqual(sum(h11.values()),3**11)

    def test_single_pauli_and_two_fault_decoder(self):
        d=self.C["decoder"]
        self.assertEqual(d["full_single_physical_qutrit_Pauli_faults_exactly_corrected"],320)
        self.assertEqual(d["two_distinct_fault_cases"],49920)
        self.assertEqual(d["two_fault_cases_exactly_corrected_by_separate_t1_decoder"],6240)
        self.assertAlmostEqual(d["two_fault_conditional_exact_recovery_fraction"],.125)
        for v in d["probability_guarantees"]:
            self.assertGreaterEqual(v["provably_corrected_probability_lower_bound"],0)

    def test_uniform_magic_transversal_no_go(self):
        x=self.C["transversal_gate_nogos"]
        self.assertEqual(x["T9_relative_phase_exponent_mod9"],4)
        self.assertFalse(x["uniform_T9_transversal_preserves_code"])
        self.assertFalse(x["uniform_Fourier_transversal_preserves_code"])

    def test_uv_anomaly_and_global_center_rule(self):
        x=self.P["UV_SIC_E8_center"]
        self.assertEqual([z["one_loop_b0"] for z in x["SU3_gauge_theory_one_loop"]],[0,-1,-18])
        self.assertTrue(x["E6_neutral_SU3_triplets_forbidden_even_as_nonadjoint_H_representations"])
        self.assertEqual([z["allowed"] for z in x["charge_tests"]],[True]*4+[False]*3)

    def test_nonflat_torus_flux_still_has_sphere_gap(self):
        x=self.P["nonflat_magnetic_flux_Dirac_gap"]
        self.assertAlmostEqual(x["S5_ordinary_Dirac_min_abs_eigenvalue"],2.5)
        self.assertEqual([z["total_7D_Dirac_zero_modes"] for z in x["sample_flux_sectors"]],[0]*5)
        self.assertEqual([z["cover_torus_Chern_number"] for z in x["sample_flux_sectors"]],[-27,-9,0,9,27])
        self.assertEqual(x["base_pullback_line_Chern_class"],"c1(L_m)=3m eta")

    def test_adversarial_loss_is_not_calibrated_loss(self):
        x=self.P["temporal_memory_loss_loophole"]
        self.assertAlmostEqual(x["adversarial_thinning_unconditional_match_upper_bound"],.5)
        self.assertFalse(x["numerical_scenarios"][0]["unconditional_witness_violation"])
        self.assertTrue(x["numerical_scenarios"][1]["unconditional_witness_violation"])
        self.assertGreater(x["numerical_scenarios"][1]
                           ["Hoeffding_sufficient_trials_for_alpha_0p01_power_0p95"],0)

    def test_external_refinement_only(self):
        x=self.P["W33_refinement_versus_gravity"]
        rows=x["refinement_samples"]
        self.assertLess(rows[-1]["relative_error_against_continuum_k1"],
                        rows[0]["relative_error_against_continuum_k1"])
        self.assertEqual(rows[-1]["first_internal_W33_mass_squared"],10)
        self.assertIn("externally",x["gravitational_obstruction"])

    def test_all_reports_preserve_limitations(self):
        self.assertEqual(self.C["status"],"PASS")
        self.assertEqual(self.P["status"],"PASS")
        self.assertIn("not", self.C["decoder"]["boundaries"][0])
        self.assertIn("not", self.P["temporal_memory_loss_loophole"]["limitation"])

if __name__=="__main__":
    unittest.main()
