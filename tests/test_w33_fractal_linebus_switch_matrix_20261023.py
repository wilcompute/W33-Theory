"""The W33 line-bus switch is an exact 4-port permutation specification."""
import sys,random
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import (
    LINES,THROUGH,EDGE_LINE,PORT_NO,LINE,portal,permutation_matrix,
    xor_permutation,bus_schedule,linebus_neighbors,linebus_route,counts,build)
def test_geometry_40_buses_with_160_incidents():
    assert len(LINES)==40 and len(EDGE_LINE)==240
    assert all(len(THROUGH[i])==4 for i in range(40))
    assert sum(len(x) for x in LINES)==160
    assert all(len(set(x))==4 for x in LINES)
def test_permutation_group_is_klein_four():
    P=[permutation_matrix(i) for i in range(4)]
    for k in range(4):
        assert np.array_equal(P[k].T@P[k],np.eye(4,dtype=int))
        for j in range(4):
            assert np.array_equal(P[k]@P[j],P[k^j])
    assert [xor_permutation(i) for i in (1,2,3)]==[
        (1,0,3,2),(2,3,0,1),(3,2,1,0)]
def test_every_bus_pair_covered_in_three_slots():
    s=bus_schedule()
    assert len(s)==120
    edges=set()
    for row in s:
        assert len(row['pairs'])==2
        for a,b in row['pairs']:
            assert (a,b) not in edges;edges.add((a,b))
    assert len(edges)==240
    assert [sum(len(r['pairs']) for r in s if r['slot']==i) for i in range(3)]==[80,80,80]
def test_parent_geometry_port_mapping():
    s=build(2)
    assert s['per_parent']['four_port_buses']==40
    assert s['per_parent']['bus_endpoint_incidents']==160
    assert s['per_parent']['generic_4x4_mesh_mzi_estimate_per_parent']==240
    for child in range(40):
        ps=s['bus_port_map'][str(child)]
        assert len(ps)==4
        assert set(p['child_port_address'] for p in ps)==set(LINE)
def test_leaf_level2_undirected_edge_count():
    adj={a:linebus_neighbors(a) for a in ((i,j) for i in range(40) for j in range(40))}
    assert sum(len(v) for v in adj.values())==2*9840
    assert all(a in adj[b] for a,neighbors in adj.items() for b in neighbors)
def test_recursive_routes_to_depth_four():
    rng=random.Random(72)
    for n in (1,2,3,4):
        for _ in range(25):
            a=tuple(rng.randrange(40) for i in range(n))
            b=tuple(rng.randrange(40) for i in range(n))
            r=linebus_route(a,b)
            assert r[0]==a and r[-1]==b
            assert all(y in linebus_neighbors(x) for x,y in zip(r,r[1:]))
def test_counts_and_reproducible_digest():
    s=build(3)
    assert s['sha256']==build(3)['sha256']
    assert counts(2)['interchild_4port_buses']==40
    assert counts(3)['interchild_4port_buses']==1640
    assert any('not claimed new' in x for x in s['scope_warnings'])
