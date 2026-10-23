"""Test synthetic W33 four-gateway parent scheduler and its evidence limits."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_gateway_scheduler_20261023 import gen_requests,schedule
from w33_fractal_port_fabric_20261023 import LINE,ADJ,base_route
def test_deterministic_replay():
    a=gen_requests(200,23);b=gen_requests(200,23)
    assert a==b
    assert schedule(a)==schedule(b)
def test_every_request_delivered_and_legally_routed():
    req=gen_requests(200,2026)
    x=schedule(req)
    assert len(x['records'])==len(req)==x['request_count']
    used=set()
    for r in x['records']:
        assert r['dst_child'] in ADJ[r['src_child']]
        assert r['gateway'] in LINE
        assert r['queue_wait']>=0
        assert r['completed_slot']>=r['cross_slot']+1
        assert r['local_src_hops']==len(base_route(r['src_local'],r['gateway']))-1
        for k in (r['src_child'],r['dst_child']):
            ident=(k,r['gateway'],r['cross_slot'])
            assert ident not in used
            used.add(ident)
def test_dedicated_and_shared_envelopes_are_distinct():
    req=gen_requests(500,20261023)
    a=schedule(req,'one-per-gateway');b=schedule(req,'dedicated-peer')
    assert a['total_queue_wait_slots']>b['total_queue_wait_slots']
    assert a['mean_queue_wait_slots']>b['mean_queue_wait_slots']
    assert b['request_count']==a['request_count']==500
def test_empty_and_invalid_mode():
    assert schedule([])['records']==[]
    try:schedule([],mode='invalid')
    except ValueError:pass
    else:raise AssertionError('invalid mode accepted')
