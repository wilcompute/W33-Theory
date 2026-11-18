"""Regression checks of five independent W33-TOE threads:
AdS dimension/provenance, explicit H27->189, E8 H27 branching,
linked H27 unitary twist vs E6 Higgs, exact fixed-n photon stats.

Numerical isometries are representation mathematics, NOT experiments.
"""
import sys,unittest,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_AdS_dimension_BF_provenance_falsifier as BF
import toe_20261118_H27_explicit189_intertwiner_reynolds as H
import toe_20261118_H27_explicit_E8_248_embedding_charge_sectors as E8
import toe_20261118_linked_wire_chi_twist_Higgs_global_compatibility as W
import toe_20261118_exact_binomial_multitime_CI_photon_design as S

class DeepNewGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b=BF.run();cls.h=H.run();cls.e=E8.run()
        cls.w=W.run();cls.s=S.run()

    def test_AdS4_BF_is_minus_nine_over_four(self):
        self.assertEqual(self.b["true_scalar_BF_bounds"]["AdS4"],"-9/4")

    def test_AdS5_BF_is_minus_four(self):
        self.assertEqual(self.b["true_scalar_BF_bounds"]["AdS5"],"-4")
        self.assertEqual(self.b["original_correct_IIB_mode_dimension"],5)

    def test_formal_AdS4_window_not_physical_spectrum(self):
        self.assertIn("63/4",self.b["corrected_AdS4_formal_interval_at_c0"])
        self.assertTrue(next(z for z in self.b["cases"] if
                             z["AdS_dimension"]==4 and z["correction_budget"]==0)
                        ["exact_mass_formula_transferred_only_formally_to_different_D"])

    def test_mass_formula_minimum_and_provenance(self):
        self.assertEqual(self.b["dispersion_min_mass"],"-25/4")
        self.assertIn("TYPE IIB AdS5",self.b["source"])

    def test_formal_AdS4_and_AdS5_counts_not_conflated(self):
        rows=self.b["cases"]
        c={(x["AdS_dimension"],x["correction_budget"]):x
           ["oriented_unstable_horizontal_winding_count_at_y"] for x in rows}
        self.assertGreater(c[4,0],c[5,0])
        self.assertGreater(c[4,1],c[5,1])

    def test_H27_numeric_189x27_full_rank_isometry(self):
        self.assertEqual((self.h["source_dim"],self.h["target_dim"]),(27,189))
        self.assertLess(self.h["explicit_189x27_isometry_unitarity_max_error"],3e-12)

    def test_H27_numeric_189x27_all27_intertwiners(self):
        self.assertLess(self.h["explicit_intertwiner_all27_max_error"],3e-12)

    def test_H27_invariant_ancilla_destroys_information(self):
        self.assertEqual(self.h["invariant_ancilla_restricted_encoder_rank"],9)
        for p in self.h["encoded_basis_states_ancilla_sector_probabilities"]:
            self.assertAlmostEqual(p,1/3,places=11)

    def test_E8_exact_branching_decomposition(self):
        self.assertEqual(self.e["E8_decomposition_dimensions"],[78,8,81,81])
        self.assertEqual(sum(self.e["E8_decomposition_dimensions"]),248)

    def test_E8_regular_H27_248_intertwiner(self):
        self.assertEqual(self.e["concrete_Fourier_embedding_shape"],[248,27])
        self.assertLess(self.e["isometry_error"],1e-12)
        self.assertLess(self.e["all27_intertwining_max_error"],1e-12)

    def test_E8_H27_character_census(self):
        a=self.e["H27_character_multiplicities"]
        self.assertEqual((a["trivial_1D"],a["each_of_eight_nontrivial_1D"],
                          a["rho_omega"],a["rho_omega2"]),(78,1,27,27))

    def test_E8_not_full_E6_matter_intertwiner(self):
        self.assertFalse(self.e["physical_E6_gauge_equivariance"])
        self.assertTrue(self.e["impossible_E6_singlet_regular27_embedding_under_fixed_branching"])
        self.assertTrue(self.e["native_E6_adjoint16_minus3_is_SU3_family_singlet"])

    def test_chi_parity_higgs_A_B_odd_C_even(self):
        self.assertEqual(self.w["global_Chi_pi_holonomy_singlet_eigenvalues"],[-1,-1,1])

    def test_higgs_rank_under_single_chi_twist(self):
        self.assertEqual(self.w["full_D_term_charge_rank"],2)
        self.assertEqual(self.w["Chi_parity_invariant_D_term_charge_rank"],1)
        self.assertFalse(self.w["Chi_parity_invariant_Dflat_nonzero_solution_with_zero_FI"])

    def test_higgs_global_loop_gradient_penalty(self):
        self.assertIn("pi^2 / ell^2",self.w["odd_singlet_loop_covariant_laplacian_gap"])
        self.assertEqual(self.w["W7_SU5_singlet_eigenvalues"],[1,1,1])

    def test_finite_C2_flavor_is_not_automatically_chi_gauge(self):
        self.assertTrue(self.w["independent_unitary_C2_flavor_possible_without_acting_on_Higgs"])

    def test_exact_one_sided_99pct_CI(self):
        self.assertAlmostEqual(self.s["confidence"],.99)
        self.assertEqual(self.s["proposed_fixed_stopping_n_per_setting"],450)
        self.assertEqual(self.s["total_proposed_accepted_trials"],1350)

    def test_design_counts_and_upper_witness(self):
        p=self.s["proposed_design_point_observations"]
        self.assertEqual(p["success_counts"],[441,439,439])
        self.assertLess(p["corrected_upper_bound_W3"],-.02)

    def test_statistics_do_not_claim_experimental_power(self):
        self.assertTrue(self.s["is_design_point_only"])
        self.assertFalse(self.s["optional_stopping_not_allowed"] is False)
        self.assertFalse(self.s["statistical_power_not_computed"] is False)
        self.assertFalse(self.s["detector_and_heralding_bias_not_calibrated"] is False)

if __name__=="__main__":unittest.main()
