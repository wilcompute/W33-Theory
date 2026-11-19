"""Regressions for E8 Green-Schwarz design, unification/KK, signed causal layers, and Bell."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_two_GS_axions_causal_layer_and_Bell_gates as m
from math import pi,sqrt,log

class FiveGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=m.global_e8_anomaly_two_axions()
        cls.y=m.yukawa_hierarchy_and_overlap_gap()
        cls.g=m.orbifold_KK_and_zero_mode_count()
        cls.c=m.signed_causal_layer_cancellation()
        cls.b=m.postselection_Bell_detection_loophole()

    def test_source_gravity_and_mixed_anomalies_share_direction(self):
        self.assertEqual(self.e["gravitational_U1_anomaly_vector"],[20,10,10])
        self.assertEqual(self.e["Spin10sq_U1_anomaly_vector"],[2,1,1])
        self.assertEqual(len(self.e["chiral_source_fields"]),16)

    def test_one_axion_not_enough_for_cubic_anomaly(self):
        self.assertTrue(self.e["one_axion_no_go"])
        self.assertNotEqual(self.e["cubic_on_one_axion_kernel"],"0")
        self.assertIn("b - 5*c",self.e["cubic_on_one_axion_kernel"])

    def test_two_axion_anomaly_polynomial_identity(self):
        import sympy as sp
        b,c=sp.symbols("b c")
        q2=sp.sympify(self.e["two_axion_P_decomposition_Q2"])
        self.assertEqual(sp.expand(q2-sp.Rational(3,2)*(b+c)*(5*b-c)),0)
        self.assertEqual(self.e["two_axion_exact_factorization_residual"],"0")
        self.assertEqual(self.e["two_axion_shift_vectors"],[[2,1,1],[0,1,-5]])

    def test_two_axion_design_still_needs_inflow(self):
        self.assertIn("NOT sufficient",self.e["scientific_status"])
        self.assertIn("no further chiral charged fields",self.e["assumptions"])

    def test_formal_yukawa_rank_does_not_give_hierarchy(self):
        self.assertGreater(self.y["max_min_spurion_ratio"],1.)
        self.assertLess(self.y["max_min_spurion_ratio"],1.5)
        self.assertGreater(self.y["minimum_overlap_or_Higgs_projection_coupling_spread"],69000)

    def test_two_distinct_Higgs_10s_need_doublet_alignment(self):
        self.assertIn("10_34",self.y["independent_10_H_representation_issue"])
        self.assertIn("10_24",self.y["independent_10_H_representation_issue"])
        self.assertIn("bulk cup",self.y["source_bulk_cup_gate"])

    def test_orbifold_adjoints_zero_mode_multiplicities(self):
        self.assertEqual(self.g["adjoint_parity_even_total"],12)
        self.assertEqual(self.g["adjoint_parity_even_total"]+self.g["odd_total"],24)
        self.assertEqual(self.g["zero_mode_multiplicity"][1]["weak_triplet_zero_modes"],2)
        self.assertEqual(self.g["zero_mode_multiplicity"][1]["color_octet_zero_modes"],2)
        self.assertEqual(self.g["zero_mode_multiplicity"][1]["X_leptoquark_zero_modes"],0)

    def test_KK_log_threshold_is_not_cutoff_independent(self):
        rows=self.g["KK_samples"]
        self.assertEqual([r["KK_levels_N"] for r in rows],[8,32,128,512,2048])
        self.assertTrue(all(rows[i+1]["parity_split_log_mass_sum"]>
                            rows[i]["parity_split_log_mass_sum"] for i in range(4)))

    def test_KK_asymptotic_half_log_and_gamma(self):
        rows=self.g["KK_samples"]
        self.assertAlmostEqual(rows[-1]["asymptotic_minus_half_log_N"],
                               log(2/sqrt(pi)),places=3)

    def test_causal_three_layer_weights_are_unique_over_rationals(self):
        self.assertTrue(self.c["unique_primitive_integer_weight_solution_up_to_scale"])
        self.assertEqual(self.c["weights"],[1,-5,4])

    def test_signed_causal_leading_sqrt_density_cancels(self):
        self.assertLess(abs(self.c["leading_sqrt_density_cancel_residual"]),1e-11)
        self.assertEqual(self.c["weights"],[1,-5,4])

    def test_signed_causal_subleading_log_density_cancels(self):
        self.assertEqual(self.c["subleading_log_density_cancel_residual"],0.0)
        self.assertEqual(self.c["finite_asymptotic_signed_sum"],3.0)

    def test_signed_causal_numerical_limit(self):
        rows=self.c["sampled"]
        self.assertTrue(all(rows[i+1]["signed_1_minus5_plus4"]<
                            rows[i]["signed_1_minus5_plus4"] for i in range(len(rows)-1)))
        self.assertAlmostEqual(rows[-1]["signed_1_minus5_plus4"],3,delta=.012)

    def test_signed_operator_not_literal_neighbour_count(self):
        self.assertIn("SIGNED",self.c["important_boundary"])
        self.assertIn("Order-only interval layer counts",self.c["important_boundary"])

    def test_local_hidden_variables_fake_superquantum_CHSH_with_detection(self):
        self.assertEqual(self.b["postselected_CHSH"],4.)
        self.assertEqual(self.b["postselected_correlations"],
                         {"00":1.,"01":1.,"10":1.,"11":-1.})
        self.assertEqual(set(self.b["per_setting_joint_detection_efficiency"].values()),{.25})

    def test_proper_event_ready_model_stays_local(self):
        self.assertLessEqual(abs(self.b["unconditioned_fair_event_ready_CHSH"]),2)
        self.assertIn("pre-choice",self.b["physical_conclusion"])

if __name__=="__main__":unittest.main()
