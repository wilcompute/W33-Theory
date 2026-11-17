"""Regression for six independent TOE developments, including prior controls."""
import sys,unittest,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261116_proton_Knu_dressing_bounds as p
import toe_20261116_KK_four_mode_minmax_protection as kk
import toe_20261116_11D_X8_nilpotent_variation as x8
import toe_20261116_IIB_circle_Gysin_linking as y
import toe_20261116_qutrit_eventready_timetag_sequential as q
import toe_20261116_E6_triplet_filter_tolerance as filt
import toe_20261116_nearequal_torus_BF_8derivative as oldKK
import toe_20261116_qutrit_anytime_eprocess as oldQ

class ProtonBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=p.verify()
    def test_exp_lifetime(self):
        self.assertAlmostEqual(p.rate(self.z["single_operator_C6_upper_GeV_minus2"])/p.LIMIT,1)
    def test_bound_scale(self):
        self.assertTrue(2e-31<p.limit_c6()<2.5e-31)
    def test_lifetime_inverse_square(self):
        self.assertTrue(math.isclose(p.rate(2*p.limit_c6()),p.LIMIT/4,rel_tol=1e-12))
    def test_weak_yukawa_passes(self):
        self.assertTrue(self.z["weak_reference"]["passes_single_operator_bound"])
    def test_strong_yukawa_fails(self):
        self.assertFalse(self.z["strong_reference"]["passes_single_operator_bound"])
    def test_superpartner_decoupling(self):
        self.assertAlmostEqual(p.model(ms=2e4)["lifetime_years"]/p.model(ms=1e4)["lifetime_years"],16)
    def test_triplet_mass_scaling(self):
        self.assertAlmostEqual(p.model(Mtriplet=1e17)["lifetime_years"]/p.model(Mtriplet=5e16)["lifetime_years"],4)

class KKFourModes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=kk.verify()
    def test_unique_square_shell(self):
        self.assertEqual(set(kk.wavevectors()),{(1,0),(-1,0),(0,1),(0,-1)})
    def test_four_real_modes(self):
        self.assertEqual(self.z["real_physical_cos_sin_mode_count"],4)
    def test_gap(self):
        self.assertAlmostEqual(kk.GAP,1.0169440813078374,places=10)
    def test_next_shell_not_unstable(self):
        self.assertTrue(self.z["next_shell_at_6pi_stable_in_this_branch"])
    def test_minmax_random_sanity(self):
        self.assertLess(self.z["random_matrix_sanity"]["max_eigen_after_bounded_perturb"],-4)
    def test_conditional_threshold(self):
        self.assertTrue(kk.testN(100,10.,100.)["at_least_four_unstable_if_bound_proven"])
    def test_no_claim_exact_un_equal(self):
        self.assertTrue(self.z["no_physical_unequal_flux_spectrum_claimed"])
    def test_prior_proxy(self):
        self.assertTrue(oldKK.verify()["finite_N_geometry_and_proxy"][-1]["physical_KK_gap_is_NOT_computed"])

class CurvatureX8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=x8.verify()
    def test_curvature_square_zero(self):
        self.assertTrue(self.z["matrix_curvature_wedge_square_zero"])
    def test_all_Pontryagin(self):
        self.assertTrue(self.z["pointwise_tr_R2_and_tr_R4_zero"])
    def test_arbitrary_first_variation(self):
        self.assertTrue(self.z["first_variation_of_X8_zero_for_arbitrary_deltaR"])
    def test_nonzero_second_order_possible(self):
        self.assertTrue(self.z["sample_delta_tr_R2_squared_nonzero"])
    def test_Wedge_sign(self):
        self.assertEqual(x8.wedge_mask(1<<1,1<<0),(-1,3))
    def test_exact_product_factors(self):
        self.assertEqual([z["dimension"] for z in self.z["factors"]],[5,2,2,2])

class GysinTorsionLinking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=y.verify()
    def test_pq_66(self):
        self.assertEqual(y.reduce_pair(6,6)["torsion_linking_H2_H4_unit"],"1/6 (mod 1)")
    def test_coprime_bundle(self):
        self.assertEqual(y.reduce_pair(7,6)["pi1"],"trivial")
    def test_pq_12_18(self):
        self.assertEqual(y.reduce_pair(12,18)["gcd"],6)
    def test_pushforward_kernel(self):
        self.assertEqual(y.reduce_pair(6,9)["H3_generator_fiber_pushforward_to_H2_base"],[2,-3])
    def test_gysin_cohomology_ranks(self):
        self.assertEqual(y.reduce_pair(2,5)["Betti_H0_through_H5"],[1,0,1,1,0,1])
    def test_gysin_e_zero_rejected(self):
        with self.assertRaises(ValueError):y.reduce_pair(0,0)
    def test_sign_convention(self):
        self.assertEqual(y.reduce_pair(-6,9)["torsion_linking_H2_H4_unit"],"1/3 (mod 1)")

class OpticalEventReady(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=q.verify()
    def test_crossing_pinned(self):
        self.assertGreaterEqual(self.z["success_count_16"],14)
    def test_router_95_feasible(self):
        self.assertTrue(self.z["nominal_symmetric_95_percent_router"]["has_positive_witness_gap"])
    def test_router_90_impossible(self):
        self.assertFalse(self.z["symmetric_90_percent_router"]["has_positive_witness_gap"])
    def test_asymmetric_route(self):
        self.assertTrue(self.z["asymmetric_99_90_percent_routers"]["has_positive_witness_gap"])
    def test_efficiency_loss(self):
        self.assertLess(self.z["nominal_symmetric_95_percent_router"]["calibrated_pair_detection"],.75)
    def test_all_heralds_counted(self):
        self.assertEqual(self.z["nominal_symmetric_95_percent_router"]["no_click_label"],0)
    def test_prior_evidence_theorem(self):
        self.assertLessEqual(oldQ.check_factor(.51,.6,.51),1)

class FilterRobustness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=filt.verify()
    def test_unique_quadratic(self):
        self.assertEqual(self.z["unique_quadratic_filter"]["coefficients"],["-4/5","0","1/5"])
    def test_filter_exact(self):
        self.assertEqual(self.z["unique_quadratic_filter"]["values_at_minus3_minus2_plus2"],[1,0,0])
    def test_detuning_tolerance(self):
        self.assertLess(self.z["proton_bound_high_yukawa"]["max_commuting_eigenvalue_detuning_for_both_triplets"],.3)
    def test_misalignment_reintroduces_exchange(self):
        self.assertFalse(self.z["proton_bound_high_yukawa"]["cases"][-1]["passes_experimental_limit"])
    def test_no_claim_all_orders(self):
        self.assertIn("no all-orders protection",self.z["coefficient_tuning"])
if __name__=="__main__":
    unittest.main()
