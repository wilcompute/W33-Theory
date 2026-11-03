"""A demand-specific exact capacity obstruction and constructive repairs.

Prior repo networking: BT3308_BT3319_knight_hypercube_gauge_closure.md.
Recent external comparison: Universal Nested Quantum Switch, arXiv2603.00236.
Bell-pair edge resources and coherent graph walks are different models.
"""
import collections
import itertools
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]


def cube_paths(a,b):
    bits=[i for i in range(4) if (a^b)>>i&1]
    for order in itertools.permutations(bits):
        path=[a]
        for j in order:path.append(path[-1]^(1<<j))
        yield path


def edges(path):return [tuple(sorted((a,b))) for a,b in zip(path,path[1:])]


def find_six():
    E=sorted({tuple(sorted((v,v^(1<<j)))) for v in range(16) for j in range(4)})
    ix={e:i for i,e in enumerate(E)}
    choices=[[((sum(1<<ix[e] for e in edges(path))),path) for path in cube_paths(a,a^15)] for a in range(8)]
    def search(remaining,used,selected):
        if len(selected)==6:return selected
        if len(selected)+len(remaining)<6:return None
        feasible={a:[(mask,path) for mask,path in choices[a] if not mask&used] for a in remaining}
        a=min(remaining,key=lambda a:len(feasible[a]));rest=[b for b in remaining if b!=a]
        for mask,path in feasible[a]:
            got=search(rest,used|mask,selected+[path])
            if got:return got
        return search(rest,used,selected)
    result=search(list(range(8)),0,[]);assert result and len(result)==6
    assert max(collections.Counter(e for path in result for e in edges(path)).values())==1
    return result


def build():
    six=find_six()
    doubled=[next(cube_paths(a,a^15)) for a in range(8)]
    loads=collections.Counter(e for path in doubled for e in edges(path))
    assert max(loads.values())==2
    assert len({v for path in doubled for v in [path[0],path[-1]]})==16
    # For k served antipodal requests in Q_even, each served endpoint has odd
    # used degree<=d-1. Other vertices have used degree<=d. Thus kd<=nd/2-k.
    assert 6*5<=32 and 7*5>32
    return dict(status='PASS_Q4_ANTIPODAL_SWITCH_CAPACITY',dimension=4,vertices=16,edges=32,
        requested_pairs=[[a,a^15] for a in range(8)],single_layer_maximum_served=6,
        single_layer_six_path_witness=six,doubled_resource_eight_path_witness=doubled,
        doubled_maximum_edge_load=2,
        upper_bound_proof='For k edge-disjoint antipodal paths, each path has length>=4, so at least4k edges are used. At each of the2k terminal vertices the used degree is odd and hence<=3; at other vertices it is<=4. Therefore used edges<=32-k. Thus5k<=32 and k<=6. The six-path witness attains the bound.',
        general_even_cube_bound='For Q_d with even d and n=2^d, at most floor(nd/(2(d+1))) antipodal requests can be served using one Bell pair per edge.',
        comparison='arXiv2603.00236 Theorem1 states pairwise universality after restricting to one hypercube layer, but its proof explicitly treats odd d and then invokes two resource copies for arbitrary d. The single-layer restriction is false for d=4 by this witness. This does not refute the full degree7 nested16-node resource or the two-layer repair.',
        boundary='Exact ideal edge-disjoint entanglement-swapping resource model, allowing several independent Bell qubits per intermediate node. No memory noise, calibration, throughput schedule or worst-case universality theorem for the full nested resource is claimed.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_hypercube_switch_capacity.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['single_layer_maximum_served'],d['single_layer_six_path_witness'],flush=True)
