import sys
import pathlib
import unittest
import numpy as np

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'analysis'))
import w33_20261031_tick_loop_rigidity as L


class TickLoopRigidity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=L.build()

    def test_exact_pair_invisible_witness(self):
        self.assertEqual(L.exact_trace((0,3,6)),(3,0))
        self.assertEqual(L.exact_trace((1,3,6)),(0,0))
        self.assertEqual(self.result['pair_preserving_local_swap']['ordered_triples_changed'],2808)

    def test_exact_orientation_odd_witness(self):
        self.assertEqual(L.exact_trace((0,12,15)),(2,1))
        self.assertEqual(L.exact_trace((15,12,0)),(1,-1))

    def test_integer_formula_cyclic_and_conjugate(self):
        rng=np.random.default_rng(4199040)
        for triple in rng.integers(0,120,(100,3)):
            a,b=L.exact_trace(triple)
            self.assertEqual((a,b),L.exact_trace(np.roll(triple,1)))
            self.assertEqual((a-b,-b),L.exact_trace(triple[::-1]))

    def test_full_tensor_and_product_controls(self):
        self.assertEqual(self.result['ordered_triples'],1728000)
        design=self.result['partial_Mendelsohn_system']
        self.assertEqual((design['directed_edges'],design['cyclic_blocks']),(9720,3240))
        edges=[(t[i],t[(i+1)%3]) for t in design['cycles'] for i in range(3)]
        self.assertEqual(len(set(edges)),9720)
        self.assertEqual(sum(c['count'] for c in self.result['numerical_Eisenstein_census']),1728000)
        self.assertLess(self.result['full_14400_product_reconstruction_error'],1e-11)
        tri=self.result['isolated_triangle']
        self.assertEqual(L.exact_trace(tri['max_chirality_exact_witness'])[1],2)
        self.assertTrue(tri['imaginary_support_requires_three_noncommuting_directions'])
        for row in tri['samples']:
            expected=min(0,6*row['J']-4*row['K']-abs(row['lambda_loop'])/np.sqrt(3))
            self.assertAlmostEqual(row['minimum'],expected)

    def test_concrete_clifford_and_antiunitary_maps(self):
        self.assertEqual(len(self.result['Clifford_generator_permutations']),9)
        for perm in self.result['Clifford_generator_permutations'].values():
            self.assertEqual(sorted(perm),list(range(120)))
        self.assertEqual(sorted(self.result['antiunitary_permutation']),list(range(120)))


if __name__=='__main__':
    unittest.main()
