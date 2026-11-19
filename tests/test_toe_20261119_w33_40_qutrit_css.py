"""Exact tests for the W(3,3) 40-qutrit 19-logical asymmetric CSS code."""
import pathlib
import sys
import unittest
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_w33_40_qutrit_css as c


class W33CSS40Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.P,cls.A,cls.HX,cls.HZ=c.checks()
        cls.report=c.certify()

    def test_symplectic_projective_geometry(self):
        self.assertEqual(len(self.P),40)
        self.assertTrue(np.all(self.A.sum(axis=0)==12))
        self.assertEqual(np.trace(self.A),0)

    def test_exact_mod3_chain_complex_and_ranks(self):
        self.assertTrue(np.all((self.HX@self.HZ.T)%3==0))
        self.assertEqual(c.rank_mod3(self.HX),11)
        self.assertEqual(c.rank_mod3(self.HZ),10)
        self.assertEqual(self.report["logical_qutrits"],19)

    def test_no_undetectable_X_or_Z_weight_one_two_three(self):
        self.assertEqual(c.count_undetectable_through_three(self.HZ),
                         {1:0,2:0,3:0})
        self.assertEqual(c.count_undetectable_through_three(self.HX),
                         {1:0,2:0,3:0})

    def test_Z_distance_at_least_six(self):
        self.assertFalse(c.verify_no_Z_weight_four_or_five(self.HX)
                         ["weight_four_five_Z_kernel_vectors_exist"])

    def test_weight_four_X_logical(self):
        v=np.zeros(40,dtype=np.int64);v[:4]=1
        self.assertTrue(np.all((self.HZ@v)%3==0))
        self.assertEqual(c.rank_mod3(np.column_stack((self.HX,v))),12)

    def test_weight_six_Z_logical(self):
        v=np.zeros(40,dtype=np.int64)
        v[[0,1,2]]=1;v[[4,9,11]]=2
        self.assertTrue(np.all((self.HX@v)%3==0))
        self.assertEqual(c.rank_mod3(np.column_stack((self.HZ,v))),11)
        self.assertEqual(np.count_nonzero(v),6)

    def test_asymmetric_parameters(self):
        self.assertEqual(self.report["code_parameters"],"[[40,19,4]]_3")
        self.assertEqual((self.report["X_distance"],self.report["Z_distance"]),(4,6))
        self.assertIn("separate",self.report["prior_art"][2])

if __name__=="__main__":
    unittest.main()
