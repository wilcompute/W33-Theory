"""Regression for W33's frozen twelve-perfect-matching four-lane scheduler."""
import random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_four_lane_scheduler_20261023 import (
    ADJ, LINE, MATCHINGS, COLOR, lane_for, sparse_counts,
    schedule_certificate, sparse_neighbors, sparse_route, route_bound, build
)
def test_one_factors_independent_geometry():
    assert len(COLOR)==240 and len(MATCHINGS)==12
    for group in MATCHINGS:
        vertices=[]
        for x in group:
            u,v=divmod(x,40)
            assert u<v and v in ADJ[u]
            vertices.extend((u,v))
        assert sorted(vertices)==list(range(40))
def test_slot_capacity_and_three_slot_optimality():
    s=schedule_certificate()
    assert len(s['links'])==240
    assert set(s['slot_link_counts'].values())=={80}
    assert s['logical_port_terminations']==480
    assert s['ideal_binary_2x2_switches_per_40child_parent']==320
    assert s['per_child_physical_link_terminations']==12
    assert all(LINE[l['lane']]==l['gateway_point'] for l in s['links'])
def test_sparse_recursive_link_counts():
    assert [sparse_counts(n)['total_logical_links'] for n in (1,2,3)]==[240,9840,393840]
    assert sparse_counts(3)['cartesian_total_links']==1152000
    assert [route_bound(n) for n in (1,2,3,4)]==[2,7,17,37]
def test_degree_sum_level2_and_exact_lanes():
    degree=sum(len(sparse_neighbors((i,j))) for i in range(40) for j in range(40))
    assert degree//2==9840
    from collections import Counter
    dist=Counter(len(sparse_neighbors((i,j))) for i in range(40) for j in range(40))
    assert dist[15]==160 and dist[12]==1440
def test_routes_legal_up_to_depth_five():
    rng=random.Random(4431)
    for n in range(1,6):
        for _ in range(50):
            a=tuple(rng.randrange(40) for _ in range(n))
            b=tuple(rng.randrange(40) for _ in range(n))
            p=sparse_route(a,b)
            assert p[0]==a and p[-1]==b
            assert len(p)-1<=route_bound(n)
            assert all(y in sparse_neighbors(x) for x,y in zip(p,p[1:]))
def test_manifest_is_deterministic_and_scoped():
    a,b=build(3),build(3)
    assert a['sha256']==b['sha256']
    assert a['comparison']['new_sparse_level2_diameter']==7
    assert any('NO' in a['evidence'] for _ in [0])
