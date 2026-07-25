#!/usr/bin/env python3
"""PART LXVII — Order-3 generation splitting on canonical H1.

Builds the W(3,3) triangle chain complex, extracts H1 as harmonic chains
ker(d1) cap ker(d2^T), and checks every projective symplectic transvection
x -> x + omega(x,a) a. Each order-3 transvection acts on H1 with
character 1^27 + omega^27 + omega^2^27.
"""
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np

q=3
Omega=np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]], dtype=int)%3

def norm(v):
    v=tuple(int(x)%q for x in v)
    if not any(v): return None
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%q for y in v)

def add(u,v): return tuple((a+b)%q for a,b in zip(u,v))
def sc(c,u): return tuple((c*a)%q for a in u)
def om(u,v): return int((np.array(u,dtype=int)@Omega@np.array(v,dtype=int))%q)
def points(): return sorted({norm(v) for v in product(range(q), repeat=4) if any(v)})

def pline(p,r):
    L=set()
    for a,b in product(range(q), repeat=2):
        if a or b: L.add(norm(add(sc(a,p),sc(b,r))))
    L.discard(None); return frozenset(L)

def all_lines(P):
    L=set()
    for p,r in combinations(P,2):
        line=pline(p,r)
        if len(line)==q+1: L.add(line)
    return sorted(L,key=lambda x:sorted(x))

def is_iso(line):
    a,b=sorted(line)[:2]
    return om(a,b)==0

def pair(i,j): return (i,j) if i<j else (j,i)
def tau(a,x): return norm(add(x, sc(om(x,a), a)))

def cluster_roots(vals):
    omega=np.exp(2j*np.pi/3)
    counts={"1":0,"omega":0,"omega2":0,"other":0}
    for z in vals:
        ds=[abs(z-1),abs(z-omega),abs(z-omega.conjugate())]
        if min(ds)>1e-6: counts["other"]+=1
        else: counts[["1","omega","omega2"][ds.index(min(ds))]]+=1
    return counts

def main():
    P=points(); idx={p:i for i,p in enumerate(P)}
    Li=[L for L in all_lines(P) if is_iso(L)]
    edges=set(); triangles=[]
    for line in Li:
        ids=sorted(idx[p] for p in line)
        for i,j in combinations(ids,2): edges.add(pair(i,j))
        for tri in combinations(ids,3): triangles.append(tri)
    edges=sorted(edges); eidx={e:i for i,e in enumerate(edges)}
    d1=np.zeros((len(P),len(edges)),dtype=float)
    for e,(i,j) in enumerate(edges): d1[i,e]=-1; d1[j,e]=1
    d2=np.zeros((len(edges),len(triangles)),dtype=float)
    for t,(a,b,c) in enumerate(triangles):
        for u,v,sgn in [(b,c,1),(a,c,-1),(a,b,1)]: d2[eidx[pair(u,v)],t]+=sgn
    M=np.vstack([d1,d2.T])
    U,S,Vt=np.linalg.svd(M, full_matrices=True)
    rank=int((S>1e-9).sum())
    H=Vt[rank:].T
    assert H.shape==(240,81)
    def action_on_edges(a):
        Pmap={i:idx[tau(a,p)] for i,p in enumerate(P)}
        G=np.zeros((len(edges),len(edges)),dtype=float)
        for e,(i,j) in enumerate(edges):
            ii,jj=Pmap[i],Pmap[j]
            ep=pair(ii,jj); ee=eidx[ep]
            sign=1 if (ii,jj)==ep else -1
            G[ee,e]=sign
        return G
    expected={"1":27,"omega":27,"omega2":27,"other":0}
    bad=[]; max_res=0.0
    P_H=H@H.T
    for a in P:
        G=action_on_edges(a)
        res=float(np.linalg.norm((np.eye(len(edges))-P_H)@(G@H)))
        max_res=max(max_res,res)
        B=H.T@G@H
        counts=cluster_roots(np.linalg.eigvals(B))
        if counts!=expected:
            bad.append({"a":a,"counts":counts})
    results={
        "projective_transvections_checked":len(P),
        "all_pass":len(bad)==0,
        "bad_cases":bad,
        "H1_dimension":H.shape[1],
        "boundary_ranks":{"rank_d1":int(np.linalg.matrix_rank(d1)),"rank_d2":int(np.linalg.matrix_rank(d2))},
        "harmonic_definition":"H1 = ker(d1) cap ker(d2^T)",
        "max_H1_invariance_residual":max_res,
        "expected_generation_character":expected,
        "verified_for_every_projective_transvection":len(bad)==0,
        "charpoly_H1":"(x - 1)^27 (x^2 + x + 1)^27",
        "generation_split":"H1_C = H1^(0) + H1^(1) + H1^(2), each dimension 27",
        "main_theorem":"Every order-3 symplectic transvection acts on canonical H1 with eigenvalue multiplicities 1^27, omega^27, omega2^27."
    }
    assert results["all_pass"]
    Path("PART_LXVII_order3_generation_split_results.json").write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=="__main__": main()
