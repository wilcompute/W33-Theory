"""Correct the remote ``4 x 10`` layer: spread, not ovoid.

Recent remote notes promoted the count identity

    40 = 4 * 10

as a partition of the W(3,3) point graph into four ovoids of size 10. That
would force the point graph to contain a 10-coclique and in particular a
4-coloring by maximum independent sets.

The explicit W(3,3) graph says otherwise. On the actual SRG(40,12,2,4)
point graph,

    alpha(W(3,3)) = 7,

with an exact search finding a 7-coclique and proving that no 8-coclique
exists. So the point-ovoid reading is false.

What survives exactly is the line-side factorization:

    40 points = 10 lines in a spread * 4 points on each line.

That is the genuine ``4 x 10`` structure on W(3,3) at q = 3. The integer 10
is the spread size (Phi_4), not the independence number of the point graph.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_spread_not_ovoid_bridge_summary.json"


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


def _build_w33() -> dict[str, Any]:
    points = _projective_points_f3_4()
    index = {point: i for i, point in enumerate(points)}
    adjacency = [set() for _ in range(40)]
    lines: set[tuple[int, int, int, int]] = set()

    for i, j in combinations(range(40), 2):
        if _omega(points[i], points[j]) != 0:
            continue
        adjacency[i].add(j)
        adjacency[j].add(i)

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

    return {"points": points, "adjacency": adjacency, "lines": sorted(lines)}


def _find_spread(lines: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    point_to_lines: list[list[int]] = [[] for _ in range(40)]
    line_masks: list[int] = []
    for li, line in enumerate(lines):
        mask = 0
        for p in line:
            mask |= 1 << p
            point_to_lines[p].append(li)
        line_masks.append(mask)

    full = (1 << 40) - 1
    chosen: list[int] = []
    answer: list[int] | None = None

    def backtrack(used: int) -> bool:
        nonlocal answer
        if used == full:
            answer = chosen.copy()
            return True
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
            if backtrack(used | mask):
                return True
            chosen.pop()
        return False

    if not backtrack(0) or answer is None:
        raise RuntimeError("Failed to find a spread in the explicit W(3,3) model.")
    return [lines[i] for i in answer]


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


def _line_partition_by_spreads(spreads: list[tuple[int, ...]]) -> bool:
    spread_masks = []
    for spread in spreads:
        mask = 0
        for li in spread:
            mask |= 1 << li
        spread_masks.append(mask)

    full_lines = (1 << 40) - 1

    def backtrack(chosen: list[int], used: int) -> bool:
        if len(chosen) == 4:
            return used == full_lines
        pivot = next(li for li in range(40) if not ((used >> li) & 1))
        for si, spread in enumerate(spreads):
            if pivot not in spread:
                continue
            mask = spread_masks[si]
            if used & mask:
                continue
            chosen.append(si)
            if backtrack(chosen, used | mask):
                return True
            chosen.pop()
        return False

    return backtrack([], 0)


def _independent_set_certificate(adjacency: list[set[int]], target: int) -> dict[str, Any]:
    best: list[int] = []

    def backtrack(chosen: list[int], candidates: set[int]) -> bool:
        nonlocal best
        if len(chosen) > len(best):
            best = chosen.copy()
        if len(chosen) == target:
            return True
        if len(chosen) + len(candidates) < target:
            return False
        pivot = min(candidates)
        if backtrack(chosen + [pivot], candidates - {pivot} - adjacency[pivot]):
            return True
        candidates.remove(pivot)
        return backtrack(chosen, candidates)

    found = backtrack([], set(range(40)))
    return {"found": found, "best": best}


def build_summary() -> dict[str, Any]:
    w33 = _build_w33()
    points = w33["points"]
    adjacency = w33["adjacency"]
    lines = w33["lines"]

    size_8 = _independent_set_certificate(adjacency, 8)
    size_7 = _independent_set_certificate(adjacency, 7)
    if not size_7["found"]:
        raise RuntimeError("Failed to find an explicit 7-coclique witness.")

    all_spreads = _all_spreads(lines)
    spread = _find_spread(lines)
    covered_points = sorted({p for line in spread for p in line})
    four_spread_partition_exists = _line_partition_by_spreads(all_spreads)

    return {
        "graph_dictionary": {
            "vertex_count": 40,
            "degree": 12,
            "line_count": len(lines),
            "line_size": 4,
            "spread_size": len(spread),
            "spread_count": len(all_spreads),
        },
        "independence_certificate": {
            "size_7_witness_indices": size_7["best"],
            "size_7_witness_points": [points[i] for i in size_7["best"]],
            "size_8_exists": size_8["found"],
            "maximum_independence_number": 7,
        },
        "spread_certificate": {
            "spread_lines": spread,
            "covered_point_count": len(covered_points),
            "covered_point_indices": covered_points,
            "spread_factorization": "40 = 10 x 4",
            "all_spreads_count": len(all_spreads),
            "four_spread_partition_of_all_40_lines_exists": four_spread_partition_exists,
        },
        "spread_not_ovoid_theorem": {
            "the_explicit_w33_point_graph_has_no_8_coclique_and_hence_no_10_coclique": (
                not size_8["found"]
            ),
            "the_exact_maximum_independence_number_on_the_explicit_graph_is_7": (
                len(size_7["best"]) == 7 and not size_8["found"]
            ),
            "the_remote_four_ovoids_of_size_10_reading_is_false_on_the_point_graph": (
                not size_8["found"]
            ),
            "the_exact_surviving_4_times_10_structure_is_a_spread_of_10_lines_each_of_size_4": (
                len(spread) == 10 and all(len(line) == 4 for line in spread) and len(covered_points) == 40
            ),
            "the_integer_10_is_the_spread_size_phi4_not_the_point_graph_independence_number": (
                len(spread) == 10 and len(size_7["best"]) == 7
            ),
            "the_dual_salvage_as_four_disjoint_spreads_of_all_40_lines_also_fails_on_the_explicit_line_geometry": (
                len(all_spreads) == 36 and not four_spread_partition_exists
            ),
        },
        "interpretation": (
            "The promoted remote ovoid partition is false on the actual W(3,3) point graph. "
            "The explicit graph has maximum independent size 7, so there is no 10-coclique and "
            "hence no partition into four ovoids of size 10. What survives exactly is the line-side "
            "spread law: one spread consists of 10 totally isotropic lines, each of size 4, and those "
            "10 lines partition the full 40-point carrier. So the honest `4 x 10` structure is spread "
            "size times line size, not ovoid count times ovoid size. Even the stronger dual salvage "
            "fails: the explicit line geometry has 36 spreads, but they do not partition the 40 lines "
            "into four disjoint spreads of size 10."
        ),
        "literature_note": {
            "statement": "The generalized quadrangle W(3,q) possesses an ovoid only if q is even.",
            "source": "Ihringer, 'Intriguing Sets in Quadrangles and Hexagons', slide 19 / lines 449-460.",
        },
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    theorem = summary["spread_not_ovoid_theorem"]
    print("=" * 72)
    print("W33 SPREAD-NOT-OVOID BRIDGE")
    print("=" * 72)
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
