#!/usr/bin/env python3
"""Independent test gates for fivefront model-scoped TOE continuation."""
import sys,unittest,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
from toe_20261120_fivefront_hardware_gravity_index import (
    w33_graph,css_matrices,tanner_schedule,detector_dictionary,
    qutrit_syndrome_gate,domain_wall_index,spacetime_volume_gate,
    su3_reference_gate,memory_loss_guard,three_context_classical_gluing,run
)

class FiveFrontTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=run(write=False)['tracks']
    def test_w33_geometry(self):
        G=w33_graph()
        self.assertEqual((G.number_of_nodes(),G.number_of_edges()),(80,160))
        self.assertTrue(all(x==4 for _,x in G.degree()))
    def test_qutrit_css_checks(self):
        hx,hz=css_matrices(8)
        self.assertEqual((hx.shape,hz.shape),((632,1833),(1120,1833)))
        self.assertFalse(np.any((hx@hz.T).data%3))
        self.assertEqual(1833-hx.shape[0]-hz.shape[0],81)
    def test_round_detector_unique_syndromes(self):
        hx,hz=css_matrices(8)
        X,DX=detector_dictionary(hz,rounds=3)
        Z,DZ=detector_dictionary(hx,rounds=3)
        self.assertEqual(X['unique_single_fault_signatures'],17718)
        self.assertEqual(Z['unique_single_fault_signatures'],14790)
        self.assertEqual(len(DX),17718)
        self.assertEqual(len(DZ),14790)
        # A measurement fault has two temporal detector entries.
        self.assertIn(((2,5,1),(3,5,2)),DX)
        # Data fault produces a single round's column syndrome.
        self.assertTrue(any(k and all(x[0]==2 for x in k) for k,v in DX.items() if v[0]=='data' and v[1]==2))
    def test_schedule_conflict_free(self):
        hx,hz=css_matrices(8)
        for H in (hx,hz):
            s=tanner_schedule(H)
            self.assertEqual(sum(len(x) for x in s),H.nnz)
            self.assertTrue(all(len({r for r,c in x})==len(x) for x in s))
            self.assertTrue(all(len({c for r,c in x})==len(x) for x in s))
    def test_single_ancilla_hook_is_only_support_bound(self):
        q=self.result['phenomenological_qutrit_css']
        self.assertLessEqual(q['X_check_hook_guard_support_only']['max_reduced_hook_weight'],3)
        self.assertLessEqual(q['Z_check_hook_guard_support_only']['max_reduced_hook_weight'],2)
        self.assertTrue(q['weight_four_logical_splitting_ambiguity'])
        self.assertLess(q['one_fault_only_guaranteed_event_probability']['X']['0.0001'],.8)
    def test_domainwall_Fredholm_and_periodic_no_go(self):
        a=self.result['exceptional_chiral_index_toy']
        self.assertEqual((a['open_line_ker_D'],a['open_line_ker_Ddagger']),(1,0))
        self.assertEqual(a['open_line_Fredholm_index'],1)
        self.assertLess(a['ODE_max_residual'],1e-6)
        self.assertEqual(a['periodic_circle_cases'][0]['index'],0)
        self.assertEqual(a['periodic_circle_cases'][1]['index'],0)
        self.assertEqual(a['direct_sum_N_copies_index_N']['4'],4)
        self.assertTrue(all(v==0 for v in a['E6_complete_27_U1psi_anomaly_per_family'].values()))
    def test_causal_density_charts_caveat(self):
        a=self.result['causal_volume_density_inverse']
        self.assertTrue(a['order_only_unidentifiable'])
        self.assertEqual(a['scalar_R_at_origin_true'],-1.)
        self.assertLess(abs(a['inference_with_known_coordinate_chart_and_uniform_sprinkling'][-1]['estimated_a']-.25),.05)
    def test_SU3_reference_requires_nuisance_calibration(self):
        a=self.result['SU3_reference_phase_robustness']
        self.assertEqual(a['adjoint_character_K_and_identity'],8)
        self.assertLess(a['certified_max_total_phase_error_radians'],math.pi/3)
        self.assertGreater(a['per_setting_shots_sufficient_Hoeffding'],0)
        self.assertIn('gauge invariant',a['model_boundary'])
    def test_memory_efficiency_and_frequencies_both_calibrated(self):
        a=self.result['three_time_memory_two_layer_confidence']
        self.assertGreater(a['expected_frequency_planning'][0]['W3_upper_99pct_joint'],0)
        self.assertLess(a['expected_frequency_planning'][-1]['W3_upper_99pct_joint'],0)
        self.assertLess(a['seeded_binomial_multinomial_forecasts'][-1]['W3_upper_99pct_joint'],0)
        self.assertIn('NOT prove every pair',a['hierarchy_caution'])
    def test_pairwise_marginals_global_gluing_obstruction(self):
        a=self.result['outside_box_three_context_marginal_gluing']
        self.assertEqual(a['max_symmetric_q_gluable'],2/3)
        self.assertTrue(a['cases'][2]['global_joint_exists'])
        self.assertFalse(a['cases'][3]['global_joint_exists'])
        self.assertEqual(len(a['cases'][2]['one_joint_distribution']),8)
    def test_full_reproduction_same_seed(self):
        b=run(write=False)['tracks']
        self.assertEqual(self.result,b)

if __name__=='__main__':unittest.main()
