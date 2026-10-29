"""Regression for the exact partial-overlap three-photon theorem."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261029_three_photon_partial_overlap import coefficients,main
class PartialOverlap(unittest.TestCase):
    def test_all_signed_patterns(self):
        self.assertEqual(coefficients(511),(4374,13122,8748))
        upper=tuple(max(coefficients(i)[j] for i in range(511)) for j in range(3))
        self.assertEqual(upper,(3564,5832,3888))
        self.assertEqual(tuple(x-y for x,y in zip(coefficients(511),upper)),(810,7290,4860))
    def test_geometry_and_witness(self):
        r=main()
        self.assertEqual(r["W33_independent_triple_common_neighbor_histogram"],{"1":2880,"4":360})
        self.assertEqual(r["dual_independent_triple_common_neighbor_histogram"],{"0":1080,"2":2160})
        self.assertGreater(r["guaranteed_probability_gap_at_s0"],0)
        self.assertGreater(r["guaranteed_probability_gap_at_s1"],0)
if __name__=="__main__":unittest.main()
