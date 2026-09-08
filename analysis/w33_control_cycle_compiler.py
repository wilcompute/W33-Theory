#!/usr/bin/env python3
"""Compile finite-control cycles out of arbitrary HoloVM counter control graphs.

The 12-step add-loop cancellation is a special case of a general rule.  Every
simple control-flow cycle C=(pc_0,...,pc_{m-1}) induces a fixed sequential
Sp(4,3) control endpoint E_C from the program's immutable W33 instruction
layout.  If E_C has finite order r then r complete traversals of C have identity
finite-control endpoint, regardless of the guest values that caused those
traversals.

This module enumerates simple cycles of any finite INC/DECJZ/HALT Program,
computes their exact finite-control orders, and emits a repetition compressor:

    C^n  ->  C^(n mod r)

for the *compiled control artifact only*.  It never removes guest transitions,
receipts, memory updates, continuation roots, or branch evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from w33_authenticated_counter_machine import layout_for
from w33_finite_control_unbounded_guest_hypervisor import IDENTITY, matmul
from w33_steinberg_photonic_macro_refinement import sequential_group_endpoint
from w33_twelve_step_control_cancellation import matrix_order
from w33_typed_universal_microvm import Instruction, Program, add_r1_into_r0_program

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_CONTROL_CYCLE_COMPILER.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def successors(program: Program, pc: int) -> tuple[int, ...]:
    ins = program.instructions[pc]
    if ins.op == "HALT":
        return ()
    if ins.op == "INC":
        return (int(ins.target),)
    return tuple(dict.fromkeys((int(ins.target), int(ins.zero_target))))


def canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    if not cycle:
        raise ValueError("empty cycle")
    rots = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
    return min(rots)


def simple_cycles(program: Program) -> tuple[tuple[int, ...], ...]:
    n = len(program.instructions)
    found: set[tuple[int, ...]] = set()
    for start in range(n):
        def dfs(pc: int, path: tuple[int, ...], seen: frozenset[int]) -> None:
            for nxt in successors(program, pc):
                if nxt == start:
                    found.add(canonical_cycle(path))
                elif nxt not in seen and len(path) < n:
                    dfs(nxt, path + (nxt,), seen | {nxt})
        dfs(start, (start,), frozenset({start}))
    return tuple(sorted(found))


def cycle_word(program: Program, cycle: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    layout = tuple(layout_for(program))
    return tuple((int(layout[pc]), 1) for pc in cycle)


def endpoint_power(endpoint, exponent: int):
    cur = IDENTITY
    for _ in range(int(exponent)):
        cur = matmul(endpoint, cur)
    return cur


@dataclass(frozen=True)
class CycleCertificate:
    cycle: tuple[int, ...]
    axis_word: tuple[tuple[int, int], ...]
    endpoint_order: int
    endpoint_digest: str

    @property
    def certificate_id(self) -> str:
        return digest({
            "schema": "w33.control-cycle-certificate.v1",
            "cycle": self.cycle,
            "axis_word": self.axis_word,
            "endpoint_order": self.endpoint_order,
            "endpoint_digest": self.endpoint_digest,
        })


def certify_cycles(program: Program) -> tuple[CycleCertificate, ...]:
    rows = []
    for cycle in simple_cycles(program):
        word = cycle_word(program, cycle)
        endpoint = sequential_group_endpoint(word)
        order = matrix_order(endpoint, limit=120)
        rows.append(CycleCertificate(cycle, word, order, digest(endpoint)))
    return tuple(rows)


def compress_repetitions(cert: CycleCertificate, repeats: int) -> dict[str, Any]:
    if not isinstance(repeats, int) or repeats < 0:
        raise ValueError("repeats must be a natural number")
    residual = repeats % cert.endpoint_order
    naive_word = cert.axis_word * repeats
    residual_word = cert.axis_word * residual
    if sequential_group_endpoint(naive_word) != sequential_group_endpoint(residual_word):
        raise AssertionError("cycle repetition compression changed finite-control endpoint")
    return {
        "cycle_certificate_id": cert.certificate_id,
        "repeats": repeats,
        "endpoint_order": cert.endpoint_order,
        "cancelled_complete_order_blocks": repeats // cert.endpoint_order,
        "residual_repeats": residual,
        "naive_control_transvections": len(naive_word),
        "compiled_control_transvections": len(residual_word),
        "saved_control_transvections": len(naive_word) - len(residual_word),
        "semantic_transition_count_preserved": len(naive_word),
        "compiled_endpoint_digest": digest(sequential_group_endpoint(residual_word)),
    }


def synthetic_three_cycle() -> Program:
    # 0 -> 1 -> 2 -> 0 on the nonzero path, with DECJZ zero exits to HALT.
    return Program((
        Instruction("INC", 0, 1),
        Instruction("INC", 1, 2),
        Instruction("DECJZ", 0, 0, 3),
        Instruction("HALT"),
    ), name="three-pc-cycle-witness")


def verify() -> dict[str, Any]:
    add = add_r1_into_r0_program()
    add_certs = certify_cycles(add)
    synth = synthetic_three_cycle()
    synth_certs = certify_cycles(synth)

    add_pair = next((c for c in add_certs if c.cycle == (0, 1)), None)
    if add_pair is None:
        raise AssertionError("add program lost canonical 0-1 control cycle")
    add12 = compress_repetitions(add_pair, 6)
    add13 = compress_repetitions(add_pair, 7)

    all_certs = add_certs + synth_certs
    power_checks = []
    for cert in all_certs:
        endpoint = sequential_group_endpoint(cert.axis_word)
        power_checks.append(endpoint_power(endpoint, cert.endpoint_order) == IDENTITY)
        # Exercise multiple repetition counts rather than one hand-picked cycle.
        for repeats in range(0, 2 * cert.endpoint_order + 3):
            compress_repetitions(cert, repeats)

    checks = {
        "add_program_has_canonical_two_pc_cycle": add_pair.cycle == (0, 1),
        "add_pair_control_order_is_six": add_pair.endpoint_order == 6,
        "six_add_cycle_repetitions_compile_to_identity_control": add12["compiled_control_transvections"] == 0 and add12["saved_control_transvections"] == 12,
        "seven_add_cycle_repetitions_leave_one_cycle": add13["compiled_control_transvections"] == 2 and add13["semantic_transition_count_preserved"] == 14,
        "synthetic_program_has_nontrivial_simple_cycle": any(len(c.cycle) == 3 for c in synth_certs),
        "every_cycle_order_is_exactly_exercised": all(power_checks),
        "compiler_preserves_semantic_transition_count": all(
            compress_repetitions(c, c.endpoint_order + 1)["semantic_transition_count_preserved"] == len(c.axis_word) * (c.endpoint_order + 1)
            for c in all_certs
        ),
    }
    out = {
        "schema": "w33.control-cycle-compiler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "add_program": {
            "image_id": add.image_id,
            "layout": list(layout_for(add)),
            "cycles": [vars(c) | {"certificate_id": c.certificate_id} for c in add_certs],
            "six_repetitions": add12,
            "seven_repetitions": add13,
        },
        "synthetic_program": {
            "image_id": synth.image_id,
            "layout": list(layout_for(synth)),
            "cycles": [vars(c) | {"certificate_id": c.certificate_id} for c in synth_certs],
        },
        "theorem": "For any enumerated simple control-flow cycle C with finite Sp(4,3) endpoint order r, replacing n repetitions of C by n mod r repetitions in the compiled finite-control artifact preserves the exact finite-control endpoint. The guest still executes all n|C| semantic transitions.",
        "boundary": "Cycle compression is valid only for the finite-control backend. It does not remove branch decisions, counter/Merkle updates, authenticated receipts, continuation history, externally visible safe points, measurements, or physical energy expenditure.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True, default=list) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True, default=list))
    raise SystemExit(result["status"] != "PASS")
