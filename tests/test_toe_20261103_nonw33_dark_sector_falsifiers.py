"""Focused regression suite for the 2026-11-03 non-W33 dark-sector falsifier.
No external likelihood is rerun. Assertions are mathematical identities,
numerical reproductions and boundary checks against frozen published fits.
"""
import json,math,sys,unittest
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261103_dark_sector_consistency_triangle as tri
import toe_20261103_dark_sector_observable_identifiability as obs
def data(name):
 return json.loads((ROOT/'data'/('toe_20261103_'+name+'.json')).read_text(encoding='utf-8'))
class TOEPhysicsBenchmarks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p=tri.get_inputs()
  cls.a=data('dark_sector_consistency_triangle')
  cls.b=data('dark_sector_observable_identifiability')
 def test_01_provenance_and_fit_sign(self):
  p=self.p
  self.assertGreater(p['beta'],0)
  self.assertAlmostEqual(p['beta'],.05299751293406564,places=12)
  self.assertLess(p['wa'],0)
  self.assertLess(p['fit_delta_chi2_vs_LCDM'],0)
  self.assertEqual(p,self.a['inputs'])
 def test_02_constant_clock_scalar_equation_exact(self):
  p=self.p; s=self.a['constant_clock']['linear_scalar_clock_s_abs']
  for sign in (-1,1):
   for z in (0,.2,1,2,4):
    x=tri.exact_clock(p,sign*s,z)
    self.assertLess(abs(x['kg_residual']),1e-10)
    self.assertLess(abs(x['continuity_residual']),1e-10)
    self.assertGreaterEqual(x['wphi'],-1-1e-13)
    self.assertGreater(x['E2'],0)
    self.assertAlmostEqual(tri.exact_clock(p,sign*s,0)['weff'],p['w0'])
 def test_03_best_CPL_central_shape_not_matched(self):
  t=self.a['constant_clock']
  for row in t['results']:
   self.assertGreater(row['predicted_CPL_wa_tangent_at_today'],0)
   self.assertLess(row['target_CPL_wa'],0)
   self.assertGreater(row['model_w_eff_at_z1'],-1)
   self.assertLess(row['target_CPL_w_at_z1'],-1)
 def test_04_phantom_effective_w_non_ghost_control(self):
  a=tri.exact_clock(self.p,-.02,1)
  self.assertGreater(a['wphi'],-1)
  self.assertLess(a['weff'],-1)
  self.assertGreater(a['potential_density'],0)
 def test_05_phiMDE_analytic_growing_mode_and_bias(self):
  r=self.a['analytic_two_species_growth']
  beta=r['beta'];u=beta**2
  self.assertAlmostEqual(r['growing_CDM_exponent'],1+2*u)
  self.assertAlmostEqual(r['uncoupled_test_baryon_to_CDM_density_contrast'],(3-2*u)/((1+2*u)*(3+2*u)))
  self.assertLess(r['ode_control_max_error'],1e-9)
  self.assertGreater(r['fitted_recombination_to_today_mass_ratio'],1)
 def test_06_boson_wkb_mass_and_loop_window(self):
  a=self.a['oscillating_scalar_candidate']
  self.assertGreater(a['fiducial_dark_scalar_mass_eV'],a['lyalpha_pure_fuzzy_2026_model_dependent_lower_limit_eV'])
  self.assertLess(a['loop_delta_mphi_squared_over_H0_squared'],1e-60)
  self.assertGreater(a['onset_redshift'],1e7)
  self.assertGreater(a['benchmark_redshift_scales'][-1]['mass_over_H'],1e8)
  self.assertLess(a['chi_amplitude_at_onset_over_Mpl'],1)
 def test_07_observable_identifiability_jacobian_and_precision(self):
  r=self.b
  beta=self.p['beta']
  b,x=sp.symbols('beta Delta',real=True)
  J=sp.Matrix([[x,b],[4*b,0]])
  self.assertEqual(str(J.det()),r['exact_jacobian_determinant'])
  self.assertAlmostEqual(r['massless_fifth_force_enhancement_over_newton'],2*beta*beta)
  self.assertAlmostEqual(r['mass_ratio_recombination_over_today'],
                         self.a['analytic_two_species_growth']['fitted_recombination_to_today_mass_ratio'])
 def test_08_two_scale_yukawa_inverse_control(self):
  r=self.b['two_scale_massive_yukawa_control']
  self.assertAlmostEqual(r['recovered_beta'],self.p['beta'],places=13)
  self.assertAlmostEqual(r['recovered_mu'],r['hypothetical_mu_h_per_Mpc'],places=13)
  self.assertGreater(r['k_samples'][1]['g_eff_minus_1'],r['k_samples'][0]['g_eff_minus_1'])
 def test_09_model_scope_and_ownership(self):
  s=(ROOT/'analysis/2026-11-03_non_W33_dark_sector_independent_falsifiers.md').read_text(encoding='utf-8').lower()
  for phrase in ('not an observational likelihood exclusion','not a new discovery','not a toe','not a fit for interacting fuzzy dark matter','preserved'):
   self.assertIn(phrase,s)
if __name__=='__main__':unittest.main()
