"""Independent regressions for five W33 deep research fronts plus controls."""
import json,math,sys,hashlib,unittest
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_q8_full_povm_uncertainty_bound as robust
import w33_20261109_q8_structured_fourier_readout as phase
import w33_20261109_q8_perm_fourier_phases_27 as structured
import w33_20261109_native_twist_chern_no_go as chern
import w33_20261109_photon_causal_nonlocality_gate as photon
from w33_20261109_q8_ten_context_tomography import select,projection_design

NAMES=(
 "w33_20261109_q8_full_povm_uncertainty_bound",
 "w33_20261109_q8_structured_fourier_readout",
 "w33_20261109_q8_perm_fourier_phases_27",
 "w33_20261109_native_twist_chern_no_go",
 "w33_20261109_photon_causal_nonlocality_gate",
 "w33_20261109_des_y6_public_provenance_probe"
)
def frozen(k):
    return json.loads((ROOT/"data"/(k+".json")).read_text(encoding="utf8"))

class TestW33DeepFive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d={name:frozen(name) for name in NAMES}

    def test_frozen_artifacts_exist_and_honest_scopes(self):
        self.assertEqual(len(self.d),6)
        self.assertTrue(self.d[NAMES[0]]["status"].startswith("PASS"))
        self.assertFalse(self.d[NAMES[-1]]["S9_model_likelihood_scored"])
        self.assertFalse(self.d[NAMES[-1]]["actual_unblinded_cosmic_shear_FITS_downloaded_and_parsed"])

    def test_realignment_full_POVM_calibration_bound(self):
        x=self.d[NAMES[0]]
        self.assertGreater(x["ideal_CCNR"],1)
        self.assertGreater(x["joint_error_example"]["ccnr_conservative_lower"],1)
        self.assertTrue(x["joint_error_example"]["certified"])
        self.assertGreater(x["selfnormalizing_augmented_sigma_min"],.1)
        self.assertGreater(x["maximum_effect_Frobenius_error_for_expected_values_zero_statistical_noise"],1e-6)
        self.assertLess(x["maximum_effect_Frobenius_error_for_expected_values_zero_statistical_noise"],1e-5)
        self.assertGreater(x["prospective_95pct_independent_accepted_shots_per_setting_for_zero_calibration_error"],10**10)

    def test_adversarial_calibration_stress_and_separable_control(self):
        x=self.d[NAMES[0]]
        for key,items in x["adversarial_full_complex_POVM_phase_stress"].items():
            self.assertEqual(len(items),4)
            for row in items:
                if row["conservative"]["bound_is_finite"]:
                    self.assertGreaterEqual(row["true_ccnr"]+1e-10,row["conservative"]["ccnr_conservative_lower"])
                    self.assertLessEqual(row["actual_rho_error_Frobenius"],
                                         row["conservative"]["state_coefficients_error_upper"]+1e-10)
        self.assertTrue(all(not item["conservative"]["certified"]
                            for item in x["adversarial_full_complex_POVM_phase_stress"]["pure_separable_control"]))

    def test_phase_only_masked_fourier_has_rank_obstruction(self):
        _,(B,_,_,ops,_)=select(return_components=True)
        rng=np.random.default_rng(20261109336)
        for mode in ("asymmetric","symmetric"):
            for k in range(12):
                a=rng.uniform(-3,3,9)
                b=rng.uniform(-3,3,9)
                X=projection_design(phase.make(a,0,mode),ops)
                Y=projection_design(phase.make(b,1,mode),ops)
                self.assertLessEqual(np.linalg.matrix_rank(X[:,64:],tol=1e-9),4)
                self.assertLessEqual(np.linalg.matrix_rank(Y[:,64:],tol=1e-9),4)
                self.assertLessEqual(np.linalg.matrix_rank(np.vstack([X[:,64:],Y[:,64:]]),tol=1e-9),8)
        self.assertTrue(all(not f["full_rank_found"] for f in self.d[NAMES[1]]["families"]))

    def test_phase_and_fixed_permutations_restore_full_rank(self):
        p=self.d[NAMES[2]]
        self.assertEqual(p["rank_after_extra"],80)
        self.assertEqual(p["selected_total_fixed_adjacent_routing_inversions"],10)
        self.assertEqual(p["two_mode_givens_per_extra_basis_upper"],27)
        self.assertLess(p["post_phase_optimization_condition_number"],18)
        self.assertLess(p["max_tested_reconstruction_error"],5e-12)
        _,(B,_,_,op,_)=select(return_components=True)
        a,b=p["programmed_diagonal_phase_masks"]
        U=structured.make(np.array(a),p["first_permutation"],0)
        V=structured.make(np.array(b),p["second_permutation"],1)
        m=np.vstack([projection_design(B,op),projection_design(U,op),projection_design(V,op)])
        self.assertEqual(np.linalg.matrix_rank(m,tol=1e-9),80)
        self.assertEqual(hashlib.sha256(np.stack([U,V]).tobytes()).hexdigest(),
                         p["matrix_digest_sha256"])
        self.assertAlmostEqual(np.linalg.cond(m),p["post_phase_optimization_condition_number"],places=8)

    def test_exact_AIII_occupied_frame_and_numeric_chern(self):
        p=self.d[NAMES[3]]
        self.assertTrue(p["phase_twists_fixed_hopping_modulus"])
        self.assertTrue(p["exact_chiral_anticommutator_zero_for_all_twists"])
        self.assertGreater(p["sampled_min_gap"],p["analytical_gap_lower"]-1e-10)
        self.assertLess(abs(p["sampled_first_chern_number"]),1e-10)
        self.assertLess(p["berry_curvature_max_plaquette_abs"],1e-10)

    def test_chsh_internal_not_spacelike(self):
        p=self.d[NAMES[4]]
        ch=p["internal_degree_of_freedom"]
        self.assertAlmostEqual(ch["CHSH_abs"],2*np.sqrt(2),places=12)
        self.assertFalse(ch["spatial_nonlocality_certified"])
        self.assertEqual(p["passive_spatial_detection"]["single_photon_two_party_coincidence_probability"],0)
        self.assertEqual(p["passive_spatial_detection"]["random_optical_wavefunction_controls"],16)

    def test_measurement_gauge_makes_entangled_and_product_indistinguishable(self):
        p=self.d[NAMES[4]]["untrusted_POVM_ambiguity"]
        self.assertLess(p["max_indistinguishability_error"],1e-12)
        self.assertGreater(p["entangled_schmidt_coefficients"][1],.7)
        self.assertLess(p["separable_schmidt_coefficients"][1],1e-12)

    def test_DES_Y6_fail_closed_current_HTTP_probe(self):
        p=self.d[NAMES[5]]
        R=p["public_endpoint_checks"]
        self.assertEqual(R["DES_Y6_release"]["HTTP_status"],200)
        self.assertEqual(R["DES_Y6_old_unblinded_FITS"]["HTTP_status"],404)
        self.assertEqual(R["DES_Y6_old_pipeline_notebook"]["HTTP_status"],404)
        self.assertFalse(p["S9_model_likelihood_scored"])
        self.assertFalse(p["matched_full_covariance_downloaded_and_validated"])

    def test_full_report_never_relabels_synthetic_as_physical(self):
        p=self.d[NAMES[0]]
        self.assertIn("synthetic",p["scope"].lower())
        q=self.d[NAMES[2]]
        self.assertIn("exclude routing",q["strict_hardware_scope"].lower())

if __name__=="__main__":
    unittest.main()
