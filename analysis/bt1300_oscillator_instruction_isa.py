#!/usr/bin/env python3
"""BT1300 - Oscillator instruction ISA.

BT1299 proved that the [72,66]_3 oscillator horizon is the holonet runtime
microframe.  BT1300 turns that frame into an instruction layout.

The 72 lanes are the explicit F3 horizon coordinates:

    66 payload lanes = K12 edges on the 3x4 CSS grid,
     6 parity lanes  = column-pair checks.

The clock layout is:

    9 route digits per frame,
    8 ticks per route digit,
    72 = 9*8 ticks.

Because q!=2q at q=3, q!+q = q^2, so the frame naturally splits as

    q! digits * 8 = 48   tomotope packet body,
    q  digits * 8 = 24   local-lift epilogue = 18 payload + 6 parity.

This is an ISA theorem: route compiler packets lower into a fixed 8-tick
micro-op word, and the level-six stress route fills the 48-tick tomotope body
with exactly one tick of slack.
"""
from __future__ import annotations

import json
import math
from itertools import combinations
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1300_oscillator_instruction_isa.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def vertex_label(index: int) -> tuple[int, int]:
    return (index // 4, index % 4)


def edge_class(a: int, b: int) -> str:
    va, vb = vertex_label(a), vertex_label(b)
    if va[0] == vb[0]:
        return "row_edge"
    if va[1] == vb[1]:
        return "column_edge"
    return "mixed_edge"


def micro_op_for_tick(tick: int) -> str:
    if tick < 3:
        return f"q3_xor_axis_{tick}"
    return f"apartment_hop_{tick - 3}"


def build_lane_layout() -> list[dict[str, Any]]:
    edge_pairs = list(combinations(range(12), 2))
    column_pairs = list(combinations(range(4), 2))
    lanes: list[dict[str, Any]] = []
    for lane in range(72):
        digit, tick = divmod(lane, 8)
        base = {
            "lane": lane,
            "digit": digit,
            "tick": tick,
            "micro_op": micro_op_for_tick(tick),
            "frame_region": "tomotope_body" if lane < 48 else "local_lift_epilogue",
        }
        if lane < 66:
            a, b = edge_pairs[lane]
            base.update(
                {
                    "kind": "payload",
                    "coordinate": f"K12_edge_{a}_{b}",
                    "edge": [a, b],
                    "edge_vertices": [vertex_label(a), vertex_label(b)],
                    "edge_class": edge_class(a, b),
                }
            )
        else:
            pair = column_pairs[lane - 66]
            base.update(
                {
                    "kind": "parity",
                    "coordinate": f"column_pair_parity_{pair[0]}_{pair[1]}",
                    "column_pair": list(pair),
                    "edge_class": "parity_symbol",
                }
            )
        lanes.append(base)
    return lanes


def compile_packet_word(packet: dict[str, Any]) -> dict[str, Any]:
    depth = packet["depth"]
    active_ticks = []
    tick_rows = []
    for tick in range(8):
        if tick < 3:
            active = tick in packet["xor_axes"]
            reason = "xor_axis_present" if active else "xor_axis_idle"
        else:
            active = (tick - 3) < packet["apartment_hops"]
            reason = "apartment_hop_budget" if active else "apartment_hop_idle"
        lane = depth * 8 + tick
        active_ticks.append(tick) if active else None
        tick_rows.append(
            {
                "tick": tick,
                "lane": lane,
                "micro_op": micro_op_for_tick(tick),
                "active": active,
                "reason": reason,
            }
        )
    return {
        "depth": depth,
        "source_digit": packet["source_digit"],
        "target_digit": packet["target_digit"],
        "active_tick_count": len(active_ticks),
        "bt828_reversible_moves": packet["reversible_moves"],
        "active_ticks": active_ticks,
        "tick_rows": tick_rows,
        "fits_one_digit_word": len(active_ticks) == packet["reversible_moves"]
        and packet["reversible_moves"] <= 8,
    }


def build_payload() -> dict[str, Any]:
    q = 3
    lam = 2
    qfac = math.factorial(q)
    route_tick = 2**q
    digit_slots = q**2
    lanes_total = route_tick * digit_slots
    tomotope_body_ticks = qfac * route_tick
    local_lift_ticks = q * route_tick

    bt1299 = load_json("data/bt1299_harmonic_microframe_runtime.json")
    horizon = load_json("data/w33_horizon_f3_parity_matrix.json")
    bt828 = load_json("data/bt828_holonet_packet_compiler.json")

    lanes = build_lane_layout()
    payload_lanes = [lane for lane in lanes if lane["kind"] == "payload"]
    parity_lanes = [lane for lane in lanes if lane["kind"] == "parity"]
    body_lanes = [lane for lane in lanes if lane["frame_region"] == "tomotope_body"]
    epilogue_lanes = [
        lane for lane in lanes if lane["frame_region"] == "local_lift_epilogue"
    ]
    epilogue_payload_lanes = [
        lane for lane in epilogue_lanes if lane["kind"] == "payload"
    ]
    edge_class_counts: dict[str, int] = {}
    for lane in lanes:
        edge_class_counts[lane["edge_class"]] = (
            edge_class_counts.get(lane["edge_class"], 0) + 1
        )

    compiled_programs = []
    for program in bt828["compiled_programs"]:
        words = [compile_packet_word(packet) for packet in program["digit_packets"]]
        active_ticks = sum(word["active_tick_count"] for word in words)
        used_lanes = [
            row["lane"] for word in words for row in word["tick_rows"] if row["active"]
        ]
        compiled_programs.append(
            {
                "program": program["program"],
                "level": program["level"],
                "route_bound": program["route_bound"],
                "bt828_reversible_moves": program["reversible_moves"],
                "isa_active_ticks": active_ticks,
                "active_lanes": used_lanes,
                "words": words,
                "fits_microframe": program["route_bound"] <= lanes_total,
                "fits_tomotope_body": program["route_bound"] <= tomotope_body_ticks,
                "active_ticks_match_bt828": active_ticks == program["reversible_moves"],
            }
        )

    stress = next(
        program
        for program in compiled_programs
        if program["program"] == "six_digit_stress"
    )
    first_nine_bound = route_tick * q**2

    checks = {
        "bt1299_verified": bt1299["verified"] is True,
        "horizon_matrix_verified": horizon["summary"]["all_identities_hold"] is True,
        "bt828_compiler_verified": all(bt828["checks"].values()),
        "lane_count_is_72": len(lanes) == lanes_total == 72,
        "payload_count_is_66": len(payload_lanes) == 66,
        "parity_count_is_6": len(parity_lanes) == qfac == 6,
        "digit_slots_are_q_squared": digit_slots == q**2 == 9,
        "tick_slots_are_2_power_q": route_tick == 2**q == 8,
        "frame_identity_uses_q_factorial_plus_q": qfac + q == q**2,
        "tomotope_body_is_q_factorial_digits": len(body_lanes)
        == tomotope_body_ticks
        == 48,
        "local_lift_epilogue_is_q_digits": len(epilogue_lanes)
        == local_lift_ticks
        == 24,
        "epilogue_splits_18_payload_plus_6_parity": len(epilogue_payload_lanes)
        == q * qfac
        == 18
        and len(parity_lanes) == qfac,
        "body_plus_epilogue_reconstructs_frame": tomotope_body_ticks + local_lift_ticks
        == lanes_total,
        "edge_class_counts_match_horizon": edge_class_counts
        == {
            "row_edge": 18,
            "column_edge": 12,
            "mixed_edge": 36,
            "parity_symbol": 6,
        },
        "pure_plus_routed_horizon_split": edge_class_counts["row_edge"]
        + edge_class_counts["column_edge"]
        == 30
        and edge_class_counts["mixed_edge"] + edge_class_counts["parity_symbol"] == 42,
        "all_programs_match_bt828_moves": all(
            program["active_ticks_match_bt828"] for program in compiled_programs
        ),
        "all_programs_fit_microframe": all(
            program["fits_microframe"] for program in compiled_programs
        ),
        "all_existing_programs_fit_tomotope_body": all(
            program["fits_tomotope_body"] for program in compiled_programs
        ),
        "stress_route_bound_is_tomotope_body": stress["route_bound"]
        == tomotope_body_ticks
        == 48,
        "stress_active_ticks_are_47": stress["isa_active_ticks"] == 47,
        "stress_has_one_tick_body_slack": stress["route_bound"]
        - stress["isa_active_ticks"]
        == 1,
        "depth_q2_consumes_one_full_frame": first_nine_bound == lanes_total,
        "basis_ratio_preserved": bt1299["runtime_supercycle"]["basis_change_ratio"]
        == "45/30 = 72/48 = q/lambda = 3/2",
    }

    payload = {
        "theorem": "BT1300 oscillator instruction ISA",
        "verified": all(checks.values()),
        "checks": checks,
        "isa_header": {
            "frame_lanes": lanes_total,
            "payload_lanes": len(payload_lanes),
            "parity_lanes": len(parity_lanes),
            "route_digits_per_frame": digit_slots,
            "ticks_per_digit": route_tick,
            "micro_ops": [micro_op_for_tick(tick) for tick in range(8)],
            "frame_split": "72 = 48 + 18 + 6",
            "body_split": "48 = q! * 2^q",
            "epilogue_split": "24 = q * 2^q = 18 payload + 6 parity",
        },
        "lane_layout": lanes,
        "edge_class_counts": edge_class_counts,
        "compiled_programs": compiled_programs,
        "architecture_reading": (
            "The 72-tick oscillator frame is an ISA frame.  The first q!=6 "
            "route digits form the 48-tick tomotope packet body.  The final "
            "q=3 route digits form a 24-tick local-lift epilogue, split as "
            "18 payload lanes plus 6 F3 parity lanes. Existing BT828 route "
            "programs lower into the 8-tick word [3 Q3 XOR ops, 5 apartment "
            "hop ops]; the level-six stress route fills the tomotope body "
            "with one tick of slack."
        ),
        "honesty_boundary": (
            "This is a deterministic instruction layout and coverage theorem "
            "for the existing BT828 compiler packets. It is not yet a shortest "
            "path optimizer for the full 540-chart atlas."
        ),
    }
    return payload


def main() -> None:
    payload = build_payload()
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "theorem": payload["theorem"],
                "verified": payload["verified"],
                "checks_passed": sum(payload["checks"].values()),
                "checks_total": len(payload["checks"]),
                "out": str(OUT.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not payload["verified"]:
        failed = [name for name, passed in payload["checks"].items() if not passed]
        raise SystemExit(f"BT1300 failed checks: {failed}")


if __name__ == "__main__":
    main()
