#!/usr/bin/env python3
"""WASM-like stack bytecode adapter for the W(3,3) packet ISA.

The previous witness introduced a tiny fixed-width register ISA.  This adapter
adds the next useful compiler boundary: a compact stack bytecode object, close
in spirit to WASM's operand-stack model, is loaded as bytes, decoded, compiled
to the existing tiny-RISC packet ISA, and executed through the same routed W33
dynamic packet events.

The sample program is intentionally the same loop:

    total = 0
    i = 0
    while i < 8:
        total += i*i
        i += 1
    out(total)

It returns 140 after stack-object decode, tiny-RISC lowering, and routed packet
execution.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from w33_binary_object_loader import page_records
from w33_tiny_risc_packet_isa import Instr, execute
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_stack_bytecode_adapter.json"
DEFAULT_MD = ROOT / "docs" / "w33_stack_bytecode_adapter.md"


OPCODES = {
    0x01: "CONST",
    0x02: "LOCAL_GET",
    0x03: "LOCAL_SET",
    0x04: "I32_ADD",
    0x05: "I32_MUL",
    0x06: "I32_LT",
    0x07: "BR_IF",
    0x08: "OUT",
    0xFF: "HALT",
}
OP_BY_NAME = {value: key for key, value in OPCODES.items()}


@dataclass(frozen=True)
class StackInstr:
    opname: str
    a: int = 0
    b: int = 0

    def encode(self) -> bytes:
        return bytes([OP_BY_NAME[self.opname], self.a & 0xFF, self.b & 0xFF])


STACK_PROGRAM = [
    StackInstr("CONST", 0),
    StackInstr("LOCAL_SET", 0),  # total = 0
    StackInstr("CONST", 0),
    StackInstr("LOCAL_SET", 1),  # i = 0
    StackInstr("CONST", 8),
    StackInstr("LOCAL_SET", 2),  # limit = 8
    StackInstr("LOCAL_GET", 1),  # loop starts at stack pc 6
    StackInstr("LOCAL_GET", 1),
    StackInstr("I32_MUL"),
    StackInstr("LOCAL_GET", 0),
    StackInstr("I32_ADD"),
    StackInstr("LOCAL_SET", 0),
    StackInstr("LOCAL_GET", 1),
    StackInstr("CONST", 1),
    StackInstr("I32_ADD"),
    StackInstr("LOCAL_SET", 1),
    StackInstr("LOCAL_GET", 1),
    StackInstr("LOCAL_GET", 2),
    StackInstr("I32_LT"),
    StackInstr("BR_IF", 6),
    StackInstr("LOCAL_GET", 0),
    StackInstr("OUT"),
    StackInstr("HALT"),
]


def encode_stack_program(program: list[StackInstr] = STACK_PROGRAM) -> bytes:
    return b"".join(instr.encode() for instr in program)


def decode_stack_program(blob: bytes) -> list[StackInstr]:
    if len(blob) % 3:
        raise ValueError("stack bytecode object length must be a multiple of 3 bytes")
    out = []
    for byte_pc in range(0, len(blob), 3):
        opcode, a, b = blob[byte_pc : byte_pc + 3]
        if opcode not in OPCODES:
            raise ValueError(f"unknown stack opcode 0x{opcode:02x} at byte {byte_pc}")
        out.append(StackInstr(OPCODES[opcode], a, b))
    return out


def compile_to_tiny_risc(program: list[StackInstr]) -> tuple[list[Instr], list[dict[str, Any]]]:
    tiny: list[Instr] = [Instr("MOVI", 7, 0, 0)]  # r7 is the zero register.
    lowering: list[dict[str, Any]] = []
    stack_to_tiny_pc: dict[int, int] = {}
    unresolved_branches: list[tuple[int, int]] = []
    value_stack: list[int] = []
    free_scratch = [3, 4, 5, 6]
    pending_less: tuple[int, int] | None = None

    def alloc() -> int:
        if not free_scratch:
            raise AssertionError("stack program exceeded four scratch registers")
        return free_scratch.pop(0)

    def release(reg: int) -> None:
        if reg in {3, 4, 5, 6} and reg not in free_scratch:
            free_scratch.insert(0, reg)

    def pop_value() -> int:
        if not value_stack:
            raise AssertionError("stack compiler underflow")
        return value_stack.pop()

    for stack_pc, instr in enumerate(program):
        stack_to_tiny_pc[stack_pc] = len(tiny)
        before = len(tiny)
        if instr.opname == "CONST":
            reg = alloc()
            tiny.append(Instr("MOVI", reg, 0, instr.a))
            value_stack.append(reg)
        elif instr.opname == "LOCAL_GET":
            reg = alloc()
            tiny.append(Instr("ADD", reg, instr.a, 7))
            value_stack.append(reg)
        elif instr.opname == "LOCAL_SET":
            reg = pop_value()
            tiny.append(Instr("ADD", instr.a, reg, 7))
            release(reg)
        elif instr.opname in {"I32_ADD", "I32_MUL"}:
            right = pop_value()
            left = pop_value()
            opname = "ADD" if instr.opname == "I32_ADD" else "MUL"
            tiny.append(Instr(opname, left, left, right))
            release(right)
            value_stack.append(left)
        elif instr.opname == "I32_LT":
            right = pop_value()
            left = pop_value()
            pending_less = (left, right)
        elif instr.opname == "BR_IF":
            if pending_less is None:
                raise AssertionError("BR_IF must follow I32_LT in this compact adapter")
            left, right = pending_less
            unresolved_branches.append((len(tiny), instr.a))
            tiny.append(Instr("BLT", left, right, 0))
            release(left)
            release(right)
            pending_less = None
        elif instr.opname == "OUT":
            reg = pop_value()
            tiny.append(Instr("OUT", reg, 0, 0))
            release(reg)
        elif instr.opname == "HALT":
            tiny.append(Instr("HALT", 0, 0, 0))
        else:
            raise NotImplementedError(instr.opname)
        lowering.append(
            {
                "stack_pc": stack_pc,
                "stack_op": instr.opname,
                "stack_args": [instr.a, instr.b],
                "tiny_pc_start": before,
                "tiny_pc_end": len(tiny) - 1,
            }
        )

    for branch_pc, target_stack_pc in unresolved_branches:
        target_tiny_pc = stack_to_tiny_pc[target_stack_pc]
        old = tiny[branch_pc]
        tiny[branch_pc] = Instr(old.opname, old.a, old.b, target_tiny_pc)

    return tiny, lowering


def build_payload() -> dict[str, Any]:
    blob = encode_stack_program()
    decoded = decode_stack_program(blob)
    object_record = page_records("wasm_like_stack_sum_squares_object", blob)
    tiny_program, lowering = compile_to_tiny_risc(decoded)
    execution = execute(tiny_program)
    trace = execution["trace"]
    checks = {
        "stack_object_roundtrip": object_record["roundtrip_matches"],
        "decoded_program_matches": decoded == STACK_PROGRAM,
        "tiny_result_is_140": execution["output"] == [140],
        "tiny_program_halts": trace[-1]["opname"] == "HALT",
        "lowering_covers_all_stack_ops": len(lowering) == len(decoded),
        "all_tiny_routes_diameter_two": all(row["hops"] <= 2 for row in trace),
        "stack_object_nonempty": len(blob) > 0,
        "tiny_program_nonempty": len(tiny_program) > 0,
    }
    return {
        "schema": "w33.stack_bytecode_adapter.v1",
        "theorem": "WASM-like stack bytecode lowers into the routed W33 tiny packet ISA",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "stack_object": {
            "byte_len": object_record["byte_len"],
            "trit_len": object_record["trit_len"],
            "page_count": object_record["page_count"],
            "sha256": object_record["sha256"],
            "roundtrip_matches": object_record["roundtrip_matches"],
            "page_points": [page["point_label"] for page in object_record["pages"]],
        },
        "stack_program": [
            {"stack_pc": pc, "opname": instr.opname, "args": [instr.a, instr.b]}
            for pc, instr in enumerate(decoded)
        ],
        "lowering": lowering,
        "tiny_program": [
            {"pc": pc, "opname": instr.opname, "args": [instr.a, instr.b, instr.c]}
            for pc, instr in enumerate(tiny_program)
        ],
        "execution": {
            "result": execution["output"],
            "dynamic_steps": len(trace),
            "max_route_hops": max(row["hops"] for row in trace),
            "trace_preview": trace[:48],
            "trace_tail": trace[-12:],
        },
        "checks": checks,
        "interpretation": (
            "The adapter shows the wrapper can accept a compact stack-object "
            "format, not just Python bytecode. Stack instructions lower into the "
            "same tiny packet ISA, and execution remains routed by W33."
        ),
        "honesty_boundary": (
            "This is a WASM-like teaching subset, not full WebAssembly validation "
            "or sandboxing. The value is the object-loader/decoder/compiler/packet "
            "contract."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for row in payload["lowering"]:
        rows.append(
            "| {stack_pc} | {stack_op} | `{stack_args}` | {tiny_pc_start}..{tiny_pc_end} |".format(
                **row
            )
        )
    return f"""# W(3,3) Stack Bytecode Adapter

A compact WASM-like stack object is decoded, lowered into the tiny packet ISA,
and executed as routed W33 packet events.

Stack object bytes: `{payload['stack_object']['byte_len']}`. Stack pages:
`{payload['stack_object']['page_count']}`. Tiny instructions:
`{len(payload['tiny_program'])}`. Dynamic routed steps:
`{payload['execution']['dynamic_steps']}`. Result:
`{payload['execution']['result']}`.

| Stack PC | Stack op | Args | Tiny PC range |
|---:|---|---|---|
{chr(10).join(rows)}

Boundary: this is a compact stack-bytecode subset, not full WebAssembly.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")
    print(f"status: {payload['status']}")
    print(
        "stack-bytecode: bytes={byte_len}, pages={page_count}, tiny_instr={tiny}, dynamic_steps={steps}, result={result}".format(
            byte_len=payload["stack_object"]["byte_len"],
            page_count=payload["stack_object"]["page_count"],
            tiny=len(payload["tiny_program"]),
            steps=payload["execution"]["dynamic_steps"],
            result=payload["execution"]["result"],
        )
    )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
