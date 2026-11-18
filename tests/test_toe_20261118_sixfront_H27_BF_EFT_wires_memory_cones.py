"""Six independent post-November TOE fronts: exact regression gates.

Avoid calling these mathematical/conditional checks a physical G2, E6
unification, M-theory, photonic or spacetime realization.
"""
import sys,unittest,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_H27_Fourier_minimal7_E6_tensor_embedding as H
import toe_20261118_BF_cusp_coupled_negative_index_tower as B
import toe_20261118_two_wire_H27_flat_bundle_index_three as T
import toe_20261118_E6_sextic_EFT_three_time_confidence as E
import toe_20261118_W33_two_cover_common_cone_obstruction as C
import toe_20261118_three_time_096_depol_pairwise_classical_proof as Q

class AdvancedPhysicalFronts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.h=H.run()
        cls.b=B.run()
        cls.t=T.run()
        cls.e=E.run()
        cls.c=C.run()
        cls.q=Q.run()

    def test_H27_all_729_group_products(self):
        self.assertEqual(self.h["native_H27_order"],27)
        self.assertTrue(self.h["native_group_law_all_729_pairs_verified"])

    def test_H27_Fourier_is_a_unitary(self):
        self.assertEqual(self.h["Fourier_unitary_shape"],[27,27])
        self.assertLess(self.h["Fourier_unitarity_max_residual"],1e-12)

    def test_H27_Fourier_equivariant_all_27(self):
        self.assertLess(self.h["Fourier_all27_equivariance_max_residual"],1e-12)

    def test_E6_tensored_ancilla_minimal_7(self):
        self.assertEqual(self.h["tensor_ancilla_minimum_complex_dimension"],7)
        self.assertEqual(self.h["target_tensor_dimension"],189)
        self.assertTrue(self.h["target_contains_equivariant_regular27_isometry"])

    def test_E6_tensored_ancilla_correct_irrep_census(self):
        n=self.h["target_irrep_multiplicity_census"]
        self.assertEqual([n[str(a)+str(b)] for a in range(3) for b in range(3)], [9]*9)
        self.assertEqual((n["omega"],n["omega2"]),(9,27))

    def test_BF_corrections_robust_open_lambda_window(self):
        rows=self.b["rows"]
        for q in rows:
            lo,hi=q["BF_lambda_open_interval"]
            self.assertTrue(0<=lo<hi<=12)
            self.assertGreaterEqual(q["robust_oriented_winding_count"],0)

    def test_BF_extent_grows_sqrt_height(self):
        rows=[x for x in self.b["rows"] if x["correction_budget"]==2.2]
        self.assertEqual(len(rows),3)
        self.assertTrue(rows[0]["robust_oriented_winding_count"]<
                        rows[1]["robust_oriented_winding_count"]<
                        rows[2]["robust_oriented_winding_count"])

    def test_BF_uniform_coupled_stress(self):
        a=self.b["finite_mixing_stress"]
        self.assertGreater(a["guaranteed_robust_oriented_mode_count"],0)
        for trial in a["trials"]:
            self.assertGreaterEqual(trial["n_below_BF"],
                                    a["guaranteed_robust_oriented_mode_count"])
            self.assertLess(trial["max_negative_subspace_eigenvalue"],0)

    def test_two_wire_H27_fundamental_group_gate(self):
        self.assertEqual(self.t["full_H27_flat_holonomy_generated_elements"],27)
        self.assertEqual(self.t["holonomy_representation_dimension"],3)
        self.assertIn("F2",self.t["two_component_unlink_exterior_pi1"])

    def test_cyclic_lens_no_full_H27_holonomy(self):
        self.assertIn("trivial",self.t["lens_L41_pi1"])
        self.assertIn("cannot surject",self.t["single_core_wire_pi1"])

    def test_two_wire_one_sphere_net_index_three(self):
        self.assertEqual(self.t["single_sphere_puncture_relative_betti"],[0,6,3,0])
        self.assertEqual(self.t["one_spherical_defect_rank3_net_index"],3)

    def test_twisted_two_wire_retains_vectorlike_modes(self):
        self.assertEqual(self.t["unavoidable_rank3_vectorlike_pair_count_in_this_CW_model"],3)
        self.assertEqual(self.t["base_H27_rank3_local_system_betti"],[0,3,3,0])

    def test_E6_three_singlet_gauge_ring_is_one_invariant(self):
        a=self.e["E6"]
        self.assertEqual(a["exponents_tested_to_12"],[(j,j,j) for j in range(13)])

    def test_E6_sextic_vacuum_cutoff_control(self):
        a=self.e["E6"]
        self.assertIn("=1",a["natural_O1_example"])
        self.assertEqual(a["suppressed_field_requires_hierarchy"][2]["required_abs_lambda_over_kappa"],0.0020000000000000005)

    def test_E6_I3_correction_changes_stationary_branch(self):
        a=self.e["E6"]
        self.assertEqual(a["higher_order_sensitivity"][-1]["real_nonnegative_stationary_u"],[])
        self.assertAlmostEqual(a["higher_order_sensitivity"][-1]["higher_I3_derivative_at_old_vacuum"],.3)

    def test_memory_pairwise_classical_at_096(self):
        a=self.e["three_time_Beyer_protocol"]["examples"][2]
        self.assertGreater(a["p"],a["pcritical"])
        self.assertLess(a["W3_axis"],-.33)

    def test_memory_designpoint_99pct_bound(self):
        a=self.e["three_time_Beyer_protocol"]["examples"][2]["sample_design"]
        self.assertEqual(a["accepted_trials_per_setting"],3859)
        self.assertEqual(a["total_accepted_trials_three_settings"],11577)
        self.assertLess(a["design_point_upper_witness"],0)

    def test_memory_noise_tradeoff_nontrivial(self):
        examples=self.e["three_time_Beyer_protocol"]["examples"]
        self.assertTrue(all(x["max_equal_visibility_threshold"]>0 for x in examples))
        self.assertLess(examples[2]["max_equal_visibility_threshold"],examples[0]["max_equal_visibility_threshold"])

    def test_W33_two_cover_nonproportional_cones(self):
        a=self.c
        self.assertGreater(a["nonproportional_Frobenius_residual"],.001)
        mn,mx=a["old_to_optimized_relative_velocity_range_fixed_deck_basis"]
        self.assertLess(mn,1)
        self.assertGreater(mx,1)

    def test_W33_optimum_is_more_isotropic(self):
        self.assertLess(self.c["optimized_within_species_spatial_speed_anisotropy"],
                        self.c["old_within_species_spatial_speed_anisotropy"])
        self.assertAlmostEqual(self.c["optimized_within_species_spatial_speed_anisotropy"],math.sqrt(83/80))


    def test_noisy_three_time_096_pairwise_explicit_CPTP(self):
        self.assertTrue(self.q["all_conditional_branch_maps_CPTP"])
        self.assertLess(max(self.q["pairwise_full_Choi_errors"]),1e-12)

    def test_noisy_three_time_096_witness_is_strongly_negative(self):
        self.assertLess(self.q["genuine_three_time_fixed_axes_W3"],-.33)
        self.assertGreater(self.q["p"],self.q["pairwise_classical_threshold"])

    def test_noisy_three_time_E2E3_eight_random_unitary_records(self):
        self.assertEqual(self.q["classical_record_branch_counts"]["E2_noisy_to_E3_noisy"],8)
        self.assertAlmostEqual(self.q["measured_design_expectations"]["second_protected_z"],.95)

if __name__=="__main__":unittest.main()
