"""W(3,3) BREAKTHROUGH 173: now-fan rigid outer reconstruction.

BT171 used GAP's primitive-group atlas to find the full-W(E6) outer
involution.  BT172 showed that the involution fixes a seven-point "now fan":
three triangles through one central point, with three fixed GQ(4,2) lines.

BT173 removes the primitive-atlas dependence from the involution itself.
Given only the GQ(4,2) incidence geometry and the fixed heptad from BT172:

1. Classify all 45 points by their adjacency signature to the seven fan points.
2. This gives 7 singleton classes, 7 forced two-point classes, and 6 unresolved
   four-point cells.
3. Each four-point cell has exactly two nonedge perfect matchings compatible
   with being an involution.
4. Brute-force the resulting 2^6 = 64 candidate involutions.
5. Exactly one candidate preserves all 27 GQ lines.

That unique line-preserving candidate is exactly the BT171 outer involution.
So the outer reflection is not merely a GAP atlas artifact: once the now fan is
known, the finite geometry reconstructs the full-W(E6) lift uniquely.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry import (  # noqa: E402
    five_cliques,
    quotient_adjacency,
)
from analysis.w33_BREAKTHROUGH_172_outer_involution_temporal_qutrit import (  # noqa: E402
    outer_involution_temporal_qutrit_packet,
)


def _bt172_packet() -> dict:
    artifact = ROOT / "data" / "w33_BREAKTHROUGH_172_outer_involution_temporal_qutrit.json"
    if artifact.exists():
        return json.loads(artifact.read_text(encoding="utf-8"))
    return outer_involution_temporal_qutrit_packet()


def _perfect_matchings(cell: list[int]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    left, mid_left, mid_right, right = cell
    return [
        ((left, mid_left), (mid_right, right)),
        ((left, mid_right), (mid_left, right)),
        ((left, right), (mid_left, mid_right)),
    ]


def _cycle_distribution(permutation: list[int]) -> dict:
    seen = set()
    sizes = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        size = 0
        while current not in seen:
            seen.add(current)
            size += 1
            current = permutation[current]
        sizes.append(size)
    return dict(sorted(Counter(sizes).items()))


def now_fan_rigid_outer_reconstruction_packet() -> dict:
    bt172 = _bt172_packet()
    known_outer = bt172["outer_permutation_zero_based"]
    fixed_points = bt172["fixed_points"]
    adjacency, _reps = quotient_adjacency()
    lines = [tuple(line) for line in five_cliques(adjacency)]
    line_set = {tuple(sorted(line)) for line in lines}

    signature_classes = defaultdict(list)
    for point in range(45):
        signature = tuple(1 if adjacency[point][fixed] else 0 for fixed in fixed_points)
        signature_classes[signature].append(point)

    singletons = [points[0] for points in signature_classes.values() if len(points) == 1]
    forced_pairs = [tuple(points) for points in signature_classes.values() if len(points) == 2]
    four_cells = [points for points in signature_classes.values() if len(points) == 4]

    cell_options = []
    for cell in four_cells:
        options = []
        for matching in _perfect_matchings(cell):
            if all(not adjacency[left][right] for left, right in matching):
                options.append(tuple(tuple(sorted(edge)) for edge in matching))
        cell_options.append(options)

    valid_candidates = []
    for choices in product(*cell_options):
        candidate = list(range(45))
        for left, right in forced_pairs:
            candidate[left] = right
            candidate[right] = left
        for matching in choices:
            for left, right in matching:
                candidate[left] = right
                candidate[right] = left

        mapped_lines = {
            tuple(sorted(candidate[point] for point in line))
            for line in lines
        }
        if mapped_lines == line_set:
            valid_candidates.append(candidate)

    recovered = valid_candidates[0] if len(valid_candidates) == 1 else None
    recovered_preserves_adjacency = recovered is not None and all(
        adjacency[left][right] == adjacency[recovered[left]][recovered[right]]
        for left in range(45)
        for right in range(left + 1, 45)
    )

    checks = {
        "signature_classes_are_7_7_6": Counter(len(points) for points in signature_classes.values())
        == {1: 7, 2: 7, 4: 6},
        "singletons_are_fixed_heptad": sorted(singletons) == sorted(fixed_points),
        "forced_pairs_are_seven": len(forced_pairs) == 7,
        "four_cells_are_six": len(four_cells) == 6,
        "each_four_cell_has_two_nonedge_matchings": all(len(options) == 2 for options in cell_options),
        "candidate_count_is_2_to_qfact": 2 ** len(four_cells) == 64,
        "unique_line_preserving_candidate": len(valid_candidates) == 1,
        "recovered_candidate_is_known_outer": recovered == known_outer,
        "recovered_candidate_is_involution": recovered is not None
        and all(recovered[recovered[point]] == point for point in range(45)),
        "recovered_cycle_shape_is_7_fixed_19_pairs": recovered is not None
        and _cycle_distribution(recovered) == {1: 7, 2: 19},
        "recovered_preserves_adjacency": recovered_preserves_adjacency,
    }

    return {
        "breakthrough": 173,
        "title": "Now-fan rigid outer reconstruction",
        "fixed_points": fixed_points,
        "signature_class_size_distribution": dict(
            sorted(Counter(len(points) for points in signature_classes.values()).items())
        ),
        "singleton_classes": singletons,
        "forced_pairs": [list(pair) for pair in forced_pairs],
        "four_cells": four_cells,
        "cell_options": [[list(edge) for edge in option] for options in cell_options for option in options],
        "four_cell_option_counts": [len(options) for options in cell_options],
        "candidate_count": 2 ** len(four_cells),
        "valid_candidate_count": len(valid_candidates),
        "recovered_outer_zero_based": recovered,
        "known_outer_zero_based": known_outer,
        "recovered_cycle_distribution": _cycle_distribution(recovered) if recovered is not None else {},
        "architectural_reading": (
            "The BT171 outer involution can be recovered without GAP's primitive "
            "atlas once the BT172 now-fan is specified. The fixed heptad partitions "
            "the 45 quotient points into 7 fixed singletons, 7 forced swapped pairs, "
            "and 6 four-cells. Each four-cell has two possible nonedge matchings, "
            "but among the 64 possible involutions exactly one preserves the 27 "
            "GQ(4,2) lines. That unique involution is the full-W(E6) outer lift."
        ),
        "boundary": (
            "The theorem reconstructs the outer involution from the now-fan and "
            "incidence geometry. It does not yet explain why this particular now-fan "
            "is selected from W(3,3) before seeing the outer lift."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = now_fan_rigid_outer_reconstruction_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 173: NOW-FAN RIGID OUTER RECONSTRUCTION")
    print("=" * 78)
    print()
    print(f"signature classes     = {packet['signature_class_size_distribution']}")
    print(f"candidate count       = {packet['candidate_count']}")
    print(f"valid candidates      = {packet['valid_candidate_count']}")
    print(f"cycle distribution    = {packet['recovered_cycle_distribution']}")
    print(f"verified              = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_173_now_fan_rigid_outer_reconstruction.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
