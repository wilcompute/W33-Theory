"""Independent regression checks for the binary incidence/adjacency resolution."""
import unittest
from analysis.w33_incidence_even_line_resolution_20261029 import compute

class IncidenceEvenLineResolutionTests(unittest.TestCase):
    def test_binary_rank_complement(self):
        for q, v, n, a, k in [(3,40,25,16,8),(5,156,91,66,24),(7,400,225,176,48)]:
            with self.subTest(q=q):
                x=compute(q)
                self.assertEqual((x["points"],x["rank_incidence"],x["rank_adjacency"],x["logical_dimension"]),(v,n,a,k))
                self.assertEqual(x["even_line_span_dimension"],v-a)
                self.assertTrue(x["adjacency_nilpotent_mod2"])
    def test_mod_four_dichotomy(self):
        self.assertEqual([compute(q)["doubly_even_stabilizer"] for q in (3,5,7)],[True,False,True])
        self.assertEqual([compute(q)["orthogonal_type"] for q in (3,7)],["plus","plus"])
    def test_q3_orthogonal_and_hexads(self):
        x=compute(3)
        self.assertEqual(x["quadratic_counts"],{"singular_including_zero":136,"nonsingular":120})
        self.assertEqual(x["intersecting_line_hexads"],240)

if __name__=="__main__":
    unittest.main()
