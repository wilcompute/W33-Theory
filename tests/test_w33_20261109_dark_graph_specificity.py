"""Tests for W33-specific large flat-band degeneracy vs degree controls."""
import sys,unittest,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261109_flux_dark_mode_fragility import build
import w33_20261109_dark_graph_specificity as work

class DarkGraphSpecificity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/"data/w33_20261109_dark_graph_specificity.json").read_text())
    def test_matched_degree_and_size(self):
        d=self.data
        self.assertEqual(d["native_W33"]["degree_each"],4)
        self.assertEqual(d["connected_four_consecutive_cyclic_hopping"]["degree_each"],4)
        self.assertEqual(d["native_W33"]["incidence_rank"],25)
        self.assertEqual(d["connected_four_consecutive_cyclic_hopping"]["rank"],37)

    def test_random_controls_are_explicitly_not_uniform(self):
        d=self.data["random_configuration_sampler"]
        self.assertEqual(d["sampled_graphs"],128)
        self.assertEqual(sum(d["rank_histogram"].values()),128)
        self.assertEqual(d["equal_or_exceed_W33_flat_band_count"],0)
        self.assertEqual(d["rank_histogram"],{"40":128})
        self.assertIn("not uniform",d["type"])

    def test_one_fresh_connected_simple_4regular_bipartite_graph(self):
        B,edges,G=build()
        self.assertEqual(work.rank(B),25)
        rng=np.random.default_rng(6153)
        M=work.sample(rng)
        self.assertEqual(M.shape,(40,40))
        self.assertTrue(np.all((M==1)|(M==0)))
        self.assertTrue(np.all(M.sum(axis=0)==4))
        self.assertTrue(np.all(M.sum(axis=1)==4))
        self.assertTrue(work.connected(M))
        self.assertGreater(work.rank(M),25)

if __name__=="__main__":unittest.main()
