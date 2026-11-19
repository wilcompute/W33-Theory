"""Independent regressions for five linked TOE research frontiers, November 2026.

No test promotes a conditional finite construction to a fundamental TOE.
"""
import itertools,math,pathlib,sys,unittest
import numpy as np
import sympy as sp
from scipy.special import iv
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_causal_nerve_transfer_interference_flavor_v6 as m

class CausalTopologyGaugeQuantumGravityFlavor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=m.combined()
        cls.g=cls.data["gates"]
        cls.I=cls.g["I_intrinsic_order_based_spatial_nerve_H1_and_spin_torsor"]
        cls.II=cls.g["II_SU2_positive_type_transfer_action_nonuniqueness"]
        cls.III=cls.g["III_transfer_Hilbert_sectors_and_quantum_state_choice"]
        cls.IV=cls.g["IV_oscillatory_KR_entropy_and_coherence_quantum_measure"]
        cls.V=cls.g["V_3generation_global_quotient_flavor_charge_freedom"]
        cls.VI=cls.g["VI_spin_center_compensation_on_topology_change"]

    def test_five_linked_fronts_plus_three_cross_sector_gates_executed(self):
        self.assertEqual(len(self.g),8)
        self.assertTrue(all(v["status"]=="PASS" for v in self.g.values()))

    def test_not_claiming_quantum_gravity_or_Born_or_SM_derivation(self):
        self.assertFalse(self.data["TOE_solved"])
        self.assertFalse(self.data["Lorentzian_4D_GR_derived"])
        self.assertFalse(self.data["SM_spectrum_derived"])
        self.assertFalse(self.data["Born_rule_derived"])

    def test_Gf2_rank_redundant_rows(self):
        B=np.array([[1,0,1],[1,0,1],[0,1,1]],np.uint8)
        self.assertEqual(m.gf2rank(B),2)

    def test_antichain_future_relations_are_bipartite(self):
        R=m.causal_ring_order(12,2)
        self.assertEqual(R.shape,(24,24))
        self.assertEqual(int(R[:12,12:].sum()),12*5)
        self.assertEqual(int(R[12:,:].sum()),0)
        self.assertEqual(int(R[:,:12].sum()),0)

    def test_future_shadow_cover_nerve_recovers_circle_H1(self):
        for r in (1,2):
            obj=m.betti_from_nerve_order(m.causal_ring_order(12,r),12)
            self.assertEqual(obj["betti_H0_H1_mod2"],[1,1])

    def test_shadow_scale_zero_disconnected(self):
        o=m.betti_from_nerve_order(m.causal_ring_order(12,0),12)
        self.assertEqual(o["betti_H0_H1_mod2"],[12,0])

    def test_thickening_too_far_fills_reconstructed_cycle(self):
        for r in (3,4,5):
            o=m.betti_from_nerve_order(m.causal_ring_order(12,r),12)
            self.assertEqual(o["betti_H0_H1_mod2"],[1,0])

    def test_two_consecutive_scales_stable_betti(self):
        obs=self.I["order_based_Dowker_nerve_at_shadow_scales"]
        self.assertEqual(self.I["stable_H1_plateau_radii"],[1,2])
        self.assertEqual([x["inferred_from_order_only"]["betti_H0_H1_mod2"][1] for x in obs],[0,1,1,0,0,0])

    def test_nerve_homology_independent_of_relabeled_causal_events(self):
        R=m.causal_ring_order(12,2)
        rng=np.random.default_rng(20261119)
        pa=rng.permutation(12);pw=rng.permutation(12)+12
        R2=R[np.ix_(np.concatenate((pa,pw)),np.concatenate((pa,pw)))]
        self.assertEqual(m.betti_from_nerve_order(R,12)["betti_H0_H1_mod2"],
                         m.betti_from_nerve_order(R2,12)["betti_H0_H1_mod2"])

    def test_classification_two_spin_sectors_only_when_H1_is_nonzero(self):
        obs=self.I["order_based_Dowker_nerve_at_shadow_scales"]
        self.assertEqual([x["candidate_Z2_spin_holonomy_sectors"] for x in obs],[1,2,2,1,1,1])

    def test_periodic_versus_antiperiodic_massless_lattice_Dirac(self):
        z=self.I["two_supplementary_spin_transport_spectra"]
        self.assertEqual([x["naive_derivative_zero_modes"] for x in z],[2,0])
        self.assertGreater(z[1]["minimum_squared_massless_Dirac_eigenvalue"],.01)

    def test_SU2_exact_mixed_action_identity_for_many_angles(self):
        for lam in (0.,.25,.5,.75,1.):
            for theta in np.linspace(0,math.pi,15):
                sf=m.sf(theta)
                self.assertAlmostEqual(m.s_mixed(theta,lam),sf-lam*sf*sf/2,places=13)

    def test_SU2_weak_field_coefficient_independent_of_mixture(self):
        h=.0005
        for lam in (0.,.25,.5,.75,1.):
            self.assertAlmostEqual(m.s_mixed(h,lam)/h**2,.5,delta=1e-7)

    def test_center_distinction_with_adjoint_only_at_minus_identity(self):
        # phi is the SU(2) eigen-angle: U=-I at phi=pi, not 2*pi.
        self.assertAlmostEqual(m.s_mixed(math.pi,0),2)
        self.assertAlmostEqual(m.s_mixed(math.pi,1),0)
        self.assertAlmostEqual(m.s_mixed(0,0),0)
        self.assertAlmostEqual(m.s_mixed(0,1),0)

    def test_five_reflection_positive_transfer_character_spectra(self):
        rows=self.II["reflection_positive_mixed_action_family"]
        self.assertEqual(len(rows),5)
        for o in rows:
            self.assertGreater(o["character_coefficients_n_0_to_8"][0],0)
            self.assertGreater(min(o["character_coefficients_n_0_to_8"]),-1e-12)
            self.assertGreater(min(o["normalized_transfer_eigenvalues_n_0_to_8"]),-1e-12)

    def test_all_five_transfer_spectra_are_distinct(self):
        rows=self.II["reflection_positive_mixed_action_family"]
        W=[round(x["fundamental_Wilson_mean"],8) for x in rows]
        self.assertEqual(len(set(W)),5)
        self.assertEqual(W,sorted(W,reverse=True))

    def test_fundamental_Wilson_mean_matches_previous_Haar_calculation(self):
        rows=self.II["reflection_positive_mixed_action_family"]
        self.assertAlmostEqual(rows[0]["fundamental_Wilson_mean"],.4331274267223,places=12)

    def test_fundamental_character_coefficients_equal_modified_Bessel_formula(self):
        beta=2
        for n in range(7):
            observed=m.transfer_coeff(beta,0,n)
            expected=math.exp(-beta)*(iv(n,beta)-iv(n+2,beta))
            self.assertAlmostEqual(observed,expected,places=12)

    def test_adjoint_character_coefficients_in_even_spin_channels(self):
        beta=2
        for n in (0,2,4,6,8):
            observed=m.transfer_coeff(beta,1,n)
            j=n//2
            expected=math.exp(-beta/4)*(iv(j,beta/4)-iv(j+1,beta/4))
            self.assertAlmostEqual(observed,expected,places=12)

    def test_adjoint_half_integer_center_odd_transfer_channels_vanish(self):
        row=self.II["reflection_positive_mixed_action_family"][-1]
        for n in (1,3,5,7):
            self.assertLess(abs(row["character_coefficients_n_0_to_8"][n]),1e-12)

    def test_positive_type_character_factorization_unbroken_for_lambda_half(self):
        phi=.7;lam=.5;beta=2
        # Compare the exponent after removing a representation-independent constant.
        actual=-beta*m.s_mixed(phi,lam)
        expected=beta*((1-lam)*math.cos(phi)+lam/4*math.cos(2*phi)-1+.75*lam)
        self.assertAlmostEqual(actual,expected,places=13)

    def test_positivity_does_not_select_unique_transfer_energy(self):
        rows=self.III["transfer_derived_effective_sector_energies"]
        self.assertEqual(len(rows),5)
        self.assertIsNotNone(rows[0]["effective_one_step_spin_half_energy_if_allowed"])
        self.assertIsNone(rows[-1]["effective_one_step_spin_half_energy_if_allowed"])
        self.assertNotAlmostEqual(rows[0]["effective_one_step_spin_half_energy_if_allowed"],
                                 rows[2]["effective_one_step_spin_half_energy_if_allowed"])

    def test_distinct_KMS_noise_same_retarded_response(self):
        q=self.III["same_causal_response_distinct_KMS_states"]
        self.assertEqual(len({v["retarded_G"] for v in q}),1)
        self.assertGreater(q[0]["KMS_noise"],3*q[-1]["KMS_noise"])

    def test_KMS_thermal_energy_monotonic_with_inverse_temperature(self):
        q=self.III["same_causal_response_distinct_KMS_states"]
        self.assertGreater(q[0]["oscillator_energy"],q[1]["oscillator_energy"])
        self.assertGreater(q[1]["oscillator_energy"],q[2]["oscillator_energy"])

    def test_KR_history_counts_exact_at_8_to_64_events(self):
        for x in self.IV["size_scaling_records"]:
            n=x["N"]
            self.assertEqual(x["independent_links_M"],n*n//4)
            self.assertAlmostEqual(x["log10_number_of_labeled_histories"],
                                   n*n/4*math.log10(2))

    def test_KR_oscillatory_partition_matches_independent_binomial_sum(self):
        M=16;t=2.5
        explicit=sum(math.comb(M,k)*np.exp(1j*t*k) for k in range(M+1))
        reported=complex(*self.IV["N8_direct_complex_sum_real_imag"])
        self.assertLess(abs(explicit-reported),1e-10)

    def test_KR_critical_phase_is_two_pi_over_three(self):
        self.assertAlmostEqual(self.IV["critical_phase_for_absolute_suppression_radians"],2*math.pi/3)
        self.assertGreater(2*abs(math.cos(1.5/2)),1)
        self.assertLess(2*abs(math.cos(2.5/2)),1)

    def test_fixed_phase_can_suppress_absolute_labeled_family_amplitude(self):
        x=self.IV["size_scaling_records"][-1]
        self.assertEqual(x["N"],64)
        self.assertLess(x["log10_absolute_coherent_partition_magnitude"],-200)
        self.assertLess(x["log10_coherent_vs_unsigned_amplitude_ratio"],-500)

    def test_KR_decoherence_mixture_has_positive_semidefinite_histories_matrix(self):
        z=self.IV["partial_decoherence_PSD_certificates"]
        for x in z:
            self.assertGreater(x["minimum_eigenvalue"],-1e-11)

    def test_even_small_fixed_incoherence_swamps_absolute_interference(self):
        N=64;M=N*N//4;gamma=.999;theta=2.5
        # For 1-gamma=.001, incoherent log10 contribution is 305,
        # whereas coherent |Z|² is 10^-410. This is a toy linear functional.
        incoherent=math.log10(1-gamma)+M*math.log10(2)
        coherent=2*M*math.log10(2*abs(math.cos(theta/2)))
        self.assertGreater(incoherent,305-1)
        self.assertLess(coherent,-400)

    def test_hypercharge_mutations_cancel_all_four_local_anomalies(self):
        for K in (-2,-1,0,1,2):
            a=m.anomalies(m.species(),sp.Integer(K))
            self.assertTrue(all(v==0 for v in a.values()),str(a))

    def test_three_generation_anomaly_cancellation_symbolically_for_all_k(self):
        k=sp.symbols("k",integer=True)
        q=m.anomalies(m.species(),k)
        self.assertEqual(q,{"U1_cube":0,"grav_U1":0,"SU2_squared_U1":0,"SU3_squared_U1":0})

    def test_same_deformation_anomaly_free_without_sterile_neutrinos(self):
        k=sp.symbols("k",integer=True)
        f=[x for x in m.species() if x["multiplet"]!="nc"]
        self.assertTrue(all(v==0 for v in m.anomalies(f,k).values()))

    def test_all_deformed_charges_obey_Z6_global_quotient(self):
        for K in (-2,-1,0,1,2):
            for field in m.species():
                y=field["y"]+6*K*field["X"]
                self.assertEqual((2*field["triality"]+3*field["weak_doublet"]+y)%6,0)

    def test_neutrino_charge_is_mu_k_and_tau_minus_k(self):
        obs=self.V["global_Z6_and_anomaly_cases"]
        for row in obs:
            self.assertEqual(int(row["mu_neutrino_electric_charge"]),row["k"])
            self.assertEqual(int(row["tau_neutrino_electric_charge"]),-row["k"])

    def test_generic_offdiagonal_lepton_yukawas_forbid_nonzero_k(self):
        for row in self.V["global_Z6_and_anomaly_cases"]:
            self.assertEqual(row["offdiagonal_charged_lepton_Yukawas_all_allowed"],row["k"]==0)

    def test_diagonal_lepton_yukawa_survives_each_flavor_shift(self):
        for K in (-2,-1,0,1,2):
            for gen in range(3):
                L=next(r for r in m.species() if r["generation"]==gen and r["multiplet"]=="L")
                E=next(r for r in m.species() if r["generation"]==gen and r["multiplet"]=="ec")
                self.assertEqual(L["y"]+6*K*L["X"]+E["y"]+6*K*E["X"]-3,0)

    def test_data_explicitly_identifies_old_one_generation_implicit_assumption(self):
        self.assertIn("generation-universal",self.V["main_new_insight"])

    def test_topology_change_increases_available_spin_torsor_size(self):
        self.assertEqual(self.VI["prior_S3_b1"],0)
        self.assertEqual(self.VI["after_S1xS2_b1"],1)
        self.assertEqual(self.VI["prior_number_of_spin_structures"],1)
        self.assertEqual(self.VI["after_number_of_spin_structures"],2)

    def test_charged_doublet_effective_spin_twists_are_center_compensable(self):
        s=self.VI["four_conditional_after_transition_sectors"]
        self.assertEqual([(x["spin_Z2_twist"],x["SU2_central_minus_identity_twist"])
                          for x in s],[(0,0),(0,1),(1,0),(1,1)])
        self.assertEqual([x["effective_fundamental_twist"] for x in s],[0,1,1,0])
        self.assertEqual([x["fundamental_massless_naive_zero_modes"] for x in s],[2,0,0,2])

    def test_gauge_singlet_can_distinguish_compensated_fermion_sectors(self):
        s=self.VI["four_conditional_after_transition_sectors"]
        self.assertEqual([x["neutral_massless_naive_zero_modes"] for x in s],[2,2,0,0])
        self.assertEqual(s[0]["fundamental_massless_naive_zero_modes"],
                         s[3]["fundamental_massless_naive_zero_modes"])
        self.assertNotEqual(s[0]["neutral_massless_naive_zero_modes"],
                            s[3]["neutral_massless_naive_zero_modes"])

    def test_no_unjustified_claim_that_spin_cobordism_selects_physical_sector(self):
        self.assertIn("does not fix",self.VI["cobordism_warning"])
        self.assertIn("not an emergent SM",self.VI["scope"])

    def test_full_eight_gates_have_status_and_independent_scope(self):
        self.assertEqual(len(self.g),8)
        self.assertTrue(all(v["status"]=="PASS" for v in self.g.values()))
        self.assertIn("toy",self.g["VII_fermion_determinant_dynamic_spin_center_selection"]["scope"])

    def test_wilson_circle_det_matches_closed_form_varied_lattices(self):
        for n in (5,8,12,17):
            for mass in (0.,.01,.2,1.):
                for theta in (0.,np.pi,np.pi/3):
                    det=np.linalg.det(m.wilson_circle_operator(n,mass,theta))
                    expected=(1+mass)**n-np.exp(-1j*theta)
                    self.assertLess(abs(det-expected),1e-7)

    def test_wilson_circle_operator_massless_periodic_has_one_not_two_zero_modes(self):
        D=m.wilson_circle_operator(12,0.,0.)
        self.assertEqual(int(np.sum(np.linalg.svd(D,compute_uv=False)<1e-10)),1)
        self.assertAlmostEqual(np.linalg.det(D),0)

    def test_wilson_circle_antiperiodic_massless_has_nonzero_determinant(self):
        self.assertAlmostEqual(np.linalg.det(m.wilson_circle_operator(12,0.,np.pi)).real,2.,places=10)

    def test_wilson_circle_dirac_gauge_frame_conjugation_preserves_determinant(self):
        rng=np.random.default_rng(40)
        D=m.wilson_circle_operator(12,.1,np.pi)
        phases=np.exp(1j*rng.uniform(-np.pi,np.pi,12))
        G=np.diag(phases)
        self.assertLess(abs(np.linalg.det(D)-np.linalg.det(G@D@G.conj().T)),1e-9)

    def test_massless_spin_center_selection_doublet_and_singlet(self):
        r=self.g["VII_fermion_determinant_dynamic_spin_center_selection"]
        sector=r["sectors_by_mass"][0]["spin_center_sectors"]
        self.assertEqual([x["normalized_toy_probability_with_singlet"] for x in sector],[0,0,1,0])

    def test_massless_doublet_alone_does_not_select_unique_spin_center(self):
        r=self.g["VII_fermion_determinant_dynamic_spin_center_selection"]
        sector=r["sectors_by_mass"][0]["spin_center_sectors"]
        self.assertEqual([x["normalized_toy_probability_without_singlet"] for x in sector],
                         [0,.5,.5,0])

    def test_neutral_singlet_distinguishes_compensated_spin_center_twists(self):
        r=self.g["VII_fermion_determinant_dynamic_spin_center_selection"]
        sector=r["sectors_by_mass"][0]["spin_center_sectors"]
        self.assertEqual(sector[1]["fundamental_doublet_determinant_magnitude_squared_color"],
                         sector[2]["fundamental_doublet_determinant_magnitude_squared_color"])
        self.assertEqual(sector[1]["neutral_singlet_determinant_magnitude"],0)
        self.assertGreater(sector[2]["neutral_singlet_determinant_magnitude"],1)

    def test_finite_N_mass_mu_over_N_det_ratio_approaches_tanh(self):
        r=self.g["VII_fermion_determinant_dynamic_spin_center_selection"]
        for row in r["continuum_mass_length_gate"]:
            mu=row["dimensionless_mass_times_circle_length_mu"]
            self.assertAlmostEqual(row["continuum_ratio_detP_to_detAP"],np.tanh(mu/2),places=13)
            if mu<=5.:
                vals=row["finite_n_refinements"]
                self.assertLess(abs(vals[-1]["deviation_from_continuum_tanh_mu_over_2"]),
                                abs(vals[0]["deviation_from_continuum_tanh_mu_over_2"])+1e-15)

    def test_four_spin_center_probabilities_from_exact_continuum_formula(self):
        r=self.g["VII_fermion_determinant_dynamic_spin_center_selection"]
        for row in r["continuum_mass_length_gate"]:
            z=row["continuum_ratio_detP_to_detAP"]
            expected=np.array([z**3,z,1,z**2])/((1+z)*(1+z*z))
            np.testing.assert_allclose(row["continuum_spin_center_sectors_00_01_10_11"],
                                       expected,rtol=1e-13,atol=1e-14)

    def test_massive_sector_choice_becomes_indistinguishable_large_mass_length(self):
        r=self.g["VII_fermion_determinant_dynamic_spin_center_selection"]
        huge=r["continuum_mass_length_gate"][-1]["continuum_spin_center_sectors_00_01_10_11"]
        self.assertLess(max(abs(x-.25) for x in huge),1e-8)

    def test_mass_light_continuum_highly_prefers_one_sector(self):
        r=self.g["VII_fermion_determinant_dynamic_spin_center_selection"]
        small=r["continuum_mass_length_gate"][1]["continuum_spin_center_sectors_00_01_10_11"]
        self.assertGreater(small[2],.94)

    def test_normalized_two_sector_decoherence_is_explicitly_conditional(self):
        r=self.g["VIII_normalized_two_class_decoherence_control"]
        self.assertTrue(r["no_observed_4D_quantum_gravity_phase_selected"])
        self.assertEqual(r["conditional_competing_good_spacetime_weight"],1)
        self.assertIn("assigned unit weight",r["physical_honesty"])

    def test_incoherent_weight_contaminates_bad_history_sector_for_64_events(self):
        r=self.g["VIII_normalized_two_class_decoherence_control"]
        z=r["normalized_two_sector_measure_records"][-1]
        self.assertEqual(z["N"],64)
        self.assertGreater(z["log10_bad_incoherent_branch_weight"],305)
        self.assertLess(z["log10_bad_coherent_branch_weight"],-400)
        self.assertEqual(z["normalized_bad_sector_probability_against_unit_good_reference"],1.)

    def test_critical_coherence_error_must_be_exponential_in_history_bits(self):
        r=self.g["VIII_normalized_two_class_decoherence_control"]
        self.assertAlmostEqual(
           r["log10_incoherent_fraction_threshold_for_bad_weight_below_one_at_N64"],
           -1024*np.log10(2),places=12)

    def test_normalized_relative_measure_does_not_become_real_TOE(self):
        self.assertFalse(self.data["TOE_solved"])
        self.assertFalse(self.data["Lorentzian_4D_GR_derived"])
        self.assertFalse(self.data["Born_rule_derived"])

if __name__=="__main__":unittest.main()
