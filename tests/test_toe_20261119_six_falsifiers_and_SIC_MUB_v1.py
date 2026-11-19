#!/usr/bin/env python3
"""Independent regression gates for Nov 19 six-track and SIC/MUB packages."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_six_independent_physics_falsifiers_v1 as six
import toe_20261119_H27_sextic_SIC_MUB_hessian_dichotomy as sic

class PhysicalFalsifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=six.run()["all_results"]
        cls.b=sic.run()
    def test_wilson_index_controls(self):
        x=self.a["spinors"]
        self.assertEqual(x["checks"],6)
        self.assertEqual([v["overlap_index"] for v in x["cases"]],[1,0,-1,1,0,-1])
    def test_causal_enumeration(self):
        x=self.a["gravity"]
        self.assertEqual(x["labeled_forward_graphs"],1024)
        self.assertEqual(x["single_edge_monotonicity_checks"],5120)
        self.assertEqual(x["determinant_spread"],0.0)
    def test_causal_response_positive(self):
        x=self.a["gravity"]
        self.assertGreater(x["response_max"],x["response_min"])
    def test_su2_frame_covariance(self):
        self.assertEqual(self.a["gauge"]["gauge_cases"],48)
        self.assertLess(self.a["gauge"]["max_frame_error"],1e-12)
    def test_temporal_pair_indistinguishability(self):
        x=self.a["temporal_qutrit"]
        self.assertLess(max(x["two_output_marginal_residuals"]),1e-12)
        self.assertAlmostEqual(x["XXX_coherent"],1.0,places=12)
        self.assertAlmostEqual(x["XXX_dephased"],0.0,places=12)
    def test_heavy_flavor_two_rank(self):
        x=self.a["matter_flavor"]
        self.assertAlmostEqual(x["one_heavy_mixing_row_CP_cycle"],0.0,places=12)
        self.assertGreater(abs(x["two_independent_heavy_rows_CP_cycle"]),1e-5)
    def test_triangular_unitary_no_go(self):
        x=self.a["unitary_causal_dilation"]
        self.assertLess(x["dilation_unitarity_error"],1e-12)
        self.assertEqual(x["nontrivial_triangular_unitary_rejections"],128)
    def test_sic_hessian_massless(self):
        self.assertEqual(self.b["stationary_support_census"],[1,9,27,27])
        x=self.b["support_two"]
        self.assertEqual(x["W_hessian_rank"],2)
        self.assertEqual(x["mass_squared_eigenvalues"],[0,81,81])
        self.assertEqual(x["zero_coordinate_local_F_root_multiplicity"],2)
    def test_sic_frame(self):
        x=self.b["support_two"]
        self.assertEqual(x["projective_rays"],9)
        self.assertLess(x["SIC_gram_max_error"],1e-12)
        self.assertLess(x["SIC_POVM_error"],1e-12)
    def test_three_mubs_massive(self):
        x=self.b["support_three"]
        self.assertEqual(x["projective_rays"],9)
        self.assertEqual(x["MUB_bases"],3)
        self.assertEqual(x["mass_squared_eigenvalues"],[81,81,81])
        self.assertLess(x["basis_orthogonality_max_error"],1e-12)
        self.assertLess(x["mutual_unbiasedness_max_error"],1e-12)
if __name__=="__main__": unittest.main()
