"""Seven executed W33 research fronts: exact gauge, photonic state prep, full
multinomial calibration, shot allocation, DES gate, Bell thresholds.
"""
import json,math,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_flux_dark_mode_fragility as flux
import w33_20261109_dark_frame_photonic_protocol as prep
import w33_20261109_joint_phase_mle as mle
import w33_20261109_81_wilson_flux_decoder as wilson
import w33_20261109_onoff_hardware_threshold as bell
import w33_20261109_s9_frozen_manifest_attack as des

FILES=["w33_20261109_flux_dark_mode_fragility",
       "w33_20261109_dark_frame_photonic_protocol",
       "w33_20261109_joint_phase_mle",
       "w33_20261109_81_wilson_flux_decoder",
       "w33_20261109_onoff_hardware_threshold",
       "w33_20261109_s9_frozen_manifest_attack",
       "w33_20261109_four_readout_shot_allocation"]
def frozen(n):
    return json.loads((ROOT/"data"/(n+".json")).read_text(encoding="utf8"))

class W33Seven(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.x={n:frozen(n) for n in FILES}

    def test_seven_frozen_outputs(self):
        self.assertEqual(len(self.x),7)
        for n,x in self.x.items():self.assertTrue(x["status"].startswith("PASS"),n)

    def test_flux_graph_euler_and_girth(self):
        x=self.x[FILES[0]]
        self.assertEqual((x["vertices"],x["edges"],x["cycle_space_dimension_E_minus_V_plus_1"]),(80,160,81))
        self.assertEqual(x["shortest_incidence_cycle_edges"],8)
        self.assertLess(x["pure_gauge_max_cycle_flux_abs"],1e-11)
        self.assertLess(x["pure_gauge_spectrum_max_error"],1e-11)

    def test_single_flux_breaks_only_one_pair(self):
        x=self.x[FILES[0]]
        self.assertEqual(x["pure_gauge_dark_mode_count"],30)
        self.assertEqual(x["one_edge_rank"],26)
        self.assertEqual(x["one_edge_chiral_zero_modes"],28)
        self.assertGreater(x["single_edge_number_nonzero_independent_Wilson_holonomies"],0)

    def test_k_flux_exact_rank_bound(self):
        x=self.x[FILES[0]]
        for k in x["independent_disjoint_edge_detuning_controls"]:
            self.assertLessEqual(k["matrix_rank"],k["rigorous_rank_upper_bound"])
            self.assertGreaterEqual(k["dark_zero_modes"],k["rigorous_zero_mode_lower_bound"])
        self.assertEqual(x["generic_nonzero_flux_rank"],40)

    def test_wilson_tree_chord_decomposition(self):
        x=self.x[FILES[3]]
        self.assertEqual(x["vertex_edge_boundary_rank"],79)
        self.assertEqual(x["cycle_rank"],81)
        self.assertEqual(x["generic_flux_independent_nonzero_chords"],81)
        self.assertLess(x["canonical_reconstructed_twisted_incidence_max_error"],1e-11)
        self.assertLess(x["under_vertex_rephasing_canonical_chord_residual_max_error"],1e-11)

    def test_wilson_decoder_independent(self):
        B,edges,G=flux.build()
        rng=np.random.default_rng(4561)
        alpha=rng.uniform(-1,1,40)
        beta=rng.uniform(-1,1,40)
        pure=np.where(B>0,alpha[:,None]-beta[None,:],0)
        potentials,residual,tree=wilson.decode(pure,G)
        self.assertEqual(tree.number_of_edges(),79)
        self.assertLess(max(abs(residual[B>0])),1e-11)

    def test_dark_photon_intensities_and_six_layers(self):
        x=self.x[FILES[1]]
        p=x["target_intensities"]
        self.assertEqual([p[k]["count"] for k in ("central","12_collinear","27_noncollinear")],[1,12,27])
        self.assertEqual(x["balanced_binary_split_layers"],[1,2,4,8,16,8])
        self.assertEqual(x["two_mode_tunable_splits"],39)
        self.assertEqual(x["required_pi_phase_corrections"],12)
        self.assertLess(x["max_state_preparation_amplitude_error"],1e-12)

    def test_dark_photon_exact_leakage(self):
        x=self.x[FILES[1]]
        q=x["incident_edge_phase_detuning"]
        self.assertAlmostEqual(q["leading_line_click_probability_coefficient"],
                               1.5*math.sin(q["theta"]/2)**2,places=12)
        self.assertLess(max(abs(j["relative_t4_correction"]) for j in q["finite_time_controls"]),.04)
        z=x["differential_preparation_loss"]
        self.assertAlmostEqual(z["exact_t2_raw_line_leakage_coefficient"],
                               1.5*(1-math.sqrt(z["central_port_intensity_survival"]))**2,places=12)

    def test_phase_mle_counts_and_empirical_behavior(self):
        x=self.x[FILES[2]]
        self.assertEqual(x["contexts_evaluated"],[0,2,8])
        for row in x["designs"]:
            self.assertEqual(row["two_designs"]["forest_phase_only"]["replications"],12)
            self.assertEqual(row["two_designs"]["all_observable_phase_pairs"]["replications"],12)
            self.assertLess(row["two_designs"]["all_observable_phase_pairs"]["local_CR_trace_per_launched_trial"],
                            row["two_designs"]["forest_phase_only"]["local_CR_trace_per_launched_trial"])
            self.assertGreater(row["two_designs"]["all_observable_phase_pairs"]["phase_probe_configuration_count"],
                                row["two_designs"]["forest_phase_only"]["phase_probe_configuration_count"])

    def test_corrected_prior_Fisher_matches_independent_multinomial_jacobian(self):
        from w33_20261109_full_povm_calibration_bound import make_model
        from w33_20261109_phase25_structured_calibration import forest,probes
        from w33_20261109_phase_fisher_information import fi_per_launch
        K,_,_,_=make_model()
        for context in (0,2,8):
            roots,edges=forest(K[context])
            free=[i for i in range(9) if i not in roots]
            theta=np.linspace(-.055,.055,9)
            S=probes(edges)
            F=mle.fisher(K[context],S,theta,free)
            prior=fi_per_launch(K[context],theta,edges,roots)
            self.assertAlmostEqual(np.trace(np.linalg.inv(F)),
                      prior["phase_trace_Cramer_Rao_per_total_launch"],places=6)

    def test_multinomial_phase_gradient_independent_finite_difference(self):
        from w33_20261109_full_povm_calibration_bound import make_model
        from w33_20261109_phase25_structured_calibration import forest,probes
        K,_,_,_=make_model()
        roots,edges=forest(K[0])
        S=probes(edges)[9:]
        theta=np.linspace(-.07,.07,9)
        p,J=mle.probs_jac(K[0],S,theta)
        h=1e-6
        zz=np.zeros(9);zz[2]=h
        pp,_=mle.probs_jac(K[0],S,theta+zz)
        pm,_=mle.probs_jac(K[0],S,theta-zz)
        self.assertLess(np.max(abs((pp-pm)/(2*h)-J[:,:,2])),2e-8)

    def test_Bell_fixed_nominal_source_threshold(self):
        x=self.x[FILES[4]]
        self.assertGreater(x["fixed_nominal_analyzer_critical_global_source_survival"],.99)
        self.assertLess(x["fixed_nominal_analyzer_critical_global_source_survival"],1)
        self.assertAlmostEqual(x["critical_detector_efficiency_for_fixed_analyzer_optimized_at_94pct"],.876258145775,places=8)
        self.assertAlmostEqual(x["fixed_94pct_analyzer_CHSH_at_critical_efficiency"],2,places=9)

    def test_Bell_efficiency_scan_correct_direction(self):
        x=self.x[FILES[4]]["multi_seed_reoptimized_efficiency_scan"]
        a=[x[str(y)]["optimized_abs_CHSH"] for y in (.85,.88,.90,.92,.94,.96)]
        self.assertTrue(all(a[j]<a[j+1] for j in range(5)))
        self.assertLess(a[0],2);self.assertGreater(a[-1],2)

    def test_S9_frozen_and_fake_manifests_rejected(self):
        x=self.x[FILES[5]]
        self.assertFalse(x["real_S9_Delta_chi2_scored"])
        self.assertFalse(x["independent_publisher_SHA256_and_full_FITS"])
        self.assertEqual(x["frozen_date"],"2026-11-08")
        self.assertEqual(len(x["deliberately_invalid_evidence_manifests_rejected"]),5)
        self.assertTrue(all(v for v in x["deliberately_invalid_evidence_manifests_rejected"].values()))
        self.assertEqual(x["frozen_claim_sha256"],
                         frozen("w33_20261109_des_y6_repeat_public_audit")["S9_claim_sha256"])

    def test_S9_rejects_tampering_of_angular_cuts(self):
        x=self.x[FILES[5]]
        claim=x["frozen_claim_sha256"]
        failures=des.validate({"xi_plus_cut_arcmin":11,
                    "xi_minus_cut_arcmin":60,"cuts_are_strict_gt":True},claim)
        self.assertTrue(any("angular scale cuts" in v for v in failures))

    def test_optical_four_architectures_oracle_allocation(self):
        x=self.x[FILES[6]]["per_launched_source_photon_optimization"]
        for scenario in ("ideal","moderate"):
            self.assertEqual(len(x[scenario]),4)
            for row in x[scenario].values():
                self.assertTrue(row["optimization_success"])
                self.assertAlmostEqual(sum(row["shot_fractions_by_setting"]),1,places=9)
                self.assertTrue(all(v>=.01-1e-8 for v in row["shot_fractions_by_setting"]))
                self.assertGreater(row["fractional_variance_reduction"],.35)
                self.assertLess(row["fractional_variance_reduction"],.65)

    def test_optical_fixed_source_best_model_stays_twelve(self):
        x=self.x[FILES[6]]["per_launched_source_photon_optimization"]
        for scen in x:
            d=x[scen]
            z=d["matched_12_product"]["optimized_per_launch_CCNR_CRLB"]
            self.assertTrue(all(z<v["optimized_per_launch_CCNR_CRLB"]
                                for k,v in d.items() if k!="matched_12_product"))

if __name__=="__main__":unittest.main()
