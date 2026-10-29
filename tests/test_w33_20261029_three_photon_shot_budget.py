"""Focused exact event and binomial statistical reproduction."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261029_three_photon_1500_trial_protocol import main
class Protocol(unittest.TestCase):
 def test_preselected_input_both_independent_and_errors(self):
  x=main()
  self.assertEqual(x["input_ports"],[0,7,9])
  self.assertTrue(x["independent_in_both_graphs"])
  self.assertEqual(x["point_probability_numerators"],[26244]*4)
  self.assertEqual(x["dual_probability_numerators"],[784,1024,784,64])
  self.assertEqual(x["W33_event_probability"],"144/15625")
  self.assertLess(x["dual_false_W33_probability"],.001)
  self.assertLess(x["W33_false_dual_probability"],.001)
if __name__=="__main__":unittest.main()
