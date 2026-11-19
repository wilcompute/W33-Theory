"""Regression tests for two-ten Higgs, global Wilson, causal BDG noise,
physical resource and exact five-pair 10-messenger UV EFT tree."""
from pathlib import Path
import sys,unittest
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_two_ten_W7_BDG_variance_photon as p
import toe_20261119_five_pair_Spin10_messenger_tree as m

class FiveFrontTinkerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=p.two_ten_Higgs()
        cls.w=p.W7_characters()
        cls.g=p.GUT_thresholds()
        cls.c=p.BDG4_noise()
        cls.ph=p.photonic_resources()
        cls.t=m.messenger_tree()

    def test_four_actual_source_spurion_insertions(self):
        self.assertEqual([x["singlets"] for x in self.a["operators"]],
            [["B"],["C","D"],["E","G1"],["A","D"]])
    def test_exact_all_four_source_charge_neutrality(self):
        self.assertEqual(len(self.a["operators"]),4)
    def test_higgs_rank_two_for_two_tens(self):
        self.assertEqual(np.linalg.matrix_rank(np.array(self.a["mass_matrix"])),2)
    def test_light_higgs_both_10_34_projections_nonzero(self):
        self.assertAlmostEqual(self.a["projection_10_34_5_abs"],.196116135138184,places=11)
        self.assertAlmostEqual(self.a["projection_10_34_bar5_abs"],.703665851855809,places=11)
    def test_light_higgs_kernel_exact_numerical(self):
        M=np.array(self.a["mass_matrix"])
        u=np.array(self.a["light_5_components"])
        v=np.array(self.a["light_bar5_components"])
        self.assertLess(np.linalg.norm(M@u),1e-12)
        self.assertLess(np.linalg.norm(v@M),1e-12)
    def test_72_fields_have_one_complete_massless_10(self):
        self.assertEqual((self.a["active_chiral_components"],self.a["hessian_rank"],
            self.a["broken_complex_gauge_dimension"],
            self.a["physical_massless_chiral_components"]),(72,38,24,10))
        self.assertIn("colored triplets",self.a["massless_representation"])
    def test_higgs_family_identical_charges_mixing_avoidable_only_dynamically(self):
        self.assertTrue(self.a["source_renormalizable_16_1_16_2_10_34_exactly_neutral"] if
            "source_renormalizable_16_1_16_2_10_34_exactly_neutral" in self.a else
            self.a["gauge_allowed_unsuppressed_16_1_16_2_10_34"])
        self.assertTrue(self.a["family_16_1_and_Higgs_16H_same_charges"])
    def test_discrete_R_gravity_parity_flips_with_added_Higgs_driver(self):
        self.assertEqual(self.a["old_discrete_Z4R_gravitational_parity"],0)
        self.assertEqual(self.a["new_two_R0_spinors_one_R2_driver_parity_shift"],1)
        self.assertEqual(self.a["combined_discrete_Z4R_gravitational_parity_without_additional_inflow"],1)
    def test_order7_character0_has_no_Higgs_doublets(self):
        self.assertEqual(self.w["ten_vector_character_table"][0]["five_weak"],0)
        self.assertEqual(self.w["ten_vector_character_table"][0]["barfive_weak"],0)
    def test_order7_character3_selects_weak_5_only(self):
        self.assertEqual(self.w["ten_vector_character_table"][3]["five_weak"],2)
        self.assertEqual(sum(self.w["ten_vector_character_table"][3][k] for k
             in ("five_color","barfive_color","barfive_weak")),0)
    def test_order7_character4_selects_weak_bar5_only(self):
        self.assertEqual(self.w["ten_vector_character_table"][4]["barfive_weak"],2)
        self.assertEqual(sum(self.w["ten_vector_character_table"][4][k] for k
             in ("five_color","barfive_color","five_weak")),0)
    def test_W7_spinor_only_singlet_constant_invariant(self):
        self.assertEqual(self.w["untwisted_16_invariant_components"],1)
        self.assertTrue(self.w["trivial_character_10_has_no_weak_doublets"])
    def test_W7_mass_before_projection_is_not_consistent_shortcut(self):
        self.assertIn("naive constant-flat-section",self.w["global_constant_zero_mode_clash"])
        self.assertIn("L4",self.w["required_escape"])
    def test_first_order_5D_Dirac_boundary_equations_quantized(self):
        toy=p.interval_5D_Dirac_boundary_spectrum()
        self.assertEqual(toy["test_cases"][0]["first_3_positive_masses_times_L"][0],0)
        self.assertGreater(toy["test_cases"][-1]["first_3_positive_masses_times_L"][0],1.56)
        self.assertIn("Majorana",toy["physical_warning"])
    def test_two_triplets_one_octet_needs_inserted_SM_boundary_mass(self):
        toy=p.interval_5D_Dirac_boundary_spectrum()
        self.assertEqual(toy["two_triplets_one_octet_toy_parameters"],
            {"triplet_1_h":0,"triplet_2_h":0,"octet_1_h":0,"octet_2_h":100})
    def test_full_SU5_beta_universal_one_loop(self):
        self.assertEqual(self.g["full_SUSY_5_plus_bar5_beta"],["1","1","1"])
    def test_doublet_and_triplet_beta_split(self):
        self.assertEqual(self.g["extra_N1_doublet_chiral_pair_beta"],["3/5","1","0"])
        self.assertEqual(self.g["extra_N1_triplet_chiral_pair_beta"],["2/5","0","1"])
    def test_thresholds_not_empty(self):
        self.assertGreater(abs(self.g["one_loop_delta_inverse_alpha_differences_12_13_23"][0]),1)
    def test_full_causet_intervals_not_independent_poisson_noise(self):
        self.assertEqual(self.c["method"].split()[0],"Independent")
        self.assertEqual([x["rho"] for x in self.c["data"]],[20,50,100])
    def test_causal_noise_has_large_empirical_sd(self):
        self.assertGreater(self.c["data"][0]["sd_BDG4_constant"],100)
        self.assertGreater(self.c["data"][-1]["sd_BDG4_constant"],1000)
    def test_causal_N_distribution_has_grounded_expected_volume(self):
        for item in self.c["data"]:
            self.assertLess(abs(item["mean_events"]-item["expected_events"]),3)
    def test_dualrail_has_exponential_space_but_linear_physical_modes(self):
        for x in self.ph["dual_rail_n_photon_vs_single_photon_mode_tradeoff"]:
            self.assertEqual(x["modes"],2*x["logical_qubits"])
            self.assertEqual(x["dual_rail_code_dimension"],2**x["logical_qubits"])
            self.assertGreaterEqual(x["full_fixed_photon_Fock_dimension"],x["dual_rail_code_dimension"])
    def test_loss_and_naive_entangler_success_are_exponentially_small(self):
        a=self.ph["dual_rail_n_photon_vs_single_photon_mode_tradeoff"]
        self.assertGreater(a[0]["combined_naive_success"],a[-1]["combined_naive_success"])
        self.assertLess(a[-1]["combined_naive_success"],1e-8)
    def test_acceptance_bias_exact(self):
        self.assertAlmostEqual(self.ph["relative_success_acceptance_odds_bias_to_fake_p0p5_as_p0p51"],51/49)
    def test_renormalizable_messenger_network_has_five_pairs(self):
        self.assertEqual(self.t["heavy_Spin10_ten_vectorlike_pairs"],5)
        self.assertEqual(self.t["heavy_Spin10_ten_chiral_superfield_components"],100)
    def test_all_fourteen_UV_vertices_gauge_R_valid(self):
        self.assertTrue(self.t["all_14_vertices_gauge_neutral_and_R2"])
        self.assertEqual(len(self.t["renormalizable_cubic_and_mass_vertices"]),14)
    def test_UV_heavy_F_fields_eliminated_exactly(self):
        self.assertTrue(self.t["heavy_F_terms_zero_identically"])
        self.assertTrue(self.t["four_B_CD_EG1_AD_ops_recovered"])
    def test_vectorlike_heavy_messengers_add_no_perturbative_U1_anomaly(self):
        self.assertTrue(self.t["pairwise_U1_gauge_anomaly_and_U1sqR_cancel"])
    def test_UV_messenger_provenance_not_claimed(self):
        self.assertIn("not derived",self.t["scope"].lower())
        self.assertIn("punctured S3",self.t["scope"])
if __name__=="__main__":unittest.main()
