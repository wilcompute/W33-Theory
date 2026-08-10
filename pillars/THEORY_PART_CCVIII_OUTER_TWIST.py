#!/usr/bin/env python3
"""Pillar 108 (Part CCVIII): Outer Twist on E8 Roots and PG(3,3) Geometry

The 4x4 matrix N4 over F_3 induces an outer automorphism of order 8 on the
40 PG(3,3) points.  N4 is NOT symplectic: the twisted form Omega' = N4^T *
Omega * N4 differs from Omega.  The comparison of two isomorphisms from Omega'
to Omega (one given by N4, one by an explicit symplectic Q) produces an inner
residual a = Q * N4^{-1} in Sp(4,3) of order 6.

This inner residual a acts on the 40 PG(3,3) points and simultaneously on the
240 E8 roots (as a Weyl group element), with explicit cycle structures.  On the
27 affine points AG(3,3) (the Heisenberg F_3^3 sector), a decomposes into 5
orbits of sizes {8,8,8,1,2}.  On the 240 edges of the W(3,3) collinearity
graph, a has 34 orbits with sizes in {4,8}.

Theorems:

T1  OUTER TWIST ORDER 8: N4 (4x4 over F_3) induces a permutation p of order 8
    on the 40 PG(3,3) points.  N4 is NOT symplectic: Omega' = N4^T Omega N4
    satisfies Omega' ≠ Omega (as 4x4 matrices mod 3).

T2  INNER RESIDUAL ORDER 6: There exists a symplectic matrix Q with
    Q^T Omega Q = Omega'.  The inner residual a = Q N4^{-1} (mod scalars)
    lies in Sp(4,3) with order 6.  a satisfies Q = a * N4 (projectively).

T3  VERTEX CYCLE STRUCTURE: a acts on the 40 PG(3,3) points with cycle
    structure {1:2, 2:1, 3:2, 6:5} — exactly 2 fixed points, 1 transposition,
    2 three-cycles, and 5 six-cycles.  Total: 2+2+6+30 = 40.

T4  E8 ROOT CYCLE STRUCTURE: a acts on the 240 E8 roots with cycle structure
    {1:2, 2:2, 3:10, 6:34} — 2 fixed roots, 2 transpositions, 10 three-cycles,
    34 six-cycles.  Total: 2+4+30+204 = 240.

T5  AFFINE HEISENBERG ORBITS: On the 27 affine points AG(3,3) inside PG(3,3)
    (the Heisenberg sector F_3^3), the outer twist has exactly 5 orbits with
    size distribution {1:1, 2:1, 8:3} — one fixed point, one transposition,
    and three 8-element orbits.  Total: 1+2+24 = 27.

T6  EDGE ORBIT STRUCTURE: The outer twist has exactly 34 orbits on the 240
    edges of the W(3,3) collinearity graph (SRG(40,12,2,4)).  All orbit sizes
    are in {4, 8}: exactly 8 orbits of size 4 and 26 orbits of size 8.
    Total edges: 8*4 + 26*8 = 32+208 = 240.
"""

from __future__ import annotations

import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
BUNDLE_E8 = ROOT / "OUTER_TWIST_ON_E8_ROOTS_CERTIFICATE_BUNDLE_v01.zip"
BUNDLE_PG = ROOT / "PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01.zip"


def _matmul_mod3(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
    n = len(A)
    return [
        [sum(A[i][k] * B[k][j] for k in range(n)) % 3 for j in range(n)]
        for i in range(n)
    ]


def _transp(M: List[List[int]]) -> List[List[int]]:
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]


def _int_mat(M) -> List[List[int]]:
    return [[int(x) % 3 for x in row] for row in M]


def _perm_order(perm: List[int], max_order: int = 200) -> int:
    n = len(perm)
    cur = list(range(n))
    for k in range(1, max_order + 1):
        cur = [cur[perm[i]] for i in range(n)]
        if cur == list(range(n)):
            return k
    return -1


def _cycle_struct(perm: List[int]) -> dict:
    visited = [False] * len(perm)
    counts: Counter = Counter()
    for start in range(len(perm)):
        if not visited[start]:
            length = 0
            pos = start
            while not visited[pos]:
                visited[pos] = True
                pos = perm[pos]
                length += 1
            counts[length] += 1
    return dict(sorted(counts.items()))


def _load_e8_bundle() -> dict:
    with zipfile.ZipFile(BUNDLE_E8) as zf:
        summary = json.loads(zf.read("summary.json"))
        defects = json.loads(zf.read("isometry_defect_stats.json"))
    return {"summary": summary, "defects": defects}


def _load_pg_bundle() -> dict:
    with zipfile.ZipFile(BUNDLE_PG) as zf:
        outer_matrix = json.loads(zf.read("outer_matrix.json"))
        outer_orbits = json.loads(zf.read("outer_orbits.json"))
        edge_orbits = json.loads(zf.read("edge_orbits.json"))
        perm40 = json.loads(zf.read("perm40_from_canonical.json"))
        symp_form = json.loads(zf.read("symplectic_form.json"))
    return {
        "outer_matrix": outer_matrix,
        "outer_orbits": outer_orbits,
        "edge_orbits": edge_orbits,
        "perm40": perm40,
        "symp_form": symp_form,
    }


def analyze() -> dict:
    e8 = _load_e8_bundle()
    pg = _load_pg_bundle()
    s = e8["summary"]

    # T1: Outer twist order and non-symplectic nature
    N4 = _int_mat(s["outer_matrix_N4_mod3"])
    Omega = _int_mat(s["symplectic_form_Omega_mod3"])
    Omega_prime = _int_mat(s["twisted_form_Omega_prime = N4^T Omega N4"])
    perm_p = s["outer_point_perm_p"]

    # Verify N4^T Omega N4 = Omega'
    N4t = _transp(N4)
    N4t_Omega = _matmul_mod3(N4t, Omega)
    computed_Omega_prime = _matmul_mod3(N4t_Omega, N4)
    t1_twisted_form_correct = (computed_Omega_prime == Omega_prime)
    t1_not_symplectic = (Omega_prime != Omega)
    t1_order_p = s["orders"]["order_p (outer on points in PG coords)"]

    # Verify perm_p has order 8 by computing it ourselves
    computed_order_p = _perm_order(perm_p, max_order=16)
    t1_computed_order_matches = (computed_order_p == t1_order_p)

    # T2: Inner residual order 6
    Q = _int_mat(s["isomorphism_Q_with_Omega_prime = Q^T Omega Q"])
    A4 = _int_mat(s["inner_symplectic_matrix_A4 = Q * N4^{-1} (projectively)"])

    # Verify Q^T Omega Q = Omega' (Q isomorphism check)
    Qt = _transp(Q)
    Qt_Omega = _matmul_mod3(Qt, Omega)
    Qt_Omega_Q = _matmul_mod3(Qt_Omega, Q)
    t2_Q_preserves_Omega_prime = (Qt_Omega_Q == Omega_prime)

    t2_order_a = s["orders"]["order_a (inner symplectic residual)"]

    # T3: Vertex cycle structure of a on 40 PG(3,3) points
    # From summary (computed by bundle maker from vertex_cycles_a.csv)
    raw_vertex_cs = s["cycle_structure_vertices_a"]
    t3_cycle_struct = {int(k): v for k, v in raw_vertex_cs.items()}
    t3_total_pts = sum(length * count for length, count in t3_cycle_struct.items())
    t3_fixed = t3_cycle_struct.get(1, 0)
    t3_correct = (
        t3_total_pts == 40
        and t3_fixed == 2
        and t3_cycle_struct.get(2, 0) == 1
        and t3_cycle_struct.get(3, 0) == 2
        and t3_cycle_struct.get(6, 0) == 5
    )
    t3_fixed_vertices = s["fixed_vertices_a"]
    t3_two_cycle = s["two_cycle_vertices_a"]

    # T4: Root cycle structure on 240 E8 roots
    raw_root_cs = s["cycle_structure_roots_under_a"]
    t4_cycle_struct = {int(k): v for k, v in raw_root_cs.items()}
    t4_total_roots = sum(length * count for length, count in t4_cycle_struct.items())
    t4_fixed_roots = t4_cycle_struct.get(1, 0)
    t4_correct = (
        t4_total_roots == 240
        and t4_fixed_roots == 2
        and t4_cycle_struct.get(2, 0) == 2
        and t4_cycle_struct.get(3, 0) == 10
        and t4_cycle_struct.get(6, 0) == 34
    )
    t4_fixed_root_vectors = s["fixed_roots_under_a"]

    # T5: Affine Heisenberg orbits (27 affine points)
    outer_orbits = pg["outer_orbits"]
    affine_orbit_sizes = [len(o) for o in outer_orbits]
    affine_size_dist = dict(sorted(Counter(affine_orbit_sizes).items()))
    t5_num_orbits = len(outer_orbits)
    t5_total_affine = sum(affine_orbit_sizes)
    t5_correct = (
        t5_num_orbits == 5
        and t5_total_affine == 27
        and affine_size_dist == {1: 1, 2: 1, 8: 3}
    )

    # T6: Edge orbit structure on 240 W(3,3) collinearity edges
    edge_orbits = pg["edge_orbits"]
    edge_sizes = [len(o) for o in edge_orbits]
    edge_size_dist = dict(sorted(Counter(edge_sizes).items()))
    t6_num_orbits = len(edge_orbits)
    t6_total_edges = sum(edge_sizes)
    t6_correct = (
        t6_num_orbits == 34
        and t6_total_edges == 240
        and edge_size_dist == {4: 8, 8: 26}
    )

    # Adjacency defect stats
    defects = e8["defects"]
    adj_preservation_rate = defects["adjacency_preservation_rate"]

    return {
        "T1_order_p": t1_order_p,
        "T1_computed_order_p": computed_order_p,
        "T1_order_p_matches": t1_computed_order_matches,
        "T1_not_symplectic": t1_not_symplectic,
        "T1_twisted_form_correct": t1_twisted_form_correct,
        "T2_order_a": t2_order_a,
        "T2_Q_isomorphism_correct": t2_Q_preserves_Omega_prime,
        "T3_vertex_cycle_struct": t3_cycle_struct,
        "T3_total_pts": t3_total_pts,
        "T3_fixed_count": t3_fixed,
        "T3_correct": t3_correct,
        "T3_fixed_vertices": t3_fixed_vertices,
        "T3_two_cycle_vertices": t3_two_cycle,
        "T4_root_cycle_struct": t4_cycle_struct,
        "T4_total_roots": t4_total_roots,
        "T4_fixed_root_count": t4_fixed_roots,
        "T4_correct": t4_correct,
        "T4_fixed_root_vectors": t4_fixed_root_vectors,
        "T5_num_affine_orbits": t5_num_orbits,
        "T5_total_affine_pts": t5_total_affine,
        "T5_affine_orbit_size_dist": affine_size_dist,
        "T5_correct": t5_correct,
        "T6_num_edge_orbits": t6_num_orbits,
        "T6_total_edges": t6_total_edges,
        "T6_edge_size_dist": edge_size_dist,
        "T6_correct": t6_correct,
        "adjacency_preservation_rate": adj_preservation_rate,
    }


def main():
    summary = analyze()
    out = ROOT / "data" / "w33_outer_twist.json"
    out.write_text(__import__("json", encoding="utf-8").dumps(summary, indent=2))
    print("T1 outer twist order p:", summary["T1_order_p"],
          "  not symplectic:", summary["T1_not_symplectic"])
    print("T2 inner residual order a:", summary["T2_order_a"],
          "  Q isomorphism correct:", summary["T2_Q_isomorphism_correct"])
    print("T3 vertex cycle struct:", summary["T3_vertex_cycle_struct"],
          "  total=", summary["T3_total_pts"])
    print("T3 correct:", summary["T3_correct"])
    print("T4 root cycle struct:", summary["T4_root_cycle_struct"],
          "  total=", summary["T4_total_roots"])
    print("T4 correct:", summary["T4_correct"])
    print("T5 affine orbits:", summary["T5_num_affine_orbits"],
          "  size dist:", summary["T5_affine_orbit_size_dist"],
          "  correct:", summary["T5_correct"])
    print("T6 edge orbits:", summary["T6_num_edge_orbits"],
          "  size dist:", summary["T6_edge_size_dist"],
          "  correct:", summary["T6_correct"])
    print("wrote data/w33_outer_twist.json")


if __name__ == "__main__":
    main()
