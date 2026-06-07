#!/usr/bin/env python3
"""BT523: Cl8 Fold Chain-Map Field Kernel Theorem.

Executes branch 2 from the latest next-step list.

BT520 proved the integer factorization
    F M = 4 R
where
    F : signed Xmin faces -> octahedron corner states     (240 x 320),
    M : quadrangles -> signed Xmin faces                  (320 x 1620),
    R : quadrangles -> octahedron corner states           (240 x 1620).

This script treats that as a chain-map-like field calculation and computes
ranks/kernels/cokernels over Q, F2, and F3.

The important arithmetic point:
  over Q and F3, 4 is invertible, so F M = 4R remains a nonzero refinement;
  over F2, 4=0, so the factorization becomes F M = 0, revealing an actual
  mod-2 chain condition.
"""
from __future__ import annotations

import itertools, json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import sympy as sp

P=3
Vec=tuple[int,int,int,int]

def canonical(v)->Vec:
    vv=tuple(int(x)%P for x in v)
    if vv==(0,0,0,0): raise ValueError('zero')
    for x in vv:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%P for y in vv)  # type: ignore[return-value]
    raise AssertionError

def omega(u:Vec,v:Vec)->int:
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def geom():
    pts=[]; seen=set()
    for raw in itertools.product(range(P),repeat=4):
        if raw==(0,0,0,0): continue
        c=canonical(raw)
        if c not in seen: seen.add(c); pts.append(c)
    pidx={p:i for i,p in enumerate(pts)}; A=np.zeros((40,40),dtype=int); edges=[]
    for i,j in itertools.combinations(range(40),2):
        if omega(pts[i],pts[j])==0: A[i,j]=A[j,i]=1; edges.append((i,j))
    lines=set()
    for i,j in edges:
        u,v=pts[i],pts[j]; line=set()
        for a,b in itertools.product(range(P),repeat=2):
            if a==0 and b==0: continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines); point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L: point_lines[p].append(li)
        for e in itertools.combinations(L,2): edge_to_line[tuple(sorted(e))]=li
    return A,point_lines,edge_to_line

def quads(A):
    qs=[]; seen=set()
    for a,b in itertools.combinations(range(40),2):
        if A[a,b]: continue
        common=[x for x in range(40) if A[a,x] and A[b,x]]
        for c,d in itertools.combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen: seen.add(cyc); qs.append(cyc)
    return qs

def local(p,Ls):
    Ls=sorted(Ls); verts=[]; faces=[]; v2f=defaultdict(list)
    for pair in itertools.combinations(Ls,2): verts.append((p,tuple(sorted(pair))))
    for L in Ls:
        others=[x for x in Ls if x!=L]
        star=[tuple(sorted((L,M))) for M in others]
        opp=[tuple(sorted(pair)) for pair in itertools.combinations(others,2)]
        fp=(p,L,1); fm=(p,L,-1); faces += [fp,fm]
        for v in star: v2f[(p,v)].append(fp)
        for v in opp: v2f[(p,v)].append(fm)
    return verts,faces,v2f

def rank_mod(mat:np.ndarray, p:int)->int:
    A=(mat.copy()%p).astype(int); m,n=A.shape; r=0; c=0
    while r<m and c<n:
        piv=None
        for i in range(r,m):
            if A[i,c]%p: piv=i; break
        if piv is None: c+=1; continue
        if piv!=r: A[[r,piv]]=A[[piv,r]]
        inv=pow(int(A[r,c]), -1, p)
        A[r]=(A[r]*inv)%p
        for i in range(m):
            if i!=r and A[i,c]%p:
                A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1; c+=1
    return r

def main()->dict:
    A,point_lines,edge_to_line=geom(); qs=quads(A)
    verts=[]; signed=[]; v2f={}
    for p in range(40):
        vs,fs,loc=local(p,point_lines[p]); verts+=vs; signed+=fs; v2f.update(loc)
    verts=sorted(verts); signed=sorted(signed); vi={v:i for i,v in enumerate(verts)}; si={f:i for i,f in enumerate(signed)}
    F=np.zeros((240,320),dtype=np.int8)
    for v,fs in v2f.items():
        for f in fs: F[vi[v],si[f]]=1
    R=np.zeros((240,1620),dtype=np.int8); M=np.zeros((320,1620),dtype=np.int8)
    for qi,cyc in enumerate(qs):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es)); R[vi[(p,lpair)],qi]=1
            for f in v2f[(p,lpair)]: M[si[f],qi]=1
    assert np.array_equal(F@M,4*R)

    fields={}
    for name,mod in [('Q',0),('F2',2),('F3',3)]:
        if mod==0:
            rF=int(sp.Matrix(F).rank()); rM=int(sp.Matrix(M).rank()); rR=int(sp.Matrix(R).rank()); rFM=int(sp.Matrix(F@M).rank())
        else:
            rF=rank_mod(F,mod); rM=rank_mod(M,mod); rR=rank_mod(R,mod); rFM=rank_mod(F@M,mod)
        fields[name]={
            'rank_F':rF,'ker_F':320-rF,'coker_F':240-rF,
            'rank_M':rM,'ker_M':1620-rM,'coker_M':320-rM,
            'rank_R':rR,'ker_R':1620-rR,'coker_R':240-rR,
            'rank_FM':rFM,
            'FM_zero': bool((mod==2 and rFM==0) or (mod!=2 and rFM==rR))
        }
    assert fields['Q']['rank_F']==160 and fields['Q']['rank_M']==160 and fields['Q']['rank_R']==240
    assert fields['F2']['rank_FM']==0
    assert fields['F3']['rank_FM']==fields['F3']['rank_R']

    results={
        'theorem':'BT523 Cl8 Fold Chain-Map Field Kernel Theorem',
        'integer_factorization':'F M = 4 R',
        'field_results':fields,
        'mod2_chain_condition':'over F2, 4=0 so F M=0; M maps quadrangles into ker(F)',
        'mod3_nonzero_refinement':'over F3, 4=1 so F M=R; signed lift refines the old corner map without collapse',
        'substrate_reading':{'F2':'true chain complex parity shadow','F3':'ternary W33 geometry stays active','ker_F_over_Q':160,'coker_M_over_Q':160,'coker_R_over_Q':0}
    }
    out=Path('data/PART_BT523_CL8_FOLD_CHAIN_MAP_FIELDS_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
