"""Focused regression tests for independently reproduced six-front TOE bounds."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261120_six_uv_memory_drift_chirality_hodge_causal as m

class BoundedGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.d=m.main(write=False)
    def test_01_e8(self):
        self.assertEqual(self.d["e8"]["adjoint_dimension"],248)
        self.assertEqual(self.d["e8"]["single_adjoint_degree3_invariants"],0)
        self.assertEqual(self.d["e8"]["single_adjoint_degree6_invariants"],1)
    def test_02_misalignment(self):
        self.assertAlmostEqual(self.d["qutrit"]["rotated_input_fidelity"],self.d["qutrit"]["analytical_fidelity"],places=12)
        self.assertLess(self.d["qutrit"]["witness_gamma036"],0)
    def test_03_output_unitary(self):self.assertLess(self.d["qutrit"]["common_output_unitary_trace_overlap_error"],1e-12)
    def test_04_su3_timing(self):
        self.assertLess(self.d["twirling"]["palindromic_complex_trace_error"],1e-12)
        self.assertGreater(self.d["twirling"]["chronological_complex_trace_error"],1e-5)
    def test_05_su3_count(self):self.assertEqual(self.d["twirling"]["symmetric_exposures"],18)
    def test_06_spectral_flow(self):self.assertEqual(self.d["chirality"]["periodic_spectral_flow"],0)
    def test_07_levi_geometry(self):
        self.assertEqual((self.d["hodge"]["points"],self.d["hodge"]["lines"],self.d["hodge"]["flags"]),(40,40,160))
    def test_08_levi_projector(self):self.assertTrue(self.d["hodge"]["exact_projector_square"])
    def test_09_levi_nonzero(self):self.assertEqual(self.d["hodge"]["projector_entries_nonzero"],160**2)
    def test_10_KL_fails(self):
        self.assertFalse(self.d["hodge"]["corrects_unknown_single_edge_phase"])
        self.assertAlmostEqual(self.d["hodge"]["one_edge_KL_deviation_Frobenius_squared"],.253125)
    def test_11_pi_phase(self):
        self.assertAlmostEqual(self.d["hodge"]["compressed_pi_phase_eigenvalue"],-1/80)
        self.assertAlmostEqual(self.d["hodge"]["pi_phase_total_Frobenius_leakage"],6399/6400)
    def test_12_causal_2d(self):self.assertAlmostEqual(self.d["causal"]["Myrheim_Meyer_controls"]["2"]["pair_comparability"],.5,delta=.035)
    def test_13_causal_4d(self):self.assertAlmostEqual(self.d["causal"]["Myrheim_Meyer_controls"]["4"]["pair_comparability"],.1,delta=.035)
    def test_14_causal_3chain(self):self.assertGreater(self.d["causal"]["Myrheim_Meyer_controls"]["2"]["three_chain_fraction"],self.d["causal"]["Myrheim_Meyer_controls"]["4"]["three_chain_fraction"])
    def test_15_time_reversal(self):self.assertEqual(sum(self.d["causal"]["time_reversal_arrow"]),0)
if __name__=="__main__":unittest.main()
