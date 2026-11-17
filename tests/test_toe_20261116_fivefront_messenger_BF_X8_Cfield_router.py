"""Regression tests for five-front TOE conditional calculations, 2026-11-16."""
import sys,math,unittest
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261116_fivefront_messenger_gap_X8_Cfield_router as f
import toe_20261116_X8_Bianchi_metricjet_quadratic as x8
import toe_20261116_IIB_circle_Gysin_linking as gy
import toe_20261116_fivefront_exact_negative_controls as old

class E6MessengerMatching(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=f.messenger_walk_filter()
    def test_five_chain_lengths(self):
        self.assertEqual([r["messenger_pairs"] for r in self.z["paths"]],[2,3,4,5,6])
    def test_order_growth(self):
        self.assertEqual([r["first_mixing_power"] for r in self.z["paths"]],[1,2,3,4,5])
    def test_schur_n2_direct(self):
        m,mu,yu,yd=sp.symbols("m mu yu yd",nonzero=True)
        v=sp.sympify(self.z["paths"][0]["endpoint_operator_coefficient"],
                     locals={"m":m,"mu":mu,"yu":yu,"yd":yd})
        self.assertEqual(sp.simplify(v-mu*yu*yd/(m*m-mu*mu)),0)
    def test_schur_n3(self):
        m,mu,yu,yd=sp.symbols("m mu yu yd",nonzero=True)
        v=sp.sympify(self.z["paths"][1]["endpoint_operator_coefficient"],
                     locals={"m":m,"mu":mu,"yu":yu,"yd":yd})
        self.assertEqual(sp.simplify(v+mu**2*yu*yd/(m*(m*m-2*mu*mu))),0)
    def test_3x3_adj_expansion(self):
        m,mu=sp.symbols("m mu",positive=True)
        A=sp.Matrix([[m,mu,0],[mu,m,mu],[0,mu,m]])
        self.assertEqual(sp.limit(A.inv()[0,2]/mu**2,mu,0),1/m**3)
    def test_B_minus_L_danger(self):
        self.assertIn("B-L=0",self.z["BminusL_and_Rparity_no_go"])
    def test_not_full_E6_symmetry(self):
        self.assertIn("not an E6-consistent",self.z["interpretation"])

class KKStripLowerBound(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=f.kk_two_mode_gap()
    def test_inf_value(self):
        self.assertAlmostEqual(self.z["BF_deficit_infimum"],1.6628431434177413,places=12)
    def test_sup_exact(self):
        self.assertAlmostEqual(self.z["BF_deficit_supremum"],2.25,places=12)
    def test_lambda_bound(self):
        self.assertAlmostEqual(self.z["lambda_upper_open"],3*math.pi**2/4)
    def test_modes_at_y2(self):
        self.assertEqual(old.lattice_modes(.3,2),[(-1,0),(1,0)])
    def test_positive_gap_every_grid_point(self):
        for i in range(1,49):
            y=4/math.pi+(math.pi-4/math.pi)*i/50
            self.assertGreater(f.delta(3*math.pi/y),self.z["BF_deficit_infimum"]-1e-12)
    def test_not_full_KK(self):
        self.assertIn("unconstructed",self.z["limitation"])

class X8BackgroundWedge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=f.x8_C3_bidegree()
    def test_jet_actual_example(self):
        self.assertTrue(x8.verify()["quadratic_X8_nonzero"])
    def test_exact_degrees(self):
        self.assertEqual(self.z["X8_t_squared_form"][0]["external_degree"],4)
        self.assertEqual(self.z["X8_t_squared_form"][0]["internal_degree"],4)
    def test_wedge_zero_only_sample(self):
        self.assertIn("SPECIFIC",self.z["critical_caveat"])
    def test_external5_possible_other_examples(self):
        self.assertIn(">=5 external",self.z["critical_caveat"])
    def test_expected_mask(self):
        self.assertEqual(self.z["X8_t_squared_form"][0]["bitmask"],495)

class FlatGerbeTopology(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=f.flat_Cfield_topology()
    def test_torsion6(self):
        self.assertEqual(self.z["IIB_Y5"]["examples"][1]["flat_degree4_differential_character"],"U(1) x Z_6")
    def test_torsion1(self):
        self.assertEqual(self.z["IIB_Y5"]["examples"][0]["flat_degree4_differential_character"],"U(1)")
    def test_p1_zero_product(self):
        self.assertIn("lambda=p1(TM6)/2=0",self.z["M6_product"]["integral_half_shift"])
    def test_no_M6_torsion(self):
        self.assertEqual(self.z["M6_product"]["flat_differential_4_characters"],"H^3(M6;R/Z)=(U1)^4, no torsion")
    def test_gysin_consistency(self):
        self.assertEqual(gy.reduce_pair(6,6)["gcd"],6)
    def test_physical_Page_caveat(self):
        self.assertIn("NOT a charge-duality derivation",self.z["large_scope_warning"])

class SwitchAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=f.active_router_budget()
    def test_distinct_delays(self):
        l=self.z["fiber_delays_m"]
        self.assertEqual(len(l),3)
        self.assertTrue(l[0]>l[1]>l[2])
    def test_delay_spacing(self):
        l=self.z["fiber_delays_m"]
        self.assertAlmostEqual(l[0]-l[1],299792458e-9/1.47,places=10)
    def test_jitter30ps(self):
        self.assertLess(self.z["misroute_probability_gaussian_jitter_sigma30ps"],1e-30)
    def test_jitter300ps(self):
        self.assertGreater(self.z["misroute_probability_gaussian_jitter_sigma300ps"],.1)
    def test_good_switch(self):
        self.assertTrue(self.z["illustrative_two_switch_loss_cases"][0]["above_previous_91p96pct_benchmark"])
    def test_bad_switch(self):
        self.assertFalse(self.z["illustrative_two_switch_loss_cases"][-1]["above_previous_91p96pct_benchmark"])
    def test_ideal_not_measured(self):
        self.assertFalse(self.z["measured_hardware"])
    def test_prior_active_no_go(self):
        self.assertFalse(old.photonic_active_routing()["time_shift_commutes_with_stationary_U"])

class AllFronts(unittest.TestCase):
    def test_all(self):
        self.assertEqual(f.verify()["status"],"PASS_FIVEFRONT_WILSONIAN_KK_X8_CFIELD_ROUTER_STRESS")
if __name__=="__main__":unittest.main()
