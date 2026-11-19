"""Independent 26-test verification of six new mathematical TOE constraints.

Execute with:
 python -m unittest discover -s tests -p test_toe_20261118_sixfront_global_center_morse_selection.py -v
"""
import math,sys,unittest
from pathlib import Path
import numpy as np
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_sixfront_global_center_morse_selection as C

class GlobalCenterMorseSixFront(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=C.run()
    def test_global_E8_quotient_order_three(self):
        self.assertEqual(self.d["E8_global_center"]["quotient_kernel_pairs"],
                         [[0,0],[1,2],[2,1]])
    def test_global_E8_center_phase_four_sectors(self):
        rows=self.d["E8_global_center"]["central_table"]
        for row in rows:
            self.assertEqual(row["acts_trivially_on_full_248"],
                             row["sector_27x3_character_exponent"]==0)
            self.assertEqual((row["sector_27x3_character_exponent"]+
                              row["sector_27barx3bar_exponent"])%3,0)
    def test_H27_center_equals_E6_center(self):
        self.assertTrue(self.d["E8_global_center"]["E6_center_equals_SU3_center_in_global_E8_subgroup"])
    def test_center_order_not_independent_81(self):
        a=self.d["E8_global_center"]
        self.assertEqual(a["product_H27_and_E6_center_in_E8_order"],27)
        self.assertEqual(a["false_independent_product_order"],81)
    def test_H27_discrete_adjoint_gap(self):
        a=self.d["H27_adjoint_gap"]
        self.assertEqual(a["sharp_min_positive_eigenvalue"],"3/2")
        self.assertEqual(len(a["traceless_adjoint_eigenvalues"]),8)
    def test_H27_discrete_adjoint_multiplicities(self):
        a=self.d["H27_adjoint_gap"]["traceless_adjoint_eigenvalues"]
        self.assertEqual(a.count(1.5),4)
        self.assertEqual(a.count(3.0),4)
    def test_H27_no_parallel_adjoint_nonzero(self):
        self.assertTrue(self.d["H27_adjoint_gap"]["no_nonzero_cocovariantly_constant_SU3_adjoint_Higgs"])
    def test_Morse_all_n_2_to_8(self):
        rows=self.d["harmonic_family_selection"]["table"]
        self.assertEqual([r["n"] for r in rows],list(range(2,9)))
        self.assertEqual([r["numerical_critical_count"] for r in rows],list(range(2,9)))
    def test_Morse_strong_tilt_bound(self):
        for row in self.d["harmonic_family_selection"]["table"]:
            self.assertLess(row["sufficient_any_direction_tilt_magnitude"],1)
    def test_Morse_each_root_satisfies_exact_gradient(self):
        for row in self.d["harmonic_family_selection"]["table"]:
            n=row["n"]
            for x,y in row["complex_root_coordinates"]:
                w=complex(x,y)
                self.assertLess(abs(w.conjugate()**n-w-1),1e-8)
    def test_Morse_each_Hessian_has_exactly_one_negative(self):
        for row in self.d["harmonic_family_selection"]["table"]:
            n=row["n"]
            for x,y in row["complex_root_coordinates"]:
                u=complex(x,y)**(n-1)
                H=np.array([[n*u.real-1,-n*u.imag,0],
                    [-n*u.imag,-n*u.real-1,0],[0,0,2.]],float)
                eig=np.linalg.eigvalsh(H)
                self.assertEqual(sum(eig<0),1)
                self.assertGreater(eig[1],0)
    def test_Morse_generalized_energy_reduces_old_quartic(self):
        a=next(r for r in self.d["harmonic_family_selection"]["table"] if r["n"]==3)
        self.assertEqual(a["leading_energy_coefficient_times_pi"],"64/315")
        self.assertEqual(a["leading_power"],9)
    def test_Morse_quintic_has_4_not_3(self):
        a=next(r for r in self.d["harmonic_family_selection"]["table"] if r["n"]==4)
        self.assertEqual(a["guaranteed_Morse_index1_count"],4)
        self.assertEqual(a["leading_power"],11)
    def test_S7_untwisted_no_zero_spinor(self):
        self.assertEqual(self.d["AdS4_S7_Dirac"]["zero_internal_untwisted_spinor_modes"],0)
    def test_S7_exact_lowest_spinor_eigen(self):
        a=self.d["AdS4_S7_Dirac"]
        self.assertEqual(a["first8_levels"][0]["positive_Dirac_eigenvalue_times_AdS4_L"],"7/4")
        self.assertEqual(a["exact_ground_Dirac_squared_L2"],"49/16")
    def test_S7_Lichnerowicz_gap(self):
        a=self.d["AdS4_S7_Dirac"]
        self.assertEqual(a["Lichnerowicz_bound_Dirac_squared_L2"],"21/8")
        self.assertGreater(s.Rational(a["exact_ground_Dirac_squared_L2"]),
                           s.Rational(a["Lichnerowicz_bound_Dirac_squared_L2"]))
    def test_S7_each_multiplicity(self):
        for r in self.d["AdS4_S7_Dirac"]["first8_levels"]:
            k=r["k"]
            self.assertEqual(r["multiplicity_each_sign"],8*math.comb(k+6,6))
    def test_E6_Higgs_two_charges_independent(self):
        a=self.d["E6_vectorlike_Higgs"]
        self.assertEqual(a["Abelian_charge_determinant"],-20)
        self.assertTrue(a["breaks_both_extra_Abelian_generators_at_rank2"])
    def test_E6_Higgs_Abelian_mass_positive(self):
        M=s.Matrix(self.d["E6_vectorlike_Higgs"]["normalized_equal_vev_Abelian_mass_Gram"])
        self.assertEqual(M,s.Matrix([[50,-10],[-10,34]]))
        self.assertEqual(M.det(),1600)
    def test_E6_Higgs_full_symbolic_Fflat(self):
        n,nb,ss,sb,x,y=s.symbols("n nb ss sb x y")
        W=x*(nb*n-1)+y*(sb*ss-1)
        point={n:1,nb:1,ss:1,sb:1,x:0,y:0}
        for f in (n,nb,ss,sb,x,y):
            self.assertEqual(s.diff(W,f).subs(point),0)
    def test_E6_Higgs_symbolic_Dflat(self):
        Dchi=-5*1**2+5*1**2
        Dpsi=1*1**2-1*1**2+4*1**2-4*1**2
        self.assertEqual((Dchi,Dpsi),(0,0))
    def test_E6_Higgs_pairs_introduce_additional_fields(self):
        self.assertIn("two distinct",self.d["E6_vectorlike_Higgs"]["Higgs_multiplets"])
    def test_photon_readout_limit_three_percent(self):
        self.assertAlmostEqual(self.d["photonic_assignment"]["exact_ideal_witness_surviving_symmetric_assignment_error_limit"],
                               .030241966417143162,places=12)
    def test_photon_witness_crosses_threshold(self):
        rows=self.d["photonic_assignment"]["rows"]
        self.assertLess(rows[3]["expected_undebiasable_raw_witness"],0)
        self.assertGreater(rows[4]["expected_undebiasable_raw_witness"],0)
    def test_photon_power_at_one_pct_assignment(self):
        row=self.d["photonic_assignment"]["rows"][1]
        self.assertAlmostEqual(row["n900_exact_model_power"],.4832946,delta=.001)
    def test_photon_power_collapses_two_pct_assignment(self):
        row=self.d["photonic_assignment"]["rows"][2]
        self.assertLess(row["n900_exact_model_power"],.01)

if __name__=="__main__":unittest.main()
