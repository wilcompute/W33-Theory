"""Independent tests for five integrated fundamental-physics gates and two bridges.

These tests check exact algebra and independently reconstructed quantities.
They do not make a scientific prediction or establish a completed TOE.
"""
from __future__ import annotations
import math,pathlib,sys,unittest
import numpy as np
import sympy as sp
from scipy.special import iv
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_five_deep_closure_gates_v5 as m

class FiveCompleteAttemptsPlusGlobalBridges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=m.produce()
        cls.g=cls.data["gates"]

    def test_seven_integrated_gates_executed(self):
        self.assertEqual(len(self.g),7)
        self.assertTrue(all(v["status"]=="PASS" for v in self.g.values()))

    def test_no_fake_TOE_or_SM_or_Einstein_claim(self):
        self.assertFalse(self.data["TOE_solved"])
        self.assertFalse(self.data["4D_Einstein_Lorentzian_dynamics_derived"])
        self.assertFalse(self.data["Born_rule_or_unique_vacuum_derived"])
        self.assertFalse(self.data["SM_spectrum_or_couplings_derived"])

    def test_Gf2_rank_of_crown_boundary(self):
        B=np.array([[1,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,1]],dtype=np.uint8)
        self.assertEqual(m.gf2rank(B),3)

    def test_unbounded_crown_H1_one(self):
        r=self.g["I_bounded_poset_contractible_spin_holonomy_obstruction"]["unbounded_crown"]
        self.assertEqual(r["H1_mod2"],1)
        self.assertEqual(r["simplex_counts"],{"0":4,"1":4})
        self.assertEqual(r["betti"],{"0":1,"1":1})

    def test_endpoints_destroy_order_complex_H1(self):
        r=self.g["I_bounded_poset_contractible_spin_holonomy_obstruction"]
        self.assertEqual(r["bounded_causal_interval"]["H1_mod2"],0)
        self.assertEqual(r["with_unique_initial_event"]["H1_mod2"],0)

    def test_bounded_poset_cone_contractible_all_dimensions(self):
        r=self.g["I_bounded_poset_contractible_spin_holonomy_obstruction"]["bounded_causal_interval"]
        self.assertEqual(r["simplex_counts"]["3"],4)
        self.assertEqual(r["betti"].get("0"),1)
        self.assertTrue(all(v==0 for k,v in r["betti"].items() if k!="0"))

    def test_single_element_poset_H0_only(self):
        r=m.order_complex(["a"],[])
        self.assertEqual(r["betti"],{"0":1})

    def test_two_disconnected_elements_two_components(self):
        r=m.order_complex(["a","b"],[])
        self.assertEqual(r["betti"],{"0":2})

    def test_SU2_fundamental_adj_action_exact_identity(self):
        r=self.g["II_gauge_invariance_action_nonuniqueness_and_center"]
        for rec in r["one_plaquette_SU2_angle_checks"]:
            sf=rec["fundamental_S"];sa=rec["adjoint_rescaled_S"]
            self.assertAlmostEqual(sa,sf-.5*sf*sf,places=12)

    def test_SU2_weak_curvature_same_quadratic(self):
        for theta in (.0001,.001):
            self.assertAlmostEqual(m.fundamental(theta)/theta**2,.125,delta=2e-8)
            self.assertAlmostEqual(m.adjoint_rescaled(theta)/theta**2,.125,delta=2e-8)

    def test_SU2_curvature_quartic_difference_not_universality_theorem(self):
        t=.3
        observed=m.adjoint_rescaled(t)-m.fundamental(t)
        self.assertAlmostEqual(observed,-.5*m.fundamental(t)**2,places=12)
        self.assertLess(observed,0)

    def test_center_minus_one_detectable_in_fundamental_only(self):
        r=self.g["II_gauge_invariance_action_nonuniqueness_and_center"]
        self.assertAlmostEqual(r["center_minus_identity_fundamental_action"],2)
        self.assertAlmostEqual(r["center_minus_identity_adjoint_action"],0)

    def test_different_SU2_field_equations_at_finite_angle(self):
        r=self.g["II_gauge_invariance_action_nonuniqueness_and_center"]
        self.assertGreater(abs(r["finite_theta_07_force_fund"]-
                               r["finite_theta_07_force_adj"]),.005)

    def test_oscillator_retarded_green_function_temperature_independent(self):
        r=self.g["III_response_noise_KMS_vacuum_ambiguity"]
        vals=[x["retarded_response_same_for_all_beta"] for x in r["thermal_states"]]
        self.assertEqual(len(set(vals)),1)
        self.assertAlmostEqual(vals[0],math.sin(r["harmonic_frequency_w"]*r["comparison_time_t"])/r["harmonic_frequency_w"])

    def test_KMS_boundary_identity_each_temperature(self):
        r=self.g["III_response_noise_KMS_vacuum_ambiguity"]
        for x in r["thermal_states"]:
            self.assertLess(x["KMS_identity_error"],1e-11)

    def test_Wightman_Gram_positivity_each_temperature(self):
        r=self.g["III_response_noise_KMS_vacuum_ambiguity"]
        for x in r["thermal_states"]:
            self.assertGreater(x["positive_Wightman_kernel_min_eigenvalue"],-1e-10)

    def test_same_commutator_with_different_noise_levels(self):
        r=self.g["III_response_noise_KMS_vacuum_ambiguity"]
        ns=[x["symmetric_noise_covariance_at_t"] for x in r["thermal_states"]]
        self.assertGreater(ns[0]/ns[-1],3)
        for x in r["thermal_states"]:
            self.assertLess(x["commutator_state_independent_error"],1e-12)

    def test_thermal_oscillator_exact_energy(self):
        r=self.g["III_response_noise_KMS_vacuum_ambiguity"]
        for x in r["thermal_states"]:
            self.assertAlmostEqual(x["mean_energy"],r["harmonic_frequency_w"]*(x["occupancy_n"]+.5))

    def test_three_layer_coverage_count_exact_n8(self):
        r=self.g["IV_exact_poset_entropy_and_existing_4D_Regge_control"]
        hist={int(k):v for k,v in r["exact_enumeration_N8_link_count_histogram"].items()}
        self.assertEqual(sum(hist.values()),2**16)
        for k in range(17):self.assertEqual(hist[k],math.comb(16,k))

    def test_three_layer_64_elements_exact_entropy(self):
        r=self.g["IV_exact_poset_entropy_and_existing_4D_Regge_control"]
        row=next(x for x in r["three_layer_labeled_entropy"] if x["N"]==64)
        self.assertEqual(row["independent_cover_bits"],1024)
        self.assertAlmostEqual(row["log10_number_of_labeled_layered_posets"],1024*math.log10(2))
        self.assertEqual(row["mean_links_beta_zero"],512)

    def test_finite_edge_penalty_does_not_hold_mean_degree_fixed(self):
        r=self.g["IV_exact_poset_entropy_and_existing_4D_Regge_control"]
        vals=[x["per_vertex_mean_cover_degree_beta_2"] for x in r["three_layer_labeled_entropy"]]
        for j in range(len(vals)-1):self.assertAlmostEqual(vals[j+1],2*vals[j])

    def test_size_dependent_beta_needed_to_hold_n_edges(self):
        r=self.g["IV_exact_poset_entropy_and_existing_4D_Regge_control"]
        for x in r["three_layer_labeled_entropy"]:
            M=x["independent_cover_bits"];N=x["N"]
            beta=x["beta_needed_for_one_expected_link_per_event"]
            p=1/(1+math.exp(beta))
            self.assertAlmostEqual(M*p,N)

    def test_existing_real_4D_Regge_action_crosschecked(self):
        r=self.g["IV_exact_poset_entropy_and_existing_4D_Regge_control"]
        expected=20*math.sqrt(3)/4*(2*math.pi-3*math.acos(.25))
        self.assertAlmostEqual(r["existing_4D_Regge_S4_action"],expected,places=10)

    def test_4D_Schlaefli_gradient_against_finite_difference(self):
        r=self.g["IV_exact_poset_entropy_and_existing_4D_Regge_control"]
        self.assertAlmostEqual(r["existing_4D_Regge_one_edge_gradient_numeric"],
                                r["existing_4D_Regge_one_edge_gradient_Schlaefli"],delta=1e-6)

    def test_SM_anomaly_equations_hold_symbolically_for_two_parameters(self):
        a,x=sp.symbols("a x",integer=True)
        z=[a,-a-x,-a+x,-3*a,3*a+x,3*a-x]
        r=m.sm_anomalies(z)
        for k,v in r.items():
            if k!="SU2_Witten_left_doublets":self.assertEqual(sp.simplify(v),0)
        self.assertEqual(r["SU2_Witten_left_doublets"],4)

    def test_SM_cubic_anomaly_factorization_shows_multiple_branches(self):
        a,b,e=sp.symbols("a b e",integer=True)
        z=[a,b,-2*a-b,-3*a,e,6*a-e]
        c=sp.factor(m.sm_anomalies(z)["U1_cubed"])
        self.assertEqual(sp.simplify(c-18*a*(2*a-b-e)*(4*a+b-e)),0)

    def test_all_sample_charges_obey_Z6_quotient(self):
        r=self.g["V_SM_global_Z6_anomaly_Yukawa_charge_lattice"]
        for fam in r["sample_charge_families"]:
            self.assertEqual(fam["Z6_center_residues"],[0]*7)

    def test_all_sample_charges_are_anomaly_free_and_Yukawa_compatible(self):
        r=self.g["V_SM_global_Z6_anomaly_Yukawa_charge_lattice"]
        for fam in r["sample_charge_families"]:
            self.assertTrue(all(v==0 for k,v in fam["anomaly_sums"].items() if k!="SU2_Witten_left_doublets"))
            self.assertEqual(fam["all_renormalizable_Yukawa_charge_sums"],[0]*4)

    def test_observed_SM_charges_exist_but_not_uniquely_selected(self):
        r=self.g["V_SM_global_Z6_anomaly_Yukawa_charge_lattice"]
        vals=[x["charges_by_field"] for x in r["sample_charge_families"]]
        self.assertEqual(vals[0],{"Q_L":1,"u_c":-4,"d_c":2,"L_L":-3,"e_c":6,"nu_c":0})
        self.assertNotEqual(vals[1],vals[0])

    def test_hypercharge_exotic_candidate_gives_charged_neutrino(self):
        r=self.g["V_SM_global_Z6_anomaly_Yukawa_charge_lattice"]
        self.assertEqual(r["sample_charge_families"][1]["left_neutrino_em_charge_given_Higgs"],1/3)
        self.assertEqual(r["sample_charge_families"][0]["left_neutrino_em_charge_given_Higgs"],0)

    def test_without_nuc_gravitational_anomaly_fixes_x_equals_3a(self):
        a,x=sp.symbols("a x",integer=True)
        r=self.g["V_SM_global_Z6_anomaly_Yukawa_charge_lattice"]
        parsed=sp.sympify(r["no_nu_c_remaining_grav_anomaly"],locals={"a":a,"x":x})
        self.assertEqual(sp.simplify(parsed-(x-3*a)),0)

    def test_center_blind_action_and_fund_doublets_are_distinguishable(self):
        r=self.g["VI_center_sensitive_matter_global_transport_bridge"]
        self.assertEqual(r["SU2_center_flux_adjoint_cost"],0)
        self.assertEqual(r["SU2_center_flux_fundamental_cost"],2)
        self.assertEqual(r["center_action_on_fundamental_doublet"],-1)
        self.assertEqual(r["SM_Z6_combined_center_residues"],[0]*7)

    def test_SU2_one_plaquette_Haar_normalization(self):
        r=self.g["VII_nonperturbative_center_sensitive_Haar_observable"]["Haar_partition_records"]
        self.assertAlmostEqual(r[0]["fundamental"]["Z"],1)
        self.assertAlmostEqual(r[0]["adjoint"]["Z"],1)

    def test_SU2_adjoint_ensemble_center_odd_Wilson_loop_exactly_zero(self):
        r=self.g["VII_nonperturbative_center_sensitive_Haar_observable"]["Haar_partition_records"]
        for row in r:self.assertLess(abs(row["adjoint"]["fundamental_Wilson_trace_normalized_mean"]),1e-11)

    def test_SU2_fundamental_ensemble_Wilson_mean_Bessel_closed_form(self):
        r=self.g["VII_nonperturbative_center_sensitive_Haar_observable"]["Haar_partition_records"]
        for row in r[1:]:
            beta=row["beta"]
            direct=row["fundamental"]["fundamental_Wilson_trace_normalized_mean"]
            expected=(iv(1,beta)-iv(3,beta))/(2*(iv(0,beta)-iv(2,beta)))
            self.assertAlmostEqual(direct,expected,places=12)

    def test_full_center_sensitive_vs_blind_expectation_at_beta2(self):
        r=self.g["VII_nonperturbative_center_sensitive_Haar_observable"]
        fundamental,adjoint=r["beta2_unequal_Wilson_mean"]
        self.assertAlmostEqual(fundamental,.4331274267223,places=11)
        self.assertAlmostEqual(adjoint,0,places=11)

if __name__=="__main__":
    unittest.main()
