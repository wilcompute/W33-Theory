"""Deterministic offline tests for 5 independent Witting optical/tomographic/causal fronts."""
from __future__ import annotations
import itertools
import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_fivefront_tightframe_coherent_memory as f

class TestFiveFrontTightFrames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rays,cls.supports,cls.decks,cls.graph,cls.P,cls.O=f.geometry()
        cls.opt=f.optical_front(cls.rays,cls.supports,cls.O)
        cls.tom=f.tomography_front(cls.supports,cls.decks,cls.graph,cls.O)
        cls.chan=f.channel_front(cls.rays)
        cls.hamiltonian=f.hamiltonian_front(cls.rays,cls.supports,cls.O)
        cls.causal=f.causal_front(cls.graph)
        cls.opdual=f.operator_duality_front(cls.supports,cls.decks,cls.graph,cls.P,cls.O)

    def test_all_45_eight_mode_Reck_interferometers(self):
        d=self.opt
        self.assertEqual(d["explicit_8mode_reck_decompositions"],45)
        self.assertEqual(d["gate_count_range"],[27,28])
        self.assertLess(d["max_reconstruction_error"],1e-10)

    def test_loss_robust_exact_threshold(self):
        d=self.opt
        self.assertAlmostEqual(d["required_min_to_max_efficiency_ratio"],math.sqrt(5/8))
        self.assertTrue(d["seeded_eta_in_0p80_to_1_preserves_all_540_nonorthogonal_maxima"])
        self.assertTrue(d["adversarial_all_winning_ports_eta_0p79_reverses_pair_0_5"])

    def test_24D_projector_exact_integer_idempotent(self):
        A=self.graph.astype(np.int64)
        M=15*np.eye(45,dtype=np.int64)-5*A+np.ones((45,45),np.int64)
        np.testing.assert_array_equal(M@M,30*M)
        self.assertEqual(np.trace(M),720)
        self.assertEqual(self.tom["rank_of_24D_projector"],24)

    def test_three_exact_pair_covariances(self):
        d=self.tom
        self.assertEqual(d["exact_orthogonal_pair_covariance_integer"],"X_orth X_orth^T=540 M")
        self.assertEqual(d["exact_nonorth_pair_covariance_integer"],"X_non X_non^T=360 M")
        self.assertEqual(d["exact_all_pair_covariance_integer"],"X X^T=900 M")
        self.assertLess(d["max_tight_frame_residual"],1e-11)

    def test_hidden_chart_bias_noiseless_tomography(self):
        d=self.tom
        self.assertTrue(d["all_27_aggregate_deck_weights_uniform_despite_hidden_bias"])
        self.assertLess(d["exact_540_probe_inversion_error"],1e-11)
        self.assertEqual(d["sparse_independent_nonorth_probe_count"],24)
        self.assertTrue(d["sparse_probe_full_rank_GF7"])
        self.assertLess(d["sparse_probe_condition_number"],10)

    def test_finite_shot_cost_is_reported(self):
        d=self.tom["synthetic_finite_shot_binomial_reconstruction"]
        self.assertEqual(d["1000"]["total_trusted_independent_trials"],540000)
        self.assertEqual(d["1000000"]["total_trusted_independent_trials"],540000000)
        self.assertGreater(d["1000"]["hidden_chart_bias_l2_error"],
                           d["1000000"]["hidden_chart_bias_l2_error"])

    def test_540probe_binomial_shot_upper_bound(self):
        d=self.tom
        self.assertAlmostEqual(d["certified_shot_rms_l2_upper_bounds"]["1000000"],
                               math.sqrt(18/1000000))
        self.assertEqual(d["total_540probe_shots_for_rms_l2_0p001"],9720000000)

    def test_explicit_4_to_9x5_coherent_Naimark(self):
        d=self.chan
        self.assertEqual(d["coherent_output_factorization"],[9,5])
        self.assertEqual(d["coherent_total_output_dim"],45)
        self.assertTrue(d["40distinguishable_Witting_click_amplitudes_exact"])
        self.assertLess(d["input_isometry_error"],1e-11)
        self.assertEqual(d["flagged_Choi_pure_schmidt_rank"],4)
        self.assertTrue(all(abs(x-0.5)<1e-11 for x in
                            d["flagged_Choi_schmidt_coefficients"]))

    def test_nine_dimensional_reduced_channel_is_nonEB(self):
        d=self.chan
        self.assertEqual(d["reduced_9level_channel_Kraus_count"],5)
        self.assertEqual(d["reduced_9level_channel_Choi_rank"],5)
        self.assertGreater(d["reduced_9level_channel_NPT_negativity"],0.5)
        self.assertLess(d["reduced_9level_channel_partial_transpose_min_eigenvalue"],0)
        self.assertTrue(d["cannot_claim_Pauli_covariance"])

    def test_45_real_chart_Hamiltonian_symmetric_projectors(self):
        d=self.hamiltonian
        self.assertEqual(d["45_explicit_16x16_two_copy_Hermitian_terms"],45)
        self.assertEqual(d["all_45_Q_spectra"],"(4/3)^6, 0^10")
        self.assertLess(d["max_exact_doubleSIC_SIC2design_residual"],1e-10)
        self.assertEqual(d["whole_chart_invariant"],
                         "sum_z Q_z = 36 Pi_sym(C4 tensor C4)")

    def test_two_ray_gapped_selector_and_entangling_gate(self):
        d=self.hamiltonian
        self.assertAlmostEqual(d["energy_chart_separation_exact"],1/3)
        self.assertTrue(d["generic_interaction_time_creates_two_copy_entanglement"])
        self.assertEqual(d["output_schmidt_rank"],2)
        self.assertAlmostEqual(d["guaranteed_preferred_chart_energy_gap_lower_bound"],
                               1/3-0.2)

    def test_exact_two_copy_Hilbert_Schmidt_Gram_and_spectrum(self):
        d=self.opdual
        self.assertEqual(d["Hermitian_chart_operator_Gram_integer_identity"],
                         "9 G_Q = 36 I - 12 A + 60 J")
        self.assertEqual(d["Gram_Q_spectrum"],{"288":1,"8":24,"0":20})
        self.assertEqual(d["Gram_Q_rank"],25)
        self.assertEqual(d["decomposition_45"],
                         "1 uniform + 20 schedule-only + 24 two-copy-only")

    def test_27_complete_decks_collapse_two_copy_operator_information(self):
        d=self.opdual
        self.assertTrue(d["all_27_complete_schedule_operator_sums_equal_4Pi_sym"])
        self.assertEqual(d["schedule_K_rank"],21)
        self.assertEqual(d["operator_detectable_hidden_chart_weights_dimension"],24)
        self.assertEqual(d["operator_blind_schedule_only_weights_dimension"],20)

    def test_exact_hidden_24dim_operator_inversion(self):
        d=self.opdual
        self.assertLess(d["max_hidden_operator_inverse_error"],1e-11)
        self.assertLess(d["max_20D_schedule_visible_weighted_Q_residual"],1e-11)
        self.assertAlmostEqual(d["HS_norm_squared_of_weighted_Q"],
                               d["HS_isometry_norm_squared_expected"],places=11)

    def test_joint_schedule_and_two_copy_full45_decoder(self):
        d=self.opdual
        self.assertEqual(d["combined_27deck_and_45operator_Gram_spectrum"],
                         {"303":1,"6":20,"8":24})
        self.assertEqual(d["combined_complete_chart_label_dimension"],45)
        self.assertLess(d["full45_joint_inverse_residual"],1e-11)

    def test_graph_metric_collapse_not_gravity(self):
        d=self.causal
        self.assertEqual(d["point_graph_diameter"],2)
        self.assertTrue(d["Lorentzian_continuum_from_naive_GQ_shortest_path_refuted"])
        self.assertTrue(d["scaling_edge_length_to_zero_collapses_metric_diameter"])
        self.assertEqual(len(d["example_rescaled_diameters"]),6)

    def test_three_level_memory_witness(self):
        d=self.causal
        self.assertEqual(d["qutrit_memory_Schmidt_number_fidelity_bounds"],
                         {1:.5,2:.75,3:1.})
        self.assertAlmostEqual(d["noise_p_threshold_to_witness_at_least_3_coherent_levels"],.375)
        self.assertEqual(d["binomial_independent_trials_for_each_one_percent_error_bound"],3685)
        self.assertLess(d["Hoeffding_typeI_and_typeII_error_upper_bound"],.01)

    def test_ideal_memory_noise_synthetic_classification(self):
        d=self.causal["synthetic_shot_memory_results"]
        self.assertTrue(d["0.3"]["reject_Schmidt_number_le_2_at_threshold_0p775"])
        self.assertFalse(d["0.375"]["reject_Schmidt_number_le_2_at_threshold_0p775"])
        self.assertFalse(d["0.5"]["reject_Schmidt_number_le_2_at_threshold_0p775"])

    def test_frozen_certificate(self):
        d=json.loads((ROOT/"data/toe_20261121_optical_tightframe_coherent_Hamiltonian_causal.json")
                     .read_text(encoding="utf8"))
        self.assertEqual(d["status"],"PASS")
        self.assertEqual(len([x for x in d if x.startswith("front")]),6)

if __name__=="__main__":
    unittest.main()
