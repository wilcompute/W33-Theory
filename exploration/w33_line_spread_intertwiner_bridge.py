"""Exact 40 <-> 36 line-spread intertwiner on the common 1+15 core.

The corrected q = 3 story replaces the false point-ovoid carrier by the real
line/spread carrier:

    40 lines  <->  36 spreads.

The exact incidence matrix B (40 x 36) between lines and spreads contains the
next structural closure:

  - line side: 40 = 1 + 15 + 24,
  - spread side: 36 = 1 + 15 + 20,

with the same common 1+15 packet on both sides.

Concretely:

  1. On the line side, the disjointness graph on the 40 lines is

         SRG(40,27,18,18)

     with eigenvalues 27, 3, -3 and multiplicities 1, 15, 24.

  2. On the spread side, the overlap-1 graph on the 36 spreads is

         SRG(36,20,10,12)

     with eigenvalues 20, -4, 2 and multiplicities 1, 15, 20.

  3. The incidence matrix B has singular spectrum

         90^1, 18^15, 0^20,

     equivalently

         B B^T : 90^1, 18^15, 0^24,
         B^T B : 90^1, 18^15, 0^20.

So B kills exactly the line-side 24 and the spread-side 20, and identifies the
common 1+15 packet.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_line_spread_intertwiner_bridge_summary.json"


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


def build_summary() -> dict[str, Any]:
    lines = _build_lines()
    spreads = _all_spreads(lines)

    incidence = np.zeros((40, 36), dtype=int)
    for j, spread in enumerate(spreads):
        for li in spread:
            incidence[li, j] = 1

    bbt = incidence @ incidence.T
    btb = incidence.T @ incidence

    line_disjoint = ((bbt - 9 * np.eye(40, dtype=int)) // 3).astype(int)
    np.fill_diagonal(line_disjoint, 0)

    spread_overlap_1 = np.zeros((36, 36), dtype=int)
    for i, j in combinations(range(36), 2):
        if btb[i, j] == 1:
            spread_overlap_1[i, j] = spread_overlap_1[j, i] = 1

    eig_line = np.rint(np.linalg.eigvalsh(line_disjoint)).astype(int)
    eig_spread = np.rint(np.linalg.eigvalsh(spread_overlap_1)).astype(int)
    eig_bbt = np.rint(np.linalg.eigvalsh(bbt)).astype(int)
    eig_btb = np.rint(np.linalg.eigvalsh(btb)).astype(int)

    # Exact polynomial intertwiner laws:
    #   A_line B = B q(A_sp),  q(x) = (x-2)^2 / 12
    #   A_sp B^T = B^T p(A_line), p(x) = ((x+3)(x-15))/18
    q_spread = (spread_overlap_1 @ spread_overlap_1 - 4 * spread_overlap_1 + 4 * np.eye(36, dtype=int)) / 12
    p_line = (line_disjoint @ line_disjoint - 12 * line_disjoint - 45 * np.eye(40, dtype=int)) / 18

    residual_line_to_spread = line_disjoint @ incidence - incidence @ q_spread
    residual_spread_to_line = spread_overlap_1 @ incidence.T - incidence.T @ p_line

    return {
        "carrier_dictionary": {
            "line_side": "40 = 1 + 15 + 24",
            "spread_side": "36 = 1 + 15 + 20",
            "common_core": "1 + 15",
            "killed_shadows": {"line_side": 24, "spread_side": 20},
        },
        "spectral_data": {
            "line_disjoint_eigenvalues": [int(x) for x in eig_line],
            "spread_overlap_1_eigenvalues": [int(x) for x in eig_spread],
            "BBt_eigenvalues": [int(x) for x in eig_bbt],
            "BtB_eigenvalues": [int(x) for x in eig_btb],
        },
        "exact_intertwiner_laws": {
            "BBt_identity": "B B^T = 9 I + 3 A_line_disjoint",
            "BtB_identity": "B^T B = 10 I + A_spread(ov=1) + 4 A_spread(ov=4) = 6 I + 4 J - 3 A_spread(ov=1)",
            "line_from_spread_polynomial": "A_line B = B * ((A_sp - 2I)^2 / 12)",
            "spread_from_line_polynomial": "A_sp B^T = B^T * ((A_line + 3I)(A_line - 15I) / 18)",
        },
        "line_spread_intertwiner_theorem": {
            "the_line_side_has_exact_split_40_equals_1_plus_15_plus_24": (
                bool(np.array_equal(np.unique(eig_line, return_counts=True)[0], np.array([-3, 3, 27])))
                and bool(np.array_equal(np.unique(eig_line, return_counts=True)[1], np.array([24, 15, 1])))
            ),
            "the_spread_side_has_exact_split_36_equals_1_plus_15_plus_20": (
                bool(np.array_equal(np.unique(eig_spread, return_counts=True)[0], np.array([-4, 2, 20])))
                and bool(np.array_equal(np.unique(eig_spread, return_counts=True)[1], np.array([15, 20, 1])))
            ),
            "the_incidence_operator_B_kills_exactly_the_line_side_24_and_the_spread_side_20": (
                bool(np.array_equal(np.unique(eig_bbt, return_counts=True)[0], np.array([0, 18, 90])))
                and bool(np.array_equal(np.unique(eig_bbt, return_counts=True)[1], np.array([24, 15, 1])))
                and bool(np.array_equal(np.unique(eig_btb, return_counts=True)[0], np.array([0, 18, 90])))
                and bool(np.array_equal(np.unique(eig_btb, return_counts=True)[1], np.array([20, 15, 1])))
            ),
            "the_common_nonzero_singular_packet_is_exactly_1_plus_15": (
                bool(np.array_equal(np.unique(eig_btb[eig_btb > 0], return_counts=True)[0], np.array([18, 90])))
                and bool(np.array_equal(np.unique(eig_btb[eig_btb > 0], return_counts=True)[1], np.array([15, 1])))
            ),
            "the_polynomial_intertwiner_from_spread_to_line_is_exact": (
                bool(np.linalg.norm(residual_line_to_spread) < 1e-12)
            ),
            "the_polynomial_intertwiner_from_line_to_spread_is_exact": (
                bool(np.linalg.norm(residual_spread_to_line) < 1e-12)
            ),
        },
        "interpretation": (
            "The real q=3 incidence carrier is now fully rigid. The 40 lines support the exact "
            "split 1+15+24, the 36 spreads support the exact split 1+15+20, and the line-spread "
            "incidence operator B identifies the common 1+15 core while killing the line-side 24 "
            "and the spread-side 20. So the spread carrier is not a side story. It is the exact "
            "quotient/intertwiner shadow of the old 40-packet."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["line_spread_intertwiner_theorem"]
    print("=" * 72)
    print("W33 LINE-SPREAD INTERTWINER BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
