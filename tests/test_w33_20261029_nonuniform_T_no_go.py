"""Regression of nonuniform diagonal T power obstruction."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from w33_20261029_nonuniform_t_gate_no_go import certify,geometry,span_basis,null_basis

class TestNonuniformTNoGo(unittest.TestCase):
    def test_geometry(self):
        rows=geometry()
        self.assertEqual(len(rows),40)
        self.assertEqual(len(span_basis(rows)),16)
        self.assertEqual(len(null_basis(rows)),24)

    def test_all_patterns_excluded_if_nonclifford(self):
        data=certify()
        self.assertEqual(data["status"],"PASS")
        self.assertEqual(data["parity_rank"],39)
        self.assertTrue(data["odd_theta_pattern_impossible"])
        witness=data["contradiction_four_terms"]
        self.assertEqual(len(witness),4)
        self.assertEqual([r["size"] for r in witness],[2,6,4,2])
        self.assertEqual(data["contradiction_xor_mask"],"0x0")
        self.assertEqual(data["contradiction_rhs"],1)

if __name__=="__main__":unittest.main()
