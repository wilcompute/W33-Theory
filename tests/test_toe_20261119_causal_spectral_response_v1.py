#!/usr/bin/env python3
"""Regression checks for the Nov 19 causal spectral-response construction."""
import sys
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261119_causal_spectral_response_v1 as mod

class CausalSpectralResponse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert=mod.run()
    def test_block_determinant_general_case(self):
        self.assertEqual(self.cert["block_dag_cases"],32)
    def test_gauge_frame_covariance(self):
        self.assertEqual(self.cert["gauge_frame_checks"],24)
        self.assertLess(max(self.cert["gauge_max_residuals"]),1e-10)
    def test_det_blind_but_responds_to_flux(self):
        vals=self.cert["su2_diamond"]
        self.assertEqual(len(vals),4)
        self.assertLess(max(v["bare_det_real"] for v in vals)-min(v["bare_det_real"] for v in vals),1e-10)
        self.assertGreater(vals[0]["spectrally_regularized_det_ratio_mu_0p1"],
                           vals[-1]["spectrally_regularized_det_ratio_mu_0p1"])
    def test_exact_slope(self):
        for v in self.cert["su2_diamond"]:
            self.assertAlmostEqual(v["spectral_gap_inverse_trace"],v["closed_form_slope"],places=10)
    def test_complete_cancellation_without_causal_cycle(self):
        self.assertAlmostEqual(self.cert["su2_diamond"][-1]["endpoint_probe_det_lambda_2"],1.0,places=10)
        self.assertLess(self.cert["su2_diamond"][-1]["propagator_source_endpoint_normsq"],1e-20)
    def test_higher_SU3_invariants(self):
        a=self.cert["su3_same_first_wilson_moment"]["case_A"]
        b=self.cert["su3_same_first_wilson_moment"]["case_B"]
        self.assertAlmostEqual(a["wilson_trace_real"],b["wilson_trace_real"],places=10)
        self.assertAlmostEqual(a["spectral_gap_inverse_trace"],b["spectral_gap_inverse_trace"],places=10)
        self.assertGreater(abs(a["second_logdet_derivative_at_zero"]-b["second_logdet_derivative_at_zero"]),1e-4)
        self.assertGreater(abs(a["spectrally_regularized_det_ratio_mu_0p1"]-b["spectrally_regularized_det_ratio_mu_0p1"]),1e-6)
    def test_endpoint_response_is_not_gravity_selection(self):
        self.assertTrue(self.cert["status"].endswith("NOT_A_TOE"))
        self.assertGreater(len(self.cert["caveats"]),3)

if __name__=="__main__":
    unittest.main()
