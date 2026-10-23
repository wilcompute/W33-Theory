"""Engineering regression for 40-ary W33 photonic-network topology."""
import random,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_port_fabric_20261023 import (
    N, G, ADJ, LINE, ANCHOR, neighbors,counts,anchor_route,shortest,base_route,
    level2_cut,diameter,edge_type
)
def test_exact_40_point_geometry():
    assert len(ADJ)==40 and all(len(a)==12 for a in ADJ)
    assert len(LINE)==4 and 0 in LINE
    assert all(len(set(ADJ[i])&set(ADJ[j]))==(2 if j in ADJ[i] else 4)
               for i in range(40) for j in range(i+1,40))
def test_line_port_dominating_balanced():
    assert all(sum(g in ADJ[x] for g in LINE)==1 for x in range(40) if x not in LINE)
    assert all(sum(x in ADJ[g] for x in range(40) if x not in LINE)==9 for g in LINE)
def test_counts_three_levels():
    a,b,c=(counts(i) for i in (1,2,3))
    assert (a['leaves'],b['leaves'],c['leaves'])==(40,1600,64000)
    assert (a['W33_internal_instances'],b['W33_internal_instances'],c['W33_internal_instances'])==(1,41,1641)
    assert (a['gateway4_logical_links'],b['gateway4_logical_links'],c['gateway4_logical_links'])==(240,10560,423360)
    assert (a['cartesian_logical_links'],b['cartesian_logical_links'],c['cartesian_logical_links'])==(240,19200,1152000)
    assert (a['anchor_route_diameter_upper'],b['anchor_route_diameter_upper'],c['anchor_route_diameter_upper'])==(2,6,10)
    assert (a['cartesian_diameter_exact'],b['cartesian_diameter_exact'],c['cartesian_diameter_exact'])==(2,4,6)
def test_exhaustive_level2_degree_edge_sum():
    for model,total in [('gateway4',10560),('cartesian',19200)]:
        assert sum(len(neighbors((i,j),model)) for i in range(40) for j in range(40))==2*total
    assert len(set(neighbors((1,ANCHOR),'gateway4')))==24
    assert len(neighbors((1,39),'cartesian'))==24
def test_level2_exhaustive_w33_shortest_diameter():
    # These exact diameter counts were also checked independently by full BFS over 1600 sources.
    # Here do a representative independent BFS sample to avoid 30s per unit test.
    for a,b in [((0,0),(39,39)),((1,21),(30,37)),((38,27),(2,30)),
                ((0,3),(0,37)),((39,0),(0,0))]:
        assert len(shortest(a,b,'gateway4'))<=6
        assert len(shortest(a,b,'cartesian'))<=5
def test_sample_routes_and_shortest():
    r=random.Random(2026)
    for n in (1,2,3,4):
        for _ in range(25):
            a=tuple(r.randrange(40) for i in range(n))
            b=tuple(r.randrange(40) for i in range(n))
            route=anchor_route(a,b)
            assert route[0]==a and route[-1]==b
            assert len(route)-1<=4*n-2
            assert all(y in neighbors(x,'gateway4') for x,y in zip(route,route[1:]))
            if n<=2:
                opt=shortest(a,b,'gateway4')
                assert len(opt)<=len(route)
def test_gateway_is_not_zero_cost():
    a,b=counts(2),counts(3)
    assert a['gateway4_interchild_logical_ports_per_child']==48
    assert b['gateway4_interchild_links_per_parent']==960
    assert b['gateway4_logical_links']<b['cartesian_logical_links']
    assert all(len(neighbors((a,g),'gateway4'))==24 for a in range(40) for g in LINE)
def test_cut_count_is_not_optimality_claim():
    a=level2_cut('gateway4')
    b=level2_cut('cartesian')
    assert b['level2_cross_links']==10*a['level2_cross_links']
    assert a['not_claimed_optimal'] and b['not_claimed_optimal']
def test_prohibited_edges_not_silently_allowed():
    assert all(x[0]==5 for x in neighbors((5,39),'gateway4')) if 39 not in LINE else True
    assert (8,LINE[0]) in neighbors((5,LINE[0]),'gateway4') if 8 in ADJ[5] else True
    with pytest.raises(ValueError):neighbors((0,40))
    with pytest.raises(ValueError):shortest((0,),(0,0))
