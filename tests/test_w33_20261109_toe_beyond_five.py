"""Tests five independent W33 physics continuations and negative controls."""
import json,math,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_point_line_30_zero_modes as flat
import w33_20261109_phase_fisher_information as phase
import w33_20261109_onoff_bell_robust_envelope as bell
import w33_20261109_oracle_ppt_optical_power as power

FILES=["w33_20261109_point_line_30_zero_modes",
       "w33_20261109_phase_fisher_information",
       "w33_20261109_oracle_ppt_optical_power",
       "w33_20261109_onoff_bell_robust_envelope",
       "w33_20261109_des_y6_repeat_public_audit"]
def get(name):return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))

class TestFiveTOEFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.R={n:get(n) for n in FILES}

    def test_all_outputs_are_produced(self):
        self.assertEqual(len(self.R),5)
        self.assertTrue(all(d["status"].startswith("PASS") for d in self.R.values()))

    def test_cross_incidence_orbit_exact(self):
        r=self.R[FILES[0]]
        self.assertEqual([o["size"] for o in r["incidence_point_line_pair_orbits"]],[160,1440])
        self.assertEqual(r["point_line_intertwiner_dimension"],2)
        self.assertEqual(r["direct_sum_80_dim_commutant_dimension"],10)

    def test_native_dark_tight_frame_exact_and_detuning_response(self):
        r=self.R[FILES[0]]
        frames=r["explicit_15D_dark_tight_frames"]
        self.assertEqual(len(frames),2)
        for f in frames:
            self.assertEqual(f["projector_rank"],15)
            self.assertEqual(f["unit_norm_40vector_tight_frame_rank"],15)
            self.assertEqual(f["frame_constant"],"8/3")
            self.assertEqual(f["pair_inner_product_if_collinear"],"-1/3")
            self.assertEqual(f["pair_inner_product_if_noncollinear"],"1/9")
        leak=r["one_detuned_edge_dark_state_test"]
        self.assertAlmostEqual(leak["exact_short_time_line_leakage_t2_coefficient"],
                               leak["independent_matrix_leakage_t2_coefficient"],places=12)
        self.assertGreater(leak["exact_short_time_line_leakage_t2_coefficient"],0)

    def test_symmetry_forced_chiral_flat_band(self):
        r=self.R[FILES[0]]
        self.assertEqual(r["native_B_rank"],25)
        self.assertEqual(r["chiral_H0_spectrum"]["zero"],30)
        self.assertEqual(r["B_singular_spectrum"],{"4":1,"sqrt6":24,"0":15})
        for x in r["six_invariant_coupling_controls"]:
            self.assertGreaterEqual(x["zero_eigenvalue_multiplicity"],30)
            self.assertEqual(x["point_chiral_kernel_dimension"],x["line_chiral_kernel_dimension"])

    def test_forest_dense_phase_info_all_ten(self):
        r=self.R[FILES[1]]
        self.assertEqual(len(r["per_setting"]),10)
        self.assertEqual(r["contexts_with_dense_better_than_forest"],10)
        for x in r["per_setting"]:
            self.assertGreater(x["forest_trace_variance_over_dense"],1)
            self.assertGreater(x["forest"]["local_Fisher_smallest_eigenvalue_per_total_launch"],0)
            self.assertGreater(x["dense"]["local_Fisher_smallest_eigenvalue_per_total_launch"],0)

    def test_phase_tree_computation_from_new_seed(self):
        from w33_20261109_full_povm_calibration_bound import make_model
        from w33_20261109_phase25_structured_calibration import forest
        K,_,_,_=make_model()
        roots,tree=forest(K[2])
        self.assertEqual(len(roots),3)
        x=phase.fi_per_launch(K[2],np.linspace(-.04,.08,9),tree,roots)
        self.assertEqual(x["phase_parameter_count"],6)

    def test_oracle_benchmark_is_not_certification(self):
        r=self.R[FILES[2]]
        self.assertAlmostEqual(r["true_CCN_norm_separability_excess"],.003058794098,places=9)
        self.assertGreater(r["confidence_calibration"]["phase_only_1e10_rigorous_radius_over_required"],10)
        self.assertFalse(r["confidence_calibration"]["calibration_sufficient_for_CCNR_at_1e10_trials_each"])
        self.assertEqual(len(r["optical_architecture_sample_budgets"]),12)

    def test_oracle_12_context_advantage(self):
        r=self.R[FILES[2]]["optical_architecture_sample_budgets"]
        ideal={x["architecture"]:x for x in r if x["scenario"]=="ideal"}
        n=lambda name:ideal[name]["optimistic_gaussian_known_witness_95pct_size_95pct_power_launched_photon_budget"]
        self.assertLess(n("matched_12_product"),n("generic_9mode"))
        self.assertLess(n("matched_12_product"),n("permutation_Fourier"))

    def test_bell_robust_pessimism(self):
        r=self.R[FILES[3]]
        self.assertEqual(r["fixed_settings_corner_count"],16)
        self.assertGreater(r["baseline_optimized_nominal_CHSH"],2)
        self.assertLess(r["worst_fixed_settings"]["fixed_displacement_CHSH_oriented"],2)
        self.assertLess(r["independent_pessimistic_reoptimized_device"]["CHSH"],2)
        self.assertGreater(r["nominal_95pct_power_95pct_size_sufficient_Hoeffding_trial_budget_under_perfect_IID_source_model"],500000)
        self.assertIsNone(r["worst_corner_95pct_power_95pct_size_sufficient_Hoeffding_trial_budget"])

    def test_Bell_parameter_specific_corner(self):
        r=self.R[FILES[3]]
        worst=r["worst_fixed_settings"]
        self.assertAlmostEqual(worst["eta"],.85)
        self.assertAlmostEqual(worst["gamma"],.91)
        self.assertAlmostEqual(worst["source_survival"],.98)

    def test_DES_public_data_readiness_is_still_false(self):
        r=self.R[FILES[4]]
        self.assertFalse(r["frozen_S9_scored"])
        self.assertFalse(r["official_unblinded_validated_full_file_download"])
        self.assertEqual(r["S9_frozen"],"2026-11-08")
        assert len(r["tested_FITS_candidate_first_cards"])>=1
        self.assertEqual(next(iter(r["tested_FITS_candidate_first_cards"].values()))["status_code"],404)

    def test_spectral_anomaly_scope_is_finite(self):
        r=self.R[FILES[0]]
        self.assertIn("full group",r["scope"].lower())
        self.assertIn("linear",r["exact_theorem"].lower())
        self.assertNotIn("proved TOE",r["status"])

if __name__=="__main__":unittest.main()
