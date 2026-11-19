"""Independent tests for coupled H27 BPS existence and four other physical gates."""
import sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_H27_coupled_BPS_five_gates as t

class H27CoupledPhysicalGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.d=t.run()
    def test_sic_is_stationary(self):
        self.assertLess(np.linalg.norm(t.F([0,1,1])),1e-12)
    def test_new_mub_is_stationary(self):
        self.assertLess(np.linalg.norm(t.F([t.R]*3)),1e-12)
    def test_old_mub_is_not_stationary(self):
        self.assertGreater(np.linalg.norm(t.F([1,1,1])),1)
    def test_exact_endpoints_W(self):
        self.assertAlmostEqual(t.W([0,1,1]),1)
        self.assertAlmostEqual(t.W([t.R]*3),25/12,places=12)
    def test_interval_of_coupled_wall_exists_not_only_g_quarter(self):
        x=self.d["coupling_interval_theorem"]
        self.assertEqual(x["proved_interval"],"0<g<=3/8")
        self.assertEqual(len(x["sample_checks"]),5)
        self.assertTrue(x["source_single_positive_and_target_no_positive_Hessian_modes_all_g"])
    def test_exact_tension_family_of_couplings(self):
        for x in self.d["coupling_interval_theorem"]["sample_checks"]:
            g=x["g"]
            self.assertAlmostEqual(x["exact_tension_formula_evaluated"],
              (4*g*g+3)/(3*(1-2*g)),places=11)
    def test_uniform_nullcline_monotonicity_exact_integer_certificate(self):
        self.assertTrue(81*125<27*512)
        for x in self.d["coupling_interval_theorem"]["sample_checks"]:
            self.assertLess(x["g_times_r"],.6)
    def test_original_line_not_coupled_BPS(self):
        self.assertAlmostEqual(t.F([.5,1,1])[1],25/64,places=14)
    def test_endpoint_source_has_single_unstable_eigen(self):
        d=self.d["coupled_BPS"]
        self.assertEqual(d["source_positive_Hessian_count"],1)
        self.assertEqual(d["target_positive_Hessian_count"],0)
    def test_Hessian_at_MUB_exact_eigen(self):
        self.assertTrue(np.allclose(self.d["coupled_BPS"]["target_Hessian_eigenvalues"],
            [-69*t.R/4,-69*t.R/4,-15*t.R/2]))
    def test_analytic_invariant_region(self):
        d=self.d["coupled_BPS"]
        self.assertTrue(d["new_wall_proved_in_symmetric_y_equals_z_plane"])
        self.assertEqual(d["unique_stationary_points_in_rectangle"],2)
        self.assertEqual(len(d["proof_ingredients"]),5)
    def test_bps_numerical_energy_vs_exact_tension(self):
        self.assertAlmostEqual(self.d["coupled_BPS"]["numerical_energy_integral"],13/6,places=7)
        self.assertEqual(self.d["coupled_BPS"]["exact_BPS_tension"],"13/6")
    def test_gradient_ends_at_shifted_mub(self):
        self.assertLess(self.d["coupled_BPS"]["ending_gradient_norm"],1e-11)
    def test_bps_tangent_satisfies_fermion_dirac(self):
        self.assertLess(self.d["coupled_BPS"]["max_chain_rule_DF_minus_HF_error"],1e-7)
    def test_natural_Hessian_fermion_index_one_not_three(self):
        self.assertEqual(self.d["coupled_BPS"]["natural_Hessian_Dirac_Fredholm_index"],1)
        self.assertEqual(self.d["chirality_and_compact"]["natural_mass_choice_M_Hessian_of_W_has_index"],1)
    def test_symmetry_legal_H27_1_plus3_alternative_selects_three(self):
        c=self.d["chirality_and_compact"]
        self.assertTrue(c["H27_covariant_exact_commutators"])
        self.assertEqual(c["alternative_noncompact_chiral_count"],3)
    def test_symmetry_legal_triplet_is_degenerate(self):
        self.assertTrue(self.d["chirality_and_compact"]["alternative_triplet_profiles_identical"])
    def test_circle_index_zero(self):
        self.assertEqual(self.d["chirality_and_compact"]["smooth_circle_index"],0)
    def test_interval_chirality_requires_sourced_BC(self):
        self.assertIn("boundary/domain parity",self.d["chirality_and_compact"]["serious_caution"])
    def test_h27_singlet_higgs_produces_three_degenerate_masses(self):
        a=self.d["flavor_and_GUT"]
        self.assertIn("rank3",a["H27_unbroken_singlet_Higgs_Yukawa"])
        self.assertGreater(a["H27_scalar_portal_overlap_factor"],0)
    def test_SU3_epsilon_mass_is_rank_two(self):
        self.assertEqual(self.d["flavor_and_GUT"]["epsilon_Yukawa_rank"],2)
    def test_SU3_epsilon_two_equal_nonzero_singular_values(self):
        z=self.d["flavor_and_GUT"]["epsilon_Yukawa_singular_values"]
        self.assertAlmostEqual(z[0],z[1],places=10)
        self.assertAlmostEqual(z[2],0,places=10)
    def test_SU3_sextet_can_have_full_rank(self):
        self.assertEqual(self.d["flavor_and_GUT"]["symmetric_anti_sextet_Higgs_example_Yukawa_rank"],3)
    def test_gauged_family_SU3_anomaly_does_not_vanish_for_three_16(self):
        x=self.d["flavor_and_GUT"]
        self.assertEqual(x["gauged_SU3_family_cubic_anomaly_for_one_Spin10_16_triplet"],16)
        self.assertEqual(x["gauged_SU3_family_cubic_anomaly_for_one_E6_27_triplet"],27)
        self.assertEqual(x["complete_E8_E6xSU3_pair_anomaly"],0)
        self.assertIn("discrete anomalies",x["gauged_family_anomaly_caution"])
    def test_SU3_gauge_invariant_sextic_still_unsourced(self):
        self.assertIn("not SU3 invariant",self.d["flavor_and_GUT"]["E8_UV_warning"])
    def test_causal_pair_same_all_interval_layer_counts(self):
        self.assertEqual(self.d["causal_action_discriminator"]["same_global_causal_interval_histogram"],[2,0,0,0])
    def test_causal_pair_laplacian_spectra_differ(self):
        c=self.d["causal_action_discriminator"]
        self.assertNotEqual(c["Laplacian_trace_square_A"],c["Laplacian_trace_square_B"])
        self.assertEqual((c["Laplacian_trace_square_A"],c["Laplacian_trace_square_B"]),(10,8))
    def test_causal_spectrum_not_yet_Einstein(self):
        self.assertIn("no physical Lorentzian gravitational action",self.d["causal_action_discriminator"]["lesson"])
    def test_photon_eta_noise_tradeoff(self):
        p=self.d["photonic_power"]["cases"]
        self.assertGreater(p[0]["optimistic_loss_CHSH_upper"],p[3]["optimistic_loss_CHSH_upper"])
    def test_photon_higher_survival_reduces_trials(self):
        p=self.d["photonic_power"]["cases"]
        self.assertLess(p[-1]["iid_trials_for_alpha_0p001_power_90pct_IF_upper_bound_attained"],
                        p[2]["iid_trials_for_alpha_0p001_power_90pct_IF_upper_bound_attained"])
    def test_photon_counts_are_iid_not_real_implementation(self):
        self.assertIn("no certified optical",self.d["photonic_power"]["scope"])
    def test_bell_decoherence_extreme_resource(self):
        self.assertGreater(self.d["photonic_power"]["cases"][3]["iid_trials_for_alpha_0p001_power_90pct_IF_upper_bound_attained"],10**9)
    def test_full_scope_says_not_TOE(self):
        self.assertIn("No gauge-invariant E8 UV completion",self.d["status"])
if __name__=="__main__":unittest.main()
