"""Independent numerical and algebraic tests for five TOE research fronts v4."""
import pathlib
import sys
import unittest
import numpy as np
from scipy.special import ndtr

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_physics_five_frontiers_v4 as f
import toe_20261119_physics_full_covariance_uv_operational as previous


class FivePhysicalFrontiersV4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all=f.produce()
        cls.r=cls.all["frontiers"]

    def test_complete_adjoint_beta_equal_GUT_shifts(self):
        g=self.r["complete_2x24F_fixed_benchmark_threshold_scan"]
        np.testing.assert_allclose(g["complete_24F_one_loop_beta"],
                                   [10/3,10/3,10/3])
        self.assertEqual(len(g["diagonal_two_24F_results"]),4)

    def test_adjoint_Clebsch_relation_under_sign_options(self):
        g=self.r["complete_2x24F_fixed_benchmark_threshold_scan"]
        mt=g["fixed_old_masses"]["triplet_1_GeV"]
        mo=g["fixed_old_masses"]["octet_1_GeV"]
        for x in g["diagonal_two_24F_results"]:
            sign=x["signed_octet_triplet_relative_signs"][0]
            self.assertAlmostEqual(x["X_fermion_masses_GeV"][0],
                abs(mt+sign*mo)/2,delta=1e-4)

    def test_renormalizable_two_adjoint_scan_does_not_restore_old_crossing(self):
        g=self.r["complete_2x24F_fixed_benchmark_threshold_scan"]
        self.assertGreater(g["best_mismatch_norm"],7)
        for sol in g["diagonal_two_24F_results"]:
            self.assertGreater(sol["Euclidean_inverse_alpha_mismatch_norm"],7)
            self.assertGreater(sol["best_second_triplet_GeV"],f.MZ)
            self.assertLessEqual(sol["best_second_octet_GeV"],2e16)
            self.assertAlmostEqual(
                np.linalg.norm(sol["inverse_alpha_differences"]),
                sol["Euclidean_inverse_alpha_mismatch_norm"])

    def test_adjoint_full_components_and_invalid_low_X_guard(self):
        actual,x=f._adjoint_couplings(np.log10(2e7),np.log10(1e5),
                                      np.log10(2e16),1,1)
        self.assertEqual(len(actual),2)
        self.assertEqual(len(x),2)
        self.assertTrue(np.all(x>f.MZ))
        invalid,_=f._adjoint_couplings(1,2,np.log10(2e16),1,1)
        self.assertGreater(np.linalg.norm(invalid),100)

    def test_neutrino_takagi_reconstruction_for_five_angles(self):
        n=self.r["typeIII_hidden_flavor_and_nonunitarity"]
        self.assertEqual(len(n["rows"]),5)
        self.assertLess(max(row["light_mass_reconstruction_error_GeV"]
                     for row in n["rows"]),1e-22)

    def test_neutrino_trace_lower_bound_and_exponential_scale(self):
        n=self.r["typeIII_hidden_flavor_and_nonunitarity"]
        baseline=n["exact_trace_nonunitarity_lower_bound"]
        self.assertGreater(baseline,0)
        for row in n["rows"]:
            self.assertAlmostEqual(
               row["Tr_theta_theta_dagger"]/baseline,
               np.cosh(2*row["Im_Casas_Ibarra_angle"]),places=10)

    def test_neutrino_FCNC_offdiagonal_estimate_remains_tiny(self):
        n=self.r["typeIII_hidden_flavor_and_nonunitarity"]
        self.assertLess(n["rows"][0]["nonunitarity_e_mu_abs"],1e-17)
        self.assertLess(n["rows"][-1]["nonunitarity_e_mu_abs"],1e-14)
        self.assertGreater(n["rows"][-1]["nonunitarity_e_mu_abs"],
                           n["rows"][0]["nonunitarity_e_mu_abs"])

    def test_Higgs_sensitivity_grows_with_hidden_angle(self):
        n=self.r["typeIII_hidden_flavor_and_nonunitarity"]
        rows=n["rows"]
        self.assertGreater(rows[-1]["reference_higgs_sensitivity_over_mh2"],1000)
        for i in range(1,len(rows)):
            self.assertGreater(rows[i]["reference_higgs_sensitivity_over_mh2"],
                               rows[i-1]["reference_higgs_sensitivity_over_mh2"])

    def test_nonlocal_exponential_suppression_forces_KL_violation(self):
        g=self.r["nonlocal_form_factor_KL_positivity_gate"]
        x=np.array(g["dimensionless_Euclidean_q_over_M2"])
        y=np.array(g["exponential_form_factor_q_times_propagator_over_residue"])
        np.testing.assert_allclose(y,np.exp(-x),rtol=1e-13)
        self.assertTrue(np.all(y<1))
        np.testing.assert_allclose(g["strict_positivity_violations"],1-y)

    def test_healthy_spectral_comparator_preserves_positive_bound(self):
        g=self.r["nonlocal_form_factor_KL_positivity_gate"]
        qs=np.array(g["dimensionless_Euclidean_q_over_M2"])
        np.testing.assert_allclose(
            g["positive_extra_massive_state_comparator"],1+.35*qs/(qs+4))
        self.assertTrue(min(g["positive_extra_massive_state_comparator"])>=1)

    def test_DESI_source_covariance_is_positive(self):
        z,y,kind,C=f._bao_arrays()
        self.assertEqual(C.shape,(13,13))
        self.assertGreater(np.linalg.eigvalsh(C).min(),0)
        self.assertAlmostEqual(y[4],19.45534918)

    def test_DESI_q_marginal_integral_positive_and_normalized(self):
        z,y,kind,C=f._bao_arrays()
        theta=np.array([[.3,-1,0],[.35,-.84,-.53]],float)
        L=f._q_marginal_likelihood(theta,z,y,kind,C)
        self.assertEqual(len(L),2)
        self.assertTrue(np.all(np.isfinite(L)))
        self.assertTrue(np.all(L>0))
        self.assertTrue(np.all(L<1))

    def test_DESI_QMC_four_seed_finite_evidences(self):
        d=self.r["DESI_DR2_bayesian_prior_sensitivity"]
        self.assertEqual(len(d["results"]),3)
        self.assertGreater(d["LCDM_evidence_rel_common_normalization"],0)
        for result in d["results"]:
            self.assertEqual(result["Sobol_points_per_scramble"],8192)
            self.assertEqual(len(result["evidence_seed_samples"]),4)
            self.assertLess(result["estimated_log_evidence_standard_error"],.10)

    def test_DESI_prior_sensitive_Bayesian_model_selection(self):
        d=self.r["DESI_DR2_bayesian_prior_sensitivity"]
        logs=[row["log_Bayes_factor_vs_LCDM"] for row in d["results"]]
        self.assertLess(logs[0],0)
        self.assertLess(logs[1],0)
        self.assertLess(logs[2],0)
        self.assertLess(logs[2],logs[0])

    def test_nonphantom_CPL_prior_is_not_same_as_full_physical_scalar(self):
        d=self.r["DESI_DR2_bayesian_prior_sensitivity"]
        n=next(x for x in d["results"]
               if x["name"]=="phantom_free_canonical_CPL")
        self.assertGreaterEqual(n["prior_w0"][0],-1)
        self.assertGreaterEqual(n["prior_wa"][0],0)
        self.assertTrue(d["only_BAO"])

    def test_two_photon_dualrail_state_is_entangled(self):
        p=self.r["two_copy_photon_SSR_activation"]
        psi=np.array(p["conditional_2qubit_dualrail_wavefunction_real"])
        self.assertAlmostEqual(np.linalg.norm(psi),1)
        self.assertAlmostEqual(abs(np.linalg.det(psi)),.5)
        self.assertAlmostEqual(p["unconditional_local_number_herald_probability"],.5)

    def test_event_ready_photon_CHSH_requires_two_copies(self):
        p=self.r["two_copy_photon_SSR_activation"]
        E=np.array(p["correlation_matrix_E"])
        self.assertAlmostEqual(E[0,0]+E[0,1]+E[1,0]-E[1,1],2*np.sqrt(2))
        self.assertAlmostEqual(p["event_ready_ideal_CHSH"],2*np.sqrt(2))
        self.assertEqual(p["postselected_local_photon_numbers"],[1,1])

    def test_loss_resources_scale_with_two_photon_survival(self):
        p=self.r["two_copy_photon_SSR_activation"]
        for eta,accept in zip(p["ideal_two_photon_transmission_efficiency_cases"],
                               p["herald_probability_with_independent_transmission_loss"]):
            self.assertAlmostEqual(accept,.5*eta**2,places=14)

    def test_supplemental_event_ready_CHSH_finite_trial_bound(self):
        b=self.all["supplemental_event_ready_Bell_sample_resources"]
        p=b["ideal_CHSH_game_quantum_win_fraction"]
        self.assertAlmostEqual(p,np.cos(np.pi/8)**2)
        self.assertLessEqual(b["Hoeffding_upper_bound_at_target_N"],1e-6)
        self.assertGreater(b["minimum_ideal_valid_heralded_trials"],500)

    def test_supplemental_two_photon_source_emission_cost(self):
        b=self.all["supplemental_event_ready_Bell_sample_resources"]
        self.assertAlmostEqual(b["ideal_herald_success_probability"],.32)
        self.assertAlmostEqual(
          b["expected_source_pair_emissions_for_N"],
          b["minimum_ideal_valid_heralded_trials"]/.32)

    def test_not_a_fundamental_TOE(self):
        self.assertFalse(self.all["theory_of_everything_solved"])
        self.assertFalse(self.all["W33_used_as_physical_input"])
        self.assertTrue(all(v["status"]=="PASS" for v in self.r.values()))

if __name__=="__main__":
    unittest.main()
