"""Regression tests for the November-18 five-front independent physics audit."""
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_W33_triperiodic_Levi_homogenization as W
import toe_20261118_fivefront_Klein_F4_winding_memory as P


class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.le=P.run()
        cls.co=W.run()

    def test_klein_group_centralizer_and_elliptic_restriction(self):
        d=self.le["Klein_gauge"]
        self.assertEqual(d["parent_PSL_order"],660)
        self.assertEqual(d["centralizer_order"],12)
        self.assertEqual(d["effective_residual_action_order"],6)
        self.assertEqual((d["V4_joint_plus_dimension"],d["S_plus_T_minus_dimension"]),(2,1))
        self.assertNotEqual(d["mod23_binary_cubic_discriminant"],0)
        self.assertEqual(d["T_projective_fixed_points_on_E"],4)

    def test_klein_rational_moduli_no_go(self):
        d=self.le["Klein_gauge"]
        self.assertEqual((d["b1_Q"],d["quotient_b1_rational"]),(2,0))
        self.assertEqual((d["b2_Q"],d["quotient_b2_rational"]),(2,0))
        self.assertEqual((d["quotient_b0_rational"],d["quotient_b3_rational"]),(1,1))
        self.assertEqual(d["induced_T_action_H1_E"],"-identity")

    def test_F4_one_loop_scale_separation(self):
        d=self.le["F4_RG"]
        self.assertAlmostEqual(d["color_match_GeV"],138472.95943940224,places=5)
        self.assertAlmostEqual(d["hypercharge_match_log10_GeV"],32.56961486264917)
        self.assertGreater(d["separation_lnmu"],60)
        self.assertAlmostEqual(d["color_match_residual_hypercharge"],-18.93045915,delta=.01)

    def test_F4_no_UV_completeness_claim(self):
        d=self.le["F4_RG"]
        self.assertTrue(d["no_common_one_loop_SM_scale"])
        self.assertIn("threshold",d["limitation"])

    def test_winding_sharp_hermite_boundary_and_cusp(self):
        d=self.le["winding"]
        self.assertAlmostEqual(d["universal_unstable_threshold_ratio"],2*math.sqrt(3)/math.pi)
        self.assertTrue(d["square_ratio1"]["BF_violation"])
        self.assertTrue(d["hexagonal_ratio1"]["BF_violation"])
        self.assertEqual(d["minimum_m2L2"],-25/4)
        self.assertTrue(d["cusp_still_unstable_at_any_fixed_finite_positive_ratio"])

    def test_quantum_memory_choi_entanglement(self):
        d=self.le["photon"]
        self.assertAlmostEqual(d["choi_fidelity"],7/15)
        self.assertAlmostEqual(d["negativity"],1/5)
        self.assertEqual(sum(v<-.01 for v in d["Choi_PT_eigenvalues"]),3)
        self.assertEqual(d["depolarizing_EB_threshold_eta"],1/4)

    def test_quantum_memory_accepted_event_errors(self):
        d=self.le["photon"]["exact_one_sided_99percent_both_errors"]
        self.assertEqual((d["accepted_shots"],d["plus_click_threshold"]),(292,117))
        self.assertLess(d["false_positive"],.01)
        self.assertLess(d["false_negative"],.01)

    def test_W33_base_and_finite_covers(self):
        d=self.co
        self.assertEqual(d["base"]["cycle_rank"],81)
        self.assertEqual(d["selected_tree_chords"],[[1,45],[16,45],[28,46]])
        self.assertEqual([(x["vertices"],x["edges"]) for x in d["n_covers"]],
                         [(640,1280),(2160,4320)])
        self.assertEqual([x["cycle_rank"] for x in d["n_covers"]],[641,2161])

    def test_exact_K_matrix_and_ellipticity(self):
        d=self.co
        self.assertEqual(d["conductance_matrix_K_over_160_numerators"],
                         [[81,-27,9],[-27,81,-3],[9,-3,81]])
        self.assertGreater(min(d["eigenvalues_K"]),.3)
        self.assertEqual(d["effective_edge_resistance"],"79/160")
        self.assertEqual(d["diffusion_matrix_denominator"],12800)

    def test_bloch_remainder_decreases_quadratically(self):
        d=self.co
        errs=[x["relative_error"] for x in d["bloch_diagnostics"]]
        self.assertLess(errs[1],errs[0]/3)
        self.assertLess(errs[2],errs[1]/3)
        self.assertLess(errs[-1],.0005)


if __name__=="__main__":
    unittest.main()
