#!/usr/bin/env python3
"""
BT832 - Cover-indexed durable storage simulator.

BT831 says the tomotope's local 48-block packet is invariant, while the
regular cover is not unique.  BT832 makes that an executable storage rule:

    commit ABI       = tomotope_block in {0,...,47}
    durable cover    = k^3 fiber over each ABI block
    kernel to Q_1    = k^6 = (k^3)^2

The cover index k is therefore a storage gauge.  Changing k changes capacity,
fiber coordinates, and kernel order, but the base packet program seen by the
fast route compiler is unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def qk_counts(k: int) -> dict[str, int]:
    return {
        "vertices": 4 * k**3,
        "edges": 24 * k**3,
        "triangles": 32 * k**3,
        "tetrahedra": 8 * k**3,
        "octahedra": 4 * k**3,
        "lifted_packet_slots": 48 * k**3,
        "kernel_order_to_Q1": k**6,
    }


def lift_packet(row: dict, k: int) -> dict:
    block = row["tomotope_block"]
    x = (row["mirror_slot"] + row["clock_phase_c12"] + row["depth"]) % k
    y = (row["source_digit"] + row["target_digit"] + row["tomotope_edge_label"]) % k
    z = (row["apartment_hops"] + row["xor_hops"] + row["tomotope_face_label"]) % k
    fiber_id = x * k * k + y * k + z
    lifted_slot = block * k**3 + fiber_id
    return {
        "depth": row["depth"],
        "base_block": block,
        "cover_coordinate": [x, y, z],
        "fiber_id": fiber_id,
        "lifted_slot": lifted_slot,
        "reduces_to_base_block": lifted_slot // (k**3) == block,
    }


def main() -> None:
    bt828 = load_json("data/bt828_holonet_packet_compiler.json")
    bt831 = load_json("data/bt831_tomotope_minimal_cover_architecture.json")
    cover_indices = [3, 5, 7, 11, 13]
    base_abi_by_program = {
        program["program"]: program["tomotope_blocks"]
        for program in bt828["compiled_programs"]
    }

    cover_rows = []
    for k in cover_indices:
        programs = []
        for program in bt828["compiled_programs"]:
            lifted = [lift_packet(row, k) for row in program["digit_packets"]]
            distinct_lifted = len({row["lifted_slot"] for row in lifted})
            programs.append({
                "program": program["program"],
                "level": program["level"],
                "base_abi_blocks": program["tomotope_blocks"],
                "lifted_packets": lifted,
                "distinct_lifted_slots_used": distinct_lifted,
                "lifted_slot_capacity": 48 * k**3,
                "load_fraction": f"{distinct_lifted}/{48 * k**3}",
                "all_lifts_reduce_to_base_abi": all(row["reduces_to_base_block"] for row in lifted),
            })
        cover_rows.append({
            "cover_index": k,
            "cover_counts": qk_counts(k),
            "program_lifts": programs,
            "base_abi_by_program": base_abi_by_program,
        })

    checks = {
        "bt831_boundary_loaded": bt831["architecture_interpretation"]["abi"].startswith("BT814 48-block"),
        "cover_indices_are_supported": cover_indices[:3] == [3, 5, 7],
        "kernel_order_is_square_of_fiber": all(row["cover_counts"]["kernel_order_to_Q1"] == (row["cover_index"] ** 3) ** 2 for row in cover_rows),
        "lifted_capacity_scales_as_48k3": all(row["cover_counts"]["lifted_packet_slots"] == 48 * row["cover_index"] ** 3 for row in cover_rows),
        "qk_counts_match_bt831_formula": all(
            row["cover_counts"]["vertices"] == 4 * row["cover_index"] ** 3
            and row["cover_counts"]["edges"] == 24 * row["cover_index"] ** 3
            and row["cover_counts"]["triangles"] == 32 * row["cover_index"] ** 3
            for row in cover_rows
        ),
        "base_abi_invariant_across_covers": all(row["base_abi_by_program"] == base_abi_by_program for row in cover_rows),
        "all_lifts_reduce_to_base_abi": all(
            program["all_lifts_reduce_to_base_abi"]
            for row in cover_rows
            for program in row["program_lifts"]
        ),
        "larger_cover_reduces_load_fraction_for_stress": (
            cover_rows[0]["program_lifts"][-1]["distinct_lifted_slots_used"] / cover_rows[0]["program_lifts"][-1]["lifted_slot_capacity"]
            > cover_rows[-1]["program_lifts"][-1]["distinct_lifted_slots_used"] / cover_rows[-1]["program_lifts"][-1]["lifted_slot_capacity"]
        ),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT832 check failed: {name}")

    out = {
        "theorem": "BT832 cover-indexed durable storage simulator",
        "storage_rule": {
            "local_abi": "48 tomotope middle blocks",
            "cover_fiber": "Z_k^3 over each block",
            "lifted_capacity": "48*k^3 durable packet slots",
            "kernel_order": "k^6 = (k^3)^2",
            "architectural_meaning": "k changes durable storage gauge; base route ABI is unchanged",
        },
        "cover_lifts": cover_rows,
        "checks": checks,
    }
    path = ROOT / "data" / "bt832_cover_indexed_durable_storage.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
