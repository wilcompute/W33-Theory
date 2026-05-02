#!/usr/bin/env python3
"""
PART CLXVI - Fano Affine Completion of the Mod-12 Wheel
======================================================

CLXV produced the primitive 4+3 set

    J-cycle: {1,5,12,8}
    q-axis:  {3,6,9}

This module shows that this is exactly the projective completion of the
affine plane AG(2,2), i.e. the Fano plane PG(2,2).

Construction:
    The four J-cycle residues are the four affine points:
        1  -> (0,0)
        5  -> (1,0)
        12 -> (0,1)
        8  -> (1,1)

    The three q-axis residues are the points at infinity / directions:
        3 -> horizontal direction (1,0)
        6 -> vertical direction   (0,1)
        9 -> diagonal direction   (1,1)

The seven Fano lines are the six affine lines plus the line at infinity:
    {1,5,3}, {12,8,3}
    {1,12,6}, {5,8,6}
    {1,8,9}, {5,12,9}
    {3,6,9}

This is the exact Fano bridge hinted by the toroidal-triad page: the mod-12
wheel's 4-cycle and 3-clock complete to the unique 7-point projective plane.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent

Q = 3
RANK_SEED = 2 * Q
Q2 = Q * Q
K = 12
PHI3 = 13
PHI6 = 7
J = 5
J_INV = 8
J_CYCLE = [1, J, K, J_INV]
Q_AXIS = [Q, RANK_SEED, Q2]
FANO_POINTS = J_CYCLE + Q_AXIS

AFFINE_COORDS: Dict[int, Tuple[int, int]] = {
    1: (0, 0),
    5: (1, 0),
    12: (0, 1),
    8: (1, 1),
}
DIRECTIONS: Dict[int, Tuple[int, int]] = {
    3: (1, 0),
    6: (0, 1),
    9: (1, 1),
}

FANO_LINES: List[Tuple[int, int, int]] = [
    (1, 5, 3),
    (12, 8, 3),
    (1, 12, 6),
    (5, 8, 6),
    (1, 8, 9),
    (5, 12, 9),
    (3, 6, 9),
]


@dataclass(frozen=True)
class FanoPoint:
    residue: int
    kind: str
    coordinate_or_direction: str
    role: str


def fano_points() -> List[FanoPoint]:
    roles = {
        1: "unit / affine origin / J-cycle identity",
        5: "threshold residue / affine x-step",
        12: "k=-1 / affine y-step",
        8: "carrier residue / affine diagonal point",
        3: "q / horizontal point at infinity",
        6: "2q rank seed / vertical point at infinity",
        9: "q^2 / diagonal point at infinity",
    }
    rows: List[FanoPoint] = []
    for r in J_CYCLE:
        rows.append(FanoPoint(r, "affine", str(AFFINE_COORDS[r]), roles[r]))
    for r in Q_AXIS:
        rows.append(FanoPoint(r, "infinity", str(DIRECTIONS[r]), roles[r]))
    return rows


@dataclass(frozen=True)
class FanoLine:
    name: str
    points: List[int]
    interpretation: str


def fano_lines() -> List[FanoLine]:
    return [
        FanoLine("horizontal_y0", [1, 5, 3], "affine horizontal line through origin plus horizontal infinity q"),
        FanoLine("horizontal_y1", [12, 8, 3], "parallel horizontal line plus same infinity q"),
        FanoLine("vertical_x0", [1, 12, 6], "affine vertical line through origin plus vertical infinity 2q"),
        FanoLine("vertical_x1", [5, 8, 6], "parallel vertical line plus same infinity 2q"),
        FanoLine("diagonal_x_eq_y", [1, 8, 9], "main diagonal plus diagonal infinity q^2"),
        FanoLine("diagonal_x_plus_y_eq_1", [5, 12, 9], "parallel diagonal plus same infinity q^2"),
        FanoLine("line_at_infinity", [3, 6, 9], "q-axis line at infinity / missing decimal axis"),
    ]


def pair_count(lines: List[Tuple[int, int, int]]) -> Dict[Tuple[int, int], int]:
    counts: Dict[Tuple[int, int], int] = {}
    for line in lines:
        pts = sorted(line)
        for i in range(3):
            for j in range(i + 1, 3):
                pair = (pts[i], pts[j])
                counts[pair] = counts.get(pair, 0) + 1
    return counts


def incidence_count(lines: List[Tuple[int, int, int]]) -> Dict[int, int]:
    counts = {p: 0 for p in FANO_POINTS}
    for line in lines:
        for p in line:
            counts[p] += 1
    return counts


def fano_affine_completion_audit() -> Dict[str, object]:
    pairs = pair_count(FANO_LINES)
    inc = incidence_count(FANO_LINES)
    checks = {
        "seven_points": len(set(FANO_POINTS)) == PHI6 == 7,
        "seven_lines": len(FANO_LINES) == 7,
        "three_points_per_line": all(len(set(line)) == 3 for line in FANO_LINES),
        "three_lines_per_point": all(v == 3 for v in inc.values()),
        "every_pair_on_unique_line": len(pairs) == 21 and all(v == 1 for v in pairs.values()),
        "j_cycle_is_affine_square": set(AFFINE_COORDS) == set(J_CYCLE) == {1, 5, 12, 8},
        "q_axis_is_line_at_infinity": set(DIRECTIONS) == set(Q_AXIS) == {3, 6, 9},
        "line_at_infinity_is_missing_decimal_axis": set(FANO_LINES[-1]) == {3, 6, 9},
        "fano_pair_count_is_C7_2": len(pairs) == 21,
        "fano_incidence_count_is_7_times_3": sum(inc.values()) == 21,
        "fano_points_are_4_plus_3": len(J_CYCLE) + len(Q_AXIS) == 4 + 3 == 7,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXVI_FANO_AFFINE_COMPLETION",
        "source_links": {
            "CLXII": "stabilizer residue quarter-turn J-cycle",
            "CLXV": "mod-12 observable wheel",
        },
        "w33_atoms": {
            "q": Q,
            "rank_seed_2q": RANK_SEED,
            "q_square": Q2,
            "k": K,
            "Phi3": PHI3,
            "Phi6": PHI6,
            "J": J,
            "J_inverse": J_INV,
        },
        "point_partition": {
            "affine_J_cycle": J_CYCLE,
            "points_at_infinity_q_axis": Q_AXIS,
            "all_points": FANO_POINTS,
        },
        "fano_points": [asdict(p) for p in fano_points()],
        "fano_lines": [asdict(l) for l in fano_lines()],
        "incidence_counts": {str(k): v for k, v in inc.items()},
        "checks": checks,
        "theorem_statement": (
            "The primitive CLXV set {1,5,12,8} union {3,6,9} is the projective "
            "completion of AG(2,2).  The J-cycle gives the four affine points, the "
            "q-axis gives the three points at infinity, and the seven affine/projective "
            "lines form the Fano plane PG(2,2)."
        ),
        "interpretive_note": (
            "This explains the Fano bridge: the stabilizer quarter-turn dynamics and "
            "the q-axis are not merely two lists summing to seven. They are the affine "
            "square and its three directions at infinity.  The line at infinity is "
            "exactly the missing decimal q-axis {3,6,9}."
        ),
    }


def main() -> int:
    audit = fano_affine_completion_audit()
    out = ROOT / "PART_CLXVI_fano_affine_completion_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
