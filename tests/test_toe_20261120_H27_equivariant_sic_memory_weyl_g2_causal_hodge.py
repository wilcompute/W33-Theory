"""Regression tests for six carefully qualified TOE finite-model gates.

Run: python -m unittest discover -s tests -p 'test_toe_20261120_*.py' -q
"""
from pathlib import Path
import sys,unittest,math
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261120_H27_equivariant_sic_memory_weyl_g2_causal_hodge as m

class SixGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=m.run(write=False)['tracks']

    def test_H27_19d_character_space(self):
        z=self.r['H27_equivariant_SIC_SU3']
        self.assertEqual(z['dimension'],19)
        self.assertEqual(z['baryon_character_ranks']['00'],3)
        self.assertEqual(list(z['baryon_character_ranks'].values()).count(2),8)
    def test_H27_19_independent_complex_sources(self):
        z=self.r['H27_equivariant_SIC_SU3']
        self.assertEqual(len(z['selected_19_characters_and_seed_triples']),19)
        self.assertGreater(z['19_constraint_min_singular_value'],1)
    def test_H27_exact_minor_certificate(self):
        z=self.r['H27_equivariant_SIC_SU3']
        self.assertEqual(z['mod7_nonzero_19x19_minor_determinant'],2)
        self.assertEqual(len(z['mod7_minor_pivot_columns']),19)
    def test_H27_covariance_of_baryons(self):
        self.assertLess(self.r['H27_equivariant_SIC_SU3']['H27_covariance_source_residual'],1e-9)
    def test_H27_source_targets_not_breaking(self):
        self.assertLess(self.r['H27_equivariant_SIC_SU3']['max_nontrivial_character_source_value'],1e-9)
    def test_H27_vacuum_equivariant_modulo_color(self):
        self.assertLess(self.r['H27_equivariant_SIC_SU3']['H27_vacuum_color_gauge_residual'],1e-9)
    def test_H27_antifundamental_massframe(self):
        self.assertGreater(self.r['H27_equivariant_SIC_SU3']['anti_triplet_frame_min_abs_det'],1)
    def test_H27_antifundamental_phase_covariance(self):
        self.assertLess(self.r['H27_equivariant_SIC_SU3']['H27_antifundamental_coupling_residual'],1e-9)
    def test_H27_Dflat(self):
        self.assertLess(self.r['H27_equivariant_SIC_SU3']['nine_SIC_triplets_Dflat_residual'],1e-9)
    def test_H27_holomorphic_mass_gap_modulo_gauge(self):
        z=self.r['H27_equivariant_SIC_SU3']
        self.assertEqual(z['full_100x100_holomorphic_Hessian_rank'],92)
        self.assertEqual(z['full_holomorphic_Hessian_gauge_kernel'],8)
        self.assertLess(z['max_gauge_tangent_Flinear_residual'],1e-9)
    def test_anomaly_symmetric_matter(self):
        self.assertIn('9 antifundamental',self.r['H27_equivariant_SIC_SU3']['SU3_cubic_chiral_gauge_anomaly'])

    def test_qutrit_threshold_gamma36(self):
        z=self.r['qutrit_three_time_finite_shots']
        self.assertAlmostEqual(z['gamma_thresholds_epsilon']['0.36'],.01026320761596826,places=11)
    def test_qutrit_threshold_gamma75(self):
        self.assertAlmostEqual(self.r['qutrit_three_time_finite_shots']['gamma_thresholds_epsilon']['0.75'],.0428932188136,places=10)
    def test_qutrit_gamma1_threshold(self):
        self.assertAlmostEqual(self.r['qutrit_three_time_finite_shots']['gamma_thresholds_epsilon']['1.0'],.0750494088515,places=10)
    def test_qutrit_analytic_witness(self):
        self.assertAlmostEqual(m.witness(3,.75,.01),-.7894929399347173,places=11)
    def test_qutrit_99_percent_hoeffding_prospective(self):
        z=self.r['qutrit_three_time_finite_shots']
        self.assertEqual(z['sufficient_shots_each_of_first_and_pooled_late_populations'],30650)
        self.assertEqual(z['total_independent_shots'],61300)
    def test_qutrit_seeded_simulation_certification(self):
        self.assertLess(self.r['qutrit_three_time_finite_shots']['simulated_confidence_upper_witness'],0)

    def test_weyl_full_rank_character_transform(self):
        self.assertEqual(self.r['SU3_Weyl_detector_twirl_minimality']['nine_weyl_character_Fourier_transform_rank'],9)
    def test_weyl_minimum_full_unknown_readout(self):
        self.assertEqual(self.r['SU3_Weyl_detector_twirl_minimality']['minimum_nonzero_Weyl_settings_for_full_unknown_detector'],9)
    def test_weyl_three_shift_diagonal_only(self):
        self.assertEqual(self.r['SU3_Weyl_detector_twirl_minimality']['minimum_X_shift_settings_for_unknown_diagonal_detector'],3)
        self.assertGreater(self.r['SU3_Weyl_detector_twirl_minimality']['arbitrary_detector_three_shift_frobenius_residual'],.01)
    def test_weyl_nine_setting_correct(self):
        self.assertLess(self.r['SU3_Weyl_detector_twirl_minimality']['error_full_uniform_nine_twirls'],1e-12)
    def test_weyl_nonuniform_weights_create_error(self):
        z=self.r['SU3_Weyl_detector_twirl_minimality']
        self.assertGreater(z['nonuniform_example_max_nontrivial_Weyl_Fourier_weight'],.1)
        self.assertGreater(z['nonuniform_example_complex_trace_error'],1e-4)
        self.assertLessEqual(z['nonuniform_example_complex_trace_error'],z['nonuniform_example_L1_bound'])

    def test_S7_spin_curvature(self):
        z=self.r['G2_smooth_compactification_chirality']
        self.assertEqual(z['round_unit_S7_scalar_curvature'],42)
        self.assertAlmostEqual(z['untwisted_Lichnerowicz_dirac_spectral_gap_lower_bound'],math.sqrt(10.5))
    def test_S7_no_untwisted_zero_modes(self):
        z=self.r['G2_smooth_compactification_chirality']
        self.assertEqual(z['untwisted_S7_zero_modes'],0)
        self.assertEqual(z['exact_unit_S7_Dirac_spectrum_first_four_levels'][0]['multiplicity_each_sign'],8)
    def test_periodic_chiral_index_zero(self):
        self.assertEqual(self.r['G2_smooth_compactification_chirality']['periodic_index_dimkerQ_minus_dimkerQ_adj'],0)

    def test_causal_4D_diamond_geometry(self):
        self.assertEqual(self.r['causal_4D_time_reversal']['events_per_sprinkling'],48)
    def test_causal_4D_exact_time_reversal(self):
        z=self.r['causal_4D_time_reversal']
        self.assertEqual(z['exact_time_reversal_arrow_sign_matches'],z['sprinkling_count'])
        self.assertEqual(z['paired_time_reverse_ensemble_arrow_mean'],0)
    def test_causal_4D_odd_statistic_nontrivial(self):
        self.assertGreater(self.r['causal_4D_time_reversal']['arrow_nonzero_samples'],300)

    def test_Levi_geometry(self):
        z=self.r['W33_Hodge_edge_phase_leakage']
        self.assertEqual((z['W33_points'],z['W33_lines'],z['Levi_vertices'],z['Levi_flags']),(40,40,80,160))
        self.assertEqual(z['Levi_cycle_space_rank'],81)
    def test_Levi_exact_Hodge_projector(self):
        z=self.r['W33_Hodge_edge_phase_leakage']
        self.assertTrue(z['K_squared_exactly_160_K'])
        self.assertEqual(z['signed_cycle_K_coefficient_by_distance'],[81,-27,9,-3,1])
    def test_Levi_all_edges_couple(self):
        self.assertTrue(self.r['W33_Hodge_edge_phase_leakage']['all_160x160_cycle_projector_entries_nonzero'])
    def test_Levi_single_edge_phase_formula(self):
        z=self.r['W33_Hodge_edge_phase_leakage']
        expected=4*math.sin(z['one_edge_phi_radians']/2)**2*81*79/160**2
        self.assertAlmostEqual(z['one_edge_hodge_leakage_numeric'],expected,places=12)
    def test_Levi_independent_Gaussian_phase_formula(self):
        z=self.r['W33_Hodge_edge_phase_leakage']
        theoretical=(6399/160)*(1-math.exp(-z['gaussian_IID_phase_sigma']**2))
        self.assertAlmostEqual(z['expected_total_Hodge_leakage_at_sigma'],theoretical,places=10)
        self.assertLess(abs(z['empirical_mean_total_Hodge_leakage_400_trials']-theoretical),.05)

if __name__=='__main__':unittest.main()
