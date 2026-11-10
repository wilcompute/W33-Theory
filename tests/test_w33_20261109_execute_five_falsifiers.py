"""Regression for all five executed W33 TOE continuation fronts.

All frozen data are synthetic/finite numerical except direct public HTTP
status. No real photon or DES observation was manufactured or scored.
"""
import json,math,sys,unittest
from pathlib import Path
from fractions import Fraction as F
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_povm_81probe_calibration as cal
import w33_20261109_3d_wilson_a3_chirality as d3
import w33_20261109_s9_frozen_likelihood_harness as s9
import w33_20261109_single_photon_event_ready_network as bell

FILES=["w33_20261109_povm_81probe_calibration",
       "w33_20261109_optical_fisher_competition",
       "w33_20261109_3d_wilson_a3_chirality",
       "w33_20261109_s9_frozen_likelihood_harness",
       "w33_20261109_single_photon_event_ready_network"]
def frozen(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))

class TestW33FiveNew(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r={name:frozen(name) for name in FILES}

    def test_all_five_frozen_sources(self):
        self.assertEqual(len(self.r),5)
        for name,x in self.r.items():
            self.assertTrue(x["status"].startswith("PASS"),name)

    def test_povm_81_probe_completeness_and_exact_recovery(self):
        x=self.r[FILES[0]]
        self.assertEqual(x["independent_probe_states"],81)
        self.assertEqual(x["registered_click_outcomes_per_context"],10)
        self.assertLess(x["exact_expected_probability_reconstruction_operator_error"],1e-12)
        states,plus,iphi=cal.probes()
        self.assertEqual(states.shape,(81,9))
        self.assertEqual(len(plus),36);self.assertEqual(len(iphi),36)
        self.assertLess(np.max(abs(np.linalg.norm(states,axis=1)-1)),1e-12)

    def test_calibration_confidence_finite_sample_controls(self):
        x=self.r[FILES[0]]
        self.assertEqual(len(x["finite_calibration_trials"]),3)
        for n,case in x["finite_calibration_trials"].items():
            self.assertTrue(case["true_error_below_conservative_bound"])
            self.assertLessEqual(case["maximum_simulated_operator_norm_effect_error"],
                                 case["certified_each_POVM_effect_operator_norm_radius"])
            self.assertEqual(case["total_trusted_calibration_pulses"],int(n)*810)
        self.assertGreater(x["necessary_per_probe_calibration_pulses_for_this_worst_case_Hoeffding_cert_even_with_infinite_physics_shots"],10**11)

    def test_four_architectures_same_total_shots(self):
        x=self.r[FILES[1]]
        for label in ("ideal","moderate","harsh"):
            data=x["model_outputs"][label]
            self.assertEqual(len(data),4)
            self.assertEqual(data["generic_9mode"]["contexts"],10)
            self.assertEqual(data["matched_12_product"]["contexts"],12)
            for case in data.values():
                self.assertGreater(case["per_launched_photon_Fisher_smallest_eigenvalue"],0)
        crb=x["model_outputs"]["moderate"]
        self.assertLess(crb["matched_12_product"]["per_launched_photon_CCNR_dual_Cramer_Rao_variance_coefficient"],
                        crb["generic_9mode"]["per_launched_photon_CCNR_dual_Cramer_Rao_variance_coefficient"])

    def test_architecture_pessimistic_loss_does_not_improve_info(self):
        x=self.r[FILES[1]]["model_outputs"]
        for model in x["ideal"]:
            self.assertGreaterEqual(x["harsh"][model]["per_launched_photon_inverse_Fisher_trace"],
                                    x["ideal"][model]["per_launched_photon_inverse_Fisher_trace"]-1e-9)

    def test_3d_AIII_exact_sector_multiplicities(self):
        x=self.r[FILES[2]]
        self.assertEqual([v["exact_total_3D_AIII_degree"] for v in x["3D_lattice_Wilson_Dirac_models"]],
                         [0,40,-80,40,39,15,25,-77])
        self.assertLess(x["point_gauge_rephasing_spectrum_error"],1e-12)
        for model in x["3D_lattice_Wilson_Dirac_models"]:
            self.assertGreater(F(model["exact_global_gap"]),0)
            self.assertEqual(sum(q["multiplicity_weighted_degree"] for q in model["sector_contributions"]),
                             model["exact_total_3D_AIII_degree"])

    def test_3d_independent_Brillouin_integration(self):
        x=self.r[FILES[2]]
        for row in x["independently_integrated_unit_sector_degrees"]:
            self.assertLess(row["abs_error"],.06)
        self.assertEqual(d3.degree(F("2")),1)
        self.assertEqual(d3.degree(F("0")),-2)
        self.assertEqual(d3.spectrum_model("2.9",".4")["exact_total_3D_AIII_degree"],15)
        doublers=x["naive_8_doubler_zero_net_chirality"]
        self.assertEqual(sum(j["multiplicity"]*j["naive_local_chirality"] for j in doublers),0)

    def test_synthetic_DES_likelihood_replay_and_fail_closed(self):
        x=self.r[FILES[3]]
        self.assertFalse(x["S9_real_survey_chi2_scored"])
        self.assertEqual(x["frozen_S9_date"],"2026-11-08")
        self.assertEqual(x["synthetic_source"]["kept_bins"],6)
        self.assertEqual(len(x["negative_controls_rejected"]),3)
        self.assertLess(x["synthetic_bin_covariance_joint_permutation_invariance_error"],1e-9)
        self.assertEqual(x["live_endpoint_get"]["former_unblinded_FITS"]["status_code"],404)

    def test_covariance_identifier_negative(self):
        ids,ang,mask,C,A,P,models,data=s9.make_synthetic()
        keep=np.where(mask)[0]
        labels=[ids[j] for j in keep]
        self.assertTrue(s9.validate_ids(labels,labels,labels))
        with self.assertRaises(ValueError):
            s9.validate_ids(labels,list(reversed(labels)),labels)
        chi,beta=s9.profile_chi2(data[keep],models["synthetic_CPL"][keep],
                                 C[np.ix_(keep,keep)],A[keep],P)
        self.assertTrue(math.isfinite(chi));self.assertEqual(len(beta),2)

    def test_single_photon_causal_and_reference_resources(self):
        x=self.r[FILES[4]]
        self.assertTrue(x["two_party_spacelike_proposal"]["all_times_are_design_targets_not_measured"])
        self.assertGreater(x["two_party_spacelike_proposal"]["minimum_cross_site_spacelike_margin_ns"],200)
        self.assertEqual(x["additional_phase_reference_resource_ledger"]["total_reference_mean_photons_per_trial"],20000)
        self.assertTrue(x["one_realized_synthetic_IID_CHSH_50k"]["synthetic_rejects_CHSH_local_bound"])
        self.assertFalse(x["no_phase_reference_negative_control"]["synthetic_rejects_CHSH_local_bound"])
        self.assertAlmostEqual(x["ideal_phase_coherent_signal_survival_threshold"],1/math.sqrt(2),places=12)

    def test_no_source_loss_efficiency_confusion(self):
        x=self.r[FILES[4]]["expected_signal_eta_phase_grid"]
        self.assertTrue(any(z["quantum_CHSH_above_local_bound"] for z in x))
        self.assertTrue(any(not z["quantum_CHSH_above_local_bound"] for z in x))
        self.assertAlmostEqual(bell.chsh_expected(.95,0),0,places=13)
        self.assertAlmostEqual(bell.chsh_expected(1,1),2*math.sqrt(2),places=13)

if __name__=="__main__":unittest.main()
