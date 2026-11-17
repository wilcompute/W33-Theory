"""Independent tests for E6 Higgs Hessian & proton operators, M5 KK and CS, qutrit routing."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261116_E6_full_hessian_proton_triplets as e6
import toe_20261116_11D_C3_CS_global_Page_audit as cs
import toe_20261116_nearequal_torus_BF_8derivative as kk
import toe_20261116_qutrit_temporal_router_loophole as opt
import toe_20261116_E6_isolated_SM_Higgs_vacuum as prior_e6
import toe_20261116_qutrit_F3_optical_budget as prior_opt

class E6HessianAndPhenomenology(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=e6.verify()
    def test_full_Higgs_rank(self):
        self.assertEqual(self.data["full_higgs_rank"]["gauge_fixed_Higgs_Hessian_rank"],120)
    def test_dim186_breaking(self):
        self.assertEqual(self.data["full_higgs_rank"]["full_186_chiral_zeromodes_after_gauge_restore"],66)
    def test_real_centralizer(self):
        self.assertEqual(self.data["full_higgs_rank"]["centralizer_exact_Hessian_rank"],16)
    def test_charged_pairs(self):
        self.assertEqual(self.data["full_higgs_rank"]["charged_Hbar_H_sector_rank"],100)
    def test_neutral_frame_Goldstones(self):
        self.assertEqual(self.data["full_higgs_rank"]["neutral_2by2_frame_sector_rank"],4)
    def test_triplet_mass(self):
        self.assertEqual(self.data["SU5_triplet_exchange"]["spectator_color_triplet_mass_in_units_of_v"],5)
    def test_dangerous_operators(self):
        r=self.data["SU5_triplet_exchange"]
        self.assertIn("('Q', 'Q')",r["up_type_counts"])
        self.assertIn("('e_c', 'u_c')",r["up_type_counts"])
        self.assertIn("('L', 'Q')",r["down_type_counts"])
        self.assertIn("('d_c', 'u_c')",r["down_type_counts"])
    def test_prior_vacuum_independent(self):
        self.assertEqual(prior_e6.verify()["physical_Higgs_sector_holomorphic_Hessian_rank"],120)

class FiveDTopologicalCouplings(unittest.TestCase):
    def test_C3_A_pairing(self):
        a=cs.pairings(5,6,6)
        self.assertEqual(a["five_D_external_C3_vector_F2_pairing"],[6,6,5])
    def test_B_antisymmetric(self):
        a=cs.pairings(5,6,6)
        self.assertEqual(a["five_D_twoform_B2_pairing_matrix"],[[0,5],[-5,0]])
    def test_gcd_and_second_Smith(self):
        a=cs.pairings(100,101,100)
        self.assertEqual(a["integer_Smith_Q_gcd"],1)
        self.assertEqual(a["B2_pairing_Smith_invariants"],[100,100])
    def test_no_global_normalization_claim(self):
        self.assertIn("not sufficient",cs.verify()["physical_globally_nontrivial"])

class LargeNStability(unittest.TestCase):
    def test_square_BF_gap(self):
        self.assertGreater(kk.GAP_EQUAL,1)
        self.assertLess(kk.M_EQUAL,-5)
    def test_uniform_shape_BF_gap(self):
        self.assertGreater(kk.UNIFORM_GAP,.46)
    def test_near_equal_radion_law(self):
        for n in (100,1000):
            self.assertGreater(kk.case(n)["exact_homogeneous_BF_gap"],0)
            self.assertLess(kk.case(n)["exact_homogeneous_BF_gap"],50/n**2)
    def test_KK_proxy_not_actual(self):
        z=kk.verify()
        self.assertTrue(all(x["physical_KK_gap_is_NOT_computed"] for x in z["finite_N_geometry_and_proxy"]))
    def test_uniform_C_need_N2(self):
        z=kk.verify()
        self.assertIn("uniformly O(C/N^2)",z["controlled_eight_derivative_thresholds"]["bounded_N_independent_C_cannot_remove_O1_KK_gap"])

class PhotonicLossAndSelection(unittest.TestCase):
    def test_temporal_router_threshold(self):
        x=opt.budget()
        self.assertGreater(x["minimum_equal_side_temporal_routing_efficiency"],.91)
        self.assertLess(x["minimum_equal_side_temporal_routing_efficiency"],.93)
    def test_router_bad(self):
        self.assertFalse(next(z["witness_asymptotically_detectable"] for z in opt.budget()["sweep"] if z["temporal_demultiplexer_efficiency_each_analyzer"]==.9))
    def test_spatial_multiport_not_timebin(self):
        self.assertIn("not alone",opt.verify()["temporal_mode_no_go"])
    def test_postselect_fake_success(self):
        self.assertEqual(opt.fake_coincidence_test()["postselected_coincidence_matching"],1)
        self.assertEqual(opt.fake_coincidence_test()["valid_eventready_all_trial_matching"],.25)
    def test_non_IID_prior_witness(self):
        x=prior_opt.verify()
        self.assertLess(x["identity_and_analyzer"]["operator_max_norm_residual"],1e-12)

if __name__=="__main__":unittest.main()
