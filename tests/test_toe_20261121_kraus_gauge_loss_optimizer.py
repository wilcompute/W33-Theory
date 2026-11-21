"""Test seeded U(5) Kraus-gauge mesh search and loss-dependent decoder ranking."""
from __future__ import annotations
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_kraus_gauge_loss_optimizer as exp

class GaugeLossCompiler(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data=exp.main()

    def test_both_decoders_unchanged_lossless_under_unitary_mixing(self):
        import numpy as np
        rays,_,_,_=exp.decoder.prior.geometry()
        _,Ropt,Rpetz,T,_,_=exp.decoder.optimize_decoder(rays)
        rng=np.random.default_rng(20261121)
        G=exp.random_haar_U5(rng)
        for k in (Ropt,Rpetz):
            shifted=exp.gauge_mix(k,G)
            self.assertEqual(shifted.shape,(5,2,9))
            self.assertLess(np.max(abs(G.conj().T@G-np.eye(5))),1e-10)

    def test_loss_improves_after_sampling_gauges(self):
        a=self.data
        self.assertGreater(a["Petz"]["best_unconditional_fidelity"],
                           a["Petz"]["baseline_unconditional_fidelity"])
        self.assertGreater(a["SDP_rank5"]["best_unconditional_fidelity"],
                           a["SDP_rank5"]["baseline_unconditional_fidelity"])

    def test_selected_optimal_decoder_sample_wins(self):
        self.assertGreater(self.data["SDP_rank5"]["best_unconditional_fidelity"],
                           self.data["Petz"]["best_unconditional_fidelity"])

    def test_best_optimized_witness_at_two_percent_loss(self):
        self.assertGreater(self.data["SDP_rank5"]["best_unconditional_fidelity"],.785)
        self.assertEqual(self.data["SDP_rank5"]["best_mesh_gate_count"],45)

    def test_sampling_scope_disclaimed(self):
        self.assertEqual(self.data["Petz"]["seeded_random_unitary_trials"],200)
        self.assertEqual(self.data["SDP_rank5"]["seeded_random_unitary_trials"],200)
        self.assertIn("no global",self.data["scope"])

if __name__=="__main__":unittest.main()
