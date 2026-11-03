"""Regression tests for non-W33 TOE research, 2026-11-03 late pass.
One real 3-run CLASS transfer certificate is frozen; unittest validates it but
does not re-run CLASS in every Python test (producer runs in Ubuntu WSL).
"""
import unittest,json,math,sys
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261103_ultralight_subhorizon_growth_controls as U
def read(name):return json.loads((ROOT/'data'/('toe_20261103_'+name+'.json')).read_text(encoding='utf-8'))
class EightFronts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.g=read('ultralight_subhorizon_growth_controls')
  cls.c=read('real_CLASS_fading_species_transfers')
  cls.n=read('chiral_messenger_naturalness_floor')
  cls.m=read('model_selection_guard')
  cls.v=read('ultralight_uv_density_clock')
 def test01_class_real_outputs_present(self):
  c=self.c;self.assertIn('REAL_PATCHED_CLASS',c['status'])
  self.assertEqual(len(c['runs']),3)
  self.assertTrue(all(len(z['redshifts'])==5 for z in c['runs']))
  self.assertEqual([z['z'] for z in c['runs'][0]['redshifts']],[0,.5,1,2,5])
  self.assertAlmostEqual(c['runs'][0]['full_spectrum_CLASS_info']['s8'],.825051,places=6)
 def test02_class_baryon_transfer_response(self):
  c=self.c['k_diagnostics']
  for z in c[:3]:
   self.assertLess(z['fading_baryon_to_CDM_z0'],z['cp0_baryon_to_CDM_z0'])
   self.assertGreater(z['fading_vs_cp0_normalized_z5_to_z0_growth_ratio'],1.002)
   self.assertLess(z['fading_vs_cp0_normalized_z5_to_z0_growth_ratio'],1.005)
 def test03_class_transfer_reproducibility_normalization(self):
  c=self.c
  for krec in c['k_diagnostics']:
   k=str(krec['k_h_per_Mpc'])
   a=c['runs'][0]['redshifts'];b=c['runs'][1]['redshifts']
   t=(a[0][k]['d_m']/a[4][k]['d_m'])/(b[0][k]['d_m']/b[4][k]['d_m'])
   self.assertAlmostEqual(t,krec['fading_vs_cp0_normalized_z5_to_z0_growth_ratio'],places=12)
 def test04_subhorizon_ula_pressure_controls(self):
  reg=self.g['results']
  self.assertEqual(len(reg),7)
  k=.2
  row=next(z for z in reg if z['k_h_per_Mpc']==k)
  self.assertAlmostEqual(row['uncoupled_ultralight']['0.0']['delta_c'],
                         row['pressureless_uncoupled']['0.0']['delta_c'],delta=1e-7)
  last=reg[-1]
  self.assertLess(last['uncoupled_ultralight']['0.0']['delta_c']/last['pressureless_uncoupled']['0.0']['delta_c'],.99)
 def test05_ultralight_mass_and_recombination_clock(self):
  self.assertAlmostEqual(self.g['mass_ratio_recombination_to_today'],self.v['mass_ratio_rec_over_today'],places=12)
  self.assertAlmostEqual(self.v['field_envelope_correction_rec_to_constant_mass_dust']**2*
                         self.v['mass_ratio_rec_over_today'],1.,places=13)
 def test06_adiabatic_medium_curvature(self):
  v=self.v;b=v['beta']
  p=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
  f=p['free_neg']['p'];omc=f['wc']/f['h']**2
  self.assertAlmostEqual(v['adiabatic_moduli_density_curvature_in_H0_squared_today'],3*b*b*omc,places=12)
  self.assertAlmostEqual(v['fixed_chi_field_quadratic_curvature_in_H0_squared_today'],
                          2*v['adiabatic_moduli_density_curvature_in_H0_squared_today'],places=12)
 def test07_boson_loop_naturalness_not_observation(self):
  self.assertLess(self.v['one_loop_mchi_1e_minus20_eV_curvature_over_H0_squared'],1e-70)
  self.assertIn('scheme',self.v['limitations'])
 def test08_chiral_anomaly_and_messenger_floor(self):
  n=self.n;self.assertEqual(n['three_generation_SM_linear_and_cubic'],[-9,-81])
  self.assertEqual(n['singlet_linear_cubic'],[9,81])
  self.assertEqual(n['mixed_Y_squared_Q_and_Y_Q_squared'],[0,0])
  rows=n['naturalness_cases']
  self.assertAlmostEqual(rows[1]['largest_M_for_threshold_less_mh_squared_GeV']/
                         rows[0]['largest_M_for_threshold_less_mh_squared_GeV'],.1)
  self.assertGreater(rows[0]['minimum_threshold_over_higgs_mass_squared'],1)
 def test09_U1_landau_and_clock_threshold(self):
  v=self.v;self.assertLess(v['allowed_beta_alpha_over_beta_dark_using_older_fit_clock'],2e-6)
  rows=v['eV_to_GeV_thresholds_illustrative']
  self.assertTrue(rows[0]['pole_above_reduced_Planck_mass'])
  self.assertFalse(rows[2]['pole_above_reduced_Planck_mass'])
  self.assertLess(rows[-1]['largest_g_at_1e16_for_pole_above_planck'],.4)
 def test10_model_selection_aic_bic_N_guard(self):
  m=self.m
  self.assertAlmostEqual(m['fading_minus_LCDM_delta_chi2'],sum(m['group_contributions_fading_minus_LCDM_same_joint_fit'].values()),places=8)
  self.assertLess(m['delta_AIC_fading_minus_LCDM'],0)
  self.assertLess(m['BIC_independent_observation_threshold_for_fading_preference'],210)
  self.assertGreater(m['BIC_independent_observation_threshold_for_fading_preference'],200)
  self.assertIn('NOT_PERFORMED',m['holdout_validation'])
 def test11_consistency_of_staged_producers(self):
  for f in ('ultralight_subhorizon_growth_controls','real_CLASS_fading_species_transfers',
            'chiral_messenger_naturalness_floor','model_selection_guard','ultralight_uv_density_clock'):
   self.assertTrue((ROOT/'analysis'/('toe_20261103_'+f+'.py')).is_file())
 def test12_physics_boundary_labels_report(self):
  report=(ROOT/'analysis/2026-11-03_eight_fronts_class_ultralight_uv_falsifiers.md').read_text(encoding='utf-8').lower()
  for phrase in ('not a toe','not a new likelihood fit','not a fully coupled ultralight class',
                 'not a bayes factor','not a global anomaly-free chiral lattice measure'):
   self.assertIn(phrase,report)
if __name__=='__main__':unittest.main()
