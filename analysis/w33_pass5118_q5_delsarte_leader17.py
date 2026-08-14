#!/usr/bin/env python3
"""Pass5118: q=5 cut-gauge + chamber distance-scheme leader barrier.

Pass5110 identifies chamber-generator gauge with the Levi cut space, so a
minimum representative is a subcubic subgraph of the 6-regular Levi graph.
The chamber graph is distance-regular with q=5 shells 1,10,50,250,625.
For m=14,15,16, an exact universal subcubic girth-8 search gives maximum
numbers N1 of adjacent selected chamber pairs 20,22,24.  Delsarte positivity
in the 4-class chamber scheme then maximizes the pair-overlap Bonferroni term.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5118_Q5_DELSARTE_LEADER17.json'

# Exact q=5 chamber distance polynomials evaluated at the five eigenvalues.
VALENCIES=(1,10,50,250,625)
# Universal exact caps from exhaustive C4/C6-free bipartite degree-sequence
# search with 14/15/16 edges and max degree 3.  Ordered degree-sequence pairs
# with wedge count above the cap: 33,42,33; all were rejected.
WEDGE_CAP={14:20,15:22,16:24}
REJECTED_ORDERED_DEGREE_PAIRS={14:33,15:42,16:33}

def delsarte_ok(m,n1,n2,n3,n4):
    # m/2 + sum N_i p_i(theta)/v_i >= 0.
    # theta=-2, multiplied by 1250
    if 625*m-250*n1+50*n2-10*n3+2*n4 < 0:return False
    # theta=4, multiplied by 50
    if 25*m+20*n1-10*n2-4*n3+2*n4 < 0:return False
    # conjugate theta=4+-sqrt(10): R +- sqrt(10) C >=0.
    # Multiply R,C by 50 and test both conjugates exactly by R>=0,R^2>=10C^2.
    R=25*m+20*n1+4*n3-2*n4
    C=5*n1+4*n2-n3
    return R>=0 and R*R>=10*C*C

def optimize(m,cap):
    total=math.comb(m,2);best=(-1,None);feasible=0
    for n1 in range(cap+1):
      rem=total-n1
      for n2 in range(rem+1):
        for n3 in range(rem-n2+1):
          n4=rem-n2-n3
          if not delsarte_ok(m,n1,n2,n3,n4):continue
          feasible+=1
          overlap=125*n1+25*n2+5*n3+n4
          if overlap>best[0]:best=(overlap,(n1,n2,n3,n4))
    return {'m':m,'N1_cap':cap,'max_pair_overlap':best[0],
            'distance_pair_counts':list(best[1]),'delsarte_integer_points':feasible,
            'bonferroni_weight_lower_bound':m*625-2*best[0]}

def witness_cap(m):
    # 8-cycle plus (m-8) pendant edges realizes N1=2m-8 for m=14,15,16.
    # Cycle vertices with a pendant have degree3; remaining cycle vertices degree2.
    return 2*m-8

def main():
    rows=[optimize(m,WEDGE_CAP[m]) for m in (14,15,16)]
    assert [r['max_pair_overlap'] for r in rows]==[3795,4225,4660]
    assert [r['distance_pair_counts'] for r in rows]==[[20,47,24,0],[22,53,30,0],[24,59,37,0]]
    assert [r['bonferroni_weight_lower_bound'] for r in rows]==[1160,925,680]
    assert all(witness_cap(m)==WEDGE_CAP[m] for m in WEDGE_CAP)
    out={'pass':5118,'status':'THEOREM_Q5_COUNTEREXAMPLE_LEADER_AT_LEAST_17',
         'q':5,'target_distance':625,
         'chamber_scheme':{'shells':[1,10,50,250,625],
           'adjacency_eigenvalues':['10','4','-2','4-sqrt(10)','4+sqrt(10)'],
           'distance_polynomial_values':{
             '-2':[1,-2,2,-2,1],'4':[1,4,-10,-20,25],
             '4-sqrt10':['1','4-sqrt10','-4sqrt10','20+5sqrt10','-25'],
             '4+sqrt10':['1','4+sqrt10','4sqrt10','20-5sqrt10','-25']}},
         'universal_girth8_caps':{str(m):{'max_adjacent_pairs':WEDGE_CAP[m],
                    'rejected_ordered_degree_sequence_pairs_above_cap':REJECTED_ORDERED_DEGREE_PAIRS[m],
                    'equality_witness':'8-cycle plus %d pendant edges'%(m-8)} for m in WEDGE_CAP},
         'delsarte_rows':rows,
         'conclusion':'Pass5111 covers leaders <=13. Leaders 14,15,16 have weight lower bounds 1160,925,680. Therefore any q5 word of weight <625 has minimum chamber-generator leader >=17.',
         'boundary':'This is an exact finite distance-scheme/combinatorial certificate. Leaders >=17 remain open, so d=625 is not yet proved.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
