#!/usr/bin/env python3
"""Tiny RISC object file executed through the W(3,3) packet ABI.

The Python bytecode VM proves a high-level program stream can be routed through
W33.  This witness lowers one step closer to ordinary machine architecture: a
fixed-width binary instruction object is loaded as bytes, decoded, executed by a
small register machine, and each dynamic instruction receives a W33 packet route.

The ISA is intentionally tiny and auditable:

    MOVI rd, imm
    ADD rd, ra, rb
    ADDI rd, ra, imm
    MUL rd, ra, rb
    BLT ra, rb, target_pc
    OUT ra
    HALT

The sample program computes sum(i*i for i in range(8)) = 140 using a loop.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_binary_object_loader import page_records
from w33_component_execution_simulator import line_lookup
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_tiny_risc_packet_isa.json"
DEFAULT_MD = ROOT / "docs" / "w33_tiny_risc_packet_isa.md"


OPCODES = {
    0x01: "MOVI",
    0x02: "ADD",
    0x03: "ADDI",
    0x04: "MUL",
    0x05: "BLT",
    0x06: "OUT",
    0xFF: "HALT",
}
OP_BY_NAME = {value: key for key, value in OPCODES.items()}


@dataclass(frozen=True)
class Instr:
    opname: str
    a: int = 0
    b: int = 0
    c: int = 0

    def encode(self) -> bytes:
        return bytes([OP_BY_NAME[self.opname], self.a & 0xFF, self.b & 0xFF, self.c & 0xFF])


PROGRAM = [
    Instr("MOVI", 0, 0, 0),  # r0 = total
    Instr("MOVI", 1, 0, 0),  # r1 = i
    Instr("MOVI", 2, 0, 8),  # r2 = limit
    Instr("MOVI", 3, 0, 1),  # r3 = one
    Instr("MUL", 4, 1, 1),   # loop: r4 = i*i
    Instr("ADD", 0, 0, 4),   # total += r4
    Instr("ADD", 1, 1, 3),   # i += 1
    Instr("BLT", 1, 2, 4),   # if i < limit: goto loop
    Instr("OUT", 0, 0, 0),
    Instr("HALT", 0, 0, 0),
]


def encode_program(program: list[Instr] = PROGRAM) -> bytes:
    return b"".join(instr.encode() for instr in program)


def decode_program(blob: bytes) -> list[Instr]:
    if len(blob) % 4:
        raise ValueError("tiny RISC object length must be a multiple of 4 bytes")
    out = []
    for pc in range(0, len(blob), 4):
        opcode, a, b, c = blob[pc : pc + 4]
        if opcode not in OPCODES:
            raise ValueError(f"unknown opcode 0x{opcode:02x} at byte {pc}")
        out.append(Instr(OPCODES[opcode], a, b, c))
    return out


def point_from_event(seed: str) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % len(hn.POINTS)


def route_for_event(step: int, pc: int, instr: Instr, lookup: dict[tuple[int, int], int]) -> dict[str, Any]:
    src_idx = point_from_event(f"tiny-risc:{step}:{pc}:{instr.opname}:src")
    dst_idx = point_from_event(f"tiny-risc:{step}:{pc}:{instr.a}:{instr.b}:{instr.c}:dst")
    if src_idx == dst_idx:
        dst_idx = (dst_idx + 1) % len(hn.POINTS)
    route = hn.route(hn.POINTS[src_idx], hn.POINTS[dst_idx])
    route_indices = [hn.POINTS.index(point) for point in route]
    return {
        "source": point_id(hn.POINTS[src_idx]),
        "destination": point_id(hn.POINTS[dst_idx]),
        "route": [point_id(point) for point in route],
        "hops": len(route_indices) - 1,
        "line_buses": [
            lookup[(left, right)] for left, right in zip(route_indices, route_indices[1:])
        ],
        "microframe": step // 16,
        "q6_body_edge": step % 16,
        "body_ticks": [3 * step + offset for offset in range(3)],
    }


def execute(program: list[Instr]) -> dict[str, Any]:
    lookup = line_lookup(all_lines())
    registers = [0] * 8
    output: list[int] = []
    trace = []
    pc = 0
    step = 0
    while 0 <= pc < len(program):
        if step > 10_000:
            raise AssertionError("tiny RISC program did not halt")
        instr = program[pc]
        next_pc = pc + 1
        if instr.opname == "MOVI":
            registers[instr.a % len(registers)] = instr.c
        elif instr.opname == "ADD":
            registers[instr.a % len(registers)] = (
                registers[instr.b % len(registers)] + registers[instr.c % len(registers)]
            )
        elif instr.opname == "ADDI":
            registers[instr.a % len(registers)] = registers[instr.b % len(registers)] + instr.c
        elif instr.opname == "MUL":
            registers[instr.a % len(registers)] = (
                registers[instr.b % len(registers)] * registers[instr.c % len(registers)]
            )
        elif instr.opname == "BLT":
            if registers[instr.a % len(registers)] < registers[instr.b % len(registers)]:
                next_pc = instr.c
        elif instr.opname == "OUT":
            output.append(registers[instr.a % len(registers)])
        elif instr.opname == "HALT":
            trace.append(
                {
                    "step": step,
                    "pc": pc,
                    "opname": instr.opname,
                    "args": [instr.a, instr.b, instr.c],
                    "registers": registers.copy(),
                    "output": output.copy(),
                    **route_for_event(step, pc, instr, lookup),
                }
            )
            break
        else:
            raise NotImplementedError(instr.opname)
        trace.append(
            {
                "step": step,
                "pc": pc,
                "opname": instr.opname,
                "args": [instr.a, instr.b, instr.c],
                "registers": registers.copy(),
                "output": output.copy(),
                **route_for_event(step, pc, instr, lookup),
            }
        )
        pc = next_pc
        step += 1
    return {"registers": registers, "output": output, "trace": trace}


def build_payload() -> dict[str, Any]:
    blob = encode_program()
    decoded = decode_program(blob)
    object_record = page_records("tiny_risc_sum_squares_object", blob)
    execution = execute(decoded)
    trace = execution["trace"]
    checks = {
        "object_roundtrip": object_record["roundtrip_matches"],
        "decoded_program_matches": decoded == PROGRAM,
        "result_is_140": execution["output"] == [140],
        "program_halts": trace[-1]["opname"] == "HALT",
        "dynamic_trace_expands_static_program": len(trace) > len(PROGRAM),
        "all_routes_diameter_two": all(row["hops"] <= 2 for row in trace),
        "all_hops_have_line_buses": all(len(row["line_buses"]) == row["hops"] for row in trace),
        "q6_edges_in_range": all(0 <= row["q6_body_edge"] < 16 for row in trace),
    }
    return {
        "schema": "w33.tiny_risc_packet_isa.v1",
        "theorem": "fixed-width binary ISA object executes as routed W33 packet events",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "isa": {
            "instruction_width_bytes": 4,
            "register_count": 8,
            "opcodes": OPCODES,
        },
        "object": {
            "byte_len": object_record["byte_len"],
            "trit_len": object_record["trit_len"],
            "page_count": object_record["page_count"],
            "sha256": object_record["sha256"],
            "roundtrip_matches": object_record["roundtrip_matches"],
            "page_points": [page["point_label"] for page in object_record["pages"]],
        },
        "static_program": [
            {"pc": pc, "opname": instr.opname, "args": [instr.a, instr.b, instr.c]}
            for pc, instr in enumerate(PROGRAM)
        ],
        "execution": {
            "result": execution["output"],
            "dynamic_steps": len(trace),
            "trace_preview": trace[:48],
            "trace_tail": trace[-12:],
            "max_route_hops": max(row["hops"] for row in trace),
        },
        "checks": checks,
        "interpretation": (
            "The wrapper does not have to stop at Python bytecode. A fixed-width "
            "binary object can be loaded as reversible trit pages, decoded into a "
            "small ISA, executed as dynamic packet events, and routed by W33."
        ),
        "honesty_boundary": (
            "This is a deliberately tiny teaching ISA. It is not a WASM, ELF, or "
            "native x86/ARM translator yet, but it fixes the loader/decoder/VM "
            "contract needed for one."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for row in payload["static_program"]:
        rows.append("| {pc} | {opname} | `{args}` |".format(**row))
    return f"""# W(3,3) Tiny RISC Packet ISA

This witness lowers the wrapper below Python bytecode. A fixed-width binary
object is loaded through the reversible trit-page loader, decoded into a tiny
register ISA, executed as dynamic packet events, and routed through W33.

Object bytes: `{payload['object']['byte_len']}`. Trit pages:
`{payload['object']['page_count']}`. Dynamic packet events:
`{payload['execution']['dynamic_steps']}`. Result: `{payload['execution']['result']}`.

| PC | Op | Args |
|---:|---|---|
{chr(10).join(rows)}

Boundary: this is a compact binary-ISA witness, not a native x86/ARM/WASM
translator yet.
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
        "tiny-risc: bytes={byte_len}, pages={page_count}, dynamic_steps={steps}, result={result}".format(
            byte_len=payload["object"]["byte_len"],
            page_count=payload["object"]["page_count"],
            steps=payload["execution"]["dynamic_steps"],
            result=payload["execution"]["result"],
        )
    )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
