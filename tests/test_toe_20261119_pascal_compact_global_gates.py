"""All six independent Pascal-H27 physical compatibility gates."""
import sys,unittest
from math import sqrt
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_pascal_compact_global_gates as m

class SixPhysicalGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=m.run()

    def test_exact_pascal_Gram_l2(self):
        P,K,e=m.pascal_gram()
        self.assertTrue(np.allclose(e,[m.PHI**-4,1,1,m.PHI**4]))
        self.assertTrue(np.allclose(K,P.T@P))
    def test_noncompact_three(self):
        self.assertEqual(self.r["compact_index"]["noncompact_three_chiral_index"],3)
    def test_compact_index_zero(self):
        self.assertEqual(self.r["compact_index"]["periodic_S1_Fredholm_index"],0)
    def test_compact_three_mirror_wall_candidates(self):
        x=self.r["compact_index"]
        self.assertEqual(x["left_wall_candidates"],3)
        self.assertEqual(x["right_antiwall_candidates"],3)
    def test_no_exact_periodic_zero_at_m0_2(self):
        x=self.r["compact_index"]
        self.assertEqual(x["circle_at_m0_2_exact_zero_modes"],0)
        self.assertTrue(all(not q["exact_periodic_zero_mode"] for q in x["channels"]))
    def test_compact_sign_changes_even(self):
        self.assertEqual([q["mass_sign_changes"] for q in self.r["compact_index"]["channels"]],[0,2,2,2])
    def test_old_wall_degenerate_profiles_rank2(self):
        self.assertEqual(self.r["localized_masses"]["unperturbed_profile_rank"],2)
        self.assertLess(self.r["localized_masses"]["unperturbed_profile_Gram_eigenvalues"][0],1e-10)
    def test_small_flavor_splitting_restores_three_independent_profiles(self):
        self.assertEqual(self.r["localized_masses"]["perturbed_profile_rank"],3)
        self.assertGreater(self.r["localized_masses"]["perturbed_profile_Gram_eigenvalues"][0],1e-6)
    def test_one_defect_mass_rank_one(self):
        self.assertEqual(self.r["localized_masses"]["defect_rank_census"][0]["Y_rank_at_tol_1e_minus10"],1)
    def test_two_defects_mass_rank_two(self):
        self.assertEqual(self.r["localized_masses"]["defect_rank_census"][1]["Y_rank_at_tol_1e_minus10"],2)
    def test_three_defects_mass_rank_three(self):
        self.assertEqual(self.r["localized_masses"]["defect_rank_census"][2]["Y_rank_at_tol_1e_minus10"],3)
    def test_hierarchical_toy_Y_is_not_prediction(self):
        y=self.r["localized_masses"]["defect_rank_census"][2]["Y_singular_values"]
        self.assertLess(y[-1]/y[0],1e-8)
        self.assertIn("inserted",self.r["localized_masses"]["qualification"])
    def test_pascal_mass_not_equivariant_in_H27_1_plus3(self):
        r=self.r["H27_GUT_anomalies"]
        self.assertGreater(r["4_channel_PascalK2_H27_shift_commutator_norm"],2)
        self.assertGreater(r["4_channel_PascalK2_H27_clock_commutator_norm"],5)
    def test_SM_complete_16_anomaly_ledger(self):
        self.assertEqual(len(self.r["H27_GUT_anomalies"]["local_SM_anomalies_for_complete_Spin10_16"]),5)
        self.assertEqual(self.r["H27_GUT_anomalies"]["Witten_doublets_three_complete_16"],12)
    def test_pascal_Boolean_inclusion_graph_exact_edges(self):
        for row in self.r["pascal_graph"]["levels"]:
            self.assertEqual(row["edges"],3**row["L"]-2**row["L"])
    def test_pascal_graph_has_universal_vertices(self):
        for row in self.r["pascal_graph"]["levels"]:
            self.assertEqual(row["max_degree"],row["N"]-1)
    def test_pascal_graph_diameter2_for_all_L_ge2(self):
        for row in self.r["pascal_graph"]["levels"]:
            if row["L"]>=2:self.assertEqual(row["diameter"],2)
    def test_pascal_raw_graph_no_local_continuum_gap(self):
        for row in self.r["pascal_graph"]["levels"]:
            self.assertGreater(row["laplacian_lambda2"],.99)
    def test_pascal_K_equals_exponential_rotated_hypercube_adjacency(self):
        x=self.r["Pascal_hypercube_log_mass_equivalence"]
        for r in x["tests"]:
            self.assertLess(r["max_operator_K_minus_expm_error"],2e-10)
    def test_hasse_Pascal_cover_is_hypercube(self):
        for r in self.r["Pascal_hypercube_log_mass_equivalence"]["tests"]:
            self.assertEqual(r["cover_graph_degree"],r["L"])
            self.assertEqual(r["cover_graph_diameter"],r["L"])
    def test_hypercube_inclusion_cover_exact_edge_count(self):
        for r in self.r["Pascal_hypercube_log_mass_equivalence"]["tests"]:
            self.assertEqual(r["cover_graph_edges"],r["L"]*2**(r["L"]-1))
    def test_log_pascal_mass_hypercube_binomial_spectrum(self):
        for r in self.r["Pascal_hypercube_log_mass_equivalence"]["tests"]:
            self.assertEqual(len(r["hypercube_adjacency_eigenvalues_with_multiplicity"]),2**r["L"])
            self.assertEqual(r["hypercube_adjacency_eigenvalues_with_multiplicity"][0],-r["L"])
            self.assertEqual(r["hypercube_adjacency_eigenvalues_with_multiplicity"][-1],r["L"])
    def test_hypercube_dimension_grows_with_dyadic_level(self):
        x=self.r["Pascal_hypercube_log_mass_equivalence"]
        self.assertIn("increasing its graph dimension L",x["obstruction"])
    def test_optical_CHSH_upper_bound_decreases_with_jitter(self):
        rows=self.r["photon"]["cases"]
        self.assertGreater(rows[0]["optimistic_unconditional_CHSH_upper_bound"],rows[-2]["optimistic_unconditional_CHSH_upper_bound"])
    def test_optical_significance_shows_severe_dephasing_cost(self):
        rows=self.r["photon"]["cases"]
        self.assertGreater(rows[-2]["Hoeffding_alpha_0p05_trials_targeting_upper_bound_gap"],1e9)
    def test_deformed_H27_transverse_gradient_not_zero(self):
        self.assertEqual(self.r["new_H27_deformed_wall"]["transverse_force_x_half_g_quarter"],"25/64")
    def test_deformed_old_MUB_not_stationary(self):
        self.assertEqual(self.r["new_H27_deformed_wall"]["gradient_at_old_111_endpoint_g_quarter"],[1,1,1])
    def test_new_conditional_BPS_tension_differs(self):
        self.assertEqual(self.r["new_H27_deformed_wall"]["conditional_BPS_tension_if_wall_exists"],"13/6")
        self.assertEqual(self.r["new_H27_deformed_wall"]["old_undeformed_wall_tension"],"1")
    def test_no_claim_full_TOE(self):
        self.assertIn("unsolved",self.r["limitations"])
        self.assertIn("unknown",self.r["new_H27_deformed_wall"]["failure"])

if __name__=="__main__":unittest.main()
