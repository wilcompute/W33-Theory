"""Independent regression: five Q8 correlation/physics frontiers."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_q8_correlation_five as mod

class TestFiveCorrelationFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=mod.main()

    def test_64_dimensional_frame(self):
        x=self.out["track_1_exact_tight_schmidt"]
        self.assertEqual((x["rows"],x["columns"],x["frame_rank"]),(72,64,64))
        self.assertLess(x["max_orthonormal_frame_error"],4e-12)
        self.assertLess(x["max_mixed_correlation_reconstruction_error"],4e-12)
        self.assertEqual(x["unmeasured_local_bloch_components"],16)

    def test_tight_mixed_witness(self):
        x=self.out["track_1_exact_tight_schmidt"]
        self.assertLess(x["max_pure_Schmidt_trace_norm_identity_error"],4e-12)
        self.assertAlmostEqual(x["tight_mixed_bounds"]["Schmidt_number_le_2"],5/3)
        self.assertEqual(x["visibility_2"],.25)
        self.assertEqual(x["visibility_3"],.625)
        self.assertTrue(x["isotropic_checks"]["0.65"]["Schmidt_number_3"])
        self.assertFalse(x["isotropic_checks"]["0.5"]["Schmidt_number_3"])

    def test_product_control_fails_closed(self):
        x=self.out["track_2_detector_confidence_LP"]["experiments"]["product"]
        self.assertFalse(x["nominal_calibrated_interval"]["SN2_certified"])
        self.assertFalse(x["wide_efficiency_interval"]["SN2_certified"])
        self.assertLess(x["nominal_calibrated_interval"]["lower_bound"],2/3)

    def test_robust_confidence_succeeds_for_maxent(self):
        x=self.out["track_2_detector_confidence_LP"]["experiments"]["isotropic_0p8"]
        self.assertTrue(x["finite_sample_control"]["SN3_certified"])
        self.assertGreater(x["finite_sample_control"]["lower_bound"],5/3)
        self.assertLess(x["finite_sample_control"]["lower_bound"],x["true_trace_norm"])

    def test_24_optical_contexts(self):
        x=self.out["track_3_optical_compilation"]
        self.assertEqual(x["number_of_contexts"],24)
        self.assertLess(x["verified_matrix_error"],4e-12)
        self.assertLessEqual(x["max_two_mode_couplers_per_9mode_context"],18)

    def test_dimension_was_supplied(self):
        x=self.out["track_4_scaling_null"]
        self.assertIn("d supplied",x["model"])
        self.assertAlmostEqual(x["running_dimensions"]["3"]["64"],3.0059057194,places=6)
        self.assertAlmostEqual(x["running_dimensions"]["4"]["64"],4.0078742926,places=6)

    def test_cosmology_frozen_s9_not_scored(self):
        x=self.out["track_5_cosmology_prereg"]
        self.assertFalse(x["S9_scored"])
        self.assertAlmostEqual(x["DES_Y6_public_LambdaCDM_S8"],.789)
        self.assertAlmostEqual(x["frozen_Dovekie_pre_Halofit_refit_S8"]["free_neg"],.833128,places=5)
        self.assertIn("NOT",x["warning"])
        self.assertIn("xi",x["why_not_scored"])

    def test_frozen_result(self):
        path=ROOT/"data/w33_20261109_q8_correlation_five.json"
        if path.exists():
            freeze=json.loads(path.read_text(encoding="utf8"))
            self.assertEqual(freeze["status"],self.out["status"])
            self.assertEqual(freeze["track_1_exact_tight_schmidt"]["frame_rank"],64)

if __name__=="__main__":
    unittest.main()
