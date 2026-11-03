"""Regression checks for Nov 3 W33 eight-front certified research packet.

Regenerates the short q9 group certificate, validates frozen long census,
and checks exact/numerical conclusions without rerunning 91.6m triple loop.
"""
import json,sys,unittest
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261103_q9_exact_full_orbit_cubic_certificate import main as q9short
class EightFrontTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data={}
  for n in ('q9_seed_cubic_orbit_types','q9_exact_full_orbit_cubic_certificate',
     'three_setting_ic_povm','216_permutation_isotypic_probe',
     'albert_fixed_frame_irrep_obstruction','native_three_voltage_bloch',
     'two_bit_phase_witness'):
   cls.data[n]=json.loads((ROOT/f'data/w33_20261103_{n}.json').read_text())
 def test_01_q9_full_triplet_count(self):
  r=self.data['q9_seed_cubic_orbit_types']
  self.assertEqual(r['all_distinct_triplets'],91558740)
  self.assertEqual(len(r['three_point_types']),7)
  self.assertEqual(sum(x['triple_count'] for x in r['three_point_types'].values()),91558740)
 def test_02_q9_full_orbit_certificate(self):
  r=q9short()
  self.assertEqual(r['isotropic_line_moment'],'24616/15')
  self.assertEqual(r['global_triple_checksum'],'1617040')
  self.assertTrue(r['isotropic_line_value_unique'])
 def test_03_three_settings_IC_minimal(self):
  r=self.data['three_setting_ic_povm']
  self.assertEqual([x['operator_rank'] for x in r['full_unitary_results'][:3]],[201,401,576])
  self.assertEqual([x['rank'] for x in r['phase_only_control'][:3]],[201,401,576])
  self.assertTrue(r['three_settings_informationally_complete'])
  self.assertEqual(r['algebraic_lower_bound_on_settings'],3)
 def test_04_discrete_phase_control_and_imaginary_witness(self):
  r=self.data['two_bit_phase_witness']
  self.assertFalse(r['three_settings_complete_with_two_bit_phases'])
  self.assertEqual([x['real_Hermitian_span_rank'] for x in r['two_bit_phase_trials']],[499,515,499])
  self.assertLess(r['imaginary_coherence_witness_no_phase_TV'],1e-10)
  self.assertGreater(r['imaginary_coherence_witness_with_one_90deg_phase_TV'],.02)
 def test_05_real_rep_splits(self):
  r=self.data['216_permutation_isotypic_probe']
  self.assertTrue(r['all_orbital_matrices_G_equivariant_exact'])
  self.assertEqual(r['orbitals_count'],10)
  self.assertEqual(sum(r['proposed_complex_irrep_dimensions']),216)
  by={x['squared_gram_eigenvalue']:x for x in r['K_eigenspace_split_by_generic_G_commuting_hermitian']}
  self.assertEqual([x['dimension'] for x in by[2304]['generic_selfadjoint_centralizer_eigenblocks']],[20,60])
 def test_06_complex60_and_double15(self):
  r=self.data['216_permutation_isotypic_probe']
  self.assertTrue(r['real20_complex_structure_evidence']['60']['complex_type_candidate'])
  self.assertFalse(r['real20_complex_structure_evidence']['20']['complex_type_candidate'])
  self.assertTrue(r['isomorphism_of_two_15D_eigenspaces_evidence']['fifteen_modules_equivalent_numeric'])
 def test_07_albert_frame_no_go(self):
  r=self.data['albert_fixed_frame_irrep_obstruction']
  self.assertEqual(r['point_stabilizer_orbit_sizes'],[1,12,27])
  self.assertEqual(r['point_adjacency_spectrum'],{'12':1,'2':24,'-4':15})
  self.assertTrue(r['positive_24D_module_absolutely_irreducible'])
 def test_08_Bloch_three_isotropic_spatial_directions(self):
  r=self.data['native_three_voltage_bloch']
  self.assertEqual(len(r['edge_voltages']),3)
  self.assertLess(r['metric_condition_number'],1.001)
  self.assertLess(r['small_k_max_relative_quadratic_error'],1e-4)
if __name__=='__main__':unittest.main()
