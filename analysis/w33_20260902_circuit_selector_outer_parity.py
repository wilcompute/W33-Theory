#!/usr/bin/env python3
"""Resolve every circuit216->1080 Steinberg image line against PGSp outer parity.

The target St81^3 multiplicity algebra has now been proved to carry the global
outer involution J=diag(1,1,-1).  The circuit216 permutation carrier contains a
single St81, so every nonzero equivariant orbital map into the 1080 obstruction
carrier has an 81-dimensional image corresponding to one projective line in
the three-dimensional target multiplicity space.

This script reconstructs the complete circuit->obstruction Hom orbital basis,
projects each self-Gram A_i^T A_i into St81^3, expands it in exact M3 matrix
units, extracts its rank-one multiplicity line, and classifies that line under
J as:
  OUTER_EVEN  -- contained in the +1 plane,
  OUTER_ODD   -- the -1 line,
  MIXED       -- not invariant as a line under the outer involution.

The result determines whether any geometrically primitive circuit incidence
relation canonically selects the odd channel, the even plane, or a mixed line.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np
import sympy as sp

import w33_20260829_216_clifford_torsor_nogo as base
import w33_20260901_packet48_bt796_crossid as shell
from w33_20260901_steinberg_frame_common import build as build_frame
from w33_20260831_c5_wedderburn_kernel import mulvec
from w33_20260902_building_bt796_path_algebra import make_matrix_units

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260902_CIRCUIT_SELECTOR_OUTER_PARITY.json'


def comp(p,q): return tuple(p[q[i]] for i in range(len(q)))
def paired_closure(A,B,n,m):
    I=(tuple(range(n)),tuple(range(m))); G={I}; Q=deque([I])
    while Q:
        a,b=Q.popleft()
        for ga,gb in zip(A,B):
            z=(comp(ga,a),comp(gb,b))
            if z not in G:G.add(z);Q.append(z)
    assert len(G)==25920
    return list(G)


def main():
    F=build_frame(); D=shell.build(); acts,rel,T,E=F['acts'],F['rel'],F['T'],F['E']
    frame=list(F['frame']); units,_conn=make_matrix_units(frame,E,T,rel,F['reps'])
    order=[(i,j) for i in range(3) for j in range(3)]
    B=sp.Matrix.hstack(*[units[k] for k in order]); assert B.rank()==9
    J=sp.diag(1,1,-1)

    pts,idx,lines,N=base.geometry(); supports,masks=base.supports_from_N(N); assert supports==D['supports']
    circuits=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C:w^=masks[i]
        if w==0:circuits.append(C)
    assert len(circuits)==216
    cidx={C:i for i,C in enumerate(circuits)}
    circuit_gens=[tuple(cidx[tuple(sorted(p45[x] for x in C))] for C in circuits) for p45 in D['g45']]
    G=paired_closure(circuit_gens,acts,216,1080)
    H=[(gc,gt) for gc,gt in G if gc[0]==0]; assert len(H)==120
    unseen=set(range(1080)); orbits=[]
    while unseen:
        x=min(unseen); O={gt[x] for _gc,gt in H}; unseen-=O; orbits.append(sorted(O))
    orbits.sort(key=lambda O:(len(O),O[0]))
    tr=[None]*216
    for gc,gt in G:
        c=gc[0]
        if tr[c] is None:tr[c]=gt
    propagated=[]
    for O in orbits:
        propagated.append([frozenset(tr[c][x] for x in O) for c in range(216)])

    def target_cross(i,j):
        row=np.zeros(1080,dtype=np.int64)
        for c in range(216):
            if 0 in propagated[i][c]:
                for y in propagated[j][c]:row[y]+=1
        oval=[None]*59
        for y,v in enumerate(row.tolist()):
            r=int(rel[0,y])
            if oval[r] is None:oval[r]=v
            else:assert oval[r]==v
        q=sp.Matrix(oval)
        return mulvec(E,mulvec(q,E,T),T)

    records=[]; counts={'OUTER_EVEN':0,'OUTER_ODD':0,'MIXED':0,'ZERO':0}
    representative={}
    for i,O in enumerate(orbits):
        X=target_cross(i,i)
        if X==sp.zeros(59,1):
            counts['ZERO']+=1; records.append({'orbit':i,'targetOrbitSize':len(O),'reading':'ZERO'}); continue
        sol,_=B.gauss_jordan_solve(X); M=sp.Matrix(3,3,[sp.factor(sol[q]) for q in range(9)])
        r=M.rank()
        # Nonzero source Steinberg has multiplicity one, hence projected self-Gram
        # is rank one on multiplicity space.
        assert r==1
        v=next(M[:,c] for c in range(3) if M[:,c]!=sp.zeros(3,1))
        # primitive projective normalization
        q=next(x for x in v if x!=0); v=sp.simplify(v/q)
        Jv=J*v
        if Jv==v:reading='OUTER_EVEN'
        elif Jv==-v:reading='OUTER_ODD'
        else:reading='MIXED'
        counts[reading]+=1; representative.setdefault(reading,i)
        records.append({'orbit':i,'targetOrbitSize':len(O),'reading':reading,
                        'multiplicityLine':[str(sp.factor(x)) for x in v],
                        'selfGramM3':[[str(sp.factor(M[a,b])) for b in range(3)] for a in range(3)]})

    # Span dimensions of the actual projective line vectors by parity class.
    def span_of(reading):
        V=[]
        for r in records:
            if r.get('reading')==reading:V.append(sp.Matrix([sp.Rational(x) for x in r['multiplicityLine']]))
        return 0 if not V else sp.Matrix.hstack(*V).rank()
    spans={k:span_of(k) for k in ('OUTER_EVEN','OUTER_ODD','MIXED')}

    out={'schema':'w33.20260902.circuit-selector-outer-parity.v1','status':'PASS',
         'sourceCarrier':216,'sourceSteinbergMultiplicity':1,'targetSteinbergMultiplicity':3,
         'outerConjugatorJ':[['1','0','0'],['0','1','0'],['0','0','-1']],
         'homOrbitalCount':len(orbits),'classificationCounts':counts,
         'representativeOrbitByClass':representative,'lineSpanDimensions':spans,
         'orbitalMaps':records,
         'theorem':('Every nonzero circuit216-to-obstruction orbital incidence map determines an exact projective line in the St81 multiplicity-three space. Relative to the global PGSp outer grading J=diag(1,1,-1), the certificate classifies each primitive incidence line as outer-even, outer-odd, or mixed and records the exact rational line coordinates.'),
         'boundary':('An outer-even/odd multiplicity line is a finite representation-theoretic channel. It is not by itself a particle generation, chirality eigenstate, or physical propagation mode.')}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','counts':counts,'spans':spans,'reps':representative},sort_keys=True))

if __name__=='__main__':main()
