"""Regression of five Nov-9 W33/Q8 fronts and extra 10/11 setting designs."""
import json,sys,unittest
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_q8_ten_context_tomography as ten
import w33_20261109_q8_horodecki_ccnr_exact as ccnr
import w33_20261109_q8_rational_detector_dual as dual
import w33_20261109_q8_native_dirac_optics as native
import w33_20261109_q8_11_context_tradeoff as eleven

def frozen(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))

class TestNov9FiveMore(unittest.TestCase):
    def test_optimal_projective_settings_and_reconstruction(self):
        x=ten.main()
        self.assertEqual((x["ten_setting_design_rank"],x["global_projective_minimum_settings"]),(80,10))
        self.assertEqual(x["eight_bell_design_rank"],64)
        self.assertEqual(x["nine_setting_upper_bound_rank"],72)
        self.assertFalse(x["extra_bases_are_mutually_unbiased"])
        self.assertLess(x["max_random_state_reconstruction_error"],1e-12)
        self.assertAlmostEqual(x["combined_condition_number"],29.468942303378,places=6)
        self.assertEqual(x["matrix_sha256"],frozen("w33_20261109_q8_ten_context_tomography")["matrix_sha256"])

    def test_analytic_Horodecki_CCNR_all_parameters(self):
        p=ccnr.exact_proof()
        self.assertTrue(p["realignment_trace_norm_strict_gt_1_for_every_0_lt_a_lt_1"])
        self.assertEqual(p["F_at_S0"],"a**2*(a - 1)*(3*a + 1)/4")
        out=ccnr.main()
        self.assertEqual(len(out["sampled_Horodecki_family"]),15)
        self.assertLess(out["reconstruction_max_abs_error"],1e-12)
        self.assertTrue(all(x["CCNR_from_10_measured_bases"]>1 for x in out["sampled_Horodecki_family"]))

    def test_rational_detector_dual_crossing_separable_bound(self):
        x=dual.main()
        self.assertEqual(len(x["results"]),2)
        for p in x["results"]:
            self.assertGreater(Fraction(p["strict_rational_lower_after_frame_error"]),Fraction(2,3))
            self.assertTrue(p["operator_norm_proved_at_most_one_by_rational_Gershgorin"])
            self.assertEqual(len(p["lp_dual_certificates"]),8)
            self.assertGreater(p["numeric_SDP_minimum"],p["strict_decimal_lower"])
        vals={p["state"]:p["strict_decimal_lower"] for p in x["results"]}
        self.assertAlmostEqual(vals["Tiles"],.69006394656,places=6)
        self.assertAlmostEqual(vals["Pyramids"],.69885689557,places=6)

    def test_native_incidence_Dirac_zero_chiral_index(self):
        x=native.native_dirac()
        self.assertEqual(x["incidence_rank_over_Q_exact"],25)
        self.assertEqual((x["graded_plus_zero_modes"],x["graded_minus_zero_modes"]),(15,15))
        self.assertEqual(x["zero_mode_index_plus_minus"],0)
        self.assertEqual(x["singular_square_spectrum"],{"0":15,"6":24,"16":1})
        self.assertLess(x["local_U1_pure_gauge_singular_error"],1e-12)
        self.assertGreater(x["generic_edge_phase_min_singular"],1e-6)

    def test_generic_nonbell_9mode_optical_Givens(self):
        x=native.compare_optics()
        self.assertEqual(len(x["extra_10setting_bases"]),2)
        self.assertEqual(x["sum_of_per_context_couplers_ten_if_not_shared"],216)
        for row in x["extra_10setting_bases"]:
            self.assertEqual(row["couplers"],36)
            self.assertTrue(row["adjacent_only"])
            self.assertLess(row["max_measurement_unitary_error"],1e-12)

    def test_three_way_tomographic_tradeoff(self):
        x=eleven.main()
        self.assertLess(x["ten"]["condition"],30)
        self.assertLess(x["eleven"]["condition"],10)
        self.assertAlmostEqual(x["twelve"]["condition"],2**.5,places=10)
        self.assertEqual(x["eleven"]["rank"],80)
        self.assertLess(x["eleven"]["max_reconstruction_error"],1e-12)

    def test_frozen_des_data_gate(self):
        x=frozen("w33_20261109_des_y6_s9_audit")
        self.assertFalse(x["S9_chi2_computed"])
        self.assertEqual(x["frozen_S9_date"],"2026-11-08")
        self.assertEqual(x["release_endpoint_test"]["former_unblinded_3x2pt_FITS"]["HTTP_GET_status"],404)
        self.assertTrue(x["python_theory_tools_available"]["astropy"])
        self.assertEqual(len(x["required_pipeline_artifacts"]),7)

    def test_all_frozen_producer_outputs_present(self):
        for name in ("w33_20261109_q8_ten_context_tomography",
                     "w33_20261109_q8_horodecki_ccnr_exact",
                     "w33_20261109_q8_rational_detector_dual",
                     "w33_20261109_q8_native_dirac_optics",
                     "w33_20261109_q8_11_context_tradeoff",
                     "w33_20261109_des_y6_s9_audit"):
            self.assertTrue(frozen(name)["status"])

if __name__=="__main__":
    unittest.main()
