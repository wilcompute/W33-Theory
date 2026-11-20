"""Regression tests for the mixed W33-Levi x repetition ternary hypergraph product."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from toe_20261120_mixed_levi_repetition_hgp import levi_graph,shortest_cycle,no_low_weight_kernel,run
from scipy.sparse import csr_matrix

class MixedHGPTests(unittest.TestCase):
    def test_levi_geometry(self):
        g=levi_graph()
        self.assertEqual((len(g.nodes()),len(g.edges())),(80,160))
        self.assertEqual(len(shortest_cycle(g)),8)
    def test_asymmetric_code(self):
        c=run(write=False)
        self.assertEqual(c["CSS"]["physical_qutrits"],638)
        self.assertEqual(c["CSS"]["encoded_qutrits"],81)
        self.assertEqual((c["CSS"]["dX"],c["CSS"]["dZ"]),(3,8))
        self.assertTrue(c["proof"]["CSS_orthogonality"])
        self.assertNotEqual(c["proof"]["XZ_pairing_mod3"],0)
        self.assertEqual((c["CSS"]["max_X_check_weight"],c["CSS"]["max_Z_check_weight"]),(6,4))
    def test_distance_firewall(self):
        self.assertFalse(no_low_weight_kernel(csr_matrix([[1,2],[0,0]])))
        self.assertFalse(no_low_weight_kernel(csr_matrix([[0,1],[0,0]])))
        self.assertTrue(no_low_weight_kernel(csr_matrix([[1,0],[0,1]])))
    def test_deterministic(self):
        self.assertEqual(run(write=False),run(write=False))

if __name__=="__main__":
    unittest.main()
