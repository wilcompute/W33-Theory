"""Nov 2 local / Nov 3 UTC: exact and numerical regression certificate.
Uses frozen producer JSON, plus independent integer determinant and Shannon
probability normalization checks. Heavy 7140-trade and 45-mask producers
are reproducible separately but not rerun on each test invocation.
"""
import json,math,unittest
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
def read(tag):
 return json.loads((ROOT/'data'/('w33_20261102_'+tag+'.json')).read_text(encoding='utf-8'))
class EightFronts(unittest.TestCase):
 def test01_phase_signature_theorem(self):
  r=read('phase_signature_no_go_4bit')
  t=r['rigorous_upper_bounds']
  self.assertEqual([(t[str(b)]['forced_blind_imaginary_pairs'],t[str(b)]['hermitian_rank_upper_bound']) for b in (2,3,4)],
                   [(60,516),(8,568),(0,576)])
  self.assertEqual(r['four_bit_hermitian_rank'],576)
  self.assertGreater(r['constructive_four_bit_candidate']['min_eigenvalue'],8e-6)
  z=r['constructive_four_bit_candidate']
  tags=list(zip([x%8 for x in z['phase_mask_1']],[x%8 for x in z['phase_mask_2']]))
  self.assertEqual(len(set(tags)),24)
 def test02_exact_cubic_eiconal_pencil_rank4(self):
  r=read('exact_eiconal_cubic_pencil_obstruction')
  self.assertEqual(r['rank_of_linearized_eiconal_constraints'],4)
  z=r['four_row_determinant_certificate']
  rows=[r['integer_samples'][i] for i in z['row_indices']]
  M=sp.Matrix([[*t['grad_quartic_coefficients'],-t['norm_quartic']] for t in rows])
  self.assertEqual(str(int(M.det())),z['integer_determinant'])
  self.assertTrue(r['both_cubics_harmonic'])
 def test03_exact_W33_scalar_isotropy(self):
  r=read('exact_isotropic_3deck_scalar_wave')
  self.assertEqual(r['exact_low_band_quadratic_tensor'],[['67/38400','0','0'],['0','67/38400','0'],['0','0','67/38400']])
  self.assertEqual(r['effective_resistance_matrix'][0],['39/20','0','0'])
  self.assertLess(max(abs(z['scalar_wave_speed_ratio']-1) for z in r['small_k_numeric_controls']),.002)
 def test04_q13_exact_symplectic_trade_search(self):
  r=read('q13_transvection_trades')
  self.assertEqual(r['total_tested_transvections'],7140)
  for c in r['trade_summary']:
   self.assertEqual(c['max_overlap'],24)
   self.assertEqual(sum(c['overlap_histogram'].values()),2380)
  self.assertEqual(r['best_distinct_symmetric_difference']['xor_weight'],272)
  self.assertFalse(r['improved_upper_bound'])
 def test05_Holevo_and_exact_transition_distribution(self):
  r=read('216_route_holevo_capacity')
  h={int(k):v for k,v in r['single_row_numerators_histogram'].items()}
  self.assertEqual(h,{16:100,64:95,256:20,1600:1})
  self.assertEqual(sum(h.values()),216)
  self.assertEqual(sum(k*v for k,v in h.items()),14400)
  p=[k/14400 for k,n in h.items() for _ in range(n)]
  I=math.log2(216)+sum(x*math.log2(x) for x in p)
  self.assertAlmostEqual(I,r['matched_route_alphabet_classical_channel_capacity_bits_per_detected_photon'],places=12)
  self.assertLess(I,math.log2(24))
 def test06_4bit_loss_Fisher(self):
  r=read('fourbit_loss_fisher')
  groups={z['profile']:z for z in r['detector_efficiency_fisher_cases']}
  self.assertLess(groups['ideal']['launch_photons_per_setting_for_0p01_sd_CRB'],groups['uniform_0p70']['launch_photons_per_setting_for_0p01_sd_CRB'])
  self.assertLess(groups['uniform_0p70']['launch_photons_per_setting_for_0p01_sd_CRB'],groups['variable_0p35_to_0p90']['launch_photons_per_setting_for_0p01_sd_CRB'])
 def test07_q9_formal_Galois_Field_explicit(self):
  s=(ROOT/'lean/W33Q9ProjectiveSquareClass.lean').read_text(encoding='utf-8')
  for word in ('i_squared_minus_one','mul_assoc','distrib','nonzero_has_inverse','four_nonzero_squares','projective_square_class_well_defined'):
   self.assertIn(word,s)
  self.assertNotIn(':= by sorry',s)
 def test08_provenance_and_physics_boundaries(self):
  s=(ROOT/'analysis/2026-11-02_eight_fronts_fourbit_eiconal_q13_wave_capacity.md').read_text(encoding='utf-8')
  for term in ('Tkachev','Holevo','not a global minimum proof','not a 27D Albert no-go','measured value of c'):
   self.assertIn(term.lower(),s.lower())
if __name__=='__main__':unittest.main()
