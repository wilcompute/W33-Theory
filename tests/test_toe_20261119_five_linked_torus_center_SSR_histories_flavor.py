"""Independent checks of five linked physical TOЕ gates; no fundamental solution claim."""
import pathlib,sys,itertools,math,unittest
import numpy as np
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261119_five_linked_torus_center_SSR_histories_flavor as p

class FivePhysicsGateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.o=p.all_gates();cls.g=cls.o['five_gates']
 def test_all_five_run(self):self.assertEqual(len(self.g),5)
 def test_no_TOE_claim(self):
  for x in ('TOE_solved','4d_gravity_derived','SM_chirality_derived','Born_rule_derived'):self.assertFalse(self.o[x])
 def test_causal_relation_2_layer(self):
  A=p.torus_causal(6);self.assertEqual(A.shape,(36,36));self.assertTrue(np.all(A.sum(axis=1)==9));self.assertTrue(np.all(A.sum(axis=0)==9))
 def test_2torus_homology_GF2_all_dimensions(self):
  for x in self.g['causal_torus_overlap_chirality_flux']['torus_orders']:
   self.assertEqual(x['nerve']['betti'],[1,2,1]);self.assertEqual(x['degrees_unique'],[4])
 def test_2torus_euler_characteristic(self):
  for x in self.g['causal_torus_overlap_chirality_flux']['torus_orders']:
   self.assertEqual(x['nerve']['betti'][0]-x['nerve']['betti'][1]+x['nerve']['betti'][2],0)
 def test_2torus_boundary_matrix_rank_formula(self):
  for x in self.g['causal_torus_overlap_chirality_flux']['torus_orders']:
   f=x['nerve']['simplex_counts_0_to_3'];r=x['nerve']['boundary_ranks_1_to_3'];self.assertEqual([f[0]-r[0],f[1]-r[0]-r[1],f[2]-r[1]-r[2]],[1,2,1])
 def test_torus_max_overlap_4regular(self):
  for L in (5,6,7,8):
   q=p.graph_from_overlap(p.torus_causal(L),L);self.assertEqual(len(q['edges']),2*L*L);self.assertEqual(q['high_overlap'],6)
 def test_2torus_four_neighbor_chart_from_graph(self):
  L=6;g=p.graph_from_overlap(p.torus_causal(L),L)
  for y in range(L):
   for x in range(L):
    v=g['chart'][(x,y)];self.assertEqual({g['chart'][(x+1)%L,y],g['chart'][(x-1)%L,y],g['chart'][x,(y+1)%L],g['chart'][x,(y-1)%L]},g['adj'][v])
 def test_causal_relabeled_independent(self):
  L=6;A=p.torus_causal(L);r=np.random.default_rng(171);A=A[np.ix_(r.permutation(L*L),r.permutation(L*L))];self.assertEqual(p.nerve_betti_2(A)['betti'],[1,2,1]);self.assertEqual(len(p.graph_from_overlap(A,L)['edges']),72)
 def test_flux_zero_index(self):
  x=self.g['causal_torus_overlap_chirality_flux'];self.assertTrue(all(v['index']==0 for v in x['L6_flux_index'] if v['flux_Q']==0))
 def test_flux_1_minus_chirality_index_m1(self):
  x=self.g['causal_torus_overlap_chirality_flux'];self.assertEqual([(v['flux_Q'],v['index']) for v in x['L6_flux_index'] if v['m']==1.],[(-1,1),(0,0),(1,-1)])
 def test_overlap_mass_branch_flips_index(self):
  x=self.g['causal_torus_overlap_chirality_flux'];self.assertEqual([(v['flux_Q'],v['index']) for v in x['L6_flux_index'] if v['m']==2.5],[(-1,-1),(0,0),(1,1)])
 def test_overlap_exact_GW_identity(self):
  for x in self.g['causal_torus_overlap_chirality_flux']['L6_flux_index']:self.assertLess(x['Ginsparg_Wilson_error'],1e-12)
 def test_flux_gap_nonzero(self):
  for x in self.g['causal_torus_overlap_chirality_flux']['L6_flux_index']:self.assertGreater(x['gap'],.1)
 def test_chiral_index_needs_inserted_flux(self):self.assertIn('input',self.g['causal_torus_overlap_chirality_flux']['not_derived'])
 def test_center_pure_adj_W_zero(self):
  z=self.g['dynamical_fundamental_center']['Haar_quadrature'];self.assertTrue(all(abs(x['pure_W'])<1e-12 for x in z if x['lambda']==1.))
 def test_fundamental_explicit_center_break(self):
  z=self.g['dynamical_fundamental_center']['Haar_quadrature'];self.assertTrue(all(x['with_fundamental_W']<0 for x in z if x['lambda']==1.))
 def test_center_break_decouples_heavy_matter(self):
  z=self.g['dynamical_fundamental_center']['Haar_quadrature'];self.assertLess(abs(z[-1]['with_fundamental_W']),.001)
 def test_center_break_formula_analytic_moments(self):
  for v in self.g['dynamical_fundamental_center']['Haar_quadrature']:
   b=v['b'];e=v['pure_W'];e2=v['pure_W2'];self.assertAlmostEqual(v['with_fundamental_W'],((b*b+1)*e-2*b*e2)/(b*b+1-2*b*e))
 def test_SU2_haar_normalized_moments_bound(self):
  for v in self.g['dynamical_fundamental_center']['Haar_quadrature']:
   self.assertGreaterEqual(v['pure_W2'],v['pure_W']**2-1e-12)
 def test_SSR_local_number_commutation(self):
  p0,p1,p2,X,Z=p.projectors_local();n=np.diag([0,1,1,2]);self.assertTrue(np.allclose(X@n,n@X));self.assertTrue(np.allclose(Z@n,n@Z))
 def test_SSR_2copies_CHSH(self):self.assertAlmostEqual(self.g['two_copy_particle_SSR_Bell']['CHSH_exact'],1+np.sqrt(2))
 def test_SSR_2copy_nA_sector_weight(self):self.assertEqual(self.g['two_copy_particle_SSR_Bell']['two_copy_local_charge_sector_probabilities'],{0:.25,1:.5,2:.25})
 def test_SSR_twirl_nonnegative_trace_one(self):
  s=p.twocopy_state();r=p.local_twirl(np.outer(s,s.conj()));self.assertAlmostEqual(np.trace(r).real,1.);self.assertGreater(np.linalg.eigvalsh(r).min(),-1e-12)
 def test_SSR_no_postselection_correlations(self):self.assertGreater(self.g['two_copy_particle_SSR_Bell']['CHSH_exact'],2.)
 def test_SSR_loss_exact_polynomial(self):
  for item in self.g['two_copy_particle_SSR_Bell']['loss_with_all_runs_included']:
   eta=item['survival_probability_per_photon_eta'];self.assertAlmostEqual(item['SSR_valid_unconditional_CHSH'],2-4*eta+(3+np.sqrt(2))*eta**2,places=12)
 def test_SSR_loss_threshold(self):self.assertAlmostEqual(self.g['two_copy_particle_SSR_Bell']['fixed_measurements_symmetric_photon_survival_threshold'],4/(3+np.sqrt(2)))
 def test_SSR_no_lost_runs_discarded(self):
  s=self.g['two_copy_particle_SSR_Bell']['loss_with_all_runs_included'];self.assertAlmostEqual(s[0]['SSR_valid_unconditional_CHSH'],2.);self.assertAlmostEqual(s[-1]['SSR_valid_unconditional_CHSH'],1+np.sqrt(2))
 def test_KR_orbit_polynomial_palindrome(self):
  v=self.g['unlabeled_history_group_action_entropy']['unlabeled_history_edge_count_polynomial'];self.assertEqual(v,v[::-1])
 def test_KR_number_orbits(self):self.assertEqual(self.g['unlabeled_history_group_action_entropy']['number_unlabeled_layered_histories'],1240)
 def test_KR_group_order(self):self.assertEqual(self.g['unlabeled_history_group_action_entropy']['G_order'],96)
 def test_KR_one_link_orbits_by_layer(self):
  v=self.g['unlabeled_history_group_action_entropy']['unlabeled_history_edge_count_polynomial'];self.assertEqual(v[1],2)
 def test_KR_groupoid_amplitude_independent_binomial(self):
  v=self.g['unlabeled_history_group_action_entropy'];z=np.exp(1j*v['theta']);a=complex(*v['groupoid_weighted_sum_real_imag']);self.assertLess(abs(a-(1+z)**16/96),1e-12)
 def test_KR_unlabeled_amplitude_not_groupoid_amplitude(self):
  v=self.g['unlabeled_history_group_action_entropy'];self.assertGreater(v['magnitude_ratio_orbit_unweighted_over_groupoid'],1000)
 def test_KR_entropy_64_lowerbound_still_huge(self):
  v=self.g['unlabeled_history_group_action_entropy']['large_N_entropy_bounds'][-1];self.assertGreater(v['log10_orbit_count_lower_bound'],200)
 def test_flavor_anomaly_two_param_zero_with_RH_neutrino(self):self.assertEqual(self.g['anomaly_free_flavor_graph']['with_three_nu_c_two_parameter_cubic_anomaly'],'0')
 def test_flavor_generic_nonzero_cubic_without_RH_neutrinos(self):self.assertIn('648',self.g['anomaly_free_flavor_graph']['without_nu_c_generic_two_parameter_cubic_anomaly'])
 def test_flavor_two_independent_edge_constraints(self):
  v=self.g['anomaly_free_flavor_graph'];self.assertEqual(v['one_Higgs_three_generation_Yukawa_tree_minimum_edges'],2)
 def test_flavor_connected_graph_dim_zero(self):
  for v in self.g['anomaly_free_flavor_graph']['rank_table']:
   if len(v['allowed_offdiagonal_Yukawa_edges'])>=2:self.assertEqual(v['remaining_family_difference_dimension'],0)
 def test_flavor_single_edge_dim_one(self):
  for v in self.g['anomaly_free_flavor_graph']['rank_table']:
   if len(v['allowed_offdiagonal_Yukawa_edges'])==1:self.assertEqual(v['remaining_family_difference_dimension'],1)
 def test_flavor_unbroken_mumu_majorana_forbidden(self):
  v=self.g['anomaly_free_flavor_graph'];self.assertNotIn((1,1),v['unbroken_Lmu_minus_Ltau_allowed_Weinberg_operator_indices'])
 def test_flavor_Weinberg_exact_allowed_e_e_mu_tau(self):
  v=self.g['anomaly_free_flavor_graph'];self.assertEqual(v['unbroken_Lmu_minus_Ltau_allowed_Weinberg_operator_indices'],[(0,0),(1,2)])
 def test_flavor_not_claiming_PMNS_fit(self):self.assertIn('not',self.g['anomaly_free_flavor_graph']['limitation'])

if __name__=='__main__':unittest.main()