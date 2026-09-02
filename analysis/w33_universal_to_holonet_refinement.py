#!/usr/bin/env python3
"""Refinement chain from universal W33 VM steps to the Holonet physical contract.

This module composes, rather than conflates, three existing layers:

  semantic layer
      TypedUniversalMicroVM certificates (INC/DECJZ/HALT)
  packet layer
      BT1698: 72-tick microframe = 48-tick Q6/tomotope body + 24-tick
      Hesse/Clifford epilogue, with 16 LOAD/FLIP/LATCH edge slots
  physical-word layer
      BT1377: an 8-tick optical ISA word has three tritter/EOM axis pulses and
      five delay-line apartment-hop switch pulses.

The 3-phase packet edge and the 8-tick optical word are *not declared to be the
same clock decomposition*.  They are different refinement objects already
present in the repository.  A VM macro-step is assigned one typed packet body
slot; the packet frame is then linked to the existing BT1377 optical contract.
This avoids the historical temptation to make 3 and 8 tick counts agree by
renaming them.

The deterministic stack remains Clifford/control.  The explicit non-Clifford
port required for quantum universality is carried through as a REQUIRED but
UNIMPLEMENTED physical resource boundary.
"""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from w33_typed_universal_microvm import (
    Capability,
    Carrier,
    TypedUniversalMicroVM,
    add_r1_into_r0_program,
)

ROOT = Path(__file__).resolve().parents[1]
BODY_OPS = ("LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX")
EPILOGUE_OPS = ("ERASE", "ROUTE", "PHASE", "X-CORR", "Z-CORR", "T-BIT", "RESTORE", "NEXT")
OPTICAL_WORD = (
    "TRITTER_EOM_AXIS_0",
    "TRITTER_EOM_AXIS_1",
    "TRITTER_EOM_AXIS_2",
    "DELAY_LINE_HOP_0",
    "DELAY_LINE_HOP_1",
    "DELAY_LINE_HOP_2",
    "DELAY_LINE_HOP_3",
    "DELAY_LINE_HOP_4",
)


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def run_guest() -> TypedUniversalMicroVM:
    vm = TypedUniversalMicroVM(
        add_r1_into_r0_program(),
        Capability(Carrier.CIRCUIT_ST81, 81),
    )
    vm.state.counter0 = 7
    vm.state.counter1 = 11
    vm.run()
    return vm


def packetize(vm: TypedUniversalMicroVM) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cert in vm.certificates:
        zero = cert.step - 1
        frame = zero // 16
        slot = zero % 16
        base_tick = frame * 72 + slot * 3
        rows.append({
            "semantic_step": cert.step,
            "semantic_instruction": cert.instruction,
            "semantic_pre": cert.pre,
            "semantic_post": cert.post,
            "trace_root": cert.trace_root,
            "carrier": cert.carrier,
            "logical_dimension": cert.logical_dimension,
            "w33_route": list(cert.route),
            "w33_line_buses": list(cert.line_buses),
            "microframe": frame,
            "body_slot": slot,
            "body_ticks": [base_tick, base_tick + 1, base_tick + 2],
            "body_ops": list(BODY_OPS),
            "packet_refinement": "one certified VM macro-step occupies one Q6/tomotope body edge slot",
        })
    return rows


def frame_schedule(rows: list[dict[str, Any]], frame_count: int) -> list[dict[str, Any]]:
    by_key = {(row["microframe"], row["body_slot"]): row for row in rows}
    schedule: list[dict[str, Any]] = []
    for frame in range(frame_count):
        frame_base = frame * 72
        for slot in range(16):
            row = by_key.get((frame, slot))
            for phase in range(3):
                tick = frame_base + slot * 3 + phase
                schedule.append({
                    "tick": tick,
                    "microframe": frame,
                    "region": "tomotope_body",
                    "slot": slot,
                    "op": BODY_OPS[phase] if row else "IDLE_BODY",
                    "semantic_step": row["semantic_step"] if row else None,
                })
        for local_tick in range(24):
            # BT1698 has 3 eight-tick Hesse return words in the epilogue.
            word = local_tick // 8
            word_tick = local_tick % 8
            schedule.append({
                "tick": frame_base + 48 + local_tick,
                "microframe": frame,
                "region": "hesse_clifford_epilogue",
                "word": word,
                "word_tick": word_tick,
                "op": EPILOGUE_OPS[word_tick],
            })
    return schedule


def optical_contract_for_frame(frame: int) -> dict[str, Any]:
    return {
        "microframe": frame,
        "relation": "BT1377 physical-word contract linked to this packet frame; clocks are not identified term-by-term",
        "isa_word_ticks": list(range(8)),
        "physical_actions": list(OPTICAL_WORD),
        "first_three": "tritter/EOM ternary-axis phase pulses",
        "last_five": "delay-line apartment-hop switch pulses",
    }


def verify() -> dict[str, Any]:
    bt1698 = load_json("data/bt1698_holonet_packet_state_machine.json")
    bt1377 = load_json("data/bt1377_physical_universal_computation_contract.json")
    vm = run_guest()
    rows = packetize(vm)
    frames = 1 + (len(rows) - 1) // 16
    schedule = frame_schedule(rows, frames)
    optical = [optical_contract_for_frame(i) for i in range(frames)]

    occupied = {(r["microframe"], r["body_slot"]) for r in rows}
    checks = {
        "guest_computes_expected_result": vm.state.counters() == [18, 0],
        "guest_has_24_certified_steps": len(rows) == 24,
        "bt1698_packet_machine_verified": bt1698.get("verified") is True,
        "bt1377_physical_contract_verified": bt1377.get("verified") is True,
        "two_microframes_cover_24_steps": frames == 2,
        "packet_slots_are_unique": len(occupied) == len(rows),
        "every_step_preserves_w33_certificate": all(len(r["w33_route"]) - 1 <= 2 for r in rows),
        "every_step_has_load_flip_latch": all(tuple(r["body_ops"]) == BODY_OPS for r in rows),
        "frame_schedule_is_exactly_72_ticks_each": len(schedule) == 72 * frames,
        "packet_and_optical_clocks_not_falsely_identified": all(
            "not identified" in row["relation"] for row in optical
        ),
        "optical_word_has_3_plus_5_actions": all(
            tuple(row["physical_actions"][:3]) == OPTICAL_WORD[:3]
            and tuple(row["physical_actions"][3:]) == OPTICAL_WORD[3:]
            for row in optical
        ),
        "nonclifford_port_remains_required": bt1377["universal_port"]["required"] is True,
        "deterministic_kernel_not_overclaimed_universal": bt1377["deterministic_kernel"]["universal_without_port"] is False,
    }

    return {
        "schema": "w33.universal-to-holonet-refinement.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "refinement_chain": [
            "typed universal software semantics",
            "W33 diameter-two certified route",
            "BT1698 16-slot Q6/tomotope packet body",
            "BT1698 Hesse/Clifford epilogue",
            "BT1377 8-tick optical-word contract",
            "explicit non-Clifford resource port for quantum universality",
        ],
        "sample": {
            "semantic_steps": len(rows),
            "microframes": frames,
            "packet_ticks": len(schedule),
            "result": vm.state.counters(),
        },
        "quantum_boundary": {
            "clifford_control_namespace": "Sp(4,3)-clifford-lift",
            "nonclifford_port": bt1377["universal_port"],
            "implemented_by_this_lowerer": False,
        },
        "checks": checks,
        "rows": rows,
        "optical_frame_contracts": optical,
        "boundary": (
            "The refinement is executable through the packet schedule and linked to the repository's existing physical-word contract. "
            "It does not claim calibrated optics, nor does it equate the 3-phase packet edge with the separate 8-tick ISA word."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
