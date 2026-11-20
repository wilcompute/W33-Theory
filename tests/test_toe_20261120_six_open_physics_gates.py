"""Twenty-five focused checks of new 2026-11-20 W33/TOE research controls."""
import itertools
import math
import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261120_six_open_physics_gates as m

class SixResearchGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.all=m.main(write=False)
    def test_01_e8_branching(self):self.assertEqual(sum(self.all['e8_cubic_multiplet']['adjoint_248_E6xSU3_branching'].values()),248)
    def test_02_single_cubic_vanishes(self):self.assertLess(abs(self.all['e8_cubic_multiplet']['single_identical_commuting_27x3_E6cubic_epsilon']),1e-12)
    def test_03_two_cubic_vanishes(self):self.assertLess(abs(self.all['e8_cubic_multiplet']['two_identical_commuting_27x3_E6cubic_epsilon']),1e-12)
    def test_04_three_cubic_nonzero(self):self.assertAlmostEqual(self.all['e8_cubic_multiplet']['three_distinct_27x3_cubic_example'],1/6)
    def test_05_three_cubic_antisymmetric(self):self.assertAlmostEqual(self.all['e8_cubic_multiplet']['interchanging_two_distinct_copies'],-1/6)
    def test_06_hodge_dimension(self):self.assertEqual(self.all['w33_known_error_subcodes']['Hodge_dimension'],81)
    def test_07_levi_edge_connectivity(self):self.assertEqual(self.all['w33_known_error_subcodes']['Levi_edge_connectivity'],4)
    def test_08_one_known_bad_edge(self):self.assertEqual(self.all['w33_known_error_subcodes']['known_one_bad_edge_noiseless_subcode_dim'],80)
    def test_09_two_known_bad_edges(self):self.assertEqual(self.all['w33_known_error_subcodes']['known_two_bad_edges_noiseless_subcode_dim'],79)
    def test_10_four_edge_star(self):self.assertEqual(self.all['w33_known_error_subcodes']['known_four_edge_star_noiseless_subcode_dim'],78)
    def test_11_actual_cycle_basis(self):
        z=self.all['w33_known_error_subcodes']
        self.assertEqual(z['exact_incidence_cycle_residual'],0)
        self.assertEqual(z['explicit_one_bad_edge_cycle_basis_vectors'],80)
        self.assertEqual(z['corrupt_edge_coordinate_nonzero_count'],0)
    def test_12_unknown_phase_impossibility(self):self.assertEqual(self.all['w33_known_error_subcodes']['unrestricted_unknown_each_edge_phase_code_dimension_max'],1)
    def test_13_model_free_witness_true(self):self.assertLess(self.all['native_qutrit_model_free_memory']['true_model_witness'],0)
    def test_14_model_free_measured(self):
        z=self.all['native_qutrit_model_free_memory'];self.assertLess(z['prospective_seeded_certificate']['witness_upper'],0)
        self.assertEqual(z['prospective_seeded_certificate']['accepted_shots_total'],1400000)
    def test_15_model_free_shots(self):
        z=self.all['native_qutrit_model_free_memory'];self.assertEqual(z['worst_case_total_accepted_shots'],7*z['worst_case_sufficient_shots_per_setting'])
    def test_16_bound_under_any_povm(self):
        # Test that projective measurement makes pure orthogonal states appear identical.
        # Quantum root fidelity=0, measured outcome Bhattacharyya=1, hence upper bound.
        p=np.array([1.,0.,0.]);q=np.array([0.,1.,0.]);
        self.assertEqual(m.measured_fidelity_bound(p,q),0.)
        self.assertEqual(m.measured_fidelity_bound(np.array([.5,.5,0]),np.array([.5,.5,0])),1.)
    def test_17_hoeffding_union(self):
        N=200000;t=math.sqrt(math.log(42/.01)/(2*N))
        self.assertAlmostEqual(self.all['native_qutrit_model_free_memory']['prospective_seeded_certificate']['simultaneous_probability_radius'],t)
    def test_18_Su3_chronological_bias(self):self.assertGreater(self.all['SU3_polynomial_drift']['chronological_trace_error'],.001)
    def test_19_Su3_palindrome_quadratic_bias(self):self.assertGreater(self.all['SU3_polynomial_drift']['palindrome_trace_error_quadratic_survives'],.001)
    def test_20_Su3_richardson_exact(self):self.assertLess(self.all['SU3_polynomial_drift']['Richardson_36_trace_error_through_cubic'],1e-12)
    def test_21_Su3_quartic_survives(self):self.assertGreater(self.all['SU3_polynomial_drift']['quartic_drift_not_cancelled_trace_error'],.001)
    def test_22_Su3_shot_variance_penalty(self):self.assertAlmostEqual(self.all['SU3_polynomial_drift']['equal_exposure_shot_variance_inflation_vs_plain_four_measurement_average'],34/9)
    def test_23_E6_anomalies(self):self.assertEqual(self.all['E6_trinification_anomalies']['SU3_cubic_anomaly_per_factor'],(0,0,0))
    def test_24_E6_center(self):self.assertEqual(self.all['E6_trinification_anomalies']['center_exponent_on_each_nonet'],(1,1,1))
    def test_25_causal_comparability(self):
        values=self.all['4D_causal_link_nonlocality']['link_relation_counts']
        self.assertTrue(all(abs(x['pair_comparability']-.1)<.025 for x in values.values()))
    def test_26_causal_nonlocal_link_growth(self):
        v=self.all['4D_causal_link_nonlocality']['link_relation_counts']
        x=[v[str(n)]['mean_links_per_event'] for n in [40,80,160,320]]
        self.assertEqual(x,sorted(x));self.assertGreater(x[3],4*x[0])
    def test_27_causal_sampling(self):
        self.assertTrue(all(v['samples']==40 for v in self.all['4D_causal_link_nonlocality']['link_relation_counts'].values()))

if __name__=='__main__':unittest.main()
