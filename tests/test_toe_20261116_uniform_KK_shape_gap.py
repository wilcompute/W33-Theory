"""Tests of the sharp shape-uniform 11D equal-flux KK BF deficit."""
import importlib.util, math, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"analysis"/"toe_20261116_uniform_KK_BF_shape_gap.py"
sp=importlib.util.spec_from_file_location("sharpbf",P)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class ShapeUniformBF(unittest.TestCase):
    def test_verify(self):
        self.assertTrue(m.verify()["status"].startswith("PASS"))
    def test_sharp_hexagonal(self):
        t=.5+math.sqrt(3)/2*1j
        w=m.reduced_witness(t)
        bound=m.exact_shape_theorem()["BF_depth_away_from_bound_in_m2L2"]
        self.assertAlmostEqual(w["witness_BF_gap"],bound,places=10)
        self.assertAlmostEqual(w["witness_lambda"],2*math.pi*math.sqrt(3),places=10)
    def test_square_has_larger_deficit(self):
        w=m.reduced_witness(1j)
        self.assertGreater(w["witness_BF_gap"],m.exact_shape_theorem()["BF_depth_away_from_bound_in_m2L2"])
    def test_elongated_torus_requires_higher_harmonic(self):
        for height in (10,100,10000,1e6):
            w=m.reduced_witness(height*1j)
            self.assertGreater(w["witness_Fourier_label"][0],1)
            self.assertGreaterEqual(w["witness_lambda"],1)
            self.assertLessEqual(w["witness_lambda"],2*math.sqrt(3)*math.pi)
    def test_boundary_reduced_samples(self):
        for x in (0,.1,.25,.49,.5):
            t=x+math.sqrt(1-x*x)*1j
            w=m.reduced_witness(t)
            self.assertGreaterEqual(w["witness_BF_gap"],m.exact_shape_theorem()["BF_depth_away_from_bound_in_m2L2"]-1e-9)
    def test_wrong_domain_rejected(self):
        with self.assertRaises(ValueError):m.reduced_witness(.8+.4j)
    def test_mass_BF_band(self):
        self.assertEqual(m.gap(0),0)
        self.assertEqual(m.gap(12),0)
        self.assertAlmostEqual(m.gap(15/4),2.25)
if __name__=="__main__":unittest.main()
