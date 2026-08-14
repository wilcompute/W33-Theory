#!/usr/bin/env python3
"""Pass5141 (bonkers): exact word-metric shells of the four-root U(q) Cayley carrier.

The canonical positive-root factorization gives diameter at most four.  We BFS
the exact Cayley graph for q=2,3,4,5,7,11,13 and expose a striking odd-prime
q>=5 polynomial shell law.  The anchors are theorem-level computations; the
uniform polynomial extrapolation is explicitly left conjectural here.
"""
from __future__ import annotations
import json
from collections import Counter,deque
from pathlib import Path
from analysis.w33_pass5129_allq_intrinsic_unipotent_controller import roots,mm,I4
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5141_ROOT_CAYLEY_METRIC_GROWTH.json'

def profile(q):
    U,H,F=roots(q);idx={g:i for i,g in enumerate(U)};e=idx[I4()]
    conn=[z for h in H for z in h if z!=I4()]
    dist=[-1]*len(U);dist[e]=0;Q=deque([e])
    while Q:
        u=Q.popleft();g=U[u]
        for h in conn:
            v=idx[mm(g,h,F)]
            if dist[v]<0:dist[v]=dist[u]+1;Q.append(v)
    C=Counter(dist);assert -1 not in C and max(C)<=4
    return {'q':q,'vertices':q**4,'degree':4*(q-1),'diameter':max(C),'shells':{str(k):C[k] for k in sorted(C)}}

def odd_formula(q):
    return {0:1,1:4*(q-1),2:8*(q-1)**2,3:(q-1)**2*(10*q-21),4:(q-1)**2*(q-4)**2}

def main():
    qs=(2,3,4,5,7,11,13);A={str(q):profile(q) for q in qs}
    for q in (5,7,11,13):
        got={int(k):v for k,v in A[str(q)]['shells'].items()};assert got==odd_formula(q)
    out={'pass':5141,'status':'EXACT_CAYLEY_METRIC_ANCHORS_WITH_ODD_Q_POLYNOMIAL_FRONTIER',
      'all_q_theorem':'The root-direction Cayley graph has diameter at most 4 because every U(q) element has the canonical four-positive-root factorization.',
      'anchors':A,
      'odd_prime_q_ge5_anchor_formula':{'d0':'1','d1':'4(q-1)','d2':'8(q-1)^2','d3':'(q-1)^2(10q-21)','d4':'(q-1)^2(q-4)^2'},
      'formula_checks':'Exact at q=5,7,11,13; the four shell polynomials sum identically to q^4.',
      'small_field_exceptions':'q=3 has diameter 3 and moves the would-be four distance-4 states into distance 3; q=2,4 have separate characteristic-two compression profiles.',
      'connection':'The metric counts the minimum number of root-direction chart moves needed to reach a controller state from identity, complementing Pass5137 spectrum and Pass5138 coordinate compiler.',
      'boundary':'The displayed q>=5 odd polynomial shell law is a four-anchor conjectural family until a symbolic word-factorization count is supplied; only the BFS anchors and diameter<=4 statement are promoted as theorems.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
