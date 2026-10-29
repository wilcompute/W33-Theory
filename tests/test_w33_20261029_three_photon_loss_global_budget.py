"""Test globally optimized W33/dual three-photon budgets under explicit loss assumptions."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from w33_20261029_three_photon_loss_global_budget import ideal,scenario
class TestOpticalLossBudget(unittest.TestCase):
    def test_ideal_correction(self):
        r=scenario(0,1,0)
        self.assertEqual((r['N'],r['cutoff']),(19427,15))
        self.assertTrue(r['all_smaller_N_checked'])
        self.assertLess(max(r['false_positive'],r['false_negative']),.001)
    def test_loss_scenarios(self):
        a=scenario(.8,1,0)
        b=scenario(.8,.9,0)
        self.assertEqual((a['N'],b['N']),(2437,3345))
        self.assertGreater(b['N'],a['N'])
if __name__=='__main__':unittest.main()
