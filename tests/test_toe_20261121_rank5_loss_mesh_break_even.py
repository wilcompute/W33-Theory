"""Reproduce the deterministic ten-mode Petz/optimal optical loss comparison."""
from __future__ import annotations
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_rank5_loss_mesh_break_even as study

class DecoderLossMesh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=study.main()

    def test_optical_mesh_count(self):
        for name in ("Petz","SDP_rank5"):
            self.assertEqual(len(self.d["cases"][name]),5)
            self.assertTrue(all(x["mesh_gate_count"]==45 for x in self.d["cases"][name]))

    def test_better_ideal_optimized_fidelity(self):
        x=self.d["cases"]
        self.assertGreater(x["SDP_rank5"][0]["unconditional_fidelity"],
                           x["Petz"][0]["unconditional_fidelity"])

    def test_loss_crossover(self):
        c=self.d["numerical_crossing_per_active_gate_intensity_loss"]
        self.assertAlmostEqual(c,.01706290421950856,places=5)

    def test_surviving_optimal_decoder_remains_better(self):
        self.assertTrue(self.d["conditional_advantage_SDP_in_sampled_grid"])

    def test_more_photon_loss_can_reverse_unconditional_advantage(self):
        x=self.d["cases"]
        self.assertGreater(x["Petz"][-1]["unconditional_fidelity"],
                           x["SDP_rank5"][-1]["unconditional_fidelity"])
        self.assertGreater(x["Petz"][-1]["survival_average"],
                           x["SDP_rank5"][-1]["survival_average"])

    def test_loss_model_caveat(self):
        self.assertIn("Architecture-specific",self.d["interpretation"])
        self.assertIn("no universal",self.d["interpretation"])

if __name__=="__main__": unittest.main()
