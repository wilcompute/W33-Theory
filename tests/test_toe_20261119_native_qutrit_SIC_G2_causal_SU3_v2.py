"""Regression for five independent, explicitly bounded finite TOE research gates."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261119_native_qutrit_three_time_hierarchy_v2 as memory
import toe_20261119_SIC_Welch_moduli_obstruction as sic
import toe_20261119_G2_real_form_14_generator_certificate as g2
import toe_20261119_causal_Hasse_oriented_spectral_obstruction as causal
import toe_20261119_SU3_reference_calibration_gauge_frame_falsifier as su3

class FiveFalsifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mem=memory.run()
        cls.sic=sic.run()
        cls.g2=g2.run()
        cls.caus=causal.run()
        cls.su3=su3.run()

    def test_native_qutrit_three_time_witness(self):
        for a in self.mem['samples']:
            self.assertAlmostEqual(a['published_dimension_d_three_time_witness'],-2*a['gamma'])
            self.assertLess(max(a['pairwise_Fidelity_sums']),1e-12)

    def test_three_native_classical_choi_decompositions(self):
        for a in self.mem['samples']:
            self.assertLess(max(a['pairwise_classical_certificates']['pairwise_full_choi_residuals']),1e-12)

    def test_one_physical_quantum_unitary_process(self):
        for a in self.mem['samples']:
            self.assertEqual(a['joint_quantum_dilation']['same_environment_dimension'],4)
            self.assertLess(a['joint_quantum_dilation']['three_output_channel_max_residual'],1e-12)
            self.assertLess(a['joint_quantum_dilation']['intertime_unitarity_max_error'],1e-12)

    def test_H27_symmetric_channel_is_unital(self):
        s=self.mem['H27_symmetry_selection_rule']
        self.assertGreater(s['H27_covariance_residuals_for_E1_E2_E3'][0],1e-3)
        self.assertLess(max(s['H27_covariance_residuals_for_E1_E2_E3'][1:]),1e-12)
        self.assertFalse(s['nonunital_H27_covariant_qutrit_CPTP_possible'])

    def test_SIC_global_frame_potential_bound(self):
        self.assertAlmostEqual(self.sic['SIC_samples'][0]['Welch_frame_potential'],13.5)
        self.assertAlmostEqual(self.sic['three_MUB_frames_potential'],15)
        self.assertAlmostEqual(self.sic['SIC_vs_three_MUB_gap'],1.5)

    def test_SIC_continuous_labeled_projective_inequivalence(self):
        ss=self.sic['SIC_samples']
        self.assertNotAlmostEqual(ss[0]['bargmann_triangle_036'][0],ss[1]['bargmann_triangle_036'][0],places=5)
        self.assertTrue(all(abs(x['Welch_frame_potential']-13.5)<1e-11 for x in ss))

    def test_SIC_quadratic_moduli_nullity(self):
        q=self.sic['quadratic_moduli']
        self.assertEqual(q['design_constraint_jacobian_rank'],26)
        self.assertEqual(q['frame_potential_quadratic_zero_directions'],10)
        self.assertEqual(q['global_SU3_zero_directions'],8)
        self.assertTrue(q['one_explicit_additional_Hesse_modulus'])

    def test_G2_exact_phi_stabilizer(self):
        self.assertEqual(self.g2['exact_matrix_rank'],35)
        self.assertEqual(self.g2['exact_Lie_algebra_dimension'],14)
        self.assertEqual(self.g2['pairwise_commutator_span_checks'],91)

    def test_G2_preserves_real_cubic_pair(self):
        self.assertLess(self.g2['numerical_real_cubic_variation_max_C0'],1e-7)
        self.assertLess(self.g2['numerical_real_cubic_variation_max_Cphi'],1e-7)

    def test_causal_63_n5_and_dual_pair_count(self):
        self.assertEqual(self.caus['unlabeled_poset_classes'],63)
        self.assertEqual(self.caus['self_dual_isomorphism_classes'],15)
        self.assertEqual(self.caus['distinct_dual_pairs'],24)

    def test_causal_undirected_spectrum_information_loss(self):
        self.assertEqual(self.caus['undirected_Hasse_laplacian_spectral_classes'],14)
        self.assertEqual(self.caus['undirected_Hasse_graph_isomorphism_types'],14)

    def test_causal_inverse_spectral_response_duality(self):
        self.assertLess(self.caus['inverse_propagator_Frobenius_response_dual_max_difference'],1e-12)
        self.assertNotEqual(self.caus['nonselfdual_example']['minimal_points_P'],
                            self.caus['nonselfdual_example']['minimal_points_dual'])

    def test_SU3_four_setting_visibility_phase_calibration(self):
        q=self.su3['reference_compensated']
        self.assertLess(q['complex_RMSE'],.08)
        self.assertGreater(q['coverage_if_valid_common_phase'],.98)

    def test_SU3_differential_phase_drift_bias(self):
        self.assertGreater(self.su3['differential_phase_drift']['complex_RMSE'],.15)
        self.assertLess(self.su3['reference_compensated']['complex_RMSE'],.08)

    def test_SU3_mode_loss_breaks_frame_invariance(self):
        q=self.su3['color_mode_gauge_bias']
        self.assertGreater(q['max_color_biased_frame_trace_error'],.7)
        self.assertEqual(q['identity_reference_trace_all_frames'],3.)

if __name__=='__main__':unittest.main()
