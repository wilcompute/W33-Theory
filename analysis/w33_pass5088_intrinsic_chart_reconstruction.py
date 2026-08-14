#!/usr/bin/env python3
"""Pass5088 (outside box): reconstruct q=3 opposite-pair charts from the code alone.

Pass5081 says the complete dual minimum shell is exactly the theta triples, so
start only from those 3-subsets of apartment coordinates.  Form their
intersection graph.  Among its K4 cliques, select those whose four triples have
six-coordinate union and every coordinate occurs twice.  Exactly 1080 survive,
and their six-sets are exactly the opposite-pair K4-cut charts.  The final
comparison to W(3,3) labels is a certificate; the reconstruction rule itself is
code-intrinsic.
"""
from __future__ import annotations
from collections import Counter
import itertools,json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5088_INTRINSIC_CHART_RECONSTRUCTION.json'

def main():
    G=build_W(3);theta=[]
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(4),3):
            theta.append(tuple(sorted((loc[tuple(sorted((i,j)))],loc[tuple(sorted((i,k)))],loc[tuple(sorted((j,k)))]))))
    theta=sorted(set(theta));m=len(theta);assert m==4320
    bycoord={}
    for t,T in enumerate(theta):
        for a in T:bycoord.setdefault(a,[]).append(t)
    nbr=[set() for _ in range(m)]
    for ids in bycoord.values():
        for i,j in itertools.combinations(ids,2):nbr[i].add(j);nbr[j].add(i)
    assert set(map(len,nbr))=={21}
    k4=set()
    for a in range(m):
        for b in (x for x in nbr[a] if x>a):
            common=sorted(x for x in (nbr[a]&nbr[b]) if x>b)
            for ii,c in enumerate(common):
                for d in common[ii+1:]:
                    if d in nbr[c]:k4.add((a,b,c,d))
    recovered=set()
    for Q in k4:
        cnt=Counter(x for t in Q for x in theta[t])
        if len(cnt)==6 and set(cnt.values())=={2}:recovered.add(frozenset(cnt))
    actual={frozenset(loc.values()) for _,loc in G['charts']}
    assert len(k4)==114480 and len(recovered)==1080 and recovered==actual
    out={'pass':5088,'status':'THEOREM_Q3_CODE_INTRINSIC_CHART_RECOVERY','dual_minimum_checks':m,
         'check_intersection_degree':21,'K4_cliques':len(k4),'tetrahedral_six_coordinate_K4s':len(recovered),
         'recovered_charts':len(recovered),'actual_opposite_pair_charts':len(actual),'exact_match':True,
         'intrinsic_rule':'Take K4s of weight-3 dual-word intersection graph; retain four triples whose union has six coordinates each appearing exactly twice.',
         'compiler_consequence':'The 1080 local K4 cut charts, and hence the Pass5078 eight-entry q3 local decoder placement, can be synthesized from the code dual shell without external W33 labels.',
         'boundary':'Exact q=3 finite-code reconstruction; no all-q uniqueness theorem is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
