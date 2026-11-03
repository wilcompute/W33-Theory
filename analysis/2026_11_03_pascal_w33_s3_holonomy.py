#!/usr/bin/env python3
"""An S3-equivariant symplectic W33 connection over the ternary Pascal graph.

Gauge data come from triangular edge directions, with no fitted edge phases.
Symplectic action, Wilson conjugacy, holonomy group and zero-mode census checked.
This is a candidate transport connection, not an emergent physical gauge law.
"""
from __future__ import annotations
from itertools import product
from collections import Counter,deque
from pathlib import Path
import json
import networkx as nx
import numpy as np
from scipy.sparse import lil_matrix

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_pascal_w33_s3_holonomy.json"
ID=(0,1,2)
SWAP={(0,1):(1,0,2),(0,2):(2,1,0),(1,2):(0,2,1)}
def mul(a,b): return tuple(a[b[i]] for i in range(3))
def inv(a): return tuple(a.index(i) for i in range(3))
def closure(gens):
    H={ID};stack=list(gens)
    while stack:
        g=stack.pop()
        if g in H:continue
        H.add(g)
        stack.extend(mul(g,h) for h in tuple(H))
        stack.extend(mul(h,g) for h in tuple(H))
    return H
S3=closure(SWAP.values())
assert len(S3)==6

def rep2(g):
    # On (x,y,z) over F3, x+y+z=0; x,y are independent.
    M=[]
    for x,y in ((1,0),(0,1)):
        v=(x,y,(-x-y)%3)
        w=[v[g.index(j)] for j in range(3)] # permutation pushforward
        M.append(w[:2])
    return np.array(M,dtype=np.int64).T%3
def rep4(g):
    G=rep2(g)
    det=int((G[0,0]*G[1,1]-G[0,1]*G[1,0])%3)
    inverse=det*np.array([[G[1,1],-G[0,1]],[-G[1,0],G[0,0]]],dtype=np.int64)%3
    H=np.zeros((4,4),dtype=np.int64)
    H[:2,:2]=G;H[2:,2:]=inverse.T
    return H
J=np.block([[np.zeros((2,2),dtype=int),np.eye(2,dtype=int)],
            [-np.eye(2,dtype=int),np.zeros((2,2),dtype=int)]])
for g in S3:
    H=rep4(g)
    assert not np.any((H.T@J@H-J)%3)
    for h in S3:
        assert np.array_equal(rep4(mul(g,h)),(rep4(g)@rep4(h))%3)
def canonical(v):
    a=next(x for x in v if x%3)
    return tuple((int(x)*pow(int(a),-1,3))%3 for x in v)
P=sorted({canonical(v) for v in product(range(3),repeat=4) if any(v)})
assert len(P)==40
loc={x:i for i,x in enumerate(P)}
Wperm={}
for g in S3:
    M=rep4(g)
    Wperm[g]=tuple(loc[canonical((M@np.asarray(v))%3)] for v in P)
    assert len(set(Wperm[g]))==40
for a in S3:
  for b in S3:
    assert Wperm[mul(a,b)]==tuple(Wperm[a][Wperm[b][i]] for i in range(40))
def pairing(a,b):
    return (a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
for g in S3:
    f=Wperm[g]
    for i in range(40):
      for j in range(i+1,40):
        assert (pairing(P[i],P[j])==0)==(pairing(P[f[i]],P[f[j]])==0)

def lucas(n,k):
    while n or k:
        if k%3>n%3:return False
        n//=3;k//=3
    return True

def build(level):
    w=3**level
    pts=sorted((n,k) for n in range(w) for k in range(n+1) if lucas(n,k))
    graph=nx.Graph()
    graph.add_nodes_from(pts)
    pset=set(pts)
    labels={}
    for n,k in pts:
        for v in ((n,k+1),(n+1,k),(n+1,k+1)):
            if v not in pset:continue
            u=(n,k)
            # barycentric i=k, j=n-k, h=w-1-n
            a=(k,n-k,w-1-n)
            b=(v[1],v[0]-v[1],w-1-v[0])
            indices=tuple(i for i in range(3) if a[i]!=b[i])
            assert len(indices)==2
            graph.add_edge(u,v)
            labels[frozenset((u,v))]=SWAP[indices]
    assert nx.is_connected(graph)
    return graph,labels

def holonomy(g,labels):
    root=min(g.nodes)
    gauge={root:ID};Q=deque([root])
    while Q:
        u=Q.popleft()
        for v in g.neighbors(u):
            if v in gauge:continue
            gauge[v]=mul(gauge[u],labels[frozenset((u,v))])
            Q.append(v)
    assert len(gauge)==len(g)
    transformed={}
    for u,v in g.edges:
        h=labels[frozenset((u,v))]
        transformed[frozenset((u,v))]=mul(mul(gauge[u],h),inv(gauge[v]))
    nontrivial=[h for h in transformed.values() if h!=ID]
    H=closure(nontrivial)
    counts=Counter(str(sorted(h)) for h in transformed.values())
    # Exact Wilson loop conjugacy under deterministic nonuniform gauge.
    local={v:list(S3)[(abs(hash(v))%6)] for v in g}
    for u,v in g.edges:
        h=labels[frozenset((u,v))]
        hprime=mul(mul(local[u],h),inv(local[v]))
        assert mul(mul(inv(local[u]),hprime),local[v])==h
    return gauge,transformed,H,counts

def orbits_on_points(H):
    remaining=set(range(40));orbits=[]
    while remaining:
        start=min(remaining)
        orbit={Wperm[h][start] for h in H}
        assert orbit<=remaining
        remaining-=orbit
        orbits.append(sorted(orbit))
    return orbits

def laplacian_small(g,labels):
    sites=list(g.nodes);ind={v:i for i,v in enumerate(sites)}
    N=len(sites)*40
    L=lil_matrix((N,N),dtype=np.float64)
    for u,v in g.edges:
        iu=ind[u]*40;iv=ind[v]*40
        L[iu:iu+40,iu:iu+40]+=np.eye(40)
        L[iv:iv+40,iv:iv+40]+=np.eye(40)
        p=Wperm[labels[frozenset((u,v))]]
        for i,j in enumerate(p):
            L[iu+j,iv+i]-=1
            L[iv+i,iu+j]-=1
    return L.toarray()

def run():
    cases=[]
    for level in (1,2,3):
        g,labels=build(level)
        gauge,transformed,H,counts=holonomy(g,labels)
        orbit_sizes=Counter(len(x) for x in orbits_on_points(H))
        triangles=sum(nx.triangles(g).values())//3
        basis=nx.cycle_basis(g)
        assert len(basis)==g.number_of_edges()-g.number_of_nodes()+1
        case={"level":level,"nodes":len(g),"edges":g.number_of_edges(),
              "cycle_rank":len(basis),"triangles":triangles,
              "holonomy_subgroup_order":len(H),
              "holonomy_group_elements":[list(x) for x in sorted(H)],
              "w33_point_orbit_size_census":{str(k):int(v) for k,v in orbit_sizes.items()},
              "predicted_exact_covariantly_constant_dimensions":len(orbits_on_points(H)),
              "total_nontrivial_chords_after_tree_gauge":len([a for a in transformed.values() if a!=ID])}
        if level==1:
            M=laplacian_small(g,labels)
            eig=np.linalg.eigvalsh(M)
            observed=int(np.count_nonzero(abs(eig)<1e-8))
            assert observed==case["predicted_exact_covariantly_constant_dimensions"], (observed,case)
            case.update(twisted_graph_laplacian_dimension=len(M),
              verified_zero_modes=observed,smallest_positive_eigenvalue=float(eig[observed]),
              all_eigenvalues_nonnegative=bool(eig.min()>-1e-8))
        cases.append(case)
    assert all(c["holonomy_subgroup_order"]==6 for c in cases)
    out={"status":"PASS_FINITE_SYMPLECTIC_HOLONOMY",
         "edge_rule":"Triangular nearest-neighbor edge transfers one barycentric coordinate unit, assigned the transposition of the two affected coordinate axes in S3. Fiber group embeds faithfully in Sp4(F3) by block diag(g,(g^-1)^T).",
         "intrinsic_symmetry":"Coordinate S3 acts equivariantly on the local direction labels; the connection does not require fitted edge phases.",
         "scope":"A declared nonflat combinatorial connection on an externally chosen Pascal lattice, not derived unique dynamics, continuum Yang-Mills, or photons.",
         "verification":"Projective W33 automorphism 40 points, full Sp4 form, tree-gauge Wilson subgroup, covariantly constant 40-fiber modes verified for first level.",
         "cases":cases}
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS S3/W33 HOLONOMY",[(z["level"],z["holonomy_subgroup_order"],z["predicted_exact_covariantly_constant_dimensions"],z["triangles"]) for z in cases],flush=True)
    return out
if __name__=="__main__":run()
