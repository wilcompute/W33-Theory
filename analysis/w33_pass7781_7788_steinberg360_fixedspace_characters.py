#!/usr/bin/env python3
from __future__ import annotations
import json, itertools
from collections import deque,Counter
from pathlib import Path
import numpy as np, sys
from sympy import Matrix
from sympy.combinatorics import Permutation,PermutationGroup
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
from analysis.w33_pass7509_7516_steinberg_global_intertwiner import build_T
OUT=ROOT/'data/PART_W33_PASS7781_7788_STEINBERG360_FIXEDSPACE_CHARACTERS.json'
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
    z=[0]*len(p)
    for i,j in enumerate(p):z[j]=i
    return tuple(z)
def schreier_stabilizer(ag,leaves):
    li={L:i for i,L in enumerate(leaves)};e=tuple(range(1120));tr=[None]*len(leaves);tr[0]=e;dq=deque([0])
    while dq:
        i=dq.popleft();X=leaves[i]
        for g in ag:
            Y=frozenset(g[a] for a in X);j=li[Y]
            if tr[j] is None:tr[j]=comp(g,tr[i]);dq.append(j)
    S=[];seen=set()
    for i,X in enumerate(leaves):
        for g in ag:
            Y=frozenset(g[a] for a in X);j=li[Y];h=comp(inv(tr[j]),comp(g,tr[i]))
            if h!=e and h not in seen:seen.add(h);S.append(h)
    return S
def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();sch=schreier_stabilizer(ag,leaves)
    R2,A22,J2,base2,bl,AO,lab,edges,L,P,T,maps=build_T();assert (R,A2,base)==(R2,A22,base2)
    D={}
    for j in np.flatnonzero(np.any(T!=0,axis=0)):D.setdefault(tuple(int(x) for x in T[:,j]),[]).append(int(j))
    fibres=[frozenset(v) for v in D.values()];fi={F:i for i,F in enumerate(fibres)}
    induced=[]
    for h in sch:induced.append(tuple(fi[frozenset(h[x] for x in F)] for F in fibres))
    hs=[];ps=[];G=PermutationGroup([Permutation(list(range(360)))])
    for h,p in zip(sch,induced):
        H=PermutationGroup([Permutation(list(x)) for x in ps+[p]]);o=int(H.order())
        if o>int(G.order()):hs.append(h);ps.append(p);G=H
        if o==51840:break
    assert int(G.order())==51840 and len(ps)==5
    H360=G.stabilizer(0);assert int(H360.order())==144
    G1120=PermutationGroup([Permutation(list(h)) for h in hs]);assert int(G1120.order())==155520
    F0=fibres[0];els=[g for g in G1120.generate_schreier_sims() if frozenset(int(g(x)) for x in F0)==F0]
    Hlift=PermutationGroup(els);assert int(Hlift.order())==432
    bpos={a:i for i,a in enumerate(bl)};pg=[]
    for g in Hlift.generators:pg.append(tuple(bpos[int(g(a))] for a in bl))
    H40=PermutationGroup([Permutation(list(p)) for p in pg]);assert int(H40.order())==144
    orbs=sorted([sorted(map(int,o)) for o in H40.orbits()],key=lambda x:(len(x),x[0]));sizes=[len(o) for o in orbs];assert sizes==[1,3,4,8,24]
    O=np.zeros((40,5),dtype=np.int64)
    for j,o in enumerate(orbs):O[o,j]=1
    A=AO[np.ix_(bl,bl)].astype(np.int64);I=np.eye(40,dtype=np.int64)
    N2=-(A-12*I)@(A+4*I);Nm4=(A-12*I)@(A-2*I)
    r1=1;r15=int(Matrix((Nm4@O).tolist()).rank());r24=int(Matrix((N2@O).tolist()).rank())
    assert (r1,r15,r24)==(1,2,2) and 1+r15+r24==5
    ds=H360;derived=[]
    for _ in range(6):
        derived.append(int(ds.order()));nd=ds.derived_subgroup()
        if int(nd.order())==int(ds.order()):break
        ds=nd
        if int(ds.order())==1:derived.append(1);break
    hist=Counter(int(g.order()) for g in H360.generate_schreier_sims())
    out={'schema':'w33.pass7781_7788.steinberg360_fixedspace_characters.v1','status':'PASS','passes':'7781-7788','effective_controller':'W(E6) on 360 Steinberg/D4 flags','controller_order':51840,'flag_stabilizer_order':144,'flag_stabilizer_W33_point_orbits':sizes,'flag_stabilizer_derived_orders':derived,'flag_stabilizer_center_order':int(H360.center().order()),'flag_stabilizer_element_orders':{str(k):v for k,v in sorted(hist.items())},'W33_point_module':'1 + V15 + V24','fixed_dimensions':{'1':r1,'V15':r15,'V24':r24},'frobenius_reciprocity':'For the transitive 360-set G/H, multiplicity of an irreducible V in C[G/H] equals dim(V^H). Hence the two copies of dimensions 15 and 24 are forced by the two-dimensional H-fixed spaces in the two nontrivial W33 point eigenspaces.','prior_art_boundary':'Pass7605-7612 already proved the full 360 decomposition 1+20+30+60+81+90+2*15+2*24. This pass adds the geometric fixed-space explanation of precisely the doubled 15 and 24, rather than reclaiming the decomposition.','theorem':'The multiplicity-two 15D and 24D sectors of the 360 Steinberg-vector permutation module are induced directly from the D4-flag stabilizer geometry on the base W33: its five point-orbits project with ranks 1,2,2 to the 1,15,24 W33 eigenspaces.','claim_boundary':'Exact finite representation theorem; no character-table naming beyond dimensions is required.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','H_orbits':sizes,'fixed':'1+2*15+2*24 explanation'}))
if __name__=='__main__':main()
