"""Regress five independent wire/TOE audits and the recovered native E6 wire producer."""
import sys,math,unittest
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_wire_independent_fivefront_controls as P
import toe_20261118_wire_Novikov_E6 as Native


class WireFiveFrontAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=P.run()

    def test_wire_general_boundary_index(self):
        cases=self.d["wire"]["m"]
        self.assertEqual(len(cases),18)
        for x in cases:
            self.assertEqual(x["relative_betti"],[0,x["point_defects"],0,0])
            self.assertEqual(x["relative_Euler"],-x["point_defects"])

    def test_wire_independent_holonomy_extension(self):
        x=self.d["wire"]["charged_spinor_chi"]
        self.assertEqual(set(x),{"-5","-1","3"})
        self.assertEqual(x["-5"]["modulus"],32)
        self.assertEqual(x["-1"]["modulus"],2)
        self.assertAlmostEqual(x["3"]["modulus"],1/8)
        self.assertTrue(all(not v["extendable_through_C4_core"] for v in x.values()))

    def test_parallels_native_torus_complex(self):
        for t in (1,-1,s.I,-s.I,2,s.Rational(1,2),2*s.I):
            x=Native.topology(t)
            self.assertEqual(x["relative_negative"],[0,3,0,0])
            self.assertEqual(x["relative_positive"],[0,0,3,0])
            self.assertEqual(x["fill_points_solid_torus"],
                             [1,1] if t==1 else [0,0])

    def test_native_charged_E6_spectrum(self):
        x=Native.model_spectrum()
        self.assertEqual(x["family_components"],48)
        self.assertEqual(x["family_conjugate_components"],0)
        for obj in x["charged_family_sector"].values():
            self.assertEqual(obj["chiral_copies"],3)
            self.assertEqual(obj["conjugate_chiral_copies"],0)

    def test_W33_finite_symplectic_orbit_changes_support(self):
        z=self.d["selector"]
        self.assertEqual(z["transvection_count"],40)
        self.assertEqual(z["gauge_fixed_support_distribution"],
                         {"3":4,"5":9,"7":12,"11":12,"29":3})
        self.assertEqual(z["example_next"]["active_chords"],29)

    def test_W33_diffusion_invariant(self):
        self.assertEqual(self.d["selector"]["exact_diffusion_numerator320"],
                         [[162,2,2],[2,162,2],[2,2,162]])

    def test_E6_anomaly_polynomial(self):
        z=self.d["anomaly"]
        self.assertEqual(z["single_family_Tr_chi_squared"],80)
        self.assertEqual(z["single_family_Tr_chi_cubed"],0)
        self.assertEqual(z["extra_Abelian_rank"],2)
        self.assertEqual(z["three_family_gravity_polynomial"],"Tr(a Chi+b Psi)=-144*b")

    def test_only_available_neutrino_singlet_cannot_break_both_U1(self):
        z=self.d["anomaly"]
        self.assertEqual(z["singlet_VEV_Abelian_mass_matrix_unscaled"],[[25,15],[15,9]])
        self.assertEqual(z["singlet_VEV_mass_matrix_rank"],1)
        self.assertEqual(z["residual_unbroken_U1_generator"],"3 Chi -5 Psi")
        self.assertEqual(z["residual_U1_gravitational_anomaly"],720)
        self.assertEqual(z["residual_U1_cubic_anomaly"],259200)

    def test_BF_robust_correction_window(self):
        z=self.d["BF"]
        self.assertEqual(z["max_BF_violation"],2.25)
        row=next(x for x in z["sample_ratios"]
                 if x["flux_ratio"]==2 and x["upward_mass_shift_bound"]==1)
        self.assertAlmostEqual(row["lambda_margin_band"][0],.527864045,places=8)
        self.assertAlmostEqual(row["lambda_margin_band"][1],9.472135955,places=8)
        self.assertAlmostEqual(row["robust_BF_violating_modular_fraction"],
                               .453122108370014,places=9)

    def test_BF_strong_instability_increases_as_shift_bound_relaxes(self):
        for ratio in (1,1.2,2,5,10):
            vals=[row["robust_BF_violating_modular_fraction"]
                  for row in self.d["BF"]["sample_ratios"] if row["flux_ratio"]==ratio]
            self.assertEqual(len(vals),5)
            self.assertTrue(all(a>b for a,b in zip(vals,vals[1:])))
            self.assertTrue(all(0<=p<=1+1e-12 for p in vals))

    def test_quantum_Ville_anytime_null(self):
        z=self.d["memory"]
        self.assertAlmostEqual(z["e_factor_for_success"],1.4)
        self.assertAlmostEqual(z["e_factor_for_failure"],.8)
        for v in z["null_crossing_by_n"]["horizons"].values():
            self.assertLess(v["crossing_probability"],.01)
        self.assertAlmostEqual(z["null_crossing_by_n"]["horizons"]["600"]["crossing_probability"],.008755904950957225,places=10)

    def test_quantum_sequential_power_and_expected_sample(self):
        z=self.d["memory"]["alternative_crossing_by_n"]
        self.assertGreater(z["horizons"]["600"]["crossing_probability"],.998)
        self.assertGreater(z["horizons"]["292"]["crossing_probability"],.95)
        self.assertAlmostEqual(z["expected_accepted_events_until_cross_or_600"],
                               124.62359731383,places=8)


if __name__=="__main__":
    unittest.main()
