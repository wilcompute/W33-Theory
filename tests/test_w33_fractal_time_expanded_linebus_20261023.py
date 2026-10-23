"""Three-slot time-expanded W33 line-bus physical-consistency checks."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_time_expanded_linebus_20261023 import (
    geometry_slot_audit,mask_for_edge,slot_for_edge,fixed_path_schedule,
    timed_shortest,compare_routes,report
)
from w33_fractal_linebus_switch_matrix_20261023 import EDGE_LINE

def test_each_slot_has_80_edges_and_each_child_4_edges():
    s=geometry_slot_audit()
    assert s['edges_per_global_slot']=={0:80,1:80,2:80}
    assert s['per_node_available_edges_per_slot']==4

def test_fixed_route_requires_valid_slot_or_explicit_wait():
    for path in ((0,4,7),(0,14,7)):
        for initial in range(3):
            s=fixed_path_schedule(path,initial)
            assert s['hops']==2
            assert s['wait_slots']==s['elapsed_slots']-2
            assert s['arrival_tick']==initial+s['elapsed_slots']
            now=path[0]
            for ev in s['events']:
                if ev['kind']=='MOVE':
                    assert ev['source']==now
                    assert slot_for_edge(ev['source'],ev['target'])==ev['slot']
                    now=ev['target']
            assert now==path[-1]

def test_fixed_w33_interference_routes_need_alignment():
    s=compare_routes()
    assert s['slot_arrival_difference']==-1
    assert s['optical_frame_difference_mod4']==1
    assert not s['can_interfere_without_time_alignment_in_this_model']
    assert s['arm_a']['requires_optical_storage'] or s['arm_b']['requires_optical_storage']

def test_timed_bfs_uses_exact_480_states_and_legal_steps():
    r=report()
    assert r['time_expanded_state_count']==480
    for q in r['examples']:
        x=q['result']
        assert x['reachable']
        assert x['elapsed_slots']==len(x['actions'])
        assert x['hops']+x['wait_slots']==x['elapsed_slots']
        if q['required_frame'] is not None:
            assert x['frame_exponent']==q['required_frame']
        for ev in x['actions']:
            if ev['kind']=='MOVE':
                assert slot_for_edge(ev['a'],ev['b'])==ev['slot']

def test_failure_does_not_traverse_failed_bus():
    for a,b in ((0,7),(0,31),(8,17)):
        ans=timed_shortest(a,b,failed_buses=(0,))
        assert ans['reachable']
        for ev in ans['actions']:
            if ev['kind']=='MOVE':
                assert EDGE_LINE[tuple(sorted((ev['a'],ev['b']))) ]!=0

def test_reproducible():
    a=report()
    assert report()['sha256']==a['sha256']
    v={k:x for k,x in a.items() if k!='sha256'}
    assert hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()==a['sha256']
