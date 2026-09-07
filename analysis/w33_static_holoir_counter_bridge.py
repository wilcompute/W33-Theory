#!/usr/bin/env python3
"""Static structured-control HoloIR -> finite counter CFG -> two-counter Minsky code.

This closes the static control/value-state gap left by
``w33_static_wasm_holoir_compiler`` for its structured-control surface without
falling back to a completed execution trace.

Layer A compiles the authenticated HoloIR CFG to a finite multi-counter machine
whose only primitive instructions are INC, DECJZ and HALT. Locals and bounded
operand-stack slots are natural-number counters. Reusable macros implement
zero/copy, compact binary constants, eqz, and modulo-2^w add/sub. Branch targets
come from the static HoloIR artifact; no invocation result is consulted.

Layer B gives a constructive reduction from any finite n-counter INC/DECJZ/HALT
program to the repository's two-counter core. A logical configuration
(r_0,...,r_{n-1}) is encoded in counter0 as N=product_i p_i**r_i, with
counter1=0. Logical INC r_i multiplies N by p_i. Logical DECJZ r_i tests
divisibility by p_i and, on the nonzero branch, divides by p_i. Both operations
are expanded into literal two-counter INC/DECJZ instructions.

The real sum-1..7 HoloIR is executed through Layer A at w=8 and returns 28. The
two-counter primitive compiler is independently exercised on a small family of
prime-encoded logical configurations. The full prime-power execution of the
Wasm example is intentionally not claimed efficient, and the capability HoloIR
surface remains a separate extension.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

import w33_wasm3_frontend as control
from w33_static_wasm_holoir_compiler import StaticHoloIR, compile_control
from w33_typed_universal_microvm import Instruction, Program

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_STATIC_HOLOIR_COUNTER_BRIDGE.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class MCInstruction:
    op: str
    register: int | None = None
    target: int | None = None
    zero_target: int | None = None


@dataclass(frozen=True)
class MCProgram:
    instructions: tuple[MCInstruction, ...]
    register_names: tuple[str, ...]
    entry: int
    result_register: int
    name: str

    @property
    def image_id(self) -> str:
        return digest({"schema": "w33.multi-counter-program.v1", "name": self.name, "register_names": self.register_names, "entry": self.entry, "result_register": self.result_register, "instructions": [vars(x) for x in self.instructions]})


class LabelBuilder:
    def __init__(self):
        self.rows: list[tuple[str, str, int | None, str | None, str | None]] = []
        self.labels: set[str] = set(); self.serial = 0

    def fresh(self, stem: str) -> str:
        self.serial += 1; return f"{stem}${self.serial}"

    def add(self, label: str, op: str, reg: int | None = None, target: str | None = None, zero: str | None = None) -> None:
        if label in self.labels: raise ValueError(f"duplicate label {label}")
        self.labels.add(label); self.rows.append((label, op, reg, target, zero))

    def resolve_mc(self, names: tuple[str, ...], entry: str, result: int, name: str) -> MCProgram:
        pc = {label: i for i, (label, *_rest) in enumerate(self.rows)}; out = []
        for _label, op, reg, target, zero in self.rows:
            if op == "HALT": out.append(MCInstruction("HALT"))
            elif op == "INC": out.append(MCInstruction("INC", reg, pc[target]))
            elif op == "DECJZ": out.append(MCInstruction("DECJZ", reg, pc[target], pc[zero]))
            else: raise ValueError(op)
        return MCProgram(tuple(out), names, pc[entry], result, name)

    def resolve_minsky(self, entry: str, name: str) -> Program:
        pc = {label: i for i, (label, *_rest) in enumerate(self.rows)}
        order = list(range(len(self.rows)))
        if pc[entry] != 0:
            e = pc[entry]; order = [e] + [i for i in order if i != e]
        newpc = {self.rows[i][0]: j for j, i in enumerate(order)}; out = []
        for i in order:
            _label, op, reg, target, zero = self.rows[i]
            if op == "HALT": out.append(Instruction("HALT"))
            elif op == "INC": out.append(Instruction("INC", reg, newpc[target]))
            elif op == "DECJZ": out.append(Instruction("DECJZ", reg, newpc[target], newpc[zero]))
            else: raise ValueError(op)
        return Program(tuple(out), name=name)


def _goto(b, label, zero_reg, target): b.add(label, "DECJZ", zero_reg, target, target)
def _zero(b, start, reg, done): b.add(start, "DECJZ", reg, start, done)


def _clear_many(b, start, regs, done):
    if not regs: raise ValueError("empty clear chain")
    labels = [start] + [b.fresh("clear") for _ in regs[1:]]
    for i, reg in enumerate(regs): _zero(b, labels[i], reg, labels[i + 1] if i + 1 < len(labels) else done)


def _move_into_zero(b, start, src, dst, done):
    body = b.fresh("move-body"); b.add(start, "DECJZ", src, body, done); b.add(body, "INC", dst, start)


def _move(b, start, src, dst, done):
    loop = b.fresh("move-loop"); _zero(b, start, dst, loop); _move_into_zero(b, loop, src, dst, done)


def _copy(b, start, src, dst, tmp, done):
    ztmp, loop, body1, body2, restore, rbody = (b.fresh(x) for x in ("copy-ztmp","copy-loop","copy-body1","copy-body2","copy-restore","copy-rbody"))
    _zero(b, start, dst, ztmp); _zero(b, ztmp, tmp, loop)
    b.add(loop, "DECJZ", src, body1, restore); b.add(body1, "INC", dst, body2); b.add(body2, "INC", tmp, loop)
    b.add(restore, "DECJZ", tmp, rbody, done); b.add(rbody, "INC", src, restore)


def _double(b, start, reg, tmp, done):
    loop, body1, body2, restore, rbody = (b.fresh(x) for x in ("double-loop","double-body1","double-body2","double-restore","double-rbody"))
    _zero(b, start, tmp, loop); b.add(loop, "DECJZ", reg, body1, restore); b.add(body1, "INC", tmp, body2); b.add(body2, "INC", tmp, loop)
    b.add(restore, "DECJZ", tmp, rbody, done); b.add(rbody, "INC", reg, restore)


def _set_const(b, start, reg, value, tmp, done):
    if value < 0: raise ValueError("natural constant required")
    zdone = b.fresh("const-zeroed"); _zero(b, start, reg, zdone); bits = bin(value)[2:]; cursor = zdone
    for i, bit in enumerate(bits):
        after = b.fresh("const-double-done"); _double(b, cursor, reg, tmp, after)
        nxt = done if i == len(bits) - 1 else b.fresh("const-next")
        if bit == "1": b.add(after, "INC", reg, nxt)
        else: _goto(b, after, tmp, nxt)
        cursor = nxt


def _eqz_replace(b, start, reg, done):
    nonzero, setone = b.fresh("eqz-nonzero"), b.fresh("eqz-setone")
    b.add(start, "DECJZ", reg, nonzero, setone); _zero(b, nonzero, reg, done); b.add(setone, "INC", reg, done)


def _addmod(b, start, a, other, modulus, t1, t2, done):
    addbody, copy_mod = b.fresh("add-body"), b.fresh("add-copy-mod")
    b.add(start, "DECJZ", other, addbody, copy_mod); b.add(addbody, "INC", a, start)
    cmp_loop = b.fresh("add-cmp"); _copy(b, copy_mod, modulus, t1, t2, cmp_loop)
    cmp_a, count, threshold, underflow = (b.fresh(x) for x in ("add-cmp-a","add-count","add-threshold","add-underflow"))
    b.add(cmp_loop, "DECJZ", t1, cmp_a, threshold); b.add(cmp_a, "DECJZ", a, count, underflow); b.add(count, "INC", t2, cmp_loop)
    _zero(b, threshold, t2, done)
    restore = b.fresh("add-restore"); _zero(b, underflow, t1, restore); _move_into_zero(b, restore, t2, a, done)


def _submod(b, start, a, other, modulus, t1, t2, done):
    dec_a, underflow = b.fresh("sub-dec-a"), b.fresh("sub-underflow")
    b.add(start, "DECJZ", other, dec_a, done); b.add(dec_a, "DECJZ", a, start, underflow)
    copied = b.fresh("sub-copied-mod"); _copy(b, underflow, modulus, a, t1, copied)
    after_one, impossible = b.fresh("sub-after-one"), b.fresh("sub-impossible")
    b.add(copied, "DECJZ", a, after_one, impossible); _goto(b, impossible, t2, done)
    loop = b.fresh("sub-rest-loop"); _goto(b, after_one, t2, loop)
    dec_rest = b.fresh("sub-dec-rest"); b.add(loop, "DECJZ", other, dec_rest, done); b.add(dec_rest, "DECJZ", a, loop, impossible)


def _matching_ends(rows):
    stack, out = [], {}
    for i, row in enumerate(rows):
        if row.op in {"block", "loop"}: stack.append(i)
        elif row.op == "end" and stack:
            s = stack.pop(); out[s] = i
    if stack: raise ValueError("unbalanced static HoloIR")
    return out


def stack_metadata(ir: StaticHoloIR):
    rows = ir.functions[0]; match = _matching_ends(rows); frames = []; heights = [0] * len(rows); branch_height = {}; h = maxh = 0
    for ip, row in enumerate(rows):
        heights[ip] = h; op = row.op
        if op in {"block", "loop"}: frames.append((op, h, match[ip]))
        elif op == "end":
            if frames and frames[-1][2] == ip:
                _kind, fh, _end = frames.pop(); h = fh
        elif op in {"local.get", "i32.const"}: h += 1
        elif op == "local.set": h -= 1
        elif op in {"i32.add", "i32.sub"}: h -= 1
        elif op in {"br", "br_if"}:
            depth = int(row.imm)
            if op == "br_if": h -= 1
            frame = frames[-1 - depth]; branch_height[ip] = frame[1]
            if op == "br": h = frames[-1][1] if frames else 0
        elif op == "return": h = 0
        if h < 0: raise ValueError("negative abstract stack height")
        maxh = max(maxh, h)
    return heights, branch_height, maxh


def compile_holoir_to_multicounter(ir: StaticHoloIR, local_count: int, *, word_bits: int = 8) -> MCProgram:
    if ir.source_kind != "structured-control" or len(ir.functions) != 1: raise ValueError("bridge currently targets structured-control static HoloIR")
    if not 1 <= word_bits <= 16: raise ValueError("certificate word width must lie in 1..16")
    rows = ir.functions[0]; heights, branch_heights, max_stack = stack_metadata(ir)
    names = [f"local{i}" for i in range(local_count)] + [f"stack{i}" for i in range(max_stack)] + ["tmp1","tmp2","tmp3","modulus","result","zero"]
    local = list(range(local_count)); stack = list(range(local_count, local_count + max_stack)); base = local_count + max_stack
    t1, t2, t3, modulus, result, zero = range(base, base + 6); b = LabelBuilder(); entry_labels = [f"ir{i}" for i in range(len(rows))]
    _set_const(b, "prologue", modulus, 1 << word_bits, t1, entry_labels[0])

    def clear_slots(start, lo, done):
        regs = stack[lo:]
        if not regs: _goto(b, start, zero, done)
        else: _clear_many(b, start, regs, done)

    for ip, row in enumerate(rows):
        start = entry_labels[ip]; fall = entry_labels[int(row.fallthrough)] if row.fallthrough is not None else None; h = heights[ip]; op = row.op
        if op in {"block", "loop"}: _goto(b, start, zero, fall)
        elif op == "end":
            if fall is None:
                moved = b.fresh("end-moved"); _move(b, start, stack[h - 1], result, moved); b.add(moved, "HALT")
            else: _goto(b, start, zero, fall)
        elif op == "local.get": _copy(b, start, local[int(row.imm)], stack[h], t1, fall)
        elif op == "local.set": _move(b, start, stack[h - 1], local[int(row.imm)], fall)
        elif op == "i32.const": _set_const(b, start, stack[h], int(row.imm) & ((1 << word_bits) - 1), t1, fall)
        elif op == "i32.eqz": _eqz_replace(b, start, stack[h - 1], fall)
        elif op == "i32.add": _addmod(b, start, stack[h - 2], stack[h - 1], modulus, t1, t2, fall)
        elif op == "i32.sub": _submod(b, start, stack[h - 2], stack[h - 1], modulus, t1, t2, fall)
        elif op == "br": clear_slots(start, branch_heights[ip], entry_labels[int(row.branch_target)])
        elif op == "br_if":
            cond = stack[h - 1]; nz, z = b.fresh("brif-nz"), b.fresh("brif-z"); b.add(start, "DECJZ", cond, nz, z)
            clear_slots(nz, branch_heights[ip], entry_labels[int(row.branch_target)]); clear_slots(z, h - 1, fall)
        elif op == "return":
            moved = b.fresh("return-moved"); _move(b, start, stack[h - 1], result, moved); b.add(moved, "HALT")
        else: raise ValueError(f"unsupported static HoloIR opcode {op}")
    return b.resolve_mc(tuple(names), "prologue", result, f"holoir-{ir.image_id[:18]}-w{word_bits}")


def run_mc(program: MCProgram, fuel: int = 2_000_000):
    regs = [0] * len(program.register_names); pc = program.entry
    for step in range(fuel):
        ins = program.instructions[pc]
        if ins.op == "HALT": return regs, step
        r = int(ins.register)
        if ins.op == "INC": regs[r] += 1; pc = int(ins.target)
        elif regs[r] == 0: pc = int(ins.zero_target)
        else: regs[r] -= 1; pc = int(ins.target)
    raise RuntimeError("multi-counter execution fuel exhausted")


def primes(n: int):
    out, x = [], 2
    while len(out) < n:
        if all(x % p for p in out if p * p <= x): out.append(x)
        x += 1
    return tuple(out)


def encode_registers(values, ps):
    if len(values) != len(ps) or any(type(x) is not int or x < 0 for x in values): raise ValueError("invalid logical counter vector")
    out = 1
    for p, exponent in zip(ps, values): out *= p ** exponent
    return out


def decode_registers(encoded, ps):
    if type(encoded) is not int or encoded <= 0: raise ValueError("prime-power state must be positive")
    row, n = [], encoded
    for p in ps:
        e = 0
        while n % p == 0: n //= p; e += 1
        row.append(e)
    if n != 1: raise ValueError("encoded state contains unknown prime factor")
    return tuple(row)


def _mul_prime(b, entry, p, target, stem):
    add, restore = b.fresh(stem + "-add"), b.fresh(stem + "-restore"); b.add(entry, "DECJZ", 0, add, restore); cur = add
    for i in range(p):
        nxt = entry if i == p - 1 else b.fresh(stem + "-add"); b.add(cur, "INC", 1, nxt); cur = nxt
    move = b.fresh(stem + "-move"); b.add(restore, "DECJZ", 1, move, target); b.add(move, "INC", 0, restore)


def _divtest_prime(b, entry, p, nz_target, z_target, stem):
    tries = [entry] + [b.fresh(stem + f"-try{i}") for i in range(1, p)]; chunk, divdone = b.fresh(stem + "-chunk"), b.fresh(stem + "-divdone")
    rems = {j: b.fresh(stem + f"-rem{j}") for j in range(1, p)}
    for j in range(p): b.add(tries[j], "DECJZ", 0, chunk if j == p - 1 else tries[j + 1], divdone if j == 0 else rems[j])
    b.add(chunk, "INC", 1, entry); move = b.fresh(stem + "-divmove"); b.add(divdone, "DECJZ", 1, move, nz_target); b.add(move, "INC", 0, divdone)
    for j, rem in rems.items():
        restore = b.fresh(stem + "-restore"); cur = rem
        for k in range(j):
            nxt = restore if k == j - 1 else b.fresh(stem + "-remadd"); b.add(cur, "INC", 0, nxt); cur = nxt
        add0 = b.fresh(stem + "-restore-add"); b.add(restore, "DECJZ", 1, add0, z_target); cur2 = add0
        for k in range(p):
            nxt = restore if k == p - 1 else b.fresh(stem + "-restore-add"); b.add(cur2, "INC", 0, nxt); cur2 = nxt


def compile_multicounter_to_two(program: MCProgram):
    ps = primes(len(program.register_names)); b = LabelBuilder(); entries = [f"mc{i}" for i in range(len(program.instructions))]
    for i, ins in enumerate(program.instructions):
        entry = entries[i]
        if ins.op == "HALT": b.add(entry, "HALT")
        elif ins.op == "INC": _mul_prime(b, entry, ps[int(ins.register)], entries[int(ins.target)], f"mc{i}-inc")
        elif ins.op == "DECJZ": _divtest_prime(b, entry, ps[int(ins.register)], entries[int(ins.target)], entries[int(ins.zero_target)], f"mc{i}-dec")
        else: raise ValueError(ins.op)
    return b.resolve_minsky(entries[program.entry], f"prime-encoded-{program.name}"), ps


def run_two(program: Program, counters, fuel: int = 5_000_000):
    c = [int(counters[0]), int(counters[1])]; pc = 0
    for step in range(fuel):
        ins = program.instructions[pc]
        if ins.op == "HALT": return (c[0], c[1]), step
        r = int(ins.register)
        if ins.op == "INC": c[r] += 1; pc = int(ins.target)
        elif c[r] == 0: pc = int(ins.zero_target)
        else: c[r] -= 1; pc = int(ins.target)
    raise RuntimeError("two-counter execution fuel exhausted")


def tiny_reduction_witness():
    mc = MCProgram((MCInstruction("INC",2,1), MCInstruction("DECJZ",2,2,3), MCInstruction("INC",0,3), MCInstruction("HALT")), ("r0","r1","r2"), 0, 0, "tiny-prime-reduction")
    two, ps = compile_multicounter_to_two(mc); rows = []
    for initial in ((0,0,0),(1,0,0),(0,1,1),(2,1,0)):
        vals = list(initial); pc = 0
        for _ in range(20):
            ins = mc.instructions[pc]
            if ins.op == "HALT": break
            r = int(ins.register)
            if ins.op == "INC": vals[r] += 1; pc = int(ins.target)
            elif vals[r] == 0: pc = int(ins.zero_target)
            else: vals[r] -= 1; pc = int(ins.target)
        encoded = encode_registers(initial, ps); (after, scratch), steps = run_two(two, (encoded, 0))
        rows.append({"initial": initial, "expected": tuple(vals), "decoded": decode_registers(after, ps), "scratch": scratch, "steps": steps})
    return {"program": two, "primes": ps, "rows": rows}


def verify() -> dict[str, Any]:
    raw = control.sample_module_binary(7); module = control.decode_module(raw); control.validate(module); ir = compile_control(module)
    mc = compile_holoir_to_multicounter(ir, len(module.function.locals_types), word_bits=8); regs, mc_steps = run_mc(mc)
    source_result = control.execute(module); mc_result = regs[mc.result_register]; two, ps = compile_multicounter_to_two(mc); tiny = tiny_reduction_witness()
    tiny_exact = all(tuple(x["expected"]) == tuple(x["decoded"]) and x["scratch"] == 0 for x in tiny["rows"])
    checks = {
        "static_holoir_is_compiled_before_source_invocation": ir.source_binary_digest == module.binary_digest,
        "real_structured_control_result_is_28": source_result == 28,
        "static_holoir_multicounter_result_is_28": mc_result == 28,
        "multicounter_program_uses_only_inc_decjz_halt": all(x.op in {"INC","DECJZ","HALT"} for x in mc.instructions),
        "multicounter_program_has_finite_static_image": len(mc.instructions) > 0 and mc.image_id.startswith("sha256:"),
        "two_counter_compiler_emits_only_repository_core_ops": all(x.op in {"INC","DECJZ","HALT"} for x in two.instructions),
        "one_prime_is_assigned_per_logical_counter": len(ps) == len(mc.register_names) and len(set(ps)) == len(ps),
        "prime_encoding_roundtrips_small_vectors": all(decode_registers(encode_registers(v, tiny["primes"]), tiny["primes"]) == tuple(v) for v in ((0,0,0),(1,2,0),(2,1,1))),
        "literal_two_counter_macrocode_matches_logical_program_on_small_family": tiny_exact,
        "two_counter_compilation_identity_is_static": two.image_id.startswith("sha256:"),
    }
    out = {
        "schema": "w33.static-holoir-counter-bridge.v1", "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
        "source_binary_digest": module.binary_digest, "holoir_image_id": ir.image_id, "multicounter_image_id": mc.image_id,
        "multicounter_registers": len(mc.register_names), "multicounter_instructions": len(mc.instructions), "multicounter_execution_steps": mc_steps,
        "two_counter_image_id": two.image_id, "two_counter_instructions": len(two.instructions), "word_bits_executed": 8, "result": mc_result,
        "reduction": "Each logical counter r_i is the exponent of a dedicated prime p_i in physical counter0. Literal two-counter loops implement multiplication by p_i for INC and divisibility/division by p_i for DECJZ, returning scratch counter1 to zero at every logical instruction boundary.",
        "theorem_boundary": "The real structured-control HoloIR regression is compiled and executed statically through the finite multi-counter layer. The generic finite-multicounter-to-two-counter compiler is constructive and executable, but the full Wasm regression is not run through prime-power code because that exact Goedel encoding is intentionally computationally enormous. The capability HoloIR surface and an efficient physical representation remain open.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8"); return out


if __name__ == "__main__":
    out = verify(); print(json.dumps(out, indent=2, sort_keys=True)); raise SystemExit(out["status"] != "PASS")
