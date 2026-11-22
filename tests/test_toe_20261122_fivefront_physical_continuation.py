"""Regression for five Witting follow-up producers and their negative controls.
Run the five analysis producers before this suite; it reads their JSON.
"""
from __future__ import annotations
import json,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261122_witting_3design_collision_moments as design
import toe_20261122_witting_coherence_cloning_capacity as coherence
import toe_20261122_witting_40mode_naimark_finite_shots as optical
import toe_20261122_w33_two_plaquette_pair_creation as gauge
import toe_20261122_witting_multicriteria_dualframe_search as readout
import toe_20261122_actual_witting_4to9_dephasing as realchannel
def load(name):
    f=ROOT/"data"/("toe_20261122_"+name+".json")
    if not f.exists():raise RuntimeError("Run producer before tests: "+str(f))
    return json.loads(f.read_text(encoding="utf8"))

class PhysicalFivefrontContinuation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load("witting_3design_collision_moments")
        cls.c=load("witting_coherence_cloning_capacity")
        cls.o=load("witting_40mode_naimark_finite_shots")
        cls.g=load("w33_two_plaquette_pair_creation")
        cls.r=load("witting_multicriteria_dualframe_search")
        cls.a=load("actual_witting_4to9_dephasing")

    def test_all_five_independent_producers_pass(self):
        self.assertEqual([d["status"]for d in (self.d,self.c,self.o,self.g,self.r)],["PASS"]*5)

    def test_witting_third_moment_is_exact_but_MUB_is_not(self):
        self.assertLess(self.d["Witting40_3design_max_matrix_error"],1e-11)
        self.assertGreater(self.d["fiveMUB20_not_3design_max_matrix_error"],.1)

    def test_fourth_moment_fails_higher_design_lower_bound(self):
        self.assertTrue(self.d["not_4design"])
        self.assertAlmostEqual(self.d["Witting_frame_potentials"]["4"],1/30,places=10)
        self.assertAlmostEqual(self.d["fiveMUB_frame_potentials"]["3"],1/16,places=10)

    def test_three_copy_purity_formula(self):
        self.assertIn("Tr(rho^3)",self.d["purity_reconstruction_identity"])
        self.assertAlmostEqual(
            self.d["random_mixed_rho_C3"],
            (1+3*self.d["random_mixed_rho_Tr_rho2"]+2*self.d["random_mixed_rho_Tr_rho3"])/3000,
            places=11)

    def test_witting_pure_triple_collision_state_independent(self):
        rows=[r for r in self.d["independent_input_collision_tests"]if r["POVM"]=="Witting40"]
        self.assertEqual(len(rows),2)
        for row in rows:
            self.assertAlmostEqual(row["pair_collision"],.04)
            self.assertAlmostEqual(row["triple_collision"],.002)

    def test_cloner_is_symmetric_broadcast_channel(self):
        self.assertAlmostEqual(self.c["cloner_both_marginals_depolarizing_alpha"],.6)
        self.assertLess(self.c["max_cloning_marginal_residual"],1e-11)

    def test_capacity_zero_before_entanglement_breaking(self):
        self.assertEqual(self.c["zero_quantum_capacity_proven_for_lambda_ge"],.5)
        self.assertEqual(self.c["entanglement_breaking_only_at_lambda"],1)
        s=next(x for x in self.c["scan"]if x["lam"]==.6)
        self.assertTrue(s["zero_capacity_by_antidegradability"])
        self.assertFalse(s["entanglement_breaking"])
        self.assertGreater(s["Choi_negativity"],0)

    def test_oneuse_capacity_witness_not_upper_bound(self):
        self.assertGreater(self.c["coherent_information_witness_zero_lambda"],.35)
        self.assertLess(self.c["coherent_information_witness_zero_lambda"],.41)
        self.assertIn("do not decide",self.c["limits"])

    def test_isometry_reconstruction_and_rotation_count(self):
        self.assertEqual(self.o["Naimark_isometry_shape"],[40,4])
        self.assertEqual(self.o["number_two_mode_Givens_rotations"],150)
        self.assertLess(self.o["max_isometry_reconstruction_residual"],1e-10)

    def test_optical_loss_is_not_uniform_by_input_state(self):
        x=next(z for z in self.o["loss_sweep"]if z["per_active_two_mode_element_loss"]==.01)
        self.assertAlmostEqual(x["mean_power_survival"],.8076565962239846,places=8)
        self.assertLess(x["worst_state_power_survival"],x["best_state_power_survival"])

    def test_binomial_launch_budget_hits_size_and_power(self):
        for x in self.o["binomial_one_sided_5sigma_90percent_power"]:
            self.assertLessEqual(x["null_binomial_size"],2.866515718791933e-7)
            self.assertGreaterEqual(x["alternative_power"],.9)
        self.assertIn("NOT included",self.o["limits"])

    def test_two_W33_plaquettes_share_exact_one_edge(self):
        self.assertEqual(len(self.g["W33_vertices"]),6)
        self.assertEqual(len(self.g["seven_edges_as_local_indices"]),7)
        mask=self.g["two_Wilson_link_masks"]
        self.assertEqual((mask[0]&mask[1]).bit_count(),1)

    def test_exact_128D_Gauss_sector(self):
        self.assertEqual(self.g["kinematic_matter_link_hilbert_dim"],8192)
        self.assertEqual(self.g["Gauss_positive_sector_hilbert_dim"],128)

    def test_static_charge_energy_tracks_shortest_path(self):
        self.assertEqual(len(self.g["static_B0_h1_energy_by_pair_separation"]),15)
        for x in self.g["static_B0_h1_energy_by_pair_separation"]:
            self.assertAlmostEqual(x["electric_energy_over_vacuum"],2*x["distance"])

    def test_matter_creation_changes_plaquette_dynamics(self):
        q=self.g["dynamical_pair_sweep"]
        weak=next(x for x in q if x["case"]=="weak_creation"and x["t"]==1.5)
        strong=next(x for x in q if x["case"]=="strong_creation"and x["t"]==1.5)
        self.assertGreater(strong["mean_dynamical_matter_count"],weak["mean_dynamical_matter_count"]+1)

    def test_readout_all_controls_full_rank(self):
        e=readout.Evaluator()
        for row in (readout.OLD,readout.NEW,self.r["best_seeded_candidate_labels_zero_based"]):
            self.assertEqual(e.eval(row)["local_POVM_rank"],16)

    def test_readout_constructive_variance_gain_and_tradeoff(self):
        b=self.r["best_seeded_candidate_metrics"]
        n=self.r["initial_new25"]
        self.assertLess(b["single_shot_fidelity_SD"],n["single_shot_fidelity_SD"])
        self.assertLess(b["chart_leakage_MI_bits"],1.46)
        self.assertLess(b["worst_drift_gain_per_RMS"],1.65)
        self.assertGreater(b["worst_drift_gain_per_RMS"],n["worst_drift_gain_per_RMS"])

    def test_readout_search_reproducible_seed(self):
        self.assertEqual(self.r["seed"],444)
        self.assertEqual(self.r["candidate_attempts"],50000)
        self.assertEqual(len(set(self.r["best_seeded_candidate_labels_zero_based"])),24)

    def test_all_models_disclaim_TOE_physical_measurements(self):
        self.assertIn("physical QCD experiment",self.g["limits"])
        self.assertIn("no physical",self.d["limits"].lower())
        self.assertIn("not a global",self.r["limits"].lower())


    def test_native_Witting_routed_channel_has_five_kraus(self):
        self.assertEqual(self.a["Kraus_shape"],[5,9,4])
        self.assertGreater(self.a["positive_maximally_mixed_input_coherent_information_at_zero"],1)

    def test_native_output_dephasing_lowers_coherent_information(self):
        self.assertGreater(self.a["positive_coherent_information_ends_for_maxmixed_at_lambda"],.22)
        self.assertLess(self.a["positive_coherent_information_ends_for_maxmixed_at_lambda"],.24)
        vals=[x["maximally_mixed_input_coherent_information_bits"]for x in self.a["scans"]]
        self.assertGreater(vals[0],vals[1])
        self.assertGreater(vals[1],vals[2])

    def test_full_rail_dephasing_is_EB_but_partial_noise_capacity_unknown(self):
        self.assertTrue(self.a["fully_dephased_lambda1_is_entanglement_breaking"])
        self.assertIn("does NOT prove capacity zero",self.a["essential_scope"])

if __name__=="__main__":unittest.main()
