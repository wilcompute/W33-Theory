#!/usr/bin/env python3
"""Pass7605-7612: the 360 Steinberg vectors carry a rank-14 W(E6) orbital algebra.

The 11 raw Gram relations are not closed.  The actual leaf-controller orbitals
split three Gram classes and form a 14-dimensional (noncommutative) coherent
algebra.  Its 8-dimensional center determines the full multiplicity pattern of
the 360-point permutation module.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.combinatorics import Permutation,PermutationGroup
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from analysis import w33_pass7501_7564_common as E
from analysis.w33_pass7509_7516_steinberg_global_intertwiner import build_T
OUT=ROOT/'data/PART_W33_PASS7605_7612_STEINBERG360_ORBITAL_ALGEBRA.json'

def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def inv(p):
    z=[0]*len(p)
    for i,j in enumerate(p):z[j]=i
    return tuple(z)
def schreier_stabilizer(ag,leaves):
    li={L:i for i,L in enumerate(leaves)};idp=tuple(range(1120));tr=[None]*len(leaves);tr[0]=idp;dq=deque([0])
    while dq:
        i=dq.popleft();X=leaves[i]
        for g in ag:
            Y=frozenset(g[a] for a in X);j=li[Y]
            if tr[j] is None:tr[j]=comp(g,tr[i]);dq.append(j)
    S=[];seen=set()
    for i,X in enumerate(leaves):
        for g in ag:
            Y=frozenset(g[a] for a in X);j=li[Y];h=comp(inv(tr[j]),comp(g,tr[i]))
            if h!=idp and h not in seen:seen.add(h);S.append(h)
    return S
def invn(p):
    z=[0]*len(p)
    for i,j in enumerate(p):z[j]=i
    return tuple(z)
def pair_orbit(seed,gens,n):
    S={seed[0]*n+seed[1]};q=deque(S)
    while q:
        z=q.popleft();a,b=divmod(z,n)
        for g in gens:
            w=g[a]*n+g[b]
            if w not in S:S.add(w);q.append(w)
    return S

def main():
    R,A2,ag,J,base,leaves,lgens,parity=E.build();sch=schreier_stabilizer(ag,leaves)
    R2,A22,J2,base2,bl,AO,lab,edges,L,P,T,maps=build_T();assert R==R2 and A2==A22 and base==base2
    D={}
    for j in np.flatnonzero(np.any(T!=0,axis=0)):D.setdefault(tuple(int(x) for x in T[:,j]),[]).append(int(j))
    assert len(D)==360 and set(map(len,D.values()))=={3}
    vecs=list(D);fibres=[frozenset(D[v]) for v in vecs];fi={F:i for i,F in enumerate(fibres)};V=np.asarray(vecs,dtype=np.int64).T;Gram=V.T@V

    # The leaf stabilizer acts on the three-A2 fibres, hence on the 360 vectors.
    fgens=[]
    for h in sch:
        p=tuple(fi[frozenset(h[x] for x in F)] for F in fibres);fgens.append(p)
    FG=PermutationGroup([Permutation(list(p)) for p in fgens]);assert int(FG.order())==51840 and [len(o) for o in FG.orbits()]==[360]
    stab=FG.stabilizer(0);subs=sorted([sorted(map(int,o)) for o in stab.orbits()],key=lambda x:(len(x),x[0]));subdegrees=[len(o) for o in subs]
    assert subdegrees==[1,3,4,8,8,24,24,24,24,24,24,48,72,72]
    gram_by_suborbit=[dict(Counter(int(Gram[0,j]) for j in o)) for o in subs]

    # Reduce to five actual generators before taking ordered-pair orbits.
    chosen=[];cur=PermutationGroup([Permutation(list(range(360)))]);growth=[]
    for p in fgens:
        H=PermutationGroup([Permutation(list(x)) for x in chosen+[p]]);o=int(H.order())
        if o>int(cur.order()):chosen.append(p);cur=H;growth.append(o)
        if o==51840:break
    assert growth==[3,24,648,25920,51840]
    gens=chosen+[invn(p) for p in chosen];orbsets=[pair_orbit((0,o[0]),gens,360) for o in subs]
    assert sum(map(len,orbsets))==360*360
    mats=[]
    for S in orbsets:
        A=np.zeros((360,360),dtype=np.int8)
        for z in S:a,b=divmod(z,360);A[a,b]=1
        mats.append(A)
    tmap=[]
    for A in mats:tmap.append(next(j for j,B in enumerate(mats) if np.array_equal(A.T,B)))
    assert tmap==[0,1,2,3,4,5,7,6,8,10,9,11,12,13]

    # Verify coherent-algebra closure and build exact structure constants.
    reps=[divmod(next(iter(S)),360) for S in orbsets];pijk=np.zeros((14,14,14),dtype=np.int64)
    for i,A in enumerate(mats):
        for j,B in enumerate(mats):
            C=A.astype(np.int64)@B.astype(np.int64)
            for t,S in enumerate(orbsets):
                a,b=reps[t];v=int(C[a,b]);zz=np.fromiter(S,dtype=np.int64);aa=zz//360;bb=zz%360
                assert np.all(C[aa,bb]==v);pijk[i,j,t]=v

    # Center equations: sum_i c_i(A_i A_j-A_j A_i)=0.
    eq=[]
    for j in range(14):
        for t in range(14):eq.append([int(pijk[i,j,t]-pijk[j,i,t]) for i in range(14)])
    M=sp.Matrix(eq);ns=M.nullspace();assert len(ns)==8
    c=sp.zeros(14,1)
    for k,v in enumerate(ns):c+=(k+1)*v
    den=1
    for x in c:den=math.lcm(den,int(sp.denom(x)))
    ci=[int(x*den) for x in c];Z=sum(ci[i]*mats[i].astype(np.int64) for i in range(14));assert np.array_equal(Z,Z.T)
    w,Q=np.linalg.eigh(Z.astype(float));zspec=Counter(round(float(x),6) for x in w)
    expected={-67.0:90,-49.0:48,-39.0:81,-25.0:20,-13.0:60,113.0:30,257.0:30,2081.0:1};assert zspec==expected

    # The center has 8 primitive sectors. Since dim(commutant)=14, exactly two
    # sectors have multiplicity two.  The tetrahedral orbital A_1 resolves them.
    split={}
    for lam,n in expected.items():
        idx=np.where(np.isclose(w,lam,atol=1e-5))[0];q=Q[:,idx];B=q.T@(mats[1].astype(float)@q);es=Counter(round(float(x.real),6) for x in np.linalg.eigvals(B))
        if len(es)>1:split[str(int(lam))]=dict(es)
    assert split=={'-49':{-1.0:24,3.0:24},'113':{-1.0:15,3.0:15}}
    decomp={'1':1,'15':2,'20':1,'24':2,'30':1,'60':1,'81':1,'90':1};assert sum(int(d)*m for d,m in decomp.items())==360 and sum(m*m for m in decomp.values())==14

    rawgram=Counter(int(Gram[i,j]) for i in range(360) for j in range(i+1,360))
    out={'schema':'w33.pass7605_7612.steinberg360_orbital_algebra.v1','status':'PASS','passes':'7605-7612','vectors':360,'controller':'W(E6)','controller_order':51840,
      'raw_Gram_offdiagonal_counts':dict(sorted(rawgram.items())),'raw_Gram_relations_close':False,
      'orbital_rank':14,'subdegrees':subdegrees,'orbital_Gram_fingerprints':gram_by_suborbit,'transpose_orbitals':tmap,'algebra_commutative':False,'center_dimension':8,
      'generic_center_coefficients':ci,'generic_center_spectrum':{str(k):v for k,v in sorted(zspec.items())},'multiplicity_two_blocks_resolved_by_tetrahedral_relation':split,
      'permutation_module_decomposition':decomp,
      'decomposition_formula':'1 + 20 + 30 + 60 + 81 + 90 + 2*24 + 2*15 = 360',
      'theorem':'The 360 Steinberg vectors form one transitive W(E6) set of permutation rank 14. Their coherent orbital algebra has center dimension 8 and Wedderburn multiplicities 1,1,1,1,1,1,2,2, giving the exact module decomposition 1+20+30+60+81+90+2*24+2*15. The unique 81-dimensional constituent is the W33 Steinberg/H1 sector; the 24- and 15-dimensional sectors are precisely the two multiplicity-two blocks.',
      'claim_boundary':'Exact W(E6) permutation/coherent-algebra theorem. No physical particle interpretation is assigned.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','rank':14,'center':8,'decomposition':decomp}))
if __name__=='__main__':main()
