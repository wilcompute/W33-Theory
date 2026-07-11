#!/usr/bin/env python3
"""Pass 165: the doily's trade lattice and the fusion with the Pass-71 codes.

The doily track (Passes 70-76) built the [15,5,5] spread code and its dual
[15,10,3] on W(2,2).  The chiral program (Passes 158-163) built trade
lattices from incidence kernels.  This witness applies the trade
construction to the doily and identifies exactly how the two tracks'
objects coincide:

1. THE DOILY TRADE LATTICE.  W(2,2) = GQ(2,2), SRG(15,6,1,3), spectrum
   {6, 1^9, (-3)^5}.  Its integer trade lattice (zero sum on all 15
   lines) has rank 5, with exact Gram data and minimal shell computed;
   the span/perp double-threes of the 60 hyperbolic pairs and the ovoid
   differences (W(2,2) has ovoids because q = 2 is even; A*1_O = 3j -
   3*1_O, so ovoid differences are integral (-3)-eigenvectors = trades)
   are located inside it.

2. THE F2 FUSION.  In line space, the 6 spreads span the [15,5,5] code
   (re-derived independently); in point space the 6 ovoids span its dual
   twin.  The exact subspace relations between {incidence kernel,
   incidence row space, spread code, ovoid code, their duals} are
   computed -- the fusion dictionary between the two tracks.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import sys

import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)

OUT = ROOT / "data" / "w33_pass165_doily_trade_fusion.json"


def build_doily():
    points = sorted(v for v in product(range(2), repeat=4) if any(v))

    def symp(x, y):
        return (x[0] * y[2] + x[2] * y[0] + x[1] * y[3] + x[3] * y[1]) % 2

    adjacency = np.zeros((15, 15), dtype=np.int64)
    for a, b in combinations(range(15), 2):
        if symp(points[a], points[b]) == 0:
            adjacency[a, b] = adjacency[b, a] = 1
    lines = [
        frozenset(t)
        for t in combinations(range(15), 3)
        if all(adjacency[x, y] for x, y in combinations(t, 2))
    ]
    return points, adjacency, lines


def f2_rank(matrix):
    work = [row.copy() for row in matrix.astype(np.uint8)]
    rank = 0
    for col in range(work[0].shape[0] if len(work) else 0):
        pivot = next((r for r in range(rank, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for r in range(len(work)):
            if r != rank and work[r][col]:
                work[r] = work[r] ^ work[rank]
        rank += 1
    return rank


def f2_span_basis(rows):
    basis = []
    for row in rows:
        residual = row.copy().astype(np.uint8)
        for b in basis:
            pivot = int(np.flatnonzero(b)[0])
            if residual[pivot]:
                residual = residual ^ b
        if residual.any():
            # keep basis reduced with leading-one pivots
            basis.append(residual)
            basis.sort(key=lambda v: int(np.flatnonzero(v)[0]))
            # re-reduce
            changed = True
            while changed:
                changed = False
                for i in range(len(basis)):
                    for j in range(len(basis)):
                        if i == j:
                            continue
                        pivot = int(np.flatnonzero(basis[j])[0])
                        if basis[i][pivot]:
                            basis[i] = basis[i] ^ basis[j]
                            changed = True
                basis = [b for b in basis if b.any()]
                basis.sort(key=lambda v: int(np.flatnonzero(v)[0]))
    return basis


def subspace_key(basis):
    return tuple(sorted(tuple(int(x) for x in b) for b in basis))


def intersection_dim(basis_a, basis_b, length=15):
    """dim(A cap B) = dim A + dim B - dim(A+B) over F2."""
    stacked = np.array(list(basis_a) + list(basis_b), dtype=np.uint8)
    if stacked.size == 0:
        return 0
    dim_sum = f2_rank(stacked)
    return len(basis_a) + len(basis_b) - dim_sum


def enumerate_code(basis):
    basis = np.array(basis, dtype=np.uint8)
    k = basis.shape[0]
    coeffs = np.array(
        [[(m >> b) & 1 for b in range(k)] for m in range(2**k)], dtype=np.uint8
    )
    return (coeffs @ basis) % 2


def weight_enumerator(words):
    return Counter(int(w) for w in words.sum(axis=1))


def main():
    points, adjacency, lines = build_doily()
    checks = {}

    checks["fifteen_points_fifteen_lines"] = len(points) == 15 and len(lines) == 15
    a2 = adjacency @ adjacency
    srg_ok = bool((adjacency.sum(axis=1) == 6).all())
    for a, b in combinations(range(15), 2):
        expected = 1 if adjacency[a, b] else 3
        if a2[a, b] != expected:
            srg_ok = False
    checks["doily_srg_15_6_1_3"] = srg_ok

    incidence = np.zeros((15, 15), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            incidence[row, p] = 1

    # ------------------------------------------------------------------
    # 1. the integer trade lattice
    # ------------------------------------------------------------------
    trade = generic_saturated_kernel(incidence)
    checks["doily_trade_rank_5"] = trade.shape == (15, 5)
    checks["trade_is_minus3_eigenspace"] = bool(
        np.array_equal(adjacency @ trade, -3 * trade)
    )
    gram = Matrix((trade.T @ trade).tolist())
    smith = smith_normal_form(gram, domain=ZZ)
    invariants = [abs(int(smith[i, i])) for i in range(5)]
    determinant = int(gram.det())
    is_even = bool(all(int(gram[i, i]) % 2 == 0 for i in range(5)))

    min_norm, shell = staged_minimal_shell(trade)
    shell = [np.asarray(v, dtype=np.int64) for v in shell]
    support_sizes = Counter(int(np.count_nonzero(v)) for v in shell)
    value_profiles = Counter(
        tuple(sorted(Counter(int(x) for x in v if x).items())) for v in shell
    )

    hyperbolic = [(a, b) for a, b in combinations(range(15), 2) if not adjacency[a, b]]
    checks["sixty_hyperbolic_pairs"] = len(hyperbolic) == 60

    # ovoids: 5-point cocliques meeting every line once
    ovoids = [
        frozenset(c)
        for c in combinations(range(15), 5)
        if not any(adjacency[x, y] for x, y in combinations(c, 2))
    ]
    checks["six_ovoids"] = len(ovoids) == 6
    ovoid_vectors = np.zeros((len(ovoids), 15), dtype=np.int64)
    for n, ovoid in enumerate(ovoids):
        for p in ovoid:
            ovoid_vectors[n, p] = 1
    checks["ovoid_eigen_relation"] = all(
        np.array_equal(
            adjacency @ ovoid_vectors[n],
            3 * np.ones(15, dtype=np.int64) - 3 * ovoid_vectors[n],
        )
        for n in range(len(ovoids))
    )
    ovoid_diffs = [
        ovoid_vectors[i] - ovoid_vectors[j]
        for i, j in combinations(range(len(ovoids)), 2)
    ]
    checks["ovoid_differences_are_trades"] = all(
        np.array_equal(adjacency @ d, -3 * d) for d in ovoid_diffs
    )
    diff_norms = Counter(int(d @ d) for d in ovoid_diffs)
    ovoid_pair_meets = Counter(len(a & b) for a, b in combinations(ovoids, 2))

    # are the minimal trades exactly the ovoid differences?
    shell_set = {tuple(int(x) for x in v) for v in shell}
    diff_set = {tuple(int(x) for x in d) for d in ovoid_diffs} | {
        tuple(int(-x) for x in d) for d in ovoid_diffs
    }
    minimal_are_ovoid_diffs = shell_set == diff_set

    # span/perp candidates
    span_perp_in_shell = 0
    for a, b in hyperbolic:
        perp = np.flatnonzero(adjacency[a] & adjacency[b])
        mask = np.ones(15, dtype=bool)
        for p in perp:
            mask &= adjacency[p].astype(bool)
        span = np.flatnonzero(mask)
        vector = np.zeros(15, dtype=np.int64)
        vector[span] = 1
        vector[perp] -= 1
        if tuple(int(x) for x in vector) in shell_set:
            span_perp_in_shell += 1

    # ------------------------------------------------------------------
    # 2. the F2 fusion with the Pass-71 codes
    # ------------------------------------------------------------------
    r2 = f2_rank(incidence.astype(np.uint8))

    # spreads: 5 pairwise-disjoint lines
    spreads = []
    for combo in combinations(range(15), 5):
        union = set()
        ok = True
        for l in combo:
            if union & lines[l]:
                ok = False
                break
            union |= lines[l]
        if ok:
            spreads.append(frozenset(combo))
    checks["six_spreads"] = len(spreads) == 6
    spread_vectors = np.zeros((len(spreads), 15), dtype=np.uint8)
    for n, spread in enumerate(spreads):
        for l in spread:
            spread_vectors[n, l] = 1

    spread_basis = f2_span_basis([spread_vectors[n] for n in range(len(spreads))])
    spread_words = enumerate_code(spread_basis)
    spread_enum = weight_enumerator(spread_words)
    spread_min = min(w for w in spread_enum if w > 0)
    checks["spread_code_15_5_5"] = len(spread_basis) == 5 and spread_min == 5

    # dual of the spread code (their [15,10,3])
    all_words = np.array(
        [[(m >> b) & 1 for b in range(15)] for m in range(2**15)], dtype=np.uint8
    )
    in_dual = ((all_words @ np.array(spread_basis).T) % 2 == 0).all(axis=1)
    dual_words = all_words[in_dual]
    dual_enum = weight_enumerator(dual_words)
    dual_min = min(w for w in dual_enum if w > 0)
    checks["spread_dual_15_10_3"] = len(dual_words) == 2**10 and dual_min == 3

    # code family in LINE space
    pencil_rows = [
        np.array([1 if p in lines[l] else 0 for l in range(15)], dtype=np.uint8)
        for p in range(15)
    ]  # rows of N^T: lines through each point
    r_l_basis = f2_span_basis(pencil_rows)
    # kernel of N^T over F2: line-vectors with zero sum over every pencil
    nt = incidence.T.astype(np.uint8)
    # solve nt @ y = 0: kernel via rref
    work = [nt[r].copy() for r in range(15)]
    pivots = []
    row = 0
    for col in range(15):
        pivot = next((r for r in range(row, len(work)) if work[r][col]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        for r in range(len(work)):
            if r != row and work[r][col]:
                work[r] = work[r] ^ work[row]
        pivots.append(col)
        row += 1
    free_cols = [c for c in range(15) if c not in pivots]
    k_l_basis = []
    for fc in free_cols:
        vec = np.zeros(15, dtype=np.uint8)
        vec[fc] = 1
        for r, pc in zip(work[: len(pivots)], pivots):
            if r[fc]:
                vec[pc] = 1
        k_l_basis.append(vec)
    k_l_basis = f2_span_basis(k_l_basis)
    checks["line_kernel_dim"] = len(k_l_basis) == 15 - r2

    # ovoid code in POINT space and the point-space kernel
    ovoid_basis = f2_span_basis(
        [ovoid_vectors[n].astype(np.uint8) for n in range(len(ovoids))]
    )
    trade_f2_basis = f2_span_basis(
        [(trade[:, c] % 2).astype(np.uint8) for c in range(5)]
    )

    ovoid_diff_basis = f2_span_basis(
        [
            (ovoid_vectors[i] ^ ovoid_vectors[j]).astype(np.uint8)
            for i, j in combinations(range(len(ovoids)), 2)
        ]
    )

    relations = {
        "rank2_incidence": r2,
        "point_kernel_dim": len(trade_f2_basis),
        "line_kernel_dim": len(k_l_basis),
        "spread_code_dim": len(spread_basis),
        "ovoid_code_dim": len(ovoid_basis),
        "ovoid_diff_code_dim": len(ovoid_diff_basis),
        "spread_cap_line_kernel": intersection_dim(spread_basis, k_l_basis),
        "ovoid_cap_point_kernel": intersection_dim(ovoid_basis, trade_f2_basis),
        "ovoid_diff_inside_point_kernel": intersection_dim(
            ovoid_diff_basis, trade_f2_basis
        )
        == len(ovoid_diff_basis),
        "spread_code_equals_line_kernel": subspace_key(spread_basis)
        == subspace_key(k_l_basis),
        "ovoid_code_equals_point_kernel": subspace_key(ovoid_basis)
        == subspace_key(trade_f2_basis),
    }

    point_kernel_words = enumerate_code(trade_f2_basis)
    point_kernel_enum = weight_enumerator(point_kernel_words)

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass165.doily_trade_fusion.v1",
        "status": "PASS" if all_pass else "FAIL",
        "trade_lattice": {
            "rank": 5,
            "determinant": determinant,
            "smith_invariants": invariants,
            "even": is_even,
            "minimal_norm": int(min_norm),
            "shell_size": len(shell),
            "support_sizes": {str(k): int(v) for k, v in sorted(support_sizes.items())},
            "value_profiles": {
                str(dict(p)): int(c) for p, c in sorted(value_profiles.items())
            },
            "minimal_trades_are_ovoid_differences": bool(minimal_are_ovoid_diffs),
            "span_perp_vectors_in_shell": span_perp_in_shell,
            "ovoid_difference_norms": {
                str(k): int(v) for k, v in sorted(diff_norms.items())
            },
            "ovoid_pair_intersections": {
                str(k): int(v) for k, v in sorted(ovoid_pair_meets.items())
            },
        },
        "f2_fusion": {
            **{
                k: (int(v) if not isinstance(v, bool) else bool(v))
                for k, v in relations.items()
            },
            "spread_code_weight_enumerator": {
                str(k): int(v) for k, v in sorted(spread_enum.items())
            },
            "spread_dual_weight_enumerator_head": {
                str(k): int(dual_enum[k]) for k in sorted(dual_enum)[:6]
            },
            "point_kernel_weight_enumerator": {
                str(k): int(v) for k, v in sorted(point_kernel_enum.items())
            },
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
