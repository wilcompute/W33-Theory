"""Five 2026-11-09 TOE follow-ups: structured calibration, true loss POVMs,
Sp(4,3) commutant, actual DES Y6 access, realistic single-photon CHSH.

Published numerical data, not laboratory observations or completed TOE.
"""
import json,math,sys,unittest
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_phase25_structured_calibration as cal
import w33_20261109_four_architectures_full_loss_povm as optics
import w33_20261109_sp4_commutant_generation_obstruction as sym
import w33_20261109_onoff_single_photon_real_detector as bell

NAMES=["w33_20261109_phase25_structured_calibration",
       "w33_20261109_four_architectures_full_loss_povm",
       "w33_20261109_sp4_commutant_generation_obstruction",
       "w33_20261109_des_y6_official_link_audit",
       "w33_20261109_onoff_single_photon_real_detector"]
def result(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))

class TestNextFive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.R={n:result(n) for n in NAMES}

    def test_all_five_frozen(self):
        self.assertEqual(len(self.R),5)
        self.assertTrue(all(x["status"].startswith("PASS") for x in self.R.values()))

    def test_calibration_symplectic_support_components_and_probe_count(self):
        x=self.R[NAMES[0]]
        self.assertEqual(x["support_graph_connected_components_per_setting"],[1,1,3,1,1,3,1,1,1,1])
        self.assertEqual(x["calibration_probe_count_per_setting"],[25,25,21,25,25,21,25,25,25,25])
        self.assertEqual(x["total_calibration_probes_per_full_cycle"],242)
        self.assertLess(x["exact_expected_full_POVM_effect_reconstruction_error"],5e-12)

    def test_calibration_exact_phase_ambiguity_is_physical_gauge(self):
        from w33_20261109_full_povm_calibration_bound import make_model
        K,_,_,_=make_model()
        for base in K[:8]:
            roots,edges=cal.forest(base)
            phase=np.array([.07*j for j in range(9)])
            q=cal.probabilities(base@np.diag(np.exp(1j*phase)),cal.probes(edges))
            fitted,_,_=cal.fit_phase(q,base,roots,edges)
            truth=base@np.diag(np.exp(1j*phase))
            self.assertLess(np.linalg.norm(cal.effects(fitted)-cal.effects(truth)),3e-12)

    def test_sampled_calibration_operator_bounds(self):
        x=self.R[NAMES[0]]
        for case in x["finite_trials"].values():
            self.assertLessEqual(case["observed_max_effect_operator_error"],
                                 case["simultaneous_95pct_effect_error_bound_conditioned_on_model"]+1e-12)

    def test_model_mismatch_rejected_by_phase_invariant_basis(self):
        x=self.R[NAMES[0]]["heldout_model_falsifier"]
        self.assertTrue(x["basis_only_model_rejected_at_95pct_simultaneous_confidence"])
        self.assertGreater(x["basis_only_sampled_max_probability_deviation"],
                           x["basis_only_sampled_95pct_falsifier_threshold"])

    def test_full_POVM_rank_and_seven_noise_replicates(self):
        x=self.R[NAMES[1]]["full_POVM_results"]
        for model,values in x["moderate"].items():
            self.assertEqual(values["replicates"],7)
            self.assertGreater(values["mean_full_POVM_min_Fisher_eig"],0)
            self.assertGreater(values["mean_true_full_POVM_CCNR_CRLB"],0)
            self.assertLess(values["mean_click_survival"],1)

    def test_twelve_settings_lead_one_benchmark(self):
        x=self.R[NAMES[1]]["full_POVM_results"]
        for scenario in x:
            m=x[scenario]
            z=m["matched_12_product"]["mean_true_full_POVM_CCNR_CRLB"]
            self.assertTrue(all(z<m[k]["mean_true_full_POVM_CCNR_CRLB"]
                      for k in m if k!="matched_12_product"))

    def test_ideal_fisher_reproduces_previous_saved_designs(self):
        actual=self.R[NAMES[1]]["full_POVM_results"]["ideal"]
        prior=result("w33_20261109_optical_fisher_competition")["model_outputs"]["ideal"]
        for k in actual:
            self.assertAlmostEqual(actual[k]["mean_true_full_POVM_CCNR_CRLB"],
              prior[k]["per_launched_photon_CCNR_dual_Cramer_Rao_variance_coefficient"],places=8)

    def test_exact_symplectic_pair_orbits(self):
        x=self.R[NAMES[2]]
        self.assertEqual([r["size"] for r in x["ordered_pair_orbits"]],[40,480,1080])
        self.assertEqual(x["full_ordered_pair_count"],1600)
        self.assertEqual(x["generators_used"],40)
        self.assertEqual(x["full_Sp4F3_point_commutant_dimension"],3)

    def test_exact_symmetry_projector_dimensions(self):
        x=self.R[NAMES[2]]
        self.assertEqual([j["dimension"] for j in x["native_collinearity_adjacency_eigenspaces"]],[1,24,15])
        self.assertEqual(x["native_collinearity_graph_SRG_parameters"],[40,12,2,4])

    def test_independent_projective_group_generators(self):
        pts,lines,inc,gen=sym.action()
        self.assertEqual(len(set(gen)),40)
        self.assertEqual(len(sym.orbit((0,0),gen)),40)
        self.assertEqual(len(sym.orbit((0,1),gen)),480)

    def test_DES_FITS_absent_fail_closed(self):
        x=self.R[NAMES[3]]
        self.assertFalse(x["frozen_S9_scored"])
        self.assertFalse(x["complete_covariance_nz_model_refits_verified"])
        self.assertEqual(x["S9_frozen"],"2026-11-08")
        self.assertEqual(x["PPD_public_GitHub_repo_root_status"],200)
        self.assertEqual(x["DES_Y6_3x2pt_GitHub_repo_public_status"],404)
        historic=next(iter(x["tested_FITS_candidate_first_cards"].values()))
        self.assertEqual(historic["status_code"],404)

    def test_Bell_ideal_reproduces_2026_literature_benchmark(self):
        ideal=self.R[NAMES[4]]["optimized_cases"]["ideal"]
        self.assertAlmostEqual(ideal["CHSH"],2.6884,places=3)
        self.assertLess(ideal["signed_CHSH"],-2.6)

    def test_Bell_detectors_correct_POVM(self):
        for amp in (0,.2,.4,.9):
            E=bell.no_click(amp+.02j,.9,.001)
            eig=np.linalg.eigvalsh(E)
            self.assertGreaterEqual(min(eig),-1e-12)
            self.assertLessEqual(max(eig),1+1e-12)
        z=self.R[NAMES[4]]["optimized_cases"]["high_eff"]["displacements_real_imag"]
        S,_=bell.CHSH(z,.95,1.,1.,1e-5)
        self.assertAlmostEqual(abs(S),self.R[NAMES[4]]["optimized_cases"]["high_eff"]["CHSH"],places=11)

    def test_Bell_threshold_not_guaranteed_in_practical_case(self):
        cases=self.R[NAMES[4]]["optimized_cases"]
        self.assertGreater(cases["realistic_2026_telecom_proxy"]["CHSH"],2)
        self.assertLess(cases["realistic_2026_telecom_proxy"]["CHSH"],2.05)
        self.assertLess(cases["source_and_detector_loss"]["CHSH"],2)
        self.assertLess(cases["phase_randomized"]["CHSH"],2)

    def test_Bell_simulation_all_trial_confidence(self):
        x=self.R[NAMES[4]]
        self.assertTrue(x["one_realized_all_trial_ideal_case"]["certificate_passes_no_postselection"])
        self.assertFalse(x["phase_randomized_negative_control"]["certificate_passes_no_postselection"])
        self.assertEqual(x["one_realized_all_trial_ideal_case"]["trials"],150000)

if __name__=="__main__":unittest.main()
