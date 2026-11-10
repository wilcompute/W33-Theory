"""Independent regression: W33 81D gauge vacuum, EXACT octagon Hessian,
finite boundary index, photonic loss and calibrated 2-qutrit Schmidt test.
"""
import json,sys,math,unittest
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_full_u1_variational_vacuum as u1
import w33_20261109_exact_octagon_hessian_theorem as octa
import w33_20261109_robust_q8_schmidt_photon_counts as q8
import w33_20261109_photonic_loss_robust_null as phot
from w33_20261109_flux_dark_mode_fragility import build

NAMES=["full_u1_variational_vacuum","flux_hessian_8cycle_metric",
       "one_edge_flux_poly_curvature","exact_octagon_hessian_theorem",
       "boundary_chiral_index_falsifier",
       "robust_q8_schmidt_photon_counts","photonic_loss_robust_null"]

def read(name):
    return json.loads((ROOT/"data"/("w33_20261109_"+name+".json")).read_text())
class FiveFrontsExact(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d={n:read(n) for n in NAMES}

    def test_all_seven_reproducible_certificates(self):
        self.assertTrue(all(v["status"].startswith("PASS_") for v in self.d.values()))

    def test_exact_integer_all_edge_hessian_six_points(self):
        d=self.d["exact_octagon_hessian_theorem"]
        self.assertEqual(len(d["all_six_integer_point_full_160x160_certificates"]),6)
        self.assertEqual([x["max_absolute_integer_residual"] for x in d["all_six_integer_point_full_160x160_certificates"]],[0]*6)
        self.assertEqual(d["graph"]["edges"],160)

    def test_independent_full_hessian_integer_points_1_and_6(self):
        B,edges,C,G=octa.setup()
        self.assertEqual(C.shape,(1620,160))
        self.assertEqual(int(np.trace(G)),160*81)
        for t in (1,6):
            err,row=octa.integer_certificate(t,B,edges,G)
            self.assertEqual(err,0)
            self.assertTrue(row["integer_values_within_safe_range"])

    def test_one_edge_exact_factored_difference(self):
        d=self.d["one_edge_flux_poly_curvature"]
        t=sp.symbols("t")
        s=sp.sympify(d["P_one_pi_minus_flat_exact_factored"])
        self.assertEqual(sp.expand(s-324*t**4*(6*t+1)**22),0)
        self.assertIn("16*t",d["P_flat_factored"])

    def test_matsubara_stability_matches_full_81d_hessian(self):
        d=self.d["full_u1_variational_vacuum"]
        expected=self.d["one_edge_flux_poly_curvature"]["beta_curvature_controls"]
        k=next(z for z in expected if z["beta"]==1.)["kappa_local_single_link_Matsubara"]
        self.assertLess(abs(k-d["flat_vacuum_local_Hessian"]["flat_local_positive_Hessian_threshold_kappa"]),2e-10)
        self.assertEqual(d["chord_number"],81)

    def test_all_temperature_hessian_numeric_matches_octagon_metric(self):
        for row in self.d["flux_hessian_8cycle_metric"]["beta_direction_controls"]:
            if row["beta"]>=.3:
                self.assertLess(row["worst_operator_relative_residual"],1e-5)
                self.assertGreater(row["ratio_mean"],0)

    def test_full_u1_analytic_gradient_against_fd(self):
        ctx=u1.model()
        u1.test_grad(ctx)

    def test_flat_is_only_local_not_global_claim(self):
        d=self.d["full_u1_variational_vacuum"]
        self.assertIn("not global",d["limits"].lower())
        r=d["multistart_local_variational_results"]
        flat0=r[0]["fixed_sector_reference_objectives"]["flat"]
        self.assertLess(r[0]["best_multistart_local"]["objective"],flat0-.1)
        self.assertLess(r[2]["best_multistart_local"]["objective"],flat0-.02)
        self.assertAlmostEqual(r[-1]["best_multistart_local"]["objective"],r[-1]["fixed_sector_reference_objectives"]["flat"],places=7)

    def test_bipartite_square_no_chiral_index(self):
        d=self.d["boundary_chiral_index_falsifier"]
        s=d["original_balanced_gapped_40x40"]
        self.assertEqual(s["net_left_minus_right"],0)
        self.assertEqual(s["total_chiral_zero_modes"],0)

    def test_one_sublattice_defect_one_protected_zero(self):
        d=self.d["boundary_chiral_index_falsifier"]
        self.assertEqual(d["rectangular_41x40_index"]["net_left_minus_right"],1)
        self.assertEqual(d["rectangular_41x40_index"]["total_chiral_zero_modes"],1)
        self.assertLess(d["boundary_zero_exact_vector_residual"],1e-11)
        self.assertTrue(all(x["zero_mode_count"]==1 for x in d["phase_disorder_controls"]))

    def test_robust_q8_isotropic_closed_witness(self):
        d=self.d["robust_q8_schmidt_photon_counts"]
        for r in d["results"]:
            self.assertAlmostEqual(r["ideal_F8"],8*r["isotropic_eta"]**2/9,places=11)
            self.assertAlmostEqual(r["observed_F8_after_known_response"],.99**2*r["ideal_F8"],places=11)

    def test_q8_correlated_detector_postselection_fails_calibration(self):
        d=self.d["robust_q8_schmidt_photon_counts"]
        self.assertGreater(d["outcome_dependent_detector_postselection_attack_l1_shift"],.1)
        self.assertTrue(d["outcome_dependent_attack_exceeds_certified_max_l1"])

    def test_q8_certificates_are_threshold_conditional(self):
        d=self.d["robust_q8_schmidt_photon_counts"]
        r={x["isotropic_eta"]:x for x in d["results"]}
        b95=r[.95]["rank_witnesses"][1]["budget"]
        self.assertTrue(b95["feasible"])
        self.assertEqual(b95["M_accepted_pairs_per_basis"],101343)
        self.assertGreaterEqual(b95["Hoeffding_power_lower_bound"],.95-1e-7)
        self.assertIsNone(r[.8]["rank_witnesses"][1]["budget"].get("M_accepted_pairs_per_basis"))

    def test_photon_prep_99pct_is_not_strong_enough_for_one_flux(self):
        d=self.d["photonic_loss_robust_null"]
        x=d["gate_transmission_cases"]["0.99"]
        self.assertFalse(x["phase_flip_cases"]["1"]["robust_certificate_possible_from_fidelity_only"])
        self.assertTrue(x["phase_flip_cases"]["14"]["robust_certificate_possible_from_fidelity_only"])
        self.assertTrue(x["phase_flip_cases"]["15"]["robust_certificate_possible_from_fidelity_only"])

    def test_photon_single_link_threshold(self):
        d=self.d["photonic_loss_robust_null"]
        thr=d["single_link_detection_minimum_per_gate_intensity_survival_from_fidelity_only"]
        self.assertAlmostEqual(thr,.9979317858857661,places=8)

    def test_S9_frozen_and_unscored(self):
        d=read("s9_frozen_manifest_attack")
        self.assertFalse(d["real_S9_Delta_chi2_scored"])
        self.assertEqual(d["frozen_claim_sha256"],"70951becb3bfe08644e11c56c6cf5939b8970b554810665f5fc60bd6525173da")
        self.assertFalse(d["independent_publisher_SHA256_and_full_FITS"])

if __name__=="__main__":unittest.main()
