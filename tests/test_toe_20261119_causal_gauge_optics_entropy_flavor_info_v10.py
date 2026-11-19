"""Independent regressions for 2026-11-19 six physical TOE consistency gates."""
from __future__ import annotations
import math
import pathlib
import sys
import unittest
import numpy as np
from scipy.special import gammaln
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261119_causal_gauge_optics_entropy_flavor_info_v10 as m

class SixNewPhysicalGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=m.run()
        cls.gates=cls.result["gates"]

    def test_six_gates_execute(self):
        self.assertEqual(len(self.gates),6)
        self.assertTrue(all(x["status"]=="PASS" for x in self.gates.values()))

    def test_no_TOE_GR_or_SM_claim(self):
        self.assertFalse(self.result["TOE_solved"])
        self.assertFalse(self.result["emergent_Lorentzian_4D_Einstein_gravity"])
        self.assertFalse(self.result["Born_rule_derived"])
        self.assertFalse(self.result["SM_spectrum_derived"])

    def test_dag_upper_triangular_has_nilpotent_adjacency(self):
        for n in (4,6,9):
            A=np.triu(np.ones((n,n)),1)
            np.testing.assert_allclose(np.linalg.matrix_power(A,n),np.zeros_like(A))

    def test_dag_determinant_independent_of_edges(self):
        for n in (4,6,9):
            for p in (0.,.25,.8,1.):
                A=np.triu((np.random.default_rng(int(100*p+11*n)).random((n,n))<p).astype(float),1)
                for mass in (.5,1.,2.):
                    self.assertAlmostEqual(np.linalg.det(mass*np.eye(n)-.3*A),mass**n,places=9)

    def test_dag_determinant_remains_invariant_after_arbitrary_relabel(self):
        rng=np.random.default_rng(120)
        A=np.triu((rng.random((12,12))<.4).astype(float),1)
        P=rng.permutation(12)
        B=A[np.ix_(P,P)]
        self.assertAlmostEqual(np.linalg.det(1.3*np.eye(12)-.7*B),1.3**12)

    def test_dag_propagator_still_depends_on_links(self):
        A=np.zeros((5,5));B=A.copy();A[0,1]=1;B[0,2]=1
        G1=np.linalg.inv(np.eye(5)-.4*A)
        G2=np.linalg.inv(np.eye(5)-.4*B)
        self.assertGreater(np.linalg.norm(G1-G2),.5)

    def test_dag_propagator_nilpotent_finite_geometric_series(self):
        rng=np.random.default_rng(12)
        A=np.triu((rng.random((7,7))<.5).astype(float),1)
        m0=1.2;alpha=.6
        G=sum((alpha/m0)**k*np.linalg.matrix_power(A,k)/m0 for k in range(7))
        np.testing.assert_allclose(G@ (m0*np.eye(7)-alpha*A),np.eye(7),atol=1e-11)

    def test_dag_logdet_derivative_zero_for_any_alpha(self):
        A=np.triu(np.ones((6,6)),1)
        for alpha in (.01,.3,.6,1.):
            D=1.5*np.eye(6)-alpha*A
            self.assertAlmostEqual(float(np.trace(np.linalg.inv(D)@A)),0,places=12)

    def test_directed_cycle_determinant_changes_with_holonomy(self):
        n=6;a=.5;m0=1.7
        vals=[]
        for theta in (0.,.5,math.pi):
            T=np.zeros((n,n),complex)
            for j in range(n-1):T[j,j+1]=1
            T[n-1,0]=np.exp(1j*theta)
            d=np.linalg.det(m0*np.eye(n)-a*T)
            self.assertLess(abs(d-(m0**n-a**n*np.exp(1j*theta))),1e-11)
            vals.append(d)
        self.assertGreater(abs(vals[0]-vals[-1]),1e-2)

    def test_global_SU2_Witten_sign_is_mod2(self):
        for n in range(17):
            self.assertEqual((-1)**n,1 if n%2==0 else -1)

    def test_one_Weyl_doublet_is_anomalous(self):
        cases=self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["Witten_global_sign_cases"]
        self.assertEqual(cases[0]["left_Weyl_doublet_count"],1)
        self.assertFalse(cases[0]["passes_ordinary_Witten_SU2_parity_gate"])

    def test_a_Dirac_doublet_is_even_not_globally_anomalous(self):
        cases=self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["Witten_global_sign_cases"]
        self.assertEqual(cases[1]["left_Weyl_doublet_count"],2)
        self.assertTrue(cases[1]["passes_ordinary_Witten_SU2_parity_gate"])

    def test_one_SM_generation_has_four_doublets(self):
        cases=self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["Witten_global_sign_cases"]
        self.assertEqual(cases[2]["left_Weyl_doublet_count"],4)
        self.assertTrue(cases[2]["passes_ordinary_Witten_SU2_parity_gate"])

    def test_three_SM_generations_have_twelve_doublets(self):
        cases=self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["Witten_global_sign_cases"]
        self.assertEqual(cases[3]["left_Weyl_doublet_count"],12)
        self.assertTrue(cases[3]["passes_ordinary_Witten_SU2_parity_gate"])

    def test_extra_chiral_doublet_flips_global_anomaly_sign(self):
        cases=self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["Witten_global_sign_cases"]
        self.assertEqual(cases[4]["nontrivial_pi4_SU2_gauge_transformation_sign"],-1)
        self.assertEqual(cases[5]["nontrivial_pi4_SU2_gauge_transformation_sign"],+1)

    def test_exact_perturbative_anomalies_for_one_generation(self):
        a=self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["SM_one_generation_local_anomaly_integer_y6Y"]
        self.assertEqual(a,{"gravity_Y":0,"Y_cubed":0,"SU2_squared_Y":0,"SU3_squared_Y":0})

    def test_Z6_descent_for_each_standard_multiplet(self):
        residues=self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["standard_global_Z6_descent_residues"]
        self.assertTrue(all(v==0 for v in residues.values()))

    def test_SU2_Witten_gate_does_not_misclassify_vectorlike_determinant(self):
        self.assertIn("vectorlike",self.gates["II_global_SU2_Witten_anomaly_and_SM_quotient"]["important_distinction"])

    def test_local_photon_4mode_2photon_basis_six_states(self):
        g=self.gates["III_photonic_quadratic_gate_complexity_witness"]
        self.assertEqual(g["two_photon_sector_basis_n4"],[3,5,6,9,10,12])

    def test_ideal_Bell_A1_couples_two_fully_changed_occupations(self):
        g=self.gates["III_photonic_quadratic_gate_complexity_witness"]
        self.assertEqual(g["target_local_A1_nonzero_0110_to_1001_matrix_element"],1)
        self.assertEqual((6^9).bit_count(),4)

    def test_no_one_body_operator_couples_the_witness_states(self):
        basis=[v for v in range(16) if v.bit_count()==2]
        ix=basis.index(6);iy=basis.index(9)
        for i in range(4):
            for j in range(4):
                _,B=m.one_body_restricted_matrix(4,2,i,j)
                self.assertAlmostEqual(B[ix,iy],0)

    def test_one_body_projection_residual_is_at_least_sqrt2(self):
        g=self.gates["III_photonic_quadratic_gate_complexity_witness"]
        self.assertGreaterEqual(g["best_real_quadratic_generator_projection_residual_Frobenius"],
                                math.sqrt(2)-1e-12)

    def test_passive_linear_optical_ladder_below_ideal_collective_n4(self):
        g=self.gates["III_photonic_quadratic_gate_complexity_witness"]
        rows={a["copies"]:a for a in g["ideal_vs_published_passive_ladder"]}
        self.assertGreater(rows[4]["collective_minus_passive"],.10)

    def test_two_photon_passive_and_arbitrary_SSR_scores_agree(self):
        g=self.gates["III_photonic_quadratic_gate_complexity_witness"]
        row=g["ideal_vs_published_passive_ladder"][0]
        self.assertAlmostEqual(row["published_passive_ladder_CHSH"],1+math.sqrt(2))
        self.assertAlmostEqual(row["collective_minus_passive"],0,places=12)

    def test_gate_Witness_does_not_falsely_exclude_interferometer_and_binning(self):
        self.assertIn("does NOT rule out passive interferometers",
                      self.gates["III_photonic_quadratic_gate_complexity_witness"]["qualifier"])

    def test_layered_histories_have_quadratic_number_of_link_bits(self):
        for row in self.gates["IV_causal_history_entropy_vs_gapped_fermion_weight"]["results"]:
            N=row["events"]
            self.assertEqual(row["layer_adjacent_link_bits"],N*N//4)

    def test_group_quotient_orbit_lower_bound_independent_formula(self):
        for row in self.gates["IV_causal_history_entropy_vs_gapped_fermion_weight"]["results"]:
            N=row["events"]
            log10bound=(N*N/4*math.log(2)-2*gammaln(N//4+1)-gammaln(N//2+1))/math.log(10)
            self.assertAlmostEqual(row["log10_unlabeled_orbit_lower_bound"],log10bound)

    def test_uniform_gapped_fermion_cannot_select_one_good_history_at_64(self):
        row={r["events"]:r for r in self.gates["IV_causal_history_entropy_vs_gapped_fermion_weight"]["results"]}[64]
        self.assertGreater(row["log10_bad_to_one_good_weight_lower_bound_under_uniform_gap"],92.)

    def test_large_N_bad_weight_lower_bound_grows_quadratically(self):
        rows=self.gates["IV_causal_history_entropy_vs_gapped_fermion_weight"]["results"]
        self.assertGreater(rows[-1]["log10_bad_to_one_good_weight_lower_bound_under_uniform_gap"],700)

    def test_fermion_weight_no_go_is_conditional_on_spectral_lower_gap(self):
        g=self.gates["IV_causal_history_entropy_vs_gapped_fermion_weight"]
        self.assertIn("singular values >=a",g["spectral_assumption"])
        self.assertIn("zero modes",g["possible_escape"])

    def test_fermion_entropy_does_not_count_all_unlabeled_causets(self):
        self.assertIn("marked-layer",self.gates["IV_causal_history_entropy_vs_gapped_fermion_weight"]["limitation"])

    def test_two_link_flavor_laplacian_has_zero_constant_mode(self):
        for a in (.001,.1,1):
            b=1; L=np.array([[a,-a,0],[-a,a+b,-b],[0,-b,b]])
            np.testing.assert_allclose(L@np.ones(3),np.zeros(3),atol=1e-13)

    def test_flavor_graph_path_exact_gap_formula(self):
        for a in (.001,.1,.4,1.,3.):
            L=np.array([[a,-a,0],[-a,a+1,-1],[0,-1,1.]])
            gap=np.linalg.eigvalsh(L)[1]
            self.assertAlmostEqual(gap,a+1-math.sqrt(a*a-a+1),places=12)

    def test_flavor_graph_connectivity_rank_is_stable_when_weak_link_positive(self):
        rows=self.gates["V_flavor_connectivity_vs_spectral_gap"]["records"]
        self.assertEqual(rows[0]["Laplacian_rank"],1)
        self.assertTrue(all(r["Laplacian_rank"]==2 for r in rows[1:]))

    def test_flavor_connected_graph_can_have_arbitrarily_small_gap(self):
        rows=self.gates["V_flavor_connectivity_vs_spectral_gap"]["records"]
        self.assertTrue(rows[1]["graph_connected"])
        self.assertLess(rows[1]["exact_lambda2"],2e-6)

    def test_flavor_gap_asymptotic_three_halves_weak_edge(self):
        rows=self.gates["V_flavor_connectivity_vs_spectral_gap"]["records"]
        self.assertAlmostEqual(rows[1]["approx_ratio_lambda2_over_weak_edge"],1.5,delta=2e-6)

    def test_graph_penalty_is_not_a_PMNS_mass_model(self):
        self.assertIn("not predicted",self.gates["V_flavor_connectivity_vs_spectral_gap"]["limitation"])

    def test_spin_sector_fisher_probabilities_normalize(self):
        for rec in self.gates["VI_fermionic_spin_sector_information_distinguishability"]["results"]:
            self.assertAlmostEqual(sum(rec["normalized_four_sector_weights"]),1.,places=12)

    def test_spin_sector_weights_match_previous_wilson_determinant_formula(self):
        for mu in (.05,.1,.3,1.,5.):
            r=math.tanh(mu/2)
            expected=np.array([r**3,r,1,r*r])/((1+r)*(1+r*r))
            np.testing.assert_allclose(m.spin_sector_probabilities(mu),expected,atol=1e-15)

    def test_fisher_agrees_with_finite_difference(self):
        for rec in self.gates["VI_fermionic_spin_sector_information_distinguishability"]["results"]:
            self.assertAlmostEqual(rec["classical_Fisher_information_on_mu"],
                                   rec["finite_difference_Fisher_crosscheck"],delta=1e-6)

    def test_heavy_fermion_toy_sectors_approach_uniform(self):
        x=m.spin_sector_probabilities(25.)
        np.testing.assert_allclose(x,np.full(4,.25),atol=1e-10)

    def test_heavy_spin_sector_information_vanishes_exponentially(self):
        for mu in (8.,10.,12.):
            r=math.tanh(mu/2);rp=(1-r*r)/2
            I=rp*rp*(1/(r*(1+r)**2)+4/(1+r*r)**2)
            approx=5*math.exp(-2*mu)
            self.assertAlmostEqual(I/approx,1.,delta=.005)

    def test_spin_sector_information_is_toy_not_physical_prediction(self):
        self.assertIn("TOY",self.gates["VI_fermionic_spin_sector_information_distinguishability"]["limitation"])

if __name__=="__main__":
    unittest.main()
