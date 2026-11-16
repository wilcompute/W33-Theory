"""Regression tests for the circle-bundle cup ring and winding lattice census."""
import importlib.util
from pathlib import Path
import math
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("circle",ROOT/"analysis"/"toe_20261116_circle_bundle_ring_winding_lattice.py")
circle=importlib.util.module_from_spec(spec)
spec.loader.exec_module(circle)

class TestRingWinding(unittest.TestCase):
    def test_gysin_cup_square(self):
        self.assertEqual(circle.circle_ring(3,0)["cup_product_mod_g"]["u_squared"],0)
        self.assertEqual(circle.circle_ring(3,3)["cup_product_mod_g"]["u_squared"],2)
        self.assertEqual(circle.circle_ring(4,4)["cup_product_mod_g"]["u_squared"],2)
        self.assertEqual(circle.circle_ring(1,1)["H4"],"0")
    def test_basis_all_signs(self):
        for p,q in [(3,0),(0,3),(3,3),(-4,6),(6,-10),(-3,-3)]:
            record=circle.circle_ring(p,q)
            a,b=record["primitive_charges"]
            r,s=record["H2_free_generator_in_pullback_basis"]
            self.assertEqual(a*s-b*r,1)
    def test_mass_band(self):
        self.assertAlmostEqual(circle.lower_mass(0),-4)
        self.assertAlmostEqual(circle.lower_mass(12),-4)
        self.assertAlmostEqual(circle.lower_mass(15/4),-25/4)
        self.assertLess(circle.lower_mass(3*math.pi),-4)
    def test_square_arithmetic(self):
        for N,N0,n in [(1,1,4),(1,2,0),(2,1,8),(5,1,20)]:
            self.assertEqual(circle.winding_census(N,N0)["number_of_unstable_nonzero_Fourier_labels"],n)
    def test_weyl_cell_bound(self):
        for r in (1,2,5,10,25,100,400):
            b=circle.winding_weyl_bound(r,1,1j)
            self.assertLessEqual(b["lower_proved_bound"],b["exact_count"])
            self.assertLessEqual(b["exact_count"],b["upper_proved_bound"])
        self.assertLess(abs(circle.winding_weyl_bound(400,1,1j)["exact_count"]/1600-1),.01)
    def test_large_radius_deep_instability(self):
        c1=circle.controlled_equal_flux_family(100)
        c2=circle.controlled_equal_flux_family(400)
        self.assertEqual(c1["total_BF_violating_Fourier_labels"],400)
        self.assertEqual(c1["strong_BF_violating_labels_m2L2_at_most_minus_6"],124)
        self.assertEqual(c2["total_BF_violating_Fourier_labels"],1604)
        self.assertEqual(c2["strong_BF_violating_labels_m2L2_at_most_minus_6"],532)
        self.assertGreater(c2["sphere_radius_over_lPlanck"],c1["sphere_radius_over_lPlanck"])
        self.assertGreater(c2["one_torus_cycle_radius_over_lPlanck"],c1["one_torus_cycle_radius_over_lPlanck"])
    def test_modular_invariance(self):
        tau=.34+1.2j
        for t in (tau+1,-1/tau):
            self.assertEqual(circle.winding_census(5,2,tau)["number_of_unstable_nonzero_Fourier_labels"],circle.winding_census(5,2,t)["number_of_unstable_nonzero_Fourier_labels"])

if __name__=="__main__":
    unittest.main()
