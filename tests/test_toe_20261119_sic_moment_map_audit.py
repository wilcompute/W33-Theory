"""Regression for the H27 SIC / SU(3) moment-map completion boundary."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis"/"toe_20261119_sic_moment_map_audit.py"
DATA=ROOT/"data"/"toe_20261119_sic_moment_map_audit.json"

class TestH27SICMomentMap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result=subprocess.run([sys.executable,str(SCRIPT)],capture_output=True,text=True,cwd=ROOT)
        assert result.returncode==0,(result.stdout,result.stderr)
        cls.data=json.loads(DATA.read_text(encoding="utf-8"))

    def test_affine_and_projective_counts(self):
        self.assertEqual(self.data["support_counts_0_through_3"],[1,9,27,27])
        self.assertEqual(self.data["support_two_affine_vacua"],27)
        self.assertEqual(self.data["support_two_projective_rays"],9)

    def test_F_mass_rank(self):
        self.assertEqual(self.data["holomorphic_hessian_rank"],2)
        self.assertEqual(self.data["F_hessian_at_1_1_0"],[[-9,0,0],[0,-9,0],[0,0,0]])

    def test_su3_no_go_and_nine_field_repair(self):
        self.assertEqual(self.data["su3_fundamental_single_triplet_moment_norm_squared"],"4/3")
        self.assertEqual(self.data["nine_field_su3_moment_maps"],["0"]*8)
        self.assertEqual(self.data["nine_unnormalized_sic_frame_operator"],"6*I_3")

    def test_gauge_invariance_boundary(self):
        self.assertIn("NOT SU(3)-gauge invariant",self.data["limits"])
        self.assertEqual(self.data["nine_state_pair_overlap_squared"],"1/4")

if __name__=="__main__":
    unittest.main()
