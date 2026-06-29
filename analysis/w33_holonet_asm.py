#!/usr/bin/env python3
"""Pass 48 - Holonet assembler with 4-bit and 6502-style targets.

The router is the symplectic form

    B(x,y) = x0*y1 - x1*y0 + x2*y3 - x3*y2 (mod 3).

Pass 47 showed this fits a 4-bit machine if MUL and MOD3 are primitive
opcodes.  This pass adds a tiny assembler and a stricter 8-bit target where
multiply and mod-3 are synthesized from load/add/subtract/compare/branch.
The 8-bit target is 6502-style, not cycle-accurate MOS 6502.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_holonet_asm.json"

INV3 = {1: 1, 2: 2}


def norm(v: tuple[int, ...]) -> tuple[int, ...] | None:
    for c in v:
        if c != 0:
            return tuple((x * INV3[c]) % 3 for x in v)
    return None


POINTS = sorted(
    {
        p
        for p in (norm(v) for v in itertools.product(range(3), repeat=4) if any(v))
        if p is not None
    }
)


def ref_b(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3


FOUR_BIT_PROGRAM = [
    ("LD", 0, 0),
    ("LD", 1, 5),
    ("MUL", 0, 1),
    ("LD", 2, 2),
    ("LD", 3, 7),
    ("MUL", 2, 3),
    ("ADD", 0, 2),
    ("MOD3", 0),
    ("LD", 4, 1),
    ("LD", 5, 4),
    ("MUL", 4, 5),
    ("LD", 6, 3),
    ("LD", 7, 6),
    ("MUL", 6, 7),
    ("ADD", 4, 6),
    ("MOD3", 4),
    ("LDI", 8, 3),
    ("SUB", 8, 4),
    ("ADD", 0, 8),
    ("MOD3", 0),
    ("ST", 0, 8),
    ("HLT",),
]


@dataclass
class AssembledProgram:
    instructions: list[tuple[Any, ...]]
    labels: dict[str, int]
    source_lines: list[str]


class TinyAssembler:
    """A minimal label assembler for the 6502-style target."""

    def assemble(self, lines: list[str]) -> AssembledProgram:
        labels: dict[str, int] = {}
        pending: list[tuple[Any, ...]] = []
        source_lines: list[str] = []
        pc = 0
        for raw in lines:
            line = raw.split(";", 1)[0].strip()
            if not line:
                continue
            if line.endswith(":"):
                labels[line[:-1]] = pc
                source_lines.append(line)
                continue
            parts = line.replace(",", " ").split()
            op = parts[0].upper()
            args: list[Any] = []
            for token in parts[1:]:
                if token.startswith("#"):
                    args.append(int(token[1:]))
                elif token.startswith("$"):
                    args.append(int(token[1:]))
                elif token.lstrip("-").isdigit():
                    args.append(int(token))
                else:
                    args.append(token)
            pending.append((op, *args))
            source_lines.append(line)
            pc += 1

        resolved: list[tuple[Any, ...]] = []
        for inst in pending:
            op, *args = inst
            out_args = [
                labels[arg] if isinstance(arg, str) and arg in labels else arg
                for arg in args
            ]
            resolved.append((op, *out_args))
        return AssembledProgram(resolved, labels, source_lines)


def reduce3_macro(cell: int, prefix: str) -> list[str]:
    return [
        f"{prefix}_reduce:",
        f"LDA ${cell}",
        "CMP #3",
        f"BCC {prefix}_done",
        "SEC",
        "SBC #3",
        f"STA ${cell}",
        f"JMP {prefix}_reduce",
        f"{prefix}_done:",
    ]


def mul3_macro(dst: int, a: int, b: int, cnt: int, prefix: str) -> list[str]:
    return [
        "LDA #0",
        f"STA ${dst}",
        f"LDA ${b}",
        f"STA ${cnt}",
        f"{prefix}_loop:",
        f"LDA ${cnt}",
        "CMP #0",
        f"BEQ {prefix}_done",
        f"LDA ${dst}",
        "CLC",
        f"ADC ${a}",
        f"STA ${dst}",
        f"LDA ${cnt}",
        "SEC",
        "SBC #1",
        f"STA ${cnt}",
        f"JMP {prefix}_loop",
        f"{prefix}_done:",
        *reduce3_macro(dst, f"{prefix}_mod"),
    ]


def add3_macro(dst: int, src: int, prefix: str) -> list[str]:
    return [
        f"LDA ${dst}",
        "CLC",
        f"ADC ${src}",
        f"STA ${dst}",
        *reduce3_macro(dst, prefix),
    ]


def sub3_macro(dst: int, src: int, prefix: str) -> list[str]:
    return [
        f"LDA ${dst}",
        "CLC",
        "ADC #3",
        "SEC",
        f"SBC ${src}",
        f"STA ${dst}",
        *reduce3_macro(dst, prefix),
    ]


def router_6502_source() -> list[str]:
    # RAM: x0..x3 = 0..3, y0..y3 = 4..7, result=8, pos=9, neg=10, tmp=11, cnt=12.
    lines: list[str] = []
    lines += mul3_macro(9, 0, 5, 12, "x0y1")
    lines += mul3_macro(11, 2, 7, 12, "x2y3")
    lines += add3_macro(9, 11, "pos")
    lines += mul3_macro(10, 1, 4, 12, "x1y0")
    lines += mul3_macro(11, 3, 6, 12, "x3y2")
    lines += add3_macro(10, 11, "neg")
    lines += [
        "LDA $9",
        "STA $8",
    ]
    lines += sub3_macro(8, 10, "result")
    lines += ["HLT"]
    return lines


class CPU4:
    def __init__(self, ram_size: int = 16):
        self.r = [0] * 16
        self.ram = [0] * ram_size
        self.cycles = 0

    def run(self, program: list[tuple[Any, ...]], mem: list[int]) -> int:
        self.r = [0] * 16
        self.ram = [0] * len(self.ram)
        self.cycles = 0
        for i, value in enumerate(mem):
            self.ram[i] = value & 0xF
        pc = 0
        while pc < len(program):
            inst = program[pc]
            op = inst[0]
            self.cycles += 1
            if op == "HLT":
                break
            if op == "LDI":
                self.r[inst[1]] = inst[2] & 0xF
            elif op == "LD":
                self.r[inst[1]] = self.ram[inst[2]] & 0xF
            elif op == "ST":
                self.ram[inst[2]] = self.r[inst[1]] & 0xF
            elif op == "MUL":
                self.r[inst[1]] = (self.r[inst[1]] * self.r[inst[2]]) & 0xF
            elif op == "ADD":
                self.r[inst[1]] = (self.r[inst[1]] + self.r[inst[2]]) & 0xF
            elif op == "SUB":
                self.r[inst[1]] = (self.r[inst[1]] - self.r[inst[2]]) & 0xF
            elif op == "MOD3":
                self.r[inst[1]] %= 3
            else:
                raise ValueError(f"unknown CPU4 op {op}")
            pc += 1
        return self.ram[8] % 3


class CPU8:
    """Small 6502-style accumulator machine."""

    def __init__(self, ram_size: int = 32):
        self.ram_size = ram_size
        self.reset()

    def reset(self) -> None:
        self.a = 0
        self.carry = False
        self.zero = False
        self.ram = [0] * self.ram_size
        self.steps = 0
        self.weighted_cycles = 0
        self.trace: list[tuple[int, tuple[Any, ...], int]] = []

    def _set_flags(self, value: int) -> None:
        self.zero = (value & 0xFF) == 0

    def run(self, program: list[tuple[Any, ...]], mem: list[int]) -> int:
        self.reset()
        for i, value in enumerate(mem):
            self.ram[i] = value & 0xFF
        pc = 0
        while pc < len(program):
            inst = program[pc]
            op = inst[0]
            self.steps += 1
            self.weighted_cycles += {
                "LDA": 3,
                "STA": 3,
                "CLC": 2,
                "SEC": 2,
                "ADC": 3,
                "SBC": 3,
                "CMP": 2,
                "BEQ": 2,
                "BCC": 2,
                "JMP": 3,
                "HLT": 1,
            }[op]
            self.trace.append((pc, inst, self.a))
            if op == "HLT":
                break
            if op == "LDA":
                src = inst[1]
                self.a = (
                    src if isinstance(src, int) and inst[2] == "imm" else self.ram[src]
                )
                self._set_flags(self.a)
            elif op == "STA":
                self.ram[inst[1]] = self.a & 0xFF
            elif op == "CLC":
                self.carry = False
            elif op == "SEC":
                self.carry = True
            elif op == "ADC":
                src = inst[1]
                value = (
                    src if isinstance(src, int) and inst[2] == "imm" else self.ram[src]
                )
                self.a = (self.a + value + (1 if self.carry else 0)) & 0xFF
                self.carry = self.a > 0xFF
                self._set_flags(self.a)
            elif op == "SBC":
                src = inst[1]
                value = (
                    src if isinstance(src, int) and inst[2] == "imm" else self.ram[src]
                )
                borrow = 0 if self.carry else 1
                self.a = (self.a - value - borrow) & 0xFF
                self.carry = self.a >= 0
                self._set_flags(self.a)
            elif op == "CMP":
                value = inst[1]
                self.zero = self.a == value
                self.carry = self.a >= value
            elif op == "BEQ":
                if self.zero:
                    pc = inst[1]
                    continue
            elif op == "BCC":
                if not self.carry:
                    pc = inst[1]
                    continue
            elif op == "JMP":
                pc = inst[1]
                continue
            else:
                raise ValueError(f"unknown CPU8 op {op}")
            pc += 1
        return self.ram[8] % 3


def normalize_6502_instruction(inst: tuple[Any, ...]) -> tuple[Any, ...]:
    op, *args = inst
    if op in {"LDA", "ADC", "SBC"}:
        arg = args[0]
        mode = (
            "imm"
            if isinstance(arg, int) and len(args) == 1 and arg <= 3 and op != "LDA"
            else "mem"
        )
        # The assembler has already turned both #n and $n into ints.  Recover
        # immediate mode from source markers in a narrow way by using source
        # text in assemble_6502 below; this fallback is not used there.
        return (op, arg, mode)
    return inst


def assemble_6502(lines: list[str]) -> AssembledProgram:
    labels: dict[str, int] = {}
    pending: list[tuple[Any, ...]] = []
    source_lines: list[str] = []
    pc = 0
    for raw in lines:
        line = raw.split(";", 1)[0].strip()
        if not line:
            continue
        if line.endswith(":"):
            labels[line[:-1]] = pc
            source_lines.append(line)
            continue
        parts = line.replace(",", " ").split()
        op = parts[0].upper()
        args: list[Any] = []
        for token in parts[1:]:
            if token.startswith("#"):
                args.extend([int(token[1:]), "imm"])
            elif token.startswith("$"):
                args.extend([int(token[1:]), "mem"])
            elif token.lstrip("-").isdigit():
                args.append(int(token))
            else:
                args.append(token)
        pending.append((op, *args))
        source_lines.append(line)
        pc += 1
    resolved = []
    for inst in pending:
        op, *args = inst
        resolved.append(
            tuple([op, *[labels.get(a, a) if isinstance(a, str) else a for a in args]])
        )
    return AssembledProgram(resolved, labels, source_lines)


def verify_target(cpu: Any, program: list[tuple[Any, ...]]) -> dict[str, Any]:
    ok = True
    max_steps = 0
    max_weighted = 0
    for x in POINTS:
        for y in POINTS:
            result = cpu.run(program, [*x, *y, 0, 0, 0, 0, 0])
            ok = ok and result == ref_b(x, y)
            max_steps = max(max_steps, getattr(cpu, "cycles", getattr(cpu, "steps", 0)))
            max_weighted = max(max_weighted, getattr(cpu, "weighted_cycles", 0))
    return {
        "verified_pairs": len(POINTS) ** 2,
        "matches_reference": ok,
        "max_instruction_steps": max_steps,
        "max_weighted_cycles": max_weighted,
    }


def build_certificate() -> dict[str, Any]:
    source = router_6502_source()
    asm8 = assemble_6502(source)
    cpu4 = CPU4()
    cpu8 = CPU8()
    v4 = verify_target(cpu4, FOUR_BIT_PROGRAM)
    v8 = verify_target(cpu8, asm8.instructions)
    sample_cpu = CPU8()
    sample_cpu.run(asm8.instructions, [*POINTS[0], *POINTS[3], 0, 0, 0, 0, 0])
    checks = {
        "forty_projective_addresses": len(POINTS) == 40,
        "four_bit_target_verified": v4["matches_reference"] is True
        and v4["verified_pairs"] == 1600,
        "eight_bit_target_verified": v8["matches_reference"] is True
        and v8["verified_pairs"] == 1600,
        "eight_bit_has_no_mul_or_mod_opcode": all(
            inst[0] not in {"MUL", "MOD3"} for inst in asm8.instructions
        ),
        "eight_bit_synthesizes_arithmetic_from_branches": {
            "ADC",
            "SBC",
            "CMP",
            "BEQ",
            "BCC",
            "JMP",
        }
        <= {inst[0] for inst in asm8.instructions},
    }
    return {
        "theorem": "Pass 48 Holonet assembler targets",
        "verified": all(checks.values()),
        "breakthrough": (
            "The symplectic router now compiles through a tiny holonet-asm layer "
            "to both the 4-bit Pass-47 target and an 8-bit 6502-style target "
            "where MUL and MOD3 are synthesized from add/subtract/compare/branch. "
            "Both targets reproduce B(x,y) mod 3 on all 1600 ordered W33 address pairs."
        ),
        "four_bit_target": {
            "program_instructions": len(FOUR_BIT_PROGRAM),
            **v4,
            "has_mul_mod_primitives": True,
        },
        "eight_bit_6502_style_target": {
            "program_instructions": len(asm8.instructions),
            **v8,
            "primitive_opcodes": sorted({inst[0] for inst in asm8.instructions}),
            "has_mul_mod_primitives": False,
            "sample_trace_first_12": [
                {"pc": pc, "op": list(inst), "a_before": a}
                for pc, inst, a in sample_cpu.trace[:12]
            ],
        },
        "source_excerpt": asm8.source_lines[:40],
        "claim_boundary": [
            "The 8-bit target is 6502-style accumulator semantics, not a cycle-accurate MOS 6502 emulator.",
            "The weighted-cycle count is an internal cost model for this emulator, not a hardware benchmark.",
            "This proves the classical router/compiler layer only; quantum advantage still requires the photonic/magic layer.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(
        f"  4-bit: {cert['four_bit_target']['program_instructions']} instructions, "
        f"{cert['four_bit_target']['max_instruction_steps']} executed steps"
    )
    print(
        f"  8-bit: {cert['eight_bit_6502_style_target']['program_instructions']} instructions, "
        f"{cert['eight_bit_6502_style_target']['max_instruction_steps']} max executed steps"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
