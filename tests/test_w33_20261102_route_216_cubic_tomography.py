"""Regression for exact W33 route-minimum cubic tomography (2026-11-02)."""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"analysis"/"w33_20261102_route_216_cubic_tomography.py"
spec=importlib.util.spec_from_file_location("route_cubic_tomography",PATH)
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

class RouteCubicTomography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=M.compute()

    def test_full_216_orbit(self):
        self.assertEqual(self.result["minimum_support_orbit"],216)
        self.assertEqual(self.result["lines_per_support"],10)
        self.assertEqual(self.result["points_covered"],20)

    def test_exact_point_and_line_gram(self):
        self.assertIn("60 I+15 A_point+48 J",self.result["gram_point"])
        self.assertIn("44 I+8 A_line+10 J",self.result["gram_line"])

    def test_tight_24_dimensional_frame(self):
        self.assertEqual(self.result["point_gram_eigenvalues"],{"2160":1,"90":24,"0":15})
        self.assertTrue(self.result["spherical_tight_2_design"])

    def test_full_cubic_tomography(self):
        a={(x["edge_pairs"],x["common_centers"]):
           (x["moment"],x["triple_count"]) for x in self.result["cubic_types"]}
        self.assertEqual(a,{(0,1):(0,2880),(0,4):(-48,360),
                            (1,0):(12,4320),(2,0):(-24,2160),
                            (3,0):(108,160)})
        self.assertEqual(sum(n for _,n in a.values()),9880)

if __name__=="__main__":
    unittest.main()
