"""Independent regression for constructive causal witness and five other TOE gates."""
from __future__ import annotations
from pathlib import Path
import sys,unittest,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from toe_20261120_causal_witness_constructive import (
    main as causal, switch_state, process_states, causal_no_signalling_effects,pauli_expansion
)
from toe_20261120_five_independent_operational_gates import (
    main as rest, optical_compression_and_noncentral_control,
    anomaly_polynomial_sieve,noise_drift_calibration,calibration_bound,
    w33_levi_graph_and_8cycle,z3_wilson_nondeterminacy,
    dimensional_scale_free_parameter
)

class CausalWitnessTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.o=causal(write=False)
 def test_rank_one_chirality_independent_process(self):
  psi=switch_state()
  self.assertEqual(psi.shape,(64,))
  self.assertAlmostEqual(float(np.vdot(psi,psi).real),1)
 def test_two_direction_signal_effects_and_theorem(self):
  P,_=process_states()
  A,B=causal_no_signalling_effects()
  self.assertAlmostEqual(float(np.trace(P@A).real),.125)
  self.assertAlmostEqual(float(np.trace(P@B).real),.125)
  self.assertAlmostEqual(self.o['causal_separable_fidelity_upper_bound'],255/256)
 def test_linear_witness_negative_ideal_positive_mixture(self):
  self.assertAlmostEqual(self.o['linear_witness_ideal_expectation'],-1/256)
  self.assertAlmostEqual(self.o['linear_witness_dephased_causal_mixture_expectation'],255/256-.5)
 def test_visibility_threshold(self):
  self.assertAlmostEqual(self.o['coherent_visibility_minimum_for_this_weak_witness'],127/128)
  P,deph=process_states()
  for v in (0.,.99,.995,1.):
   rho=v*P+(1-v)*deph
   measured=255/256-float(np.trace(P@rho).real)
   self.assertEqual(measured<0, v>127/128)
 def test_634_pauli_reconstruction(self):
  tomo=self.o['tomography']
  self.assertEqual(tomo['number_nonzero_pauli_terms'],634)
  self.assertAlmostEqual(tomo['pauli_L1_coefficient_norm'],2.96875)
  self.assertLess(tomo['max_reconstruction_residual'],1e-14)
  self.assertEqual(tomo['exact_pauli_expansion']['IIIIII'],1/64)
 def test_160_random_fixed_order_controls(self):
  self.assertEqual(self.o['pure_fixed_order_controls_tested'],160)
  self.assertLess(self.o['max_pure_fixed_order_control_fidelity'],255/256)
 def test_sample_complexity_scope(self):
  self.assertGreater(self.o['hypothetical_importance_sampled_global_pauli_shots'],20_000_000)
  self.assertIn('NOT automatically',self.o['measurement_boundary'])

class OpticalChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.o=optical_compression_and_noncentral_control()
 def test_exact_central_compression(self):
  self.assertLess(self.o['central_pair_control_tensor_target_factorization_max_residual'],1e-12)
 def test_noncentral_requires_input_sensitive_target(self):
  self.assertGreater(self.o['nine_input_fringe_spread'],.1)
  self.assertGreater(self.o['noncentral_operator_Frobenius_squared'],2)
  self.assertGreater(self.o['noncentral_control_purified_target_entropy_bits'],.3)
 def test_18mode_unitary(self):
  self.assertLess(self.o['ideal_18_mode_network_unitarity_error'],1e-12)

class ChiralityChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.o=anomaly_polynomial_sieve()
 def test_charge_polynomial_coefficients(self):
  self.assertEqual(self.o['difference_matrix_on_A_B_C'],[[0,3,-3],[0,-3,-15]])
  self.assertIn('iff B=C=0',self.o['equal_index_condition'])
 def test_anomaly_flux_model(self):
  self.assertEqual(self.o['flux_only_Q3_indices'],[3,12,48])
  self.assertEqual(self.o['flux_only_Q3_anomalies'],[0,2160,-18])
 def test_auxiliary_topological_chirality_not_dynamical(self):
  self.assertEqual(self.o['common_SU2_twist_topological_example']['c2_E'],-3)
  self.assertIn('does not dynamically select 3',self.o['physical_boundary'])

class NoiseChecks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.o=noise_drift_calibration()
 def test_previously_omitted_drift_false_certifies(self):
  self.assertGreaterEqual(self.o['false_certifications_if_zero_drift_assumed'],380)
  self.assertEqual(self.o['false_certifications_with_drift_bound_0p04'],0)
  self.assertGreater(self.o['true_test_noncentrality_Frobenius_squared'],.5)
 def test_confidence_bound_drifts_monotonic(self):
  n=150000;a=146500;b=145500
  d0=calibration_bound(a,b,n,drift_bound=0)
  d1=calibration_bound(a,b,n,drift_bound=.02)
  d2=calibration_bound(a,b,n,drift_bound=.04)
  self.assertLessEqual(d0,d1)
  self.assertLessEqual(d1,d2)
 def test_bias_and_state_prep_monotonic(self):
  n=150000;a=145000;b=145000
  x=calibration_bound(a,b,n)
  y=calibration_bound(a,b,n,readout_bias_bound=.02)
  z=calibration_bound(a,b,n,readout_bias_bound=.02,prep_trace_error=.03)
  self.assertLessEqual(x,y)
  self.assertLessEqual(y,z)
 def test_trace_threshold(self):
  self.assertAlmostEqual(self.o['required_trace_magnitude_for_tolerance'],math.sqrt(1-(.25**2)/9))

class GaugeNonidentifiabilityTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.o=z3_wilson_nondeterminacy()
 def test_levi_graph_and_8cycle(self):
  g=w33_levi_graph_and_8cycle()
  self.assertEqual(g['graph'].number_of_nodes(),80)
  self.assertEqual(g['graph'].number_of_edges(),160)
  self.assertEqual(len(g['cycle']),8)
 def test_exact_gauge_degeneracy(self):
  self.assertEqual(self.o['exhaustive_gauge_link_assignments'],3**8)
  self.assertEqual(self.o['degeneracy_each_Wilson_holonomy'],3**7)
 def test_beta_not_selected_by_W33(self):
  vals=[r['Wilson_Re_expected'] for r in self.o['calculated_couplings']]
  self.assertAlmostEqual(vals[0],0)
  self.assertGreater(vals[2],.5)
  self.assertGreater(vals[-1],.99)
  self.assertTrue(all(x<y for x,y in zip(vals,vals[1:])))
 def test_partition_derivative_is_variance(self):
  for r in self.o['calculated_couplings']:
   b=r['coupling_beta']
   h=1e-5
   f=lambda z:(math.exp(z)-math.exp(-z/2))/(math.exp(z)+2*math.exp(-z/2))
   df=(f(b+h)-f(b-h))/(2*h)
   self.assertAlmostEqual(df,r['beta_derivative_as_variance'],places=8)
 def test_gauge_invariance_checks(self):
  self.assertEqual(self.o['exact_gauge_transform_invariance_trials'],150)

class ScaleAndScope(unittest.TestCase):
 def test_speed_not_selected(self):
  a=dimensional_scale_free_parameter()
  self.assertTrue(np.allclose(a['different_physical_speeds_with_same_graph'],[1,1000,1e6]))
 def test_packet_metadata(self):
  x=rest(write=False)
  self.assertEqual(x['schema'],'toe.deep_five_20261120.v1')
  self.assertIn('no real lab',x['overall_scope'])

if __name__=='__main__':unittest.main()
