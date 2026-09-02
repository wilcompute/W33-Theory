#!/usr/bin/env python3
"""Exact topology/QEC closure for the committed 44-face K12 complex.

This module corrects a subtle but consequential inference in the older
Reye-K12 horizon work.  The committed 44 oriented triangles do use every
*directed* K12 edge exactly once, but that condition alone does not imply a
closed surface: a triangular 2-manifold also requires every vertex link to be a
single cycle.

For the actual face table in w33_reye_k12_orientable_horizon_completion.py:

* the face-edge dual graph has components of 40 and 4 faces;
* the 4-face component is the tetrahedral sphere on vertices 8,9,10,11;
* many raw vertex links are disconnected, so the 44-face complex is singular;
* normalization splits each vertex by link component and yields two honest
  orientable surfaces: a torus (20 vertices,60 edges,40 faces) and a sphere
  (4 vertices,6 edges,4 faces).

Over GF(3) the raw chain complex therefore has

    rank(d1)=11, rank(d2)=42, b0=1, b1=13, b2=2,

not the genus-6 surface values rank(d2)=43,b1=12,b2=1.  Its standard CSS chain
code is [[66,13,3]]_3.  A deterministic gauge fixing by five independent
Z-logical cycles gives an explicit K12-labelled [[66,8,3]]_3 CSS code.  This is
a genuine native 66-edge stabilizer construction, but it is a gauge-fixed code
on a singular pseudocomplex, NOT a standard genus-6 surface code.
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque
from itertools import combinations, product
import hashlib
import json

import numpy as np

import w33_reye_k12_orientable_horizon_completion as k12

Q=3


def digest_json(v):
    return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def rref(a):
    A=np.asarray(a,dtype=np.int64)%Q
    if A.ndim!=2: raise ValueError("matrix required")
    m,n=A.shape; piv=[]; r=0
    for c in range(n):
        p=next((i for i in range(r,m) if int(A[i,c])%Q),None)
        if p is None: continue
        A[[r,p]]=A[[p,r]]
        if int(A[r,c])==2: A[r]=(2*A[r])%Q
        for i in range(m):
            if i!=r and int(A[i,c])%Q:
                A[i]=(A[i]-int(A[i,c])*A[r])%Q
        piv.append(c); r+=1
        if r==m: break
    return A,piv


def rank(a): return len(rref(a)[1])


def row_basis(a):
    rr,p=rref(a); return rr[:len(p)]%Q


def nullspace(a):
    A=np.asarray(a,dtype=np.int64)%Q
    rr,piv=rref(A); free=[j for j in range(A.shape[1]) if j not in piv]; out=[]
    for f in free:
        x=np.zeros(A.shape[1],dtype=np.int64); x[f]=1
        for i,p in enumerate(piv): x[p]=(-int(rr[i,f]))%Q
        out.append(x)
    return np.asarray(out,dtype=np.int64)%Q


def in_rowspace(v,M):
    v=np.asarray(v,dtype=np.int64)%Q; M=np.asarray(M,dtype=np.int64)%Q
    return rank(np.vstack([M,v]))==rank(M)


def chain_complex():
    faces=list(k12.oriented_horizon_faces())
    edges=list(combinations(range(12),2)); ei={e:i for i,e in enumerate(edges)}
    d1=np.zeros((12,66),dtype=np.int64)
    for j,(u,v) in enumerate(edges): d1[u,j]=2; d1[v,j]=1
    d2=np.zeros((66,len(faces)),dtype=np.int64)
    for f,(a,b,c) in enumerate(faces):
        for u,v in ((a,b),(b,c),(c,a)):
            e=tuple(sorted((u,v))); d2[ei[e],f]=(d2[ei[e],f]+(1 if u<v else 2))%Q
    return faces,edges,d1%Q,d2%Q


def face_dual_components(faces):
    edge_faces=defaultdict(list)
    for i,f in enumerate(faces):
        for e in combinations(f,2): edge_faces[tuple(sorted(e))].append(i)
    adj=[set() for _ in faces]
    for e,rows in edge_faces.items():
        if len(rows)!=2: raise RuntimeError(f"edge {e} has {len(rows)} face incidences")
        a,b=rows; adj[a].add(b); adj[b].add(a)
    comps=[]; seen=set()
    for s in range(len(faces)):
        if s in seen: continue
        q=[s];seen.add(s); comp=[]
        while q:
            u=q.pop();comp.append(u)
            for v in adj[u]:
                if v not in seen:seen.add(v);q.append(v)
        comps.append(sorted(comp))
    return comps,edge_faces


def link_components(faces,vertex):
    adj=defaultdict(set)
    for f in faces:
        if vertex not in f: continue
        a,b=[x for x in f if x!=vertex]
        adj[a].add(b); adj[b].add(a)
    if not adj:return []
    if any(len(ns)!=2 for ns in adj.values()):
        raise RuntimeError(f"vertex {vertex} link is not 2-regular")
    seen=set(); comps=[]
    for s in sorted(adj):
        if s in seen:continue
        q=[s];seen.add(s);c=[]
        while q:
            u=q.pop();c.append(u)
            for v in adj[u]:
                if v not in seen:seen.add(v);q.append(v)
        comps.append(sorted(c))
    return comps


def component_topology(faces,indices):
    fs=[faces[i] for i in indices]
    vs=sorted({v for f in fs for v in f})
    es=sorted({tuple(sorted(e)) for f in fs for e in combinations(f,2)})
    link_profile={v:[len(c) for c in link_components(fs,v)] for v in vs}
    normalized_vertices=sum(len(link_components(fs,v)) for v in vs)
    chi_norm=normalized_vertices-len(es)+len(fs)
    genus=(2-chi_norm)//2
    return {"raw_vertices":len(vs),"normalized_vertices":normalized_vertices,"edges":len(es),"faces":len(fs),"normalized_chi":chi_norm,"normalized_genus":genus,"link_cycle_lengths":link_profile}


def homology_basis_cycles(d1,d2):
    cycles=nullspace(d1); boundaries=row_basis(d2.T)
    span=[r.copy() for r in boundaries]; cur=rank(np.asarray(span,dtype=np.int64)); out=[]
    for v in cycles:
        nr=rank(np.asarray(span+[v],dtype=np.int64))
        if nr>cur: out.append(v.copy());span.append(v.copy());cur=nr
    return np.asarray(out,dtype=np.int64)%Q


def low_weight_logical(Hx,Hz,max_weight=3):
    # CSS distance = min of pure-X and pure-Z distances.  Search exactly through
    # weight max_weight and return the first witness for each sector.
    def sector(commute,stab):
        cols=np.asarray(commute,dtype=np.int64).T%Q
        for w in range(1,max_weight+1):
            for sites in combinations(range(66),w):
                for vals in product((1,2),repeat=w):
                    syn=np.zeros(cols.shape[1],dtype=np.int64)
                    for s,a in zip(sites,vals): syn=(syn+a*cols[s])%Q
                    if np.any(syn):continue
                    v=np.zeros(66,dtype=np.int64)
                    for s,a in zip(sites,vals):v[s]=a
                    if not in_rowspace(v,stab):
                        return {"weight":w,"sites":list(sites),"values":list(vals),"vector":v.tolist()}
        return None
    return {"Z":sector(Hx,Hz),"X":sector(Hz,Hx)}


def sparse_rows(M):
    return [[{"edge_index":int(i),"value":int(row[i])} for i in np.flatnonzero(row)] for row in np.asarray(M,dtype=np.int64)]


def verify():
    faces,edges,d1,d2=chain_complex(); comps,edge_faces=face_dual_components(faces)
    raw_links={v:[len(c) for c in link_components(faces,v)] for v in range(12)}
    singular=[v for v,c in raw_links.items() if len(c)!=1]
    topo=[component_topology(faces,c) for c in comps]
    r1,r2=rank(d1),rank(d2); b0=1; b2=len(faces)-r2; b1=66-r1-r2

    Hx=row_basis(d1); Hz0=row_basis(d2.T)
    raw_logicals=low_weight_logical(Hx,Hz0,3)
    H1=homology_basis_cycles(d1,d2)
    extra=H1[:5]
    Hz8=row_basis(np.vstack([Hz0,extra]))
    fixed_logicals=low_weight_logical(Hx,Hz8,3)
    k0=66-rank(Hx)-rank(Hz0); k8=66-rank(Hx)-rank(Hz8)

    tetra_faces=sorted(comps,key=len)[0]
    tetra_vertices=sorted({v for i in tetra_faces for v in faces[i]})
    directed=Counter(e for f in faces for e in k12.directed_edges(f))
    undirected=Counter(tuple(sorted(e)) for f in faces for e in k12.directed_edges(f))
    checks={
        "all_132_directed_edges_once":len(directed)==132 and set(directed.values())=={1},
        "all_66_unordered_edges_twice":len(undirected)==66 and set(undirected.values())=={2},
        "face_dual_components_are_40_and_4":sorted(map(len,comps))==[4,40],
        "four_face_component_is_tetrahedron_8_9_10_11":len(tetra_faces)==4 and tetra_vertices==[8,9,10,11],
        "raw_complex_has_singular_vertex_links":len(singular)>0,
        "normalization_is_torus_plus_sphere":sorted((x["normalized_genus"],x["normalized_chi"]) for x in topo)==[(0,2),(1,0)],
        "normalization_has_24_vertices":sum(x["normalized_vertices"] for x in topo)==24,
        "chain_closes_over_GF3":not np.any((d1@d2)%Q),
        "boundary_ranks_are_11_and_42":r1==11 and r2==42,
        "raw_betti_numbers_are_1_13_2":(b0,b1,b2)==(1,13,2),
        "raw_standard_chain_code_is_66_13_3":k0==13 and raw_logicals["X"] is not None and raw_logicals["Z"] is not None and raw_logicals["X"]["weight"]==3 and raw_logicals["Z"]["weight"]==3,
        "five_extra_Z_logicals_are_independent":H1.shape==(13,66) and rank(Hz8)==47,
        "five_constraint_gauge_fix_encodes_8":k8==8,
        "gauge_fixed_native_code_still_has_distance3":fixed_logicals["X"] is not None and fixed_logicals["Z"] is not None and fixed_logicals["X"]["weight"]==3 and fixed_logicals["Z"]["weight"]==3,
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
        "schema":"w33.k12-singular-css-closure.v1","status":"PASS" if all(checks.values()) else "FAIL","checks":checks,
        "raw_complex":{"V":12,"E":66,"F":44,"chi":-10,"singular_vertices":singular,"vertex_link_cycle_lengths":raw_links,"face_dual_components":comps,"rank_d1_GF3":r1,"rank_d2_GF3":r2,"betti_GF3":{"b0":b0,"b1":b1,"b2":b2}},
        "normalization":{"components":topo,"reading":"normalization is T^2 disjoint-union S^2; the raw chi=-10 comes from identifying 24 normalized vertices down to 12 raw vertices, not from genus 6"},
        "raw_css":{"parameters":"[[66,13,3]]_3","X_rank":rank(Hx),"Z_rank":rank(Hz0),"distance_witnesses":raw_logicals},
        "native_k8_gauge_fix":{"parameters":"[[66,8,3]]_3","extra_Z_logical_constraints_sparse":sparse_rows(extra),"extra_constraint_sha256":digest_json(extra.tolist()),"X_rank":rank(Hx),"Z_rank":rank(Hz8),"distance_witnesses":fixed_logicals,"construction":"add the first five deterministic GF(3) H1 complement cycles as commuting Z stabilizers"},
        "theorem":"The committed 44-face K12 object is an orientable twofold-triple pseudocomplex with singular vertex links, not a genus-6 surface. Its normalization is a torus plus a sphere, its GF(3) first Betti number is 13, and its standard edge-chain CSS code is [[66,13,3]]_3. Five explicit independent Z-logical gauge-fixing constraints produce a native K12-labelled [[66,8,3]]_3 CSS code of distance 3.",
        "boundary":"The native [[66,8,3]]_3 gauge-fixed code is an exact stabilizer theorem on the committed singular incidence complex. It must not be called the standard genus-6 K12 surface code. The five chosen logical constraints are deterministic, not yet derived from an external physical symmetry principle, and no fault-tolerant syndrome circuit is claimed here.",
    }

if __name__=="__main__":
    out=verify();print(json.dumps(out,indent=2));raise SystemExit(0 if out["status"]=="PASS" else 1)
