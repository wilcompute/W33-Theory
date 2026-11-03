"""Focused Nov 3 TOE five-front regression and certification, no background work.

Heavy producers (four patched CLASS calculations and exact frequency-resolved
KG) are rerun separately; these tests verify the committed frozen results.
"""
from pathlib import Path
import math,json,unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def read(k):return json.loads((ROOT/'data'/('toe_20261103_'+k+'.json')).read_text())
class TOE5(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.l=read('class_lensing_growth_jacobian')
  cls.t=read('class_lensing_tilt_projection')
  cls.w=read('exact_kg_wkb_crosscheck')
  cls.s=read('sparse_exotic_chiral_q15')
  cls.u=read('compact_two_function_uv_window')
  cls.g=read('gravity_multidistance_nuisance_design')
 def test01_real_CLASS_cmb_phi_metadata(self):
  self.assertIn('REAL_CLASS',self.l['status'])
  self.assertEqual(len(self.l['models']),3)
  self.assertEqual(len(self.l['observables']),6)
  self.assertEqual(self.l['models'][0]['file_header_column'],'phiphi')
 def test02_real_CLASS_lensing_fractional_change(self):
  vals=self.l['observables']
  self.assertAlmostEqual(vals[0]['lens_relative_coupling_effect_percent'],1.1175607389581454,places=8)
  self.assertAlmostEqual(vals[-1]['lens_relative_coupling_effect_percent'],2.77965595025631,places=8)
  self.assertTrue(all(x['lens_relative_coupling_effect_percent']>0 for x in vals))
 def test03_fitted_primordial_lnAs_is_proportional(self):
  for row in self.l['observables']:
   self.assertAlmostEqual(row['derivative_logC_to_lnAs_finite'],1.,places=7)
 def test04_primordial_tilt_projection(self):
  self.assertIn('THREE_PARAMETER',self.t['status'])
  self.assertEqual(self.t['actual_runs'],4)
  self.assertGreater(self.t['lensing_response_removed_by_amplitude_and_tilt'],.9998)
  self.assertGreater(self.t['projected_Cprime_1sigma_illustrative'],.7)
  self.assertLess(max(abs(x) for x in self.t['full_cp_change_logC_residual_after_amplitude_and_ns_fit']),.0005)
 def test05_primordial_linear_projection_orthogonality(self):
  J=np.array(self.t['Jacobian'])
  r=np.array(self.t['projected_cprime_response'])
  self.assertLess(abs(r@J[:,1]),1e-12)
  self.assertLess(abs(r@J[:,2]),1e-12)
  v=self.t['eigenvalues_1pct_fisher'];self.assertGreater(min(v),0)
 def test06_Klein_Gordon_full_oscillator_comparators(self):
  w=self.w
  self.assertIn('EXACT_KLEIN',w['status'])
  rows=w['runs'];self.assertEqual(len(rows),4)
  self.assertEqual([x['m_over_H_today'] for x in rows],[20,40,80,160])
  self.assertTrue(all(x['canonical_corrected_action_relative_drift']<.002 for x in rows))
 def test07_canonical_action_vs_naive(self):
  rows=self.w['runs']
  for r in rows:
   self.assertLess(r['canonical_corrected_late_action_5to95_fractional_spread'],
                   r['late_invariant_5_to95_percent_fractional_spread'])
  self.assertLess(rows[-1]['canonical_corrected_action_relative_drift'],1e-4)
  self.assertGreater(rows[1]['relative_final_to_initial_WKB_number_drift'],.05)
 def test08_sparse_real_Q15_dimensions(self):
  s=self.s['rows'];last=s[-1]
  self.assertEqual(last['charge_Q'],15)
  self.assertEqual(last['L'],10)
  self.assertEqual(last['matrix_dimension'],40000)
  self.assertEqual(last['nonzeros'],680000)
  self.assertLess(last['sparse_memory_MiB'],14)
  self.assertGreater(last['compared_dense_GiB'],23)
 def test09_sparse_large_Q15_gauge_covariance(self):
  for row in self.s['rows']:
   self.assertLess(row['hermitian_max_entry_defect'],1e-12)
   self.assertLess(row['gauge_covariance_probe_relative_residual'],1e-12)
 def test10_sparse_small_L_overlap_index_control(self):
  row=self.s['rows'][0]
  self.assertEqual(abs(row['exact_dense_L3_index']),1)
  self.assertAlmostEqual(row['sparse_min_abs_eigen_estimate'],row['exact_dense_min_abs_eigen'],places=8)
 def test11_global_compact_potential_obstruction(self):
  u=self.u
  self.assertIn('EXACT exp(-lambda',u['exact_global_no_go'])
  self.assertEqual(len(u['models']),5)
  for r in u['noncompact_exact_exponential_turn_monodromy']:
   self.assertLess(r['V_exp_after_one_compact_turn_over_before'],1)
   self.assertLess(r['m_exp_after_one_compact_turn_over_before'],1)
 def test12_periodic_coupled_background_Einstein(self):
  models=self.u['models'];non=models[0]
  for model in models:
   self.assertEqual(len(model['samples']),5)
   self.assertTrue(all(abs(row['Friedmann_Raychaudhuri_residual'])<1e-9 for row in model['samples']))
   self.assertTrue(all(row['w_phi']>=-1-1e-12 for row in model['samples']))
  self.assertGreater(abs(models[1]['samples'][2]['E2']-non['samples'][2]['E2']),.01)
 def test13_heavy_loop_naturalness_condition_scope(self):
  heavy=self.u['heavy_one_loop_naturalness_thresholds']
  row=next(x for x in heavy if x['one_real_boson_mass_eV']==1e12)
  self.assertLess(row['maximum_dimensionless_exponential_phi_mass_slope_to_keep_abs_one_loop_mphi_squared_below_H0_squared'],4e-29)
  self.assertIn('NOT an observational',self.u['loop_threshold'])
 def test14_gravity_design_optimal_and_nuisance(self):
  g=self.g;opt=g['best_four_distance_vs_Yukawa_plus_constant']
  nuisance=g['same_best_design_with_additional_inverse_cube_nuisance']
  self.assertEqual([round(x*1e6) for x in opt['ds_m']],[150,200,225,500])
  self.assertLess(opt['l2_residual_phase_radians']/.01,1)
  self.assertLess(nuisance['l2_residual_phase_radians']/.01,.1)
  self.assertLess(nuisance['l2_residual_phase_radians'],opt['l2_residual_phase_radians'])
 def test15_gravity_clock_and_quantum_scope(self):
  self.assertAlmostEqual(self.g['clock_gravity_shift_one_meter_near_earth'],1.0911369672198217e-16,places=23)
  self.assertIn('no quantum clock device',self.g['scope'].lower())
 def test16_report_limitation_firewalls(self):
  s=(ROOT/'analysis/2026-11-03_lensing_tilt_sparse_q15_and_wkb_TOE_fronts.md').read_text().lower()
  for phrase in ('no toe was proved','no full radiation-era coupled ultralight class','not a globally invariant weyl measure',
    'no full repository suite','neither actual lensing survey data','not a proof'):
   self.assertIn(phrase,s)
 def test17_all_producers_present(self):
  for name in ('class_lensing_growth_jacobian','class_lensing_tilt_projection','exact_kg_wkb_crosscheck',
   'sparse_exotic_chiral_q15','compact_two_function_uv_window','gravity_multidistance_nuisance_design'):
   self.assertTrue((ROOT/'analysis'/('toe_20261103_'+name+'.py')).exists())
if __name__=='__main__':unittest.main()
