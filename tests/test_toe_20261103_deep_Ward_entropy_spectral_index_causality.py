"""Regression suite for six original independent TOE deep-pattern tests.

The expensive modified-CLASS and large sparse-Krylov producers were already
executed on the user's authorized computer, not rerun by this suite.
"""
from pathlib import Path
import json,math,sys,unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
def load(n):return json.loads((ROOT/'data'/('toe_20261103_'+n+'.json')).read_text())
class DeepTOE(unittest.TestCase):
 @classmethod
 def setUpClass(c):
  c.w=load('hyperbolic_isometry_ward')
  c.f=load('W33_fiber_4D_continuum_scale')
  c.e=load('CLASS_gauge_invariant_species_entropy')
  c.q=load('Q15_krylov_sign_action')
  c.r=load('retarded_gravity_frequency_null')
  c.j=load('ultralight_wave_Jeans_clock')
 def test01_exact_hyperbolic_killing(self):
  self.assertIn('PASS_EXACT_HYPERBOLIC',self.w['status'])
  self.assertEqual(self.w['symbolic_Lie_K_metric'],[['0','0'],['0','0']])
  self.assertEqual(self.w['exact_scalar_curvature_over_1_over_Mpl_squared'],'-2*beta**2')
 def test02_hyperbolic_protected_mass_cannot_fade(self):
  self.assertEqual(self.w['finite_isometry_pulledback_metric_ratio'],'1')
  self.assertEqual(self.w['finite_isometry_dark_mass_potential_ratio'],'exp(-2*a*gamma)')
  self.assertEqual(self.w['finite_isometry_rolling_potential_ratio'],'exp(-a*lam)')
  self.assertIn('gamma=0 and lambda=0',self.w['theorem'])
 def test03_W33_exact_srg_and_eigenspaces(self):
  from toe_20261103_W33_fiber_4D_continuum_scale import w33
  A=w33()
  self.assertEqual(A.shape,(40,40))
  self.assertEqual(int(A.sum()),480)
  self.assertEqual(self.f['adjacency_spec']['2'],24)
  self.assertEqual(self.f['lap_spec']['10'],24)
 def test04_W33_base_continuum_scale(self):
  self.assertAlmostEqual(self.f['regular_graph_normalized_gap'],5/6,places=14)
  rows=self.f['rows']
  self.assertLess(rows[-1]['normalized_product_first_eigenvalue'],rows[0]['normalized_product_first_eigenvalue'])
  self.assertAlmostEqual(rows[-1]['physical_base_first_mass_squared_if_a_phys_length_over_L'],4*math.pi**2,delta=.1)
  self.assertEqual(rows[-1]['physical_internal_mass_squared_if_a_phys_length_over_L_and_standard_kinetic_operator'],23040)
 def test05_normalized_W3q_gap_not_continuum(self):
  rows=self.f['q_GQ_bare_graph_normalized_gap_tower']
  self.assertEqual(rows[0]['q'],3)
  self.assertGreater(rows[-1]['normalized_point_graph_gap'],.96)
 def test06_actual_CLASS_entropy_background_ward(self):
  self.assertIn('REAL_CLASS',self.e['status'])
  fading=self.e['summary'][0]['z0_k0p1'];off=self.e['summary'][1]['z0_k0p1']
  self.assertAlmostEqual(fading['baryon_rho_log_derivative'],-3,delta=1e-6)
  self.assertAlmostEqual(fading['effective_mass_log_derivative_minus_dlnm_over_dN'],
                         fading['beta_times_phi_N_if_fading'],delta=1e-6)
  self.assertAlmostEqual(off['CDM_rho_log_derivative'],-3,delta=1e-6)
 def test07_actual_CLASS_entropy_gauge(self):
  for run in self.e['runs']:
   self.assertEqual(len(run['results']),8)
   for row in run['results']:
    self.assertLess(row['Sbc_gauge_transform_absolute_error'],1e-9)
  fading=self.e['summary'][0]['z0_k0p1']
  self.assertGreater(abs(fading['gauge_invariant_Sbc_over_delta_c']),
                     abs(fading['delta_b_minus_delta_c_over_delta_c']))
  self.assertGreater(abs(fading['raw_diff_under_gauge_shift_relative_change']),1e-4)
 def test08_sbc_normalization_not_gauge_invariant(self):
  self.assertIn('S_bc/delta_c are NOT themselves gauge invariant',self.e['scope'])
  faded=self.e['summary'][0]['z0_k0p1']
  self.assertAlmostEqual(faded['delta_b_over_delta_c'],.9880147973233715,places=8)
  self.assertAlmostEqual(faded['gauge_invariant_Sbc_over_delta_c'],-.020363683886920843,places=7)
 def test09_large_chiral_sparse_sign_action(self):
  self.assertEqual(self.q['dimension'],40000)
  self.assertEqual(self.q['nonzeros'],680000)
  self.assertEqual([x['m'] for x in self.q['krylov_m_comparisons']],[24,48,72,96,128])
  self.assertLess(self.q['approx_sign_H_squared_on_single_vector_relative_error'],1e-5)
  self.assertLess(self.q['approx_sign_H_gauge_transform_vector_relative_defect'],1e-11)
 def test10_L10_gap_is_not_certified(self):
  self.assertTrue(all(v>.001 for v in self.q['H2_ritz_residual_norms']))
  self.assertIn('NOT a rigorous gap lower bound',self.q['spectral_scope'])
  self.assertIn('not numerically established',self.q['index_scope'])
 def test11_UL_JEANS_oscillating_scalar_units(self):
  self.assertIn('PASS_DIMENSIONFUL',self.j['status'])
  self.assertAlmostEqual(self.j['m_recombination_over_today_from_actual_fitted_field_excursion'],1.0149281190426924,places=9)
  r=self.j['table']
  self.assertGreater(r[0]['kJeans_h_Mpc'],900)
  self.assertGreater(r[1]['kJeans_h_Mpc'],150)
  self.assertLess(r[1]['kJeans_h_Mpc'],180)
 def test12_UL_Jeans_crossing_small_modes(self):
  a,b=self.j['table']
  self.assertLess(a['checks_k_over_kJeans_to_fourth']['0.2'],1e-12)
  self.assertGreater(b['checks_k_over_kJeans_to_fourth']['500'],1)
  self.assertLess(a['checks_k_over_kJeans_to_fourth']['500'],1)
  self.assertAlmostEqual(self.j['Jeans_fractional_shift_at_recombination_due_only_to_mass_variation'],.01117532608180527,places=9)
 def test13_retarded_static_delay_and_bandwidth(self):
  r=self.r
  self.assertAlmostEqual(r['light_propagation_delay_seconds'],200e-6/299792458.,places=18)
  self.assertGreater(r['massless_source_modulation_frequency_for_0p01_rad_phase_lag_Hz'],2e9)
  self.assertGreater(r['Yukawa_evanescent_to_propagating_frequency_Hz'],3e11)
 def test14_retarded_1kHz_non_quantum_witness(self):
  r=self.r
  entry=next(x for x in r['frequency_table'] if x['modulation_frequency_Hz']==1000)
  self.assertLess(entry['massless_retarded_phase_lag_rad'],5e-9)
  self.assertIn('not a proof',r['scope'])
 def test15_producer_and_certificate_names(self):
  names=['hyperbolic_isometry_ward','W33_fiber_4D_continuum_scale',
         'CLASS_gauge_invariant_species_entropy','Q15_krylov_sign_action',
         'retarded_gravity_frequency_null','ultralight_wave_Jeans_clock']
  for name in names:
   self.assertTrue((ROOT/'analysis'/('toe_20261103_'+name+'.py')).is_file())
   self.assertTrue((ROOT/'data'/('toe_20261103_'+name+'.json')).is_file())
 def test16_report_not_a_TOE_and_ownership(self):
  s=(ROOT/'analysis/2026-11-03_toe_deep_Ward_entropy_spectral_index_causality.md').read_text(encoding='utf-8').lower()
  for p in ('no theory of everything','no full monorepo suite',
    'not a new discovery','global chiral weyl measure',
    'not a radiation-era boltzmann substitute',
    'no common local quantum action','full class axion perturbation hierarchy'):
   self.assertIn(p,s)
if __name__=='__main__':unittest.main()
