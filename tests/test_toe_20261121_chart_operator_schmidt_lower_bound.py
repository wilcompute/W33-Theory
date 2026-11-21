"""Witting chart gates have OSR8, providing a three-entangler lower bound."""
from __future__ import annotations
import math,unittest,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_chart_operator_schmidt_lower_bound as calc

class Rank8Witting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=calc.main()

    def test_45_verified_chart_interactions(self):
        self.assertEqual(self.r["charts_tested"],45)
        self.assertEqual(self.r["all_operator_schmidt_ranks"],[8])

    def test_exact_operator_singular_values(self):
        self.assertLess(self.r["max_singular_value_error_against_exact_spectrum"],1e-10)

    def test_three_rank_two_entanglers_necessary_not_sufficient(self):
        self.assertEqual(self.r["min_rank2_entangling_gate_count_lower_bound"],3)
        self.assertIn("not proven sufficient",self.r["warning"])

    def test_nontrivial_phase_gate_ranks(self):
        self.assertEqual([r["operator_schmidt_rank"]for r in self.r["phase_dependence"]],[1,8,8,8,1])

    def test_rank_one_controlled_phase_has_OSR_two(self):
        A=np.diag([1,0,0,0])
        B=np.diag([0,0,0,1])
        U=np.eye(16)+(-1-1j)*np.kron(A,B)
        self.assertEqual(int((calc.os_singular_values(U)>1e-10).sum()),2)

if __name__=="__main__":unittest.main()
