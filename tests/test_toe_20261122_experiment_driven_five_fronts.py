"""Twenty independent checks for the five experiment-driven Witting models."""
from __future__ import annotations
import json,math,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261122_experiment_driven_five_fronts as study

class ExperimentalFiveFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rays,cls.H,cls.A,cls.P=study.witting()
        cls.d=study.main()
        cls.s=cls.d["front1_Witting_reflection_quantum_switch"]
        cls.e=cls.d["front2_classical_minentropy_and_security_boundary"]
        cls.b=cls.d["front3_true_multioutcome_ququart_correlations"]
        cls.g=cls.d["front4_W33_Z2_two_path_AB_interference"]
        cls.k=cls.d["front5_torus_Klein_nonorientable_control"]

    def test_exact_witting_incidence(self):
        self.assertEqual(self.rays.shape,(40,4))
        self.assertEqual(self.H.shape,(45,40))
        self.assertEqual(set(self.H.sum(0)),{9})
        self.assertEqual(set(self.H.sum(1)),{8})

    def test_45D_spectral_decomposition(self):
        self.assertEqual([round(float(np.trace(P)))for P in self.P],[1,20,24])

    def test_switch_all_780_witting_reflections(self):
        self.assertEqual(self.s["unordered_pairs"],780)
        self.assertEqual(self.s["ray_pair_counts"],{"orthogonal":240,"nonorthogonal":540})

    def test_switch_outcome_exact_r(self):
        self.assertAlmostEqual(self.s["noncommuting_minus_probability"],4/9)
        self.assertAlmostEqual(self.s["commuting_minus_probability"],0)
        self.assertLess(self.s["max_analytic_residual"],1e-10)

    def test_switch_blind_to_complex_conjugation(self):
        self.assertTrue(self.s["globally_conjugating_ray_vectors_cannot_change_two_reflection_result"])

    def test_switch_does_not_prove_causal_indefiniteness(self):
        self.assertIn("NOT a device-independent causal inequality",self.s["boundary"])

    def test_full40_entropy(self):
        row=self.e["detector_profiles"][0]
        self.assertAlmostEqual(row["raw_classical_Hmin_bits"],math.log2(40))
        self.assertAlmostEqual(row["given_chart_Hmin_bits"],3)

    def test_four_bit_entropy_loss_for_every_25bin_scheme(self):
        self.assertAlmostEqual(self.e["compression_exact_raw_Hmin_loss_bits"],4.)
        for row in self.e["detector_profiles"][1:]:
            self.assertAlmostEqual(row["raw_classical_Hmin_bits"],math.log2(2.5))
            self.assertAlmostEqual(row["given_chart_Hmin_bits"],math.log2(2.5))

    def test_no_security_certification_in_entropy_count(self):
        self.assertFalse(self.e["security_certified_quantum_min_entropy"])
        self.assertIn("No trusted contextuality test",self.e["boundary"])

    def test_normalized_two_party_ququart_POVM(self):
        Q=study.ray_projectors(self.rays)
        p=np.einsum("aij,bji->ab",Q,Q).real/400
        self.assertAlmostEqual(p.sum(),1)
        np.testing.assert_allclose(p.sum(0),np.full(40,1/40),atol=1e-11)

    def test_exact_two_party_mutual_information(self):
        self.assertAlmostEqual(self.b["detectors"][0]["classical_mutual_information_bits"],
                               .2+.9*math.log2(4/3),places=10)

    def test_coarsening_decreases_two_party_information(self):
        p=self.b["detectors"]
        self.assertGreater(p[0]["classical_mutual_information_bits"],
                           p[1]["classical_mutual_information_bits"])
        self.assertGreater(p[1]["classical_mutual_information_bits"],
                           p[2]["classical_mutual_information_bits"])

    def test_one_setting_local_classical_model_exists(self):
        self.assertTrue(self.b["one_fixed_setting_is_locally_simulable"])
        self.assertIn("NOT Bell-inequality violation",self.b["boundary"])

    def test_actual_W33_collinearity_graph(self):
        self.assertEqual((self.g["vertices"],self.g["edges"],self.g["cycle_rank"]),(40,240,201))
        self.assertEqual(self.g["four_cycles_selected_from_nonadjacent_pair"],540)

    def test_AB_loop_both_flux_polarities(self):
        self.assertEqual(self.g["positive_flux_Pplus"],1)
        self.assertEqual(self.g["negative_flux_Pplus"],0)
        self.assertEqual(self.g["example_loop"][0],self.g["example_loop"][-1])

    def test_AB_local_gauge_invariance(self):
        self.assertEqual(self.g["local_gauge_transformation_checks"],400)

    def test_AB_is_not_dynamic_field(self):
        self.assertIn("STATIC Z2",self.g["boundary"])

    def test_Klein_torus_connected_orientation_double_cover(self):
        values=self.k["grid_comparisons"]
        self.assertEqual([v["Klein_orientation_cover_vertices"]for v in values],[72,128])
        for v in values:
            self.assertEqual(v["Klein_vertical_orientation_holonomy"],-1)
            self.assertEqual(v["torus_orientation_holonomy"],1)

    def test_Klein_torus_different_spectrum_and_odd_closed_walks(self):
        for v in self.k["grid_comparisons"]:
            self.assertGreater(v["spectral_l2_difference"],2)
            self.assertEqual(v["first_odd_Klein_closed_walk_length"],v["L"]+1)
            self.assertGreater(v["first_odd_Klein_closed_walk_count"],0)
            self.assertGreater(v["Klein_min_eigenvalue"],-4.)

    def test_no_experimental_or_TOE_claim(self):
        self.assertEqual(self.d["status"],"PASS")
        self.assertEqual(sum(k.startswith("front")for k in self.d),5)
        self.assertIn("No real measurements",self.d["scope"])
        self.assertIn("not a replica",self.k["boundary"])

if __name__=="__main__":unittest.main()
