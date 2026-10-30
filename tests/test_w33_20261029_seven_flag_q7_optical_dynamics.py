"""Regression of 2026-10-29 optimized seven-flag W33 extraction, optical noise,
H27 chiral chain, and exact intrinsic Cayley moment obstruction.
The exhaustive q7 4-line and six-bit Sidon searches compile as C++ separately.
"""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
class Tier3(unittest.TestCase):
 def test_seven_flag_two_fault_recovery(self):
  from w33_20261029_seven_flag_sidon_fault_recovery import verify
  r=verify()
  self.assertEqual(r["flag_ancillas"],7)
  self.assertEqual(r["check_count"],16)
  self.assertEqual(r["total_CNOTs"],394)
  self.assertEqual(r["total_elementary_fault_cases"],10262)
  self.assertEqual(r["histories_examined"],3306573)
  self.assertEqual(r["ambiguous_recovery_records"],0)
 def test_even_chain(self):
  from w33_20261029_K_even_chiral_chain_no_go import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual(r["checked_ring_sizes"][-1]["internal_ground_multiplicity"],2*(3**8))
 def test_exact_anisotropy(self):
  from w33_20261029_Hp_intrinsic_subriemannian_obstruction import verify
  r=verify()
  self.assertEqual(r["commutator_center_shift"],(0,0,1))
  self.assertEqual(r["tested_points"],7*7*3)
 def test_calibration(self):
  from w33_20261029_photon_adversarial_loss_calibration_budget import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual([v["stats"]["emitted_trials"] for v in r["cases"]],
                   [43047,95513,187342,98767])
if __name__=="__main__":unittest.main()
