"""Round22: five TOE stress tests with independently regenerated certificates."""
from pathlib import Path
import sys,math,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_toe22_cubic_jacobi as cubic
import w33_20261009_toe22_two_boson_quantum_selector as quantum
import w33_20261009_toe22_symplectic_locality_nogo as space
import w33_20261009_toe22_native_gauge_hamiltonian as gauge
import w33_20261009_toe22_scale_nogo as scale
def saved(k):
 return json.loads((ROOT/'data'/f'w33_20261009_toe22_{k}.json').read_text())

def test_construct_unique_cubic_and_exact_jacobi_failure():
 a=cubic.run();b=saved('cubic_jacobi')
 assert a==b
 assert a['group_order']==51840 and a['invariant_alternating_form_dimension'] if 'invariant_alternating_form_dimension' in a else a['unique_alternating_cubic_prior_dimension']==1
 assert len(a['jacobi_witnesses'])==8
 assert all(x['nonzero']>=77 for x in a['jacobi_witnesses'])
 assert a['elementary_cycle_Jacobi_witness']['nonzero_entries']>0
 assert a['independent_full_form_symmetry_checks']==5

def test_two_boson_full_3240_quantum_selector():
 a=quantum.run()
 assert a==saved('two_boson_quantum_selector')
 assert a['Hilbert_dimension']==3240
 assert abs(a['calculations']['0']['energy0']+8)<1e-8
 assert a['calculations']['32']['doublon_probability']>.98
 for row in a['calculations'].values():
  assert row['gap']>0
  assert row['max_site_density_error_from_2_over_80']<1e-6
 assert a['calculations']['32']['gap']<a['calculations']['0']['gap']

def test_spacetime_affine_sp4_locality_no_go():
 a=space.run()
 assert a==saved('symplectic_locality_nogo')
 assert a['symplectic_nonzero_orbit_size']==80
 assert a['number_translation_states']==81
 assert a['complete_graph_laplacian_eigenvalues']=={'zero':1,'81_over_80':80}
 assert abs(a['samples'][0]['heat']-space.run()['samples'][0]['heat'])<1e-14

def test_160_link_gauss_flatness_ranks_and_unique_state():
 a=gauge.run()
 assert a==saved('native_gauge_hamiltonian')
 assert (a['gauge_star_rank_over_F3'],a['independent_wilson_rank_over_F3'],a['full_stabilizer_rank'])==(79,81,160)
 assert a['vertex_operator_weight']==4 and a['wilson_operator_weight']==8
 assert a['n_eightcycle_wilson_terms']==1620
 assert a['unique_ground_state_dimension']==1

def test_feynman_hellmann_and_absolute_mass_scale_free():
 a=scale.run()
 b=saved('scale_nogo')
 assert abs(a['Feynman_Hellmann_U_8']['difference'])<2e-5
 assert a['Hilbert_dimension']==3240
 assert len(a['scale_covariance'])==3
 assert all(x['relative_error']<1e-6 for x in a['scale_covariance'])
 assert abs(a['strong_coupling_U32']['relative_difference'])<.03
