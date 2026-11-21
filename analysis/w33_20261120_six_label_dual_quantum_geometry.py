#!/usr/bin/env python3
"""Finite W(3,3)/Q(4,3) minimal induced-motif separator and 45 two-qutrit frames.

Build both polar graphs, compare every induced graph on <=5 vertices, then
show the first distinction is a 6-vertex K3,3 (720 versus 0).
Finite mathematics only: not a six-particle effect or a physical TOE.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_six_motif_duality_quantum_frames.json"

def canon(v,q=3):
    v=tuple(int(x)%q for x in v)
    f=next(x for x in v if x)
    return tuple(x*pow(f,-1,q)%q for x in v)

def symp(a,b,q=3):
    return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%q

def geometry(q=3):
    assert q in (2,3,5) # prime-field checks
    pts=sorted({canon(v,q) for v in product(range(q),repeat=4) if any(v)})
    n=(q+1)*(q*q+1)
    assert len(pts)==n
    ix={p:i for i,p in enumerate(pts)}
    A=np.zeros((n,n),dtype=np.int8)
    for i,j in combinations(range(n),2):
        if not symp(pts[i],pts[j],q): A[i,j]=A[j,i]=1
    lines=set()
    for i,j in combinations(range(n),2):
        if not A[i,j]:continue
        u,v=pts[i],pts[j]
        L=frozenset(ix[canon(tuple((a*u[k]+b*v[k])%q for k in range(4)),q)]
                    for a,b in product(range(q),repeat=2) if a or b)
        assert len(L)==q+1
        lines.add(L)
    lines=sorted(lines,key=lambda x:tuple(sorted(x)))
    assert len(lines)==n
    M=np.array([[int(i in line) for line in lines] for i in range(n)],dtype=int)
    B=(M.T@M-(q+1)*np.eye(n,dtype=int)).astype(np.int8)
    assert np.array_equal(M@M.T,A+(q+1)*np.eye(n))
    assert set(A.sum(1))=={q*(q+1)}
    assert set(B.sum(1))=={q*(q+1)}
    return pts,A,B,M

def small_motifs(C,n):
    pairs=list(combinations(range(n),2))
    idx={e:i for i,e in enumerate(pairs)}
    rewrites=[[idx[tuple(sorted((p[a],p[b])))] for a,b in pairs]
              for p in permutations(range(n))]
    canonical=[]
    for mask in range(1<<len(pairs)):
        canonical.append(min(sum(((mask>>i)&1)<<row[i] for i in range(len(pairs)))
                             for row in rewrites))
    counts=Counter()
    for subset in combinations(range(C.shape[0]),n):
        mask=sum(int(C[subset[a],subset[b]])<<i for i,(a,b) in enumerate(pairs))
        counts[canonical[mask]]+=1
    assert sum(counts.values())==comb(C.shape[0],n)
    return counts

def triad_counts(C):
    n=C.shape[0]
    adj=[sum(1<<j for j in range(n) if C[i,j]) for i in range(n)]
    hist=Counter()
    for i,j,k in combinations(range(n),3):
        if C[i,j] or C[j,k] or C[i,k]:continue
        common=adj[i]&adj[j]&adj[k]
        c=common.bit_count()
        hist[c]+=1
        if c>=3:
            ids=[v for v in range(n) if (common>>v)&1]
            assert all(not C[u,v] for u,v in combinations(ids,2))
    f1=sum(k*v for k,v in hist.items())
    f2=sum(comb(k,2)*v for k,v in hist.items() if k>=2)
    f3=sum(comb(k,3)*v for k,v in hist.items() if k>=3)
    assert f3%2==0
    return dict(histogram={str(k):v for k,v in sorted(hist.items())},
                independent_triads=sum(hist.values()),
                moments=[f1,f2,f3],induced_K33=f3//2)

def frames45(pts,A):
    ix={p:i for i,p in enumerate(pts)}
    planes=set()
    for i,j in combinations(range(40),2):
        if A[i,j]:continue
        a,b=pts[i],pts[j]
        P=frozenset(ix[canon(tuple((r*a[k]+s*b[k])%3 for k in range(4)))]
                    for r,s in product(range(3),repeat=2) if r or s)
        assert len(P)==4
        planes.add(P)
    assert len(planes)==90
    frames=set()
    covers=set()
    for P in planes:
        Q=frozenset(i for i,v in enumerate(pts) if all(symp(v,pts[k])==0 for k in P))
        assert len(Q)==4 and Q in planes and P.isdisjoint(Q)
        assert all(not A[i,j] for i,j in combinations(P,2))
        assert all(not A[i,j] for i,j in combinations(Q,2))
        assert all(A[i,j] for i in P for j in Q)
        frames.add(frozenset((P,Q)))
        for p in combinations(sorted(P),3):
            for q in combinations(sorted(Q),3):
                covers.add(frozenset(p+q))
    assert len(frames)==45 and len(covers)==720
    return frames

def weyl_frames(pts,frames):
    omega=np.exp(2j*np.pi/3)
    eye=np.eye(3,dtype=complex)
    X=np.roll(eye,1,axis=0)
    Z=np.diag([1,omega,omega**2])
    def W(v):
        return np.kron(np.linalg.matrix_power(Z,v[0])@np.linalg.matrix_power(X,v[1]),
                       np.linalg.matrix_power(Z,v[2])@np.linalg.matrix_power(X,v[3]))
    err=0.
    for frame in frames:
        P,Q=list(frame)
        for i in P:
            for j in Q:
                err=max(err,float(np.linalg.norm(W(pts[i])@W(pts[j])-W(pts[j])@W(pts[i]))))
        def plane_vectors(P):
            a,b=(pts[i] for i in sorted(P)[:2])
            return {tuple((r*a[k]+s*b[k])%3 for k in range(4))
                    for r,s in product(range(3),repeat=2)}
        U,V=plane_vectors(P),plane_vectors(Q)
        assert len(U)==len(V)==9
        assert len({tuple((u[k]+v[k])%3 for k in range(4)) for u in U for v in V})==81
    assert err<1e-12
    all_w=np.stack([W(v).ravel() for v in product(range(3),repeat=4)])
    gram=all_w.conj()@all_w.T
    hs=float(np.max(abs(gram-9*np.eye(81))))
    assert hs<1e-11
    return {"frames":45,"max_cross_commutator_residual":err,"HS_basis_residual":hs}

def run(write=True):
    pts,A,B,M=geometry(3)
    s1=np.linalg.eigvalsh(A);s2=np.linalg.eigvalsh(B)
    assert max(abs(s1-s2))<1e-12
    assert Counter(round(float(x)) for x in s1)==Counter({12:1,2:24,-4:15})
    low={}
    for n in range(2,6):
        x,y=small_motifs(A,n),small_motifs(B,n)
        assert x==y
        low[str(n)]={"matching":True,"motif_types":len(x),"subsets_per_graph":comb(40,n)}
    a,b=triad_counts(A),triad_counts(B)
    assert a["histogram"]=={"1":2880,"4":360}
    assert b["histogram"]=={"0":1080,"2":2160}
    assert a["moments"]==[4320,2160,1440] and b["moments"]==[4320,2160,0]
    assert a["induced_K33"]==720 and b["induced_K33"]==0
    frames=frames45(pts,A)
    quantum=weyl_frames(pts,frames)
    qchecks={}
    for q in (2,3,5):
        _,P,D,_=geometry(q)
        r1,r2=triad_counts(P),triad_counts(D)
        prediction=q*q*(q*q+1)//2*comb(q+1,3)**2
        assert r1["induced_K33"]==prediction
        assert r2["induced_K33"]==(prediction if q==2 else 0)
        qchecks[str(q)]={"W_point":r1,"dual":r2,"point_K33_theorem":prediction}
    result={"status":"PASS_MINIMAL_SIX_LABEL_DUAL_GEOMETRY_DISCRIMINATOR",
            "point_spectrum":{"12":1,"2":24,"-4":15},
            "Laplacian_heat_trace_both":"1+24exp(-10t)+15exp(-16t)",
            "all_induced_motifs_through_five":low,
            "W33_independent_triad_centers":a,
            "Q43_independent_triad_centers":b,
            "n_symplectic_tensor_splits":len(frames),
            "induced_K33_per_split":16,
            "quantum":quantum,
            "prime_field_tests":qchecks,
            "odd_prime_power_formula":"q^2(q^2+1)/2 * binom(q+1,3)^2 for W point K33; dual 0 for odd q",
            "scope":"Finite-geometry, Weyl-algebra and full small-motif census. Not a six-particle effect or a physical prediction."}
    if write:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    return result

if __name__=="__main__":
    r=run()
    print(json.dumps({"status":r["status"],"motifs":r["all_induced_motifs_through_five"],
                      "K33":{q:(v["W_point"]["induced_K33"],v["dual"]["induced_K33"])
                             for q,v in r["prime_field_tests"].items()}},indent=2))
