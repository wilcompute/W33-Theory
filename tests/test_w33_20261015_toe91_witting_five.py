"""TOE91 Witting research regressions: five fronts and certificate regeneration."""
from functools import lru_cache
from pathlib import Path
import json
from fractions import Fraction
import numpy as np
import pytest
from analysis import w33_20261015_toe91_finitekey_analyzer_carrier as F
from analysis import w33_20261015_toe91_symplectic_phase_audit as P
from analysis import w33_20261015_toe91_symplectic_unitary_lift as U

ROOT=Path(__file__).resolve().parents[1]

@lru_cache(None)
def c():return F.certificate()
@lru_cache(None)
def phase():return P.certificate()
@lru_cache(None)
def lifts():return U.certificate()

def test_conditional_isotropic_key_rate_is_not_entanglement_witness():
 x=c()['finite_key']
 assert x['positive_hashing_threshold_visibility']==pytest.approx(.691019401041,abs=1e-10)
 q={v['visibility']:v for v in x['cases']}
 assert q[.25]['matching_probability']==.4375
 assert q[.25]['asymptotic_one_way_hashing_rate_bits_per_pair']<0
 assert q[.7]['positive_hashing_lower_bound']
 assert not q[.2]['positive_hashing_lower_bound']
 assert x['one_sided_Hoeffding_matching_deviation']>0

def test_40_setting_analyzer_perturbation_and_loss_bound():
 a=c()['analyzer_calibration']
 assert a['settings']==40
 assert a['two_party_measurement_outcomes_per_setting']==16
 assert a['simulated_max_rail_rotation_radians']==.01
 assert a['perturbed_vs_ideal_joint_match_operator_spectral_error']>0
 assert a['conservative_separable_ceiling_with_setting_efficiency_band']==pytest.approx(.421097360886,abs=1e-9)
 assert a['max_basis_unitarity_residual']==0.

def test_explicit_product_state_setting_selection_attack():
 a=c()['product_state_postselection_attack']
 assert a['uniform_40_basis_matching']==.4
 assert len(a['four_matching_bases'])==4
 lo,mid,hi=a['basis_dependent_postselection']
 assert lo['conditioned_product_state_matching']==.4
 assert mid['accepted_fraction']==.19
 assert mid['conditioned_product_state_matching']==pytest.approx(13/19)
 assert hi['accepted_fraction']==.1
 assert hi['conditioned_product_state_matching']==1.

def test_physical_event_W33_oriented_edge_bijection():
 a=c()['detector_to_W33_carrier']
 assert a['directed_outcome_substitution_events']==480
 assert a['unoriented_W33_orthogonality_edges']==240
 assert a['F3_vertex_boundary_matrix_shape']==[40,240]
 assert a['F3_incidence_rank']==39
 assert a['F3_cycle_kernel_dimension']==201
 assert a['turn_counts_for_every_oriented_edge']=={
   'triangle_turns':2,'open_turns':9,'total_nonbacktracking':11}

def test_four_transvections_preserve_all_bargmann_triples():
 x=phase()
 assert len(x['tests'])==4
 for t in x['tests']:
  assert t['nonorthogonal_triples']==3240
  assert t['unitary_Bargmann_max_error']==0.
  assert t['unitary_possible'] is True
  assert t['antiunitary_possible'] is False

def test_explicit_U4_lifts_of_four_F3_transvections():
 x=lifts()
 assert len(x['tested_generators'])==4
 for gen in x['tested_generators']:
  assert gen['maps_all_40_tetrads']
  assert gen['generator_cube_is_identity']
  assert gen['max_projective_ray_image_residual']==0.
  assert gen['max_orthonormality_residual']==0.
  assert len(set(gen['permutation_40']))==40
  U4=np.array(gen['phase_adjusted_4x4_unitary_real'])+1j*np.array(gen['phase_adjusted_4x4_unitary_imag'])
  assert np.max(abs(U4.conj().T@U4-np.eye(4)))<1e-9
  assert np.max(abs(U4@U4@U4-np.eye(4)))<1e-8

@pytest.mark.parametrize('name,producer',[
 ('w33_20261015_toe91_finitekey_analyzer_carrier.json','carrier'),
 ('w33_20261015_toe91_symplectic_phase_audit.json','phase'),
 ('w33_20261015_toe91_symplectic_unitary_lift.json','lift')])
def test_exact_frozen_certificate(name,producer):
 obj={'carrier':c,'phase':phase,'lift':lifts}[producer]()
 assert obj==json.loads((ROOT/'data'/name).read_text(encoding='utf8'))
