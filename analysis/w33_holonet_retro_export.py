#!/usr/bin/env python3
"""Pass 49 - export the Holonet router as retro machine artifacts.

Pass 48 proved that the W(3,3) router compiles to small 4-bit and
6502-style 8-bit machines.  This pass makes the compiler layer inspectable:
it writes deterministic assembly listings and golden traces, then adds a
second 8-bit accumulator target with Z80-style mnemonics.

The target listings are intentionally "style" listings.  They are canonical
Holonet assembly exports for these machine families, not vendor assembler
input promised to assemble unmodified on historical silicon.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import w33_holonet_asm as pass48

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = ROOT / "artifacts" / "holonet_asm"
OUT = ROOT / "data" / "w33_holonet_retro_export.json"

SAMPLE_X = (1, 0, 0, 0)
SAMPLE_Y = (0, 1, 0, 0)


def render_4004_listing() -> str:
    lines = [
        "; Pass 49 Holonet router export: 4004-flavoured 4-bit target",
        "; RAM $0..$3 = source address x0..x3",
        "; RAM $4..$7 = destination address y0..y3",
        "; RAM $8 = B(x,y) mod 3",
        "; This target keeps Pass 47's primitive MUL and MOD3 opcodes.",
        "",
    ]
    for pc, inst in enumerate(pass48.FOUR_BIT_PROGRAM):
        op, *args = inst
        if op == "LDI":
            text = f"LDI R{args[0]}, #{args[1]}"
        elif op == "LD":
            text = f"LD  R{args[0]}, ${args[1]:02X}"
        elif op == "ST":
            text = f"ST  ${args[1]:02X}, R{args[0]}"
        elif op in {"MUL", "ADD", "SUB"}:
            text = f"{op:<4}R{args[0]}, R{args[1]}"
        elif op == "MOD3":
            text = f"MOD3 R{args[0]}"
        elif op == "HLT":
            text = "HLT"
        else:
            raise ValueError(f"unknown 4-bit op {op}")
        lines.append(f"{pc:04X}: {text}")
    return "\n".join(lines) + "\n"


def run_4004_trace(mem: list[int]) -> tuple[int, list[dict[str, Any]]]:
    cpu = pass48.CPU4()
    cpu.r = [0] * 16
    cpu.ram = [0] * 16
    for i, value in enumerate(mem):
        cpu.ram[i] = value & 0xF
    trace: list[dict[str, Any]] = []
    pc = 0
    while pc < len(pass48.FOUR_BIT_PROGRAM):
        inst = pass48.FOUR_BIT_PROGRAM[pc]
        trace.append(
            {
                "pc": pc,
                "op": list(inst),
                "registers_before": cpu.r[:],
                "ram_before": cpu.ram[:9],
            }
        )
        op = inst[0]
        cpu.cycles += 1
        if op == "HLT":
            break
        if op == "LDI":
            cpu.r[inst[1]] = inst[2] & 0xF
        elif op == "LD":
            cpu.r[inst[1]] = cpu.ram[inst[2]] & 0xF
        elif op == "ST":
            cpu.ram[inst[2]] = cpu.r[inst[1]] & 0xF
        elif op == "MUL":
            cpu.r[inst[1]] = (cpu.r[inst[1]] * cpu.r[inst[2]]) & 0xF
        elif op == "ADD":
            cpu.r[inst[1]] = (cpu.r[inst[1]] + cpu.r[inst[2]]) & 0xF
        elif op == "SUB":
            cpu.r[inst[1]] = (cpu.r[inst[1]] - cpu.r[inst[2]]) & 0xF
        elif op == "MOD3":
            cpu.r[inst[1]] %= 3
        else:
            raise ValueError(f"unknown 4-bit op {op}")
        pc += 1
    return cpu.ram[8] % 3, trace


def render_6502_listing() -> str:
    lines = [
        "; Pass 49 Holonet router export: 6502-style accumulator target",
        "; No MUL and no MOD3.  Arithmetic is synthesized from load/store,",
        "; add/subtract, compare, and branches.",
        "",
    ]
    lines.extend(pass48.router_6502_source())
    return "\n".join(lines) + "\n"


@dataclass
class Z80Program:
    source: list[str]
    instructions: list[tuple[Any, ...]]
    labels: dict[str, int]


class Z80Builder:
    def __init__(self) -> None:
        self.source: list[str] = []

    def emit(self, line: str) -> None:
        self.source.append(line)

    def label(self, name: str) -> None:
        self.source.append(f"{name}:")

    def reduce3(self, cell: int, prefix: str) -> None:
        self.label(f"{prefix}_reduce")
        self.emit(f"LD A, (${cell:02X})")
        self.emit("CP #3")
        self.emit(f"JP C, {prefix}_done")
        self.emit("SUB #3")
        self.emit(f"LD (${cell:02X}), A")
        self.emit(f"JP {prefix}_reduce")
        self.label(f"{prefix}_done")

    def mul3(self, dst: int, a: int, b: int, cnt: int, prefix: str) -> None:
        self.emit("LD A, #0")
        self.emit(f"LD (${dst:02X}), A")
        self.emit(f"LD A, (${b:02X})")
        self.emit(f"LD (${cnt:02X}), A")
        self.label(f"{prefix}_loop")
        self.emit(f"LD A, (${cnt:02X})")
        self.emit("CP #0")
        self.emit(f"JP Z, {prefix}_done")
        self.emit(f"LD A, (${dst:02X})")
        self.emit(f"ADD A, (${a:02X})")
        self.emit(f"LD (${dst:02X}), A")
        self.emit(f"LD A, (${cnt:02X})")
        self.emit("SUB #1")
        self.emit(f"LD (${cnt:02X}), A")
        self.emit(f"JP {prefix}_loop")
        self.label(f"{prefix}_done")
        self.reduce3(dst, f"{prefix}_mod")

    def add3(self, dst: int, src: int, prefix: str) -> None:
        self.emit(f"LD A, (${dst:02X})")
        self.emit(f"ADD A, (${src:02X})")
        self.emit(f"LD (${dst:02X}), A")
        self.reduce3(dst, prefix)

    def sub3(self, dst: int, src: int, prefix: str) -> None:
        self.emit(f"LD A, (${dst:02X})")
        self.emit("ADD A, #3")
        self.emit(f"SUB (${src:02X})")
        self.emit(f"LD (${dst:02X}), A")
        self.reduce3(dst, prefix)


def build_z80_source() -> list[str]:
    b = Z80Builder()
    b.source.extend(
        [
            "; Pass 49 Holonet router export: Z80-style accumulator target",
            "; RAM $00..$03 = source address x0..x3",
            "; RAM $04..$07 = destination address y0..y3",
            "; RAM $08 = B(x,y) mod 3",
            "; RAM $09/$0A/$0B/$0C = pos/neg/tmp/counter scratch",
            "",
        ]
    )
    b.mul3(9, 0, 5, 12, "x0y1")
    b.mul3(11, 2, 7, 12, "x2y3")
    b.add3(9, 11, "pos")
    b.mul3(10, 1, 4, 12, "x1y0")
    b.mul3(11, 3, 6, 12, "x3y2")
    b.add3(10, 11, "neg")
    b.emit("LD A, ($09)")
    b.emit("LD ($08), A")
    b.sub3(8, 10, "result")
    b.emit("HALT")
    return b.source


def assemble_z80(source: list[str]) -> Z80Program:
    labels: dict[str, int] = {}
    pending: list[tuple[Any, ...]] = []
    pc = 0
    for raw in source:
        line = raw.split(";", 1)[0].strip()
        if not line:
            continue
        if line.endswith(":"):
            labels[line[:-1]] = pc
            continue
        op = line.split()[0].upper()
        if op == "HALT":
            pending.append(("HALT",))
        elif line.startswith("LD A, #"):
            pending.append(("LD_A_IMM", int(line.split("#", 1)[1])))
        elif line.startswith("LD A, ($"):
            pending.append(("LD_A_MEM", int(line.split("$", 1)[1].split(")")[0], 16)))
        elif line.startswith("LD ($"):
            pending.append(("LD_MEM_A", int(line.split("$", 1)[1].split(")")[0], 16)))
        elif line.startswith("ADD A, #"):
            pending.append(("ADD_IMM", int(line.split("#", 1)[1])))
        elif line.startswith("ADD A, ($"):
            pending.append(("ADD_MEM", int(line.split("$", 1)[1].split(")")[0], 16)))
        elif line.startswith("SUB #"):
            pending.append(("SUB_IMM", int(line.split("#", 1)[1])))
        elif line.startswith("SUB ($"):
            pending.append(("SUB_MEM", int(line.split("$", 1)[1].split(")")[0], 16)))
        elif line.startswith("CP #"):
            pending.append(("CP_IMM", int(line.split("#", 1)[1])))
        elif line.startswith("JP Z,"):
            pending.append(("JP_Z", line.split(",", 1)[1].strip()))
        elif line.startswith("JP C,"):
            pending.append(("JP_C", line.split(",", 1)[1].strip()))
        elif line.startswith("JP "):
            pending.append(("JP", line.split(None, 1)[1].strip()))
        else:
            raise ValueError(f"cannot assemble Z80-style line: {raw}")
        pc += 1
    resolved = []
    for inst in pending:
        op, *args = inst
        resolved.append(
            tuple([op, *[labels.get(a, a) if isinstance(a, str) else a for a in args]])
        )
    return Z80Program(source=source, instructions=resolved, labels=labels)


class Z80StyleCPU:
    def __init__(self, ram_size: int = 32) -> None:
        self.ram_size = ram_size
        self.reset()

    def reset(self) -> None:
        self.a = 0
        self.zero = False
        self.carry = False
        self.ram = [0] * self.ram_size
        self.steps = 0
        self.trace: list[dict[str, Any]] = []

    def run(
        self, program: list[tuple[Any, ...]], mem: list[int], keep_trace: bool = False
    ) -> int:
        self.reset()
        for i, value in enumerate(mem):
            self.ram[i] = value & 0xFF
        pc = 0
        while pc < len(program):
            inst = program[pc]
            op = inst[0]
            if keep_trace:
                self.trace.append(
                    {
                        "pc": pc,
                        "op": list(inst),
                        "a_before": self.a,
                        "ram_before": self.ram[:13],
                    }
                )
            self.steps += 1
            if op == "HALT":
                break
            if op == "LD_A_IMM":
                self.a = inst[1] & 0xFF
            elif op == "LD_A_MEM":
                self.a = self.ram[inst[1]]
            elif op == "LD_MEM_A":
                self.ram[inst[1]] = self.a & 0xFF
            elif op == "ADD_IMM":
                self.a = (self.a + inst[1]) & 0xFF
            elif op == "ADD_MEM":
                self.a = (self.a + self.ram[inst[1]]) & 0xFF
            elif op == "SUB_IMM":
                self.a = (self.a - inst[1]) & 0xFF
            elif op == "SUB_MEM":
                self.a = (self.a - self.ram[inst[1]]) & 0xFF
            elif op == "CP_IMM":
                value = inst[1]
                self.zero = self.a == value
                self.carry = self.a < value
            elif op == "JP_Z":
                if self.zero:
                    pc = inst[1]
                    continue
            elif op == "JP_C":
                if self.carry:
                    pc = inst[1]
                    continue
            elif op == "JP":
                pc = inst[1]
                continue
            else:
                raise ValueError(f"unknown Z80-style op {op}")
            pc += 1
        return self.ram[8] % 3


def verify_z80(program: list[tuple[Any, ...]]) -> dict[str, Any]:
    cpu = Z80StyleCPU()
    ok = True
    max_steps = 0
    for x in pass48.POINTS:
        for y in pass48.POINTS:
            result = cpu.run(program, [*x, *y, 0, 0, 0, 0, 0])
            ok = ok and result == pass48.ref_b(x, y)
            max_steps = max(max_steps, cpu.steps)
    return {
        "verified_pairs": len(pass48.POINTS) ** 2,
        "matches_reference": ok,
        "max_instruction_steps": max_steps,
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def build_certificate() -> dict[str, Any]:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    pass48_cert = pass48.build_certificate()
    z80_source = build_z80_source()
    z80_program = assemble_z80(z80_source)
    z80_verify = verify_z80(z80_program.instructions)

    sample_mem = [*SAMPLE_X, *SAMPLE_Y, 0, 0, 0, 0, 0]
    sample_expected = pass48.ref_b(SAMPLE_X, SAMPLE_Y)

    result4, trace4 = run_4004_trace(sample_mem)

    asm8 = pass48.assemble_6502(pass48.router_6502_source())
    cpu6502 = pass48.CPU8()
    result6502 = cpu6502.run(asm8.instructions, sample_mem)

    cpuz80 = Z80StyleCPU()
    resultz80 = cpuz80.run(z80_program.instructions, sample_mem, keep_trace=True)

    artifact_paths = {
        "router_4004_style": ARTIFACT_DIR / "router_4004_style.asm",
        "router_6502_style": ARTIFACT_DIR / "router_6502_style.asm",
        "router_z80_style": ARTIFACT_DIR / "router_z80_style.asm",
        "trace_4004_style": ARTIFACT_DIR / "golden_trace_4004_style.json",
        "trace_6502_style": ARTIFACT_DIR / "golden_trace_6502_style.json",
        "trace_z80_style": ARTIFACT_DIR / "golden_trace_z80_style.json",
        "readme": ARTIFACT_DIR / "README.md",
    }

    artifact_paths["router_4004_style"].write_text(
        render_4004_listing(), encoding="utf-8"
    )
    artifact_paths["router_6502_style"].write_text(
        render_6502_listing(), encoding="utf-8"
    )
    artifact_paths["router_z80_style"].write_text(
        "\n".join(z80_source) + "\n", encoding="utf-8"
    )

    sample = {
        "source": list(SAMPLE_X),
        "destination": list(SAMPLE_Y),
        "expected_B_mod_3": sample_expected,
        "interpretation": "nonzero means a direct W(3,3) edge",
    }
    write_json(
        artifact_paths["trace_4004_style"],
        {"target": "4004-style", "sample": sample, "result": result4, "trace": trace4},
    )
    write_json(
        artifact_paths["trace_6502_style"],
        {
            "target": "6502-style",
            "sample": sample,
            "result": result6502,
            "trace": [
                {"pc": pc, "op": list(inst), "a_before": a}
                for pc, inst, a in cpu6502.trace
            ],
        },
    )
    write_json(
        artifact_paths["trace_z80_style"],
        {
            "target": "Z80-style",
            "sample": sample,
            "result": resultz80,
            "trace": cpuz80.trace,
        },
    )
    artifact_paths["readme"].write_text(
        "\n".join(
            [
                "# Holonet Assembly Exports",
                "",
                "Pass 49 exports the W(3,3) symplectic router into three deterministic",
                "retro machine listings plus golden traces for the same sample route.",
                "",
                "- `router_4004_style.asm`: 4-bit listing with primitive `MUL` and `MOD3`.",
                "- `router_6502_style.asm`: 6502-style accumulator listing with synthesized arithmetic.",
                "- `router_z80_style.asm`: Z80-style accumulator listing with synthesized arithmetic.",
                "- `golden_trace_*_style.json`: sample execution traces for `1000 -> 0100`.",
                "",
                "These are canonical Holonet target listings, not vendor-assembler promises.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    checks = {
        "pass48_still_verified": pass48_cert["verified"] is True,
        "z80_target_verified": z80_verify["matches_reference"] is True
        and z80_verify["verified_pairs"] == 1600,
        "sample_agrees_across_targets": result4
        == result6502
        == resultz80
        == sample_expected,
        "artifacts_written": all(
            path.exists() and path.stat().st_size > 0
            for path in artifact_paths.values()
        ),
        "z80_has_no_mul_or_mod_opcode": all(
            "MUL" not in line and "MOD3" not in line
            for line in z80_source
            if not line.strip().startswith(";")
        ),
    }

    return {
        "theorem": "Pass 49 Holonet retro target export",
        "verified": all(checks.values()),
        "breakthrough": (
            "The Holonet router is no longer only an emulator proof: it now has "
            "deterministic assembly-style export artifacts and golden traces for "
            "4-bit, 6502-style, and Z80-style targets.  The Z80-style target is "
            "independently verified on all 1600 ordered W33 address pairs with "
            "MUL and MOD3 synthesized away."
        ),
        "sample_route": sample,
        "targets": {
            "4004_style": {
                "instructions": len(pass48.FOUR_BIT_PROGRAM),
                "sample_result": result4,
                "artifact": str(artifact_paths["router_4004_style"].relative_to(ROOT)),
                "trace": str(artifact_paths["trace_4004_style"].relative_to(ROOT)),
                "claim_boundary": "4-bit Holonet ISA with primitive MUL and MOD3, matching Pass 47.",
            },
            "6502_style": {
                "instructions": pass48_cert["eight_bit_6502_style_target"][
                    "program_instructions"
                ],
                "max_instruction_steps": pass48_cert["eight_bit_6502_style_target"][
                    "max_instruction_steps"
                ],
                "sample_result": result6502,
                "artifact": str(artifact_paths["router_6502_style"].relative_to(ROOT)),
                "trace": str(artifact_paths["trace_6502_style"].relative_to(ROOT)),
                "claim_boundary": "6502-style accumulator semantics, not cycle-accurate MOS 6502.",
            },
            "z80_style": {
                "instructions": len(z80_program.instructions),
                **z80_verify,
                "sample_result": resultz80,
                "artifact": str(artifact_paths["router_z80_style"].relative_to(ROOT)),
                "trace": str(artifact_paths["trace_z80_style"].relative_to(ROOT)),
                "claim_boundary": "Z80-style accumulator/control-flow semantics, not vendor-cycle timing.",
            },
        },
        "artifact_directory": str(ARTIFACT_DIR.relative_to(ROOT)),
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_json(OUT, cert)
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    for name, target in cert["targets"].items():
        print(
            f"  {name}: {target['instructions']} instructions, "
            f"sample={target['sample_result']}, artifact={target['artifact']}"
        )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
