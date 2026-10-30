"""Regression gates: eight-flag full single-check fault history uniqueness,
K-even H27 chain, intrinsic non-Lorentzian Heisenberg moments, and
loss/calibration/dark-event optical bounds. q7 full 4-line enumeration is C++.
"""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
class Continuation(unittest.TestCase):
 def test_eight_flag_recovery_all_sixteen(self):
  from w33_20261029_eight_flag_two_fault_recovery import verify
  r=verify()
  self.assertEqual(r["check_count"],16)
  self.assertEqual(r["flag_ancillas"],8)
  self.assertEqual(r["total_CNOTs"],524)
  self.assertEqual(r["histories_examined"],4730706)
  self.assertEqual(r["ambiguous_recovery_records"],0)
 def test_H27_chain_symmetry_and_no_go(self):
  from w33_20261029_K_even_chiral_chain_no_go import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual(len(r["checked_ring_sizes"]),6)
  self.assertEqual(r["checked_ring_sizes"][-1]["internal_ground_multiplicity"],2*3**8)
 def test_H27_causal_moments(self):
  from w33_20261029_Hp_intrinsic_subriemannian_obstruction import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual(r["commutator_center_shift"],(0,0,1))
  self.assertEqual(r["Hausdorff_homogeneous_dimension"],4)
 def test_optics_calibration_budgets(self):
  from w33_20261029_photon_adversarial_loss_calibration_budget import verify
  r=verify()
  self.assertEqual(r["status"],"PASS")
  self.assertEqual([x["stats"]["emitted_trials"] for x in r["cases"]],
                   [43047,95513,187342,98767])
if __name__=="__main__":unittest.main()
