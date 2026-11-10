"""W33 next five fronts plus bonus exact octagon unimodular certificates.

These tests recompute selected determinants, reproduce the state-preparation
transfer, gauge cycle rank and binomial size/power using independent calls.
"""
import json,sys,math,unittest
from pathlib import Path
import numpy as np
import networkx as nx
from scipy.stats import binom
from sympy import Matrix
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_flux_mass_gap_design as mass
import w33_20261109_dark_nearest_neighbor_loss as optical
import w33_20261109_octagon_gauge_matter_tradeoff as action
import w33_20261109_full_octagon_integer_gauge_basis as integer
import w33_20261109_dark_photon_binomial_gate as photon
import w33_20261109_deck_octagon_78_3_basis as deck
from w33_20261109_flux_dark_mode_fragility import build

NAMES=["w33_20261109_flux_mass_gap_design",
       "w33_20261109_dark_nearest_neighbor_loss",
       "w33_20261109_octagon_gauge_matter_tradeoff",
       "w33_20261109_full_octagon_integer_gauge_basis",
       "w33_20261109_dark_photon_binomial_gate",
       "w33_20261109_deck_octagon_78_3_basis"]

def get(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))
class W33NextFivePlus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r={n:get(n) for n in NAMES}

    def test_six_certificates_pass(self):
        self.assertTrue(all(r["status"].startswith("PASS") for r in self.r.values()))

    def test_improved_15_flux_gap_and_fixed_link_count(self):
        d=self.r[NAMES[0]]
        self.assertGreater(d["best_15_edge_minimum_singular_gap_pi"],d["initial_15_edge_minimum_singular_gap_pi"]*1.30)
        self.assertEqual(len(d["best_15_edges"]),15)
        self.assertTrue(d["best_production_still_uses_only_15_phase_flips"])
        self.assertEqual(d["stochastic_gap_search"]["random_starts_attempted"],500)

    def test_optimized_flux_exact_integer_det_independent(self):
        B,edges,G=build()
        A=B.astype(int)
        d=self.r[NAMES[0]]
        for e in d["best_15_edges"]:
            self.assertEqual(A[e["point"],e["line"]],1)
            A[e["point"],e["line"]]=-1
        self.assertEqual(str(Matrix(A.tolist()).det(method="domain-ge")),d["best_exact_signed_integer_determinant"])
        self.assertEqual(np.linalg.matrix_rank(A),40)

    def test_low_phase_effective_dark_mass_first_order(self):
        d=self.r[NAMES[0]]
        cases=d["near_zero_phase_comparison"]
        self.assertEqual(len(cases),4)
        self.assertLess(cases[-1]["relative_15_mass_spectrum_error"],.01)
        self.assertGreater(d["first_order_minimal_mass_slope_initial"],0)

    def test_nearest_neighbor_light_cone_saturated(self):
        d=self.r[NAMES[1]]
        self.assertEqual(d["minimum_optical_interference_depth_from_locality"],39)
        self.assertEqual(d["constructive_serial_2port_Givens_count"],39)
        self.assertEqual(d["constructive_depth"],39)
        self.assertEqual(d["phase_pi_flips"],12)
        self.assertEqual(d["target_support_size"],40)
        self.assertLess(d["exact_ideal_preparation_amplitude_error"],1e-12)

    def test_nearest_neighbor_exact_independent_state_reconstruction(self):
        B,edges,G=build()
        p=np.array(self.r[NAMES[1]]["target_photonic_mode_amplitudes"])
        self.assertLess(np.linalg.norm(B.T@p),1e-12)
        actual,program=optical.construction(p,1.)
        self.assertLess(np.linalg.norm(actual-p),1e-12)
        self.assertEqual(len(program),39)

    def test_nearest_neighbor_loss_accounting_and_label_cost(self):
        d=self.r[NAMES[1]]["per_two_mode_gate_intensity_survival_controls"]
        self.assertLess(d["0.99"]["natural_40port_label_order"]["source_survival"],1)
        self.assertGreater(d["0.99"]["intensity_sorted_output_label_order"]["source_survival"],
                           d["0.99"]["natural_40port_label_order"]["source_survival"])
        self.assertGreater(d["0.99"]["natural_40port_label_order"]["conditional_target_state_fidelity"],.99)

    def test_all_1620_octagon_positive_wilson_cost(self):
        d=self.r[NAMES[2]]
        self.assertEqual(d["fundamental_octagon_count"],1620)
        self.assertEqual(d["fifteen_edge_cases"]["flat"]["octagons_odd_pi_flux"],0)
        self.assertEqual(d["fifteen_edge_cases"]["minimal_gap_optimized"]["octagons_odd_pi_flux"],729)
        self.assertEqual(d["fifteen_edge_cases"]["minimal_gap_optimized"]["Wilson_action_per_unit_plaquette_coupling"],1458)
        self.assertEqual(d["three_deck_Z2_corner_octagon_controls"][-1]["octagon_pi_odd_count"],233)

    def test_finite_matter_can_compete_with_positive_gauge_penalty(self):
        cases=self.r[NAMES[2]]["finite_half_filled_free_fermion_vs_positive_local_Wilson_action"]
        self.assertEqual(len(cases),3)
        at1=next(row for row in cases if row["inverse_temperature"]==1.)
        q=at1["two_flux_cases_compared_to_flat"]["minimal_gap_optimized"]
        self.assertLess(q["fermion_free_energy_minus_flat"],0)
        self.assertGreater(q["critical_gauge_penalty_weight_to_tie_flat_if_fermion_favors_flux"],0)
        self.assertLess(q["critical_gauge_penalty_weight_to_tie_flat_if_fermion_favors_flux"],.001)

    def test_full_octagon_selected_Z_basis_exact_minor(self):
        B,edges,G=build()
        d=self.r[NAMES[3]]
        self.assertEqual(d["shortest_8cycle_count"],1620)
        self.assertEqual(d["all_octagon_chord_matrix_rank_over_each_prime"],{str(p):81 for p in (2,3,5,7,11)})
        self.assertEqual(d["exact_integer_determinant_of_selected_81_octagon_minor"],"1")
        self.assertTrue(d["selected_integer_minor_unimodular"])
        self.assertEqual(len(d["GF2_selected_81_octagon_row_ids"]),81)

    def test_independent_selected_integer_minor_recomputation(self):
        B,edges,G=build()
        tree=nx.bfs_tree(G,0).to_undirected()
        chords=sorted(set(tuple(sorted(e)) for e in G.edges())-
                      set(tuple(sorted(e)) for e in tree.edges()))
        c={frozenset(e):j for j,e in enumerate(chords)}
        loops=action.loops_length8(G)
        ids=self.r[NAMES[3]]["GF2_selected_81_octagon_row_ids"]
        M=np.zeros((81,81),dtype=int)
        for row,id in enumerate(ids):
            ring=loops[id]
            for a,b in zip(ring,ring[1:]+ring[:1]):
                j=c.get(frozenset((a,b)))
                if j is not None:M[row,j]+=1 if a<40 else -1
        self.assertEqual(Matrix(M.tolist()).det(method="domain-ge"),1)

    def test_exact_78_plus_3_integer_deck_split(self):
        d=self.r[NAMES[5]]
        self.assertEqual(d["old_TOE38_local_zero_winding_octagons"],1382)
        self.assertEqual(d["old_TOE38_nonzero_three_deck_winding_octagons"],238)
        self.assertEqual(d["local_zero_deck_octagon_integer_chord_rank_mod_primes"],{"2":78,"3":78,"5":78})
        m=d["explicit_integer_Z81_basis_from_exact_actual_octagons"]
        self.assertEqual(m["zero_deck_octagons"],78)
        self.assertEqual(m["nonzero_deck_octagons"],3)
        self.assertEqual(m["determinant"],"1")
        self.assertEqual(len(m["three_selected_deck_winding_vectors"]),3)

    def test_photon_ideal_null_and_gapped_state(self):
        d=self.r[NAMES[4]]["all_traces_from_ideal_initial_40port_dark_state"]
        self.assertLess(d["0"]["max_line_probability_within_time_0_to_6"],1e-20)
        self.assertEqual(d["0"]["remaining_chiral_zero_modes"],30)
        self.assertEqual(d["15"]["remaining_chiral_zero_modes"],0)
        self.assertGreater(d["15"]["max_line_probability_within_time_0_to_6"],.6)

    def test_photon_exact_binomial_size_power_guarantee(self):
        d=self.r[NAMES[4]]["all_traces_from_ideal_initial_40port_dark_state"]
        for k in ("1","14","15"):
            n=d[k]["exact_binomial_5pct_false_positive_95pct_power"]
            self.assertLessEqual(n["exact_false_positive_probability"],.05+1e-12)
            self.assertGreaterEqual(n["exact_power_under_pessimistic_alternative"],.95-1e-12)
            c=photon.threshold(n["launched_trials"],d[k]["conservative_null_probability_upper"])
            self.assertEqual(c,n["required_line_click_count"])

    def test_s9_still_pre_registered_and_not_scored(self):
        d=get("w33_20261109_s9_frozen_manifest_attack")
        self.assertFalse(d["real_S9_Delta_chi2_scored"])
        self.assertFalse(d["independent_publisher_SHA256_and_full_FITS"])
        self.assertEqual(d["frozen_date"],"2026-11-08")

if __name__=="__main__":unittest.main()
