"""Cross-front reproducibility tests: exact gauge, posets, memory, SU3 shots."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261119_five_deep_kinematic_gates as t

class TOEDeepGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.g=t.run()['tracks']
    def test_sic_F_D(self):
        self.assertLess(self.g['SU3_SIC_gauge_completion']['frame_moment_map_Frobenius_error'],1e-10)
    def test_sic_baryon_modular_certificate(self):
        self.assertEqual(self.g['SU3_SIC_gauge_completion']['Jacobian_rank_Galois_mod7'],19)
    def test_sic_mass_hessian(self):
        x=self.g['SU3_SIC_gauge_completion']
        self.assertEqual(x['complex_holomorphic_Hessian_rank'],92)
        self.assertGreater(x['smallest_nonzero_Hessian_singular_value'],.7)
    def test_sic_gauge_boson_masses(self):
        self.assertLess(self.g['SU3_SIC_gauge_completion']['eight_gauge_vector_mass_matrix_deviation_from_6I'],1e-10)
    def test_sic_anomaly_cancellation(self):
        self.assertEqual(self.g['SU3_SIC_gauge_completion']['SU3_cubic_anomaly_fund_plus_antifund'],0)
    def test_five_poset_isomorphism(self):
        self.assertEqual(self.g['causal_poset_invariant']['five_event_unlabeled_posets'],63)
        self.assertTrue(self.g['causal_poset_invariant']['five_event_complete_isomorphism_invariant'])
    def test_six_poset_collision(self):
        x=self.g['causal_poset_invariant']
        self.assertEqual(x['six_event_naturally_labeled_relations'],4824)
        self.assertEqual(x['six_event_joint_past_future_histogram_classes'],311)
        self.assertEqual(x['first_explicit_six_event_failure']['Hasse_covers_A'],5)
        self.assertEqual(x['first_explicit_six_event_failure']['Hasse_covers_B'],6)
    def test_e6_no_real_enhancement(self):
        self.assertEqual(self.g['G2_E6_real_structure']['real_pencil_critical_points'],0)
    def test_e6_complex_reality_reconstruction(self):
        self.assertLess(self.g['G2_E6_real_structure']['real_complex_cubic_inverse_reconstruction_max_error'],1e-12)
    def test_memory_pairwise_classical(self):
        x=self.g['genuine_three_time_quantum_memory']
        self.assertEqual(x['pairwise_classical_decompositions_verified'],3)
        self.assertLess(x['largest_pairwise_channel_superoperator_error'],1e-12)
    def test_memory_genuine_three_time_only(self):
        self.assertAlmostEqual(self.g['genuine_three_time_quantum_memory']['three_time_W3_witness'],-.36,places=12)
    def test_memory_classical_threshold(self):
        x=self.g['genuine_three_time_quantum_memory']
        self.assertGreater(x['p'],x['pairwise_classical_threshold_pcrit'])
    def test_su3_shot_budget(self):
        x=self.g['SU3_finite_shots_and_loss']
        self.assertEqual(x['accepted_detections_per_phase_required'],9401)
        self.assertEqual(x['total_raw_attempts_sufficient'],27838)
    def test_su3_noncommutativity(self):
        self.assertGreater(self.g['SU3_finite_shots_and_loss']['SU3_noncommutativity_Frobenius_norm_squared'],4)

if __name__=='__main__':unittest.main()
