"""Crossfront tests for 7D H27 quotient, spinor gap, degree-six
SIC-producing F-flat dynamics, projective Wilson compensation and
time-ordered GHZ emission. Checks exact conditional mathematics only."""
import unittest,sys,math,itertools
from pathlib import Path
import numpy as np
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"analysis"))
import toe_20261118_H27_S5T2_G2_sextic_center_sequential as T

class H27S5T2SexticSequential(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=T.run()
        cls.g=cls.r["H27_seven_dimensional_quotient"]
        cls.d=cls.r["ordinary_spin_Dirac_flat_gap"]
        cls.f=cls.r["H27_first_nontrivial_sextic_F_flat"]
        cls.w=cls.r["flat_Weyl_torus_compensation"]
        cls.q=cls.r["sequential_qutrit_four_gate_emitter"]

    def test_H27_group_law_residual(self):
        self.assertLess(self.g["h27_group_law_max_residual"],1e-12)
    def test_H27_group_associativity(self):
        for a,b,c in itertools.product(T.G,repeat=3):
            self.assertEqual(T.mul(T.mul(a,b),c),T.mul(a,T.mul(b,c)))
    def test_free_action_covers_all_nonidentity(self):
        self.assertEqual(self.g["free_action_test_nonidentity"],26)
        self.assertEqual(sum(self.g["fixed_point_exclusion_cases"].values()),26)
    def test_nontrivial_center_fixed_by_S5_no(self):
        self.assertEqual(self.g["fixed_point_exclusion_cases"]["central_S5"],2)
        for c in (1,2):
            self.assertGreater(min(abs(np.linalg.eigvals(T.rho((0,0,c)))-1)),1.0)
    def test_torus1_translation_cases(self):
        self.assertEqual(self.g["fixed_point_exclusion_cases"]["first_torus_translation"],18)
    def test_torus2_translation_cases(self):
        self.assertEqual(self.g["fixed_point_exclusion_cases"]["second_torus_translation"],6)
    def test_quotient_dimension_seven(self):
        self.assertEqual(self.g["real_dimension"],7)
    def test_quotient_smooth_action(self):
        self.assertTrue(self.g["free_smooth_action"])
    def test_quotient_spin_structure_possible(self):
        self.assertTrue(self.g["natural_spin_structure_exists"])
        self.assertTrue(self.g["quotient_orientable"])
    def test_quotient_rational_Betti(self):
        self.assertEqual(self.g["rational_Betti"],
            {"0":1,"1":2,"2":1,"5":1,"6":2,"7":1})
    def test_quotient_Euler_zero(self):
        self.assertEqual(sum((-1)**int(k)*v
            for k,v in self.g["rational_Betti"].items()),0)
    def test_quotient_b1_two(self):
        self.assertEqual(self.g["first_Betti"],2)
    def test_quotient_b3_zero(self):
        self.assertEqual(self.g["third_Betti"],0)
    def test_quotient_b4_zero(self):
        self.assertEqual(self.g["fourth_Betti"],0)
        self.assertTrue(self.g["no_nonzero_deRham_4form_flux_class"])
    def test_fundamental_group_extension_not_H27_itself(self):
        self.assertTrue(self.g["full_fundamental_group_infinite"])
        self.assertIn("Z^2",self.g["fundamental_group"])
    def test_H27_gauge_Wilson_allowed(self):
        self.assertTrue(self.g["h27_finite_flat_holonomy_possible"])
    def test_torsionfree_G2_b3_no_go(self):
        self.assertFalse(self.g["torsion_free_G2_possible"])
        self.assertIn("b3>=1",self.g["G2_obstruction1"])
    def test_torsionfree_G2_b1_two_no_go(self):
        self.assertIn("b1=2",self.g["G2_obstruction2"])
    def test_nearlyparallel_G2_no_go(self):
        self.assertFalse(self.g["nearly_parallel_G2_nonzero_tau_possible"])
    def test_product_not_positive_Einstein(self):
        self.assertIn("0 (two torus",self.g["actual_product_quotient_Ricci"])
    def test_product_scalar_positive(self):
        self.assertEqual(self.g["actual_product_quotient_scalar_curvature"],"20/R^2")
    def test_quotient_not_physical_TOE_background(self):
        self.assertIn("NOT a torsion-free",self.g["scope"])

    def test_sphere_spin_Dirac_known_spectrum(self):
        self.assertIn("k+5/2",self.d["sphere_spin_Dirac_spectrum"])
    def test_product_Dirac_square_sum(self):
        self.assertEqual(self.d["product_Dirac_square"],
                         "D_S5^2 + D_T2^2")
    def test_Dirac_gap_norm_R2_exact(self):
        self.assertEqual(self.d["exact_lower_bound_Dirac_squared_times_R2"],"25/4")
    def test_Dirac_gap_numeric_R2(self):
        self.assertAlmostEqual(self.d["smallest_spin_Dirac_square"],25/16,places=12)
    def test_Lichnerowicz_lower_bound(self):
        self.assertEqual(self.d["Lichnerowicz_curvature_term_times_R2"],"5")
    def test_exact_dirac_gap_stronger_than_Bochner(self):
        R=self.d["numeric_R"]
        self.assertGreater(self.d["smallest_spin_Dirac_square"],5/R**2)
    def test_flat_H27_twisted_no_massless(self):
        self.assertTrue(self.d["flat_unitary_gauge_twist_cannot_generate_ordinary_zero_modes"])
    def test_cover_torus_momenta_count(self):
        self.assertEqual(self.d["independently_enumerated_torus_momenta_count"],49)
    def test_Dirac_scope_not_ADE(self):
        self.assertIn("ADE charged",self.d["scope"])

    def test_degree_three_dim_two(self):
        self.assertEqual(self.f["H27_Molien_dimensions_degrees_0_to_12"]["3"],2)
    def test_degree_four_zero(self):
        self.assertEqual(self.f["H27_Molien_dimensions_degrees_0_to_12"]["4"],0)
    def test_degree_five_zero(self):
        self.assertEqual(self.f["H27_Molien_dimensions_degrees_0_to_12"]["5"],0)
    def test_degree_six_dim_four(self):
        self.assertEqual(self.f["H27_Molien_dimensions_degrees_0_to_12"]["6"],4)
    def test_degree_nine_dim_seven(self):
        self.assertEqual(self.f["H27_Molien_dimensions_degrees_0_to_12"]["9"],7)
    def test_degree_twelve_dim_eleven(self):
        self.assertEqual(self.f["H27_Molien_dimensions_degrees_0_to_12"]["12"],11)
    def test_sextic_orbits_four(self):
        self.assertEqual(len(self.f["degree6_invariant_basis_exponent_orbits"]),4)
    def test_sextic_orbits_explicit_sizes(self):
        self.assertEqual(sorted(len(x) for x in
            self.f["degree6_invariant_basis_exponent_orbits"]),[1,3,3,3])
    def test_sextic_first_allowed_after_cubic(self):
        self.assertEqual(self.f["lowest_new_holomorphic_degree_beyond_cubic"],6)
    def test_F_gradient_symbolic(self):
        x,y,z=s.symbols("x y z")
        for i,var in enumerate((x,y,z)):
            parsed=s.sympify(self.f["actual_F_terms"][i])
            self.assertEqual(s.expand(parsed-3*var**2*(1-var**3)),0)
    def test_F_flat_64_stationary(self):
        self.assertEqual(self.f["number_of_complex_stationary_points"],64)
    def test_F_flat_support_counts(self):
        self.assertEqual(self.f["stationary_support_class_counts"],
                         {"0":1,"1":9,"2":27,"3":27})
    def test_F_flat_two_nonzero_27_vectors(self):
        self.assertEqual(self.f["independent_nonstabilizer_VEVs_at_support_two"],27)
    def test_F_flat_nonstabilizer_witness(self):
        self.assertEqual(self.f["nonstabilizer_F_flat_solution"],"[1,1,0]")
        self.assertTrue(self.f["qutrit_nonstabilizer_magic_state"])
    def test_fidelity_to_any_stabilizer_two_thirds(self):
        self.assertAlmostEqual(self.f["maximum_overlap_squared_with_12_stabilizer_states"],
                               2/3,places=12)
    def test_nine_projective_SIC_rays(self):
        self.assertEqual(self.f["number_of_projective_support_two_SIC_rays"],9)
    def test_SIC_equangular_1_over_four(self):
        self.assertEqual(self.f["SIC_all_distinct_pair_overlap_squared"],"1/4")
        self.assertLess(self.f["SIC_Gram_max_abs_residual"],1e-12)
    def test_SIC_POVM_completeness(self):
        self.assertLess(self.f["SIC_POVM_max_abs_residual"],1e-12)
    def test_SIC_H27_orbit_transitive(self):
        self.assertTrue(self.f["SIC_transitive_H27_orbit_verified"])
    def test_not_specific_Hesse_pencil_SIC_basepoint(self):
        self.assertTrue(self.f["not_prior_specific_Hesse_pencil_basepoint_SIC"])
        self.assertEqual(self.f["Hesse_doublet_norm_squared_on_this_SIC"],"1/6")
    def test_no_E8_flavon_completion_claim(self):
        self.assertIn("NOT be an E8-adjoint",self.f["limitation"])

    def test_torus_noncommuting_X_Z(self):
        self.assertFalse(self.w["single_triplet_X_Z_commute"])
        self.assertTrue(self.w["cannot_be_simultaneous_flat_wilson_holonomies_of_pi1_T2"])
    def test_Weyl_relation(self):
        self.assertLess(np.max(abs(T.Z@T.X-T.omega*T.X@T.Z)),1e-12)
    def test_countertwist_9D_commutes(self):
        self.assertTrue(self.w["compensated_U_V_commute"])
        self.assertLess(self.w["compensated_commutator_max_abs"],1e-12)
    def test_countertwist_character_regular(self):
        self.assertTrue(self.w["compensated_9D_rep_is_regular_of_Z3_squared"])
        traces=self.w["compensated_character_traces"]
        self.assertEqual(traces["0,0"],[9,0])
        self.assertEqual(sum(x==[0,0] for x in traces.values()),8)
    def test_H27_holonomy_nonabelian_pi1_allowed(self):
        self.assertTrue(self.w["H27_nonabelian_pi1_quotient_allows_noncommuting_holonomy"])
    def test_not_complete_E6_lift(self):
        self.assertIn("NOT an actual E6",self.w["limitation"])

    def test_sequential_gate_count_four(self):
        self.assertEqual(self.q["two_qutrit_clifford_gate_count"],4)
    def test_sequential_gate_81unitarity(self):
        for c,t,sign in ((0,1,1),(0,2,1),(0,3,1),(3,0,-1)):
            U=T.SUM(c,t,sign)
            self.assertLess(np.max(abs(U@U.conj().T-np.eye(81))),1e-12)
    def test_sequential_outputs_old_not_touched(self):
        self.assertTrue(self.q["earlier_emitted_outputs_not_touched_again"])
    def test_sequential_environment_uncomputed(self):
        self.assertEqual(self.q["final_environment_state"],"|0>")
    def test_sequential_GHZ_coherent_exact(self):
        self.assertEqual(self.q["coherent_density_max_error"],0)
    def test_sequential_dephase_classical_exact(self):
        self.assertTrue(self.q["environment_dephased_gives_exact_classical_GHZ_diagonal"])
        self.assertLess(self.q["classical_density_max_error"],1e-12)
    def test_sequential_pair_marginals_indistinguishable(self):
        self.assertLess(self.q["pairwise_marginal_max_error"],1e-12)
    def test_sequential_triple_X_coherence(self):
        self.assertEqual(self.q["triple_X_expectation_coherent"],1)
        self.assertEqual(self.q["triple_X_expectation_classical"],0)
    def test_sequential_noisy_visibility_fidelity(self):
        self.assertAlmostEqual(self.q["GHZ_fidelity"],5/6,places=12)
    def test_sequential_finite_shot_600(self):
        self.assertEqual(self.q["total_accepted_trials"],600)
        self.assertEqual(self.q["biseparable_rejection_threshold_total_matches"],539)
    def test_sequential_model_statistical_power(self):
        self.assertGreater(self.q["exact_IID_model_power"],.99)
    def test_sequential_not_full_process_tensor(self):
        self.assertIn("not yet a three-slot process tensor",self.q["limitation"])
    def test_TOE_not_claimed(self):
        self.assertFalse(self.r["valid_full_TOE"])

if __name__=="__main__":unittest.main()
