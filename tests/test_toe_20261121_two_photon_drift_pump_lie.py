"""Regression for truly two-photon optical states, Witting pump symmetry,
finite-shot detector drift and loss-aware U(5) Kraus-gauge refinement.
Generate all three result certificates first, e.g. via workflow.
"""
from __future__ import annotations
import json,math,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_two_photon_pair_pump as pair
import toe_20261121_detector_drift_calibration as drift
import toe_20261121_kraus_gauge_lie_refinement as mesh

class FiveFrontContinuation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def load(path):
            p=ROOT/"data"/path
            if not p.exists(): raise RuntimeError(f"Generate certificate before running regression: {p}")
            return json.loads(p.read_text(encoding="utf8"))
        cls.pair=load("toe_20261121_two_photon_pair_pump.json")
        cls.drift=load("toe_20261121_detector_drift_calibration.json")
        cls.mesh=load("toe_20261121_kraus_gauge_lie_refinement.json")

    def test_completed_front_certificates(self):
        self.assertEqual(self.pair["status"],"PASS")
        self.assertEqual(self.drift["status"],"PASS")
        self.assertEqual(self.mesh["status"],"PASS")

    def test_two_photon_computational_scattering_dimension(self):
        K=pair.photon_cross_amplitudes(pair.mode_beam_splitter(math.pi/8))
        self.assertEqual(K.shape,(16,16))
        self.assertLess(np.max(abs(K-np.diag(np.diag(K)))),1e-12)

    def test_bunching_rigidity_and_block_locality(self):
        U=np.eye(8,dtype=complex)
        np.testing.assert_allclose(pair.photon_cross_amplitudes(U),np.eye(16),atol=1e-12)
        np.testing.assert_allclose(pair.computational_leakage(U),0,atol=1e-12)
        self.assertTrue(self.pair["front1_two_real_photons"]["block_and_swap_limit_exact"])

    def test_postselected_entanglement_not_a_deterministic_gate(self):
        z=self.pair["front1_two_real_photons"]["postselection_scan"][-1]
        self.assertAlmostEqual(z["postselected_one_each_probability_given_logical_plus_plus"],.5)
        self.assertAlmostEqual(z["normalized_two_qubit_concurrence"],1.)
        self.assertAlmostEqual(z["maximum_input_basis_leak_probability"],1.)

    def test_postselection_is_destructive_not_heralded_gate(self):
        self.assertIn("destructive",self.pair["front1_two_real_photons"]["critical_limit"])

    def test_all_coordinate_S4_pair_covariance(self):
        v=self.pair["front2_covariant_pump_pair_creation"]
        self.assertEqual(v["S4_coordinate_symmetry_generators_verified"],24)
        self.assertLess(v["largest_24D_pair_subspace_covariance_residual"],1e-12)

    def test_energy_conserving_pair_creation(self):
        v=self.pair["front2_covariant_pump_pair_creation"]
        self.assertAlmostEqual(v["pump_excitation_energy"],2*v["single_24D_level_energy"])
        for row in v["model_scan"]:
            self.assertAlmostEqual(row["pump_energy"]+row["two_chart_energy"],
                                   v["pump_excitation_energy"])

    def test_pair_population_Rabi_formula(self):
        v=self.pair["front2_covariant_pump_pair_creation"]["model_scan"]
        self.assertAlmostEqual(v[3]["local_24D_population"],.5)
        self.assertAlmostEqual(v[-1]["local_24D_population"],1.)

    def test_heterogeneous_gain_and_finite_shot_budget(self):
        f=self.drift
        self.assertLess(f["true_reference_detector_efficiency_min_max"][0],.7)
        self.assertGreater(f["true_reference_detector_efficiency_min_max"][1],.8)
        for l in f["layouts"]:
            errors=[x["empirical_RMS_hidden_vector_error"] for x in l["finite_shot_simulation"]]
            self.assertLess(errors[1],errors[0])
            self.assertLess(errors[2],errors[1])

    def test_worst_drift_amplifies_in_new_private_compromise(self):
        r=self.drift["layouts"]
        self.assertEqual([x["name"] for x in r],["older_25","newer_25","full_40"])
        self.assertGreater(r[1]["worst_hidden_bias_for_0p5pct_RMS_drift"],
                           r[0]["worst_hidden_bias_for_0p5pct_RMS_drift"])
        self.assertGreater(r[0]["worst_hidden_bias_for_0p5pct_RMS_drift"],
                           r[2]["worst_hidden_bias_for_0p5pct_RMS_drift"])

    def test_drift_time_confounds_infinite_photon_limit(self):
        self.assertIn("cannot cancel",self.drift["scope"])

    def test_gauge_refinement_improves_both_compilers(self):
        v=self.mesh
        for name in ("Petz","SDP_rank5"):
            self.assertGreater(v[name]["refined_lossy_entanglement_fidelity"],
                               v[name]["previous_200_Haar_best"])
            self.assertEqual(v[name]["local_perturbations"],400)

    def test_refined_optimal_decoder_surpasses_eighty_percent(self):
        v=self.mesh
        self.assertGreater(v["SDP_rank5"]["refined_lossy_entanglement_fidelity"],.802)
        self.assertGreater(v["SDP_rank5"]["refined_lossy_entanglement_fidelity"],
                           v["Petz"]["refined_lossy_entanglement_fidelity"])

    def test_saved_five_by_five_gauge_is_unitary(self):
        for name in ("Petz","SDP_rank5"):
            data=self.mesh[name]
            G=np.array(data["best_G_real"])+1j*np.array(data["best_G_imag"])
            self.assertEqual(G.shape,(5,5))
            np.testing.assert_allclose(G.conj().T@G,np.eye(5),atol=1e-10)

    def test_no_physical_claim_or_global_optimality(self):
        self.assertIn("not a globally optimal",self.mesh["limitation"])
        self.assertIn("NOT emergent",self.pair["front2_covariant_pump_pair_creation"]["critical_limit"])

if __name__=="__main__":unittest.main()
