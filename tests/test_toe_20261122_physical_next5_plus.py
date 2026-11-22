"""Five+ independent regressions for capacity, lossy optical entanglement,
three-plaquette Z2 Gauss law, third-order collisions, and detector confusion.
Run each analysis producer first; CI checks the generated certificates.
"""
from __future__ import annotations
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261122_native_capacity_input_witness as cap
import toe_20261122_loss_calibrated_witting_schmidt_witness as optics
import toe_20261122_three_plaquette_W33_gauge_null_control as gauge
import toe_20261122_witting_triple_collision_finite_shots as collision
import toe_20261122_confusion_aware_Witting_detector_pareto as noise
def read(name):
    p=ROOT/"data"/("toe_20261122_"+name+".json")
    if not p.exists():raise RuntimeError("Generate producer JSON first: "+str(p))
    return json.loads(p.read_text(encoding="utf8"))
class ResearchRegressions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=read("native_capacity_input_witness")
        cls.o=read("loss_calibrated_witting_schmidt_witness")
        cls.g=read("three_plaquette_W33_gauge_null_control")
        cls.t=read("witting_triple_collision_finite_shots")
        cls.n=read("confusion_aware_Witting_detector_pareto")
    def test_all_producer_certificates(self):
        self.assertEqual([d["status"]for d in (self.c,self.o,self.g,self.t,self.n)],["PASS"]*5)
    def test_native_five_kraus_four_to_nine_channel(self):
        self.assertEqual(self.c["native_kraus_shape"],[5,9,4])
    def test_fixed_rank_two_input_psd_and_normalized(self):
        import numpy as np
        W=np.array(self.c["fixed_rank2_factor_real"])+1j*np.array(self.c["fixed_rank2_factor_imag"])
        rho=W@W.conj().T;rho/=np.trace(rho)
        self.assertEqual(W.shape,(4,2))
        self.assertGreater(np.linalg.eigvalsh(rho).min(),-1e-10)
        self.assertEqual(self.c["input_rank"],2)
    def test_capacity_positive_at_thirty_percent(self):
        v=self.c["measured_positive_oneuse_witness_at_lambda_0p3"]
        self.assertGreater(v,.0078)
        self.assertLess(self.c["maxmixed_negative_same_noise"],-.23)
    def test_maxmixed_crossing_is_not_exact_capacity_threshold(self):
        self.assertIn("not an optimal capacity",self.c["interpretation"].lower())
    def test_lossy_Naimark_reuses_150_rotations(self):
        self.assertEqual(self.o["Naimark_active_two_mode_rotations"],150)
    def test_lossy_PPT_upper_bound_proves_witness_gap(self):
        for item in self.o["optical_loss_sweep"]:
            self.assertGreater(item["ideal_phi_same_label_probability"],
                               item["rigorous_PPT_separable_bound"])
            self.assertGreater(item["entanglement_witness_gap"],0)
    def test_at_three_percent_loss_lossless_threshold_is_invalid(self):
        q=next(x for x in self.o["optical_loss_sweep"]
               if x["power_loss_per_active_two_mode_operation"]==.03)
        self.assertLess(q["ideal_phi_same_label_probability"],.04)
        self.assertGreater(q["ideal_phi_same_label_probability"],
                           q["rigorous_PPT_separable_bound"])
    def test_exact_binomial_budget_under_two_percent_loss(self):
        q=next(x for x in self.o["optical_loss_sweep"]
               if x["power_loss_per_active_two_mode_operation"]==.02)
        self.assertEqual(q["illustrative_sufficient_iid_launch_pairs_5sigma_90percent_power"],3130)
    def test_three_plaquette_Gauss_sector_counts(self):
        self.assertEqual((self.g["matter_sites"],self.g["edges"],self.g["cycles"]),(8,10,3))
        self.assertEqual(self.g["unconstrained_dimension"],262144)
        self.assertEqual(self.g["Gauss_sector_dimension"],1024)
    def test_gauge_Wilson_tHooft_algebra_checks(self):
        self.assertEqual(self.g["Wilson_tHooft_commute_anticommute_checks"],30)
    def test_dynamic_three_plaquette_matter_creation(self):
        a=self.g["time_series"]
        self.assertAlmostEqual(a[1]["mean_matter_count"],.5006202125,places=8)
        self.assertAlmostEqual(a[2]["mean_matter_count"],1.1452397392,places=8)
    def test_abstract_graph_control_precludes_W33_specific_claim(self):
        self.assertIn("unitarily equivalent",self.g["non_W33_control"])
    def test_Witting_three_copy_uniformity_across_pure_inputs(self):
        for r in self.t["pure_state_controls"]:
            self.assertAlmostEqual(r["Witting40_pair_collision"],.04)
            self.assertAlmostEqual(r["Witting40_triple_collision"],.002)
    def test_MUB_triple_collisions_depend_on_input_state(self):
        r=self.t["pure_state_controls"]
        self.assertAlmostEqual(r[0]["fiveMUB20_triple_collision"],7/900)
        self.assertAlmostEqual(r[1]["fiveMUB20_triple_collision"],.01)
    def test_finite_shot_MUB_control(self):
        k=self.t["fiveMUB20_distinguish_input_ray_5sigma_90percent_power"]
        self.assertEqual(k["iid_triplets_N"],68886)
        self.assertGreaterEqual(k["alternative_power"],.9)
    def test_mixed_state_spectral_moment_reconstruction(self):
        r=self.t
        p2=50*r["mixed_input_pair_collision_probability"]-1
        p3=(3000*r["mixed_input_triple_collision_probability"]-1-3*p2)/2
        self.assertAlmostEqual(p2,r["mixed_input_purity"],places=10)
        self.assertAlmostEqual(p3,r["mixed_input_third_moment"],places=10)
    def test_wrong_label_confusion_preserves_calibrated_unbiased_scores(self):
        for group in self.n["noise_sweep"]:
            for row in group["layouts"]:
                self.assertAlmostEqual(row["unbiased_fidelity_score_mean"],1,places=9)
    def test_25bin_variance_tradeoff_under_known_confusion(self):
        for group in self.n["noise_sweep"]:
            a=group["layouts"]
            self.assertLess(a[3]["single_shot_fidelity_estimator_sd"],
                            a[2]["single_shot_fidelity_estimator_sd"])
            self.assertLess(a[2]["single_shot_fidelity_estimator_sd"],
                            a[1]["single_shot_fidelity_estimator_sd"])
    def test_no_real_experiment_or_TOE_claimed(self):
        self.assertIn("not device-independent",self.o["limits"].lower())
        self.assertIn("not global w33",self.g["limits"].lower())
        self.assertIn("no device-independent",self.n["boundaries"].lower())
if __name__=="__main__":unittest.main()
