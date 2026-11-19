"""Focused TOE physical-sieve regression: independent of W33 mathematics."""
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_toe_physical_sieve_followup as toe

class PhysicalSieveFollowUp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ch=toe.chirality_global()
        cls.uv=toe.gauge_vacuum_and_flavor()
        cls.gravity=toe.gravity_constraint_gate()
        cls.memory=toe.quantum_memory_gate()
        cls.rge=toe.gauge_coupling_predictivity()
        cls.neutrino=toe.neutrino_rank_interpretation()

    def test_compact_exact_harmonic_no_go(self):
        self.assertEqual(self.ch["discrete_harmonic_zero_modes_scalar"],1)
        self.assertEqual(self.ch["discrete_exact_gradient_rank"],26)
        self.assertLess(self.ch["discrete_integration_by_parts_error"],1e-10)
        self.assertGreater(self.ch["discrete_smallest_positive_laplacian_eigenvalue"],.1)

    def test_nonexact_torus_harmonic_form_exists(self):
        self.assertEqual(self.ch["nonexact_cycle_divergence_norm"],0.)
        self.assertIn("not a gradient",self.ch["nonexact_harmonic_1_cycle"])

    def test_negative_three_local_index_requires_compensation(self):
        self.assertEqual(self.ch["f1_local_indices"],[-1,-1,-1])
        self.assertEqual(self.ch["local_index_sum"],-3)
        self.assertEqual(self.ch["closed_oriented_3manifold_euler"],0)

    def test_full_U9_flavor_cannot_select_SIC(self):
        self.assertLess(self.uv["U9_orbit_map_residual"],1e-12)
        self.assertLess(self.uv["U9_unitary_residual"],1e-12)
        self.assertEqual(self.uv["repeated_basis_pair_overlap_sq_values_and_counts"],{"0":27,"4":9})
        self.assertAlmostEqual(self.uv["SIC_pair_overlap_sq"][0],1.0)
        self.assertAlmostEqual(self.uv["SIC_pair_overlap_sq"][1],1.0)

    def test_SU4_parent_AF_but_baryon_irrelevant(self):
        self.assertEqual(self.uv["b0_one_loop"],2)
        self.assertEqual(self.uv["IR_SCFT_scaling_dimensions"]["Q"],"9/10")
        self.assertEqual(self.uv["IR_SCFT_scaling_dimensions"]["baryon_Q4"],"18/5")
        self.assertEqual(self.uv["IR_SCFT_scaling_dimensions"]["singlet_times_baryon_if_free_singlet"],"23/5")

    def test_curved_metric_matter_bracket_converges(self):
        d=self.gravity["discrete_bracket_relative_residuals"]
        self.assertEqual([x["N"] for x in d],[32,64,128,256])
        self.assertLess(d[-1]["spectral"],1e-10)
        self.assertTrue(all(d[j]["centered"]>d[j+1]["centered"] for j in range(3)))

    def test_dynamical_metric_without_gravity_H_not_closed(self):
        self.assertGreater(self.gravity["sample_nonzero_Dg_norm"],1)
        self.assertGreater(self.gravity["spectral_high_mode_alias_relative_error"],.01)
        self.assertIn("cannot",self.gravity["no_go"])

    def test_memory_all_trial_efficiency_threshold(self):
        self.assertAlmostEqual(self.memory["event_ready_detection_efficiency_threshold"],15/37,places=10)
        rec=self.memory["efficiency_shot_sufficient_bounds"]
        self.assertFalse(rec[1]["beats_EB_bound"])
        self.assertTrue(rec[2]["beats_EB_bound"])
        self.assertGreater(rec[4]["sufficient_Hoeffding_trials_if_rate_exact"],100)

    def test_quantum_memory_mixture_inference_is_conditional(self):
        self.assertGreater(self.memory["minimum_quantum_branch_fraction_in_mixture_at_eta_0p5"],.11)
        self.assertLess(self.memory["minimum_quantum_branch_fraction_in_mixture_at_eta_0p5"],.12)
        self.assertEqual(self.memory["single_photon_mode_examples"][-1]["single_photon_modes"],2**40)

    def test_complete_SU5_multiplets_cannot_fix_one_loop_mismatch(self):
        self.assertEqual(self.rge["fivebar_chiral_beta_shift"],["1/2"]*3)
        self.assertEqual(self.rge["ten_chiral_beta_shift"],["3/2"]*3)
        self.assertEqual(self.rge["vectorlike_5plus5bar_shift"],["1"]*3)
        self.assertEqual(self.rge["vectorlike_10plus10bar_shift"],["3"]*3)

    def test_MSSM_simple_threshold_requires_below_Z_pole(self):
        self.assertLess(self.rge["one_step_SM_below_and_MSSM_above_fitted_threshold_GeV"],91.1876)
        self.assertGreater(self.rge["formal_exact_unification_GeV"],1e16)
        self.assertAlmostEqual(self.rge["one_step_SM_below_and_MSSM_above_fitted_threshold_GeV"],68.32673775756315,places=7)

    def test_RG_alpha_s_sensitivity(self):
        r=self.rge["one_loop_strong_coupling_sensitivity"]
        self.assertEqual(len(r),3)
        self.assertGreater(r[0]["formal_exact_threshold_GeV"],r[1]["formal_exact_threshold_GeV"])
        self.assertGreater(r[1]["formal_exact_threshold_GeV"],r[2]["formal_exact_threshold_GeV"])

    def test_two_neutrino_seesaw_rank_is_physical_option(self):
        self.assertEqual(self.neutrino["minimal_two_RH_neutrino_seesaw_rank_bound"],2)
        self.assertEqual(self.neutrino["random_two_RH_seesaw_samples"],30)
        self.assertAlmostEqual(self.neutrino["normal_ordering_massless_min_sum_eV"],.0587329368186,places=10)
        self.assertAlmostEqual(self.neutrino["inverted_ordering_massless_min_sum_eV"],.0996165766558,places=10)

if __name__=="__main__":unittest.main()
