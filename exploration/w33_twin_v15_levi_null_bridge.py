"""Exact twin-V15 closure on the point/line/spread/Levi carrier chain.

The corrected spread work exposed a common geometric 15-dimensional packet on
the line/spread side. The next honest question is whether that packet is the
same as the old point-side V15.

It is not.

Under the live symplectic group there are two distinct 15-dimensional
irreducibles:

  - one on the 40-point permutation module,
  - one on the 40-line and 36-spread permutation modules.

The point-line incidence operator kills both of them, so the 80-vertex Levi
graph has an exact 30-dimensional nullspace equal to their direct sum.

This is the sharp algebraic correction of the old "same 15 everywhere" slogan.
"""

from __future__ import annotations

import json
import re
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_representation_bridge import (
    _gap_cells,
    _gap_perm,
    _run_gap,
)
from tools.analyze_balanced_orbit_stabilizer import build_w33, get_generators, matrix_to_vertex_perm


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_twin_v15_levi_null_bridge_summary.json"


def _build_lines_and_spreads(adjacency: np.ndarray) -> tuple[list[tuple[int, ...]], np.ndarray, np.ndarray]:
    n = adjacency.shape[0]
    lines = [
        cell
        for cell in combinations(range(n), 4)
        if all(adjacency[i, j] for i, j in combinations(cell, 2))
    ]

    H = np.zeros((n, len(lines)), dtype=int)
    point_to_lines: list[list[int]] = [[] for _ in range(n)]
    line_masks: list[int] = []
    for li, line in enumerate(lines):
        mask = 0
        for p in line:
            H[p, li] = 1
            point_to_lines[p].append(li)
            mask |= 1 << p
        line_masks.append(mask)

    full = (1 << n) - 1
    spreads: set[tuple[int, ...]] = set()
    chosen: list[int] = []

    def backtrack(used: int) -> None:
        if used == full:
            spreads.add(tuple(sorted(chosen)))
            return
        uncovered = [p for p in range(n) if not ((used >> p) & 1)]
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
    spreads_list = sorted(spreads)

    B = np.zeros((len(lines), len(spreads_list)), dtype=int)
    for j, spread in enumerate(spreads_list):
        for li in spread:
            B[li, j] = 1

    return lines, H, B


def _parse_decomp(value: Any) -> list[list[int]]:
    if isinstance(value, list):
        return [[int(part) for part in chunk] for chunk in value]
    if not value:
        return []
    return [
        [int(part) for part in chunk.split(",")]
        for chunk in value.split(";")
        if chunk
    ]


def _character_decomposition_report(
    point_generators: list[list[int]],
    lines: list[tuple[int, ...]],
) -> dict[str, Any]:
    gap_script = "\n".join(
        [
            "gens := [" + ",".join(_gap_perm(g) for g in point_generators) + "];;",
            "G := Group(gens);;",
            'Print("size=", Size(G), "\\n");',
            "tbl := CharacterTable(G);;",
            "irr := Irr(tbl);;",
            "degs := List(irr, chi -> chi[1]);;",
            "reps := List(ConjugacyClasses(G), Representative);;",
            "lines := " + _gap_cells(lines) + ";;",
            "valsPt := List(reps, g -> Number([1..40], i -> i^g = i));;",
            "valsLn := List(reps, g -> Number(lines, L -> Set(List(L, x -> x^g)) = L));;",
            "charPt := Character(tbl, valsPt);;",
            "charLn := Character(tbl, valsLn);;",
            "decPt := List(irr, chi -> ScalarProduct(tbl, charPt, chi));;",
            "decLn := List(irr, chi -> ScalarProduct(tbl, charLn, chi));;",
            "Fmt := dec -> JoinStringsWithSeparator("
            "List(Filtered(List([1..Length(dec)], i -> [i, degs[i], dec[i]]), x -> x[3] <> 0), "
            "x -> Concatenation(String(x[1]), \",\", String(x[2]), \",\", String(x[3]))), "
            "\";\""
            ");;",
            'Print("point=", Fmt(decPt), "\\n");',
            'Print("line=", Fmt(decLn), "\\n");',
        ]
    )
    stdout = _run_gap(gap_script).replace("\\\n", "")

    def _grab(key: str) -> str:
        match = re.search(rf"{key}=([^\n]+)", stdout)
        if not match:
            raise RuntimeError(f"Failed to recover GAP payload for {key!r}")
        return match.group(1).strip()

    return {
        "size": int(_grab("size")),
        "point": _parse_decomp(_grab("point")),
        "line": _parse_decomp(_grab("line")),
    }


def _degree_index(decomp: list[list[int]], degree: int) -> int:
    matches = [idx for idx, deg, mult in decomp if deg == degree and mult == 1]
    if len(matches) != 1:
        raise RuntimeError(f"Expected unique degree-{degree} constituent, found {matches}")
    return matches[0]


def _pretty(decomp: list[list[int]]) -> str:
    return " + ".join(f"{mult}*{deg}" if mult != 1 else str(deg) for _idx, deg, mult in decomp)


def build_summary() -> dict[str, Any]:
    points, adjacency, _ = build_w33()
    point_adj = np.asarray(adjacency, dtype=int)
    lines, H, B = _build_lines_and_spreads(point_adj)

    line_intersection = H.T @ H - 4 * np.eye(40, dtype=int)
    line_disjoint = np.ones((40, 40), dtype=int) - np.eye(40, dtype=int) - line_intersection

    BtB = B.T @ B
    spread_overlap_1 = np.zeros((36, 36), dtype=int)
    for i in range(36):
        for j in range(i + 1, 36):
            if BtB[i, j] == 1:
                spread_overlap_1[i, j] = spread_overlap_1[j, i] = 1

    # Exact projector numerators.
    P15_point_num = point_adj @ point_adj - 14 * point_adj + 24 * np.eye(40, dtype=int)  # /96
    P15_line_int_num = line_intersection @ line_intersection - 14 * line_intersection + 24 * np.eye(40, dtype=int)  # /96
    P15_line_dis_num = (line_disjoint - 27 * np.eye(40, dtype=int)) @ (
        line_disjoint + 3 * np.eye(40, dtype=int)
    )  # /(-144)
    Q15_spread_num = spread_overlap_1 @ spread_overlap_1 - 22 * spread_overlap_1 + 40 * np.eye(36, dtype=int)  # /144

    levi = np.block(
        [
            [np.zeros((40, 40), dtype=int), H],
            [H.T, np.zeros((40, 40), dtype=int)],
        ]
    )
    twin_null_num = np.block(
        [
            [P15_point_num, np.zeros((40, 40), dtype=int)],
            [np.zeros((40, 40), dtype=int), P15_line_int_num],
        ]
    )

    symplectic_generators = get_generators(points)
    antisymplectic = matrix_to_vertex_perm(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]],
        points,
    )
    if antisymplectic is None:
        raise RuntimeError("Failed to build antisymplectic generator")

    connected = _character_decomposition_report(symplectic_generators, lines)
    full = _character_decomposition_report(symplectic_generators + [antisymplectic], lines)

    connected_point15 = _degree_index(connected["point"], 15)
    connected_line15 = _degree_index(connected["line"], 15)
    connected_point24 = _degree_index(connected["point"], 24)
    connected_line24 = _degree_index(connected["line"], 24)

    full_point15 = _degree_index(full["point"], 15)
    full_line15 = _degree_index(full["line"], 15)
    full_point24 = _degree_index(full["point"], 24)
    full_line24 = _degree_index(full["line"], 24)

    levi_eigs = np.linalg.eigvalsh(levi.astype(float))
    levi_zero_mult = int(np.sum(np.isclose(levi_eigs, 0.0, atol=1e-9)))

    return {
        "carrier_dictionary": {
            "point_side": "40 = 1 + 24 + 15_p",
            "line_side": "40 = 1 + 24 + 15_l",
            "spread_side": "36 = 1 + 20 + 15_l",
            "levi_nullspace": "30 = 15_p + 15_l",
        },
        "connected_group": {
            "order": connected["size"],
            "point_module": connected["point"],
            "line_module": connected["line"],
            "point_15_index": connected_point15,
            "line_15_index": connected_line15,
            "point_24_index": connected_point24,
            "line_24_index": connected_line24,
        },
        "full_group": {
            "order": full["size"],
            "point_module": full["point"],
            "line_module": full["line"],
            "point_15_index": full_point15,
            "line_15_index": full_line15,
            "point_24_index": full_point24,
            "line_24_index": full_line24,
        },
        "exact_identities": {
            "line_intersection_15_projector": "P15_line = (A_int^2 - 14 A_int + 24 I)/96",
            "line_disjoint_15_projector": "P15_line = -(A_dis - 27 I)(A_dis + 3 I)/144",
            "spread_15_projector": "Q15_spread = (A_sp^2 - 22 A_sp + 40 I)/144",
            "levi_adjacency": "L = [[0, H], [H^T, 0]]",
        },
        "twin_v15_theorem": {
            "connected_point_and_line_use_different_degree_15_irreps": connected_point15 != connected_line15,
            "connected_point_and_line_share_the_same_24_irrep": connected_point24 == connected_line24,
            "full_point_and_line_use_different_degree_15_irreps": full_point15 != full_line15,
            "full_point_and_line_share_the_same_24_irrep": full_point24 == full_line24,
            "the_line_intersection_and_line_disjoint_15_projectors_are_exactly_the_same": bool(
                np.array_equal(3 * P15_line_int_num, -2 * P15_line_dis_num)
            ),
            "point_line_incidence_kills_the_point_side_15_exactly": bool(
                np.array_equal(P15_point_num @ H, np.zeros((40, 40), dtype=int))
            ),
            "point_line_incidence_kills_the_line_side_15_exactly": bool(
                np.array_equal(H @ P15_line_int_num, np.zeros((40, 40), dtype=int))
            ),
            "line_spread_incidence_identifies_the_line_and_spread_15_exactly": bool(
                np.array_equal(3 * (P15_line_int_num @ B), 2 * (B @ Q15_spread_num))
            ),
            "the_levi_graph_has_exact_30_dimensional_nullspace": levi_zero_mult == 30,
            "the_levi_nullspace_is_exactly_the_twin_15_sum": bool(
                np.linalg.matrix_rank(twin_null_num.astype(float)) == 30
                and np.array_equal(levi @ twin_null_num, np.zeros((80, 80), dtype=int))
            ),
        },
        "interpretation": (
            "The corrected geometric algebra has twin fifteens, not one universal V15. "
            "The 40-point carrier contains 15_p, while the 40-line and 36-spread carriers contain 15_l. "
            "Point-line incidence annihilates both twins, line-spread incidence preserves the line/spread twin, "
            "and the 80-vertex Levi graph has exact nullspace 15_p + 15_l. So the spread-side 15 is not the old "
            "point-side packet in disguise; it is its exact geometric twin."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=" * 72)
    print("W33 TWIN V15 LEVI-NULL BRIDGE")
    print("=" * 72)
    print()
    print("Connected group modules")
    print(f"  order: {summary['connected_group']['order']}")
    print(f"  point : {_pretty(summary['connected_group']['point_module'])}")
    print(f"  line  : {_pretty(summary['connected_group']['line_module'])}")
    print(
        "  15-indices: "
        f"point {summary['connected_group']['point_15_index']}, "
        f"line {summary['connected_group']['line_15_index']}"
    )
    print()
    print("Full group modules")
    print(f"  order: {summary['full_group']['order']}")
    print(f"  point : {_pretty(summary['full_group']['point_module'])}")
    print(f"  line  : {_pretty(summary['full_group']['line_module'])}")
    print(
        "  15-indices: "
        f"point {summary['full_group']['point_15_index']}, "
        f"line {summary['full_group']['line_15_index']}"
    )
    print()
    for key, value in summary["twin_v15_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
