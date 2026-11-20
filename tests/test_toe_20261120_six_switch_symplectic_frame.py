"""Independent regression for six-setting symplectic form reconstruction."""
from __future__ import annotations
import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from toe_20261120_six_switch_symplectic_frame import (
    E,J,mod3det,pfaffian,count_all_forms,frame_from_switch,
    verify_random_frames,phase_class,finite_shot_demo,nonlinear_holdout,main
)
from toe_20261120_symplectic_order_sic_switch import OMEGA

class SixSettingGateTests(unittest.TestCase):
    def test_all_729_skew_forms(self):
        c=count_all_forms()
        self.assertEqual((c["all_alternating_forms"],c["singular"],
                          c["nondegenerate"]),(729,261,468))
        self.assertEqual((c["pfaffian_one"],c["pfaffian_two"]),(234,234))
    def test_det_square_pfaffian(self):
        self.assertEqual(pfaffian(J),2)
        self.assertEqual(mod3det(J),pfaffian(J)**2%3)
        self.assertEqual(mod3det(np.zeros((4,4),dtype=int)),0)
    def test_six_standard_basis_settings(self):
        mat,s=frame_from_switch(E)
        self.assertTrue(np.array_equal(mat,J))
        self.assertEqual(s,{"01":0,"02":1,"03":0,"12":0,"13":1,"23":0})
    def test_random_frame_18720_heldout_pairs(self):
        c=verify_random_frames()
        self.assertEqual(c["random_GL4_frames_tested"],24)
        self.assertEqual(c["predicted_pairs_checked"],18720)
        self.assertLess(c["max_Weyl_commutator_residual"],3e-14)
    def test_phase_classification_ideal_and_noise(self):
        self.assertEqual([phase_class(OMEGA**s) for s in range(3)],[0,1,2])
        c=finite_shot_demo()
        self.assertEqual(c["accepted_shots_per_quadrature"],76)
        self.assertEqual(c["accepted_shots_total"],912)
        self.assertEqual(c["simulation_any_six_phase_misclassifications"],0)
        self.assertEqual(c["independent_seeded_trials"],2000)
    def test_nonlinear_mislabeled_holdout_falsifier(self):
        r=nonlinear_holdout()
        self.assertTrue(r["passes_all_six_basis_calibrations"])
        self.assertNotEqual(r["bilinear_prediction"],r["adversarial_actual_phase"])
        self.assertEqual((r["bilinear_prediction"],r["adversarial_actual_phase"]),(1,2))
    def test_full_producer(self):
        r=main(write=False)
        self.assertEqual(r["status"],"PASS_SIX_SWITCH_BILINEAR_FRAME_WITH_HOLDOUT_FALSIFIER")
        self.assertIn("linearity",r["adversarial_holdout"]["invalid_assumption"])

if __name__=="__main__":unittest.main()
