#!/usr/bin/env python3
"""BT546: W33 Levi Cycle Phase-Frame Unification Theorem.

This continues BT545.

BT545 proved that the point-line Levi graph L of W(3,3) has:

    |V(L)| = 80,
    |E(L)| = 160,
    beta_1(L) = 81,
    # simple 8-cycles = 1620,
    each flag-edge in 81 simple 8-cycles.

This theorem shows that the previous minimal-logical overlap, dual visibility,
and signed phase-frame theorems are all the same Levi edge-cycle incidence
object.

Let B be the unsigned incidence matrix:

    B[e,c] = 1 iff Levi flag-edge e lies in simple 8-cycle c.

Then B is 160 x 1620 and

    diag(BB^T) = 81,
    offdiag(BB^T) in {1,3,9,27}

with row profile

    1^81, 3^54, 9^18, 27^6.

This is the previous 3-adic minimal-X overlap scheme, now derived from Levi
cycle geometry.

Let C be the oriented edge-cycle incidence matrix:

    C[e,c] = +1/-1 according to the orientation of e inside c,
             0 if e is not in c.

Then

    CC^T has spectrum 160^81 + 0^79,
    (CC^T)^2 = 160 CC^T.

Thus (1/160) CC^T is the exact rank-81 protected H_1 projector.  The signed
phase-frame theorem is precisely the oriented simple-8-cycle frame of the
W33 point-line Levi graph.

On the cycle side, B^T B has diagonal 8 and off-diagonal profile:

    0^1187, 1^288, 2^96, 3^32, 4^16 per cycle,

which is the previous dual Z-visibility scheme.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

MOD = 3
V_W33 = 40
K_W33 = 12
W33_EDGES = 240
LINES_W33 = 40
POINTS_PER_LINE = 4
LEVI_VERTICES = 80
LEVI_EDGES = 160
CYCLES8 = 1620
H1 = 81
WE6 = 51840


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % MOD for x in v)
    for a in v:
        if a % MOD:
            inv = 1 if a == 1 else 2
            return tuple((x * inv) % MOD for x in v)
    raise ValueError("zero vector")


def symplectic(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % MOD


def build_w33() -> tuple[nx.Graph, list[tuple[int, int, int, int]]]:
    points = sorted(
        {canonical_projective(v) for v in itertools.product(range(MOD), repeat=4) if any(v)}
    )
    g = nx.Graph()
    g.add_nodes_from(points)
    for i, u in enumerate(points):
        for v in points[i + 1 :]:
            if symplectic(u, v) == 0:
                g.add_edge(u, v)
    return g, points


def build_levi(g: nx.Graph, points: list[tuple[int, int, int, int]]) -> tuple[nx.Graph, list[tuple]]:
    lines = sorted(set(tuple(sorted(c)) for c in nx.find_cliques(g) if len(c) == POINTS_PER_LINE))
    p_index = {p: i for i, p in enumerate(points)}
    levi = nx.Graph()
    levi.add_nodes_from(range(len(points) + len(lines)))
    for li, line in enumerate(lines):
        for p in line:
            levi.add_edge(p_index[p], len(points) + li)
    return levi, lines


def canonical_cycle(path: list[int]) -> tuple[int, ...]:
    rots = []
    for seq in (path, list(reversed(path))):
        for i in range(len(seq)):
            rots.append(tuple(seq[i:] + seq[:i]))
    return min(rots)


def simple_cycles_fixed_length(g: nx.Graph, k: int) -> list[tuple[int, ...]]:
    cycles: set[tuple[int, ...]] = set()
    for start in g.nodes():
        stack = [(start, [start], {start})]
        while stack:
            u, path, seen = stack.pop()
            if len(path) == k:
                if g.has_edge(u, start):
                    cycles.add(canonical_cycle(path))
                continue
            for w in g.neighbors(u):
                if w == start:
                    continue
                if w not in seen:
                    stack.append((w, path + [w], seen | {w}))
    return sorted(cycles)


def edge_set(cyc: tuple[int, ...]) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted((a, b))) for a, b in zip(cyc, cyc[1:] + cyc[:1]))


def eigen_counter(mat: np.ndarray, radicals: bool = False) -> dict[str, int]:
    vals = np.linalg.eigvalsh(mat.astype(float))
    out: Counter[str] = Counter()
    for x in vals:
        if abs(x) < 1e-7:
            key = "0"
        elif abs(x - 160) < 1e-7:
            key = "160"
        elif abs(x - 648) < 1e-7:
            key = "648"
        elif abs(x - 72) < 1e-7:
            key = "72"
        elif abs(x - 40) < 1e-7:
            key = "40"
        elif abs(x - (144 + 36 * math.sqrt(6))) < 1e-7:
            key = "144+36sqrt6"
        elif abs(x - (144 - 36 * math.sqrt(6))) < 1e-7:
            key = "144-36sqrt6"
        else:
            key = f"{x:.12g}"
        out[key] += 1
    return dict(sorted(out.items()))


def as_plain_counter(counter: Counter) -> dict[str, int]:
    return {str(int(k)): int(v) for k, v in sorted(counter.items(), key=lambda kv: int(kv[0]))}


def main() -> dict:
    w33, points = build_w33()
    levi, lines = build_levi(w33, points)

    cycles = simple_cycles_fixed_length(levi, 8)
    levi_edges = sorted(tuple(sorted(e)) for e in levi.edges())
    edge_index = {e: i for i, e in enumerate(levi_edges)}

    B = np.zeros((len(levi_edges), len(cycles)), dtype=int)
    C = np.zeros((len(levi_edges), len(cycles)), dtype=int)
    cycle_edges = []

    for j, cyc in enumerate(cycles):
        es = edge_set(cyc)
        cycle_edges.append(es)
        for e in es:
            B[edge_index[e], j] = 1
        # Orient each canonical cycle in its listed order.  Orient each Levi edge
        # from lower integer label to higher integer label.
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            e = tuple(sorted((a, b)))
            sign = 1 if (a, b) == e else -1
            C[edge_index[e], j] = sign

    BBt = B @ B.T
    CCt = C @ C.T
    BtB = B.T @ B

    unsigned_off = Counter(BBt[np.triu_indices(LEVI_EDGES, 1)])
    signed_off = Counter(CCt[np.triu_indices(LEVI_EDGES, 1)])

    # Per-row X-side 3-adic profile.
    unsigned_row_profiles = []
    signed_row_profiles = []
    for i in range(LEVI_EDGES):
        unsigned_row_profiles.append(Counter(BBt[i, j] for j in range(LEVI_EDGES) if j != i))
        signed_row_profiles.append(Counter(CCt[i, j] for j in range(LEVI_EDGES) if j != i))
    assert len(set(tuple(sorted(p.items())) for p in unsigned_row_profiles)) == 1
    assert len(set(tuple(sorted(p.items())) for p in signed_row_profiles)) == 1
    unsigned_row_profile = unsigned_row_profiles[0]
    signed_row_profile = signed_row_profiles[0]

    # Cycle-side Z-visibility profile.
    cycle_overlap_profiles = []
    for i in range(CYCLES8):
        cycle_overlap_profiles.append(Counter(BtB[i, j] for j in range(CYCLES8) if j != i))
    assert len(set(tuple(sorted(p.items())) for p in cycle_overlap_profiles)) == 1
    cycle_overlap_profile = cycle_overlap_profiles[0]

    # Projector checks for signed phase frame.
    CCt2 = CCt @ CCt
    projector_identity_holds = np.array_equal(CCt2, 160 * CCt)
    signed_rank = int(np.linalg.matrix_rank(CCt))
    unsigned_rank = int(np.linalg.matrix_rank(BBt))

    checks = {
        "w33_srg_size": w33.number_of_nodes() == V_W33 and w33.number_of_edges() == W33_EDGES,
        "w33_lines_40": len(lines) == LINES_W33,
        "levi_size": levi.number_of_nodes() == LEVI_VERTICES and levi.number_of_edges() == LEVI_EDGES,
        "levi_beta1_81": levi.number_of_edges() - levi.number_of_nodes() + 1 == H1,
        "simple_8_cycles_1620": len(cycles) == CYCLES8,
        "B_shape_160_by_1620": B.shape == (LEVI_EDGES, CYCLES8),
        "C_shape_160_by_1620": C.shape == (LEVI_EDGES, CYCLES8),
        "B_row_weight_81": set(B.sum(axis=1)) == {H1},
        "B_col_weight_8": set(B.sum(axis=0)) == {8},
        "C_absolute_is_B": np.array_equal(np.abs(C), B),
        "unsigned_row_profile_3_adic": unsigned_row_profile == Counter({1: 81, 3: 54, 9: 18, 27: 6}),
        "signed_row_profile_phase": signed_row_profile == Counter({1: 81, -3: 54, 9: 18, -27: 6}),
        "cycle_side_dual_visibility": cycle_overlap_profile == Counter({0: 1187, 1: 288, 2: 96, 3: 32, 4: 16}),
        "unsigned_spectrum_matches_prior": eigen_counter(BBt) == {"144+36sqrt6": 24, "144-36sqrt6": 24, "40": 81, "648": 1, "72": 30},
        "signed_spectrum_projector": eigen_counter(CCt) == {"0": 79, "160": 81},
        "signed_rank_81": signed_rank == H1,
        "unsigned_rank_160": unsigned_rank == LEVI_EDGES,
        "projector_identity": projector_identity_holds,
        "phase_frame_projector": projector_identity_holds and signed_rank == H1,
        "E6_vector_identity": 320 * 162 == WE6,
    }

    result = {
        "theorem": "BT546 W33 Levi Cycle Phase-Frame Unification Theorem",
        "construction": {
            "W33": "symplectic polar graph on projective points of F_3^4",
            "Levi_graph": "point-line incidence graph of W(3,3)",
            "B": "unsigned edge-by-8-cycle incidence matrix",
            "C": "oriented edge-by-8-cycle incidence matrix",
        },
        "objects": {
            "w33_vertices": w33.number_of_nodes(),
            "w33_edges": w33.number_of_edges(),
            "w33_lines": len(lines),
            "levi_vertices": levi.number_of_nodes(),
            "levi_edges_flags": levi.number_of_edges(),
            "levi_beta1": levi.number_of_edges() - levi.number_of_nodes() + 1,
            "simple_8_cycles": len(cycles),
        },
        "unsigned_X_side": {
            "matrix": "B B^T",
            "diagonal": int(BBt[0, 0]),
            "offdiag_global_profile": as_plain_counter(unsigned_off),
            "per_row_profile": as_plain_counter(unsigned_row_profile),
            "spectrum": eigen_counter(BBt),
            "reading": "The previous 3-adic minimal-X overlap scheme is the unsigned overlap of Levi flag-edges through simple 8-cycles.",
        },
        "signed_phase_frame": {
            "matrix": "C C^T",
            "diagonal": int(CCt[0, 0]),
            "offdiag_global_profile": {str(int(k)): int(v) for k, v in sorted(signed_off.items(), key=lambda kv: int(kv[0]))},
            "per_row_profile": {str(int(k)): int(v) for k, v in sorted(signed_row_profile.items(), key=lambda kv: int(kv[0]))},
            "spectrum": eigen_counter(CCt),
            "rank": signed_rank,
            "projector_identity": "(C C^T)^2 = 160 C C^T",
            "projector": "(1/160) C C^T is an exact rank-81 projector",
            "reading": "The previous signed phase-frame theorem is the oriented cycle-space frame of the W33 Levi graph.",
        },
        "cycle_Z_side": {
            "matrix": "B^T B",
            "diagonal": int(BtB[0, 0]),
            "per_cycle_overlap_profile": as_plain_counter(cycle_overlap_profile),
            "global_unordered_pair_profile": {
                "0": 961470,
                "1": 233280,
                "2": 77760,
                "3": 25920,
                "4": 12960,
            },
            "reading": "The previous dual Z-visibility scheme is the cycle-intersection profile of Levi simple 8-cycles.",
        },
        "unification": {
            "support_identity": "160*81 = 1620*8 = 12960",
            "phase_projector_identity": "spec(C C^T)=160^81 + 0^79",
            "E6_vector_identity": "320*162 = 51840 = |W(E6)|",
            "compressed_statement": "Minimal logical support incidence, 3-adic overlap, dual Z-visibility, and signed H1 phase frame are all shadows of the same W33 Levi edge-cycle incidence geometry.",
        },
        "all_identities": checks,
        "all_identities_hold": all(checks.values()),
    }

    out = Path("data/PART_BT546_W33_LEVI_CYCLE_PHASE_FRAME_UNIFICATION_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"wrote {out}")
    return result


if __name__ == "__main__":
    main()
