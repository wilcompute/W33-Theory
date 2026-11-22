"""Verify passive 4-mode reflectors and the original 780 switch probabilities."""
from __future__ import annotations
import sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261122_witting_fourmode_switch_compiler as c

class FourModeSwitch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=c.main()

    def test_40_reflections(self):
        self.assertEqual(self.d["reflections"],40)

    def test_exact_fourmode_Givens_counts(self):
        self.assertEqual(self.d["arbitrary_two_mode_Givens_per_reflection"],{"0":4,"4":36})

    def test_unitary_synthesis_error(self):
        self.assertLess(self.d["maximum_compiled_matrix_error"],1e-11)

    def test_all_switch_pair_probabilities_preserved(self):
        self.assertEqual(self.d["compiled_switch_minus_probability_pair_counts"],
                         {"0.0":240,"0.444444444":540})

    def test_does_not_claim_constructed_coherent_switch(self):
        self.assertIn("NOT coherently controlled gate order",self.d["boundary"])

if __name__=="__main__":unittest.main()
