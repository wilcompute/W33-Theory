"""W(3,3) BREAKTHROUGH 277: Fano orientation gauge stabilizer.

BT276 proved the carrier-level pullback:

    real cap 0, now cap 15, six moving units

maps to the BT172/173 now-fan carrier:

    scalar cap, now point, six peripheral four-cell anchors.

The remaining issue is orientation.  BT277 computes it exactly.  Build the
Fano plane on the seven nonzero even F_2^4 units by XOR triples, and require
15 to map to the BT172 now point.  The three fixed now-fan axes determine
three peripheral pairs, but they do not determine the whole Fano plane.

There are exactly two completions of those three axes to a Fano plane, and for
each completion exactly 24 now-fixing Fano isomorphisms from the F_2^4 octonion
plane.  Therefore the residual orientation gauge has size

    2 * 24 = 48 = mu * k,

which is exactly the BT272 Mobius-Kantor selector stabilizer.

Moreover, under every one of the 48 lifts, BT275's moving q!-cycle runs through
the three temporal axes twice:

    (a,b,c,a,b,c).

So the q! clock is a two-lap q-axis temporal sweep, with a residual 48-element
Fano/octonion gauge rather than a missing arbitrary label.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


Q = 3
MU = 4
K = 12
LAMBDA = 2
ALL_ONES = 15
MOVING_CYCLE = [3, 6, 5, 12, 9, 10]
NONZERO_EVEN_UNITS = sorted(MOVING_CYCLE + [ALL_ONES])


def _artifact(name: str) -> dict:
    path = ROOT / "data" / name
    if not path.exists():
        raise RuntimeError(f"missing prerequisite artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def unit_fano_lines() -> set[frozenset[int]]:
    return {
        frozenset(triple)
        for triple in combinations(NONZERO_EVEN_UNITS, Q)
        if triple[0] ^ triple[1] ^ triple[2] == 0
    }


def fano_completions_from_axes(
    now_point: int,
    axes: list[frozenset[int]],
) -> list[set[frozenset[int]]]:
    peripheral_pairs = [
        tuple(sorted(point for point in axis if point != now_point))
        for axis in axes
    ]
    peripheral_points = sorted(point for pair in peripheral_pairs for point in pair)
    candidate_nonfan_lines = [
        frozenset((left, mid, right))
        for left in peripheral_pairs[0]
        for mid in peripheral_pairs[1]
        for right in peripheral_pairs[2]
    ]

    completions = []
    for nonfan_lines in combinations(candidate_nonfan_lines, MU):
        ok = True
        for left, right in combinations(peripheral_points, 2):
            if any(left in axis and right in axis for axis in axes):
                continue
            if sum(left in line and right in line for line in nonfan_lines) != 1:
                ok = False
                break
        if ok:
            completions.append(set(axes) | set(nonfan_lines))
    return completions


def fano_orientation_gauge_stabilizer_packet() -> dict:
    bt172 = _artifact("w33_BREAKTHROUGH_172_outer_involution_temporal_qutrit.json")
    bt272 = _artifact("w33_BREAKTHROUGH_272_mobius_kantor_selector_classification.json")
    bt275 = _artifact("w33_BREAKTHROUGH_275_folded_gray_selector_transport.json")

    now_point = bt172["now_point"]
    axes = [
        frozenset(points)
        for _line_id, points in sorted(
            (int(line_id), fixed_points)
            for line_id, fixed_points in bt172["fixed_line_fixed_points"].items()
        )
    ]
    peripheral_pairs = [
        tuple(sorted(point for point in axis if point != now_point))
        for axis in axes
    ]
    peripheral_points = sorted(point for pair in peripheral_pairs for point in pair)
    axis_by_point = {
        point: axis_index
        for axis_index, pair in enumerate(peripheral_pairs)
        for point in pair
    }

    unit_lines = unit_fano_lines()
    completions = fano_completions_from_axes(now_point, axes)
    map_rows = []
    for completion_index, completion in enumerate(completions):
        for permuted_points in permutations(peripheral_points):
            mapping = {ALL_ONES: now_point, **dict(zip(MOVING_CYCLE, permuted_points))}
            image_lines = {frozenset(mapping[point] for point in line) for line in unit_lines}
            if image_lines == completion:
                axis_sequence = [axis_by_point[mapping[unit]] for unit in MOVING_CYCLE]
                map_rows.append(
                    {
                        "completion_index": completion_index,
                        "mapping": {str(key): value for key, value in sorted(mapping.items())},
                        "axis_sequence": axis_sequence,
                    }
                )

    maps_by_completion = Counter(row["completion_index"] for row in map_rows)
    axis_sequence_distribution = Counter(tuple(row["axis_sequence"]) for row in map_rows)
    axis_sequence_rows = [
        {"axis_sequence": list(sequence), "count": count}
        for sequence, count in sorted(axis_sequence_distribution.items())
    ]

    checks = {
        "unit_fano_has_seven_lines": len(unit_lines) == 7,
        "bt172_has_q_now_axes": len(axes) == Q,
        "each_now_axis_has_now_plus_two_peripheral_points": all(
            now_point in axis and len(axis) == Q for axis in axes
        ),
        "peripheral_points_are_six": len(peripheral_points) == 6,
        "completion_count_is_lambda": len(completions) == LAMBDA,
        "each_completion_has_seven_lines": all(len(completion) == 7 for completion in completions),
        "maps_per_completion_are_24": dict(sorted(maps_by_completion.items())) == {0: 24, 1: 24},
        "total_orientation_gauge_is_mu_k": len(map_rows) == MU * K == 48,
        "total_orientation_gauge_matches_bt272_stabilizer": len(map_rows)
        == bt272["selector_stabilizer_order"],
        "axis_sequences_are_double_q_laps": all(
            row["axis_sequence"][:Q] == row["axis_sequence"][Q:]
            and sorted(row["axis_sequence"][:Q]) == list(range(Q))
            for row in map_rows
        ),
        "axis_sequence_orbit_has_qfactorial_patterns": len(axis_sequence_distribution) == 6,
        "each_axis_sequence_has_two_to_q_lifts": set(axis_sequence_distribution.values()) == {2**Q},
        "bt275_cycle_is_the_moving_cycle": bt275["selected_selector_7_cycle"] == MOVING_CYCLE,
    }

    return {
        "breakthrough": 277,
        "title": "Fano orientation gauge stabilizer",
        "unit_fano_lines": sorted([sorted(line) for line in unit_lines]),
        "now_point": now_point,
        "now_axes": sorted([sorted(axis) for axis in axes]),
        "peripheral_pairs": peripheral_pairs,
        "completion_count": len(completions),
        "completions": [
            sorted([sorted(line) for line in completion])
            for completion in completions
        ],
        "orientation_gauge_size": len(map_rows),
        "maps_by_completion": dict(sorted(maps_by_completion.items())),
        "axis_sequence_distribution": axis_sequence_rows,
        "sample_maps": map_rows[:8],
        "architectural_reading": (
            "The missing BT276 orientation is a real finite gauge, not a loose "
            "label choice. Fixing the now cap and the three temporal axes leaves "
            "two Fano completions and 24 now-fixing isomorphisms for each, hence "
            "48 = mu*k total lifts. This is exactly the BT272 selector stabilizer. "
            "Under every lift, the BT275 q!-cycle traverses the three temporal "
            "axes twice, (a,b,c,a,b,c), so the self-entangled qutrit clock is a "
            "two-lap q-axis sweep modulo a 48-element Fano/octonion gauge."
        ),
        "boundary": (
            "This identifies the residual orientation gauge. It does not yet pick "
            "one lift from the 48; that should require an additional sign, "
            "holonomy, or octonion multiplication convention."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = fano_orientation_gauge_stabilizer_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 277: FANO ORIENTATION GAUGE STABILIZER")
    print("=" * 78)
    print()
    print(f"completion count    = {packet['completion_count']}")
    print(f"orientation gauge   = {packet['orientation_gauge_size']}")
    print(f"maps by completion  = {packet['maps_by_completion']}")
    print(f"axis sequences      = {packet['axis_sequence_distribution']}")
    print(f"verified            = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_277_fano_orientation_gauge_stabilizer.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
