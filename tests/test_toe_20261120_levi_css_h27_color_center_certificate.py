"""Focused tests for W33 qutrit syndrome / H27 color-center bundle."""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261120_levi_css_h27_color_center_certificate as m
class TestTwoGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=m.check()
    def test_status(self):self.assertEqual(self.d['status'],'PASS')
    def test_physical(self):self.assertEqual(self.d['CSS']['physical'],638)
    def test_logical(self):self.assertEqual(self.d['CSS']['logical'],81)
    def test_distance(self):self.assertEqual((self.d['CSS']['dX'],self.d['CSS']['dZ']),(3,8))
    def test_X_syndrome_count(self):self.assertEqual(self.d['CSS']['single_X_syndromes'],1276)
    def test_Z_syndrome_count(self):self.assertEqual(self.d['CSS']['single_Z_syndromes'],1276)
    def test_noncollision(self):self.assertEqual(self.d['CSS']['collisions'],0)
    def test_two_error_ambiguity(self):self.assertTrue(self.d['CSS']['two_vs_one_X_ambiguity'])
    def test_H27(self):self.assertLess(self.d['H27']['center_residual'],1e-12)
    def test_SU3_center(self):self.assertTrue(self.d['H27']['center_identified_with_SU3_color_gauge'])
    def test_quotient(self):self.assertEqual(self.d['H27']['global_flavor_quotient'],'Z3^2')
if __name__=='__main__':unittest.main()
