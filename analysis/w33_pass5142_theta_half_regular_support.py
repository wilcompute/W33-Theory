#!/usr/bin/env python3
"""Pass5142: every apartment-code support is half-regular in the intrinsic theta graph.

The apartment code is the orthogonal complement of the theta-triple checks.  In
the theta point graph, two apartment variables are adjacent when they occur in a
theta triple.  Every variable lies in 4(q-1) theta triples and every adjacent pair
lies in a unique triple.  A selected variable therefore sees exactly one selected
and one unselected partner in each incident check; an unselected variable sees
0 or 2 selected partners per incident check.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W,chamber_stars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5142_THETA_HALF_REGULAR_SUPPORT.json'

def theta_checks(G):
    q=G['q'];out=set()
    for _,loc in G['charts']:
        for i,j,k in itertools.combinations(range(q+1),3):
            out.add(tuple(sorted((loc[(i,j)],loc[(i,k)],loc[(j,k)]))))
    return sorted(out)

def anchor(q):
    G=build_W(q);checks=theta_checks(G);n=len(G['apartments']);adj=[set() for _ in range(n)]
    for T in checks:
        for a,b in itertools.combinations(T,2):adj[a].add(b);adj[b].add(a)
    D=8*(q-1);assert {len(x) for x in adj}=={D}
    stars=chamber_stars(G)
    # deterministic nontrivial words beyond the single-star extremizer
    words=[stars[0],stars[0]^stars[1],stars[0]^stars[2]^stars[3]]
    prof=[]
    for z in words:
        S={a for a in range(n) if (z>>a)&1}
        if not S:continue
        # Theta parity is the code constraint.
        assert all(sum(a in S for a in T)%2==0 for T in checks)
        din={sum(b in S for b in adj[a]) for a in S}
        dout={sum(b not in S for b in adj[a]) for a in S}
        assert din==dout=={4*(q-1)}
        prof.append({'weight':len(S),'inside_degree':next(iter(din)),'outside_degree':next(iter(dout))})
    return {'q':q,'apartments':n,'theta_checks':len(checks),'theta_degree':D,
            'half_degree':4*(q-1),'sample_codewords':prof}

def main():
    A={str(q):anchor(q) for q in (2,3,4,5)}
    out={'pass':5142,'status':'THEOREM_ALL_Q_THETA_HALF_REGULAR_SUPPORT',
         'statement':'Every nonzero binary apartment-code support S induces degree 4(q-1) inside the intrinsic 8(q-1)-regular theta point graph, and every selected apartment has the same degree 4(q-1) to the complement.',
         'proof':'Each selected apartment is in 4(q-1) theta triples. Even parity forces exactly one selected partner and one unselected partner in each triple; uniqueness of the pair-check incidence prevents double counting.',
         'edge_boundary':'e(S)=2(q-1)|S| and |partial S|=4(q-1)|S|.',
         'distance_reformulation':'The minimum-distance problem is the minimum size of a nonempty theta-even support; every such support is an induced half-regular set. Thus a pure graph theorem excluding half-regular theta-even supports below q^4 would prove d_q=q^4.',
         'anchors':A,
         'boundary':'Half-regularity is necessary for a codeword support; an arbitrary half-regular vertex subset need not satisfy all theta checks.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
