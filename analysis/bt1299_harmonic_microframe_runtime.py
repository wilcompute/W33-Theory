#!/usr/bin/env python3
"""BT1299 - Harmonic microframe runtime theorem.

The older oscillator scripts prove the local horizon packet

    [72,66]_3 = oscillator total / payload with parity 6.

The holonet runtime scripts prove a separate-looking packet/network stack:

    per digit route bound = 8,
    mirror bus = 2160,
    full Clifford runtime = 51840,
    durable commit clock T(n)=4*(7^n-1).

BT1299 identifies the missing clock spine.  The 72-symbol oscillator horizon is
the holonet microframe:

    72 = 9 * 8                     q^2 route digits per frame
    2160 = 30 * 72                 E8-Coxeter mirror bus
    51840 = 24 * 30 * 72           full Clifford runtime
          = 720 * 72               S6/Sp(4,2) frames

The commit clock is always route-epoch aligned, but it is oscillator-frame
aligned exactly at depths divisible by q=3.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1299_harmonic_microframe_runtime.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def commit_ticks(level: int) -> int:
    return 4 * (7**level - 1)


def sp4_order(field_order: int) -> int:
    return field_order**4 * (field_order**2 - 1) * (field_order**4 - 1)


def build_payload() -> dict[str, Any]:
    q = 3
    lam = 2
    k = 12
    g = 15
    f = 24
    qfac = math.factorial(q)
    h_e8 = 30

    oscillator = load_json("data/w33_universal_oscillator_stack.json")
    bt827 = load_json("data/bt827_holonet_fractal_architecture.json")
    bt828 = load_json("data/bt828_holonet_packet_compiler.json")
    bt838 = load_json("data/bt838_tomotope_wythoff_runtime_ladder.json")

    summary = oscillator["summary"]
    single_core = bt827["single_core"]
    levels = bt827["fractal_scaling"]["levels"]
    stress_program = bt828["compiled_programs"][-1]
    operations = bt838["source_operation_vertices"]

    route_tick = bt827["fractal_scaling"]["digit_route_bound_components"]["sum"]
    horizon_total = summary["horizon_total"]
    horizon_payload = summary["horizon_payload"]
    horizon_parity = summary["parity_rank"]
    mirror_slots = single_core["mirror_slots"]
    runtime_order = single_core["runtime_order"]
    tomotope_blocks = single_core["tomotope_middle_blocks"]
    polar_geography = 45

    route_digits_per_frame = horizon_total // route_tick
    s6_order = math.factorial(qfac)
    sp42_order = sp4_order(2)
    runtime_frames = runtime_order // horizon_total
    mirror_frames = mirror_slots // horizon_total

    commit_table = []
    for level in range(1, 13):
        ticks = commit_ticks(level)
        commit_table.append(
            {
                "level": level,
                "ticks": ticks,
                "route_epochs": ticks // route_tick,
                "mod_horizon_frame": ticks % horizon_total,
                "frame_locked": ticks % horizon_total == 0,
                "oscillator_frames": (
                    ticks // horizon_total if ticks % horizon_total == 0 else None
                ),
            }
        )

    fractal_rows = []
    for row in levels:
        instances = row["w33_instances_total"]
        fractal_rows.append(
            {
                "level": row["level"],
                "w33_instances_total": instances,
                "mirror_slots_total": row["mirror_slots_total"],
                "mirror_frames_total": row["mirror_slots_total"] // horizon_total,
                "runtime_atoms_total": row["local_clifford_runtime_atoms_total"],
                "runtime_frames_total": row["local_clifford_runtime_atoms_total"]
                // horizon_total,
                "route_bound": row["reversible_route_hops_bound"],
                "route_bound_as_frame_fraction": str(
                    Fraction(row["reversible_route_hops_bound"], horizon_total)
                ),
                "mirror_frame_identity_holds": row["mirror_slots_total"]
                == instances * h_e8 * horizon_total,
                "runtime_frame_identity_holds": row[
                    "local_clifford_runtime_atoms_total"
                ]
                == instances * s6_order * horizon_total,
            }
        )

    checks = {
        "oscillator_stack_is_verified": summary["all_identities_hold"] is True,
        "horizon_total_is_k_times_q_factorial": horizon_total == k * qfac == 72,
        "horizon_payload_is_K12_edges": horizon_payload == math.comb(k, 2) == 66,
        "horizon_parity_is_q_factorial": horizon_parity == qfac == 6,
        "route_tick_is_two_power_q": route_tick == 2**q == 8,
        "one_horizon_frame_is_q2_route_ticks": route_digits_per_frame == q**2 == 9,
        "first_full_route_frame_depth_is_q2": route_tick * q**2 == horizon_total,
        "tomotope_to_oscillator_total": tomotope_blocks + f == horizon_total,
        "tomotope_to_oscillator_payload": tomotope_blocks + q * qfac == horizon_payload,
        "tomotope_to_oscillator_parity": horizon_total - horizon_payload == qfac,
        "old_and_new_mirror_factorizations_match": polar_geography * tomotope_blocks
        == h_e8 * horizon_total
        == mirror_slots,
        "factorization_change_has_ratio_q_over_lambda": Fraction(polar_geography, h_e8)
        == Fraction(horizon_total, tomotope_blocks)
        == Fraction(q, lam),
        "mirror_bus_is_thirty_horizon_frames": mirror_frames == h_e8 == 30,
        "mirror_payload_plus_parity": h_e8 * horizon_payload + h_e8 * horizon_parity
        == mirror_slots,
        "mirror_parity_sheet_is_kg": h_e8 * horizon_parity == k * g == 180,
        "runtime_is_local_lift_times_clocked_horizon": f * h_e8 * horizon_total
        == runtime_order,
        "runtime_is_horizon_times_s6": runtime_frames == s6_order == sp42_order == 720,
        "s6_splits_as_local_lift_times_e8_coxeter": f * h_e8 == s6_order,
        "bt827_runtime_factorization_is_preserved": single_core["runtime_factorization"]
        == "24 * 2160 = 24 * 45 * 48",
        "bt838_ladder_exposes_48_packet_abi": operations["maximal_expanded_tomotope"]
        == tomotope_blocks
        == 48,
        "stress_route_bound_is_tomotope_packet": stress_program["level"] == 6
        and stress_program["route_bound"] == tomotope_blocks == 48,
        "depth_q2_route_bound_is_one_horizon_frame": route_tick * q**2 == horizon_total,
        "commit_clock_route_epoch_aligned": all(
            row["ticks"] % route_tick == 0 for row in commit_table
        ),
        "commit_clock_frame_lock_period_is_q": [
            row["level"] for row in commit_table if row["frame_locked"]
        ]
        == [3, 6, 9, 12],
        "commit_mod_pattern_is_24_48_0": [
            row["mod_horizon_frame"] for row in commit_table[:6]
        ]
        == [24, 48, 0, 24, 48, 0],
        "all_fractal_rows_preserve_frame_identities": all(
            row["mirror_frame_identity_holds"] and row["runtime_frame_identity_holds"]
            for row in fractal_rows
        ),
    }

    payload = {
        "theorem": "BT1299 harmonic microframe runtime theorem",
        "verified": all(checks.values()),
        "checks": checks,
        "microframe": {
            "route_tick": route_tick,
            "route_tick_reading": "8 = 2^q = one worst-case recursive digit route",
            "oscillator_horizon_total": horizon_total,
            "oscillator_horizon_payload": horizon_payload,
            "oscillator_horizon_parity": horizon_parity,
            "route_digits_per_frame": route_digits_per_frame,
            "frame_identity": "72 = 9*8 = q^2 route ticks",
            "first_full_route_frame_depth": q**2,
        },
        "mirror_bus": {
            "mirror_slots": mirror_slots,
            "frames_per_mirror_bus": mirror_frames,
            "identity": "2160 = 30*72",
            "payload_slots": h_e8 * horizon_payload,
            "parity_slots": h_e8 * horizon_parity,
            "parity_sheet_identity": "180 = k*g",
        },
        "runtime_supercycle": {
            "runtime_order": runtime_order,
            "old_factorization": "24*45*48",
            "new_factorization": "24*30*72",
            "frame_factorization": "720*72",
            "runtime_frames": runtime_frames,
            "s6_order": s6_order,
            "sp4_2_order": sp42_order,
            "local_lift_times_e8_coxeter": f * h_e8,
            "basis_change": "45*48 = 30*72; both sides equal the 2160 mirror bus",
            "basis_change_ratio": "45/30 = 72/48 = q/lambda = 3/2",
        },
        "tomotope_to_oscillator": {
            "tomotope_packet_abi": tomotope_blocks,
            "total_completion": "48 + 24 = 72",
            "payload_completion": "48 + 18 = 66",
            "parity_completion": "72 - 66 = 6",
            "reading": (
                "The tomotope packet ABI is the 48-symbol body of the frame. "
                "Adding the local Clifford lift f=24 gives the full oscillator "
                "frame, while adding the q*q!=18 active line-cone sector gives "
                "the payload."
            ),
        },
        "commit_clock": {
            "formula": "T(n)=4*(7^n-1)",
            "route_epoch_alignment": "T(n) is divisible by 8 for all n",
            "oscillator_frame_alignment": "T(n) is divisible by 72 iff 3 divides n",
            "table": commit_table,
        },
        "fractal_scaling": {
            "frame_rule": (
                "At every recursive level, mirror slots are 30 horizon frames "
                "per W33 instance and Clifford runtime atoms are 720 horizon "
                "frames per W33 instance."
            ),
            "rows": fractal_rows,
        },
        "architecture_reading": (
            "The holonet is a clocked oscillator network.  The 8-tick route "
            "digit is the instruction pulse, the [72,66]_3 horizon is the "
            "microframe, the 2160-slot mirror bus is a 30-frame E8 Coxeter "
            "bus, and the 51840 Clifford runtime is a 720-frame S6/Sp(4,2) "
            "supercycle.  Durable commits are always route-epoch aligned and "
            "become horizon-frame aligned exactly every q=3 levels."
        ),
        "honesty_boundary": (
            "This is an exact finite runtime/clock factorization across the "
            "existing oscillator, holonet, and tomotope artifacts. It does not "
            "claim a new physical hardware threshold or a new proof of the "
            "general Cayley diameter theorem."
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
        raise SystemExit(f"BT1299 failed checks: {failed}")


if __name__ == "__main__":
    main()
