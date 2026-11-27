"""Independent focused regression assertions for the round-eight producer."""
import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import toe_20261127_round8 as R

@pytest.fixture(scope='module')
def results():
    return {k:getattr(R,k)() for k in ('mic','compiler','qec','higgs','causal','maxcuts','e8_bridge')}

def test_projective_mirror_orbit(results):
    a=results['mic'];assert a['group_order']==25920 and a['seed_support_orbit']==2880 and a['support_stabilizer']==9

def test_exact_measurement_and_pivots(results):
    a=results['mic'];assert a['best_condition']['gram_determinant']=='25/59049';assert a['nondegenerate_seed_pivots']==0;assert sum(a['pivot_leaving_multiplicity'].values())==24

def test_optical_candidate(results):
    a=results['mic']['best_low_couplers'];assert a['couplers']==50;assert abs(sum(a['weights'])-4)<1e-12;assert 0<a['survival']<1

def test_lie_basis(results):
    a=results['compiler'];assert a['basis_rank']==15;assert sum(r==15 for _,r in a['exact_modular_basis_ranks'])>=4

def test_rational_circle(results):
    a=results['compiler'];assert a['rational_circle_pq']==[26569,95010];assert a['rigorous_angular_cover_bound']<5.83e-5

def test_fixed_word_error_bound(results):
    rows=results['compiler']['rational_circle_examples'];assert all(x['operator_norm_error']<=x['analytic_worst_phase_bound'] for x in rows);assert min(x['operator_norm_error'] for x in rows)<.002

def test_trinification_twirl(results):
    a=results['qec'];assert abs(a['restricted_H27_F_e']-1)<1e-12;assert abs(a['trinification_twirl_F_e']-1/27)<1e-12

def test_optimal_mixture_fidelity(results):
    for row in results['qec']['mixture']:assert abs(row['F_e']-(1-26*row['probability']/27))<1e-12

def test_full_higgs_rank(results):
    a=results['higgs'];assert sum(a['dimension_by_SO10_sector'].values())==248;assert sum(a['rank_by_SO10_sector'].values())==215;assert a['nullity']==a['broken_complex_gauge_dimension']==33

def test_charged_mass_coefficients(results):
    a=results['higgs'];assert a['charge_family_mass_coefficients']=={'4':['0','3','3'],'1':['1/6','19/6','19/6'],'-2':['1/3','10/3','10/3']};assert a['matter_optional_10_family_det']==-2

def test_e8_bridge_firewall(results):
    a=results['e8_bridge'];assert sum(a['E8_branching_dimensions'])==248;assert 3 not in a['E8_basic_invariant_degrees'];assert a['SU3_restored_effective_quartic']=='-(v^T u)^2/3'

def test_all_optimal_bipartitions(results):
    a=results['maxcuts'];assert a['maxcut_count_up_to_global_complement']==216;assert a['oriented_count']==432;assert a['symplectic_transvection_orbit_size']==216

def test_causal_scaling_and_null(results):
    a=results['causal'];assert abs(a['product_limit_order_fraction']-327/1600)<1e-12;assert a['ordinal_limit_order_fraction']==1;assert a['rows'][-1]['product']['height']==11;assert a['rows'][-1]['ordinal_sum']['height']==32;assert abs(a['degree_matched_bipartite_BFS_mean_12']['ordering_fraction']-a['rows'][0]['product']['ordering_fraction'])<.02
