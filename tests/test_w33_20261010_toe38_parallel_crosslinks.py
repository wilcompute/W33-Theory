"""Five focused Round38 independent scientific regression gates."""
from pathlib import Path
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261010_toe38_local_maxwell_2complex as mx
import w33_20261010_toe38_theta_moment_modular_frame as th
import w33_20261010_toe38_minkowski_weil_module_firewall as mf
def frozen(name):
 return json.loads((ROOT/'data'/f'w33_20261010_toe38_{name}.json').read_text(encoding='utf-8'))
def test_W33_native_octagons_and_local_commutator_maxwell_two_transverse_modes():
 baseline=frozen('local_maxwell_2complex');r=mx.run()
 assert r['n_zero_winding_native_octagons']==baseline['n_zero_winding_native_octagons']==1382
 assert r['zero_winding_8cycle_rank_at_zero']==78
 assert r['commutator_plaquette_lengths']==[32,40,40]
 assert r['cases'][0]['transverse_harmonic_dim']==3
 assert all(c['plaquette_boundary_rank']==80 and c['transverse_harmonic_dim']==0 for c in r['cases'][1:])
 assert max(c['max_d1_d2_violation'] for c in r['cases'])<1e-10
def test_light_modes_are_two_acoustic_cones_not_old_80_flat_bands():
 r=frozen('local_maxwell_2complex')
 a,b=r['cases'][1],r['cases'][2]
 for j in (0,1):
  assert 3.9<a['lowest_transverse_curl_eigenvalues'][j]/b['lowest_transverse_curl_eigenvalues'][j]<4.1
 assert b['lowest_transverse_curl_eigenvalues'][2]>99
 # Fixed physical wave scale remains arbitrary; only kinematics is tested.
 for c in r['cases'][1:]:
  assert c['lowest_transverse_curl_eigenvalues'][1]<.01
  assert c['lowest_transverse_curl_eigenvalues'][2]>90
def test_theta_moment_determinant_rank_hierarchy():
 baseline=frozen('theta_moment_modular_frame');r=th.analyze()
 assert all(abs(a-b)<.03 for a,b in zip(r['log2_halfsize_slopes_sigma2_sigma3'],[1,2]))
 assert r['leading_determinant_relative_errors'][-1]<1e-3
 assert abs(r['determinant_leading_coefficient_magnitude']-baseline['determinant_leading_coefficient_magnitude'])<1e-10
def test_theta_CP_invariant_Schmidt_but_not_invariant_under_modular_CZ():
 r=frozen('theta_moment_modular_frame')
 assert r['CP_schmidt_invariance_max_abs_difference']<1e-12
 assert r['modular_shear_CZ_coefficient_error']<1e-12
 assert abs(r['entropy_before_shear_nats'])<1e-12
 assert r['entropy_after_shear_nats']>.1
 assert r['product_after_integral_omega12_shear_normalized_singular_values'][-1]>1e-5
def test_orthogonal_finite_Minkowski_module_not_weil_symplectic_module():
 baseline=frozen('minkowski_weil_module_firewall');r=mf.run()
 assert r['invariant_alternating_linear_constraint_rank']==6
 assert r['invariant_alternating_dimension']==0
 assert r['J_rank']==4
 assert r['broken_weil_pairing_constraint_nonzero_entries_by_generator']==baseline['broken_weil_pairing_constraint_nonzero_entries_by_generator']
