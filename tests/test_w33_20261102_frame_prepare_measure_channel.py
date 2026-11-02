"""Exact regression tests for the 216-state route-POVM prepare/measure channel."""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"analysis"/"w33_20261102_frame_prepare_measure_channel.py"
SPEC=importlib.util.spec_from_file_location("w33_frame_channel",P)
M=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
class FrameMeasurementChannel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=M.compute()
    def test_exact_classical_transition_probabilities(self):
        self.assertEqual(self.r["one_input_row_numerator_counts"],{16:100,64:95,256:20,1600:1})
        self.assertEqual(self.r["transition_denominator"],14400)
        self.assertEqual(self.r["self_identification_probability"],"1/9")
    def test_row_normalisation_and_positivity(self):
        self.assertTrue(self.r["symmetric_doubly_stochastic"])
        self.assertTrue(self.r["strictly_positive_all_entries"])
    def test_spectral_gap_and_blind_sector(self):
        self.assertEqual(self.r["spectral_gap"],"39/50")
        self.assertEqual(self.r["nontrivial_zero_eigenspace"],15)
    def test_classical_five_step_tv_bound(self):
        self.assertTrue(self.r["five_steps_sufficient_for_tv_below_1pct"])
        self.assertLess(self.r["worst_case_tv_l2_bound_5_steps"],.01)
if __name__=="__main__":unittest.main()
