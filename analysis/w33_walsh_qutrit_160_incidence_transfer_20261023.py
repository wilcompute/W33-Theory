#!/usr/bin/env python3
"""Inter-bus Walsh qutrit transfer on the REAL 160 point-line incidence labels.

Mathematical complete-rank transfer target: four DISTINCT incidence rails
must be routed coherently from one W33 four-port line bus to another.
A shared W33 point is NOT a free shared physical optical waveguide.
Topology: 240 intra-line links + 240 inter-bus point coupler links,
each degree 6; point couplers and actual optical delays are UNBUILT.
"""
import collections,hashlib,itertools,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_fractal_linebus_switch_matrix_20261023 import LINES
from w33_pic_xor_walsh_pareto_20261023 import H4

def incidence_graph():
    by_point=collections.defaultdict(list)
    adj=[set() for _ in range(160)]
    for line in range(40):
        for port,p in enumerate(LINES[line]):
            by_point[p].append(4*line+port)
        for i,j in itertools.combinations(range(4),2):
            a,b=4*line+i,4*line+j
            adj[a].add(b);adj[b].add(a)
    for p,ids in by_point.items():
        assert len(ids)==4
        for a,b in itertools.combinations(ids,2):
            adj[a].add(b);adj[b].add(a)
    assert len(by_point)==40
    assert all(len(neighbors)==6 for neighbors in adj)
    return adj,by_point

def transfer(a,b):
    if a not in range(40) or b not in range(40) or a==b:raise ValueError('distinct line IDs')
    common=sorted(set(LINES[a])&set(LINES[b]))
    assert len(common)<=1
    oa=common+sorted(set(LINES[a])-set(common))
    ob=common+sorted(set(LINES[b])-set(common))
    rails_a=[4*a+LINES[a].index(p) for p in oa]
    rails_b=[4*b+LINES[b].index(p) for p in ob]
    assert len(set(rails_a+rails_b))==8 # physically distinct incidence rails
    P=np.arange(160)
    for x,y in zip(rails_a,rails_b):
        P[x],P[y]=P[y],P[x]
    Vsrc=np.zeros((160,3));Vdst=np.zeros((160,3))
    Vsrc[rails_a,:]=H4()[:,1:4]
    Vdst[rails_b,:]=H4()[:,1:4]
    # Row permutation action: updated rail amplitude at k = old amplitude at P[k].
    err=float(np.linalg.norm(Vsrc[P,:]-Vdst))
    assert err<1e-12
    assert np.linalg.norm(Vdst.T@Vdst-np.eye(3))<1e-12
    local_same_point=bool(common)
    if common:
        assert oa[0]==ob[0]
    return {'lines':[a,b],'point_intersection':common,
      'source_160_incidence_rails':rails_a,
      'destination_160_incidence_rails':rails_b,
      'four_pair_swaps':[[x,y] for x,y in zip(rails_a,rails_b)],
      'number_of_distinct_physical_rail_swaps':4,
      'one_direct_point_coupler_possible':local_same_point,
      'three_nonlocal_rail_routes_required_at_least':3 if common else 4,
      'qutrit_transfer_residual':err,
      'physical_reality':'This is a 160-mode target permutation, not a placed/routed chip or parallel optical switch schedule'}

def report():
    adj,pts=incidence_graph()
    hist=collections.Counter()
    cases={}
    for a,b in itertools.combinations(range(40),2):
        t=transfer(a,b)
        n=len(t['point_intersection'])
        hist[n]+=1
        if n not in cases: cases[n]=t
    assert hist=={0:540,1:240}
    out={'schema':'w33.walsh.qutrit.160_incidence_transfer.v1',
      'distinct_physical_incidence_ports':160,
      'W33_line_buses':40,'point_coupler_junctions':40,
      'intra_line_possible_neighbor_links':240,
      'inter_line_same_point_possible_coupler_links':240,
      'graph_all_incidence_degree':6,
      'line_pairs_checked':780,'intersections':dict(sorted(hist.items())),
      'exact_transfer':{'intersecting':cases[1],'disjoint':cases[0]},
      'optical_validation_gates':['physically implement 4 distinct interbus optical rail transfers even when buses share a W33 graph point',
        'source and target 4-rail mode matching and optical path phase',
        'enforce collision-free temporal scheduling simultaneously on all 4 rails',
        'calibrate 4x4 complex transfer including uniform auxiliary Walsh mode',
        'route valid electrode pads and junction couplers under chosen PDK and run foundry DRC/LVS'],
      'not_established':['manufacturable photonic chip','parallel switch schedule','optical quantum memory','real transfer fidelity','no-cloning compatible copy; this is MOVE not COPY']}
    out['sha256']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return out
if __name__=='__main__':
    x=report()
    p=ROOT/'data/w33_walsh_qutrit_160_incidence_transfer_20261023.json'
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
    print('PASS 160-incidence interbus transfer',x['line_pairs_checked'],x['intersections'])
