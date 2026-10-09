"""Round19 source-grounded regression across five physics fronts."""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_round19_gauge_cycle_frustration as G
import w33_20261009_round19_blocked_optics_design as O
import w33_20261009_round19_theta_quantum_rotor as Q

def data(stem):
 return json.loads((ROOT/'data'/('w33_20261009_round19_'+stem+'.json')).read_text())

def test_native_first_local_onephoton_witness_both_primes():
 for p in (1000003,1000033):
  d=data('onephoton_local_eighth')['certificate'][str(p)]
  assert d['distinct_relabel_invariant_site_return_histograms']=={'0':1,'2':1,'4':1,'6':1,'8':5}
  assert len({tuple(row) for row in d['all_orbit_eighth_histograms']})==5
 assert 2*28*4*232+70*28*28==106848

def test_gauge_native_all_eight_cycle_rank_and_theta_odd_obstruction():
 d=data('gauge_cycle_frustration')
 edges,cyc,masks,rows=G.cycle_vectors()
 assert len(edges)==160 and len(cyc)==1620
 assert G.rank_f2(masks)==81 and G.modrank(rows,3)==81
 a,b,c=d['explicit_theta_plaquette_indices']; signs=d['theta_flux_relation_signs']
 assert all(sum(s*rows[k].get(i,0) for s,k in zip(signs,(a,b,c)))==0 for i in range(160))
 assert [int((masks[a]&masks[b]).bit_count()),int((masks[a]&masks[c]).bit_count()),int((masks[b]&masks[c]).bit_count())]==[4,4,4]

def test_native_vacuum_displacement_positive_restricted_hessian():
 d=data('vacuum_displaced_complex_gaussian')
 assert len(d['samples'])==4
 for z in d['samples']:
  assert abs(z['centered_energy']-128.88739141552713)<1e-8
  assert abs(z['optimized_energy']-z['centered_energy'])<1e-6
  assert min(z['centered_displacement_hessian_eigenvalues'])>0

def test_heterotic_nonabelian_mask_retains_necessary_candidates():
 d=data('heterotic_nonabelian_cubic')
 assert d['initial_U1_R_nonR_necessary_candidates']==90
 assert d['surviving_full_nonabelian_and_R_count']==90
 assert not d['failed_group_theory_filters']
 assert d['necessary_nonabelian_irrep_tensor_mask']=={'(True, True, True, True)':90}

def test_blocked_optics_rank_repair_and_remaining_leakage_nogo():
 a=O.experiment(n=1024,light_signal=.08,phase_wire_leak=.05)
 assert a['regression_matrix_rank']==5
 assert abs(a['estimated_coefficients'][1]-.08)<.001
 assert abs(a['estimated_coefficients'][2]-.05)<.001
 b=O.experiment(n=1024,light_signal=0.,block_correlated_leak=.08,phase_wire_leak=.05)
 assert np.array_equal(a['observed_series'],b['observed_series'])

def test_theta_rotor_hermitian_and_converging_ground():
 d=data('theta_quantum_rotor')
 energies=[]
 for s in d['samples']:
  H,_=Q.rotor_matrix(s['fourier_cut'],E=.5,g=1.)
  assert not (H-H.T).nnz
  assert s['first_gap']>0
  energies.append(s['lowest_energy'])
 assert energies[0]>energies[1]>energies[2]
 assert abs(energies[2]-energies[1])<1e-5

def test_finite_time_onephoton_original_angle_observable():
 d=data('finite_time_onephoton_readout')
 for label in ('rational_unimodular','original_round16_angles'):
  x=d['phase_conventions'][label]['2.0']
  assert x['minimum_pairwise_histogram_linf_distance']>.0019
  assert x['maximum_unitarity_residual']<1e-11
