"""Regression suite for the October 29 W33 transversal-gate certificates."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_20261029_oddq_css_transversal_gate_obstruction as gate
import w33_20261029_logical_cz_e8_quadratic_refinement as cz

class TestW33LogicalGates(unittest.TestCase):
    def test_q3_geometry_and_weight_enumerator(self):
        A=gate.adjacency_q3()
        self.assertEqual(len(A),40)
        b=gate.binary_basis(A)
        self.assertEqual(len(b),16)
        self.assertEqual(gate.exact_weight_distribution(b),{
            0:1,8:45,12:1120,16:15570,20:32064,
            24:15570,28:1120,32:45,40:1})

    def test_odd_q_uniform_T_obstruction(self):
        for q in (3,5,7,9,11,13,17,19,23,31,43,47):
            cert=gate.odd_q_certificate(q)
            self.assertTrue(cert["self_orthogonal"])
            self.assertNotEqual(cert["uniform_T_obstruction"]["weight_mod8"],0)
            self.assertEqual(cert["doubly_even"],q%4==3)
        self.assertEqual(gate.odd_q_certificate(7)["uniform_T_obstruction"]["weight"],100)

    def test_E8_quadratic_four_CZ_truth_table(self):
        result=cz.main()
        self.assertEqual(result["status"],"PASS")
        self.assertEqual((result["q0_classes"],result["q1_classes"]),(136,120))
        self.assertEqual(result["hyperbolic_pairs"],4)

if __name__=="__main__":
    unittest.main()
