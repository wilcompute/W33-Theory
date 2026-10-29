"""Regress the E8 nonsplitting obstruction and 40-mode photonic compiler.
The 1.04-billion-comparison q=7 C++ run is deliberately a separate test.
"""
from __future__ import annotations
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261029_e8_double_cover_obstruction as e8
import w33_20261029_optical_mesh_and_locality as optics

class W33FiveFrontTests(unittest.TestCase):
    def test_e8_integral_nonsplit_witness(self):
        e8.main()
        import json
        p=ROOT/"data/w33_20261029_e8_double_cover_obstruction.json"
        a=json.loads(p.read_text(encoding="utf-8"))
        self.assertEqual(a["finite_group_order"],25920)
        self.assertEqual(a["involutions"],315)
        self.assertEqual(a["rank4_conjugacy_class_size"],270)
        self.assertEqual(a["rank2_conjugacy_class_size"],45)
        self.assertEqual(a["integral_square"],"-I8")
    def test_passive_photonic_circuit(self):
        optics.main()
        import json
        a=json.loads((ROOT/"data/w33_20261029_optical_mesh_and_locality.json").read_text(encoding="utf-8"))
        self.assertEqual(a["G_invariant_commutant_dimension"],3)
        self.assertLessEqual(a["beam_splitter_SU2_elements"],780)
        self.assertLess(a["reconstruction_max_abs_error"],5e-12)
        self.assertEqual(a["quarter_cycle_probabilities"]["each_neighbor"],"1/25")
        self.assertTrue(a["full_eight_qubit_css_not_implemented"])
    def test_cpp_exhaustive_source_present(self):
        p=ROOT/"analysis/cpp/w33_20261029_q7_weight8_exact.cpp"
        txt=p.read_text(encoding="utf-8")
        self.assertIn("1040232501ull",txt)
        self.assertIn("10507399ull",txt)
        self.assertIn("PROJECTED_CROSS_COLLISIONS",txt)

if __name__=="__main__":
    unittest.main()
