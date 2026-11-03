"""Fast regression guards for the Nov 3 q9 formal slice, group characters,
Molien cubics, q13 design, phase-rank hardware and native Wilson control."""
import json,unittest,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(stem):
 return json.loads((ROOT/'data'/f'w33_20261103_{stem}.json').read_text())
class Nov03EightFronts(unittest.TestCase):
 def test_01_q9_lean_arithmetic_scope(self):
  s=(ROOT/'lean/W33Q9CubicClassArithmetic.lean').read_text()
  self.assertIn('exact_cubic_checksum',s)
  self.assertIn('line_class_unique',s)
  self.assertNotIn(':= by sorry',s)
  self.assertEqual(sum([98400,2988900,23911200,398520,398520,31881600,31881600]),91558740)
  self.assertEqual(98400*3987792-2988900*283424+23911200*17680
       -2*398520*309910+2*31881600*4437,1617040*2430)
 def test_02_exact_gap_216_irreducibles(self):
  r=load('gap_216_exact_character_certificate')
  self.assertEqual(r['group_order'],25920)
  self.assertEqual(r['selected_route_class_index_0based'],1)
  self.assertEqual(r['selected_route_complex_degrees'],[1,15,15,20,24,30,30,81])
  self.assertEqual(r['route_commutant_dimension'],10)
  self.assertNotIn(24,r['class_characters'][0]['constituent_degrees'])
 def test_03_exact_molien_character_and_cubic_basis(self):
  r=load('w33_24_molien_cubic')
  self.assertEqual(r['symmetric_power_invariant_dimensions'],{'2':1,'3':2,'4':6})
  self.assertTrue(r['cubic_nonzero_on_24D'])
  self.assertNotEqual(int(r['two_invariant_cubic_basis_independence_witness']['exact_2x2_determinant']),0)
 def test_04_q13_nonhyperoval_belongs_to_positive_module(self):
  r=load('q13_positive_frame')
  self.assertEqual(r['coverage_profile'],{'0':1340,'2':960,'4':80})
  self.assertEqual(r['point_adjacency_quadratic_form'],12*r['centered_squared_norm'])
  self.assertEqual(r['negative_eigenspace_squared_norm'],0)
  self.assertEqual(r['positive_eigenspace_dimension'],1274)
 def test_05_bit_depth_falsifier(self):
  r=load('phase_bitdepth_condition')
  t={z['bits']:z for z in r['sampled_best_per_bitdepth']}
  self.assertEqual([t[b]['rank'] for b in (2,3,4,6)],[515,565,574,576])
  self.assertLess(t[6]['min_eigenvalue'],3e-6)
  self.assertGreater(t[6]['min_eigenvalue'],1e-6)
 def test_06_fisher_shot_resource(self):
  r=load('phase_fisher_shot_budget')
  t={v['bit_depth']:v for v in r['bit_depth_controls']}
  self.assertEqual(t[6]['shots_per_setting_for_std_0p01'],23256463)
  self.assertGreater(t[6]['worst_direction_CRB_std_at_1M_shots_per_setting'],.04)
 def test_07_wilson_3D_lattice_control_and_limit(self):
  r=load('wilson_dirac_3deck_control')
  self.assertEqual(r['Bloch_cell_modes'],160)
  self.assertEqual(len(r['BZ_corner_doubler_controls']),8)
  self.assertLess(r['BZ_corner_doubler_controls'][0]['native_40mode_wilson_min_abs'],1e-9)
  self.assertGreater(min(z['native_40mode_wilson_min_abs'] for z in r['BZ_corner_doubler_controls'][1:]),2.8)
  self.assertTrue(all(z['chirality_commutator_norm']>0 for z in r['BZ_corner_doubler_controls'][1:]))
 def test_08_provenance_scope_control(self):
  report=(ROOT/'analysis/2026-11-03_q9_lean_gap_24cubic_q13_photonic_wilson_8fronts.md').read_text(encoding='utf-8')
  for s in ('NOT yet formalize','not a fully formalized','does not imply 160 is optimal','not emergent',
             '23,256,463','45,889,208,640,000','dd85b447a'):
   self.assertIn(s.lower(),report.lower())
if __name__=='__main__':unittest.main()
