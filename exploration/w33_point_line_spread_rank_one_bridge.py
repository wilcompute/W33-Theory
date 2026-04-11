"""Exact point-line-spread rank-one collapse on the q=3 carrier chain.

There are now two exact incidence operators on live W33 carriers:

  H : points(40) -> lines(40)
      point-line incidence of the self-dual GQ(3,3),

  B : lines(40) -> spreads(36)
      line-spread incidence on the 36 spread carrier.

Their spectral action is complementary:

  - H keeps the common 1+24 packet and kills the 15 packet,
  - B^T keeps the common 1+15 packet and kills the 24 packet,
  - therefore H B kills both nontrivial packets and leaves only the trivial line.

The exact closure is stronger than that slogan:

    H B = J_(40x36),

the all-ones matrix. So the full point-line-spread chain is literally rank 1.

This gives a clean exact carrier cascade:

    spread side   : 36 = 1 + 15 + 20
      --B-->
    line side     : 40 = 1 + 15 + 24
      --H-->
    point side    : 40 = 1 + 24 + 15
      --HB-->
    trivial line  : 1

That is the sharpest exact finite-algebra closure on the geometric side so far.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_point_line_spread_rank_one_bridge_summary.json"


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


def _build_points_lines_spreads() -> dict[str, Any]:
    points = _projective_points_f3_4()
    index = {point: i for i, point in enumerate(points)}

    point_adj = np.zeros((40, 40), dtype=int)
    lines: set[tuple[int, int, int, int]] = set()
    for i, j in combinations(range(40), 2):
        if _omega(points[i], points[j]) != 0:
            continue
        point_adj[i, j] = point_adj[j, i] = 1
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
    lines = sorted(lines)

    H = np.zeros((40, 40), dtype=int)
    for j, line in enumerate(lines):
        for p in line:
            H[p, j] = 1

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
    spreads = sorted(spreads)

    B = np.zeros((40, 36), dtype=int)
    for j, spread in enumerate(spreads):
        for li in spread:
            B[li, j] = 1

    return {"point_adj": point_adj, "lines": lines, "H": H, "B": B}


def build_summary() -> dict[str, Any]:
    built = _build_points_lines_spreads()
    A_point = built["point_adj"]
    H = built["H"]
    B = built["B"]

    A_line = H.T @ H - 4 * np.eye(40, dtype=int)
    BtB = B.T @ B
    A_spread = np.zeros((36, 36), dtype=int)
    for i, j in combinations(range(36), 2):
        if BtB[i, j] == 1:
            A_spread[i, j] = A_spread[j, i] = 1

    # Exact projector numerators.
    P1_point_num = np.ones((40, 40), dtype=int)
    P15_point_num = A_point @ A_point - 14 * A_point + 24 * np.eye(40, dtype=int)  # /96
    P15_line_num = A_line @ A_line - 14 * A_line + 24 * np.eye(40, dtype=int)  # /96
    P24_line_num = A_line @ A_line - 8 * A_line - 48 * np.eye(40, dtype=int)  # /(-60)
    Q20_spread_num = A_spread @ A_spread - 16 * A_spread - 80 * np.eye(36, dtype=int)  # /(-108)
    Q15_spread_num = A_spread @ A_spread - 22 * A_spread + 40 * np.eye(36, dtype=int)  # /144

    HB = H @ B

    return {
        "carrier_cascade": {
            "spread_side": "36 = 1 + 15 + 20",
            "line_side": "40 = 1 + 15 + 24",
            "point_side": "40 = 1 + 24 + 15",
            "composed_image": "1",
        },
        "incidence_identities": {
            "HHt_identity": "H H^T = 4I + A_point",
            "HtH_identity": "H^T H = 4I + A_line",
            "HB_identity": "H B = J_(40x36)",
            "BtHt_identity": "B^T H^T = J_(36x40)",
        },
        "rank_one_collapse_theorem": {
            "point_line_incidence_is_4_regular_on_both_sides": bool(
                np.all(H.sum(axis=0) == 4) and np.all(H.sum(axis=1) == 4)
            ),
            "point_line_incidence_kills_the_point_side_V15_exactly": bool(
                np.array_equal(P15_point_num @ H, np.zeros((40, 40), dtype=int))
            ),
            "line_spread_incidence_kills_the_line_side_24_exactly": bool(
                np.array_equal(P24_line_num @ B, np.zeros((40, 36), dtype=int))
            ),
            "line_spread_incidence_kills_the_spread_side_20_exactly": bool(
                np.array_equal(B @ Q20_spread_num, np.zeros((40, 36), dtype=int))
            ),
            "line_spread_incidence_identifies_the_common_spread_side_15_with_the_line_side_15": bool(
                np.array_equal(3 * (P15_line_num @ B), 2 * (B @ Q15_spread_num))
            ),
            "the_composed_point_line_spread_map_is_exactly_the_all_ones_rank_one_channel": bool(
                np.array_equal(HB, np.ones((40, 36), dtype=int))
            ),
            "the_composed_map_has_rank_one": bool(np.linalg.matrix_rank(HB) == 1),
            "the_composed_map_has_single_nonzero_singular_value_squared_1440": bool(
                np.array_equal(
                    np.rint(np.linalg.svd(HB, compute_uv=False) ** 2).astype(int),
                    np.array([1440] + [0] * 35),
                )
            ),
        },
        "interpretation": (
            "The geometric side now closes as a genuine carrier cascade. Point-line incidence keeps "
            "the common 1+24 packet and kills 15; line-spread incidence keeps the common 1+15 packet "
            "and kills 24/20; the composition therefore leaves only the trivial line, and in fact does "
            "so exactly as the all-ones map H B = J. So the full q=3 point-line-spread chain is not "
            "just compatible dimension bookkeeping. It is an exact rank-one collapse."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["rank_one_collapse_theorem"]
    print("=" * 72)
    print("W33 POINT-LINE-SPREAD RANK-ONE BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
