"""Regression: five W33 Q8 experimental/TOE falsifiers plus a calibrated-POVM repair."""
import json,sys,unittest
from pathlib import Path
from fractions import Fraction
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_q8_ten_context_optimize as opt
import w33_20261109_q8_full_povm_selfnormalize as povm
import w33_20261109_boundary_chirality_anomalies as chiral
import w33_20261109_des_y6_s9_fits_contract as des

FILES=["w33_20261109_q8_ten_context_optimize",
       "w33_20261109_q8_ccnr_shot_calibration",
       "w33_20261109_q8_optical_loss_povm",
       "w33_20261109_q8_full_povm_selfnormalize",
       "w33_20261109_boundary_chirality_anomalies",
       "w33_20261109_des_y6_s9_fits_contract"]
def freeze(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))

class TestTOEFiveFrontContinuation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f={name:freeze(name) for name in FILES}

    def test_10setting_condition_and_full_rank(self):
        x=self.f[FILES[0]]
        self.assertEqual(x["settings"],10)
        self.assertEqual(x["rank"],80)
        self.assertLess(x["refined_condition"],10)
        self.assertLess(x["refined_condition"],x["baseline_condition"]*.35)
        self.assertLess(x["max_mixed_reconstruction_error"],5e-12)

    def test_optimized_unitary_rebuilds_exactly(self):
        import hashlib
        x,(Bell,U,V,op)=opt.main(return_components=True)
        self.assertEqual(x["refined_2bases_sha256"],self.f[FILES[0]]["refined_2bases_sha256"])
        self.assertLess(max(abs(U.conj().T@U-np.eye(9)).flatten()),1e-12)
        self.assertLess(max(abs(V.conj().T@V-np.eye(9)).flatten()),1e-12)

    def test_robust_ccnr_finite_shot_scope(self):
        x=self.f[FILES[1]]
        self.assertIn("refined_ten_settings",x)
        for k in ("10","11","12"):
            self.assertEqual(len(x["tests"][k]),2)
            for sample in x["tests"][k]:
                self.assertEqual(sample["frame_rank"],80)
                self.assertGreater(sample["true_realignment_norm"],1)
                self.assertFalse(sample["sample_count_sweep"][0]["LP_certifies_entangled_on_expected_frequencies"])
                self.assertTrue(sample["sample_count_sweep"][-1]["LP_certifies_entangled_on_expected_frequencies"])
        self.assertLess(x["refined_ten_settings"][0]["condition"],10)

    def test_uncalibrated_loss_creates_false_ccnr_signals(self):
        data=self.f[FILES[2]]["loss_noise_controls"]
        self.assertEqual(data[0]["separable_false_positive_count"],0)
        for row in data[1:]:
            self.assertEqual(row["separable_false_positive_count"],12)
            self.assertEqual(row["total_separable_controls"],12)
        self.assertEqual(self.f[FILES[2]]["max_rail_coupler_exposure"],15)

    def test_calibrated_POVM_repairs_false_positives(self):
        data=self.f[FILES[3]]
        self.assertTrue(data["all_product_controls_correct_after_full_POVM_calibration"])
        self.assertEqual(len(data["tested_loss_models"]),5)
        for row in data["tested_loss_models"]:
            self.assertEqual(row["corrected_false_positives"],0)
            self.assertLess(row["max_corrected_rho_error"],1e-10)
            self.assertEqual(row["tested_product_states"],12)

    def test_rectangular_index_not_predicted_by_closed_W33(self):
        data=self.f[FILES[4]]
        r=data["rational_rank"]
        self.assertEqual((r["closed_index"],r["deleted_index"]),(0,-1))
        self.assertEqual((r["closed_plus_zero_modes"],r["closed_minus_zero_modes"]),(15,15))
        self.assertEqual((r["deleted_plus_zero_modes"],r["deleted_minus_zero_modes"]),(14,15))
        self.assertEqual(len(r["all_single_point_deleted_boundary_ranks"]),40)
        self.assertTrue(all(v==25 for v in r["all_single_point_deleted_boundary_ranks"]))
        self.assertEqual(len(data["complex_disorder"]["independent_edge_holonomy_controls"]),8)

    def test_exact_standard_model_anomaly_gate_is_supplied_not_derived(self):
        r=chiral.anomaly_gate()
        for k in ("SU3_sq_U1","SU2_sq_U1","U1_cubed","gravitational_U1"):
            self.assertEqual(Fraction(r[k]),Fraction(0))
        self.assertEqual(r["SU2_left_doublet_count"],4)
        self.assertTrue(r["Witten_global_SU2_even_doublets"])

    def test_fits_gate_and_three_negative_controls(self):
        x=self.f[FILES[5]]
        self.assertTrue(x["synthetic_valid_contract"]["valid"])
        self.assertFalse(x["missing_unblinding_rejected"]["valid"])
        self.assertFalse(x["bad_covariance_rejected"]["valid"])
        self.assertFalse(x["synthetic_as_real_rejected"]["valid"])
        self.assertFalse(x["actual_DES_Y6_FITS_access"])
        self.assertFalse(x["S9_scored"])
        self.assertEqual(x["synthetic_valid_contract"]["cut_size"],6)

    def test_all_producer_data_present(self):
        for name in FILES:
            self.assertTrue(self.f[name]["status"].startswith("PASS_"))

if __name__=="__main__":
    unittest.main()
