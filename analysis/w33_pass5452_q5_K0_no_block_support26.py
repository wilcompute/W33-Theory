#!/usr/bin/env python3
"""Pass5452: q=5 K0 has no P-block support of size 26.

Pass5447 reduces any hypothetical 26-block K0 support S to one of 21 relation
profiles in the q5 R1/R2/R3 block association scheme.  In particular the number
`a` of R1 pairs satisfies 310<=a<=316, so the R1 graph induced on S has at least
310 of its C(26,2)=325 possible edges.

This pass reconstructs the exact R1 graph (SRG(325,144,68,60)) from Pass5230 and
enumerates every maximal clique.  The complete census is

  size 7: 780000,   size 15: 3120,   size 25: 156.

Turán: a 26-vertex graph with clique number <=12 has at most309 edges
(T_12(26)), so S contains an R1 clique Q of size at least13.  Extend Q to a
maximal R1 clique C.

For every maximal 15-clique, every outside vertex has 0,6,or10 neighbors in C,
so degree into C is at most10.  If k=|S cap C|>=13, the cross nonedge count is at
least (26-k)(k-10)>=39, contradicting the Pass5447 bound of at most15 non-R1
pairs.

For every maximal 25-clique, every outside vertex has exactly10 neighbors in C.
Thus the same bound gives (26-k)(k-10)<=15, with 13<=k<=25, whose only solution
is k=25.  The 156 maximal 25-cliques are exactly the 156 W-point footprints.
So S would be a point footprint plus one outside block.  Pass5447 exhaustively
checks all156*300=46800 such extensions and finds none satisfying the K0
no-singleton shell law.  Contradiction.

Therefore no nonzero K0 word has P-block support 26.
"""
from __future__ import annotations
import json,itertools
from collections import Counter
from pathlib import Path
import networkx as nx
from analysis import w33_pass5230_5237_footprint_rank4_breakthrough as p5230
from analysis.w33_pass5447_q5_K0_weight1040_support_reduction import feasible_profiles
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5452_Q5_K0_NO_BLOCK_SUPPORT26.json'

def turan_edges(n,r):
    q,s=divmod(n,r)
    parts=[q+1]*s+[q]*(r-s)
    return (n*n-sum(x*x for x in parts))//2

def main():
    A=p5230.A;F=p5230.F;O8=list(p5230.O8)
    G=nx.from_numpy_array(A)
    maximal=[];census=Counter()
    for C in nx.find_cliques(G):
        census[len(C)]+=1
        if len(C)>=13:maximal.append(tuple(sorted(C)))
    assert census==Counter({7:780000,15:3120,25:156})
    assert turan_edges(26,12)==309
    assert min(a for a,b,c,s2 in feasible_profiles())==310

    C15=[C for C in maximal if len(C)==15];C25=[C for C in maximal if len(C)==25]
    d15=Counter();d25=Counter()
    for C in C15:
        S=set(C)
        for u in range(325):
            if u not in S:d15[sum(1 for v in S if A[u,v])]+=1
    for C in C25:
        S=set(C)
        for u in range(325):
            if u not in S:d25[sum(1 for v in S if A[u,v])]+=1
    assert d15==Counter({6:780000,10:140400,0:46800})
    assert d25==Counter({10:46800})

    point_footprints={tuple(sorted(F[p].nonzero()[0])) for p in range(F.shape[0])}
    assert len(point_footprints)==156 and set(C25)==point_footprints

    # Pure arithmetic cross-nonedge obstruction.
    assert all((26-k)*(k-10)>15 for k in range(13,16))
    good25=[k for k in range(13,26) if (26-k)*(k-10)<=15]
    assert good25==[25]

    def no_singleton(S):
        return all(sum(j in S for j in D)!=1 for D in O8)
    tested=0;survivors=0
    for C in C25:
        S=set(C)
        for u in range(325):
            if u in S:continue
            tested+=1
            if no_singleton(S|{u}):survivors+=1
    assert tested==46800 and survivors==0

    out={
      'pass':5452,'status':'THEOREM_Q5_K0_NO_P_BLOCK_SUPPORT26',
      'R1_graph':'SRG(325,144,68,60)',
      'maximal_clique_census':{str(k):v for k,v in sorted(census.items())},
      'Turan_T12_26_edges':309,
      'candidate_R1_edge_lower_bound':310,
      'maximal15_outside_degree_census':{str(k):v for k,v in sorted(d15.items())},
      'maximal25_outside_degree_census':{str(k):v for k,v in sorted(d25.items())},
      'maximal25_identification':'exactly the156 W-point footprints',
      'point_footprint_plus_one_extensions_tested':tested,
      'survivors':survivors,
      'conclusion':'No nonzero q5 K0 word has P-block support exactly26.',
      'boundary':'This does not yet classify block support27 or determine the exact second block weight.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
