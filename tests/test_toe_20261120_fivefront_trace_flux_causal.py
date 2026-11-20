"""Regress five TOE falsification fronts, including explicit failed assumptions."""
from __future__ import annotations
import sys,unittest,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from toe_20261120_one_ensemble_centrality import (
    trial_operators,noncentrality,one_ensemble,sample_bound,nonunitary_no_go,
    main as trace_run
)
from toe_20261120_flux_chirality_E6_sieve import (
    links_2d,H_wilson,overlap_index_2d,e6_flux_anomaly,main as flux_run
)
from toe_20261120_causal_composition_falsifiers import (
    nonlinear_physical_address,cocycle_and_associativity,branch_equivalence,
    noisy_six_and_holdout,main as causal_run
)

class ATraceCentrality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=trace_run(write=False)
    def test_single_uniform_ensemble(self):
        c=self.result["centrality"]
        self.assertLess(c["ideal_center"]["noncentrality_Frobenius_squared"],1e-20)
        self.assertGreater(c["seeded_noncentral"]["noncentrality_Frobenius_squared"],7.)
        self.assertEqual(c["d"],9)
        self.assertLess(c["seeded_noncentral"]["one_ensemble_formula_residual"],1e-11)
    def test_critical_spam_false_positive(self):
        c=self.result["centrality"]["biased_preparation_counterexample"]
        self.assertEqual(c["biased_target_amplitude_abs"],1.)
        self.assertGreater(c["true_unitary_noncentral_Frobenius_squared"],3.)
        self.assertAlmostEqual(c["target_trace_norm_distance_to_uniform"],2/9)
    def test_zero_failure_confidence_exact(self):
        s=self.result["finite_shot"]
        self.assertEqual(s["phase_matched_zero_failure_Clopper_Pearson_accepted_shots"],2646)
        self.assertLessEqual(s["phase_matched_zero_failure_squared_Frobenius_upper"],.25**2)
        self.assertEqual(s["unknown_phase_two_quadrature_total_shots"],3961832)
    def test_nonunitary_form_invalid(self):
        n=self.result["nonunitary_failure"]
        self.assertAlmostEqual(n["rank_eight_contraction_true_noncentrality_square"],8/9)
        self.assertAlmostEqual(n["false_unitary_formula_result"],17/9)

class BFluxChirality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=flux_run(write=False)["flux_model"]
    def test_nontrivial_plaquette_curvature_and_zero_flux(self):
        U=links_2d(5,1,2)
        self.assertEqual(U.shape,(2,5,5))
        W=H_wilson(5,links_2d(5,1,0))
        self.assertLess(np.linalg.norm(W-W.conj().T),1e-11)
        self.assertEqual(overlap_index_2d(5,1,0)["index_from_Hermitian_Wilson_spectral_asymmetry"],0)
    def test_E6_charge_squared_index(self):
        rs=self.result["E6_27_branching"]
        self.assertEqual([(x["Spin10_rep"],x["four_dimensional_continuum_flux_index"]) for x in rs],
                         [("16",3),("10",12),("1",48)])
        self.assertTrue(self.result["gauge_rephase_invariance_overlap_index"])
        self.assertTrue(self.result["sign_reversal_under_2D_flux_reversal"])
    def test_anomaly_inflow_required(self):
        a=self.result["flux_zero_mode_4D_anomaly_tests"]
        self.assertEqual(a["U1psi_gravitational"],0)
        self.assertEqual(a["U1psi_cubic"],2160)
        self.assertEqual(a["Spin10_squared_U1psi"],-18)
        self.assertEqual(list(self.result["unfluxed_complete_27_anomalies"].values()),[0,0,0])

class CCausalOrdersAndComposition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=causal_run(write=False)
    def test_physical_bijective_nonlinear_address(self):
        a=self.result["physical_address"]
        self.assertTrue(a["physical_gate_address_map_is_bijective"])
        self.assertTrue(a["basis_generator_gates_unchanged"])
        self.assertEqual(a["all_81_address_pairs_that_fail_bilinear_prediction"],1512)
        self.assertEqual((a["linear_prediction"],a["measured_distorted_phase"]),(0,1))
        self.assertLess(a["composition_residual_normalized_trace_abs"],1e-12)
        self.assertAlmostEqual(a["honest_composition_residual_normalized_trace_abs"],1.,places=12)
    def test_genuine_projective_cocycle_associativity(self):
        c=self.result["cocycle_consistency"]
        self.assertEqual(c["exact_sesquilinear_commutator_address_pairs_checked"],6561)
        self.assertEqual(c["random_cocycle_associativity_triplets_checked"],30000)
    def test_central_order_definite_order_simulation(self):
        c=self.result["causal_order_ambiguity"]
        self.assertLess(c["central_W33_switch_equals_definite_target_order_plus_control_phase_error_max"],1e-12)
        self.assertEqual(c["central_switch_control_target_purification_entanglement_bits"],0)
        self.assertGreater(c["noncentral_seeded_control_vs_purified_target_entropy_bits"],.8)
    def test_realistic_noisy_spam_holdout(self):
        c=self.result["noisy_holdout_planning"]
        self.assertEqual(c["six_basis_and_one_holdout_accepted_control_shots_per_run"],2240)
        self.assertEqual(c["seeded_replications"],1500)
        self.assertEqual(c["distorted_address_detected_given_six_basis_pass_reps"],1500)
        self.assertTrue(c["no_hardware_measured"])

class DCorpusAndReproducibility(unittest.TestCase):
    def test_results_are_not_a_full_theory(self):
        self.assertIn("prior_art",trace_run(write=False))
        self.assertIn("flux_model",flux_run(write=False))
        self.assertIn("boundary",causal_run(write=False))
    def test_no_uncontrolled_file_writes_during_tests(self):
        self.assertTrue(callable(trace_run) and callable(flux_run) and callable(causal_run))

if __name__=="__main__":unittest.main()
