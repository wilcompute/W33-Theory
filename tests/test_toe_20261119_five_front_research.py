"""Regression certificates: natural-SIC UV, G2/Dirac gap, qutrit memory,
finite W33 graph calculus, W33 asymmetric decoder, ninth-root injection/no-go.
"""
import sys,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_four_structural_frontier_tests as fs
import toe_20261119_w33_code_gate_and_decoder as gates

class FiveFrontResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.UV=fs.sic_uv_naturalness()
        cls.chiral=fs.chiral_flux_gap()
        cls.memory=fs.arbitrary_instrument_memory()
        cls.calculus=fs.finite_graph_calculus()
        _,_,HX,HZ=gates.checks()
        cls.noT=gates.no_transversal_diagonal_T9(HX)
        cls.decoder=gates.decoder_certificate(HX,HZ)
        cls.inject=gates.magic_injection()

    def test_sic_one_loop_vectorlike_no_go(self):
        self.assertEqual(self.UV["SU3_nine_flavor_one_loop_b0"],0)
        self.assertEqual(self.UV["SU3_ten_flavor_one_loop_b0"],-1)
        self.assertLess(self.UV["flavor_beta_table"][2]["maximum_one_loop_b0_3N_minus_N2"],0)

    def test_nonSIC_tight_frame_counterexample(self):
        self.assertAlmostEqual(self.UV["all_36_pair_overlap_sq_sum_SIC"],36)
        self.assertAlmostEqual(self.UV["all_36_pair_overlap_sq_sum_nonSIC"],36)
        self.assertAlmostEqual(self.UV["SIC_equiangular_variance"],0)
        self.assertAlmostEqual(self.UV["nonSIC_repeated_basis_equiangular_variance"],1728)

    def test_sphere_dirac_no_torus_flux_zero_modes(self):
        self.assertTrue(self.chiral["torus_only_mag_flux_zero_mode_impossible"])
        self.assertEqual(len(self.chiral["orbifold_order3_fixed_points"]),3)
        self.assertTrue(all(e["total_D7_eigenvalue_lower_bound"]>=2.5
                            for e in self.chiral["sample_R_equals_1_mass_gaps"]))

    def test_qutrit_arbitrary_instrument_causal_break(self):
        self.assertEqual(self.memory["arbitrary_Kraus_branch_count"],6)
        self.assertLess(self.memory["Kraus_trace_preserving_sum_error"],1e-12)
        self.assertLess(self.memory["branch_max_RS_residual"],1e-12)
        self.assertAlmostEqual(sum(self.memory["branch_probabilities"]),1)

    def test_event_ready_no_postselection_loophole(self):
        self.assertTrue(self.memory["event_ready_no_click_treated_as_failure"])
        self.assertGreater(self.memory["Hoeffding_99p9pct_one_sided_lower"],1/3)
        self.assertLess(self.memory["required_minimum_efficiency_for_conservative_violation"],0.5)

    def test_finite_graph_matrix_leibniz(self):
        self.assertLess(self.calculus["matrix_bimodule_Leibniz_max_error"],1e-12)
        self.assertGreater(self.calculus["graph_Laplacian_as_derivation_counterexample_leibniz_defect_norm"],10)
        self.assertAlmostEqual(self.calculus["kinetic_action_direct"],
                               self.calculus["kinetic_action_laplacian"])

    def test_W33_Dirichlet_gap(self):
        self.assertEqual(self.calculus["Laplacian_eigenvalues_multiplicities"],{"0":1,"10":24,"16":15})
        self.assertEqual(self.calculus["nonzero_spectral_gap"],10)

    def test_transversal_T9_no_go_exact_F3(self):
        self.assertEqual(self.noT["certificate_codewords"],70)
        self.assertEqual(self.noT["ranks_F3_cubic_linear_quadratic"],[11,41,70])
        self.assertEqual(self.noT["certifier_row_generator_weight_distribution"],{"1":22,"2":48})

    def test_asymmetric_decoder_radii(self):
        self.assertEqual(self.decoder["pure_X_syndromes"],81)
        self.assertEqual(self.decoder["pure_Z_syndromes"],3201)
        self.assertEqual(self.decoder["joint_test_samples"],2500)
        self.assertEqual(self.decoder["X_decoder_radius"],1)
        self.assertEqual(self.decoder["Z_decoder_radius"],2)

    def test_noise_bias_orientations(self):
        a=self.decoder["orientation_benchmark"]
        self.assertGreater(a[0]["guaranteed_success_original"],.975)
        self.assertEqual(a[1]["better_orientation"],"tie")
        self.assertGreater(a[2]["guaranteed_success_original"],a[2]["guaranteed_success_after_Fourier_swap"])

    def test_exact_T9_injection(self):
        self.assertEqual(self.inject["tested_random_state_outcome_pairs"],60)
        self.assertLess(self.inject["maximum_statevector_norm_error"],1e-13)
        self.assertEqual(self.inject["outcome_correction_relative_omega_exponents"],[[0,0,0],[0,1,0],[0,0,2]])

    def test_Hesse_SIC_not_single_shot_T9_resource(self):
        self.assertFalse(self.inject["SIC_is_direct_deterministic_T9_resource"])
        self.assertTrue(all(sorted(s)[0]<1e-10
                            for s in self.inject["Hesse_SIC_injection_branch_singular_values"]))

if __name__=="__main__":
    unittest.main()
