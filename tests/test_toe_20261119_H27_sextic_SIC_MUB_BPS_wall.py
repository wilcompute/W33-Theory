#!/usr/bin/env python3
"""BPS toy domain-wall exact controls; not a gravity/particle prediction."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_H27_SIC_MUB_BPS_domain_wall as wall

class SICMUBWall(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=wall.run()
    def test_vacuum_energy(self):
        self.assertEqual(self.r["F_term_vacuum_energies_all_supports"],[0,0,0,0])
    def test_superpotential_and_tension(self):
        self.assertEqual(self.r["delta_W"],"1/2")
        self.assertEqual(self.r["BPS_tension_dimensionless"],"1")
    def test_cutoff_convergence(self):
        vals=[r["missing_tail"] for r in self.r["cutoff_numerical_checks"]]
        self.assertGreater(vals[0],vals[1])
        self.assertGreater(vals[1],vals[2])
        self.assertLess(vals[-1],1e-6)
    def test_nonmassive_tail_boundary(self):
        self.assertIn("-1/(3z)",self.r["SIC_side_algebraic_tail"])
        self.assertIn("exp(-9z)",self.r["MUB_side_exponential_tail"])
if __name__=="__main__":unittest.main()
