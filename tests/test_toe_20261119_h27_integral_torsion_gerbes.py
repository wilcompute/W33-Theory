"""Regression checks for the H27 7-manifold's integral torsion calculation."""
import importlib.util
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/"analysis"/"toe_20261119_h27_integral_torsion_gerbes.py"
spec=importlib.util.spec_from_file_location("h27_torsion",P)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class H27TorsionTests(unittest.TestCase):
    def test_group(self):
        self.assertEqual(len(m.GROUP),27)
        self.assertEqual(m.commutator(m.A,m.B),m.C)
    def test_all_exact_monomial_actions(self):
        for g in m.GROUP:
            for h in m.GROUP:
                for j in range(3):
                    k,p=m.schrodinger_action(h,j)
                    kk,pp=m.schrodinger_action(g,k)
                    self.assertEqual((kk,(p+pp)%3),
                                     m.schrodinger_action(m.multiply(g,h),j))
    def test_integral_vs_real(self):
        r=m.certify()
        self.assertEqual(r["H3_integral"],"(Z/3)^2")
        self.assertEqual(r["H3_deRham_dimension"],0)
        self.assertEqual(r["H2_homology"],"Z + (Z/3)^2")
    def test_integral_cup_ring_certificate(self):
        r=m.certify()
        self.assertEqual(r['torus_fundamental_class_pullback'],
                         'pi*(a cup b) = 3 eta')
        self.assertEqual(r['integral_H3_torsion_generators'],
                         ['a cup eta','b cup eta'])
        self.assertEqual(r['torsion_generator_orders'],[3,3])
    def test_freeness_and_monodromy(self):
        r=m.certify()
        self.assertEqual(r["fixed_point_free_nonidentity"],26)
        self.assertEqual(r["monodromy_on_H2_fiber"],"identity on Z/3")
    def test_physical_firewall(self):
        self.assertIn("physical flux or nonzero H3 curvature",m.certify()["not_claimed"])

if __name__=="__main__":
    unittest.main()
