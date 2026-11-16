import importlib.util
from pathlib import Path
from fractions import Fraction as F
import unittest
P=Path(__file__).resolve().parents[1]/"analysis"/"toe_20261116_e6_trinification_cubic_flat_branches.py"
spec=importlib.util.spec_from_file_location("flat",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TrinificationCubic(unittest.TestCase):
    def test_verify(self):self.assertTrue(m.verify()["status"].startswith("PASS"))
    def test_nonzero_FD_branch(self):
        for s in [1,3,11]:
            v=m.scalar_triad(s,s,s)
            self.assertEqual(v["F_norm_squared"],0)
            self.assertTrue(v["D_flat"])
    def test_A_rankone(self):
        for s in [1,2,3]:
            r=m.rank1_case(s)
            self.assertEqual(r["F_gradient_square"],"0")
            self.assertEqual(F(r["D_moment_norm_squared"]),F(4*s**4,3))
    def test_adjugate(self):
        A=[[2,1,0],[0,1,3],[1,0,1]]
        prod=m.mult(A,m.adj(A))
        self.assertEqual(prod,m.eye(m.det(A)))
if __name__=="__main__":unittest.main()
