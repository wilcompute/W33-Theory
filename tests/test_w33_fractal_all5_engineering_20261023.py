"""Check all executable frontiers without claiming physical PDK or hardware proof."""
import json,math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_all5_engineering_20261023 import (
    measure_interference,edge_info,edge_loss,route_opt,route_casebook,
    qutrit_bridge,pdk_handoff)
from w33_fractal_linebus_switch_matrix_20261023 import linebus_neighbors
from w33_linebus_coherent_path_phase_frame_20261023 import transport

def test_four_phase_experiment_recovers_ideal_i_relative_phase():
    p=measure_interference(shots_per_phase=10000)
    assert p['ideal_phase_exponent']==1
    assert abs(p['estimated_phase_rad']-math.pi/2)<.09
    assert abs(p['estimated_visibility']-.85)<.08
    assert len(p['sample_counts'])==4
    assert p==measure_interference(shots_per_phase=10000)

def test_two_routes_same_endpoints_distinct_phase():
    a,b=(0,4,7),(0,14,7)
    assert sum(transport(x,y)['scalar_i_exponent_mod4'] for x,y in zip(a,a[1:]))%4!=sum(transport(x,y)['scalar_i_exponent_mod4'] for x,y in zip(b,b[1:]))%4

def test_route_graph_integrity_frame_and_survival():
    for a,b in [((0,0),(39,39)),((0,4),(7,22)),((12,17),(31,2))]:
        answer=route_opt(a,b)
        assert answer['reachable'] and answer['path'][0]==list(a) and answer['path'][-1]==list(b)
        assert len(answer['path'])==answer['hops']+1
        assert all(tuple(y) in linebus_neighbors(x) for x,y in zip(answer['path'],answer['path'][1:]))
        edges=[edge_info(x,y) for x,y in zip(answer['path'],answer['path'][1:])]
        assert answer['frame_exponent']==sum(x['hamming'] for x in edges)%4
        assert answer['loss_db']==pytest.approx(sum(edge_loss(x) for x in edges))
        assert 0<answer['conditional_path_survival']<=1

def test_phase_constrained_route_and_fault_injection():
    for row in route_casebook():
        a,b=row['start'],row['end']
        base,phase,fault=row['loss_optimized'],row['frame_zero'],row['bus0_failed']
        assert base['reachable'] and phase['reachable'] and fault['reachable']
        assert phase['frame_exponent']==0
        assert phase['loss_db']>=base['loss_db']-1e-10
        assert all(edge_info(x,y)['line']!=0 for x,y in zip(fault['path'],fault['path'][1:]))
        assert fault['faulted_buses']==[0]

def test_qutrit_four_mode_universal_vs_binary_xor_no_go():
    r=qutrit_bridge()
    assert r['exact_givens_cell_count']==3 and r['reconstruction_residual']<1e-11
    F=np.array(r['qutrit_F3_real'])+1j*np.array(r['qutrit_F3_imag'])
    assert np.linalg.norm(F.conj().T@F-np.eye(3))<1e-12
    for row in r['xor_projected_qutrit_leakage'][1:]:
        assert row['worst_case_basis_survival']==0.
        assert row['mean_basis_survival']==pytest.approx(2/3)
        assert row['singular_values_qutrit_subblock']==pytest.approx([1.,1.,0.])
    assert all(3 not in g['modes'] for g in r['givens'])

def test_walsh_static_interferometer_alternative_exact():
    r=qutrit_bridge()['walsh_alternative']
    assert r['dynamic_binary_phase_words']==2
    for row in r['phase_tables']:
        assert row['reconstruction_residual']<1e-12
        assert all(x in (-1,1) for x in row['diagonal_signs'])

def test_pdk_handoff_fails_closed_with_complete_electrical_logical_nets():
    obj=pdk_handoff()
    assert not obj['DRC_passed'] and not obj['foundry_pdk_selected']
    assert obj['40bus_cell_count']==160
    assert len({x['device'] for x in obj['cells']})==160
    assert len({x['ctrl'] for x in obj['cells']})==80
    assert all(x['physical_port_geometries'] is None for x in obj['cells'])
    assert all(x['electrode'].startswith('UNASSIGNED_') for x in obj['cells'])

def test_null_case():
    a=route_opt((7,7),(7,7),frame_target=0)
    assert a['reachable'] and a['hops']==0 and a['loss_db']==0.
    with pytest.raises(ValueError):route_opt((0,),(0,0))
    with pytest.raises(ValueError):measure_interference(visibility=0)
