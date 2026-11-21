"""Regression checks for six-label W33 versus dual geometry and prime q controls."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import w33_20261120_six_label_dual_quantum_geometry as G

class SixLabelDualityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=G.run(write=False)

    def test_both_graphs_have_same_point_spectrum(self):
        self.assertEqual(self.result["point_spectrum"],{"12":1,"2":24,"-4":15})

    def test_all_induced_two_to_five_vertex_motifs_match(self):
        small=self.result["all_induced_motifs_through_five"]
        self.assertEqual(set(small),{"2","3","4","5"})
        self.assertTrue(all(x["matching"] for x in small.values()))

    def test_exhaustive_five_vertex_motifs(self):
        x=self.result["all_induced_motifs_through_five"]["5"]
        self.assertEqual(x["subsets_per_graph"],658008)
        self.assertEqual(x["motif_types"],23)

    def test_point_and_dual_triad_center_histograms(self):
        self.assertEqual(self.result["W33_independent_triad_centers"]["histogram"],{"1":2880,"4":360})
        self.assertEqual(self.result["Q43_independent_triad_centers"]["histogram"],{"0":1080,"2":2160})

    def test_first_two_triad_moments_are_identical(self):
        self.assertEqual(self.result["W33_independent_triad_centers"]["moments"][:2],
                         self.result["Q43_independent_triad_centers"]["moments"][:2])

    def test_six_point_triad_moment_differs(self):
        self.assertEqual(self.result["W33_independent_triad_centers"]["moments"][2],1440)
        self.assertEqual(self.result["Q43_independent_triad_centers"]["moments"][2],0)

    def test_point_has_720_K33_dual_none(self):
        self.assertEqual(self.result["W33_independent_triad_centers"]["induced_K33"],720)
        self.assertEqual(self.result["Q43_independent_triad_centers"]["induced_K33"],0)

    def test_45_symplectic_subsystem_frames(self):
        self.assertEqual(self.result["n_symplectic_tensor_splits"],45)
        self.assertEqual(self.result["induced_K33_per_split"],16)

    def test_Weyl_cross_sector_commutators_and_81_basis(self):
        self.assertEqual(self.result["quantum"]["frames"],45)
        self.assertLess(self.result["quantum"]["max_cross_commutator_residual"],1e-11)
        self.assertLess(self.result["quantum"]["HS_basis_residual"],1e-10)

    def test_q2_even_self_dual_case(self):
        a=self.result["prime_field_tests"]["2"]
        self.assertEqual((a["W_point"]["induced_K33"],a["dual"]["induced_K33"]),(10,10))

    def test_q3_odd_duality_distinction(self):
        a=self.result["prime_field_tests"]["3"]
        self.assertEqual((a["W_point"]["induced_K33"],a["dual"]["induced_K33"]),(720,0))

    def test_q5_odd_duality_distinction(self):
        a=self.result["prime_field_tests"]["5"]
        self.assertEqual((a["W_point"]["induced_K33"],a["dual"]["induced_K33"]),(130000,0))
        self.assertEqual(a["W_point"]["histogram"],{"1":312000,"6":13000})
        self.assertEqual(a["dual"]["histogram"],{"0":130000,"2":195000})

if __name__=="__main__":
    unittest.main()
