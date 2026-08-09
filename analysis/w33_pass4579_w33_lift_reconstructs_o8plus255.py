#!/usr/bin/env python3
"""Pass 4579 -- reconstruct the full 255-state O+(8,2) geometry from W33 lifts.

The input is only the exact W33 line graph and its apartment/edge lifts.  The
135 apartment classes and 120 opposite-edge classes are shown to exhaust the
255 nonzero classes of V8=V9/<j>.  The quadratic q=wt/4 mod 2 and its polar form
are reconstructed from those protected representatives; no pre-existing V8
coordinate model is imported.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4579_W33_LIFT_O8PLUS255.json'

def rank_basis_int(vecs):
    piv={}
    for x in map(int,vecs):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return list(piv.values())

def span(basis):
    out=[0]
    for b in basis:out += [x^b for x in list(out)]
    return out

def main()->int:
    vals=build_geometry();A=np.asarray(vals[5],dtype=np.uint8);aps=vals[7]
    n=40;j=(1<<n)-1
    cols=[]
    for c in range(n):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(n) for k in range(i+1,n) if A[i,k]]
    edge_vec=[cols[i]^cols[k] for i,k in edges]
    B9=rank_basis_int(edge_vec);assert len(B9)==9
    V9=set(span(B9));assert len(V9)==512 and j in V9
    reps={min(x,x^j) for x in V9};assert len(reps)==256
    def rep(x):return min(int(x),int(x)^j)
    def q(x):return (rep(x).bit_count()//4)&1
    def polar(x,y):return q(x)^q(y)^q(rep(x)^rep(y))
    nonzero=sorted(reps-{0});sing=[x for x in nonzero if q(x)==0];anis=[x for x in nonzero if q(x)==1]
    assert (len(sing),len(anis))==(135,120)

    apfib=defaultdict(list)
    for ap in aps:
        x=0
        for i in ap:x^=cols[int(i)]
        apfib[rep(x)].append(tuple(map(int,ap)))
    assert set(apfib)==set(sing) and Counter(map(len,apfib.values()))==Counter({12:135})
    efib=defaultdict(list)
    for e,x in zip(edges,edge_vec):efib[rep(x)].append(e)
    assert set(efib)==set(anis) and Counter(map(len,efib.values()))==Counter({2:120})

    ss=Counter(sum(polar(x,y)==0 for y in sing if y!=x) for x in sing)
    aa=Counter(sum(polar(x,y)==0 for y in anis if y!=x) for x in anis)
    sa=Counter(sum(polar(x,y)==0 for y in anis) for x in sing)
    ass=Counter(sum(polar(x,y)==0 for y in sing) for x in anis)
    assert ss==Counter({70:135}) and aa==Counter({63:120})
    assert sa==Counter({56:135}) and ass==Counter({63:120})

    # Every two distinct nonzero vectors determine a projective F2-line {x,y,x+y}.
    triples=set();types=Counter()
    for i,x in enumerate(nonzero):
        for y in nonzero[i+1:]:
            z=rep(x^y);assert z not in (0,x,y)
            T=tuple(sorted((x,y,z)))
            triples.add(T)
    assert len(triples)==10795
    for T in triples:types[sum(q(x)==0 for x in T)]+=1
    assert types==Counter({0:5440,1:3780,3:1575})

    out={
      'pass':4579,
      'protected_quotient':{'V9_dimension':9,'fixed_vector':'j=all ones','V8_classes_including_zero':256,'nonzero_classes':255},
      'lift_partition':{'singular_from_apartments':135,'apartments':1620,'apartment_fiber':12,
                        'anisotropic_from_edges':120,'edges':240,'edge_fiber':2,'exhausts_nonzero_V8':True},
      'quadratic':{'definition':'q([x])=wt(x)/4 mod 2','polar':'B(x,y)=q(x+y)+q(x)+q(y)','type':'plus'},
      'orthogonality':{'singular_to_singular_degree':70,'singular_to_anisotropic_degree':56,
                       'anisotropic_to_singular_degree':63,'anisotropic_to_anisotropic_degree':63,
                       'full_nonzero_orthogonal_degree_excluding_self':126},
      'projective_lines':{'total':10795,'three_singular':1575,'one_singular_two_anisotropic':3780,'three_anisotropic':5440},
      'theorem':'The W33 apartment and opposite-edge lifts alone reconstruct all 255 nonzero vectors, the plus-type quadratic, its polar form, and the complete singular/anisotropic incidence geometry of O+(8,2).',
      'boundary':'This is finite protected Hamming/quadratic geometry; it does not identify these 255 classes with physical states.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
