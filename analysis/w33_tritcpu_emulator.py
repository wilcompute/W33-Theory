#!/usr/bin/env python3
"""
Boots on a dinosaur, literally: the holonet router as a 22-instruction program executed on an emulated
4-bit CPU. Pass 46 argued the node's minimal instruction set is three mod-3 primitives; this pass makes
"runs on a 1970s 4-bit CPU" concrete by building such a CPU -- a tiny Intel-4004-flavoured machine with
sixteen 4-bit registers, a small RAM, and a handful of opcodes (load-immediate, load, store, add,
subtract, multiply, reduce-mod-3, halt) -- assembling the holonet forwarding test as a program for it,
and EXECUTING it instruction by instruction with a full trace. The program is 22 instructions: it loads
the two 4-digit addresses from memory, forms the positive part (x0 y1 + x2 y3) mod 3 and the negative
part (x1 y0 + x3 y2) mod 3, subtracts them mod 3, and stores the result -- every value stays in the
4-bit range 0..15, so a 4-bit datapath suffices with room to spare. We run it for all 1600 ordered node
pairs and it reproduces the reference adjacency exactly, in 22 cycles per routing decision. Costed
against the real Intel 4004 (1971, ~740 kHz, ~8 clocks per instruction), that is about 240 microseconds
per routing decision -- roughly four thousand holonet routes per second on a fifty-year-old four-bit
chip. So "the architecture of life boots on a dinosaur" is not a figure of speech: here is the
assembled program and the executed instruction trace, and the only thing the chip cannot supply is the
quantum advantage (the priced 9^t magic), which needs photons, not silicon. The classical machine --
routing, the address-is-route forwarding, the whole network/memory layer -- runs on hardware older than
the people using it.

This builds a 4-bit CPU emulator, assembles the holonet forwarding test (B(x,y) mod 3) as a 22-instruction
program, executes it with a trace, verifies it on all 1600 node pairs, and costs one routing decision on
a real Intel 4004.

THE EMULATION.
    CPU            16 4-bit registers, small RAM; opcodes {LDI, LD, ST, ADD, SUB, MUL, MOD3, HLT}.
    program        22 instructions: B = ((x0 y1 + x2 y3) - (x1 y0 + x3 y2)) mod 3, all values in 0..15.
    correctness    reproduces the reference adjacency for all 1600 ordered node pairs.
    cost           22 cycles/decision; on a 1971 Intel 4004 (~740 kHz, ~8 clk/instr) ~240 us/decision,
                   ~4000 routes/sec on a 4-bit chip.

Honest scope: the CPU emulator is a faithful 4-bit register machine; the program uses only its small
opcode set and is verified to reproduce the reference adjacency on all 1600 pairs (computed here). The
4004 timing (~740 kHz, ~8 clocks/instruction) is the historical figure, giving an order-of-magnitude
wall-clock, not a cycle-accurate 4004 port. This is the classical routing/forwarding layer; the quantum
advantage still needs a physical photonic substrate (the priced 9^t magic, not run here). So: the
holonet router, assembled and executed on a four-bit machine.

Verifies that the holonet forwarding test runs as a 22-instruction program on a 4-bit CPU, reproduces
the reference adjacency on all 1600 pairs, and costs ~240 us per decision on a 1971 Intel 4004.
"""
from __future__ import annotations

import itertools
import json


class TritCPU:
    """A minimal 4-bit register machine (Intel-4004-flavoured): 16 regs, small RAM, a tiny opcode set."""

    def __init__(self, ram=32):
        self.r = [0] * 16
        self.ram = [0] * ram
        self.cycles = 0
        self.trace = []

    def run(self, prog, mem):
        for i, v in enumerate(mem):
            self.ram[i] = v & 0xF
        pc = 0
        while pc < len(prog):
            op = prog[pc]
            name = op[0]
            self.cycles += 1
            if name == "HLT":
                self.trace.append((pc, "HLT", ()))
                break
            elif name == "LDI":
                self.r[op[1]] = op[2] & 0xF
            elif name == "LD":
                self.r[op[1]] = self.ram[op[2]] & 0xF
            elif name == "ST":
                self.ram[op[2]] = self.r[op[1]] & 0xF
            elif name == "MUL":
                self.r[op[1]] = (self.r[op[1]] * self.r[op[2]]) & 0xF
            elif name == "ADD":
                self.r[op[1]] = (self.r[op[1]] + self.r[op[2]]) & 0xF
            elif name == "SUB":
                self.r[op[1]] = (self.r[op[1]] - self.r[op[2]]) & 0xF
            elif name == "MOD3":
                self.r[op[1]] = self.r[op[1]] % 3
            self.trace.append((pc, name, tuple(op[1:])))
            pc += 1
        return self.ram[8]


# The holonet forwarding test B(x,y) = (x0 y1 + x2 y3) - (x1 y0 + x3 y2) (mod 3), as 4-bit assembly.
# x at RAM[0..3], y at RAM[4..7], result at RAM[8]. All intermediates stay in 0..15.
PROGRAM = [
    ("LD", 0, 0),
    ("LD", 1, 5),
    ("MUL", 0, 1),  # R0 = x0*y1
    ("LD", 2, 2),
    ("LD", 3, 7),
    ("MUL", 2, 3),
    ("ADD", 0, 2),
    ("MOD3", 0),  # R0 = (x0y1 + x2y3) mod 3  [pos]
    ("LD", 4, 1),
    ("LD", 5, 4),
    ("MUL", 4, 5),  # R4 = x1*y0
    ("LD", 6, 3),
    ("LD", 7, 6),
    ("MUL", 6, 7),
    ("ADD", 4, 6),
    ("MOD3", 4),  # R4 = (x1y0 + x3y2) mod 3  [neg]
    ("LDI", 8, 3),
    ("SUB", 8, 4),  # R8 = 3 - neg
    ("ADD", 0, 8),
    ("MOD3", 0),  # R0 = (pos + 3 - neg) mod 3 = B
    ("ST", 0, 8),
    ("HLT",),
]


def main():
    out = {}
    print(
        "== boots on a dinosaur, literally: the holonet router as a 4-bit-CPU program =="
    )

    inv = {1: 1, 2: 2}

    def norm(v):
        for c in v:
            if c != 0:
                return tuple((x * inv[c]) % 3 for x in v)

    pts = sorted({norm(v) for v in itertools.product(range(3), repeat=4) if any(v)})

    def refB(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3

    ok = True
    max_cycles = 0
    for i in range(40):
        for j in range(40):
            cpu = TritCPU()
            res = cpu.run(PROGRAM, list(pts[i]) + list(pts[j]) + [0, 0])
            max_cycles = max(max_cycles, cpu.cycles)
            if res != refB(pts[i], pts[j]):
                ok = False
    print(
        f"\n[CPU]        16 4-bit registers + RAM; opcodes {{LDI, LD, ST, ADD, SUB, MUL, MOD3, HLT}}"
    )
    print(
        f"[program]    {len(PROGRAM)} instructions: B = ((x0y1+x2y3) - (x1y0+x3y2)) mod 3 (all values in 0..15)"
    )
    print(
        f"[correct]    reproduces the reference adjacency for all 1600 node pairs: {ok}"
    )
    print(f"[cost]       {max_cycles} cycles per routing decision")
    assert ok and max_cycles == len(PROGRAM)
    out["cpu"] = {
        "registers": 16,
        "bits": 4,
        "opcodes": ["LDI", "LD", "ST", "ADD", "SUB", "MUL", "MOD3", "HLT"],
    }
    out["program_instructions"] = len(PROGRAM)
    out["verified_pairs"] = 1600
    out["cycles_per_decision"] = max_cycles

    # cost on a real Intel 4004 (1971): ~740 kHz, ~8 clocks/instruction
    clk_hz, clk_per_instr = 740_000, 8
    us_per_instr = clk_per_instr / clk_hz * 1e6
    us_per_decision = max_cycles * us_per_instr
    routes_per_sec = 1e6 / us_per_decision
    print(
        f"\n[Intel 4004] 1971, ~740 kHz, ~8 clk/instr -> ~{us_per_decision:.0f} us per routing decision (~{routes_per_sec:.0f} routes/sec)"
    )
    out["intel_4004"] = {
        "clock_hz": clk_hz,
        "us_per_decision": round(us_per_decision, 1),
        "routes_per_sec": round(routes_per_sec),
    }

    # a sample trace for one pair
    cpu = TritCPU()
    cpu.run(PROGRAM, list(pts[0]) + list(pts[3]) + [0, 0])
    print(f"\n[trace]      first 8 executed instructions for {pts[0]} vs {pts[3]}:")
    for step in cpu.trace[:8]:
        print(f"               pc={step[0]:2d}  {step[1]:4s} {step[2]}")
    out["sample_trace_first8"] = [[s[0], s[1], list(s[2])] for s in cpu.trace[:8]]

    print(
        "\nRESULT: 'the architecture of life boots on a dinosaur' is now literal. We built a tiny 4-bit"
    )
    print(
        "  CPU -- sixteen 4-bit registers, a small RAM, and the opcodes load/store/add/subtract/multiply/"
    )
    print(
        "  reduce-mod-3 -- assembled the holonet forwarding test as a 22-instruction program (the address-"
    )
    print(
        "  is-route symplectic form, with every value staying inside the 4-bit range), and executed it"
    )
    print(
        "  instruction by instruction. It reproduces the reference adjacency for all 1600 node pairs in 22"
    )
    print(
        "  cycles per decision. On the real Intel 4004 (1971, ~740 kHz) that is about 240 microseconds"
    )
    print(
        "  per routing decision -- roughly four thousand holonet routes per second on a fifty-year-old"
    )
    print(
        "  four-bit chip. So the classical machine -- routing, forwarding, the whole network/memory layer"
    )
    print(
        "  -- runs on hardware older than its users; the only thing the chip cannot supply is the quantum"
    )
    print(
        "  advantage (the priced 9^t magic), which needs photons. Honest: a faithful 4-bit register"
    )
    print(
        "  machine, the program verified on all 1600 pairs; the 4004 timing is the historical figure"
    )
    print("  (order-of-magnitude wall-clock, not a cycle-accurate port).")

    out["summary"] = (
        "boots on a dinosaur, literally: the holonet router as a 22-instruction program executed on an "
        "emulated 4-bit CPU. We built a minimal Intel-4004-flavoured machine (16 4-bit registers, small "
        "RAM, opcodes {LDI, LD, ST, ADD, SUB, MUL, MOD3, HLT}), assembled the holonet forwarding test "
        "B(x,y) = ((x0y1+x2y3) - (x1y0+x3y2)) mod 3 as a 22-instruction program (all intermediates in "
        "0..15, so a 4-bit datapath suffices), and executed it with a full instruction trace. It "
        "reproduces the reference adjacency for all 1600 ordered node pairs in 22 cycles per routing "
        "decision; on the real 1971 Intel 4004 (~740 kHz, ~8 clk/instr) that is ~240 us/decision, ~4000 "
        "routes/sec on a fifty-year-old 4-bit chip. So 'the architecture of life boots on a dinosaur' is "
        "literal -- the classical routing/forwarding/network/memory layer runs on hardware older than "
        "its users; only the quantum advantage (the priced 9^t magic) needs photons. HONEST: the CPU "
        "emulator is a faithful 4-bit register machine and the program uses only its small opcode set "
        "(verified on all 1600 pairs); the 4004 timing is the historical figure (order-of-magnitude "
        "wall-clock, not a cycle-accurate port); this is the classical layer, the quantum advantage "
        "still needs a physical photonic substrate."
    )
    out["sources"] = [
        "holonet forwarding test B(x,y) mod 3 (the routing layer); minimal instruction set (Pass 46, "
        "w33_minimal_architecture); Intel 4004 (1971, 4-bit, ~740 kHz) historical specs; CPU emulator + "
        "assembled program + trace (built/run here)."
    ]
    with open("data/w33_tritcpu_emulator.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_tritcpu_emulator.json")


if __name__ == "__main__":
    main()
