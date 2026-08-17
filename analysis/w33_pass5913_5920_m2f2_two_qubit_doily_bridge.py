#!/usr/bin/env python3
"""Pass5913-5920: exact M2(F2) -> two-qubit doily bridge.

The additive 4-space underlying M2(F2), equipped with determinant q(M) and its
polarization, is explicitly identified with the standard two-qubit symplectic
Pauli space W(3,2). The nonzero rank split 9+6 becomes a grid/complement split.
A local Clifford chart maps the specific Saniga-Planat-Pracna 9-grid C7..C15
to the determinant grid.

This is a finite F2 geometry theorem, not a q=5 physical-qubit embedding.
"""
from __future__ import annotations
import collections, itertools, json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_PASS5913_5920_M2F2_TWO_QUBIT_DOILY_BRIDGE.json"

V2=[(1,0),(0,1),(1,1)]
MATS=[tuple(x) for x in itertools.product((0,1), repeat=4)]
ZERO=(0,0,0,0)

def add(x,y): return tuple(a^b for a,b in zip(x,y))
def det(m):
    a,b,c,d=m
    return (a*d)^(b*c)
def phi(m):
    a,b,c,d=m
    return (a,d,b,c)
def q0(x): return (x[0]*x[1])^(x[2]*x[3])
def symp(x,y): return (x[0]*y[1])^(x[1]*y[0])^(x[2]*y[3])^(x[3]*y[2])
def polar_det(m,n): return det(add(m,n))^det(m)^det(n)
def outer(u,v): return (u[0]*v[0],u[0]*v[1],u[1]*v[0],u[1]*v[1])

def graph(S,pair):
    A=np.zeros((len(S),len(S)),dtype=int)
    for i,j in itertools.combinations(range(len(S)),2):
        if pair(S[i],S[j])==0: A[i,j]=A[j,i]=1
    return A

def srg_params(A):
    n=A.shape[0]; deg=A.sum(1)
    if len(set(map(int,deg)))!=1: return None
    lam=set(); mu=set()
    for i,j in itertools.combinations(range(n),2):
        c=int(A[i]@A[j]); (lam if A[i,j] else mu).add(c)
    if len(lam)==1 and len(mu)==1:
        return [n,int(deg[0]),next(iter(lam)),next(iter(mu))]
    return None

def connected(A):
    seen={0}; stack=[0]
    while stack:
        i=stack.pop()
        for j in np.flatnonzero(A[i]):
            j=int(j)
            if j not in seen: seen.add(j); stack.append(j)
    return len(seen)==len(A)

def pauli_vec(p,q):
    P={'I':(0,0),'X':(1,0),'Z':(0,1),'Y':(1,1)}
    return P[p]+P[q]

SANIGA={
1:('Z','X'),2:('Y','Y'),3:('I','X'),4:('Y','Z'),5:('Y','I'),
6:('X','X'),7:('X','Z'),8:('Y','X'),9:('Z','Y'),10:('X','I'),
11:('X','Y'),12:('I','Y'),13:('I','Z'),14:('Z','Z'),15:('Z','I')}

def S2(x):
    x1,z1,x2,z2=x
    return (x1,z1,x2,z2^x2)

def main():
    assert len(set(phi(m) for m in MATS))==16
    assert all(det(m)==q0(phi(m)) for m in MATS)
    assert all(polar_det(m,n)==symp(phi(m),phi(n)) for m in MATS for n in MATS)

    nonzero=[m for m in MATS if m!=ZERO]
    rank1=[m for m in nonzero if det(m)==0]
    rank2=[m for m in nonzero if det(m)==1]
    assert (len(rank1),len(rank2))==(9,6)

    A15=graph(nonzero,polar_det)
    assert srg_params(A15)==[15,6,1,3]

    A9=graph(rank1,polar_det); A6=graph(rank2,polar_det)
    assert srg_params(A9)==[9,4,1,2]
    assert np.all(A6.sum(1)==3) and connected(A6)
    color={}
    for s in range(6):
        if s in color: continue
        color[s]=0; stack=[s]
        while stack:
            i=stack.pop()
            for j in np.flatnonzero(A6[i]):
                j=int(j)
                if j in color: assert color[j]!=color[i]
                else: color[j]=1-color[i]; stack.append(j)
    assert sorted(color.values())==[0,0,0,1,1,1]
    assert int(A6.sum()//2)==9
    cross=np.array([[polar_det(r,g)==0 for g in rank2] for r in rank1],dtype=int)
    assert set(map(int,cross.sum(1)))=={2}
    assert set(map(int,cross.sum(0)))=={3}

    rlabel={outer(u,v):(u,v) for u in V2 for v in V2}
    assert set(rlabel)==set(rank1)
    for r,s in itertools.combinations(rank1,2):
        u,v=rlabel[r]; u2,v2=rlabel[s]
        assert (polar_det(r,s)==0)==(u==u2 or v==v2)

    C={i:pauli_vec(*pq) for i,pq in SANIGA.items()}
    source_grid={C[i] for i in range(7,16)}
    det_grid={phi(m) for m in rank1}
    v=(0,0,0,1)
    assert source_grid=={x for x in map(phi,nonzero) if (q0(x)^symp(v,x))==0}
    assert {S2(x) for x in source_grid}==det_grid
    assert all(symp(S2(x),S2(y))==symp(x,y) for x in map(phi,MATS) for y in map(phi,MATS))

    V=list(map(phi,MATS)); Vnon=[x for x in V if x!=(0,0,0,0)]
    plus=[]; minus=[]
    for v in V:
        zeros=[x for x in Vnon if (q0(x)^symp(v,x))==0]
        (plus if len(zeros)==9 else minus).append((v,zeros))
    assert len(plus)==10 and all(len(z)==9 for _,z in plus)
    assert len(minus)==6 and all(len(z)==5 for _,z in minus)
    assert all(q0(v)==0 for v,_ in plus)
    assert all(q0(v)==1 for v,_ in minus)

    for v,ov in minus:
        Ao=graph(ov,symp); assert int(Ao.sum())==0
        comp=[x for x in Vnon if x not in set(ov)]
        Ac=graph(comp,symp)
        assert np.all(Ac.sum(1)==3) and connected(Ac)
        rounded=[int(round(t)) for t in np.linalg.eigvalsh(Ac)]
        assert collections.Counter(rounded)==collections.Counter({-2:4,1:5,3:1})

    perps=[]
    for p in Vnon:
        H=[x for x in Vnon if symp(p,x)==0]
        assert len(H)==7 and p in H
        perps.append(H)
    assert len(perps)==15

    out={
      "schema":"w33.pass5913_5920.m2f2_two_qubit_doily_bridge.v1",
      "status":"PASS",
      "pass_5913_symplectic_isometry":{
        "map":"Phi([[a,b],[c,d]])=(a,d,b,c)=(x1,z1,x2,z2)",
        "quadratic_identity":"det(M)=x1*z1+x2*z2",
        "polar_identity":"det(M+N)+det(M)+det(N)=<Phi(M),Phi(N)>_sp",
        "meaning":"matrix determinant polarization is exactly two-qubit Pauli commutation geometry"},
      "pass_5914_nonzero_doily":{"nonzero_matrices":15,"commutation_graph_srg":[15,6,1,3],"identification":"W(3,2), the two-qubit doily"},
      "pass_5915_rank_9plus6":{
        "rank1_nonzero_zero_divisors":9,"rank2_units":6,"rank1_induced_srg":[9,4,1,2],
        "rank1_identification":"3x3 grid Q+(3,2)=GQ(2,1)","rank2_induced_graph":"K3,3",
        "cross_degrees":{"grid_to_complement":2,"complement_to_grid":3},
        "outer_product_grid":"rank1 matrices are u v^T with 3 choices of nonzero u and 3 of nonzero v"},
      "pass_5916_source_chart_clifford":{
        "source":"Saniga--Planat--Pracna, Geometry of Two-Qubits (2007), displayed C7..C15 9-grid",
        "source_grid_quadratic":"q0(x)+x2=0",
        "local_clifford":"S on qubit 2: (x1,z1,x2,z2)->(x1,z1,x2,z2+x2)",
        "result":"the displayed source grid maps exactly to the determinant/rank-one grid"},
      "pass_5917_hyperplane_census":{
        "grids_plus_type":10,"ovoids_minus_type":6,"perp_sets":15,"minus_zero_set_size":5,
        "minus_complement_size":10,"minus_complement_graph":"Petersen graph",
        "deduction":"the determinant model recovers the doily hyperplane census 10 grids, 6 ovoids, 15 perp-sets"},
      "pass_5918_reye_radon_interface":{
        "input_from_pass5876":"4-dimensional mod-2 quotient with quadratic det and 10/6 value distribution",
        "new_identification":"its 15 nonzero classes carry W(3,2); q=0 nonzero gives the 9-grid and q=1 gives the 6-point complement",
        "boundary":"this is a quotient geometry identification, not a q=5 physical two-qubit embedding"},
      "pass_5919_ring_line_boundary":{
        "source_ring_fact":"M2(F2) has 16 elements: 6 units and 10 zero-divisors including zero",
        "exact_affine_split":"1 zero + 9 nonzero zero-divisors + 6 units",
        "not_literal":"the 15 affine nonzero matrices are not literally the 15 projective-ring-line point pairs C1..C15",
        "isomorphic_geometry":"an explicit symplectic/local-Clifford map identifies the same two-qubit doily and 9+6 grid/complement geometry"},
      "pass_5920_verdict":{
        "upgrade":"Pass5797's prior-art boundary can be sharpened from count-level analogy to an object-level finite symplectic isomorphism.",
        "physics_boundary":"No entanglement, hardware, particle, or continuum interpretation follows from this finite isomorphism alone."}}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out

if __name__=="__main__": main()
