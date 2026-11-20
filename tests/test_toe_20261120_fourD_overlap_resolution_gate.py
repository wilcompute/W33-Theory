"""Actual 4D overlap-kernel resolution and gauge-covariance regressions."""
import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
from toe_20261120_fourD_overlap_resolution_gate import (
 G5,GAMMAS,index4,wilson_kernel,main
)
class FourDimensionalIndexTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=main(write=False)
 def test_gamma_Clifford_and_chirality(self):
  I=np.eye(4)
  for i,a in enumerate(GAMMAS):
   self.assertLess(np.linalg.norm(a@G5+G5@a),1e-12)
   for j,b in enumerate(GAMMAS):
    self.assertLess(np.linalg.norm(a@b+b@a-(2*I if i==j else 0)),1e-12)
 def test_full_native_4d_hermitian_kernel(self):
  H=wilson_kernel(3,1,1)
  self.assertEqual(H.shape,(324,324))
  self.assertLess(np.linalg.norm(H-H.conj().T),1e-10)
 def test_resolution_failure_even_with_nonzero_gap(self):
  r=self.r["samples"]
  self.assertEqual([r[i]["lattice_overlap_index"] for i in (2,3,4)],[1,1,0])
  self.assertFalse(r[3]["agrees_with_continuum"])
  self.assertFalse(r[4]["agrees_with_continuum"])
  self.assertGreater(r[3]["minimum_Wilson_gap"],.02)
 def test_resolution_success_at_L4(self):
  r=self.r["samples"]
  self.assertEqual([r[i]["lattice_overlap_index"] for i in (5,6,7,8,9)],[1,2,4,4,3])
  self.assertTrue(all(r[i]["agrees_with_continuum"] for i in (5,6,7,8,9)))
  self.assertFalse(r[10]["agrees_with_continuum"])
 def test_random_gauge_covariance(self):
  self.assertLess(self.r["random_gauge_covariance_residual_L3"],2e-12)
 def test_negative_flux_inverts_chiral_sign(self):
  self.assertEqual(index4(3,1,-1)["lattice_overlap_index"],-1)
 def test_status_and_scope(self):
  self.assertEqual(self.r["status"],"PASS_ACTUAL_4D_WILSON_OVERLAP_FLUX_RESOLUTION_GATE")
  self.assertIn("4D 4L^4-by-4L^4",self.r["sources"])
if __name__=="__main__":unittest.main()
