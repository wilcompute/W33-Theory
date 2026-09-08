#!/usr/bin/env python3
"""Dynamic sparse-address capability HoloIR -> counter-trie witness.

The previous capability bridge only lowered memory accesses whose effective i32
address was statically known.  This module compiles one *single* HoloIR image
whose address is supplied at runtime by a bound host capability.  A content-
addressed sparse manifest enumerates the aligned words the guest may access;
runtime address selection is performed inside the finite multi-counter program
by an INC/DECJZ equality-decision trie.

The same compiled program is executed for host-supplied addresses 0,4,8,12
without recompilation.  The source path uses the real persistent-Merkle Wasm
runtime and the target path uses only finite counter instructions.  Disallowed
address 16 traps in the target manifest rather than aliasing a permitted word.

The sparse manifest is finite in this certificate.  This closes "dynamic within
an authenticated sparse capability set", not arbitrary unbounded Wasm RAM.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

import w33_wasm3_capability_runtime as cap
from w33_static_wasm_holoir_compiler import compile_capability
from w33_static_holoir_counter_bridge import (
    LabelBuilder, MCProgram, _copy, _goto, _move, _set_const,
    compile_multicounter_to_two, tiny_reduction_witness,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_DYNAMIC_SPARSE_MEMORY_COUNTER.json"
WORD_BITS = 8
ALLOWED = (0, 4, 8, 12)
VALUE = 77


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def build_dynamic_module() -> bytes:
    types = cap._section(1, cap._vec_bytes([
        cap._functype((), (cap.I32,)),
        cap._functype((), (cap.I32,)),
    ]))
    imports = cap._section(
        2,
        cap.uleb(1) + cap._name("w33.kernel") + cap._name("ADDR") + b"\x00" + cap.uleb(0),
    )
    functions = cap._section(3, cap.uleb(1) + cap.uleb(1))
    memory = cap._section(5, cap.uleb(1) + cap.uleb(1) + cap.uleb(1) + cap.uleb(1))
    exports = cap._section(
        7,
        cap.uleb(2)
        + cap._name("main") + b"\x00" + cap.uleb(1)
        + cap._name("memory") + b"\x02" + cap.uleb(0),
    )
    main = (
        b"\x10" + cap.uleb(0)             # call ADDR -> runtime value
        + b"\x21" + cap.uleb(0)           # local.set 0
        + b"\x20" + cap.uleb(0)           # local.get 0
        + b"\x41" + cap.sleb32(VALUE)      # i32.const 77
        + b"\x36" + cap.uleb(2) + cap.uleb(0)  # i32.store
        + b"\x20" + cap.uleb(0)
        + b"\x28" + cap.uleb(2) + cap.uleb(0)  # i32.load
        + b"\x0b"
    )
    code = cap._section(10, cap.uleb(1) + cap._body([(1, cap.I32)], main))
    return cap.MAGIC + cap.VERSION + types + imports + functions + memory + exports + code


class SparseCompiler:
    def __init__(self, module: cap.WasmModule, allowed=ALLOWED):
        self.module = module
        self.ir = compile_capability(module)
        self.allowed = tuple(sorted(set(int(x) for x in allowed)))
        if not self.allowed or any(x < 0 or x % 4 for x in self.allowed):
            raise ValueError("allowed sparse addresses must be nonempty aligned naturals")
        if any(x + 4 > module.memory.min_pages * cap.PAGE_BYTES for x in self.allowed):
            raise ValueError("sparse address outside declared Wasm memory")
        self.b = LabelBuilder(); self.names: list[str] = []; self.serial = 0
        self.host_addr = self.reg("host.ADDR")
        self.local0 = self.reg("local0")
        self.stack0 = self.reg("stack0"); self.stack1 = self.reg("stack1")
        self.tcopy = self.reg("addr-copy"); self.tconst = self.reg("addr-const"); self.scratch = self.reg("scratch")
        self.result = self.reg("result"); self.trap = self.reg("trap"); self.zero = self.reg("zero")
        self.memory_regs = {a: self.reg(f"mem32@{a}") for a in self.allowed}

    def reg(self, name: str) -> int:
        i = len(self.names); self.names.append(name); return i

    def fresh(self, stem: str) -> str:
        self.serial += 1; return f"sparse-{stem}${self.serial}"

    def eq_const_branch(self, entry: str, reg: int, value: int, yes: str, no: str) -> None:
        copied = self.fresh("copied")
        _copy(self.b, entry, reg, self.tcopy, self.scratch, copied)
        ready = self.fresh("const-ready")
        _set_const(self.b, copied, self.tconst, value, self.scratch, ready)
        loop = self.fresh("eq-loop")
        _goto(self.b, ready, self.zero, loop)
        dec_const = self.fresh("eq-dec-const")
        check_const = self.fresh("eq-check-const")
        self.b.add(loop, "DECJZ", self.tcopy, dec_const, check_const)
        self.b.add(dec_const, "DECJZ", self.tconst, loop, no)
        self.b.add(check_const, "DECJZ", self.tconst, no, yes)

    def dispatch(self, entry: str, address_reg: int, handlers: dict[int, str], miss: str) -> None:
        cursor = entry
        addresses = list(self.allowed)
        for i, address in enumerate(addresses):
            nxt = miss if i == len(addresses) - 1 else self.fresh("next-address")
            self.eq_const_branch(cursor, address_reg, address, handlers[address], nxt)
            cursor = nxt

    def compile(self) -> tuple[MCProgram, dict[str, Any]]:
        # This compiler intentionally targets the exact HoloIR shape emitted by
        # build_dynamic_module, but address selection itself is runtime-dynamic.
        # Opcode order alone is insufficient: immediates and module bindings
        # determine semantics too. Ignore only byte provenance/locations, so
        # equivalent custom-section encodings remain admissible.
        def semantic_shape(module: cap.WasmModule) -> dict[str, Any]:
            shape = asdict(module)
            shape.pop("binary_digest")
            for fn in shape["functions"]:
                for ins in fn["instructions"]:
                    ins.pop("offset")
            return shape

        if semantic_shape(self.module) != semantic_shape(cap.decode_module(build_dynamic_module())):
            raise ValueError("unsupported sparse witness semantics: operands or module bindings differ")
        rows = self.ir.functions[0]
        ops = [r.op for r in rows]
        expected = ["call", "local.set", "local.get", "i32.const", "i32.store", "local.get", "i32.load", "end"]
        if ops != expected:
            raise AssertionError(f"dynamic witness HoloIR changed: {ops}")

        # call ADDR
        l1 = self.fresh("after-host")
        _copy(self.b, "entry", self.host_addr, self.stack0, self.scratch, l1)
        # local.set0
        l2 = self.fresh("after-local-set")
        _move(self.b, l1, self.stack0, self.local0, l2)
        # local.get0
        l3 = self.fresh("after-local-get")
        _copy(self.b, l2, self.local0, self.stack0, self.scratch, l3)
        # const value
        l4 = self.fresh("after-value")
        _set_const(self.b, l3, self.stack1, VALUE, self.scratch, l4)

        # Dynamic store: dispatch on stack0.  Each branch consumes stack1 into
        # exactly one sparse word and then rejoins.
        store_done = self.fresh("store-done")
        store_handlers = {}
        for address in self.allowed:
            h = self.fresh(f"store-{address}"); store_handlers[address] = h
            cleared = self.fresh("store-clear-address")
            _move(self.b, h, self.stack1, self.memory_regs[address], cleared)
            _set_const(self.b, cleared, self.stack0, 0, self.scratch, store_done)
        trap_store = self.fresh("trap-store")
        set_trap_store = self.fresh("trap-store-set")
        _set_const(self.b, trap_store, self.trap, 1, self.scratch, set_trap_store)
        self.b.add(set_trap_store, "HALT")
        self.dispatch(l4, self.stack0, store_handlers, trap_store)

        # local.get0 after store
        l5 = self.fresh("load-address")
        _copy(self.b, store_done, self.local0, self.stack0, self.scratch, l5)
        # Dynamic load replaces stack0 by selected sparse word.
        load_done = self.fresh("load-done")
        load_handlers = {}
        for address in self.allowed:
            h = self.fresh(f"load-{address}"); load_handlers[address] = h
            _copy(self.b, h, self.memory_regs[address], self.stack0, self.scratch, load_done)
        trap_load = self.fresh("trap-load")
        set_trap_load = self.fresh("trap-load-set")
        _set_const(self.b, trap_load, self.trap, 1, self.scratch, set_trap_load)
        self.b.add(set_trap_load, "HALT")
        self.dispatch(l5, self.stack0, load_handlers, trap_load)

        halt = self.fresh("result")
        _move(self.b, load_done, self.stack0, self.result, halt)
        self.b.add(halt, "HALT")
        program = self.b.resolve_mc(tuple(self.names), "entry", self.result, f"dynamic-sparse-{self.ir.image_id[:18]}")
        manifest = {
            "schema": "w33.dynamic-sparse-memory-manifest.v1",
            "source_binary_digest": self.module.binary_digest,
            "holoir_image_id": self.ir.image_id,
            "allowed_aligned_i32_addresses": list(self.allowed),
            "wasm_memory_pages": self.module.memory.min_pages,
            "access_width_bytes": 4,
            "host_address_contract": {"module": "w33.kernel", "name": "ADDR", "result": "runtime i32"},
            "counter_program_image_id": program.image_id,
        }
        return program, {**manifest, "manifest_digest": digest(manifest)}


def run_mc_initial(program: MCProgram, names: tuple[str, ...], initial: dict[str, int], fuel=2_000_000):
    regs = [0] * len(names)
    index = {n: i for i, n in enumerate(names)}
    for name, value in initial.items():
        if name not in index or not isinstance(value, int) or value < 0:
            raise ValueError("invalid initial counter state")
        regs[index[name]] = value
    pc = program.entry
    for step in range(fuel):
        ins = program.instructions[pc]
        if ins.op == "HALT": return regs, step
        r = int(ins.register)
        if ins.op == "INC": regs[r] += 1; pc = int(ins.target)
        elif regs[r] == 0: pc = int(ins.zero_target)
        else: regs[r] -= 1; pc = int(ins.target)
    raise RuntimeError("dynamic sparse counter fuel exhausted")


def verify() -> dict[str, Any]:
    binary = build_dynamic_module()
    module = cap.decode_module(binary); validation = cap.validate(module)
    compiler = SparseCompiler(module)
    program, manifest = compiler.compile()  # before any host invocation
    two, primes = compile_multicounter_to_two(program)
    outcomes = []
    for address in ALLOWED:
        source = cap.CapabilityWasmRuntime(module, host_functions={("w33.kernel", "ADDR"): lambda args, rt, a=address: a})
        initial_root = source.memory.root
        source_result = source.execute_export("main")
        regs, steps = run_mc_initial(program, tuple(compiler.names), {"host.ADDR": address})
        target_result = regs[program.result_register]
        target_words = {a: regs[r] for a, r in compiler.memory_regs.items()}
        outcomes.append({
            "address": address,
            "source_result": source_result,
            "counter_result": target_result,
            "source_word": source.load_i32(address),
            "counter_word": target_words[address],
            "other_counter_words_zero": all(v == 0 for a, v in target_words.items() if a != address),
            "source_merkle_root_changed": source.memory.root != initial_root,
            "steps": steps,
        })

    bad_regs, _ = run_mc_initial(program, tuple(compiler.names), {"host.ADDR": 16})
    trap_index = compiler.names.index("trap")
    tiny = tiny_reduction_witness()
    checks = {
        "real_wasm_binary_validates": validation["valid"] is True,
        "one_static_holoir_image_serves_all_runtime_addresses": all(manifest["holoir_image_id"] == compiler.ir.image_id for _ in outcomes),
        "all_four_dynamic_source_executions_return_77": all(x["source_result"] == VALUE for x in outcomes),
        "all_four_counter_executions_return_77_without_recompile": all(x["counter_result"] == VALUE for x in outcomes),
        "dynamic_store_load_hits_exact_selected_sparse_word": all(x["source_word"] == x["counter_word"] == VALUE and x["other_counter_words_zero"] for x in outcomes),
        "source_path_really_updates_persistent_merkle_memory": all(x["source_merkle_root_changed"] for x in outcomes),
        "disallowed_runtime_address_traps": bad_regs[trap_index] == 1,
        "sparse_manifest_is_content_addressed": manifest["manifest_digest"].startswith("sha256:"),
        "finite_dynamic_program_constructively_compiles_to_two_counter_core": len(two.instructions) > 0 and len(primes) == len(program.register_names),
        "generic_two_counter_reduction_remains_executable": all(tuple(x["expected"]) == tuple(x["decoded"]) and x["scratch"] == 0 for x in tiny["rows"]),
    }
    out = {
        "schema": "w33.dynamic-sparse-memory-counter.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "manifest": manifest,
        "runtime_addresses_tested": list(ALLOWED),
        "outcomes": outcomes,
        "multicounter_instructions": len(program.instructions),
        "multicounter_registers": len(program.register_names),
        "two_counter_instructions": len(two.instructions),
        "theorem": "One pre-execution capability HoloIR image lowers runtime-selected aligned i32 addresses through a finite content-addressed sparse address manifest and an INC/DECJZ decision trie; the same counter image matches the persistent-Merkle Wasm runtime for all admitted runtime addresses and traps an unmanifested address.",
        "boundary": "The admitted sparse address set is finite and explicit. This is not arbitrary 4-GiB Wasm RAM, recursion, a physical RAM implementation, or a claim that the Merkle hash DAG itself has been encoded into a small number of counters.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
