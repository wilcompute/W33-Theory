"""Independent W33 TOE five-front continuation regression, October 29/30.
The q7 pair-orbit exhaustive compiled C++ test is opt-in and separate:
g++ -O3 -std=c++20 analysis/cpp/w33_20261029_q7_five_line_pair_orbits.cpp -o q7five && ./q7five
"""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
class FiveFrontAfterFourLines(unittest.TestCase):
 def test_conditional_2D_chiral_phase(self):
  from w33_20261029_chiral_2d_peierls import verify
  r=verify()
  self.assertEqual(r["plus_phase_magnetization_lower"],"275/288")
  self.assertEqual([x["sector_configurations"] for x in r["numerical_tori"]],[16,512,65536])
 def test_heisenberg_exact_all_n_second_moments(self):
  from w33_20261029_Hp_all_n_second_moments import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual(r["moment_table"][-1]["E_center_squared"],"33/2")
  self.assertEqual(r["moment_table"][-1]["occupied_group_elements"],5167)
 def test_adaptive_conditional_Gram_stochastic_bounds(self):
  from w33_20261029_adaptive_complex_gram_photon_test import verify
  r=verify()
  self.assertEqual(r["N"],43047)
  self.assertEqual(r["cutoff"],43)
  self.assertEqual(r["exact_small_n_adaptive_dynamic_programs"],45)
 def test_ideal_w33_logical_T_injection(self):
  from w33_20261029_CSS_logical_T_injection_interface import verify
  r=verify()
  self.assertEqual(r["status"],"PASS_IDEAL_LOGICAL_INTERFACE")
  self.assertEqual(r["logical_qubits"],8)
  self.assertEqual(r["exact_teleportation_branch_phase_checks"],65536)
if __name__=="__main__":unittest.main()
