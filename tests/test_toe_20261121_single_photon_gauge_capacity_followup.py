"""Regress one-photon hidden-chart decoder and five independent physical continuations."""
from __future__ import annotations
import json
import math
import sys
import unittest
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_single_photon_gauge_capacity_followup as c

class TestWittingSinglePhotonFiveFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rays,cls.S,cls.decks,cls.A,cls.P,cls.O=c.previous.geometry()
        cls.single=c.single_photon_front(cls.rays,cls.S,cls.decks,cls.A,cls.O)
        cls.channel=c.routed_channel_front(cls.rays)
        cls.two=c.two_use_front(cls.rays)
        cls.gates=c.Hamiltonian_front(cls.P,cls.S,cls.O)
        cls.gauge=c.gauge_front(cls.A)
        cls.det=c.detector_front(cls.S,cls.O)
        cls.optim=c.optimized_input_front(cls.rays)

    def test_exact_integer_45x40_incidence(self):
        a=self.single
        self.assertEqual(a["chart_to_ray_incidence_shape"],[45,40])
        self.assertEqual(a["H_Htrans_exact"],"H H^T = 6 I - 2 A + 2 J")
        self.assertEqual(a["H_Htrans_spectrum"],{"72":1,"12":24,"0":20})
        self.assertEqual(a["H_rank"],25)

    def test_hidden_24_projector_and_27_deck_invisibility(self):
        a=self.single
        self.assertTrue(a["hidden_bias_has_identical_27_deck_totals_as_uniform"])
        self.assertTrue(a["K_visible_subspace_orthogonal_to_hidden24"])
        self.assertLess(a["exact_decoder_max_residual"],1e-12)

    def test_exact_single_photon_multinomial_estimator_variance(self):
        a=self.single
        self.assertAlmostEqual(a["unbiased_per_detection_estimator_squared_norm"],3.2)
        self.assertAlmostEqual(a["single_photon_local_Fisher_24_eigenvalue"],7.5)
        self.assertAlmostEqual(a["single_photon_local_Cramer_Rao_trace_inverse_coefficient"],3.2)
        self.assertEqual(a["sufficient_detected_single_photons_for_RMS_le_0p001"],3200000)

    def test_seeded_multinomial_sample_convergence(self):
        a=self.single["seeded_multinomial_simulations"]
        self.assertEqual(a["1000"]["shot_count"],1000)
        self.assertLess(a["1000000"]["l2_error"],a["1000"]["l2_error"])
        self.assertAlmostEqual(a["1000"]["exact_mse"]*1000,a["1000000"]["exact_mse"]*1000000)

    def test_one_pure_Witting_state_does_not_have_full_Fisher_rank(self):
        d=self.single
        self.assertEqual(d["ranks_of_single_pure_Witting_input_Fisher"],{21:40})
        self.assertTrue(d["mixed_state_can_be_prepared_by_classical_randomization"])

    def test_compressed_24_ray_labels_plus_one_bucket(self):
        a=self.single
        self.assertEqual(a["compressed_distinguishable_output_bins"],25)
        self.assertEqual(len(a["compressed_globally_resolved_ray_labels"]),24)
        self.assertEqual(a["compressed_coarse_unresolved_ray_count"],16)
        self.assertEqual(a["compressed_hidden_chart_rank"],24)
        self.assertLess(a["compressed_exact_inverse_residual"],1e-10)
        self.assertAlmostEqual(a["compressed_local_Cramer_Rao_trace_inverse_coefficient"],
                               11.8133333333333)

    def test_constrained_channel_retains_quantum_capacity(self):
        a=self.channel
        self.assertTrue(a["constrained_zero_rows_in_one_output_rail"])
        self.assertEqual(a["constrained_effective_output_support_dimension"],8)
        self.assertEqual(sorted(a["constrained_permutation"]),list(range(45)))
        self.assertGreater(a["constrained_best_IC_qubits"],1.03)
        self.assertTrue(a["perfect_full_45_Naimark_isometry_preserved"])

    def test_routing_comparison_is_not_global_optimality(self):
        a=self.channel
        self.assertGreater(a["prior_unrestricted_routed_IC_qubits"],1.08)
        self.assertLess(a["constrained_best_IC_qubits"],
                        a["prior_unrestricted_routed_IC_qubits"])

    def test_full_rank_input_optimizes_capacity_lower_bound(self):
        d=self.optim
        self.assertGreater(min(d["optimized_4x4_input_eigenvalues"]),.19)
        self.assertEqual(len(d["input_log_density_15_parameters_in_SU4_Hermitian_basis"]),15)
        self.assertGreater(d["explicit_full_rank_input_coherent_information_bits"],1.097)
        self.assertGreater(d["explicit_full_rank_input_coherent_information_bits"],
                           d["routed_maximally_mixed_coherent_information_bits"]+.01)
        self.assertAlmostEqual(d["two_use_product_state_lower_bound_total_qubits"],
                               2*d["explicit_full_rank_input_coherent_information_bits"])

    def test_two_use_product_additivity_identity(self):
        a=self.two
        self.assertEqual(a["two_use_Kraus_count"],25)
        self.assertEqual(a["two_use_output_dims"],[81,25])
        self.assertAlmostEqual(a["independent_two_use_product_coherent_information_bits"],
                               2*a["single_use_maxmixed_routed_coherent_information_bits"],
                               places=8)

    def test_tested_correlated_inputs_not_yet_superadditive(self):
        a=self.two
        self.assertEqual(len(a["structured_two_use_inputs"]),10)
        self.assertFalse(a["structured_test_has_superadditivity_over_PRODUCT_MAXMIXED"])
        self.assertLess(a["best_tested_structured_per_use"],
                        a["single_use_maxmixed_routed_coherent_information_bits"])

    def test_exact_two_commuting_exponential_compiler(self):
        a=self.gates
        self.assertEqual(a["all_45_charts_verified"],45)
        self.assertLess(a["max_projector_compilation_error"],1e-10)
        self.assertLess(a["max_two_factor_unitary_error"],1e-10)
        self.assertTrue(a["coherent_projector_phase_gate_requires_nonlinear_or_ancilla_resource"])

    def test_nonabelian_lattice_fiber_wilson_loop(self):
        a=self.gauge
        self.assertTrue(a["noncommuting_links_with_nonzero_Wilson_plaquette"])
        vals=a["lattice_rows"]
        self.assertEqual([v["L"] for v in vals],[8,16,32,64])
        self.assertGreater(vals[0]["internal_Wilson_loop_norm_minus_identity"],
                           vals[-1]["internal_Wilson_loop_norm_minus_identity"])
        self.assertGreater(vals[-1]["L_squared_Wilson_deviation"],0.1)

    def test_causality_is_externally_engineered(self):
        a=self.gauge
        self.assertTrue(a["continuous_time_hopping_has_no_strict_finite_speed_in_continuum_limit"])
        self.assertTrue(a["separate_discrete_time_local_coin_shift_has_maximum_one_cell_per_step"])

    def test_calibrated_ray_misidentification_Fisher(self):
        a=self.det
        self.assertEqual(len(a["cases"]),5)
        self.assertAlmostEqual(a["cases"][0]["per_detected_photon_Fisher_eigenvalue"],7.5)
        self.assertLess(a["cases"][2]["per_detected_photon_Fisher_eigenvalue"],7.5)
        self.assertGreater(a["cases"][2]["sufficient_detected_photons_for_RMS_0p001_from_linear_inverse"],3.2e6)

    def test_uniform_no_click_efficiency(self):
        a=self.det
        self.assertAlmostEqual(a["uniform_detection_efficiency"],.70)
        self.assertAlmostEqual(a["Fisher_per_launched_photon_with_no_click_global_eta"],5.25)

    def test_frozen_machine_certificate(self):
        p=ROOT/"data/toe_20261121_onephoton_chart_channel_gauge_sevenfronts.json"
        obj=json.loads(p.read_text(encoding="utf8"))
        self.assertEqual(obj["status"],"PASS")
        self.assertEqual(len([x for x in obj if x.startswith("front")]),7)

if __name__=="__main__":
    unittest.main()
