#!/usr/bin/env python3
"""BT1377: physical universal-computation contract for the holonet.

BT1299--BT1376 now provide the pieces of an executable architecture:

* a 72-tick oscillator microframe and 8-tick packet word;
* symbolic optical hardware timing for the 8 micro-ops;
* Q6/tomotope packet addressing;
* a concrete central C3 scheduler on Steinberg cycle witnesses;
* a strict local S3 phase-gauge correction frontier.

This verifier assembles those pieces into one physical computation contract and
keeps the universality boundary explicit.  The deterministic stack is a
protected finite Clifford/Sp(4,3) runtime.  Universal quantum computation needs
the non-Clifford port named by the older TQC artifact: Hesse-SIC/T injection or
Fibonacci braiding.  The verifier checks that the port is recorded, but it does
not pretend the deterministic Clifford scheduler alone is universal.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1377_physical_universal_computation_contract.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def all_checks(payload: dict[str, Any]) -> bool:
    checks = payload.get("checks", {})
    return bool(checks) and all(checks.values())


def hamming(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right, strict=True))


def build_result() -> dict[str, object]:
    bt1299 = load_json("data/bt1299_harmonic_microframe_runtime.json")
    bt1300 = load_json("data/bt1300_oscillator_instruction_isa.json")
    bt1303 = load_json("data/bt1303_holonet_stack_contract.json")
    bt1306 = load_json("data/bt1306_physical_timing_model.json")
    bt1374 = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    bt1375 = load_json("data/bt1375_steinberg_cycle_operator_scheduler_lift.json")
    bt1376 = load_json("data/bt1376_s3_gauge_radius3_local_optimum_certificate.json")
    tqc = load_json("data/w33_BREAKTHROUGH_344_TQC_on_SQNA.json")

    micro_ops = bt1300["isa_header"]["micro_ops"]
    tick_schedule = bt1306["tick_schedule"]
    durations = bt1306["durations"]
    stress = next(
        program
        for program in bt1374["compiled_programs"]
        if program["program"] == "six_digit_stress"
    )
    packet_rows = [
        row for program in bt1374["compiled_programs"] for row in program["packet_rows"]
    ]
    tqc_protocols = "\n".join(tqc["protocols"])

    physical_pipeline = [
        {
            "layer": "encode_route_digit",
            "logical_object": "BT828 route digit / packet row",
            "physical_action": "choose three ternary axes and up to five apartment hops",
            "verified_by": "BT1300",
        },
        {
            "layer": "emit_optical_word",
            "logical_object": "8-tick ISA word",
            "physical_action": "ticks 0..2 are tritter/EOM phase pulses; ticks 3..7 are delay-line switch pulses",
            "verified_by": "BT1306",
        },
        {
            "layer": "address_packet",
            "logical_object": "tomotope_flag = 4*block + mirror_slot mod 4",
            "physical_action": "lower the packet to a single-bit Q6 edge / switch rail",
            "verified_by": "BT1374",
        },
        {
            "layer": "synchronize_phase",
            "logical_object": "root-fixed S3 line gauge",
            "physical_action": "apply 330 nonidentity phase/counterconnection corrections; no radius-3 local improvement exists",
            "verified_by": "BT1376",
        },
        {
            "layer": "schedule_generation",
            "logical_object": "Steinberg matter state and generation",
            "physical_action": "advance by the central C3 operator on concrete cycle-vector witnesses",
            "verified_by": "BT1375",
        },
        {
            "layer": "run_clifford_supercycle",
            "logical_object": "Sp(4,3) finite Clifford runtime",
            "physical_action": "repeat 720 oscillator frames = 51840 hardware-tick windows",
            "verified_by": "BT1299/BT1303",
        },
        {
            "layer": "non_clifford_port",
            "logical_object": "Hesse-SIC/T measurement or Fibonacci braid resource",
            "physical_action": "inject the non-Clifford resource at a measurement/topological boundary",
            "verified_by": "BT344 boundary artifact",
        },
    ]

    deterministic_kernel = {
        "name": "protected finite Clifford runtime",
        "group": "Sp(4,3)",
        "runtime_order": bt1299["runtime_supercycle"]["runtime_order"],
        "runtime_frames": bt1299["runtime_supercycle"]["runtime_frames"],
        "hardware_tick_windows": durations["clifford_supercycle"]["tau_units"],
        "word_ticks": durations["word"]["tau_units"],
        "microframe_ticks": durations["microframe"]["tau_units"],
        "mirror_bus_ticks": durations["mirror_bus_epoch"]["tau_units"],
        "universal_without_port": False,
    }

    universal_port = {
        "required": True,
        "reason": "Clifford gates are efficiently simulable without a non-Clifford resource.",
        "repo_source": "w33_BREAKTHROUGH_344_TQC_on_SQNA",
        "port_options": [
            "Non-Clifford T gate via Hesse-SIC/T measurement",
            "Fibonacci anyon braiding gives universal quantum computation",
        ],
        "runtime_status": (
            "Recorded as an architecture port. The deterministic BT1299-BT1376 "
            "stack supplies routing, scheduling, correction, and Clifford "
            "execution; the non-Clifford resource is an explicit required input."
        ),
    }

    checks = {
        "bt1299_verified": bt1299["verified"] is True and all_checks(bt1299),
        "bt1300_verified": bt1300["verified"] is True and all_checks(bt1300),
        "bt1303_verified": bt1303["verified"] is True and all_checks(bt1303),
        "bt1306_verified": bt1306["verified"] is True and all_checks(bt1306),
        "bt1374_verified": bt1374["verified"] is True and all_checks(bt1374),
        "bt1375_verified": bt1375["verified"] is True and all_checks(bt1375),
        "bt1376_verified": bt1376["verified"] is True and all_checks(bt1376),
        "eight_tick_word_has_three_axis_and_five_switch_ops": micro_ops
        == [
            "q3_xor_axis_0",
            "q3_xor_axis_1",
            "q3_xor_axis_2",
            "apartment_hop_0",
            "apartment_hop_1",
            "apartment_hop_2",
            "apartment_hop_3",
            "apartment_hop_4",
        ],
        "physical_tick_schedule_matches_word": [
            row["physical_action"] for row in tick_schedule
        ]
        == [
            "program ternary XOR axis",
            "program ternary XOR axis",
            "program ternary XOR axis",
            "advance chart/building route",
            "advance chart/building route",
            "advance chart/building route",
            "advance chart/building route",
            "advance chart/building route",
        ],
        "durations_form_runtime_ladder": [
            durations["word"]["tau_units"],
            durations["tomotope_body"]["tau_units"],
            durations["parity_epilogue"]["tau_units"],
            durations["microframe"]["tau_units"],
            durations["mirror_bus_epoch"]["tau_units"],
            durations["clifford_supercycle"]["tau_units"],
        ]
        == [8, 48, 24, 72, 2160, 51840],
        "stress_route_is_six_distinct_q6_switches": stress["level"] == 6
        and len(set(stress["q6_edge_indices"])) == 6
        and stress["route_bound"] == 48,
        "packet_rows_are_single_bit_q6_edges": all(
            len(row["q6_endpoint_a"]) == 6
            and len(row["q6_endpoint_b"]) == 6
            and hamming(row["q6_endpoint_a"], row["q6_endpoint_b"]) == 1
            for row in packet_rows
        ),
        "central_c3_scheduler_is_concrete": bt1375["central_operator"][
            "cycle_length_profile"
        ]
        == {"3": 27}
        and bt1375["central_operator"]["nilpotent_rank_profile"] == [54, 27, 0],
        "phase_correction_frontier_is_radius3_strict": bt1376["base_witness"][
            "nonidentity_corrections"
        ]
        == 330
        and bt1376["local_certificate"]["total_candidate_relabels_checked"] == 1991015
        and all(
            row["best_delta"] == -5 for row in bt1376["local_certificate"]["radii"]
        ),
        "tqc_artifact_records_non_clifford_port": "Non-Clifford T" in tqc_protocols
        and "Hesse SIC" in tqc_protocols,
        "tqc_artifact_records_fibonacci_universality": tqc["fibonacci_universal_QC"]
        is True
        and "Fibonacci anyon" in tqc["conclusion"],
        "deterministic_kernel_declines_universal_overclaim": deterministic_kernel[
            "universal_without_port"
        ]
        is False
        and universal_port["required"] is True,
    }

    return {
        "bt": 1377,
        "title": "Physical universal-computation contract for the holonet",
        "verified": all(checks.values()),
        "deterministic_kernel": deterministic_kernel,
        "universal_port": universal_port,
        "physical_pipeline": physical_pipeline,
        "how_it_physically_computes": (
            "A logical packet digit is compiled into an 8-tick optical word. "
            "The first three ticks program ternary tritter/EOM axes, the last "
            "five ticks switch delay-line apartment hops, and BT1374 lowers "
            "the packet address to a single-bit Q6 edge.  BT1376 supplies the "
            "S3 phase synchronization frontier, while BT1375 makes generation "
            "advance the actual central C3 action on Steinberg cycle vectors. "
            "Repeating the 72-tick oscillator frame for 720 frames gives the "
            "51840-window finite Clifford runtime."
        ),
        "universal_computation_reading": (
            "The deterministic machine is a physical Clifford/symplectic "
            "runtime.  It becomes a universal quantum-computation architecture "
            "only when the explicit non-Clifford port is supplied: Hesse-SIC/T "
            "measurement or Fibonacci braiding as recorded by the TQC artifact."
        ),
        "boundary": (
            "BT1377 is a cross-artifact architecture contract. It does not set "
            "an optical clock speed, prove a hardware threshold, or prove that "
            "the deterministic Clifford scheduler alone is universal."
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
                "runtime_order": result["deterministic_kernel"]["runtime_order"],
                "universal_port_required": result["universal_port"]["required"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        failed = [name for name, passed in result["checks"].items() if not passed]
        raise SystemExit(f"BT1377 failed checks: {failed}")


if __name__ == "__main__":
    main()
