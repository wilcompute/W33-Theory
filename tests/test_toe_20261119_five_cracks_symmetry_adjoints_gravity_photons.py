"""Focused TOE 'five cracks' consistency tests, no W33 assumptions."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_five_cracks_symmetry_adjoints_gravity_photons as crack

class FiveCracks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=crack.su5_three_adjoint_completion()
        cls.r=crack.E8_discrete_R_necessary_gate()
        cls.v=crack.singlet_driving_field_FD_completion()
        cls.w=crack.torus_Wilson_line_gate()
        cls.e=crack.lattice_linearized_Einstein_gate()
        cls.p=crack.two_copy_one_photon_SSR_activation()

    def test_SU5_three_24F_full_threshold_unification(self):
        self.assertLess(self.g["one_loop_inverse_coupling_spread"],1e-9)
        self.assertEqual(len(self.g["SU2_triplet_masses_GeV"]),3)
        self.assertEqual(len(self.g["SU3_octet_masses_GeV"]),3)
        self.assertEqual(len(self.g["X_leptoquark_masses_GeV"]),3)
        self.assertAlmostEqual(self.g["one_loop_inverse_couplings_at_MU"][0],36.35908537,places=6)

    def test_SU5_partner_mass_matrices_are_heavy(self):
        self.assertGreater(min(self.g["X_leptoquark_masses_GeV"]),1e15)
        self.assertGreater(min(self.g["singlet_masses_GeV"]),1e15)
        self.assertLess(min(self.g["SU3_octet_masses_GeV"]),1e5)

    def test_SU5_is_formal_fine_tuned_not_proton_prediction(self):
        self.assertLess(self.g["smallest_light_to_heavy_cancellation_fraction"],3e-12)
        self.assertIn("2-loop",self.g["not_solved"])

    def test_same_triplets_support_tree_level_rank_two_neutrinos(self):
        self.assertTrue(self.g["seesaw_typeIII_two_heavy_triplets"])
        self.assertEqual(self.g["seesaw_light_mass_rank"],2)
        for a,b in zip(self.g["seesaw_reconstruction_eV"],
                       self.g["seesaw_normal_ordering_input_eV"]):
            self.assertAlmostEqual(a,b,places=12)

    def test_E8_R_forbids_singlet_cubics_but_allows_spurion_Yukawas(self):
        self.assertTrue(self.r["one_singlet_Yukawas_R_allowed"])
        self.assertTrue(self.r["singlet_bilinears_and_dangerous_cubics_R_forbidden"])
        self.assertTrue(self.r["all_pure_singlet_polynomials_forbidden_at_exact_R_level"])
        self.assertEqual(self.r["ten_R_charges"]["10_12"],1)

    def test_E8_R_gauge_mixed_anomaly_mod2(self):
        self.assertEqual(self.r["Spin10_mod_eta_2"],0)
        self.assertTrue(all(v==0 for row in self.r["U1a_U1b_R_mixed_anomaly_mod2"] for v in row))
        self.assertEqual(self.r["Dflat_pair_plus_triangle_charge_sum"],[0,0,0])

    def test_E8_R_gravitational_anomaly_not_fixed(self):
        self.assertEqual(self.r["minimal_supergravity_gravitational_Z4R_coefficient"],-21)
        self.assertEqual(self.r["gravitational_Z4R_mod_eta_2"],1)
        self.assertTrue(self.r["one_neutral_R0_chiral_makes_gravitational_mod2_zero"])

    def test_neutral_R2_drivers_give_explicit_nonzero_F_Dflat_vacuum(self):
        self.assertTrue(all(abs(z)<1e-12 for z in self.v["Fterm_driving_residual"]))
        self.assertTrue(all(abs(z)<1e-12 for z in self.v["Fterm_charged_residual"]))
        self.assertEqual(self.v["three_Dterms_residual"],[0,0,0])
        self.assertGreater(self.v["explicit_condensates"]["S13"],0.)
        self.assertEqual(self.v["local_moduli_count_on_five_field_branch"],0)

    def test_charge_lattice_residual_Z4_is_not_Rsymmetry(self):
        self.assertEqual(self.v["Higgs_charge_index_abs_det"],4)
        self.assertEqual(self.v["Higgs_charge_Smith_invariants"],[1,1,4])
        self.assertIn("NOT",self.v["global_group_caution"])

    def test_gravitational_R_anomaly_with_drivers_requires_completion(self):
        self.assertEqual(self.v["R_gravitational_mod2_with_drivers"],1)
        self.assertEqual(self.v["R_gravitational_mod2_with_drivers_plus_one_R0_modulus"],0)

    def test_T3_flat_twisted_cohomology(self):
        s=self.w["T3_flat_line_bundle_samples"]
        self.assertEqual(s[0]["twisted_Betti_dimensions"],[1,3,3,1])
        for x in s[1:]:self.assertEqual(x["twisted_Betti_dimensions"],[0,0,0,0])

    def test_Spin10_centralizer_Wilson_line_cannot_lift_unbroken_adjoint(self):
        self.assertIn("acts trivially",self.w["centralizer_obstruction"])
        self.assertIn("3 copies",self.w["centralizer_obstruction"])

    def test_linearized_lattice_Bianchi_identity_and_gauge(self):
        self.assertLess(self.e["discrete_linearized_Bianchi_max_residual"],1e-11)
        self.assertLess(self.e["pure_gauge_Einstein_max_residual"],1e-11)

    def test_transverse_traceless_Nyquist_fake_lattice_zero(self):
        self.assertLess(self.e["staggered_Nyquist_false_zero_Einstein_residual"],1e-11)
        self.assertEqual(self.e["forward_derivative_on_same_Nyquist_amplitude"],2.0)

    def test_two_copy_local_photon_activation(self):
        from math import sqrt
        self.assertEqual(self.p["two_copy_event_ready_one_local_photon_each_probability"],.5)
        self.assertAlmostEqual(self.p["conditional_CHSH_number_conserving_dual_rail"],2*sqrt(2),places=12)
        self.assertEqual(self.p["required_consumed_nonvacuum_photons"],2)

if __name__=="__main__":unittest.main()
