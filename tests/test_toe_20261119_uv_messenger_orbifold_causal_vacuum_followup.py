"""TOE next-step test pack: renormalizable messenger UV completion and 5 other fronts."""
from pathlib import Path
import sys,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_uv_messenger_orbifold_causal_vacuum_followup as q

class TOENextFiveAndMore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e=q.e8_renormalizable_messenger_completion()
        cls.g=q.orbifold_su5_projected_fermions()
        cls.s=q.CP2_twisted_SpinC_chirality()
        cls.c=q.causal_density_independent_link_thinning()
        cls.v=q.quantum_pure_vacuum_energy_selection()
        cls.p=q.photonic_phase_threshold()

    def test_three_renormalizable_messenger_pairs(self):
        self.assertEqual(len(self.e["messenger_Y_charges"]),3)
        self.assertEqual(len(self.e["messenger_Z_charges"]),3)
        self.assertTrue(self.e["all_superpotential_terms_renormalizable_in_fourD"])
        self.assertEqual(self.e["exact_integrated_out_one_pair_coefficient"],"-X*P*R/M")

    def test_heavy_messenger_vevs_not_ignored(self):
        self.assertEqual(len(self.e["Y_messenger_vevs"]),3)
        self.assertTrue(all(abs(y)>.1 for y in self.e["Y_messenger_vevs"]))
        self.assertAlmostEqual(self.e["singlet_squared_vevs"][0],2.04,places=12)
        self.assertAlmostEqual(self.e["singlet_squared_vevs"][2],2.08,places=12)

    def test_exact_F_and_D_vacuum(self):
        self.assertTrue(all(abs(f)<1e-11 for f in self.e["F_X_residual"]))
        self.assertTrue(all(abs(f)<1e-11 for f in self.e["F_Z_residual"]))
        self.assertTrue(all(abs(f)<1e-11 for f in self.e["D_Abelian_residual"]))
        self.assertLess(self.e["symbolic_full_Fterm_max_error"],1e-11)

    def test_independent_symbolic_hessian_check(self):
        self.assertEqual(self.e["Jacobian_rank"],8)
        self.assertEqual(self.e["full_superpotential_Hessian_rank"],16)
        self.assertLess(self.e["symbolic_vs_hand_Jacobian_max_error"],1e-11)
        self.assertEqual(self.e["gauge_tangent_dimension"],3)
        self.assertEqual(self.e["local_physical_complex_moduli_count"],0)

    def test_formal_three_family_Yukawa_charges_and_rank(self):
        v=self.e["three_formal_diagonal_yukawa_spurion_selections"]
        self.assertEqual([x["singlet"] for x in v],["B","A","C"])
        self.assertEqual([x["Higgs_10"] for x in v],["10_34","10_34","10_24"])
        self.assertEqual(self.e["formal_diagonal_mass_rank"],3)
        self.assertTrue(all(x>0 for x in self.e["formal_rank3_diagonal_dimensionless_masses_with_lambda_equals_one"]))
        self.assertIn("only gauge/R-allowed",self.e["Yukawa_warning"])

    def test_uv_messenger_gauge_anomalies_cancel(self):
        self.assertTrue(all(x==0 for row in self.e["added_messenger_mixed_U1squared_R_anomaly"] for x in row))
        self.assertEqual(self.e["added_messenger_grav_R_anomaly"],0)
        self.assertTrue(all(x==0 for plane in self.e["added_messenger_U1cubed_anomaly"]
                            for row in plane for x in row))
        self.assertEqual(self.e["added_messenger_grav_U1_anomaly"],[0,0,0])

    def test_full_gravitational_R_mod2_spectrum_remains_conditional(self):
        self.assertEqual(self.e["five_R2_drivers_gravitational_Z4R_mod2_from_prior_minimal_spectrum"],0)
        self.assertIn("original anomalous U1",self.e["critical_limits"])

    def test_two_boundary_orbifold_parity(self):
        self.assertTrue(self.g["Ppi_is_in_SU5"])
        self.assertEqual(self.g["SU5_generator_even_count"],12)
        self.assertEqual(self.g["SU5_generator_odd_count"],12)
        self.assertEqual(self.g["boundary_pair_even"],"(+,+): zero mode allowed")
        self.assertEqual(self.g["boundary_pair_odd"],"(+,-): zero mode forbidden")

    def test_even_SU5_sector_has_SM_adjoints(self):
        self.assertIn("su3(8)",self.g["even_subalgebra"])
        self.assertIn("su2(3)",self.g["even_subalgebra"])
        self.assertEqual(self.g["missing_X_dirac_pair_beta"],[10/3,2,4/3])
        self.assertEqual(self.g["light_Weyl_adjoint_zero_mode_betas"],[[0.,4/3,2.]])

    def test_spinC_twist_nonuniversal_family_counts(self):
        self.assertEqual([row["index"] for row in self.s["table"]],[0,1,3,6,10,15])
        self.assertEqual([row["effective_spinC_determinant_class"] for row in self.s["table"]],
                         [1,3,5,7,9,11])

    def test_Cp2_three_family_flux_is_assumed(self):
        self.assertEqual(self.s["fixed_spinC_determinant_k"],5)
        self.assertIn("no dynamical flux",self.s["physical_limit"].lower())

    def test_causal_thinning_at_fixed_alpha_keeps_growing(self):
        for a in (0,1,3,15):
            rows=[x for x in self.c["data"] if x["alpha"]==a]
            self.assertEqual(len(rows),3)
            self.assertTrue(rows[2]["expected_retained_links"]>rows[1]["expected_retained_links"]>
                            rows[0]["expected_retained_links"])
        self.assertTrue(self.c["no_fixed_positive_alpha_makes_degree_bounded"])

    def test_causal_thinning_matches_sqrt_rho_coefficients(self):
        from math import pi,sqrt
        for a in (0,1,3,15):
            rows=[x for x in self.c["data"] if x["alpha"]==a]
            self.assertAlmostEqual(rows[-1]["asymptotic_div_sqrt_rho"],
                                   pi*sqrt(6/(1+a)),places=10)
            self.assertLess(abs(rows[-1]["expected_div_sqrt_rho"]/
                                rows[-1]["asymptotic_div_sqrt_rho"]-1),.1)

    def test_vacuum_selection_needs_frequency_as_input(self):
        rows=self.v["table"]
        self.assertEqual(len(rows),4)
        self.assertTrue(all(abs(r["energy_ground"]-r["frequency_omega"]/2)<1e-12
                            for r in rows))
        self.assertNotAlmostEqual(rows[0]["q_variance"],rows[-1]["q_variance"])

    def test_same_CCR_different_pure_ground_states(self):
        self.assertAlmostEqual(self.v["table"][1]["vacuum_squeezing_r"],0.,places=12)
        self.assertGreater(self.v["table"][0]["q_variance"],self.v["table"][-1]["q_variance"])
        self.assertIn("identical CCR",self.v["result"])

    def test_photon_phase_loss_threshold(self):
        self.assertGreater(self.p["maximum_Gaussian_phase_sigma_for_CHSH_violation"],.84)
        self.assertLess(self.p["maximum_Gaussian_phase_sigma_for_CHSH_violation"],.86)
        self.assertGreater(self.p["samples"][0]["max_CHSH"],2)
        self.assertAlmostEqual(self.p["samples"][3]["max_CHSH"],2,places=10)
        self.assertLess(self.p["samples"][-1]["max_CHSH"],2)

    def test_two_QND_herald_losses_reduce_rate(self):
        self.assertAlmostEqual(self.p["ideal_two_photon_eta0p8_herald_probability"],.32)
        self.assertAlmostEqual(self.p["if_two_independent_QND_herald_efficiencies_each_0p7"],.1568)

if __name__=="__main__":unittest.main()
