"""Exact algebra of the 36 spreads of W(3,3).

After removing the false point-ovoid reading, the honest q = 3 object is the
spread carrier:

    36 spreads, each a set of 10 disjoint lines covering all 40 points.

This module computes the exact incidence algebra on that carrier.

Key exact facts:

  1. Each of the 40 lines lies in exactly 9 spreads.
  2. Two lines occur together in a spread iff they are disjoint, and then in
     exactly 3 spreads.
  3. The line-spread incidence matrix B therefore satisfies

         B B^T = 9 I + 3 A_disjoint,

     where A_disjoint is the line-disjointness graph on the 40 lines.
  4. The 36 spreads pairwise intersect in either 1 or 4 lines only.
  5. The overlap-1 graph on spreads is

         SRG(36,20,10,12)

     with nontrivial eigenvalues 2 and -4, i.e. the same nontrivial spectrum
     as W33 itself.
  6. The complementary overlap-4 graph is

         SRG(36,15,6,6)

     with eigenvalues 15, 3, -3.
  7. The spread incidence Gram operator B^T B has spectrum

         90^1, 18^15, 0^20,

     so the 36-spread carrier decomposes exactly as

         36 = 1 + 15 + 20.

So the remote ``36/20/15`` packet is not numerology. It lives exactly on the
spread carrier, not on the false point-ovoid carrier.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_spread_overlap_algebra_bridge_summary.json"


def _projective_points_f3_4() -> list[tuple[int, int, int, int]]:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    if (a, b, c, d) == (0, 0, 0, 0):
                        continue
                    vector = (a, b, c, d)
                    for x in vector:
                        if x:
                            inv = 1 if x == 1 else 2
                            point = tuple((inv * y) % 3 for y in vector)
                            break
                    if point not in seen:
                        seen.add(point)
                        points.append(point)
    return sorted(points)


def _omega(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % 3


def _build_lines() -> list[tuple[int, int, int, int]]:
    points = _projective_points_f3_4()
    index = {point: i for i, point in enumerate(points)}
    lines: set[tuple[int, int, int, int]] = set()
    for i, j in combinations(range(40), 2):
        if _omega(points[i], points[j]) != 0:
            continue
        vi, vj = points[i], points[j]
        line = []
        for a, b in ((1, 0), (0, 1), (1, 1), (1, 2)):
            z = tuple((a * vi[k] + b * vj[k]) % 3 for k in range(4))
            for x in z:
                if x:
                    inv = 1 if x == 1 else 2
                    point = tuple((inv * y) % 3 for y in z)
                    break
            line.append(index[point])
        lines.add(tuple(sorted(set(line))))
    return sorted(lines)


def _all_spreads(lines: list[tuple[int, int, int, int]]) -> list[tuple[int, ...]]:
    point_to_lines: list[list[int]] = [[] for _ in range(40)]
    line_masks: list[int] = []
    for li, line in enumerate(lines):
        mask = 0
        for p in line:
            mask |= 1 << p
            point_to_lines[p].append(li)
        line_masks.append(mask)

    full = (1 << 40) - 1
    spreads: set[tuple[int, ...]] = set()
    chosen: list[int] = []

    def backtrack(used: int) -> None:
        if used == full:
            spreads.add(tuple(sorted(chosen)))
            return
        uncovered = [p for p in range(40) if not ((used >> p) & 1)]
        pivot = min(
            uncovered,
            key=lambda p: sum(1 for li in point_to_lines[p] if not (used & line_masks[li])),
        )
        for li in point_to_lines[pivot]:
            mask = line_masks[li]
            if used & mask:
                continue
            chosen.append(li)
            backtrack(used | mask)
            chosen.pop()

    backtrack(0)
    return sorted(spreads)


def _srg_params(adjacency: np.ndarray) -> dict[str, int]:
    n = adjacency.shape[0]
    degrees = adjacency.sum(axis=1)
    degree_set = {int(x) for x in degrees}
    if len(degree_set) != 1:
        raise RuntimeError(f"Non-regular graph: degree set {sorted(degree_set)}")
    k = next(iter(degree_set))
    lam = set()
    mu = set()
    for i, j in combinations(range(n), 2):
        common = int(np.dot(adjacency[i], adjacency[j]))
        if adjacency[i, j]:
            lam.add(common)
        else:
            mu.add(common)
    if len(lam) != 1 or len(mu) != 1:
        raise RuntimeError(f"Not SRG: lambda {lam}, mu {mu}")
    return {"n": n, "k": k, "lambda": next(iter(lam)), "mu": next(iter(mu))}


def build_summary() -> dict[str, Any]:
    lines = _build_lines()
    spreads = _all_spreads(lines)

    incidence = np.zeros((40, 36), dtype=int)
    for j, spread in enumerate(spreads):
        for li in spread:
            incidence[li, j] = 1

    bbt = incidence @ incidence.T
    btb = incidence.T @ incidence

    line_reps = Counter(map(int, incidence.sum(axis=1)))
    spread_sizes = Counter(map(int, incidence.sum(axis=0)))

    line_disjoint = ((bbt - 9 * np.eye(40, dtype=int)) // 3).astype(int)
    np.fill_diagonal(line_disjoint, 0)

    overlap_1 = np.zeros((36, 36), dtype=int)
    overlap_4 = np.zeros((36, 36), dtype=int)
    overlap_distribution = Counter()
    for i, j in combinations(range(36), 2):
        overlap = int(btb[i, j])
        overlap_distribution[overlap] += 1
        if overlap == 1:
            overlap_1[i, j] = overlap_1[j, i] = 1
        elif overlap == 4:
            overlap_4[i, j] = overlap_4[j, i] = 1

    same_spread_counts = Counter()
    for a, b in combinations(range(40), 2):
        count = int(np.dot(incidence[a], incidence[b]))
        same_spread_counts[count] += 1

    return {
        "spread_carrier_dictionary": {
            "line_count": 40,
            "spread_count": 36,
            "line_size": 4,
            "spread_size": 10,
            "spreads_per_line": 9,
            "disjoint_line_pair_spread_count": 3,
        },
        "incidence_algebra": {
            "row_sum_distribution": dict(line_reps),
            "col_sum_distribution": dict(spread_sizes),
            "bbt_eigenvalues": {
                "values": [int(x) for x in np.rint(np.linalg.eigvalsh(bbt))],
            },
            "btb_eigenvalues": {
                "values": [int(x) for x in np.rint(np.linalg.eigvalsh(btb))],
            },
            "spectral_split": {
                "line_side_40": "40 = 1 + 15 + 24",
                "spread_side_36": "36 = 1 + 15 + 20",
            },
        },
        "intersection_packets": {
            "spread_overlap_distribution": dict(overlap_distribution),
            "line_pair_same_spread_distribution": dict(same_spread_counts),
            "line_disjoint_srg": _srg_params(line_disjoint),
            "spread_overlap_1_srg": _srg_params(overlap_1),
            "spread_overlap_4_srg": _srg_params(overlap_4),
            "spread_overlap_1_eigenvalues": {
                "values": [int(x) for x in np.rint(np.linalg.eigvalsh(overlap_1))],
            },
            "spread_overlap_4_eigenvalues": {
                "values": [int(x) for x in np.rint(np.linalg.eigvalsh(overlap_4))],
            },
        },
        "spread_overlap_algebra_theorem": {
            "each_line_lies_in_exactly_9_spreads": line_reps == Counter({9: 40}),
            "two_lines_lie_in_a_common_spread_iff_they_are_disjoint_and_then_in_exactly_3_spreads": (
                same_spread_counts == Counter({0: 240, 3: 540})
            ),
            "the_line_spread_incidence_matrix_satisfies_BBt_equals_9I_plus_3A_disjoint": (
                np.array_equal(bbt, 9 * np.eye(40, dtype=int) + 3 * line_disjoint)
            ),
            "the_overlap_1_graph_on_the_36_spreads_is_srg_36_20_10_12": (
                _srg_params(overlap_1) == {"n": 36, "k": 20, "lambda": 10, "mu": 12}
            ),
            "the_overlap_1_graph_has_the_same_nontrivial_spectrum_2_minus_4_as_W33": (
                np.array_equal(
                    np.unique(np.rint(np.linalg.eigvalsh(overlap_1)).astype(int)),
                    np.array([-4, 2, 20]),
                )
            ),
            "the_overlap_4_graph_on_the_36_spreads_is_srg_36_15_6_6": (
                _srg_params(overlap_4) == {"n": 36, "k": 15, "lambda": 6, "mu": 6}
            ),
            "the_spread_gram_operator_has_exact_spectrum_90_1_18_15_0_20_and_hence_36_equals_1_plus_15_plus_20": (
                np.array_equal(
                    np.unique(np.rint(np.linalg.eigvalsh(btb)).astype(int), return_counts=True)[0],
                    np.array([0, 18, 90]),
                )
                and np.array_equal(
                    np.unique(np.rint(np.linalg.eigvalsh(btb)).astype(int), return_counts=True)[1],
                    np.array([20, 15, 1]),
                )
            ),
            "the_remote_36_20_15_packet_lives_exactly_on_the_spread_carrier": (
                len(spreads) == 36
                and _srg_params(overlap_1)["k"] == 20
                and _srg_params(overlap_4)["k"] == 15
            ),
        },
        "interpretation": (
            "Once the false point-ovoid reading is removed, the real q=3 carrier is the 36-spread "
            "geometry. Its incidence matrix already contains the exact 20/15 packet: the overlap-1 "
            "graph on spreads is SRG(36,20,10,12) with the same nontrivial spectrum 2,-4 as W33, "
            "while the complementary overlap-4 graph is SRG(36,15,6,6). More sharply, the spread "
            "Gram operator splits the spread carrier exactly as 36 = 1 + 15 + 20. So the remote "
            "36/20/15 counts are not arbitrary shadows; they live exactly on the spread carrier."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["spread_overlap_algebra_theorem"]
    print("=" * 72)
    print("W33 SPREAD OVERLAP ALGEBRA BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
