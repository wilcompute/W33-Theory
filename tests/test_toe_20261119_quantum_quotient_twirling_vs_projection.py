"""Exact quotient/twirl/physical-subspace regression."""
import sys,unittest,pathlib
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261119_quantum_quotient_twirling_vs_projection as p
class SymmetryProjectionAndCoherence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=p.gate();cls.x={y['state']:y for y in cls.r['rows']}
 def test_three_distinct_coherent_histories_same_classical_diagonal(self):
  for row in self.r['rows']:np.testing.assert_allclose(row['same_labeled_diagonal_distribution'],[.5,.5],atol=1e-12)
 def test_all_density_operators_Z2_invariant(self):self.assertTrue(all(x['unitary_action_on_density_preserves_state'] for x in self.r['rows']))
 def test_twirl_trace_preserved(self):self.assertTrue(all(abs(x['Z2_twirl_trace']-1)<1e-12 for x in self.r['rows']))
 def test_twirled_purity_for_plus(self):self.assertAlmostEqual(self.x['symmetric']['Z2_twirl_purity'],1.)
 def test_twirled_purity_for_minus(self):self.assertAlmostEqual(self.x['antisymmetric']['Z2_twirl_purity'],1.)
 def test_twirled_purity_for_classical_mix(self):self.assertAlmostEqual(self.x['classical_incoherent']['Z2_twirl_purity'],.5)
 def test_projection_keeps_invariant_vector(self):self.assertAlmostEqual(self.x['symmetric']['invariant_projection_trace'],1.)
 def test_projection_kills_sign_rep_vector(self):self.assertAlmostEqual(self.x['antisymmetric']['invariant_projection_trace'],0.)
 def test_projection_keeps_half_of_mix(self):self.assertAlmostEqual(self.x['classical_incoherent']['invariant_projection_trace'],.5)
 def test_same_diagonal_different_interference_weight(self):
  np.testing.assert_allclose([self.x[k]['unnormalized_coherent_sum_weight'] for k in ('antisymmetric','classical_incoherent','symmetric')],[0.,1.,2.],atol=1e-12)
 def test_anti_invariant_amplitude_does_not_descend_as_scalar_to_orbit(self):self.assertIn('sign ambiguity',self.r['unlabeled_amplitude_obstruction'])
 def test_no_quantum_gravity_claim(self):
  self.assertFalse(self.r['TOE_solved']);self.assertIn('no dynamics',self.r['quantum_measure_limitation'])
if __name__=='__main__':unittest.main()