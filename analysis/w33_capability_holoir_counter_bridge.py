#!/usr/bin/env python3
"""Static capability-HoloIR -> multi-counter -> two-counter bridge.

This extends ``w33_static_holoir_counter_bridge`` across the second authenticated
HoloIR surface already produced before execution by
``w33_static_wasm_holoir_compiler``: straight-line calls, mutable globals,
aligned persistent-Merkle linear-memory accesses, and explicitly bound host
imports.

The lowering is deliberately finite and constructive:

* defined calls are statically inlined after an acyclic-call check;
* locals, operand-stack slots, globals and manifested i32 memory words are
  natural-number counters;
* every emitted primitive is INC, DECJZ or HALT;
* current regression memory addresses must be statically resolvable and aligned;
* bound host import w33.kernel.SEND36 is compiled from a declared counter-level
  contract (sum of three i32 arguments modulo the certificate word width);
* the resulting finite multi-counter image is fed to the existing generic
  prime-exponent reduction to the repository's universal two-counter core.

The source runtime continues to use the persistent Merkle byte-addressed memory.
The counter machine refines logical i32 contents at the statically manifested
addresses; it does not claim that a Merkle root itself is a finite RAM register.
The executable witness uses an 8-bit arithmetic certificate because all current
regression values fit in that width.  General dynamic sparse-address lowering
and full 32-bit efficient execution remain separate engineering/theorem work.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

import w33_wasm3_capability_runtime as cap
from w33_static_wasm_holoir_compiler import StaticHoloIR, compile_capability
from w33_static_holoir_counter_bridge import (
    LabelBuilder,
    MCProgram,
    _addmod,
    _copy,
    _goto,
    _move,
    _set_const,
    _submod,
    compile_multicounter_to_two,
    run_mc,
    tiny_reduction_witness,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_CAPABILITY_HOLOIR_COUNTER_BRIDGE.json"
WORD_BITS = 8
MASK = (1 << WORD_BITS) - 1


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class HostSpec:
    module: str
    name: str
    arity: int
    results: int
    kind: str

    @property
    def spec_id(self) -> str:
        return digest({"schema": "w33.counter-host-spec.v1", **vars(self)})


SEND36 = HostSpec("w33.kernel", "SEND36", 3, 1, "sum-mod-2^w")


class ClosedCapabilityCompiler:
    def __init__(self, module: cap.WasmModule, ir: StaticHoloIR, *, word_bits: int = WORD_BITS,
                 host_specs: tuple[HostSpec, ...] = ()):
        if ir.source_kind != "capability" or ir.source_binary_digest != module.binary_digest:
            raise ValueError("capability HoloIR/module identity mismatch")
        if not 1 <= word_bits <= 16:
            raise ValueError("certificate word width must lie in 1..16")
        self.module = module
        self.ir = ir
        self.word_bits = word_bits
        self.mask = (1 << word_bits) - 1
        self.host_specs = {(x.module, x.name): x for x in host_specs}
        self.b = LabelBuilder()
        self.names: list[str] = []
        self.serial = 0
        self.rows_by_function = {fn[0].function: fn for fn in ir.functions if fn}
        self.memory_regs: dict[int, int] = {}
        self.global_regs = [self.reg(f"global{i}") for i in range(len(module.globals))]
        self.t1 = self.reg("tmp1"); self.t2 = self.reg("tmp2"); self.t3 = self.reg("tmp3")
        self.modulus = self.reg("modulus"); self.result = self.reg("result"); self.zero = self.reg("zero")
        self.global_static: list[int | None] = [int(g.value) & self.mask for g in module.globals]
        self.call_sites = 0

    def reg(self, name: str) -> int:
        idx = len(self.names); self.names.append(name); return idx

    def fresh(self, stem: str) -> str:
        self.serial += 1; return f"cap-{stem}${self.serial}"

    def memory_reg(self, address: int) -> int:
        if address % 4:
            raise ValueError("counter bridge requires aligned manifested i32 address")
        if address < 0 or address + 4 > (self.module.memory.min_pages * cap.PAGE_BYTES if self.module.memory else 0):
            raise ValueError("manifested memory address outside declared Wasm memory")
        if address not in self.memory_regs:
            self.memory_regs[address] = self.reg(f"mem32@{address}")
        return self.memory_regs[address]

    def max_stack(self, function_index: int) -> int:
        rows = self.rows_by_function[function_index]
        h = 0; m = 0
        for row in rows:
            op = row.op
            if op in {"i32.const", "local.get", "global.get"}: h += 1
            elif op in {"local.set", "global.set"}: h -= 1
            elif op == "local.tee": pass
            elif op in {"i32.add", "i32.sub"}: h -= 1
            elif op == "i32.load": pass
            elif op == "i32.store": h -= 2
            elif op == "call":
                ft = self.module.function_type(int(row.imm)); h -= len(ft.params); h += len(ft.results)
            elif op == "end": pass
            else: raise ValueError(f"unsupported capability HoloIR op {op}")
            if h < 0: raise ValueError("negative capability HoloIR stack height")
            m = max(m, h)
        return m

    def emit_host(self, target: int, args: list[int], static_args: list[int | None], out: int,
                  entry: str, done: str) -> int | None:
        imp = self.module.imports[target]
        spec = self.host_specs.get((imp.module, imp.name))
        if spec is None:
            raise ValueError(f"unbound counter host contract {imp.module}.{imp.name}")
        if spec.arity != len(args) or spec.results != 1 or spec.kind != "sum-mod-2^w":
            raise ValueError("unsupported host counter contract")
        cursor = entry
        _move(self.b, cursor, args[0], out, (n1 := self.fresh("host-add1")))
        cursor = n1
        _addmod(self.b, cursor, out, args[1], self.modulus, self.t1, self.t2, (n2 := self.fresh("host-add2")))
        cursor = n2
        _addmod(self.b, cursor, out, args[2], self.modulus, self.t1, self.t2, done)
        if all(x is not None for x in static_args):
            return sum(int(x) for x in static_args) & self.mask
        return None

    def emit_function(self, function_index: int, args: list[int], static_args: list[int | None],
                      out: int, entry: str, done: str, active: tuple[int, ...]) -> int | None:
        if function_index in active:
            raise ValueError("recursive capability call graph is outside finite static inliner")
        ftype = self.module.function_type(function_index)
        if len(args) != len(ftype.params) or len(ftype.results) != 1:
            raise ValueError("bridge currently requires single-result functions")
        if function_index < len(self.module.imports):
            return self.emit_host(function_index, args, static_args, out, entry, done)

        self.call_sites += 1
        fn = self.module.functions[function_index - len(self.module.imports)]
        frame = self.call_sites
        local_count = len(ftype.params) + len(fn.locals_types)
        locals_ = [self.reg(f"f{function_index}.call{frame}.local{i}") for i in range(local_count)]
        local_static: list[int | None] = list(static_args) + [0] * len(fn.locals_types)
        stack_regs = [self.reg(f"f{function_index}.call{frame}.stack{i}") for i in range(max(1, self.max_stack(function_index)))]
        stack_static: list[int | None] = []
        h = 0; cursor = entry

        for i, arg in enumerate(args):
            nxt = self.fresh("arg")
            _move(self.b, cursor, arg, locals_[i], nxt); cursor = nxt

        rows = self.rows_by_function[function_index]
        for ip, row in enumerate(rows):
            op = row.op
            nxt = done if op == "end" else self.fresh(f"f{function_index}-ip{ip}")
            if op == "i32.const":
                v = int(row.imm) & self.mask; _set_const(self.b, cursor, stack_regs[h], v, self.t1, nxt)
                stack_static.append(v); h += 1
            elif op == "local.get":
                i = int(row.imm); _copy(self.b, cursor, locals_[i], stack_regs[h], self.t1, nxt)
                stack_static.append(local_static[i]); h += 1
            elif op == "local.set":
                i = int(row.imm); h -= 1; sv = stack_static.pop(); _move(self.b, cursor, stack_regs[h], locals_[i], nxt); local_static[i] = sv
            elif op == "local.tee":
                i = int(row.imm); _copy(self.b, cursor, stack_regs[h-1], locals_[i], self.t1, nxt); local_static[i] = stack_static[-1]
            elif op == "global.get":
                i = int(row.imm); _copy(self.b, cursor, self.global_regs[i], stack_regs[h], self.t1, nxt)
                stack_static.append(self.global_static[i]); h += 1
            elif op == "global.set":
                i = int(row.imm); h -= 1; sv = stack_static.pop(); _move(self.b, cursor, stack_regs[h], self.global_regs[i], nxt); self.global_static[i] = sv
            elif op in {"i32.add", "i32.sub"}:
                rhs_static = stack_static.pop(); lhs_static = stack_static.pop(); h -= 1
                lhs, rhs = stack_regs[h-1], stack_regs[h]
                if op == "i32.add": _addmod(self.b, cursor, lhs, rhs, self.modulus, self.t1, self.t2, nxt)
                else: _submod(self.b, cursor, lhs, rhs, self.modulus, self.t1, self.t2, nxt)
                if lhs_static is not None and rhs_static is not None:
                    stack_static.append((int(lhs_static) + (int(rhs_static) if op == "i32.add" else -int(rhs_static))) & self.mask)
                else: stack_static.append(None)
            elif op == "i32.load":
                _align, offset = row.imm; base = stack_static[-1]
                if base is None: raise ValueError("dynamic memory address requires sparse-address extension")
                address = (int(base) + int(offset)) & 0xFFFFFFFF
                mem = self.memory_reg(address); _copy(self.b, cursor, mem, stack_regs[h-1], self.t1, nxt)
                stack_static[-1] = None
            elif op == "i32.store":
                _align, offset = row.imm; value_static = stack_static.pop(); address_static = stack_static.pop(); h -= 2
                if address_static is None: raise ValueError("dynamic memory address requires sparse-address extension")
                address = (int(address_static) + int(offset)) & 0xFFFFFFFF; mem = self.memory_reg(address)
                value_reg, address_reg = stack_regs[h+1], stack_regs[h]
                moved = self.fresh("store-moved"); _move(self.b, cursor, value_reg, mem, moved); _set_const(self.b, moved, address_reg, 0, self.t1, nxt)
            elif op == "call":
                target = int(row.imm); ct = self.module.function_type(target); n = len(ct.params)
                arg_start = h - n; call_args = stack_regs[arg_start:h]; call_static = stack_static[arg_start:h]
                h = arg_start; del stack_static[arg_start:]
                call_out = stack_regs[h]
                result_static = self.emit_function(target, list(call_args), list(call_static), call_out, cursor, nxt, active + (function_index,))
                stack_static.append(result_static); h += 1
            elif op == "end":
                if h != 1: raise ValueError("single-result function must end with one stack value")
                _move(self.b, cursor, stack_regs[0], out, done)
                return stack_static[0]
            else:
                raise ValueError(f"unsupported capability HoloIR op {op}")
            cursor = nxt
        raise ValueError("capability HoloIR function lacks end")

    def compile_export(self, name: str = "main") -> tuple[MCProgram, dict[str, Any]]:
        matches = [(kind, index) for export_name, kind, index in self.module.exports if export_name == name]
        if len(matches) != 1 or matches[0][0] != 0:
            raise KeyError(name)
        entry = "prologue"; after_mod = self.fresh("after-modulus")
        _set_const(self.b, entry, self.modulus, 1 << self.word_bits, self.t1, after_mod)
        cursor = after_mod
        for i, g in enumerate(self.module.globals):
            nxt = self.fresh("after-global")
            _set_const(self.b, cursor, self.global_regs[i], int(g.value) & self.mask, self.t1, nxt); cursor = nxt
        call_done = self.fresh("main-done")
        static_result = self.emit_function(matches[0][1], [], [], self.result, cursor, call_done, ())
        self.b.add(call_done, "HALT")
        program = self.b.resolve_mc(tuple(self.names), "prologue", self.result, f"capability-{self.ir.image_id[:18]}-w{self.word_bits}")
        manifest = {
            "schema": "w33.capability-counter-manifest.v1",
            "source_binary_digest": self.module.binary_digest,
            "holoir_image_id": self.ir.image_id,
            "word_bits": self.word_bits,
            "memory_addresses": sorted(self.memory_regs),
            "host_spec_ids": sorted(x.spec_id for x in self.host_specs.values()),
            "defined_call_expansions": self.call_sites,
            "static_result_if_known": static_result,
        }
        return program, {**manifest, "manifest_digest": digest(manifest), "memory_registers": dict(self.memory_regs)}


def verify() -> dict[str, Any]:
    # Calls + globals + persistent Merkle memory. Compile before source runtime.
    mmod = cap.decode_module(cap.build_regression_module()); cap.validate(mmod)
    mir = compile_capability(mmod)
    compiler = ClosedCapabilityCompiler(mmod, mir, word_bits=WORD_BITS)
    mc, manifest = compiler.compile_export("main")
    regs, mc_steps = run_mc(mc, fuel=5_000_000)
    mc_result = regs[mc.result_register]
    logical_mem = {addr: regs[reg] for addr, reg in manifest["memory_registers"].items()}
    logical_globals = [regs[r] for r in compiler.global_regs]
    two, primes = compile_multicounter_to_two(mc)

    source = cap.CapabilityWasmRuntime(mmod)
    source_initial_root = source.memory.root; source_result = source.execute_export("main")
    source_mem = {addr: source.load_i32(addr) for addr in manifest["memory_addresses"]}

    # Bound host import. Its contract is lowered, not invoked to create the program.
    hmod = cap.decode_module(cap.build_host_import_module()); cap.validate(hmod)
    hir = compile_capability(hmod)
    hcompiler = ClosedCapabilityCompiler(hmod, hir, word_bits=WORD_BITS, host_specs=(SEND36,))
    hmc, hmanifest = hcompiler.compile_export("main")
    hregs, hsteps = run_mc(hmc, fuel=1_000_000); hresult = hregs[hmc.result_register]
    htwo, hprimes = compile_multicounter_to_two(hmc)
    host_source = cap.CapabilityWasmRuntime(hmod, host_functions={("w33.kernel", "SEND36"): lambda args, runtime: sum(args) & 0xFFFFFFFF})
    host_source_result = host_source.execute_export("main")

    tiny = tiny_reduction_witness()
    tiny_exact = all(tuple(x["expected"]) == tuple(x["decoded"]) and x["scratch"] == 0 for x in tiny["rows"])
    checks = {
        "capability_holoir_compiled_before_source_execution": mir.source_binary_digest == mmod.binary_digest,
        "closed_capability_multicounter_result_is_5": mc_result == 5,
        "source_persistent_merkle_runtime_result_is_5": source_result == 5,
        "globals_refine_exactly": logical_globals == source.globals == [2],
        "manifested_memory_words_refine_merkle_contents": logical_mem == source_mem == {0: 1, 4: 2},
        "source_merkle_root_changes_on_stores": source.memory.root != source_initial_root,
        "capability_multicounter_uses_only_inc_decjz_halt": all(x.op in {"INC", "DECJZ", "HALT"} for x in mc.instructions),
        "capability_static_image_compiles_to_two_counter_core": all(x.op in {"INC", "DECJZ", "HALT"} for x in two.instructions) and len(primes) == len(mc.register_names),
        "bound_send36_counter_contract_result_is_50": hresult == host_source_result == 50,
        "host_import_binding_is_content_addressed": hmanifest["host_spec_ids"] == [SEND36.spec_id],
        "host_static_image_compiles_to_two_counter_core": all(x.op in {"INC", "DECJZ", "HALT"} for x in htwo.instructions) and len(hprimes) == len(hmc.register_names),
        "generic_prime_reduction_still_executes_exact_small_family": tiny_exact,
        "all_compiler_manifests_are_content_addressed": manifest["manifest_digest"].startswith("sha256:") and hmanifest["manifest_digest"].startswith("sha256:"),
    }
    out = {
        "schema": "w33.capability-holoir-counter-bridge.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "capability": {
            "source_binary_digest": mmod.binary_digest,
            "holoir_image_id": mir.image_id,
            "manifest_digest": manifest["manifest_digest"],
            "memory_addresses": manifest["memory_addresses"],
            "multicounter_image_id": mc.image_id,
            "multicounter_registers": len(mc.register_names),
            "multicounter_instructions": len(mc.instructions),
            "multicounter_steps": mc_steps,
            "two_counter_image_id": two.image_id,
            "two_counter_instructions": len(two.instructions),
            "result": mc_result,
            "globals": logical_globals,
            "memory_words": logical_mem,
            "source_merkle_root": source.memory.root,
        },
        "host_import": {
            "source_binary_digest": hmod.binary_digest,
            "holoir_image_id": hir.image_id,
            "manifest_digest": hmanifest["manifest_digest"],
            "host_spec_id": SEND36.spec_id,
            "multicounter_image_id": hmc.image_id,
            "multicounter_steps": hsteps,
            "two_counter_image_id": htwo.image_id,
            "result": hresult,
        },
        "refinement": (
            "For the current closed capability regressions, the static authenticated HoloIR is lowered before source execution to an executable finite INC/DECJZ/HALT machine whose globals and manifested aligned i32 memory words match the persistent-Merkle runtime, and whose entire finite image is constructively reducible to the universal two-counter core."
        ),
        "boundary": (
            "The executable certificate uses an 8-bit modular word width because all current regression values fit. Defined calls must be acyclic, memory addresses must be statically resolvable/aligned, and host imports require explicit counter-level contracts. The counter machine refines logical contents at manifested addresses; it does not encode the Merkle hash DAG itself. General dynamic sparse addresses, recursion and efficient full-i32 two-counter execution remain open."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
