"""Exact five-front independent negative controls and local curvature metric jets."""
from pathlib import Path
import math,sys,unittest
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261116_fivefront_exact_negative_controls as n
import toe_20261116_X8_Bianchi_metricjet_quadratic as jets
import toe_20261116_11D_X8_nilpotent_variation as old_x8
import toe_20261116_KK_four_mode_minmax_protection as old_kk
import toe_20261116_qutrit_temporal_router_loophole as old_q
import toe_20261116_IIB_circle_Gysin_linking as old_g

class E6FilterLimits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=n.e6_discrete_filter_no_go()
    def test_cubic_Y_charge(self):
        self.assertTrue(self.r["all_E6_cubic_monomials_have_total_hypercharge_zero"])
    def test_three_filter_eigenvalues(self):
        self.assertEqual(self.r["filter_values_at_minus3_minus2_plus2"],["1","0","0"])
    def test_unfiltered_partner_mixing(self):
        m,mu,yu,yd=sp.symbols("m mu yu yd",nonzero=True)
        coeff=sp.sympify(self.r["induced_B_violating_coefficient"],locals={"m":m,"mu":mu,"yu":yu,"yd":yd})
        self.assertEqual(sp.simplify(coeff-mu*yu*yd/(m*m-mu*mu)),0)
        self.assertEqual(sp.simplify(sp.diff(coeff,mu).subs(mu,0)-yu*yd/m**2),0)
    def test_mixing_caveat(self):
        self.assertIn("additional unfiltered",self.r["important_caveat"])
    def test_Wilsonian_scope(self):
        self.assertIn("perturbatively",self.r["perturbative_Wilsonian_theorem"])

class KKShapeModuli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=n.kk_modular_chambers()
    def test_two_mode_strip(self):
        for y in (1.28,1.4,2.1,3.12):
            for x in (-.5,-.25,0,.25,.5):
                self.assertEqual(n.lattice_modes(x,y),[(-1,0),(1,0)])
    def test_square_four(self):
        self.assertEqual(len(n.lattice_modes(0,1)),4)
    def test_hex_six(self):
        self.assertEqual(len(n.lattice_modes(.5,math.sqrt(3)/2)),6)
    def test_long_torus_mode_multiplicity(self):
        self.assertEqual(len(n.lattice_modes(0,4)),4)
    def test_old_fourmode_valid_only_square(self):
        self.assertEqual(len(old_kk.wavevectors()),4)
        self.assertEqual(self.r["analytic_exact_two_mode_strip"]["only_signed_wavevectors"],[[-1,0],[1,0]])

class X8SecondOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=n.x8_quadratic_variation()
        cls.b=jets.verify()
    def test_firstvariation_zero(self):
        self.assertTrue(self.a["first_curvature_variation_X8_zero"])
    def test_nonzero_unconstrained_second(self):
        self.assertTrue(self.a["nonzero_example_coefficient_by_8form_mask"])
    def test_exact_finite_polynomial_crosscheck(self):
        self.assertTrue(self.a["independent_plus_minus_finite_polynomial_check_passed"])
    def test_Bianchi_met(self):
        self.assertTrue(self.b["algebraic_curvature_tensor_first_Bianchi_passed"])
    def test_Riemann_pair_met(self):
        self.assertTrue(self.b["index_pair_antisymmetry_and_pair_exchange_passed"])
    def test_Bianchi_valid_second_nonzero(self):
        self.assertTrue(self.b["quadratic_X8_nonzero"])
        self.assertTrue(self.b["second_variation_coefficient_by_8form_mask"])
    def test_Bianchi_finite_difference(self):
        self.assertTrue(self.b["independent_t_plusminus_finite_difference_passed"])
    def test_not_physical_eigenmode(self):
        self.assertIn("not a physical",self.b["mathematical_not_physical"])

class IIBSpin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=n.iib_spin_topology()
    def test_spin_6(self):
        self.assertEqual(next(x for x in self.r["examples"] if x["p"]==6)["spin_structures"],2)
    def test_spin_7_6(self):
        self.assertEqual(next(x for x in self.r["examples"] if x["p"]==7)["spin_structures"],1)
    def test_even_spin_not_many_flat_chars(self):
        val=next(x for x in self.r["examples"] if x["p"]==10)
        self.assertEqual((val["spin_structures"],val["flat_U1_characters"]),(1,5))
    def test_linking_from_gysin(self):
        self.assertEqual(old_g.reduce_pair(6,6)["torsion_linking_H2_H4_unit"],"1/6 (mod 1)")
    def test_no_Killing_spinor_from_topology_alone(self):
        self.assertIn("does not imply",self.r["crucial_distinction"])

class QutritRouter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=n.photonic_active_routing()
    def test_lossless_permutation_exists(self):
        self.assertTrue(self.r["constructed_lossless_24x24_permutation_unitary"])
    def test_noncommuting_time_shift(self):
        x=self.r["explicit_noncommutation_on_input_rail0_time0"]
        self.assertNotEqual(x["U_then_shift"],x["shift_then_U"])
    def test_three_temporal_modes(self):
        self.assertEqual(self.r["temporal_mode_and_spatial_mode_Hilbert_dimensions"],[8,3])
    def test_model_loss_threshold_compatible(self):
        a=old_q.budget()
        self.assertGreater(a["minimum_equal_side_temporal_routing_efficiency"],.9)
    def test_abstract_unitary_not_real_hardware(self):
        self.assertIn("NOT a tested fast optical switch",self.r["scope"])

class Combined(unittest.TestCase):
    def test_all_subfronts_pass(self):
        self.assertEqual(n.verify()["status"],"PASS_TOE_FIVEFRONT_EXACT_NEGATIVE_CONTROLS")

if __name__=="__main__":unittest.main()
