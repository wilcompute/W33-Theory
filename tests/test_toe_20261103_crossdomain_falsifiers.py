"""2026-11-03 independent TOE five-front plus outside-box regression.

These run against frozen mathematical and actual CLASS output certificates.
A full CLASS rerun is an independent producer command, not a unit-test side
effect. New tests never assume either a UV completion or likelihood fit.
"""
from pathlib import Path
import json, math, unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'data'/('toe_20261103_'+name+'.json')).read_text())
class CrossDomain(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.w=read('covariant_wkb_and_axion_periodicity')
  cls.r=read('class_PV_real_RSD_singlepoint')
  cls.g=read('gravity_phase_decoherence_null')
  cls.c=read('chiral_topological_resolution_guard')
  cls.p=read('class_growth_nuisance_projection')
 def test01_canonical_two_field_energy_balance(self):
  self.assertIn('COVARIANT',self.w['status'])
  rows=self.w['background_exact_energy_exchange']['redshifts']
  self.assertEqual([r['z'] for r in rows],[0,.25,.5,1,2,5])
  for r in rows:
   self.assertLess(abs(r['Friedmann_Hdot_residual']),1e-10)
   self.assertLess(abs(r['energy_transfer_residual']),1e-10)
   self.assertLess(abs(r['total_continuity_residual']),1e-10)
   self.assertGreater(r['E2'],0)
  self.assertAlmostEqual(rows[0]['E2'],1,places=13)
 def test02_axion_global_periodic_no_go(self):
  q=self.w['compact_axion_mass_periodicity']
  self.assertIn('iff beta=0',q['theorem'])
  self.assertGreater(q['minimum_decay_constants_for_tolerances']['0.01']['minimum_f_over_Mpl_for_at_most_tolerance_slope_drift'],1.9)
  self.assertGreater(q['minimum_decay_constants_for_tolerances']['0.001']['minimum_f_over_Mpl_for_at_most_tolerance_slope_drift'],6)
  for row in q['sampled_mass_monodromy_and_periodicization']:
   self.assertLess(row['exp_mass_monodromy_factor_after_2pi_f'],1)
 def test03_three_actual_class_runs(self):
  models=self.r['models']
  self.assertEqual(len(models),3)
  for m in models:
   self.assertEqual(len(m['spectrum']),7)
   self.assertLess(abs(m['diagnostics']['calibrated_sigma8_z0_vs_CLASS_info_relative_error']),.01)
   self.assertLess(m['diagnostics']['Gaussian_single_point_chi2'],1)
  self.assertGreater(models[0]['diagnostics']['f_sigma8_at_z0p07'],
                     models[1]['diagnostics']['f_sigma8_at_z0p07'])
 def test04_real_PV_RSD_obs_precision(self):
  v=self.r['fading_vs_same_params_zero_cprime_delta_fsigma8']
  self.assertGreater(v,.005)
  self.assertLess(v,.007)
  self.assertLess(v/.055,.2)
  self.assertIn('NO',self.r['real_likelihood_evaluated'])
 def test05_growth_constant_amplitude_projection(self):
  p=self.p
  residual=p['log_growth_relative_scale_residual']
  self.assertAlmostEqual(sum(residual),0,places=12)
  self.assertLess(p['rms_scale_dependent_fractional_response'],1e-5)
  self.assertLess(p['shape_only_chi2_after_exact_constant_amplitude_marginalization'],1e-5)
 def test06_newton_controlled_phase_and_entanglement(self):
  g=self.g;d=g['newton_controlled_phase_radians']
  self.assertAlmostEqual(g['pure_two_qubit_concurrence'],abs(math.sin(d/2)),places=13)
  self.assertAlmostEqual(g['pure_state_entanglement_negativity']*2,
                         g['pure_two_qubit_concurrence'],places=12)
  self.assertGreater(g['independent_local_phase_damping_coherence_threshold'],.6)
 def test07_classical_gravity_inference_boundary(self):
  g=self.g;self.assertIn('not a gravity quantization proof'.lower(),g['scope'].lower())
  comparison=g['phase_structure_identifiability']['multi_distance_normalized_comparison']
  self.assertAlmostEqual(comparison[1]['normalized_yukawa_over_newton'],1,places=12)
  self.assertGreater(max(abs(x['normalized_yukawa_over_newton']-1) for x in comparison),.1)
 def test08_chiral_anomaly_not_topological_index(self):
  c=self.c
  self.assertEqual(c['exotic_sterile_charge_sums'],{'linear':9,'cubic':81,'quadratic':513})
  rows={r['absolute_charge_Q']:r for r in c['charge_resolution_rows']}
  self.assertEqual(rows[15]['minimum_L_for_charge_plaquette_angle_below_pi_over_3'],10)
  self.assertEqual(rows[18]['minimum_L_for_charge_plaquette_angle_below_pi_over_3'],11)
 def test09_dense_algorithm_memory_firewall(self):
  rows={r['absolute_charge_Q']:r for r in self.c['charge_resolution_rows']}
  self.assertGreater(rows[15]['dense_complex128_kernel_GiB'],20)
  self.assertGreater(rows[18]['dense_complex128_kernel_GiB'],40)
  self.assertIn('NOT',self.c['scope'])
 def test10_no_overclaim(self):
  report=(ROOT/'analysis/2026-11-03_cross_domain_TOE_falsifiers.md').read_text().lower()
  for q in ('not a toe','not a complete coupled-ultralight class',
            'not a full rsd likelihood','not a chiral fermion measure',
            'not a theory-independent quantization witness',
            'not a complete quantum-stable uv model'):
   self.assertIn(q,report)
 def test11_respect_published_models(self):
  p=self.w['inputs']
  inp=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
  self.assertAlmostEqual(p['beta'],float(inp['free_neg']['p']['cp']),places=13)
 def test12_numerical_source_file_paths_exist(self):
  for x in ('covariant_wkb_axion_periodicity','class_RSD_PV_holdout',
   'chiral_topological_resolution_guard','gravity_phase_decoherence_null',
   'class_growth_nuisance_projection'):
   self.assertTrue((ROOT/'analysis'/('toe_20261103_'+x+'.py')).is_file())
if __name__=='__main__':unittest.main()
