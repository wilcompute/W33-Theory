#!/usr/bin/env python3
"""Pass 4585 (outside box) -- 135 singular classes collapse to 45 canonical support-lines.

Each singular protected class has a 12-apartment fiber whose union is 16 W33
lines.  Surprisingly only 45 distinct 16-line supports occur, each shared by
three singular classes.  Those three sum to zero in V8 and are pairwise polar-
orthogonal, hence form a totally singular projective line.  The support
stabilizer has order 576 and cycles the three points as C3; the kernel has order
192, the singular-point stabilizer from Pass 4581.
"""
from __future__ import annotations
import json
from collections import defaultdict,Counter
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,build_line_perm,transvection_matrix
from w33_pass4581_apartment_fiber_equivariance import perm_group,pmask
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4585_FORTYFIVE_SINGULAR_SUPPORT_LINES.json'

def rbasis(vecs):
    piv={}
    for x in map(int,vecs):
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return list(piv.values())
def span(B):
    S=[0]
    for b in B:S += [x^b for x in list(S)]
    return S

def main()->int:
    pts,pidx,lines,lidx,_,A,_,aps,_=build_geometry();A=np.asarray(A,dtype=np.uint8);j=(1<<40)-1
    cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(A[:,c]):m|=1<<int(r)
        cols.append(m)
    edges=[(i,k) for i in range(40) for k in range(i+1,40) if A[i,k]]
    B9=rbasis([cols[i]^cols[k] for i,k in edges]);V=set(span(B9));assert len(V)==512 and j in V
    rep=lambda x:min(int(x),int(x)^j)
    q=lambda x:(rep(x).bit_count()//4)&1
    polar=lambda x,y:q(x)^q(y)^q(rep(x)^rep(y))
    fibers=defaultdict(list)
    for ap in aps:
        x=0
        for i in ap:x^=cols[int(i)]
        fibers[rep(x)].append(tuple(map(int,ap)))
    assert len(fibers)==135 and all(q(s)==0 for s in fibers)
    support_to_s=defaultdict(list)
    for s,F in fibers.items():
        U=frozenset().union(*(set(ap) for ap in F));assert len(U)==16
        support_to_s[U].append(s)
    assert len(support_to_s)==45 and Counter(map(len,support_to_s.values()))==Counter({3:45})
    for U,S in support_to_s.items():
        assert all(polar(a,b)==0 for a in S for b in S if a!=b)
        assert rep(S[0]^S[1])==rep(S[2]) and rep(S[0]^S[1]^S[2])==0
    # Exact group action on the 45 supports.
    cand=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    gens=[];G={tuple(range(40))}
    for g in cand:
        if g in G:continue
        gens.append(g);G=perm_group(gens)
        if len(G)==25920:break
    assert len(G)==25920
    U0=min(support_to_s,key=lambda U:tuple(sorted(U)));S0=sorted(support_to_s[U0]);sidx={s:i for i,s in enumerate(S0)}
    stab=[g for g in G if frozenset(g[i] for i in U0)==U0];assert len(stab)==576
    acts=set()
    for g in stab:
        p=[]
        for s in S0:
            im=rep(pmask(s,g));assert im in sidx;p.append(sidx[im])
        acts.add(tuple(p))
    assert acts=={(0,1,2),(1,2,0),(2,0,1)}
    assert len(stab)//len(acts)==192
    orbit={frozenset(g[i] for i in U0) for g in G};assert len(orbit)==45 and orbit==set(support_to_s)
    out={'pass':4585,'support_quotient':{'singular_classes':135,'distinct_16_line_supports':45,'singular_classes_per_support':3,
      'triple_geometry':'three pairwise-orthogonal singular points summing to zero; a totally singular projective line'},
      'group':{'PSp_order':25920,'support_orbit':45,'support_stabilizer_order':576,'action_on_three_points':'C3','kernel_order':192,'kernel_equals_singular_stabilizer_order':True},
      'theorem':'The apartment singular shell canonically fibers 135 -> 45 by common 16-line support; each fiber is a totally singular O+(8,2) line and the resulting 45-set is the PSp orbit with stabilizer 576.',
      'boundary':'The 45-set is constructed intrinsically here; identifying it with any pre-existing 45-object E6/center-quad carrier still requires an explicit action intertwiner.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
