"""Exact sparse CSS stabilizer check basis minimization for W33 40 qutrits."""
import pathlib
import sys
import unittest
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_w33_40_sparse_css_checks as sparse
import toe_20261119_w33_40_qutrit_css as base

class SparseChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=sparse.certify()
        cls.pts,cls.A,cls.HX,cls.HZ=base.checks()

    def test_CSS_commutation_and_full_rank(self):
        r=self.result
        self.assertEqual((r["X_check_basis_count"],r["Z_check_basis_count"]),(11,10))
        self.assertEqual((r["X_check_weight"],r["Z_check_weight"]),(13,18))
        self.assertEqual(r["total_minimum_generator_support"],323)

    def test_new_Z_basis_is_same_stabilizer_group(self):
        r=self.result
        X=np.zeros((11,40),dtype=np.int64)
        Z=np.zeros((10,40),dtype=np.int64)
        for j,entry in enumerate(r["X_basis"]):
            X[j,entry["positions"]]=entry["coefficients"]
        for j,entry in enumerate(r["Z_basis"]):
            Z[j,entry["positions"]]=entry["coefficients"]
        self.assertTrue(np.array_equal(base.rref_mod3(X),base.rref_mod3(self.HX)))
        self.assertTrue(np.array_equal(base.rref_mod3(Z),base.rref_mod3(self.HZ)))
        self.assertTrue(np.all((X@Z.T)%3==0))

    def test_exact_minimum_ternary_quadratic_weight_enumeration(self):
        r=self.result
        self.assertEqual(r["quadratic_classical_code_minimum_weight"],18)
        self.assertEqual(r["quadratic_minimum_codewords_including_scalar"],1560)

    def test_total_support_saved(self):
        r=self.result
        self.assertEqual(r["uncustomized_row_selection_support"],413)
        self.assertEqual(r["support_reduction"],90)
        self.assertAlmostEqual(r["support_reduction_fraction"],90/413)

if __name__=="__main__":
    unittest.main()
