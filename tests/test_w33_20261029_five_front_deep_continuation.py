"""October 29 rigorous follow-through regressions. Exhaustive q7 triples in
independent compiled analysis/cpp/w33_20261029_q7_three_line_support.cpp.
"""
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))

class FollowThrough(unittest.TestCase):
 def test_all_single_CNOT_pauli_faults_flagged(self):
  from w33_20261029_flag_one_fault_certificate import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual(r["check_count"],16)
  self.assertEqual(r["Pauli_fault_insertions_after_all_CNOTs"],2460)
  self.assertEqual(r["unflagged_data_errors_above_t2"],0)
  self.assertGreater(r["flagged_data_errors_above_t2"],0)
 def test_K_even_degenerate_chiral_vacuum(self):
  from w33_20261029_K_even_chiral_ground_doublet import verify
  r=verify()
  self.assertEqual(r["ground_dimension"],6)
  self.assertAlmostEqual(r["ground_energy"],-2.75)
  self.assertAlmostEqual(r["spectral_gap_above_ground"],.75)
  self.assertTrue(r["real_K_even_H"])
 def test_heisenberg_exact_causal_wave(self):
  from w33_20261029_Hp_exact_causal_wave import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual(r["exact_energy"],"3/4")
  self.assertTrue(r["finite_support_cone"])
  self.assertEqual(r["records"][-1]["ball"],593)
 def test_adversarial_complex_Gram_minimax(self):
  from w33_20261029_adversarial_complex_gram_optical import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual(r["exact_w33_min_numerator"],17496)
  self.assertEqual(r["exact_dual_max_numerator"],6752)
  self.assertEqual((r["full_triple_survival_eta_min_to1_no_false_registration_budgets"]["1.0"]["N"],
                    r["full_triple_survival_eta_min_to1_no_false_registration_budgets"]["1.0"]["threshold"]),(43047,43))
if __name__=="__main__":unittest.main()
