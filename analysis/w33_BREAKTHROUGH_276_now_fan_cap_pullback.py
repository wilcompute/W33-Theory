"""W(3,3) BREAKTHROUGH 276: now-fan cap pullback.

BT275 made the Gray/selector clock internal to the F_2^4 octonion carrier:

    0 | [3,6,5,12,9,10] | 15

with 0 the real scalar cap, 15 the all-ones cap, and six moving even units.
BT276 pulls that carrier back to the BT172/173 quotient now-fan.

The nonzero even units are the seven imaginary octonion/Fano units.  Under the
BT172 temporal qutrit geometry:

    15  <-> the unique now point;
    six moving units <-> the six non-now fixed points;
    0   <-> the real scalar cap outside the fixed heptad.

The six BT173 four-cells are not arbitrary unresolved cells.  Each four-cell is
anchored by exactly one non-now fixed point, each anchor is hit once, and no
four-cell is anchored at the now point.  The same six anchors are also the six
line-pair orbits whose two lines each meet the fixed heptad in that one anchor.

So BT173's 2^6 search is precisely the peripheral Fano clock carrier that
BT275 folds through 0 and 15.
"""

from __future__ import annotations

from collections import defaultdict
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


Q = 3
QFACT = 6
ALL_ONES = 15


def _artifact(name: str) -> dict:
    path = ROOT / "data" / name
    if not path.exists():
        raise RuntimeError(f"missing prerequisite artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _cycles(permutation: list[int]) -> list[list[int]]:
    seen = set()
    cycles = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        cycle = []
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        cycles.append(cycle)
    return cycles


def _selected_option_index(cell: list[int], options: list[list[list[int]]], outer: list[int]) -> int:
    selected = sorted(tuple(sorted((point, outer[point]))) for point in cell if point < outer[point])
    normalized_options = [
        sorted(tuple(edge) for edge in option)
        for option in options
    ]
    return normalized_options.index(selected)


def now_fan_cap_pullback_packet() -> dict:
    bt172 = _artifact("w33_BREAKTHROUGH_172_outer_involution_temporal_qutrit.json")
    bt173 = _artifact("w33_BREAKTHROUGH_173_now_fan_rigid_outer_reconstruction.json")
    bt275 = _artifact("w33_BREAKTHROUGH_275_folded_gray_selector_transport.json")

    adjacency, _reps = quotient_adjacency()
    lines = [tuple(line) for line in five_cliques(adjacency)]
    line_sets = [frozenset(line) for line in lines]
    line_to_id = {line: index for index, line in enumerate(line_sets)}

    outer = bt173["recovered_outer_zero_based"]
    line_image = [
        line_to_id[frozenset(outer[point] for point in line)]
        for line in line_sets
    ]
    line_orbits = _cycles(line_image)

    fixed_points = bt172["fixed_points"]
    fixed_set = set(fixed_points)
    now_point = bt172["now_point"]
    peripheral_fixed_points = sorted(point for point in fixed_points if point != now_point)

    point_to_lines = defaultdict(list)
    for line_id, line in enumerate(line_sets):
        for point in line:
            point_to_lines[point].append(line_id)

    one_anchor_line_orbits = []
    for orbit in line_orbits:
        if len(orbit) != 2:
            continue
        anchors = [sorted(line_sets[line_id] & fixed_set) for line_id in orbit]
        if all(len(anchor) == 1 for anchor in anchors) and anchors[0] == anchors[1]:
            one_anchor_line_orbits.append(
                {
                    "orbit": orbit,
                    "anchor": anchors[0][0],
                    "line_fixed_intersections": anchors,
                }
            )

    four_cell_rows = []
    for index, cell in enumerate(bt173["four_cells"]):
        common_fixed = [
            fixed
            for fixed in fixed_points
            if all(adjacency[point][fixed] for point in cell)
        ]
        anchor = common_fixed[0] if len(common_fixed) == 1 else None
        selected_option = _selected_option_index(
            cell,
            [
                bt173["cell_options"][2 * index],
                bt173["cell_options"][2 * index + 1],
            ],
            outer,
        )
        incident_anchor_orbits = [
            row["orbit"]
            for row in one_anchor_line_orbits
            if row["anchor"] == anchor
            and any(line_id in point_to_lines[point] for line_id in row["orbit"] for point in cell)
        ]
        four_cell_rows.append(
            {
                "cell_index": index,
                "cell": cell,
                "anchor_fixed_point": anchor,
                "selected_option_index": selected_option,
                "incident_one_anchor_line_orbits": incident_anchor_orbits,
            }
        )

    moving_units = bt275["selected_selector_7_cycle"]
    clock_to_four_cell = [
        {
            "moving_unit": moving_unit,
            "four_cell_index": row["cell_index"],
            "anchor_fixed_point": row["anchor_fixed_point"],
            "selected_option_index": row["selected_option_index"],
        }
        for moving_unit, row in zip(moving_units, four_cell_rows)
    ]
    selected_option_word = [row["selected_option_index"] for row in four_cell_rows]

    checks = {
        "bt275_real_scalar_cap_is_zero": bt275["bt176_even_projection"][0] == 0,
        "bt275_all_ones_cap_is_present": ALL_ONES in bt275["bt176_even_projection"],
        "bt275_moving_cycle_has_qfactorial_units": len(moving_units) == QFACT,
        "bt172_fixed_heptad_has_now_plus_six_peripheral": len(fixed_points) == QFACT + 1
        and len(peripheral_fixed_points) == QFACT
        and now_point in fixed_points,
        "bt173_has_six_four_cells": len(four_cell_rows) == QFACT,
        "each_four_cell_has_one_non_now_anchor": all(
            row["anchor_fixed_point"] in peripheral_fixed_points for row in four_cell_rows
        ),
        "four_cell_anchors_cover_peripheral_fixed_points": sorted(
            row["anchor_fixed_point"] for row in four_cell_rows
        )
        == peripheral_fixed_points,
        "no_four_cell_is_anchored_at_now": all(
            row["anchor_fixed_point"] != now_point for row in four_cell_rows
        ),
        "each_four_cell_has_two_binary_options": bt173["four_cell_option_counts"] == [2] * QFACT,
        "bt173_candidate_count_is_two_to_qfactorial": bt173["candidate_count"] == 2**QFACT,
        "one_anchor_line_orbits_are_six": len(one_anchor_line_orbits) == QFACT,
        "line_orbit_anchors_cover_peripheral_fixed_points": sorted(
            row["anchor"] for row in one_anchor_line_orbits
        )
        == peripheral_fixed_points,
        "each_four_cell_touches_its_anchor_line_orbit_once": all(
            len(row["incident_one_anchor_line_orbits"]) == 1 for row in four_cell_rows
        ),
        "clock_to_cell_table_has_six_entries": len(clock_to_four_cell) == QFACT,
        "selected_option_word_has_single_flip_in_bt173_order": selected_option_word
        == [0, 0, 0, 0, 0, 1],
    }

    return {
        "breakthrough": 276,
        "title": "Now-fan cap pullback",
        "bt275_caps": {
            "real_scalar_cap": 0,
            "now_cap_all_ones": ALL_ONES,
            "moving_units": moving_units,
        },
        "bt172_now_fan": {
            "fixed_points": fixed_points,
            "now_point": now_point,
            "peripheral_fixed_points": peripheral_fixed_points,
        },
        "one_anchor_line_orbits": one_anchor_line_orbits,
        "four_cell_rows": four_cell_rows,
        "clock_to_four_cell_table": clock_to_four_cell,
        "selected_option_word_bt173_order": selected_option_word,
        "architectural_reading": (
            "The folded F2^4 clock now has a quotient-geometry pullback. The "
            "real unit 0 is the scalar cap outside the fixed heptad; the all-"
            "ones unit 15 is the now cap; the six selector moving units clock "
            "the six BT173 four-cell binary choices anchored by the six non-now "
            "fixed points. The same six anchors appear as the six line-pair "
            "orbits with one fixed point on each line. Thus BT173's 2^6 outer-"
            "reconstruction search is exactly the peripheral Fano carrier that "
            "BT275 folds through the scalar and now caps."
        ),
        "boundary": (
            "This proves the cap/peripheral carrier pullback and records the "
            "BT173-order clock table. It does not yet fix a unique Fano "
            "orientation identifying each moving F2^4 unit with a named "
            "peripheral now-fan point up to PSL(2,7)."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = now_fan_cap_pullback_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 276: NOW-FAN CAP PULLBACK")
    print("=" * 78)
    print()
    print(f"BT275 caps       = {packet['bt275_caps']}")
    print(f"now point        = {packet['bt172_now_fan']['now_point']}")
    print(f"four-cell anchors= {[row['anchor_fixed_point'] for row in packet['four_cell_rows']]}")
    print(f"option word      = {packet['selected_option_word_bt173_order']}")
    print(f"verified         = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_276_now_fan_cap_pullback.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
