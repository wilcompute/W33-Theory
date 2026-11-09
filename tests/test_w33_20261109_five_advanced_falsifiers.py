"""W33/Q8 five fronts: POVM calibration, CZ architecture, chiral winding,
DES Y6 frozen likelihood, and single-photon operational Bell gate."""
import json,math,sys,unittest
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_full_povm_calibration_bound as effect
import w33_20261109_shallow_cz_complete as cz
import w33_20261109_chiral_spectral_winding as winding
import w33_20261109_single_photon_bell_locality as bell

NAMES=("w33_20261109_full_povm_calibration_bound",
       "w33_20261109_shallow_cz_complete",
       "w33_20261109_chiral_spectral_winding",
       "w33_20261109_single_photon_bell_locality",
       "w33_20261109_des_y6_live_frozen_gate")
def read(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))

class TestFiveAdvancedFalsifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.D={name:read(name) for name in NAMES}

    def test_full_povm_uncertainty_theorem_shot_guard(self):
        d=self.D[NAMES[0]]
        self.assertTrue(d["status"].startswith("PASS"))
        self.assertIn("||E-Ehat||op<=delta",d["analytic_theorem"])
        self.assertTrue(d["one_realized_simulated_multinomial"]["certifies"])
        self.assertLessEqual(d["one_realized_simulated_multinomial"]["maximum_frequency_error"],
                             d["one_realized_simulated_multinomial"]["simultaneous_Hoeffding_epsilon"])

    def test_povm_controls_and_calibration(self):
        d=self.D[NAMES[0]]["source_controls"]
        p=d["Horodecki_a0p236"]
        self.assertGreater(p["true_CCNR"],1.003)
        self.assertLess(p["true_CCNR"],1.004)
        self.assertEqual(len(p["calibration_tests"]),4)
        for setting in p["calibration_tests"]:
            self.assertGreater(setting["dual_l1"],10)
            self.assertGreater(setting["shot_grid"][-1]["CCNR_lower"],1)
            self.assertGreaterEqual(setting["conservative_effect_guard"],
                                    setting["actual_max_POVM_effect_difference"]-1e-11)
        for name in ("separable_pure_product","maximally_mixed"):
            self.assertFalse(any(x["prospective_certifies"]
                 for row in d[name]["calibration_tests"] for x in row["shot_grid"]))

    def test_direct_POVM_bound_independent_of_stored_result(self):
        mats,A,b,ops=effect.make_model()
        rho=np.eye(9)/9
        q=effect.detected_q(mats,rho)
        c=effect.certificate(q,A,b,ops,delta=1e-6,N=10**9)
        self.assertLessEqual(c["CCNR_lower"],1+1e-12)
        self.assertGreater(c["dual_row_l1"],0)
        self.assertGreater(c["min_estimated_survival"],0)

    def test_one_CZ_fails_two_CZ_succeeds_in_seeded_set(self):
        d=self.D[NAMES[1]]
        self.assertEqual(d["single_CZ_rank_histogram"],{"76":950})
        self.assertEqual(d["two_CZ_rank_histogram"],{"80":950})
        self.assertEqual(d["max_local_only_rank"],72)
        self.assertEqual(d["full_operator_rank"],80)
        self.assertEqual(d["CZ_layers_per_extra_analyzer"],2)
        self.assertLess(d["max_test_density_reconstruction_error"],5e-12)

    def test_independent_small_CZ_rank_controls(self):
        from w33_20261109_q8_ten_context_tomography import select,projection_design
        _,(B,_,__,op,___)=select(return_components=True)
        Mb=projection_design(B,op)
        rng=np.random.default_rng(20261109721)
        for _ in range(3):
            U=cz.candidate(rng,True);V=cz.candidate(rng,True)
            W=cz.candidate(rng,True,True);Z=cz.candidate(rng,True,True)
            for bases,expect in (((U,V),76),((W,Z),80)):
                M=np.vstack([Mb,projection_design(bases[0],op),
                                projection_design(bases[1],op)])
                self.assertEqual(np.linalg.matrix_rank(M,tol=1e-9),expect)

    def test_gauge_chiral_1d_winding_not_intrinsic(self):
        d=self.D[NAMES[2]]
        self.assertEqual(d["native_W33_Dirac_index"],0)
        self.assertEqual(d["distinct_indices"],[0,15,24,39,40])
        for row in d["models"]:
            self.assertEqual(row["AIII_chiral_winding_index_exact"],
                             row["discretized_independent_winding"])
        self.assertLess(d["pure_point_gauge_phase_spectrum_error"],1e-10)

    def test_exact_rational_winding_new_parameters(self):
        self.assertEqual(winding.winding(.3,.4)["AIII_chiral_winding_index_exact"],15)
        self.assertEqual(winding.winding(-.4,.2)["AIII_chiral_winding_index_exact"],24)
        self.assertEqual(winding.winding(0,1.4)["AIII_chiral_winding_index_exact"],40)

    def test_single_photon_spatial_locality_and_eta_model(self):
        d=self.D[NAMES[3]]["result"]
        self.assertAlmostEqual(d["internal_tensor_CHSH"],2*math.sqrt(2),places=12)
        self.assertAlmostEqual(d["accessible_CHSH_max_under_local_number_SSR_no_phase_reference"],2.,places=12)
        self.assertAlmostEqual(d["spatial_CHSH_if_non_number_commuting_measurements_and_shared_reference_available"],
                               2*math.sqrt(2),places=12)
        self.assertAlmostEqual(d["specific_equal_eta_no_click_as_plus_1_CHSH_threshold"],
                               2/(1+math.sqrt(2)),places=12)
        self.assertFalse(d["does_internal_CHSH_alone_establish_spacelike_Bell_nonlocality"])

    def test_DES_does_not_make_up_likelihood(self):
        d=self.D[NAMES[4]]
        self.assertFalse(d["S9_chi_squared_scored"])
        self.assertFalse(d["genuine_DES_cosmic_shear_data_vector_acquired"])
        self.assertEqual(d["frozen_preregistration"],"2026-11-08")
        self.assertEqual(d["remote_endpoints"]["formerly_indexed_unblinded_3x2pt_FITS"]["status_code"],404)
        self.assertTrue(d["frozen_procedure_preserved"])

    def test_all_frozen_sources_have_scope(self):
        for name,d in self.D.items():
            self.assertTrue(d["status"])
            self.assertFalse(d.get("genuine_DES_cosmic_shear_data_vector_acquired",False))
        self.assertTrue(self.D[NAMES[0]]["no_empirical_photonic_experiment"])

if __name__=="__main__":
    unittest.main()
