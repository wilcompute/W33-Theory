"""Tests for five Round24 physics research frontiers.
All artifacts are recomputed or cross-checked, no other experiment modified.
"""
import sys,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe24_e8_representation_obstruction as e8
import w33_20261009_toe24_apartment_tritangent_fiber as fib
import w33_20261009_toe24_quantum_order_parameter_susceptibility as sus
import w33_20261009_toe24_css_distance_firewall as css
import w33_20261009_toe24_pair_spectroscopy_protocol as spec
def frozen(n):
 return json.loads((ROOT/'data'/f'w33_20261009_toe24_{n}.json').read_text())

def test_E8_naive_27_tensor_trivial3_is_not_steinberg81():
 out=e8.run()
 assert out==frozen('e8_representation_obstruction')
 assert out['permutation27_adjacency_spectrum']=={'10':1,'1':20,'-5':6}
 assert out['steinberg81_invariant_vectors']==0
 assert 'Hom_PSp' in out['canonical_Hom_dim']
 assert out['natural_permutation27_dim']==27

def test_45_apartment_frame_components_identical_to_E6_protected45():
 out=fib.run()
 assert out==frozen('apartment_tritangent_fiber')
 assert out['component_partition_equals_prior_Pass4585_4659_fiber_partition']
 assert out['apartment_count']==1620
 assert (out['n_components'],out['size_each'])==(45,36)
 assert out['protected_support_count']==45
 assert out['points_per_support']==16
 assert out['expected_PSp_stabilizer']==576

def test_N2_N3_pin_field_susceptibility_Hellmann_Feynman():
 out=sus.run()
 assert out['status']=='PASS'
 t=out['pinned_density_and_susceptibility']
 assert out['computational_Hilbert_dimensions']=={'2':3240,'3':88560}
 assert t['2']['32']['local_susceptibility']>15*t['2']['0']['local_susceptibility']
 assert t['3']['8']['local_susceptibility']>100*t['3']['0']['local_susceptibility']
 for rows in t.values():
  for point in rows.values():
   a=point['local_susceptibility'];b=point['energy_second_derivative_susceptibility']
   assert a>0 and abs(a-b)<.02*a+2e-4

def test_partial_flatness_codes_have_exact_distance_one():
 out=css.run()
 assert out==frozen('css_distance_firewall')
 for p in out['profiles'].values():
  assert p['exact_code_distance']==1 and len(p['verified_weight_one_logical_X_link_indices'])>0
 assert out['profiles']['avoid_incidence_edge']['remaining_logical_qutrits']==1
 assert out['profiles']['avoid_vertex']['remaining_logical_qutrits']==3

def test_pair_spectroscopy_five_exact_bands_and_noise():
 out=spec.run()
 assert out==frozen('pair_spectroscopy_protocol')
 assert [b['multiplicity'] for b in out['band_spectroscopy']]==[1,24,30,24,1]
 assert math.isclose(out['nontrivial_gap_ratio_second_over_first'],4/(4-math.sqrt(6)),rel_tol=1e-12)
 assert sum(b['weight_from_one_localized_doublon'] for b in out['band_spectroscopy'])==1
 for no in out['synthetic_on_site_noise_A_units'].values():
  assert no['trials']==50
  assert no['max_abs_ratio_shift']<=no['rigorous_Weyl_ratio_error_upper_bound']+1e-12
