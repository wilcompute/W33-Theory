"""Independent regressions for the eight-front W33 research package."""
from __future__ import annotations
import sys,json,unittest
from pathlib import Path
from fractions import Fraction
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261102_eightfront_partA as a
import w33_20261102_eightfront_partB as b
import w33_20261102_exact_blind_irreducibility as irrep
import w33_20261102_q7_full_cubic_tensor_types as cubic
class EightFrontRegressions(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.pa=json.loads((ROOT/"data/w33_20261102_eightfront_partA.json").read_text())
  cls.pb=json.loads((ROOT/"data/w33_20261102_eightfront_partB.json").read_text())
  cls.q7=json.loads((ROOT/"data/w33_20261102_q7_exhaustive_triple_moments.json").read_text())
 def test_01_optics_ideal_full_frame(self):
  Z,V,S,rot,P=b.prepare()
  self.assertEqual(len(rot),4884)
  self.assertEqual(V.shape,(216,24))
  self.assertLess(np.max(abs(P.sum(0)-1)),1e-10)
  self.assertLess(self.pb["optical_noise"]["scenarios"][0]["mean_conditional_total_variation"],1e-10)
  self.assertLess(self.pb["optical_noise"]["scenarios"][1]["mean_single_photon_survival"],1)
 def test_02_q7_full_exhaustive_orbit_five_cubic_types(self):
  self.assertEqual(self.q7["status"],"PASS_FULL_ORBIT")
  self.assertEqual(self.q7["orbit_supports"],720300)
  res=cubic.main()
  self.assertEqual(res["global_weighted_cubic_sum"],"800")
  self.assertEqual(res["distinct_triple_orbit_types"]["line"]["moment"],"93/28")
  self.assertTrue(res["line_moment_distinct_from_all_nonlines"])
 def test_03_exact_blind_module_modular_certificate(self):
  r=irrep.main()
  self.assertEqual([x["centralizer_rank_mod_prime"] for x in r["field_checks"]],[224,224])
  self.assertEqual([x["modular_nullity_of_K"] for x in r["field_checks"]],[15,15])
  self.assertEqual(r["status"],"PASS_EXACT_ABSOLUTE_IRREDUCIBILITY")
  self.assertEqual(json.loads((ROOT/"data/w33_20261102_216_stabilizer_orbitals.json").read_text())["pair_orbital_rank"],10)
 def test_04_27D_reducible_control_and_cubic_obstruction(self):
  r=a.albert_control()
  self.assertEqual(r["dimension"],27)
  self.assertEqual(r["control_adjoint_identity_tests"],12)
  self.assertNotEqual(r["iteration_a_component"],0)
 def test_05_cyclic_connected_cover_gap_bound(self):
  r=a.cyclic_cover()
  self.assertEqual([x["layers"] for x in r["cover_family"]],[3,5,9,15])
  self.assertTrue(all(x["first_gap"]<x["exact_analytic_rayleigh_upper_bound"] for x in r["cover_family"]))
 def test_06_physical_twirling_requirement(self):
  Z,V,S,rot,P=b.prepare()
  r=b.detector_twirling(Z)
  self.assertLess(r["symmetry_twirl_gain_std_after"],r["systematic_detector_gain_std_before"]/10)
  self.assertIn("physical output switching",r["scope"])
 def test_07_two_stage_simplex_effect(self):
  Z,V,S,rot,P=b.prepare()
  r=b.simplex_spectral_test(Z)
  self.assertEqual(r["status"],"EXPLICIT_6_VECTOR_SIMPLEX_WITNESS")
  self.assertEqual(r["simplex_projector_rank"],5)
 def test_08_static_disorder_echo_degradation(self):
  r=a.echo()
  f=[x["mean_entanglement_fidelity"] for x in r["results"]]
  self.assertAlmostEqual(f[0],1)
  self.assertGreater(f[1],f[2])
  self.assertGreater(f[2],f[3])
if __name__=="__main__":unittest.main()
