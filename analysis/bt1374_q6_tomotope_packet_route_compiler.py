#!/usr/bin/env python3
"""BT1374: compile holonet packet routes into Q6/tomotope addresses.

BT1371 proved a 192-row equivariant address table

    tomotope flag <-> Q6 edge.

BT1374 uses that table as an actual runtime compiler target.  Each BT828
route digit already has a 48-block tomotope body address and a 2160-slot mirror
address.  The low two mirror bits choose one of the four local transversal
flags over the tomotope block:

    tomotope_flag = 4 * tomotope_block + (mirror_slot mod 4).

The result is a concrete packet route whose executable address is a Q6 edge.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1374_q6_tomotope_packet_route_compiler.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def hamming(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def compile_digit(
    row: dict[str, Any], address_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    tomotope_block = int(row["tomotope_block"])
    transversal = int(row["mirror_slot"]) % 4
    tomotope_flag = 4 * tomotope_block + transversal
    address = address_rows[tomotope_flag]
    return {
        "depth": int(row["depth"]),
        "source_digit": int(row["source_digit"]),
        "target_digit": int(row["target_digit"]),
        "source_chart": int(row["source_chart"]),
        "target_chart": int(row["target_chart"]),
        "xor_axes": list(row["xor_axes"]),
        "apartment_hops": int(row["apartment_hops"]),
        "reversible_moves": int(row["reversible_moves"]),
        "mirror_slot": int(row["mirror_slot"]),
        "tomotope_block": tomotope_block,
        "transversal_index": transversal,
        "tomotope_flag": tomotope_flag,
        "q6_edge_index": int(address["q6_edge_index"]),
        "q6_direction": int(address["q6_direction"]),
        "q6_endpoint_a": address["q6_endpoint_a"],
        "q6_endpoint_b": address["q6_endpoint_b"],
        "clock_phase_c12": int(row["clock_phase_c12"]),
    }


def compile_program(
    program: dict[str, Any], address_rows: list[dict[str, Any]]
) -> dict[str, Any]:
    packet_rows = [compile_digit(row, address_rows) for row in program["digit_packets"]]
    return {
        "program": program["program"],
        "level": program["level"],
        "source": program["source"],
        "target": program["target"],
        "route_bound": program["route_bound"],
        "reversible_moves": program["reversible_moves"],
        "slack_to_bound": program["slack_to_bound"],
        "packet_rows": packet_rows,
        "tomotope_flags": [row["tomotope_flag"] for row in packet_rows],
        "q6_edge_indices": [row["q6_edge_index"] for row in packet_rows],
        "q6_directions": [row["q6_direction"] for row in packet_rows],
    }


def build_result() -> dict[str, object]:
    bt828 = load_json("data/bt828_holonet_packet_compiler.json")
    bt1301 = load_json("data/bt1301_full_chart_atlas_isa_compiler.json")
    bt1371 = load_json("data/bt1371_q6_tomotope_explicit_orbit_address_table.json")
    address_rows = bt1371["address_table"]
    inverse = {
        int(row["q6_edge_index"]): int(row["tomotope_flag"]) for row in address_rows
    }

    compiled_programs = [
        compile_program(program, address_rows) for program in bt828["compiled_programs"]
    ]
    all_packet_rows = [
        row for program in compiled_programs for row in program["packet_rows"]
    ]

    atlas_flags = [
        4 * int(route["tomotope_block"]) + (int(route["mirror_slot"]) % 4)
        for route in bt1301["atlas_routes"]
    ]
    atlas_flag_hist = Counter(atlas_flags)
    stress = next(
        program
        for program in compiled_programs
        if program["program"] == "six_digit_stress"
    )

    q6_edge_roundtrip_failures = [
        row
        for row in all_packet_rows
        if inverse[row["q6_edge_index"]] != row["tomotope_flag"]
    ]
    q6_endpoint_failures = [
        row
        for row in all_packet_rows
        if hamming(row["q6_endpoint_a"], row["q6_endpoint_b"]) != 1
        or row["q6_endpoint_a"][5 - row["q6_direction"]]
        == row["q6_endpoint_b"][5 - row["q6_direction"]]
    ]

    checks = {
        "bt828_compiler_loaded": all(bt828["checks"].values()),
        "bt1371_address_table_verified": bt1371["verified"] is True,
        "all_packet_digits_lower_to_q6_edges": len(all_packet_rows)
        == sum(program["level"] for program in compiled_programs),
        "every_tomotope_flag_lives_in_192_bus": all(
            0 <= row["tomotope_flag"] < 192 for row in all_packet_rows
        ),
        "q6_edge_roundtrip_through_bt1371_inverse": not q6_edge_roundtrip_failures,
        "q6_endpoints_are_single_bit_edges": not q6_endpoint_failures,
        "tomotope_block_is_flag_quotient": all(
            row["tomotope_flag"] // 4 == row["tomotope_block"]
            for row in all_packet_rows
        ),
        "transversal_is_mirror_slot_mod_4": all(
            row["tomotope_flag"] % 4 == row["mirror_slot"] % 4
            for row in all_packet_rows
        ),
        "stress_route_has_six_distinct_q6_edges": stress["level"] == 6
        and len(set(stress["q6_edge_indices"])) == 6,
        "stress_route_fills_tomotope_body_bound": stress["route_bound"] == 48,
        "atlas_ingress_uses_sparse_control_lane": len(atlas_flag_hist) == 6
        and sum(atlas_flag_hist.values()) == 540,
    }

    return {
        "bt": 1374,
        "title": "Q6/tomotope packet route compiler",
        "verified": all(checks.values()),
        "address_rule": {
            "formula": "tomotope_flag = 4 * tomotope_block + (mirror_slot mod 4)",
            "meaning": "48 tomotope body blocks times four local transversal flags = 192 Q6 edges",
        },
        "compiled_programs": compiled_programs,
        "atlas_ingress_summary": {
            "routes": len(bt1301["atlas_routes"]),
            "distinct_tomotope_flags": len(atlas_flag_hist),
            "flag_histogram": {str(k): v for k, v in sorted(atlas_flag_hist.items())},
            "reading": (
                "The full 540-chart ingress compiler uses a deliberately sparse "
                "six-flag control lane, while arbitrary BT828 packet programs "
                "lower digit-by-digit into the complete 192-row Q6/tomotope ABI."
            ),
        },
        "interpretation": (
            "BT1371's table is now a compiler target.  A holonet route digit is "
            "not merely tagged by a tomotope block: the mirror low bits choose a "
            "transversal, and the resulting tomotope flag is an executable Q6 edge."
        ),
        "boundary": (
            "This is an address compiler for packet headers.  It does not claim "
            "the listed Q6 edges form a shortest continuous path in the Q6 graph."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "programs": len(result["compiled_programs"]),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
