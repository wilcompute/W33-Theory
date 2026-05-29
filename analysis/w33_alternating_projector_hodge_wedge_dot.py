#!/usr/bin/env python3
"""Alternating projector / Hodge-star / wedge-dot duality theorem.

This verifies the operator version of the flag-codec picture:

1. AG(2,2) is the affine plane with four points.  Its full affine symmetry group
   AGL(2,2) has order 24 and is S4.  The even subgroup is A4 of order 12.

2. On the 24 tetrahedron flags, the A4 averaging projector has rank 2: it
   collapses flags to the two chiral 12-flag codecs.  The diagonal chirality
   projectors have rank 12 each.

3. Tetrahedral Hodge star reverses the flag chain and commutes with the
   alternating projector; it swaps vertex and face incidence while preserving
   chirality and edge axes.

4. On the 16-blade Boolean/tetrahedral exterior algebra, unsigned Hodge star
   maps wedge expansion to dot/contraction:

       * (e_i wedge -) = (i_i -) *

   at the support/incidence level.  This is the clean operator reading:

       Csaszar  = vertex/wedge/max-vertex-adjacency side,
       Szilassi = face/dot/max-face-adjacency side,
       tetrahedron = Hodge-star hinge conjugating wedge <-> dot.

5. PG(2,2), the Fano plane, has projective automorphism group GL(3,2) of order
   168.  This is the projective closure of the affine/alternating codec layer.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path

import numpy as np

CODEC=12
TET_FLAGS=24
FANO_AUT=168
Q4_VERTICES=16

AFFINE_POINTS=[(0,0),(1,0),(0,1),(1,1)]
AFF_IDX={p:i for i,p in enumerate(AFFINE_POINTS)}
TET_VERTS=(0,1,2,3)


def parity_perm(p):
    inv=0
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            inv += p[i] > p[j]
    return inv%2


def mat2_mul(A,x):
    return ((A[0][0]*x[0]+A[0][1]*x[1])%2,(A[1][0]*x[0]+A[1][1]*x[1])%2)


def mat2_det(A):
    return (A[0][0]*A[1][1]-A[0][1]*A[1][0])%2


def gl22():
    mats=[]
    for entries in itertools.product((0,1), repeat=4):
        A=((entries[0],entries[1]),(entries[2],entries[3]))
        if mat2_det(A)==1:
            mats.append(A)
    return mats


def agl22_perms():
    perms=set()
    for A in gl22():
        for b in AFFINE_POINTS:
            image=[]
            for x in AFFINE_POINTS:
                Ax=mat2_mul(A,x)
                y=((Ax[0]+b[0])%2,(Ax[1]+b[1])%2)
                image.append(AFF_IDX[y])
            perms.add(tuple(image))
    return sorted(perms)


def all_s4():
    return sorted(itertools.permutations(range(4)))


def flags():
    return list(itertools.permutations(TET_VERTS))


def compose_perm(g, f):
    # left action on flag values: (g o f)(i)=g[f(i)] represented by tuple of images.
    return tuple(g[x] for x in f)


def permutation_matrix_on_flags(g, F, idx):
    M=np.zeros((len(F),len(F)), dtype=float)
    for f in F:
        gf=compose_perm(g,f)
        M[idx[gf], idx[f]]=1.0
    return M


def a4_average_projector(F, idx):
    even=[g for g in all_s4() if parity_perm(g)==0]
    P=sum(permutation_matrix_on_flags(g,F,idx) for g in even)/len(even)
    return P


def chirality_projectors(F,idx):
    Pe=np.zeros((len(F),len(F)), dtype=float)
    Po=np.zeros((len(F),len(F)), dtype=float)
    for f in F:
        if parity_perm(f)==0:
            Pe[idx[f],idx[f]]=1.0
        else:
            Po[idx[f],idx[f]]=1.0
    return Pe,Po


def hodge_flag(f):
    # Reverse incidence chain: vertex<->opposite face, edge<->opposite edge.
    return (f[3],f[2],f[1],f[0])


def hodge_flag_matrix(F,idx):
    H=np.zeros((len(F),len(F)), dtype=float)
    for f in F:
        H[idx[hodge_flag(f)],idx[f]]=1.0
    return H


def vertex_of_flag(f): return f[0]
def face_of_flag(f): return tuple(sorted(f[:3]))
def missing_vertex(face): return tuple(sorted(set(TET_VERTS)-set(face)))[0]
def edge_of_flag(f): return tuple(sorted(f[:2]))
def opposite_edge(e): return tuple(sorted(set(TET_VERTS)-set(e)))
def edge_axis(e): return tuple(sorted((e,opposite_edge(e))))


def blade_subsets():
    return [tuple(c) for k in range(5) for c in itertools.combinations(range(4),k)]


def hodge_blade_matrix(B,bidx):
    H=np.zeros((len(B),len(B)), dtype=int)
    full=set(range(4))
    for s in B:
        comp=tuple(sorted(full-set(s)))
        H[bidx[comp],bidx[s]]=1
    return H


def wedge_support_matrix(i,B,bidx):
    W=np.zeros((len(B),len(B)), dtype=int)
    for s in B:
        if i in s: continue
        out=tuple(sorted(set(s)|{i}))
        W[bidx[out],bidx[s]]=1
    return W


def dot_support_matrix(i,B,bidx):
    C=np.zeros((len(B),len(B)), dtype=int)
    for s in B:
        if i not in s: continue
        out=tuple(x for x in s if x!=i)
        C[bidx[out],bidx[s]]=1
    return C


def gf2_rank(rows):
    A=[list(r) for r in rows if any(r)]
    if not A: return 0
    m=len(A); n=len(A[0]); rank=0; col=0
    while rank<m and col<n:
        piv=next((i for i in range(rank,m) if A[i][col]),None)
        if piv is None:
            col+=1; continue
        A[rank],A[piv]=A[piv],A[rank]
        for i in range(m):
            if i!=rank and A[i][col]:
                A[i]=[x^y for x,y in zip(A[i],A[rank])]
        rank+=1; col+=1
    return rank


def mat3_mul(A,x):
    return tuple(sum(A[i][j]*x[j] for j in range(3))%2 for i in range(3))


def gl32():
    mats=[]
    for entries in itertools.product((0,1), repeat=9):
        rows=[entries[0:3],entries[3:6],entries[6:9]]
        if gf2_rank(rows)==3:
            mats.append(tuple(tuple(r) for r in rows))
    return mats


def fano_points():
    return [x for x in itertools.product((0,1), repeat=3) if x!=(0,0,0)]


def fano_lines():
    pts=fano_points()
    lines=set()
    for a,b in itertools.combinations(pts,2):
        c=tuple((a[i]^b[i]) for i in range(3))
        lines.add(tuple(sorted((a,b,c))))
    return sorted(lines)


def pg22_aut_perms():
    pts=fano_points(); pidx={p:i for i,p in enumerate(pts)}
    perms=set()
    for A in gl32():
        perms.add(tuple(pidx[mat3_mul(A,p)] for p in pts))
    return sorted(perms)


def build_payload():
    agl=agl22_perms(); s4=all_s4(); a4=[g for g in s4 if parity_perm(g)==0]
    F=flags(); fidx={f:i for i,f in enumerate(F)}
    Palt=a4_average_projector(F,fidx)
    Pe,Po=chirality_projectors(F,fidx)
    Hflag=hodge_flag_matrix(F,fidx)
    B=blade_subsets(); bidx={b:i for i,b in enumerate(B)}
    Hblade=hodge_blade_matrix(B,bidx)
    wedge_dot_checks=[]
    for i in range(4):
        W=wedge_support_matrix(i,B,bidx)
        C=dot_support_matrix(i,B,bidx)
        wedge_dot_checks.append(bool(np.array_equal(Hblade@W, C@Hblade)))
    pg=pg22_aut_perms(); lines=fano_lines(); pts=fano_points()
    # Fano automorphism line preservation.
    line_set={tuple(sorted(line)) for line in lines}
    pg_preserves_lines=True
    for perm in pg:
        for line in lines:
            image=tuple(sorted(pts[perm[pts.index(p)]] for p in line))
            if image not in line_set:
                pg_preserves_lines=False
                break
        if not pg_preserves_lines: break
    # Fano flag orbit under PG group.
    incident_flags=[(p,line) for p in pts for line in lines if p in line]
    base=incident_flags[0]
    orbit=set()
    for perm in pg:
        p,line=base
        ip=pts[perm[pts.index(p)]]
        il=tuple(sorted(pts[perm[pts.index(x)]] for x in line))
        orbit.add((ip,il))
    # Hodge flag stats.
    dual_checks={
        "hodge_flag_involution": bool(np.array_equal(Hflag@Hflag, np.eye(24))),
        "hodge_preserves_chirality_projectors": bool(np.array_equal(Hflag@Pe, Pe@Hflag) and np.array_equal(Hflag@Po, Po@Hflag)),
        "hodge_commutes_with_A4_average_projector": bool(np.allclose(Hflag@Palt, Palt@Hflag)),
        "hodge_swaps_vertex_face": all(vertex_of_flag(hodge_flag(f))==missing_vertex(face_of_flag(f)) for f in F),
        "hodge_sends_edge_to_opposite_edge": all(edge_of_flag(hodge_flag(f))==opposite_edge(edge_of_flag(f)) for f in F),
        "hodge_preserves_edge_axis": all(edge_axis(edge_of_flag(hodge_flag(f)))==edge_axis(edge_of_flag(f)) for f in F),
    }
    checks={
        "AGL22_order_24": len(agl)==24,
        "AGL22_equals_S4_on_four_affine_points": set(agl)==set(s4),
        "A4_even_subgroup_order_12": len(a4)==CODEC,
        "flag_count_24": len(F)==TET_FLAGS,
        "A4_average_projector_idempotent": bool(np.allclose(Palt@Palt,Palt)),
        "A4_average_projector_rank_2": int(np.linalg.matrix_rank(Palt,tol=1e-10))==2,
        "chiral_projectors_rank_12_each": int(np.linalg.matrix_rank(Pe))==12 and int(np.linalg.matrix_rank(Po))==12,
        "chiral_projectors_sum_identity": bool(np.array_equal(Pe+Po,np.eye(24))),
        "hodge_dual_checks": all(dual_checks.values()),
        "blade_count_16": len(B)==Q4_VERTICES,
        "blade_grade_row_1_4_6_4_1": [sum(1 for b in B if len(b)==k) for k in range(5)]==[1,4,6,4,1],
        "hodge_blade_involution": bool(np.array_equal(Hblade@Hblade,np.eye(16,dtype=int))),
        "hodge_conjugates_wedge_to_dot_all_generators": all(wedge_dot_checks),
        "PG22_points_lines_7_7": len(pts)==7 and len(lines)==7,
        "PG22_projective_group_order_168": len(pg)==FANO_AUT,
        "PG22_preserves_fano_lines": pg_preserves_lines,
        "PG22_transitive_on_21_fano_flags": len(orbit)==21,
    }
    return {
        "theorem":"Alternating_Projector_Hodge_Wedge_Dot_Theorem",
        "affine_alternating_layer":{
            "AG2_2_points":AFFINE_POINTS,
            "AGL2_2_order":len(agl),
            "AGL2_2_isomorphism":"AGL(2,2) acts faithfully on four affine points and equals S4",
            "A4_order":len(a4),
            "A4_average_projector_rank":int(np.linalg.matrix_rank(Palt,tol=1e-10)),
            "chiral_projector_ranks":[int(np.linalg.matrix_rank(Pe)),int(np.linalg.matrix_rank(Po))],
            "interpretation":"A4 averaging collapses 24 flags to two chiral 12-flag codecs; diagonal chirality projectors isolate each 12-flag half."
        },
        "tetrahedral_hodge_star":{
            "flag_dual":"dual(a,b,c,d)=(d,c,b,a)",
            "checks":dual_checks,
            "interpretation":"Hodge star is the self-dual tetrahedral hinge: it swaps vertex and face incidence, maps each edge to the opposite edge, preserves chirality and edge axes, and commutes with the alternating projector."
        },
        "wedge_dot_operator_layer":{
            "blade_count":len(B),
            "grade_row":[sum(1 for b in B if len(b)==k) for k in range(5)],
            "identity":"unsigned Hodge star satisfies H*wedge_i = dot_i*H for each generator i",
            "per_generator_checks":wedge_dot_checks,
            "reading":"Csaszar is the vertex/wedge expansion side; Szilassi is the face/dot contraction side; tetrahedral Hodge star conjugates them."
        },
        "projective_fano_closure":{
            "PG2_2_points":len(pts),
            "PG2_2_lines":len(lines),
            "projective_automorphism_group_order":len(pg),
            "line_preservation":pg_preserves_lines,
            "flag_orbit_size":len(orbit),
            "interpretation":"PG(2,2) closes the affine/alternating tetrahedral layer to the 168-element Fano projective symmetry."
        },
        "operator_architecture":{
            "alternating_projector":"A4/S4 affine chirality projector on tetrahedral flags",
            "hodge_star":"tetrahedral self-dual vertex-face edge-axis duality",
            "wedge":"Csaszar maximal-vertex adjacency / exterior expansion",
            "dot":"Szilassi maximal-face adjacency / contraction",
            "projective_closure":"Fano PG(2,2) with automorphism group 168"
        },
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main():
    payload=build_payload()
    out=Path("data/w33_alternating_projector_hodge_wedge_dot.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"affine_alternating_layer":payload["affine_alternating_layer"],"tetrahedral_hodge_star":payload["tetrahedral_hodge_star"],"wedge_dot_operator_layer":payload["wedge_dot_operator_layer"],"projective_fano_closure":payload["projective_fano_closure"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
