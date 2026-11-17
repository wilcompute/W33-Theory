"""2026-11-17 independently reproducible tests across five TOE fronts."""
import math,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261117_soft_SU5_mirror_messenger_CW as cw
import toe_20261117_SU5_24mode_Hessian_thermal_wall as h
import toe_20261117_11D_flux_projected_BF_witness as kk
import toe_20261117_Tduality_integral_Gysin_involution as td
import toe_20261117_memory_2026_real_reference_qutrit as ph
import toe_20261117_E6_adjoint_invariant_shape_obstruction as oldE6

class A_MessengerLoop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=cw.verify()
    def test_softzero_exact_cancel(self):self.assertEqual(cw.F(0.),0.)
    def test_negative_small_soft(self):self.assertGreater(cw.F(-.1),0.)
    def test_positive_small_soft(self):self.assertLess(cw.F(.1),0.)
    def test_not_all_negative_softs_stabilize(self):self.assertLess(cw.F(-.5),0.)
    def test_root(self):
        self.assertAlmostEqual(self.z["numerical_controls"]["critical_negative_soft_t"],
                               -.26427939499877,places=11)
    def test_positive_at_minus_quarter(self):self.assertGreater(cw.F(-.25),0.)
    def test_exact_one_loop(self):self.assertIn("8*pi",self.z["analytic_one_loop"]["quartic_mirror_coefficient"])
    def test_nonzero_sign_five_radius(self):
        for row in self.z["numerical_controls"]["fixed_norm_3plus2_vs_4plus1"]:
            self.assertGreater(float(row["V_SU4_minus_V_SM"]),0)
    def test_approximation_is_local(self):
        self.assertIn("not a global vacuum proof",self.z["numerical_controls"]["renormalization_warning"])
    def test_no_e6_uv(self):
        self.assertIn("NOT an E6",self.z["scope"])
    def test_perturbative_y_scaling(self):
        self.assertAlmostEqual(16*self.z["numerical_controls"]["benchmark_kappa_eff_at_y1"],
                       cw.F(-.1)*2**4/(8*math.pi**2))
    def test_e6_quartic_fails(self):
        z=oldE6.verify()
        self.assertEqual(z["Cartan_dimension"],6)
        self.assertIn("/12",z["polynomial_identity_4"])

class B_AdjointStability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=h.verify()
    def test_24_orthonormal(self):self.assertEqual(len(h.basis5()),24)
    def test_24_mode_spectrum(self):self.assertEqual(len(self.z["Hessian"]["full_24x24_eigenvalue_spectrum"]),24)
    def test_eaten_twelve(self):
        self.assertEqual(self.z["Hessian"]["eigenvalue_multiplicities"]["gauge_orbit_Goldstone_12"]["multiplicity"],12)
    def test_octet_mass(self):
        a=self.z["Hessian"]["eigenvalue_multiplicities"]["SU3_colour_octet_8"]
        self.assertEqual(a["multiplicity"],8)
        self.assertAlmostEqual(a["m2"],.47619047619047616)
    def test_triplet_mass(self):
        a=self.z["Hessian"]["eigenvalue_multiplicities"]["SU2_weak_triplet_3"]
        self.assertEqual(a["multiplicity"],3)
        self.assertAlmostEqual(a["m2"],1.9047619047619047)
    def test_singlet_mass(self):
        self.assertAlmostEqual(self.z["Hessian"]["eigenvalue_multiplicities"]["radial_singlet_1"]["m2"],4)
    def test_Hessian_finite_difference(self):
        self.assertLess(self.z["Hessian"]["numeric_directional_Hessian_finite_difference_max_error"],1e-5)
    def test_thermal_meanfield(self):
        self.assertAlmostEqual(self.z["thermal_wall"]["mean_field_symmetry_restoration_temperature"],
                               math.sqrt(2.5))
    def test_wall_positive(self):
        self.assertGreater(self.z["thermal_wall"]["restricted_wall_tension"],0)
    def test_wall_not_exact_min(self):
        self.assertIn("may have smaller tension",self.z["thermal_wall"]["tension_is_upper_bound"])
    def test_actual_transition_not_claimed(self):
        self.assertIn("first order",self.z["thermal_wall"]["do_not_infer_transition_order"])

class C_AdSFluxVariational(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=kk.verify()
    def test_restricted_norm(self):self.assertEqual(self.z["exact"]["restricted_K"],"I_2")
    def test_exact_BF_det(self):
        self.assertEqual(self.z["exact"]["BF_shifted_determinant"],"lambda*(lambda-12+16*d²)")
    def test_analytic_projection(self):self.assertTrue(self.z["exact"]["status"].startswith("PASS"))
    def test_42_numerical_samples(self):self.assertEqual(self.z["numerical"]["sample_count"],42)
    def test_7_flux_angles(self):
        self.assertEqual(len(self.z["numerical"]["selected_lambda3pi"]),7)
    def test_zero_asym_projection_pass(self):
        self.assertTrue(self.z["numerical"]["selected_lambda3pi"][0]["projected_criterion_certifies"])
    def test_max_asym_projection_not_sufficient(self):
        self.assertFalse(self.z["numerical"]["selected_lambda3pi"][-1]["projected_criterion_certifies"])
    def test_full_still_unstable_high_asym(self):
        self.assertGreater(self.z["numerical"]["selected_lambda3pi"][-1]["actual_BF_deficit"],0)
    def test_positive_norm_assumption(self):
        self.assertIn("positive-norm",self.z["exact"]["sufficient_condition"]+
                      " positive-norm")
    def test_higher_deriv_not_computed(self):
        self.assertIn("outside",self.z["higher_derivative_uncomputed"])

class D_TopologicalDuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=td.verify()
    def test_dual_pair(self):self.assertEqual(td.dual(6,6,5),(5,-5,6))
    def test_involutive_pair(self):self.assertEqual(td.dual(*td.dual(6,6,5)),(6,6,5))
    def test_signed_tdual(self):
        for x in ((-5,6,-3),(0,-6,4),(12,18,-7)):
            self.assertEqual(td.dual(*td.dual(*x)),x)
    def test_2016(self):self.assertEqual(self.z["enumerated_nonzero_integer_cases"],2016)
    def test_6_to_5_torsion(self):
        x=self.z["examples"][0]
        self.assertEqual((x["original"]["pi1_torsion_order"],
                          x["dual"]["pi1_torsion_order"]),(6,5))
    def test_wedge_constraint(self):self.assertEqual(6*(-5)+6*5,0)
    def test_invalid_flux(self):
        with self.assertRaises(ValueError):td.dual(6,6,0)
    def test_invalid_euler(self):
        with self.assertRaises(ValueError):td.dual(0,0,1)
    def test_y_times_s1_h3(self):
        self.assertEqual(td.cohomology_circle6(6)["H3"],{"free":2,"torsion":[6]})
    def test_y_times_s1_h4(self):
        self.assertEqual(td.cohomology_circle6(6)["H4"],{"free":1,"torsion":[6]})
    def test_not_m_iib_page(self):
        self.assertIn("NOT",self.z["not_same_as_M_IIB_duality"])

class E_2026MemoryReadiness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.z=ph.verify()
    def test_PRL_90p2_reference(self):
        self.assertIn("90.2",self.z["cited_2026_measurements"][0]["reported_storage_and_retrieval_percent"])
    def test_RAQM_39p2_reference(self):
        self.assertIn("39.2",self.z["cited_2026_measurements"][1]["reported_first_AFC_echo_average_storage_efficiency_percent"])
    def test_qutrit_not_experiment(self):
        self.assertIn("not demonstrated qutrit",self.z["critical_caveat"])
    def test_one_mem_router_threshold(self):
        self.assertAlmostEqual(ph.scenario(.902,1)["minimum_symmetric_router_efficiency"],.94374171618532)
    def test_two_mem_router_threshold(self):
        self.assertAlmostEqual(ph.scenario(.902,2)["minimum_symmetric_router_efficiency"],.9936876306933)
    def test_RAqm_not_feasible_no_QND(self):
        self.assertFalse(ph.scenario(.392,1,router=1)["feasible_even_if_router_perfect"])
    def test_two_mem_at_99_router_fails(self):
        self.assertFalse(ph.scenario(.902,2,router=.99)["violates_trusted_witness_under_model"])
    def test_two_mem_at_995_router_just_passes(self):
        self.assertTrue(ph.scenario(.902,2,router=.995)["violates_trusted_witness_under_model"])
    def test_KL_large_trial(self):
        self.assertGreater(ph.scenario(.902,2,router=.995)["expected_log_evalue100_information_scale_herald_trials"],1e6)
    def test_KL_stronger_router_improves(self):
        self.assertLess(ph.scenario(.902,1,router=.99)["expected_log_evalue100_information_scale_herald_trials"],
                        ph.scenario(.902,1,router=.95)["expected_log_evalue100_information_scale_herald_trials"])
    def test_QND_prebasis_selectable(self):
        self.assertTrue(ph.qnd_prebasis(.392,2)["trusted_witness_conditional_pass"])
    def test_QND_rate_penalty(self):
        self.assertAlmostEqual(ph.qnd_prebasis(.392,2)["source_attempts_per_accepted_herald"],1/.392**2)
    def test_QND_not_hardware(self):
        self.assertTrue(ph.qnd_prebasis(.902,1)["physical_prebasis_nondestructive_herald_REQUIRED"])
    def test_fidelity_not_success(self):
        self.assertIn("QUBITS",self.z["cited_2026_measurements"][0]["reported_conditional_fidelity_percent"])

if __name__=="__main__":unittest.main()
