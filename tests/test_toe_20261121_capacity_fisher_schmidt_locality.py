"""Offline tests for six sourced Witting capacity, Fisher, device, and causal fronts."""
from __future__ import annotations
import json
import math
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_capacity_fisher_schmidt_locality as f


class TestCapacityFisherLocality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rays,S,decks,A,P,O=f.geometry()
        cls.ch=f.positive_capacity_front(rays)
        cls.fi=f.fisher_front(S,O)
        cls.opt=f.optical_front(rays,S,O)
        cls.h=f.hamiltonian_front(P,S,O)
        cls.sp=f.causal_front(A)
        cls.loss=f.loss_orthogonality_front(S,O)

    def test_canonical_positive_quantum_capacity(self):
        self.assertGreater(self.ch["canonical_maxmixed_coherent_information_bits"],.43)
        self.assertGreater(self.ch["canonical_unassisted_quantum_capacity_lower_bound_qubits_per_use"],0)
        self.assertEqual(self.ch["canonical_Choi_rank"],5)

    def test_output_routing_improves_valid_9dim_capacity(self):
        d=self.ch
        self.assertEqual(sorted(d["best_explicit_perm_45_output_modes"]),list(range(45)))
        self.assertGreater(d["routed_maxmixed_coherent_information_bits"],1.08)
        self.assertGreater(d["routed_maxmixed_coherent_information_bits"],
                           d["canonical_maxmixed_coherent_information_bits"])
        self.assertEqual(d["routed_Choi_rank"],5)

    def test_erasure_flag_is_a_separate_ten_dimensional_channel(self):
        d=self.ch
        self.assertEqual(d["erasure_flag_augmented_output_dim"],10)
        self.assertGreater(d["routed_10D_erasure_channel_positive_lower_bound_for_p_less_than"],.35)
        self.assertLess(d["routed_10D_erasure_channel_positive_lower_bound_for_p_less_than"],.36)

    def test_local_Fisher_isotropic_24dim(self):
        d=self.fi
        self.assertEqual(d["hidden_classical_chart_bias_dimension"],24)
        self.assertEqual(d["full_nonorthogonal_pair_count"],540)
        self.assertAlmostEqual(d["reference_matching_probability"],2/15)
        self.assertTrue(d["uniform_540_probe_locally_A_and_E_optimal_at_uniform_chart_weights"])
        self.assertAlmostEqual(d["uniform_full_540_probe_Aoptimal_Cramer_Rao_MSE_coefficient"],4492.8)

    def test_sparse_design_higher_shot_cost_than_uniform(self):
        d=self.fi
        self.assertEqual(len(d["24_probe_exchange_candidate_pair_indices"]),24)
        self.assertAlmostEqual(d["24_probe_exchange_candidate_Acriterion_coefficient"],11681.28,places=4)
        self.assertGreater(d["local_Acriterion_relative_penalty_of_sparse_candidate"],2.5)
        self.assertGreater(d["total_iid_shots_needed_for_CR_lower_bound_MSE_1e_minus6"],4_000_000_000)

    def test_45_noisy_nearest_rail_meshes(self):
        d=self.opt
        self.assertEqual(d["mesh_count"],45)
        self.assertEqual(d["correct_chart_after_gate_errors_out_of_540"],540)
        self.assertLess(d["worst_reconstructed_interferometer_unitary_2norm_error"],.0028+1e-10)
        self.assertLess(d["assumed_systematic_unitary_per_gate_error_radians"],
                        d["rigorous_sufficient_per_gate_operator_error_for_unique_chart"])

    def test_schmidt_rank8_for_all_45_chart_interactions(self):
        d=self.h
        self.assertEqual(d["charts_verified"],45)
        self.assertEqual(d["operator_schmidt_rank_each_two_copy_chart"],8)
        self.assertEqual(d["explicit_minimal_sum_of_product_operators"],8)
        self.assertEqual(d["per_chart_two_block_Pauli_correlation_terms"],6)
        self.assertLess(d["max_Pauli_product_compilation_residual"],1e-10)

    def test_noncollapsing_spatial_lattice_has_constant_local_degree(self):
        d=self.sp
        self.assertEqual(d["vertex_degree_all_L"],18)
        self.assertEqual(d["limiting_noncollapsed_spatial_metric"],
                         "3-torus with L1 (taxicab) metric")
        self.assertAlmostEqual(d["limiting_scaled_diameter"],1.5)
        self.assertTrue(d["internal_45point_fiber_scaled_diameter_goes_to_zero"])

    def test_graph_sequence_diameter_and_diffusion_gap(self):
        vals=self.sp["sequence"]
        self.assertEqual([x["cycle_length"] for x in vals],[4,8,16,32,64])
        self.assertTrue(all(vals[i+1]["graph_vertices"]>vals[i]["graph_vertices"]
                            for i in range(len(vals)-1)))
        self.assertGreater(vals[0]["scaled_metric_diameter"],
                           vals[-1]["scaled_metric_diameter"])
        self.assertLess(vals[-1]["normalized_laplacian_gap"],
                        vals[0]["normalized_laplacian_gap"])

    def test_throughput_and_24dim_chart_bias_scores_orthogonal(self):
        d=self.loss
        self.assertTrue(d["full540_local_FI_throughput_hidden_bias_cross_block_zero"])
        self.assertLess(d["max_FI_cross_block_residual"],1e-10)
        self.assertLess(d["centered_response_sum_over_all_540_pairs_residual"],1e-10)

    def test_saved_certificate(self):
        p=ROOT/"data/toe_20261121_capacity_fisher_schmidt_locality_sixfront.json"
        d=json.loads(p.read_text(encoding="utf8"))
        self.assertEqual(d["status"],"PASS")
        self.assertEqual(len([k for k in d if k.startswith("front")]),6)


if __name__=="__main__":
    unittest.main()
