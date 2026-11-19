import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261119_five_new_uv_poset_memory_realE6_SU3 as m
class TOEFiveGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.z=m.run()["tracks"]
    def test_E8_sextic_uniqueness(self): self.assertEqual(self.z["uv"]["degree6_invariants_of_one_E8_adjoint"],1)
    def test_SU3_no_single_triplet_invariant(self): self.assertEqual(self.z["uv"]["one_SU3_triplet_nonconstant_holomorphic_invariants"],0)
    def test_SIC_field_count(self): self.assertEqual(self.z["uv"]["positive_SIC_triplet_fields_needed_for_D_flatness"],9)
    def test_all_511_SIC_subsets(self): self.assertEqual(self.z["uv"]["nonempty_SIC_subset_checks"],511)
    def test_SIC_numerical_residual(self): self.assertLess(self.z["uv"]["max_SIC_subset_identity_error"],1e-12)
    def test_poset_63_types(self): self.assertEqual(self.z["causal"]["unlabeled_posets"],63)
    def test_poset_histogram(self): self.assertEqual(self.z["causal"]["distinct_interval_histograms"],28)
    def test_poset_histogram_collisions(self): self.assertEqual(self.z["causal"]["histograms_with_nonisomorphic_collisions"],18)
    def test_E6_no_real_critical(self): self.assertEqual(self.z["g2_e6"]["real_critical_points"],0)
    def test_E6_positive_quadratic(self): self.assertEqual(self.z["g2_e6"]["minimum_over_real_t"],"7/8")
    def test_memory_reset(self): self.assertLess(self.z["temporal_memory"]["max_ideal_entanglement_recovery_error"],1e-12)
    def test_memory_noise_threshold(self): self.assertGreater(self.z["temporal_memory"]["memory_depolarizing_scan"][4]["negativity"],0)
    def test_memory_classical_control(self): self.assertLess(self.z["temporal_memory"]["classical_dephased_memory_negativity"],1e-12)
    def test_su3_commutator(self): self.assertGreater(self.z["two_loop_SU3"]["Frobenius_commutator_norm_squared"],4)
    def test_su3_gauge_frame(self): self.assertLess(self.z["two_loop_SU3"]["maximum_frame_error"],1e-12)
    def test_su3_two_phase(self): self.assertLess(self.z["two_loop_SU3"]["two_reference_phase_trace_reconstruction_error"],1e-12)
if __name__=="__main__":unittest.main()
