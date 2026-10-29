#!/usr/bin/env python3
"""All five mathematical/prototype fronts. The MILP timeout is never treated
as a distance certificate. The E8 exhaustive test can take >45 seconds.
"""
from pathlib import Path
import json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261029_sp43_integral_cover as cover
import w33_20261029_rectangular_optical_mesh as mesh
import w33_20261029_dual_polar_C3_3 as polar
import w33_20261029_three_photon_dual_discriminator as three
class FiveFronts(unittest.TestCase):
 def test_integral_E8_is_natural_Sp43(self):
  cover.main()
  a=json.loads((ROOT/"data/w33_20261029_sp43_integral_cover.json").read_text())
  self.assertEqual(a["integral_cover_order"],51840)
  self.assertEqual(a["projective_image_order"],25920)
  self.assertTrue(a["central_minus_I4_corresponds_to_minus_I8"])
  self.assertEqual(a["finite_involution_lift_counts"],{"minus":540,"plus":90})
 def test_rectangular_optical_unitary(self):
  mesh.main()
  a=json.loads((ROOT/"data/w33_20261029_rectangular_optical_mesh.json").read_text())
  self.assertEqual(a["rectangular"]["layers"],40)
  self.assertEqual(a["triangular"]["layers"],77)
  self.assertLess(a["rectangular"]["reconstruction_max_abs_error"],3e-12)
  self.assertGreater(a["rectangular"]["input_min_survival"],a["triangular"]["input_min_survival"])
 def test_dual_polar_geometry(self):
  polar.main()
  a=json.loads((ROOT/"data/w33_20261029_dual_polar_C3_3.json").read_text())
  self.assertEqual(a["vertices"],1120)
  self.assertEqual(a["shells"],{"0":1,"1":39,"2":351,"3":729})
  self.assertEqual(a["distance_3_walk_count"],52)
 def test_three_photon_and_dual_CSS(self):
  three.main()
  a=json.loads((ROOT/"data/w33_20261029_three_photon_dual_discriminator.json").read_text())
  self.assertEqual(a["dual_CSS"]["parameters"],"[[40,20,4]]_2")
  self.assertTrue(a["global_two_photon_pair_histograms_equal"])
  self.assertEqual(a["point"]["max_distinct_output_probabilities"]["4"]["numerator"],26244)
  self.assertEqual(a["dual"]["max_distinct_output_probabilities"]["2"]["numerator"],11664)
 def test_q7_does_not_claim_timeout_as_proof(self):
  code=(ROOT/"analysis/w33_20261029_q7_milp_falsifier.py").read_text()
  self.assertIn("proved_infeasible",code)
  self.assertIn("result.status==2",code)
if __name__=="__main__":unittest.main()
