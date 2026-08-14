#!/usr/bin/env python3
"""Pass5109 (bonkers): V4 and central-C3 sectors of the 12-dimensional root-coset incidence defect."""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5109_CURVATURE_KERNEL_V4.json'

def main():
    q=3;I=np.eye(4,dtype=int)%q
    def E(i,j):M=np.zeros((4,4),dtype=int);M[i,j]=1;return M
    X=[E(0,1)-E(3,2),E(1,3),E(0,3)+E(1,2),E(0,2)];Hroots=[[(I+t*Z)%q for t in range(q)] for Z in X]
    mm=lambda A,B:(A@B)%q;key=lambda A:tuple(map(int,A.flat));U={key(I):I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for h in Hroots:
            b=mm(a,h[1]);k=key(b)
            if k not in U:U[k]=b;Q.append(b)
    els=list(U.values());ei={key(a):i for i,a in enumerate(els)};cos=[];fam=[]
    for f,h in enumerate(Hroots):
        seen=set()
        for g in els:
            c=frozenset(ei[key(mm(g,z))] for z in h)
            if c not in seen:seen.add(c);cos.append(c);fam.append(f)
    H=np.zeros((81,108),dtype=int)
    for j,c in enumerate(cos):H[list(c),j]=1
    Kcols=sp.Matrix(H.T.tolist()).nullspace();assert len(Kcols)==12;K=sp.Matrix.hstack(*Kcols)
    _,pivrows=sp.Matrix(K.T).rref();pivrows=list(pivrows);Ks=K[pivrows,:];assert Ks.det()!=0

    # The center of U81 is the same C3 singled out by the H27 state torsor in Pass5105/BT865.
    center=[g for g in els if all(key(mm(g,h))==key(mm(h,g)) for h in els)];assert len(center)==3
    z=next(g for g in center if key(g)!=key(I));z2=mm(z,z)
    pz=tuple(ei[key(mm(z,g))] for g in els);invz=[0]*81
    for i,j in enumerate(pz):invz[j]=i
    KZ=K[invz,:];MZ=Ks.inv()*KZ[pivrows,:];assert K*MZ==KZ
    assert sp.factor(MZ.charpoly().as_expr())==(sp.Symbol('lambda')**2+sp.Symbol('lambda')+1)**6
    assert int(sp.trace(MZ))==-6 and (MZ-sp.eye(12)).rank()==12 and MZ**2+MZ+sp.eye(12)==sp.zeros(12)

    labels={'e':(1,1,1,1),'a':(1,1,2,2),'b':(1,2,1,2),'c':(1,2,2,1)};traces={};family_maps={};center_action={}
    cidx={c:j for j,c in enumerate(cos)}
    for name,vals in labels.items():
        D=np.diag(vals)%3;Di=np.array(sp.Matrix(D.tolist()).inv_mod(3).tolist(),dtype=int)%3
        p=tuple(ei[key(mm(mm(D,g),Di))] for g in els);inv=[0]*81
        for i,j in enumerate(p):inv[j]=i
        KP=K[inv,:];M=Ks.inv()*KP[pivrows,:];assert K*M==KP;traces[name]=int(sp.trace(M))
        maps={f:set() for f in range(4)}
        for j,c0 in enumerate(cos):
            im=frozenset(p[i] for i in c0);jj=cidx[im];maps[fam[j]].add(fam[jj])
        assert all(maps[f]=={f} for f in range(4));family_maps[name]=[f for f in range(4)]
        zc=mm(mm(D,z),Di)
        if key(zc)==key(z):center_action[name]='fix'
        elif key(zc)==key(z2):center_action[name]='invert'
        else:raise AssertionError('V4 failed to normalize center')
    assert traces=={'e':12,'a':0,'b':-4,'c':0}
    assert center_action=={'e':'fix','a':'invert','b':'fix','c':'invert'}
    # V4 irreducible multiplicities; each nontrivial character is +1 on exactly one of a,b,c.
    mult={
      'trivial':(traces['e']+traces['a']+traces['b']+traces['c'])//4,
      'kernel_ea':(traces['e']+traces['a']-traces['b']-traces['c'])//4,
      'kernel_eb':(traces['e']-traces['a']+traces['b']-traces['c'])//4,
      'kernel_ec':(traces['e']-traces['a']-traces['b']+traces['c'])//4,
    }
    assert sorted(mult.values())==[2,2,4,4] and sum(mult.values())==12
    out={'pass':5109,'status':'THEOREM_CURVATURE_KERNEL_V4_AND_CENTER_PHASE_SECTORS','defect_space':'ker(H^T) over Q','dimension':12,
         'canonical_diagonal_V4':labels,'character_traces':traces,'irreducible_multiplicities':mult,'sorted_sector_dimensions':[4,4,2,2],
         'root_parallel_classes':4,'V4_fixes_each_root_family_setwise':True,
         'central_C3':{'order':3,'generator_trace_on_defect':-6,'minimal_polynomial':'x^2+x+1','characteristic_polynomial':'(x^2+x+1)^6','fixed_dimension':0,'complex_split':'omega^6 + omega^2^6','V4_conjugation':center_action},
         'interpretation':'The free 12-dimensional incidence defect is phase-pure with respect to Z(U81)=Z(H27): it has no center-trivial vectors and splits over C as six omega plus six omega^2 directions. The root-normalizing V4 simultaneously resolves the rational defect as 4+4+2+2; two V4 involutions invert the center and exchange the conjugate phase sectors.',
         'boundary':'Exact rational/complex representation data for an incidence-kernel defect. The central C3 is the algebraic H27 triality axis from BT865/Pass5105, but no particle-family or hardware channel is inferred.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
