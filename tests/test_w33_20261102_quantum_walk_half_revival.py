"""Regression of the exact half-walk W(3,q) spectral reflection."""
from pathlib import Path
import importlib.util,unittest
P=Path(__file__).resolve().parents[1]/"analysis/w33_20261102_quantum_walk_half_revival.py"
S=importlib.util.spec_from_file_location("w33halfwalk",P)
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class HalfWalkTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=M.main()
 def test_exact_q3_povm_bridge(self):
  self.assertEqual(self.r["status"],"PASS_W3Q_HALFWALK_REFLECTION_POVM_BRIDGE")
  self.assertIn("Z.T Z / 180",self.r["q3_exact_povm_reflection"])
  self.assertAlmostEqual(self.r["cases"][0]["return_and_adjacent_probability"],1/25)
  self.assertAlmostEqual(self.r["cases"][0]["nonadjacent_probability"],4/225)
 def test_q5_q7_unitarity_and_probabilities(self):
  for row in self.r["cases"]:
   self.assertTrue(row["matrix_unitarity_exact"])
   self.assertAlmostEqual((row["valency"]+1)*row["return_and_adjacent_probability"]+
        (row["points"]-row["valency"]-1)*row["nonadjacent_probability"],1)
 def test_periodic_dynamics_and_scope(self):
  self.assertEqual(self.r["unitary_period_for_odd_q"],"pi / J")
  self.assertIn("no derived J",self.r["scope"])
if __name__=="__main__":unittest.main()
