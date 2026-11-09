"""Exact symbolic PPT bound-entangled Tiles state witness and Q8 frame regression."""
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261109_q8_tiles_ppt_exact as m

class TestTilesPPT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o=m.main()

    def test_exact_PPT_and_purity(self):
        e=self.o["exact_certificate"]
        self.assertTrue(e["partial_transpose_equals_density_exact"])
        self.assertTrue(e["five_projectors_orthonormal_exact"])
        self.assertEqual(e["density_rank"],4)
        self.assertEqual(e["purity"],"1/4")
        self.assertEqual(e["centered_eight_MUB_F8_exact"],"17/144")

    def test_rational_dual_positive_gap(self):
        from fractions import Fraction
        e=self.o["exact_certificate"]
        self.assertTrue(e["valid_ppt_entanglement_witness"])
        lower=Fraction(e["rational_lower_using_sqrt3_gt_433_over_250"])
        self.assertGreater(lower,Fraction(2,3))
        self.assertEqual(lower-Fraction(2,3),
                         Fraction(e["rational_excess_over_separable"]))
        self.assertGreater(e["exact_dual_lower_decimal"],.70)

    def test_three_w33_frames_recover_entanglement(self):
        x=self.o["measurement_and_shots"]
        self.assertLess(max(x["exact_Q8_frame_reconstruction_errors"]),4e-12)
        for y in x["trace_norm_measured_by_each_coset"]:
            self.assertGreater(y,2/3)
            self.assertAlmostEqual(y,0.7022810881801117,places=9)

    def test_preparation_cost_is_finite_but_large(self):
        rows=self.o["measurement_and_shots"]["expected_counts_only_design_table"]
        self.assertEqual(len(rows),12)
        for u in (.0001,.001,.01):
            subs={r["accepted_shots_per_setting"]:r for r in rows
                  if r["efficiency_relative_uncertainty"]==u}
            self.assertFalse(subs[1000000]["detects_bound_entanglement"])
            self.assertTrue(subs[10000000]["detects_bound_entanglement"])

    def test_frozen_result(self):
        p=ROOT/"data/w33_20261109_q8_tiles_ppt_exact.json"
        if p.exists():
            a=json.loads(p.read_text(encoding="utf8"))
            self.assertEqual(a["status"],self.o["status"])
            self.assertEqual(a["exact_certificate"]["density_rank"],4)

if __name__=="__main__":
    unittest.main()
