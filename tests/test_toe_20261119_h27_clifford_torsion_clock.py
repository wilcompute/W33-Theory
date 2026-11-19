"""Regress the exact H27 Clifford/torsion-ray permutation classification."""
import importlib.util
import pathlib
import sys
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_h27_clifford_torsion_clock as m

class TorsionClockTests(unittest.TestCase):
    def test_group_order_and_center_scaling(self):
        self.assertEqual(len(m.GL2),48)
        self.assertEqual(len(m.SL2),24)
        for M in m.GL2:
            self.assertEqual(m.transform(M,m.source.C)[2],m.determinant(M))
    def test_projective_clock_orbits(self):
        self.assertEqual(len(m.RAYS),4)
        self.assertEqual(len({m.ray_permutation(M) for M in m.SL2}),12)
        self.assertEqual(len({m.ray_permutation(M) for M in m.GL2}),24)
    def test_exact_automorphisms(self):
        for M in m.GL2:
            for g in m.source.GROUP:
                for h in m.source.GROUP:
                    self.assertEqual(m.transform(M,m.source.multiply(g,h)),
                                     m.source.multiply(m.transform(M,g),m.transform(M,h)))
    def test_det_twisted_torsion_module(self):
        M=(2,0,0,1)  # determinant -1 mod 3
        self.assertEqual(m.dual_action(M,(1,0)),(2,0))
        self.assertEqual(m.torsion_action(M,(1,0)),(1,0))
        self.assertEqual(m.certify()['H3_torsion_linear_action'],
                         'det(M) * M^T on (F3)^2')
    def test_parity_boundary(self):
        for M in m.GL2:
            self.assertEqual(m.sign(m.ray_permutation(M)),
                             1 if m.determinant(M)==1 else -1)
    def test_claim_firewall(self):
        r=m.certify()
        self.assertIn("not a canonical choice of a clock or an isometry of Y7",r["scope"])

if __name__=="__main__":
    unittest.main()
