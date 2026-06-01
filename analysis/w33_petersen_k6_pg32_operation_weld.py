from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXII_PETERSEN_K6_PG32_OPERATION_WELD_results.json'

from analysis.w33_petersen_pg32_e15_weld import main as weld_main
from analysis.w33_pg32_e15_packet_bridge import pg32


def bxor(a,b): return tuple(x^y for x,y in zip(a,b))
def vxor3(a,b,c): return bxor(bxor(a,b),c)

def perfect_matchings(vertices):
    vertices=tuple(vertices)
    if not vertices:
        return [tuple()]
    a=vertices[0]
    out=[]
    for i in range(1,len(vertices)):
        b=vertices[i]
        rest=vertices[1:i]+vertices[i+1:]
        for m in perfect_matchings(rest):
            out.append(tuple(sorted(((min(a,b),max(a,b)),)+m)))
    return sorted(set(out))

def main():
    weld=weld_main()
    k5_edges=list(combinations(range(5),2))
    p_edges=[]
    for i,j in combinations(range(len(k5_edges)),2):
        if set(k5_edges[i]).isdisjoint(k5_edges[j]):
            p_edges.append((i,j))
    p_vertices=range(len(k5_edges))
    p_matchings=perfect_matchings(p_vertices)
    p_matchings=[m for m in p_matchings if all(e in p_edges or (e[1],e[0]) in p_edges for e in m)]
    edge_to_matchings=defaultdict(list)
    for mi,M in enumerate(p_matchings):
        for e in M:
            edge_to_matchings[tuple(sorted(e))].append(mi)
    duad_to_edge={tuple(ms):e for e,ms in edge_to_matchings.items()}

    k6_vertices=range(6)
    k6_edges=list(combinations(k6_vertices,2))
    triangles=[]
    for T in combinations(k6_vertices,3):
        triangles.append(tuple(sorted(tuple(sorted(e)) for e in combinations(T,2))))
    onefactors=perfect_matchings(k6_vertices)
    k6_blocks=[tuple(sorted(B)) for B in triangles+onefactors]
    k6_to_pedge={duad:duad_to_edge[duad] for duad in k6_edges}
    edge_index={e:i for i,e in enumerate(sorted(p_edges))}
    sts_blocks={tuple(sorted(edge_index[k6_to_pedge[e]] for e in B)) for B in k6_blocks}

    pair_count=Counter(tuple(sorted(p)) for B in sts_blocks for p in combinations(B,2))
    point_degree=Counter(x for B in sts_blocks for x in B)

    # Explicit PG(3,2) labeling from K6 duads: label duad ij by u_i + u_j in F2^4.
    u=[(0,0,0,0),(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,1,1)]
    duad_label={e:bxor(u[e[0]],u[e[1]]) for e in k6_edges}
    labels=set(duad_label.values())
    label_blocks={tuple(sorted(duad_label[e] for e in B)) for B in k6_blocks}
    zero_sum_blocks={B for B in combinations(sorted(labels),3) if vxor3(*B)==(0,0,0,0)}

    pg_pts,pg_lines,pg_planes,N=pg32()
    pg_line_vecs={tuple(sorted(pg_pts[i] for i in L)) for L in pg_lines}

    checks={
      'inherits_weld_result':weld['n_verified']==weld['n_checks']==17,
      'petersen_vertices_10_edges_15':len(k5_edges)==10 and len(p_edges)==15,
      'petersen_perfect_matchings_6':len(p_matchings)==6,
      'each_petersen_edge_in_two_matchings':Counter(len(v) for v in edge_to_matchings.values())==Counter({2:15}),
      'duads_are_k6_edges':set(duad_to_edge)==set(k6_edges),
      'k6_triangles_20_onefactors_15':len(triangles)==20 and len(onefactors)==15,
      'sts_blocks_35':len(sts_blocks)==35,
      'sts_each_point_degree_7':Counter(point_degree.values())==Counter({7:15}),
      'sts_each_pair_once':len(pair_count)==105 and set(pair_count.values())=={1},
      'f2_vertex_sum_zero':tuple(sum(x[i] for x in u)%2 for i in range(4))==(0,0,0,0),
      'duad_labels_all_15_nonzero':len(labels)==15 and (0,0,0,0) not in labels,
      'k6_blocks_equal_zero_sum_triples':label_blocks==set(tuple(sorted(B)) for B in zero_sum_blocks),
      'zero_sum_triples_35':len(zero_sum_blocks)==35,
      'zero_sum_triples_equal_pg32_lines':set(tuple(sorted(B)) for B in zero_sum_blocks)==pg_line_vecs,
      'operation_weld_petersen_to_pg32':len(sts_blocks)==len(pg_lines)==35,
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXII',
      'theorem':'Petersen/K6/PG(3,2) operation weld',
      'counts':{'petersen_vertices':10,'petersen_edges':15,'petersen_perfect_matchings':6,'k6_edges':15,'k6_triangles':20,'k6_onefactors':15,'sts_blocks':35,'pg32_lines':35},
      'construction':'Petersen edge -> pair of perfect matchings containing it -> K6 duad. PG(3,2) lines are exactly K6 triangles plus K6 one-factors under the F2^4 duad labeling u_i+u_j.',
      'f2_4_six_vertex_labels':u,
      'spectral_carrier':'The previous E15 weld supplies rank(E15)=15 and 15*192=2880; this pass supplies the operation-preserving line law on the 15 carrier states.',
      'reading':'This upgrades the prior cardinality weld to an operation-preserving weld. The 15 Petersen negative-sector states are canonically edges of K6 via the six perfect matchings of Petersen. The 35 PG(3,2) lines are exactly the 20 K6 triangles plus the 15 K6 one-factors, and under the explicit F2^4 labels every block has zero XOR sum. Thus the Petersen 15-sector carries the PG(3,2) line operation, not just the same cardinality.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['counts'])
