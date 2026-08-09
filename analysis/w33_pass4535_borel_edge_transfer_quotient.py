#!/usr/bin/env python3
"""Pass 4535 (outside the box) -- eight-state Borel transfer quotient on protected edges.

Take the 240 dual-W33 edges from Pass 4513 and form their line graph: two
protected edges are adjacent when they share a W33 line endpoint.  The splitting
Borel has eight edge orbits (Pass 4532).  They form an equitable partition, so
the 240-state 22-regular edge graph compresses exactly to an 8x8 integer
transfer matrix.

The quotient has spectrum 22,12,12,6,-2,-2,-2,-2.  More strikingly, its set of
distinct eigenvalues {22,12,6,-2} is the complete distinct spectrum of the full
240-state line graph.  Thus the Borel quotient is spectrally complete at the
level of eigenvalue locations while compressing multiplicities.

No dynamical/physical transfer operator is inferred; this is an equitable graph
quotient.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import numpy as np

from w33_apartment_section_core import build_geometry, build_line_perm, perm_group, transvection_matrix

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4535_BOREL_EDGE_TRANSFER_QUOTIENT.json"


def rank_q(M):
    A = [[Fraction(int(x)) for x in row] for row in M]
    m = len(A); n = len(A[0]); r = 0
    for c in range(n):
        p = next((i for i in range(r,m) if A[i][c]), None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        z=A[r][c]; A[r]=[x/z for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]; A[i]=[a-z*b for a,b in zip(A[i],A[r])]
        r += 1
        if r==m: break
    return r


def main() -> int:
    pts,pidx,lines,lidx,_Ap,Astar,*_ = build_geometry()
    trans=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[]; G={tuple(range(40))}
    for g in trans:
        trial=perm_group(gens+[g],40)
        if len(trial)>len(G): gens.append(g);G=trial
        if len(G)==25920: break
    assert len(G)==25920
    pencils=[frozenset(i for i,L in enumerate(lines) if p in L) for p in range(40)]
    pi={S:i for i,S in enumerate(pencils)}
    def pim(g,p): return pi[frozenset(g[i] for i in pencils[p])]
    fp,fl=min((p,li) for li,L in enumerate(lines) for p in L)
    H={g for g in G if g[fl]==fl and pim(g,fp)==fp}
    assert len(H)==162

    edges=[(i,j) for i in range(40) for j in range(i+1,40) if Astar[i,j]]
    assert len(edges)==240
    edge_set=set(edges)
    rem=set(edges); orbits=[]
    while rem:
        e=min(rem); o={tuple(sorted((g[e[0]],g[e[1]]))) for g in H}
        orbits.append(sorted(o)); rem-=o
    orbits.sort(key=lambda o:(len(o),o[0]))
    assert [len(o) for o in orbits]==[3,3,9,9,27,27,81,81]
    oi={e:i for i,o in enumerate(orbits) for e in o}

    Q=np.zeros((8,8),dtype=np.int64)
    for i,o in enumerate(orbits):
        first=None
        for a,b in o:
            neigh=set()
            for x in range(40):
                if x!=b:
                    e=tuple(sorted((a,x)))
                    if e in edge_set and e!=(a,b): neigh.add(e)
                if x!=a:
                    e=tuple(sorted((b,x)))
                    if e in edge_set and e!=(a,b): neigh.add(e)
            assert len(neigh)==22
            row=[sum(1 for e in neigh if oi[e]==j) for j in range(8)]
            if first is None: first=row
            else: assert row==first
        Q[i]=first
    assert np.all(Q.sum(axis=1)==22)

    expected=np.array([
      [2,2,9,0,9,0,0,0],
      [2,2,0,0,18,0,0,0],
      [3,0,8,2,0,0,9,0],
      [0,0,2,2,0,0,18,0],
      [1,2,0,0,8,2,3,6],
      [0,0,0,0,2,2,6,12],
      [0,0,1,2,1,2,10,6],
      [0,0,0,0,2,4,6,10],
    ],dtype=np.int64)
    assert np.array_equal(Q,expected)

    sizes=np.array([len(o) for o in orbits],dtype=np.int64)
    assert all(sizes[i]*Q[i,j]==sizes[j]*Q[j,i] for i in range(8) for j in range(8))
    eig_mult={}
    I=np.eye(8,dtype=np.int64)
    for lam in (22,12,6,-2):
        eig_mult[str(lam)]=8-rank_q(Q-lam*I)
    assert eig_mult=={"22":1,"12":2,"6":1,"-2":4}
    assert sum(eig_mult.values())==8

    # Full 240-state line graph.  Exact polynomial annihilator verifies no
    # eigenvalues outside the four quotient values.
    L=np.zeros((240,240),dtype=np.int64)
    for i,(a,b) in enumerate(edges):
        for j in range(i+1,240):
            c,d=edges[j]
            if len({a,b,c,d})<4: L[i,j]=L[j,i]=1
    assert np.all(L.sum(axis=1)==22)
    I240=np.eye(240,dtype=np.int64)
    P=I240.copy()
    for lam in (22,12,6,-2):
        P=P@(L-lam*I240)
    assert not P.any()

    out={
      "pass":4535,
      "full_edge_graph":{"vertices":240,"degree":22,"construction":"line graph of dual-W33","distinct_spectrum":[22,12,6,-2]},
      "Borel_orbit_sizes":sizes.tolist(),
      "equitable_quotient_matrix":Q.tolist(),
      "row_sum":22,
      "detailed_balance":"|Oi| Qij = |Oj| Qji for every orbit pair",
      "quotient_eigenvalue_multiplicities":eig_mult,
      "quotient_characteristic_polynomial":"(x-22)(x-12)^2(x-6)(x+2)^4",
      "spectral_completeness":"The 8-state quotient contains every distinct eigenvalue of the full 240-state edge line graph.",
      "theorem":"The Borel eight-orbit partition is equitable and gives an exact 8x8 transfer quotient whose four distinct eigenvalues equal the complete distinct spectrum of the 240-vertex protected-edge line graph.",
      "boundary":"An equitable graph quotient is not by itself a physical Hamiltonian, Markov transition matrix, decoder, or measured transfer function."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True));return 0


if __name__=="__main__": raise SystemExit(main())
