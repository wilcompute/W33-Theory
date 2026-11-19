"""Third-family MSSM gauge-Yukawa two-loop sensitivity, no fitted G2 inputs."""
import sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_SU5_3rd_family_RGE_sensitivity as y

class GaugeYukawaSensitivity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=y.run()
    def test_MSSM_exact_two_loop_yukawa_matrix(self):
        self.assertEqual(self.r["two_loop_MSSM_Yukawa_coefficients"],
                         [[5.2,2.8,3.6],[6,6,2],[4,4,0]])
    def test_complete_three_threshold_x_three_yukawa_grid(self):
        self.assertEqual(len(self.r["grid"]),9)
        self.assertEqual(sum(z["extra_triplet_threshold_GeV"] is None for z in self.r["grid"]),3)
    def test_zero_yukawas_reproduce_independently_integrated_gauge_only_solver(self):
        self.assertTrue(self.r["completely_zero_Yukawa_reproduces_other_two_loop_gauge_only_integrator"])
    def test_one_loop_top_bottom_tau_evolve_from_nonzero_input(self):
        z=self.r["grid"][1]
        self.assertEqual(z["yt_yb_ytau_at_1TeV"],[.8,.1,.08])
        self.assertTrue(np.isfinite(z["Yukawa_at_2e16"]).all())
        self.assertTrue(all(q>=0 for q in z["Yukawa_at_2e16"]))
    def test_yukawas_shift_two_loop_unification_residual(self):
        a=self.r["grid"][0]["mismatch_12_13_23"]
        b=self.r["grid"][1]["mismatch_12_13_23"]
        self.assertGreater(abs(a[0]-b[0]),.005)
        self.assertLess(abs(a[0]-b[0]),.05)
    def test_triplet_thresholds_shift_more_than_Yukawa_inputs(self):
        a=self.r["grid"][0]["mismatch_12_13_23"][0]
        b=self.r["grid"][3]["mismatch_12_13_23"][0]
        yshift=abs(self.r["grid"][1]["mismatch_12_13_23"][0]-a)
        self.assertGreater(abs(b-a),20*yshift)
    def test_not_pretending_two_loop_yukawas_or_real_fit(self):
        self.assertIn("supplied by hand",self.r["third_family_Yukawa_input_status"])
        self.assertIn("not all 2-loop Yukawa",self.r["limits"])
if __name__=="__main__":unittest.main()
