#!/usr/bin/env python3
"""Pass9289-9296: the four Leech sheet kernels are the sl2 Veronese conic.

Pass7957-7964 proved that the 144 mixed order-9 Leech Lagrangians form three
lifts of 48 projected Hesse lines, with sheet kernel C3^3 identified additively
with sl2(F3).  It found four order-9 kernel hyperplanes, 12 lines each, whose
dual normals form a projective frame, but did not identify that frame.

This pass identifies it exactly.  If a 36-component is labelled by the first
projective direction d=(x:y) in PG(1,3), then the fibre kernel is

    ker ell_d,   ell_d(X) = det(d, X d)

for X=[[a,b],[c,-a]] in sl2(F3).  In (a,b,c) coordinates the dual normal is
[xy:-y^2:x^2], the quadratic Veronese conic PG(1,3)->PG(2,3).
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from analysis.w33_pass7957_7964_leech_lagrangian_sheet_controller import (
    E, idx, lagrangians, proj, trans, canon,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9289_9296_LEECH_SL2_VERONESE_SHEET_GEOMETRY.json'
I2=np.eye(2,dtype=int)


def qdir(S):
    non=[u for u in S if (u[0],u[1])!=(0,0)]
    assert len(non)==3
    d=canon((non[0][0],non[0][1]))
    assert all(canon((u[0],u[1]))==d for u in non)
    return d


def normal(K):
    out=set()
    for n in itertools.product(range(3),repeat=3):
        if n==(0,0,0):continue
        if all(sum(n[i]*x[i] for i in range(3))%3==0 for x in K):out.add(canon(n))
    assert len(out)==1
    return next(iter(out))


def main()->int:
    L,mixed,_elem=lagrangians();li={H:i for i,H in enumerate(L)}
    mixidx=[i for i,H in enumerate(L) if H in mixed]
    fibres=defaultdict(list)
    for i in mixidx:fibres[proj(L[i])].append(i)
    assert len(fibres)==48 and set(map(len,fibres.values()))=={3}

    # Principal-congruence kernel X=(a b; c -a) in sl2(F3).
    Kacts=[]
    for a,b,c in itertools.product(range(3),repeat=3):
        X=np.array([[a,b],[c,(-a)%3]],dtype=int)
        A=(I2+3*X)%9;p=trans(A,I2)
        q=tuple(li[frozenset(E[p[idx[x]]] for x in H)] for H in L)
        Kacts.append(((a,b,c),q))
    assert len(Kacts)==27

    d_to_norm=defaultdict(set);d_to_kernel=defaultdict(set);normal_hist=Counter()
    for S,F0 in fibres.items():
        F=list(F0);ker=[]
        for coord,q in Kacts:
            if tuple(F.index(q[i]) for i in F)==(0,1,2):ker.append(coord)
        assert len(ker)==9
        n=normal(ker);d=qdir(S)
        d_to_norm[d].add(n);d_to_kernel[d].add(frozenset(ker));normal_hist[n]+=1
    assert len(d_to_norm)==4
    assert all(len(v)==1 for v in d_to_norm.values())
    assert all(len(v)==1 for v in d_to_kernel.values())
    assert set(normal_hist.values())=={12}

    # Exact formula ell_d(X)=det(d,Xd)=a*x*y-b*y^2+c*x^2.
    formula={}
    for d,NS in sorted(d_to_norm.items()):
        x,y=d;n=next(iter(NS))
        raw=(x*y%3,(-y*y)%3,x*x%3)
        assert canon(raw)==n
        K=next(iter(d_to_kernel[d]))
        expected=frozenset((a,b,c) for a,b,c in itertools.product(range(3),repeat=3)
                           if (a*x*y-b*y*y+c*x*x)%3==0)
        assert K==expected and len(expected)==9
        # Equivalent infinitesimal projective-stabilizer condition: Xd || d.
        for a,b,c in itertools.product(range(3),repeat=3):
            X=np.array([[a,b],[c,(-a)%3]],dtype=int);v=np.array([x,y],dtype=int)
            w=X@v%3;det=(x*int(w[1])-y*int(w[0]))%3
            assert det==(a*x*y-b*y*y+c*x*x)%3
            assert ((a,b,c) in K)==(det==0)
        formula[str(d)]={'normal':list(n),'functional':f'{x}*{y}*a - {y}^2*b + {x}^2*c'}

    # Fixed projective coordinate change from the standard Veronese
    # [x^2:xy:y^2] to the observed normals [xy:-y^2:x^2].
    P=np.array([[0,1,0],[0,0,2],[1,0,0]],dtype=int)
    assert round(np.linalg.det(P))%3!=0
    for d,NS in d_to_norm.items():
        x,y=d;v=np.array([x*x,x*y,y*y],dtype=int)%3
        assert canon(tuple(P@v%3))==next(iter(NS))

    out={'schema':'w33.pass9289_9296.leech_sl2_veronese_sheet_geometry.v1','status':'PASS','passes':'9289-9296',
      'sheet_kernel':'C3^3 = sl2(F3) additively','projected_Hesse_lines':48,'three_sheet_fibres':48,
      'component_directions':'PG(1,3), four points, 12 Hesse lines per direction',
      'kernel_theorem':'For component direction d=(x:y), the order-9 fibre-kernel hyperplane is ker ell_d where ell_d(X)=det(d,Xd) for X=[[a,b],[c,-a]].',
      'dual_normal_formula':'[x*y : -y^2 : x^2] in P(sl2(F3)^*)',
      'veronese':'The four dual normals are the quadratic Veronese conic PG(1,3)->PG(2,3), projectively equivalent to [x^2:xy:y^2].',
      'coordinate_change_from_standard_veronese':P.tolist(),
      'direction_data':formula,
      'representation_meaning':'ker ell_d consists exactly of infinitesimal sl2 transformations that preserve the projective direction d.',
      'theorem':'The four local central-C3 sheet systems are restrictions of one canonical sl2(F3) congruence geometry: their kernel hyperplanes are indexed by PG(1,3), and the dual hyperplanes trace the Veronese conic. This identifies the previously unnamed projective frame from Pass7957.',
      'claim_boundary':'Exact finite linked-module representation theorem; no continuum or physical gauge-field claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','normals':4,'lines_per_normal':12,'geometry':'Veronese conic'}));return 0
if __name__=='__main__':raise SystemExit(main())
