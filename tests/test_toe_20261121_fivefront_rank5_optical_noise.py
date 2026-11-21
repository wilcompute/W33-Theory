"""Reconstruct the five new mathematical fronts and check their boundaries."""
from __future__ import annotations
import unittest, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_fivefront_rank5_optical_noise as model

class FivefrontRank5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=model.main()
        cls.a=cls.result["front1_rank5_optimal_decoder"]
        cls.b=cls.result["front2_phase_noise_and_depolarizing_control"]
        cls.c=cls.result["front3_optical_encoding_gate_cost"]
        cls.d=cls.result["front4_covariant_reference_sector_transfer"]
        cls.e=cls.result["front5_calibrated_25bin_detector"]

    def test_five_fronts_pass(self):
        self.assertEqual(self.result["status"],"PASS")
        self.assertEqual(len([k for k in self.result if k.startswith("front")]),5)

    def test_optimal_decoder_beats_petz(self):
        self.assertGreater(self.a["rank5_CPTP_fidelity"],.91658)
        self.assertGreater(self.a["rank5_CPTP_fidelity"],
                           self.a["petz_entanglement_fidelity"]+.013)

    def test_primal_dual_certificate(self):
        self.assertGreaterEqual(self.a["dual_upper_bound"],self.a["rank5_CPTP_fidelity"])
        self.assertLess(self.a["upper_lower_gap"],2e-6)

    def test_five_kraus_minimal_dilation(self):
        self.assertEqual(self.a["Choi_rank"],5)
        self.assertEqual(self.a["Stinespring_shape"],[10,9])
        self.assertEqual(self.a["decoder_unitary_shape"],[10,10])
        self.assertLess(self.a["TP_residual"],1e-9)

    def test_recovery_phase_noise(self):
        self.assertGreater(self.b["SDP"]["clean"],self.b["Petz"]["clean"])
        self.assertGreater(self.b["SDP"]["fully_output_dephased"],
                           self.b["Petz"]["fully_output_dephased"])
        for v in self.b["SDP"]["gaussian_std_scan"]:
            self.assertLessEqual(v["average_F_e"],self.b["SDP"]["clean"]+1e-10)

    def test_depolarizing_control_is_affine(self):
        self.assertIn("(1-p)",self.b["output_replacement_affine_fidelity"])
        self.assertIn("p/4",self.b["output_replacement_affine_fidelity"])

    def test_45_exact_optical_meshes(self):
        f=self.c["single_photon_16rail_Reck_gate_count"]
        self.assertEqual((f["min"],f["max"]),(45,113))
        self.assertAlmostEqual(f["mean"],93.6)

    def test_local_four_mode_cost(self):
        f=self.c["local_4rail_SIC_basis_Reck_gate_count"]
        self.assertGreaterEqual(f["min"],4)
        self.assertLessEqual(f["max"],6)

    def test_logical_single_photon_scaling(self):
        self.assertEqual(self.c["logical_multi_ququart_single_photon_modes"],"4^n")
        self.assertIn("two interacting photons",self.c["warning"])

    def test_covariant_partial_swap_resource_transfer(self):
        q=self.d["partial_swap_sector_populations"]
        self.assertAlmostEqual(q[0]["sector_populations"][-1],0,places=10)
        self.assertAlmostEqual(q[2]["sector_populations"][-1],.5,places=10)
        self.assertAlmostEqual(q[3]["sector_populations"][-1],1,places=10)

    def test_compressed_sensor_remains_24D_identifiable(self):
        f=self.e["layouts"]
        self.assertEqual(f[0]["rank_identifiable_efficiency_combinations"],25)
        self.assertEqual(f[1]["rank_identifiable_efficiency_combinations"],25)
        self.assertEqual(f[2]["rank_identifiable_efficiency_combinations"],40)

    def test_calibration_25bin_launch_budget(self):
        f=self.e["layouts"]
        self.assertGreater(f[0]["profile_Fisher_inverse_trace"],
                           f[1]["profile_Fisher_inverse_trace"])
        self.assertAlmostEqual(f[1]["profile_Fisher_inverse_trace"],60.385185185,places=5)
        self.assertAlmostEqual(f[2]["profile_Fisher_inverse_trace"],17.0666666667,places=5)

    def test_no_fabricated_experiment_claim(self):
        self.assertIn("not",self.result["scope"].lower())
        self.assertIn("no",self.c["warning"].lower())

if __name__=="__main__":unittest.main()
