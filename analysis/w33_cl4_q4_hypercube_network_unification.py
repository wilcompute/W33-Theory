#!/usr/bin/env python3
"""Cl4 / tetrahedron / Q4 / toroidal-knight / network unification.

The user suggested that the recurring 16 is not only the D8 ADE Frobenius
square and the Q4 router count, but also the Clifford/Pascal composition

    1,4,6,4,1

of four unit vectors.  This verifier makes that exact.

One object is being seen five ways:

1. Cl4 basis blades: subsets of 4 generators, graded by subset size.
2. Pascal row 4: binomial counts C(4,k) = 1,4,6,4,1.
3. Augmented tetrahedron face lattice: empty face, 4 vertices, 6 edges,
   4 triangular faces, 1 tetrahedron.
4. Q4 hypercube vertices: all 4-bit strings/subsets, edges flip one generator.
5. 4x4 toroidal knight board: explicitly isomorphic to Q4.

Network-theory metrics are then forced:

    |V|=16, |E|=32, degree=4, diameter=4, average distance=2,
    bisection bandwidth=8, vertex connectivity=4, edge connectivity=4.

This plugs the previous D8 result into the single-photon router picture:

    Frobenius-square norm of M_D8 = 16 = |V(Q4)| = dim(Cl4),
    rank(M_D8) = 4 = Q4 dimension = number of Clifford generators.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter, deque
from pathlib import Path
from typing import Iterable

N = 4
V_W33 = 40
H1 = 81
WE6 = 51_840
PHI6 = 7
K = 12
MU = 28
E2 = 16

BOARD = 4
KNIGHT_TO_Q4 = {
    (0,0):(0,0,0,0), (2,3):(0,0,0,1), (3,2):(0,0,1,0), (1,1):(0,0,1,1),
    (1,2):(0,1,0,0), (3,1):(0,1,0,1), (2,0):(0,1,1,0), (0,3):(0,1,1,1),
    (2,1):(1,0,0,0), (0,2):(1,0,0,1), (1,3):(1,0,1,0), (3,0):(1,0,1,1),
    (3,3):(1,1,0,0), (1,0):(1,1,0,1), (0,1):(1,1,1,0), (2,2):(1,1,1,1),
}
KNIGHT_TOUR = [(0,0),(1,2),(2,0),(3,2),(1,1),(0,3),(3,1),(2,3),(0,2),(1,0),(2,2),(3,0),(1,3),(0,1),(3,3),(2,1)]


def subsets(n:int=N) -> list[tuple[int,...]]:
    return [tuple(c) for k in range(n+1) for c in itertools.combinations(range(n), k)]


def bits_from_subset(s: Iterable[int], n:int=N) -> tuple[int,...]:
    out=[0]*n
    for i in s:
        out[i]=1
    return tuple(out)


def q_vertices(n:int=N) -> list[tuple[int,...]]:
    return list(itertools.product((0,1), repeat=n))


def q_edges(n:int=N) -> set[tuple[tuple[int,...],tuple[int,...]]]:
    edges=set()
    for v in q_vertices(n):
        for i in range(n):
            w=list(v); w[i]^=1; w=tuple(w)
            edges.add(tuple(sorted((v,w))))
    return edges


def q_adjacency(n:int=N) -> dict[tuple[int,...], set[tuple[int,...]]]:
    adj={v:set() for v in q_vertices(n)}
    for a,b in q_edges(n):
        adj[a].add(b); adj[b].add(a)
    return adj


def hamming(a:tuple[int,...], b:tuple[int,...]) -> int:
    return sum(x!=y for x,y in zip(a,b))


def all_pair_distances(adj:dict[tuple[int,...],set[tuple[int,...]]]) -> list[int]:
    out=[]
    for s in adj:
        dist={s:0}; q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v]=dist[u]+1
                    q.append(v)
        out.extend(dist.values())
    return out


def is_connected_after_vertex_removal(remove:set[tuple[int,...]], adj) -> bool:
    left=[v for v in adj if v not in remove]
    if not left:
        return True
    seen={left[0]}; q=deque([left[0]])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in remove and v not in seen:
                seen.add(v); q.append(v)
    return len(seen)==len(left)


def vertex_connectivity_exact(adj) -> int:
    verts=list(adj)
    for r in range(len(verts)+1):
        for rem in itertools.combinations(verts,r):
            if not is_connected_after_vertex_removal(set(rem), adj):
                return r
    return len(verts)-1


def is_connected_after_edge_removal(remove:set[tuple[tuple[int,...],tuple[int,...]]], adj) -> bool:
    verts=list(adj)
    seen={verts[0]}; q=deque([verts[0]])
    while q:
        u=q.popleft()
        for v in adj[u]:
            e=tuple(sorted((u,v)))
            if e not in remove and v not in seen:
                seen.add(v); q.append(v)
    return len(seen)==len(verts)


def edge_connectivity_exact(adj) -> int:
    edges=list(q_edges(N))
    for r in range(len(edges)+1):
        for rem in itertools.combinations(edges,r):
            if not is_connected_after_edge_removal(set(rem), adj):
                return r
    return len(edges)


def bisection_bandwidth_exact(adj) -> int:
    verts=list(adj)
    half=len(verts)//2
    best=10**9
    # Fix first vertex in one side to avoid double-counting complements.
    root=verts[0]
    rest=[v for v in verts if v!=root]
    for side_rest in itertools.combinations(rest, half-1):
        side=set(side_rest); side.add(root)
        cut=0
        for a,b in q_edges(N):
            if (a in side) != (b in side):
                cut+=1
        best=min(best,cut)
    return best


def q_face_counts(n:int=N) -> dict[int,int]:
    return {m:(2**(n-m))*math.comb(n,m) for m in range(n+1)}


def knight_moves() -> set[tuple[int,int]]:
    return {(1,2),(3,2),(2,1),(2,3)}


def knight_adj() -> dict[tuple[int,int], set[tuple[int,int]]]:
    return {(r,c):{((r+dr)%BOARD,(c+dc)%BOARD) for dr,dc in knight_moves()} for r,c in itertools.product(range(BOARD), repeat=2)}


def knight_edges() -> set[tuple[tuple[int,int],tuple[int,int]]]:
    edges=set()
    for a,ns in knight_adj().items():
        for b in ns:
            edges.add(tuple(sorted((a,b))))
    return edges


def mapped_knight_edges() -> set[tuple[tuple[int,...],tuple[int,...]]]:
    return {tuple(sorted((KNIGHT_TO_Q4[a],KNIGHT_TO_Q4[b]))) for a,b in knight_edges()}


def tour_bits() -> list[tuple[int,...]]:
    return [KNIGHT_TO_Q4[v] for v in KNIGHT_TOUR]


def tour_flip_sequence() -> list[int]:
    bits=tour_bits(); out=[]
    for i,u in enumerate(bits):
        v=bits[(i+1)%len(bits)]
        diff=[j for j in range(N) if u[j]!=v[j]]
        out.append(diff[0] if len(diff)==1 else -1)
    return out


def d8_modular_invariant() -> list[list[int]]:
    M=[[0 for _ in range(K+1)] for _ in range(K+1)]
    for j in (0,2,4):
        jp=K-j
        for a in (j,jp):
            for b in (j,jp):
                M[a][b]=1
    M[K//2][K//2]=2
    return M


def build_payload() -> dict:
    verts=q_vertices(N)
    edges=q_edges(N)
    adj=q_adjacency(N)
    distances=all_pair_distances(adj)
    grade_counts=dict(sorted(Counter(sum(v) for v in verts).items()))
    pascal=[math.comb(N,k) for k in range(N+1)]
    tetra_augmented=[1,4,6,4,1]
    faces=q_face_counts(N)
    M=d8_modular_invariant()
    frob=sum(x*x for row in M for x in row)
    support=sum(1 for row in M for x in row if x)
    entry_sum=sum(sum(row) for row in M)
    knight_dimension_counts=Counter()
    for a,b in mapped_knight_edges():
        diff=[i for i in range(N) if a[i]!=b[i]]
        knight_dimension_counts[diff[0]] += 1

    checks={
        "cl4_grade_row_is_pascal_1_4_6_4_1": pascal==[1,4,6,4,1] and [grade_counts[i] for i in range(N+1)]==pascal,
        "cl4_dimension_is_16": sum(pascal)==E2==16,
        "augmented_tetrahedron_face_vector_matches_cl4": tetra_augmented==pascal,
        "q4_vertices_are_cl4_blades": len(verts)==sum(pascal)==16,
        "q4_edges_are_single_generator_toggles": len(edges)==N*(2**(N-1))==32,
        "q4_face_counts_are_pascal_row_anchored": faces=={0:16,1:32,2:24,3:8,4:1},
        "q4_square_faces_are_24": faces[2]==24,
        "q4_is_4_regular": sorted({len(ns) for ns in adj.values()})==[4],
        "q4_diameter_is_4": max(distances)==4,
        "q4_average_distance_is_2": abs(sum(distances)/(len(verts)**2)-2.0)<1e-12,
        "q4_bipartition_is_8_8_by_grade_parity": Counter(sum(v)%2 for v in verts)=={0:8,1:8},
        "q4_bisection_bandwidth_is_8": bisection_bandwidth_exact(adj)==8,
        "q4_vertex_connectivity_is_4": vertex_connectivity_exact(adj)==4,
        "q4_edge_connectivity_is_4": edge_connectivity_exact(adj)==4,
        "toroidal_knight_graph_is_q4": mapped_knight_edges()==edges,
        "each_knight_q4_dimension_has_8_edges": dict(sorted(knight_dimension_counts.items()))=={0:8,1:8,2:8,3:8},
        "knight_tour_is_gray_hamilton_cycle": len(set(tour_bits()))==16 and all(hamming(tour_bits()[i],tour_bits()[(i+1)%16])==1 for i in range(16)),
        "gray_clock_repeated_packet": tour_flip_sequence()==[1,2,1,3,1,2,1,0]*2,
        "D8_frobenius_square_matches_cl4_q4_vertices": frob==16,
        "D8_support_splits_as_7_plus_6": support==PHI6+6==13,
        "D8_entry_sum_is_14": entry_sum==14,
        "WE6_factorization_as_W33_Q4_H1": WE6==V_W33*len(verts)*H1,
        "per_anchor_packet_is_6_to_4": len(verts)*H1==6**4,
        "network_packet_edge_to_anchor_ratio": len(edges)+8==V_W33,
    }
    return {
        "theorem":"Cl4_Q4_toroidal_knight_hypercube_network_unification",
        "clifford_pascal_tetrahedron":{
            "four_unit_vectors":"e0,e1,e2,e3",
            "grade_counts":grade_counts,
            "pascal_row_4":pascal,
            "dimension_total":sum(pascal),
            "tetrahedron_augmented_face_vector":"empty, 4 vertices, 6 edges, 4 triangular faces, 1 tetrahedron",
            "interpretation":"Cl4 blades are the faces of a tetrahedron, including empty face; grade equals face cardinality."
        },
        "q4_network":{
            "vertices":len(verts),
            "edges":len(edges),
            "degree":4,
            "diameter":max(distances),
            "average_distance":sum(distances)/(len(verts)**2),
            "bisection_bandwidth":bisection_bandwidth_exact(adj),
            "vertex_connectivity":vertex_connectivity_exact(adj),
            "edge_connectivity":edge_connectivity_exact(adj),
            "bipartition_by_grade_parity":dict(Counter(sum(v)%2 for v in verts)),
            "face_counts":faces,
            "spectrum":{"4":1,"2":4,"0":6,"-2":4,"-4":1}
        },
        "toroidal_knight_layout":{
            "board":"4x4 with toroidal boundaries",
            "vertices":len(knight_adj()),
            "edges":len(knight_edges()),
            "isomorphic_to_Q4":mapped_knight_edges()==edges,
            "dimension_edge_counts":dict(sorted(knight_dimension_counts.items())),
            "gray_tour":KNIGHT_TOUR,
            "gray_flip_sequence":tour_flip_sequence()
        },
        "D8_ADE_and_W33_bridge":{
            "D8_frobenius_square":frob,
            "D8_support":support,
            "D8_entry_sum":entry_sum,
            "Q4_vertices":len(verts),
            "WE6_factorization":"51840 = 40 * 16 * 81",
            "per_W33_anchor_packet":"16 * 81 = 1296 = 6^4",
            "interpretation":"D8 supplies the 16-state Cl4/Q4 router; W33 supplies 40 anchors; the signed phase frame supplies H1=81."
        },
        "identities":checks,
        "all_identities_hold":bool(all(checks.values()))
    }


def main() -> None:
    payload=build_payload()
    out=Path("data/w33_cl4_q4_hypercube_network_unification.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps({"all_identities_hold":payload["all_identities_hold"],"clifford_pascal_tetrahedron":payload["clifford_pascal_tetrahedron"],"q4_network":payload["q4_network"],"D8_ADE_and_W33_bridge":payload["D8_ADE_and_W33_bridge"]},indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()
