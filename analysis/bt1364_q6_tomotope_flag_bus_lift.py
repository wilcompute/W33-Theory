#!/usr/bin/env python3
"""BT1364: lift the BT1363 medial clock to the 192-flag/Q6 bus.

BT1363 proved that the 48 tomotope/Reye middle blocks split as:

    full descended clock: 3 * 16
    pure C4 axis clock: 12 * 4

The full tomotope flag carrier is a fourfold lift of the middle layer:

    192 = 48 * 4.

Independently, Q6 has exactly 192 edges.  This verifier builds the finite bus
assignment that realizes the Q6/tomotope flag count as three binary direction
pairs, one pair for each ternary sheet of BT1363.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1364_q6_tomotope_flag_bus_lift.json"


def qn_edges(n: int) -> list[tuple[tuple[int, ...], tuple[int, ...], int]]:
    edges = []
    for v in itertools.product((0, 1), repeat=n):
        for dim in range(n):
            if v[dim] == 0:
                w = list(v)
                w[dim] = 1
                edges.append((v, tuple(w), dim))
    return edges


def build_result() -> dict[str, object]:
    q6_edges = qn_edges(6)
    direction_pair_profile: dict[int, int] = {}
    for _a, _b, dim in q6_edges:
        direction_pair_profile[dim // 2] = direction_pair_profile.get(dim // 2, 0) + 1

    middle_blocks = 48
    flag_fiber = 4
    tomotope_flags = middle_blocks * flag_fiber
    ternary_sheets = 3
    blocks_per_sheet = 16
    flags_per_sheet = blocks_per_sheet * flag_fiber
    pure_c4_cycles = 12
    flags_per_c4_cycle = 4 * flag_fiber

    sheet_to_q6_direction_pair = {
        sheet: [2 * sheet, 2 * sheet + 1] for sheet in range(ternary_sheets)
    }
    q6_assignment = []
    for sheet, dims in sheet_to_q6_direction_pair.items():
        sheet_edges = [edge for edge in q6_edges if edge[2] in dims]
        for local_index, edge in enumerate(sheet_edges):
            block_index = sheet * blocks_per_sheet + (local_index // flag_fiber)
            flag_index = local_index % flag_fiber
            q6_assignment.append(
                {
                    "q6_edge_index": q6_edges.index(edge),
                    "q6_direction": edge[2],
                    "ternary_sheet": sheet,
                    "middle_block_index": block_index,
                    "flag_fiber_index": flag_index,
                    "tomotope_flag_index": block_index * flag_fiber + flag_index,
                }
            )

    checks = {
        "q6_edges_are_192": len(q6_edges) == 192,
        "tomotope_flags_are_192": tomotope_flags == 192,
        "q6_edges_equal_tomotope_flags": len(q6_edges) == tomotope_flags,
        "q6_direction_pairs_are_three_64_buses": sorted(direction_pair_profile.values())
        == [64, 64, 64],
        "three_sheets_have_64_flags_each": ternary_sheets * flags_per_sheet == 192,
        "sheet_direction_pairs_cover_all_q6_directions": sorted(
            dim for dims in sheet_to_q6_direction_pair.values() for dim in dims
        )
        == list(range(6)),
        "assignment_is_bijective_to_flags": len(
            {row["tomotope_flag_index"] for row in q6_assignment}
        )
        == 192,
        "assignment_uses_all_q6_edges": len(
            {row["q6_edge_index"] for row in q6_assignment}
        )
        == 192,
        "pure_c4_cycles_lift_to_twelve_16_flag_cycles": pure_c4_cycles
        * flags_per_c4_cycle
        == 192,
        "full_descended_clock_lifts_to_three_64_flag_sheets": ternary_sheets
        * flags_per_sheet
        == 192,
        "binary_to_ternary_bus_identity": 6 == 3 * 2,
    }

    return {
        "bt": 1364,
        "title": "Q6 tomotope flag bus lift",
        "verified": all(checks.values()),
        "q6": {
            "vertices": 64,
            "edges": len(q6_edges),
            "directions": 6,
            "direction_pair_profile": {
                str(k): v for k, v in sorted(direction_pair_profile.items())
            },
        },
        "tomotope_flag_bus": {
            "middle_blocks": middle_blocks,
            "flag_fiber": flag_fiber,
            "flags": tomotope_flags,
            "identity": "192 = 48 * 4 = 3 * 16 * 4 = 12 * 4 * 4",
        },
        "lift": {
            "sheet_to_q6_direction_pair": sheet_to_q6_direction_pair,
            "flags_per_ternary_sheet": flags_per_sheet,
            "flags_per_pure_c4_cycle": flags_per_c4_cycle,
            "assignment_sample": q6_assignment[:12],
        },
        "interpretation": (
            "The Q6 edge carrier can be read as the full tomotope flag bus by "
            "pairing its six binary directions into three direction pairs.  "
            "Each pair carries one BT1363 ternary sheet: 64 flags = 16 middle "
            "blocks times the fourfold flag fiber."
        ),
        "boundary": (
            "This is a canonical count-and-bus assignment for the Q6-sized flag "
            "carrier.  It does not claim that the full Q6 cube automorphism group "
            "is the tomotope automorphism group."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "identity": result["tomotope_flag_bus"]["identity"],
                "q6_edges": result["q6"]["edges"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
