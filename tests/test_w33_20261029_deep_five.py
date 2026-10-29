"""Exact W33 deep-five independent regression suite."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261029_deep_five_verifier import main,polynomial
class FiveDeep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=main()
    def test_logical_line_pair_census(self):
        a=self.data["geometry"]
        self.assertEqual([x["two_line_logicals_weight_2q"] for x in a],[240,2340,11200])
        self.assertEqual([x["distinct_weight_2q_logical_cosets"] for x in a],[120,2340,11200])
        self.assertEqual([x["word_multiplicity_per_coset"] for x in a],[2,1,1])
        self.assertEqual(a[2]["adjacency_binary_rank"],176)
        self.assertFalse(a[2]["q7_exact_minimum_distance_proved"])
    def test_complex_gram_coefficients(self):
        self.assertEqual(polynomial(511),(4374,4374,4374,4374,8748))
        a=self.data["complex_gram_three_photon"]
        self.assertEqual(a["W33_masks"],[511]*4)
        self.assertEqual(a["dual_masks"],[259,3,35,32])
        self.assertEqual(a["difference_integer_coefficients"],[14120,14120,18520,18520,37040])
        self.assertEqual(a["certified_positive_pair_coefficients_after_AMGM"],
                         ["5320/3","18520/3","18520/3"])
    def test_quantitative_hardware_bound(self):
        a=self.data["loss_and_device_certified_bounds"]
        self.assertLess(a["symmetric_per_device_operator_norm_strict_error_ceiling"],0.00021)
        self.assertGreater(a["symmetric_per_device_operator_norm_strict_error_ceiling"],0.0002)
        self.assertGreater(a["emitted_per_registered_triple_trial_eta_0p9"],1.37)
    def test_odd_q_revivals(self):
        a=self.data["odd_q_continuous_time_walk"]
        self.assertEqual([x["quarter_t_pi_over_2_onsite_probability"] for x in a],
                         ["1/25","4/169","9/625"])
        self.assertEqual(a[0]["quarter_t_pi_over_2_each_nonneighbor_probability"],"4/225")
        self.assertTrue(all(x["earliest_projective_revival_t_pi"] for x in a))
    def test_e8_fock_parity(self):
        a=self.data["E8_center_Fock_parity"]
        self.assertEqual(a["Fock_sector_phases"],{str(i):(-1)**i for i in range(9)})
        self.assertTrue(a["phase_reference_or_controlled_path_required"])
if __name__=="__main__":unittest.main()
