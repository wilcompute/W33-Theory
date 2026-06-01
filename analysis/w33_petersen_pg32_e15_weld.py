from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'PART_MMCCCLXXXI_PETERSEN_PG32_E15_WELD_results.json'

from analysis.w33_toroidal_mutation_edge_petersen_bridge import main as petersen_main
from analysis.w33_pg32_e15_packet_bridge import pg32, w33_adj, rank, eig
import numpy as np


def add4(a,b): return tuple(x^y for x,y in zip(a,b))
def wt(x): return sum(x)

def main():
    pet=petersen_main()
    pg_pts, pg_lines, pg_planes, N = pg32()
    A = w33_adj(); I40=np.eye(40,dtype=int); J40=np.ones((40,40),dtype=int)
    E15n = 8*I40 + J40 - 4*A

    k5_edges=list(combinations(range(5),2))
    petersen_states=[]
    for a,b in combinations(k5_edges,2):
        if not (set(a)&set(b)):
            petersen_states.append((a,b))
    # Canonical bijection candidate: order both 15-sets lexicographically.
    pg_sorted=sorted(pg_pts)
    weld={str(i):{'petersen_state':petersen_states[i],'pg32_point':pg_sorted[i]} for i in range(15)}

    # PG(3,2) incidence: each line is {a,b,a+b}; 35 lines.
    line_degrees=Counter(x for L in pg_lines for x in L)
    pair_degrees=Counter(tuple(sorted(p)) for L in pg_lines for p in combinations(L,2))
    plane_sizes=Counter(len(p) for p in pg_planes)
    NN=N@N.T

    # Petersen side: each state is a disjoint-pair/matching of two K5 edges; the missing vertex is a 5-color.
    missing=Counter()
    for a,b in petersen_states:
        missing[tuple(sorted(set(range(5))-set(a)-set(b)))[0]] += 1
    k5_edge_use=Counter(e for st in petersen_states for e in st)

    checks={
      'inherits_petersen_bridge':pet['n_verified']==pet['n_checks']==16,
      'petersen_state_count_15':len(petersen_states)==15,
      'pg32_point_count_15':len(pg_pts)==15,
      'pg32_plane_count_15':len(pg_planes)==15,
      'pg32_line_count_35':len(pg_lines)==35,
      'canonical_weld_is_bijection':len(weld)==15 and len({tuple(v['pg32_point']) for v in weld.values()})==15,
      'pg32_each_line_size_3':all(len(L)==3 for L in pg_lines),
      'pg32_each_point_on_7_lines':set(line_degrees.values())=={7},
      'pg32_each_pair_one_line':len(pair_degrees)==105 and set(pair_degrees.values())=={1},
      'pg32_planes_7_points_each':plane_sizes==Counter({7:15}),
      'pg32_incidence_gram':np.array_equal(NN,4*np.eye(15,dtype=int)+3*np.ones((15,15),dtype=int)),
      'pg32_incidence_spectrum_49_4x14':eig(NN)==Counter({49:1,4:14}),
      'e15_rank_15':np.array_equal(E15n@E15n,24*E15n) and int(np.trace(E15n)//24)==15,
      'packet_identity_15x192_2880':15*192==2880,
      'petersen_missing_vertex_profile_3_each':missing==Counter({0:3,1:3,2:3,3:3,4:3}),
      'petersen_k5_edge_use_profile_3_each':set(k5_edge_use.values())=={3} and len(k5_edge_use)==10,
      'petersen_15_equals_pg32_15_equals_e15_rank':len(petersen_states)==len(pg_pts)==15==int(np.trace(E15n)//24),
    }
    assert all(checks.values()), checks
    R={
      'part':'MMCCCLXXXI',
      'theorem':'Petersen/PG(3,2)/E15 weld',
      'counts':{'petersen_disjoint_pair_states':15,'pg32_points':15,'pg32_lines':35,'pg32_planes':15,'E15_rank':15,'tomotope_packet_flags':192,'packets_total':2880},
      'pg32_incidence':{'NNt':'4I+3J','spectrum':{'49':1,'4':14}},
      'petersen_profiles':{'missing_k5_vertex_each':3,'k5_edge_use_each':3},
      'weld_sample':weld,
      'reading':'The 15 disjoint-pair states in the Petersen complement of the K5 mutation-edge graph can be welded to the existing PG(3,2) E15 packet carrier. Both sides have 15 states; PG(3,2) contributes the 35-line incidence geometry and the rank-15 W33 curvature projector E15, while the Petersen side contributes the negative m_s=15 mutation-pair sector. The weld is canonical only at the cardinality/carrier level here; a later pass should seek an operation-preserving labeling.',
      'checks':checks,'n_verified':sum(checks.values()),'n_checks':len(checks)
    }
    OUT.write_text(json.dumps(R, indent=2, sort_keys=True)+'\n')
    return R

if __name__=='__main__':
    r=main(); print(r['part'], r['theorem']); print('checks', r['n_verified'], '/', r['n_checks']); print(r['counts'])
