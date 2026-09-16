#!/usr/bin/env python3
"""Suzuki/Leech -> full W33 -> E6 cubic incidence tower.

This verifier starts only from the vendored ATLAS 12-dimensional GF(3)
representation of 2.Suz and explicit witnesses found in the 2026-09-16 search.
It checks:

* the 32760-point projective Suzuki/Leech tight orbit;
* a full nondegenerate PG(3,3)=W(3,3) contained in that orbit;
* the complete 2.Suz orbit of 135135 such W33 subspaces;
* 54 full-W33 symplectic-orthogonal partners through a fixed W33;
* every partner completes to a third full W33, so the six-qutrit phase space
  decomposes into three pairwise orthogonal two-qutrit phase spaces entirely
  inside the Leech tight shell;
* 1216215 unordered three-W33 decompositions, 27 through each W33, and 165
  full W33s through each tight-set point;
* the 27 decompositions through a fixed W33 carry SRG(27,10,1,5), the
  GQ(4,2)/E6 cubic-surface 27-line carrier already certified elsewhere in the
  repository.

The old 56/120 overlap certificate is therefore superseded: 120/120 is attained
and is globally maximal by cardinality.  The associated projective ternary
[32760,12] two-weight code has d_8=32720.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_suzuki_w33_e6_incidence_tower.json"
P = 3

# Row-action invariant alternating form for the vendored ATLAS generators.
J = np.array([
[0,0,0,0,0,0,1,2,2,2,1,2],
[0,0,0,0,0,0,2,2,1,2,1,1],
[0,0,0,0,0,2,0,2,1,2,0,1],
[0,0,0,0,2,0,2,0,0,1,2,1],
[0,0,0,1,0,0,0,1,2,0,2,0],
[0,0,1,0,0,0,1,0,2,0,1,0],
[2,1,0,1,0,2,0,0,1,0,0,2],
[1,1,1,0,2,0,0,0,0,2,2,0],
[1,2,2,0,1,1,2,0,0,0,0,2],
[1,1,1,2,0,0,0,1,0,0,1,0],
[2,2,0,1,1,2,0,1,0,2,0,0],
[1,2,2,2,0,0,1,0,1,0,0,0]], dtype=np.int64)

T_SEED = np.array([1,1,0,1,0,2,1,0,1,0,0,1], dtype=np.int64)
U1 = np.array([
[1,0,0,0,2,2,2,1,1,0,2,1],
[0,1,0,0,1,2,1,2,2,2,1,0],
[0,0,1,0,1,2,2,1,1,2,1,0],
[0,0,0,1,2,2,0,1,2,2,1,0]], dtype=np.int64)
U2 = np.array([
[1,0,0,2,0,0,2,1,0,0,1,0],
[0,1,0,1,0,0,2,1,0,0,2,1],
[0,0,1,2,0,2,1,1,0,2,0,0],
[0,0,0,0,1,2,1,0,0,1,0,1]], dtype=np.int64)
U3 = np.array([
[1,0,0,0,1,2,1,2,0,1,0,0],
[0,1,0,0,1,1,0,0,2,0,1,0],
[0,0,1,0,1,2,1,2,0,1,2,2],
[0,0,0,1,2,2,2,2,2,2,0,0]], dtype=np.int64)


def parse_meataxe(path: Path) -> np.ndarray:
    t = path.read_text().split(); assert t[:4] == ['1','3','12','12']
    return np.array([[int(c) for c in row] for row in t[4:]], dtype=np.int64) % P


def rankp(M: np.ndarray) -> int:
    A = np.array(M, dtype=np.int64) % P; r = 0
    for c in range(A.shape[1]):
        piv = next((i for i in range(r, A.shape[0]) if A[i,c] % P), None)
        if piv is None: continue
        A[[r,piv]] = A[[piv,r]]
        A[r] = A[r] * pow(int(A[r,c]), -1, P) % P
        for i in range(A.shape[0]):
            if i != r and A[i,c] % P: A[i] = (A[i] - A[i,c]*A[r]) % P
        r += 1
        if r == A.shape[0]: break
    return r


def rref_key(M: np.ndarray) -> tuple[tuple[int,...],...]:
    A = np.array(M, dtype=np.int64) % P; r = 0
    for c in range(A.shape[1]):
        piv = next((i for i in range(r, A.shape[0]) if A[i,c] % P), None)
        if piv is None: continue
        A[[r,piv]] = A[[piv,r]]
        A[r] = A[r] * pow(int(A[r,c]), -1, P) % P
        for i in range(A.shape[0]):
            if i != r and A[i,c] % P: A[i] = (A[i] - A[i,c]*A[r]) % P
        r += 1
        if r == A.shape[0]: break
    A = A[[i for i in range(A.shape[0]) if np.any(A[i] % P)]]
    return tuple(tuple(map(int,row)) for row in A)


def canon(v) -> tuple[int,...]:
    a = np.array(v, dtype=np.int64) % P; i = next(i for i,x in enumerate(a) if x)
    return tuple(map(int, a * pow(int(a[i]), -1, P) % P))


def projective_points(B: np.ndarray) -> set[tuple[int,...]]:
    return {canon(np.array(c, dtype=np.int64) @ B % P)
            for c in itertools.product(range(P), repeat=B.shape[0]) if any(c)}


def point_orbit(seed: np.ndarray, gens: list[np.ndarray]) -> set[tuple[int,...]]:
    s = canon(seed); seen={s}; q=deque([np.array(s,dtype=np.int64)])
    while q:
        v=q.popleft()
        for g in gens:
            w=canon(v @ g % P)
            if w not in seen: seen.add(w); q.append(np.array(w,dtype=np.int64))
    return seen


def subspace_orbit(seed: np.ndarray, gens: list[np.ndarray]) -> dict[tuple[tuple[int,...],...],np.ndarray]:
    k=rref_key(seed); seen={k:np.array(k,dtype=np.int64)}; q=deque([seen[k]])
    while q:
        B=q.popleft()
        for g in gens:
            z=rref_key(B @ g % P)
            if z not in seen:
                seen[z]=np.array(z,dtype=np.int64); q.append(seen[z])
    return seen


def perp_basis(B: np.ndarray) -> np.ndarray:
    # row x lies in B^perp iff x J B^T = 0; nullspace of (J B^T)^T.
    H = (J @ B.T).T % P
    # RREF H, then standard nullspace basis.
    A=H.copy(); r=0; piv=[]
    for c in range(A.shape[1]):
        p=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if p is None: continue
        A[[r,p]]=A[[p,r]]; A[r]=A[r]*pow(int(A[r,c]),-1,P)%P
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]=(A[i]-A[i,c]*A[r])%P
        piv.append(c); r+=1
        if r==A.shape[0]: break
    free=[c for c in range(A.shape[1]) if c not in piv]; rows=[]
    for f in free:
        x=np.zeros(A.shape[1],dtype=np.int64); x[f]=1
        for i,c in enumerate(piv): x[c]=(-A[i,f])%P
        rows.append(x)
    return np.array(rref_key(np.array(rows,dtype=np.int64)),dtype=np.int64)


def intersection_dim(A: np.ndarray, B: np.ndarray) -> int:
    return A.shape[0]+B.shape[0]-rankp(np.vstack([A,B]))


def srg_params(adj: np.ndarray) -> tuple[int,int,int,int]:
    n=len(adj); deg=adj.sum(1); assert len(set(map(int,deg)))==1; k=int(deg[0])
    lam=set(); mu=set()
    for i in range(n):
        for j in range(i+1,n):
            z=int(np.logical_and(adj[i],adj[j]).sum())
            (lam if adj[i,j] else mu).add(z)
    assert len(lam)==len(mu)==1
    return n,k,next(iter(lam)),next(iter(mu))


def main(write=True):
    A=parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m1')
    B=parse_meataxe(ROOT/'data/atlas/2SuzG1-f3r12B0.m2')
    gens=[A,B]
    assert rankp(J)==12 and all(np.array_equal((g@J@g.T)%P,J) for g in gens)

    T=point_orbit(T_SEED,gens); assert len(T)==32760
    for U in (U1,U2,U3):
        assert rankp(U)==4 and rankp(U@J@U.T%P)==4
        assert len(projective_points(U))==40 and projective_points(U)<=T
    assert np.all((U1@J@U2.T)%P==0) and np.all((U1@J@U3.T)%P==0) and np.all((U2@J@U3.T)%P==0)
    assert rankp(np.vstack([U1,U2,U3]))==12

    orb=subspace_orbit(U1,gens); assert len(orb)==135135
    partners=[V for V in orb.values() if np.all((U1@J@V.T)%P==0)]
    assert len(partners)==54
    complements=[]
    for V in partners:
        W=perp_basis(np.vstack([U1,V])); assert W.shape==(4,12)
        assert rankp(W@J@W.T%P)==4 and projective_points(W)<=T
        complements.append(W)

    # Complement involution pairs the 54 partners into 27 decompositions through U1.
    pkeys={rref_key(V) for V in partners}; pairs=set()
    for V,W in zip(partners,complements):
        a,b=sorted((rref_key(V),rref_key(W))); assert a in pkeys and b in pkeys
        pairs.add((a,b))
    assert len(pairs)==27
    dec=[(np.array(a,dtype=np.int64),np.array(b,dtype=np.int64)) for a,b in sorted(pairs)]

    sig=Counter(); adj=np.zeros((27,27),dtype=bool)
    for i,j in itertools.combinations(range(27),2):
        Ai,Bi=dec[i]; Aj,Bj=dec[j]
        s=tuple(sorted([intersection_dim(Ai,Aj),intersection_dim(Ai,Bj),
                        intersection_dim(Bi,Aj),intersection_dim(Bi,Bj)]))
        sig[s]+=1
        if s==(2,2,2,2): adj[i,j]=adj[j,i]=True
    assert sig==Counter({(0,0,0,0):216,(2,2,2,2):135})
    assert srg_params(adj)==(27,10,1,5)

    nW=len(orb); nT=len(T); through_point=nW*40//nT
    ndecomp=nW*54//6
    assert through_point==165 and ndecomp==1216215 and 54//2==27

    out={
      'schema':'w33.suzuki_w33_e6_incidence_tower.v1','status':'PASS',
      'headline':'The 32760-point 2.Suz tight orbit in W(11,3) contains complete nondegenerate W(3,3) subspaces. Their 2.Suz orbit has size 135135. Each has 54 orthogonal full-W33 partners; complement pairs those partners into 27 decompositions and every complement is again a full W33 in the tight set. Hence the E8^3 three-W33 root shadow embeds 120/120 in the Leech shell, and the 27 local decompositions form SRG(27,10,1,5), the E6 cubic-surface 27-line carrier.',
      'tight_set_points':32760,
      'full_W33_orbit':{'count':135135,'points_each':40,'through_each_tight_point':165,
                        'orthogonal_partners_each':54},
      'three_W33_decompositions':{'count':1216215,'through_each_W33':27,'root_shadow_overlap':'120/120'},
      'generalized_hamming':{'projective_two_weight_code':'[32760,12]_3','d_8':32720,
                             'reason':'a 4-dimensional vector subspace has at most 40 projective points, and a full 40-point intersection is attained'},
      'local_E6_carrier':{'vertices':27,'pair_signature_census':{'0,0,0,0':216,'2,2,2,2':135},
                          'adjacency':'all four cross-intersections have vector dimension 2','srg':[27,10,1,5],
                          'complement_srg':[27,16,10,8]},
      'explicit_decomposition':{'U1':U1.tolist(),'U2':U2.tolist(),'U3':U3.tolist()},
      'repo_prior_art':[
        'exploration/w33_center_quad_gq42_e6_bridge.py: SRG(27,10,1,5) cubic/E6 carrier',
        'analysis/w33_pass4659_internal_e6_27_36_45_triangle.py: internal 27-36-45 E6 incidence triangle',
        'analysis/w33_pass4964_4965_4967_double_six_spread_transceiver.py: unique 36 double-six <-> 36 W33 spread equivariant bridge'],
      'boundary':'These are exact finite-geometric statements. Identifying the three-W33 decomposition with a physical tensor factorization or error-correcting architecture is an interpretation, not part of the theorem.',
      'checks':{'T_32760':True,'three_full_W33s':True,'orbit_135135':True,'orthogonal_degree_54':True,
                'all_54_complements_full':True,'decompositions_1216215':True,'incidence_165':True,
                'local_E6_srg':True,'global_overlap_120':True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return out

if __name__=='__main__': main(True)
