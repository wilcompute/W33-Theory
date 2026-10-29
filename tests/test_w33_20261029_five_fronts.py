"""Focused regression checks; exact heavy producers are separately rerunnable."""
from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_incidence_even_line_resolution_20261029 import make_geometry,rank_basis,reduce_row
from w33_20261029_F9_extension_field_rank import mul,INV
from w33_20261029_explicit_mod2_E8_isometry import qE,matmul_col
def read(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf8"))
class FiveFrontTests(unittest.TestCase):
    def test_extension_field(self):
        a=read("w33_20261029_F9_extended_incidence.json")
        self.assertEqual([a["v"],a["rank_A_mod2"],a["rank_N_mod2"],a["logical_dimension"]],[820,370,451,80])
        self.assertEqual(a["even_line_span_rank"],450)
        self.assertTrue(a["AN_equal_J_mod2"])
        self.assertTrue(all(mul(a,INV[a])==3 for a in range(1,9)))
    def test_q5_distance_certificate(self):
        result=read("w33_20261029_adjacency_css_distance_falsifier.json")["results"]
        a,b=result
        self.assertEqual((a["q"],a["k"],a["distance_exact"]),(5,24,10))
        self.assertEqual(a["collision_certificate"]["combinations"],23738715)
        self.assertEqual(a["collision_certificate"]["projected_collisions"],0)
        self.assertEqual((b["q"],b["k"],b["distance_lower_bound"],b["distance_upper_bound"]),(7,48,8,14))
        self.assertEqual(b["collision_certificate"]["combinations"],10586800)
        self.assertEqual(b["collision_certificate"]["projected_collisions"],0)
        for entry in result:
            q=entry["q"]
            pts,lines,lm,A,*_=make_geometry(q)
            mask=sum(1<<i for i in entry["witness"]["support"])
            self.assertEqual(mask.bit_count(),2*q)
            self.assertNotEqual(reduce_row(mask,rank_basis(A)),0)
    def test_faithful_e8_orthogonal_representation(self):
        a=read("w33_20261029_explicit_mod2_E8_isometry.json")
        self.assertEqual(a["roots"],240)
        self.assertEqual(a["root_mod2_antipodal_classes"],120)
        self.assertEqual(a["complete_group_order"],25920)
        self.assertEqual(a["faithful_mod2_action_order"],25920)
        for generator in a["checked_group_generators"]:
            M=generator["E8_simple_root_mod2_columns"]
            self.assertTrue(all(qE(matmul_col(M,v))==qE(v) for v in range(256)))
    def test_photonic_and_dynamics_obstructions(self):
        a=read("w33_20261029_photonic_dynamics_boundaries.json")
        self.assertTrue(a["one_photon_dimension"]["one_photon_40_mode_model_fails_8_logicals"])
        self.assertTrue(a["one_photon_dimension"]["one_photon_240_mode_model_fails_8_logicals"])
        self.assertEqual(a["invariant_dynamics_counterexample"]["H2"],"A+J/40")
        self.assertEqual(a["invariant_dynamics_counterexample"]["H2_site_return_probability"],"361/400")
        self.assertTrue(a["loss_no_go"]["heralded_survival_not_excluded"])
if __name__=="__main__":unittest.main()
