"""Independent focused certifications for 2026-11-03 Pascal/symplectic portal tests.

Heavy ARPACK eigen-solves are producers; these tests verify their frozen
certificates and cross-check exact finite formulae independently.
"""
from pathlib import Path
import math,json,unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def load(stem):
    return json.loads((ROOT/'data'/('toe_20261103_'+stem+'.json')).read_text())
class PascalPortal(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
    names=['q_pascal_symplectic_scale_selector','pascal_codim_two_portal_bridge',
      'pascal_portal_sparse_spectrum','pascal_lucas_rg_hierarchy',
      'pascal_portal_two_sector_resolvent','symplectic_pascal_gate_singularity',
      'symplectic_plane_logarithmic_mass_nogo','W33_local_line_variance_action',
      'pascal_portal_dimension_no_go']
    cls.results={name:load(name) for name in names}
 def test01_q_pascal_q3_geometry(self):
    p=self.results['q_pascal_symplectic_scale_selector']
    row=next(r for r in p['projective_and_symplectic_rows'] if r['q']==3)
    self.assertEqual((row['projective_points'],row['Gaussian_4_2_all_two_spaces'],row['symplectic_isotropic_two_spaces']),(40,130,40))
    self.assertEqual(row['isotropic_fraction'],'4/13')
 def test02_other_q_invalidate_uniqueness(self):
    rows=self.results['q_pascal_symplectic_scale_selector']['projective_and_symplectic_rows']
    self.assertEqual([r['q'] for r in rows],[2,3,5,7])
    for r in rows:self.assertEqual(r['symplectic_isotropic_two_spaces'],r['projective_points'])
 def test03_weighted_pascal_growth_is_nonunique(self):
    rows=self.results['q_pascal_symplectic_scale_selector']['constants']['weighted_fibonacci_generalization']
    self.assertEqual(len(rows),5)
    v={r['diagonal_weight_x']:r['analytic_Perron_root'] for r in rows}
    self.assertAlmostEqual(v['1'],(1+math.sqrt(5))/2)
    self.assertAlmostEqual(v['2'],2.0)
    self.assertGreater(v['3'],2)
 def test04_pi_triangular_correct_exact(self):
    p=self.results['q_pascal_symplectic_scale_selector']['constants']
    self.assertEqual(p['triangular_inverse_square_exact_formula'],'4*pi**2/3 -12')
    self.assertAlmostEqual(float(p['triangular_inverse_square_sum']),4*math.pi**2/3-12,places=12)
    self.assertNotAlmostEqual(float(p['triangular_inverse_square_sum']),4*math.pi**2/3-6,places=1)
 def test05_e_row_product_ratios(self):
    rows=self.results['q_pascal_symplectic_scale_selector']['constants']['Euler_row_product_cross_ratios']
    self.assertAlmostEqual(rows[-1]['approx'],(25/24)**24,places=12)
    self.assertTrue(all(rows[i+1]['error_to_e']<rows[i]['error_to_e'] for i in range(len(rows)-1)))
 def test06_codimension_two_4D_energy(self):
    p=self.results['pascal_codim_two_portal_bridge']
    self.assertEqual(p['symplectic_selector_fraction_c'],4/13)
    self.assertAlmostEqual(p['W33_internal_Laplacian_eigenspaces']['10'],24)
    for r in p['Bernoulli_portal_trials']:
     self.assertAlmostEqual(r['positive_low_mode_W33_24sector_mass_squared_in_unit_R'],40/13)
     self.assertAlmostEqual(r['expected_portal_count'],(4/13)*r['L']**2)
 def test07_Bernoulli_concentration(self):
    rows=self.results['pascal_codim_two_portal_bridge']['Bernoulli_portal_trials']
    self.assertLess(rows[-1]['measured_effective_c_std'],rows[0]['measured_effective_c_std'])
    self.assertLess(abs(rows[-1]['measured_effective_c']-4/13),.004)
 def test08_unfiltered_mod3_pascal_doesnt_have_D2(self):
    x=self.results['pascal_lucas_rg_hierarchy']['p_prime_fractal_rows'][1]
    self.assertEqual(x['p'],3)
    self.assertAlmostEqual(x['Hausdorff_box_dimension'],math.log(6)/math.log(3))
    self.assertLess(x['Hausdorff_box_dimension'],2)
    self.assertEqual(x['finite_depth_checks'][2]['actual_nonzero_binomials_mod_p'],216)
 def test09_RG_exponent_doesnt_select_g(self):
    r=self.results['pascal_lucas_rg_hierarchy']['RG_transmutation']
    ratios=[x['Lambda_over_mu_reference'] for x in r['coupling_sensitivity_table']]
    self.assertTrue(all(x<y for x,y in zip(ratios,ratios[1:])))
    self.assertLess(r['tempting_unjustified_g2_equals_inverse_40']['scale_ratio'],1e-150)
 def test10_sparse_true_spectrum_not_meanfield(self):
    rows=self.results['pascal_portal_sparse_spectrum']['rows']
    self.assertEqual(len(rows),10)
    for row in rows:
      self.assertLess(row['lowest_actual_sparse_mass_squared'],row['mean_field_constant_Rayleigh_mass_squared'])
      self.assertGreater(row['lowest_actual_sparse_mass_squared'],0)
 def test11_two_sector_scattering(self):
    r=self.results['pascal_portal_two_sector_resolvent']
    self.assertEqual(len(r['comparison_rows']),18)
    self.assertLess(r['maximum_relative_Tmatrix_error_18_sample_eigenvalues'],.024)
    self.assertGreater(r['L32_Green_approximated_two_sector_gap']['16']['m2'],r['L32_Green_approximated_two_sector_gap']['10']['m2'])
 def test12_critical_9_over_81_symplectic_gate(self):
    r=self.results['symplectic_pascal_gate_singularity']
    self.assertEqual(r['symplectic_isotropic_2planes_q3'],40)
    self.assertEqual(r['accepted_digit_vectors_per_lagrangian_plane'],9)
    self.assertEqual(r['all_digit_vectors_F3_4'],81)
    for row in r['fixed_Lagrangian_plane_samples']:
      self.assertEqual(row['symplectic_digit_rule_accepted_cells'],row['L']**2)
 def test13_fixed_gate_is_not_four_dimensional_homogeneous(self):
    r=self.results['symplectic_pascal_gate_singularity']
    for row in r['fixed_Lagrangian_plane_samples']:
      self.assertAlmostEqual(row['discrepancy_from_homogeneous_4D_volume'],.3)
    for row in r['regular_distributed_grid_samples']:
      self.assertAlmostEqual(row['smooth_profile_mean'],1.)
 def test14_fixed_plane_mass_log_goes_zero(self):
    r=self.results['symplectic_plane_logarithmic_mass_nogo']
    rows=r['fixed_plane_transverse_Green_rows']
    self.assertGreater(rows[0]['m2_actual_fixed_plane'],rows[-1]['m2_actual_fixed_plane'])
    self.assertLess(rows[-1]['m2_actual_fixed_plane'],.84)
    self.assertGreater(rows[-1]['G2'],1)
    self.assertAlmostEqual(rows[-1]['G2']/math.log(rows[-1]['L']),1/(2*math.pi),delta=.01)
 def test15_exact_periodic_distributed_spectrum_differs(self):
    r=self.results['symplectic_plane_logarithmic_mass_nogo']
    for row in r['same_number_distributed_grid_4D_sparse_comparison']:
      self.assertGreater(row['physical_m2_distributed_exact_sparse'],row['fixed_plane_at_same_L'])
      self.assertAlmostEqual(row['identical_constant_Rayleigh'],10)
 def test16_exact_W33_line_local_action(self):
    p=self.results['W33_local_line_variance_action']
    for r in p['rows']:
      self.assertTrue(r['graph_Laplacian_equals_scaled_sum_of_local_centered_line_projectors'])
      self.assertAlmostEqual(r['local_variance_energy_identity_numerical_residual'],0.)
    self.assertEqual(p['rows'][0]['graph_eigen_laplacian'],{'0':1,'10':24,'16':15})
 def test17_incidence_blind_15_prior_art(self):
    r=self.results['W33_local_line_variance_action']['rows'][0]
    self.assertEqual(r['rank_point_to_line_incidence'],25)
    self.assertEqual(r['incidence_dark_kernel_dimension'],15)
    self.assertIn('pass4956',self.results['W33_local_line_variance_action']['prior_owner'].lower())
 def test18_q_not_selected_by_selector_ratio(self):
    r=self.results['pascal_portal_dimension_no_go']['rows']
    byq={row['q']:row['line_selector_fraction_c'] for row in r}
    self.assertGreater(byq[2],byq[3])
    self.assertGreater(byq[3],byq[5])
    self.assertGreater(byq[5],byq[7])
 def test19_spacetime_dimension_not_selected(self):
    r=self.results['pascal_portal_dimension_no_go']['rows']
    rows=[x for x in r if x['q']==3]
    self.assertEqual([x['dimension_d'] for x in rows],[2,3,4,5,6])
    self.assertTrue(all(abs(x['mean_effective_mass_squared']-40/13)<1e-12 for x in rows))
    self.assertGreater(rows[0]['coefficient_of_variation'],rows[-1]['coefficient_of_variation'])
 def test20_report_scope_firewall(self):
    s=(ROOT/'analysis/2026-11-03_pascal_symplectic_critical_portal_scale_test.md').read_text(encoding='utf-8').lower()
    for term in ('not a theory of everything','not a physical mass prediction',
         'pascal itself does not uniquely','logarithmic','homogenization','pass4956',
         'no unique d=4','not a proved'):
      self.assertIn(term,s)
 def test21_sources_and_data_exist(self):
    for name in self.results:
      self.assertTrue((ROOT/'analysis'/('toe_20261103_'+name+'.py')).exists())
      self.assertTrue((ROOT/'data'/('toe_20261103_'+name+'.json')).exists())
if __name__=='__main__':unittest.main()
