"""Focused reproducibility regressions for the five W33 continuation fronts."""
import importlib.util, pathlib, gzip, json, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
P=ROOT/"analysis/w33_20261102_five_deeper_fronts.py"
S=importlib.util.spec_from_file_location("new_five_fronts",P)
M=importlib.util.module_from_spec(S);S.loader.exec_module(M)
class DeeperFrontTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=M.main()
 def test_216_mode_compiler(self):
  r=self.r["optical_compiler"];self.assertEqual(r["adjacent_rotations"],4884)
  self.assertLess(r["max_reconstruction_error"],1e-12)
  self.assertLess(r["max_qr_residual"],1e-12)
  p=ROOT/r["mesh_file"]
  with gzip.open(p,"rt",encoding="utf-8") as f:j=json.load(f)
  self.assertEqual(len(j["rotations"]),4884)
  self.assertEqual(j["input_modes"],24);self.assertEqual(j["output_modes"],216)
 def test_effect_null_leverage(self):
  r=self.r["effect_blind_sector"]
  self.assertEqual(r["exact_null_rank_from_CRT"],15)
  self.assertEqual(r["blind_leverage_each_outcome"],"5/72")
  self.assertLess(r["max_numerical_blind_leverage_deviation"],1e-10)
 def test_cubic_counterexample_scope(self):
  r=self.r["albert_cubic_euclidean_adjoint"]
  self.assertEqual(r["cubic_value"],0)
  self.assertTrue(r["adjoint_of_adjoint_nonzero"])
  self.assertFalse(r["canonical_euclidean_sharp_identity_holds"])
 def test_q7_verified_distinct_supports(self):
  r=self.r["q7"];self.assertGreaterEqual(r["distinct_random_walk_supports_verified"],1000)
  self.assertEqual(r["fixed_point_eigenvalue"],6)
  self.assertEqual(r["positive_eigenspace_dim"],224)
 def test_no_bare_continuum_limit(self):
  r=self.r["continuum"]
  self.assertEqual(r["gap_limit_as_q_to_infinity"],1)
  self.assertEqual(r["tables"][0]["adjacency_eigenvalues"],[12,2,-4])
  self.assertEqual(r["tables"][2]["adjacency_eigenvalues"],[56,6,-8])
if __name__=="__main__":unittest.main()
