#!/usr/bin/env python3
"""Corrected capability-HoloIR -> multi-counter bridge.

The v1 bridge exposed a real aliasing bug in CI: a host call with three stack
arguments reused the first argument stack register as the call result register,
so the first argument was cleared before SEND36 summed it.  The source/HoloIR
semantics returned 50 while the counter image returned 49.

This module preserves v1's theorem boundary but fixes host-call lowering by
copying every host argument into a fresh shadow register before writing the
result.  The same statically compiled image is then checked against the real
calls/globals/Merkle-memory regression and the bound SEND36 regression.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import w33_wasm3_capability_runtime as cap
from w33_static_wasm_holoir_compiler import compile_capability
from w33_static_holoir_counter_bridge import _addmod, _copy, _move, compile_multicounter_to_two, run_mc, tiny_reduction_witness
from w33_capability_holoir_counter_bridge import (
    ClosedCapabilityCompiler,
    SEND36,
    WORD_BITS,
    digest,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_CAPABILITY_HOLOIR_COUNTER_BRIDGE_V2.json"


class AliasSafeCapabilityCompiler(ClosedCapabilityCompiler):
    """v1 compiler with call-result/argument aliasing removed for host calls."""

    def emit_host(self, target: int, args: list[int], static_args: list[int | None], out: int,
                  entry: str, done: str) -> int | None:
        imp = self.module.imports[target]
        spec = self.host_specs.get((imp.module, imp.name))
        if spec is None:
            raise ValueError(f"unbound counter host contract {imp.module}.{imp.name}")
        if spec.arity != len(args) or spec.results != 1 or spec.kind != "sum-mod-2^w":
            raise ValueError("unsupported host counter contract")

        # Host output may occupy one of the caller's operand-stack registers.
        # Snapshot all arguments before touching `out`; this is the exact bug
        # found by the prior CI witness 1+7+42 -> 49 instead of 50.
        shadows: list[int] = []
        cursor = entry
        for i, arg in enumerate(args):
            shadow = self.reg(f"host-shadow{self.serial}-{i}")
            nxt = self.fresh("host-shadow")
            _copy(self.b, cursor, arg, shadow, self.t3, nxt)
            shadows.append(shadow)
            cursor = nxt

        n1 = self.fresh("host-add1")
        _move(self.b, cursor, shadows[0], out, n1)
        n2 = self.fresh("host-add2")
        _addmod(self.b, n1, out, shadows[1], self.modulus, self.t1, self.t2, n2)
        _addmod(self.b, n2, out, shadows[2], self.modulus, self.t1, self.t2, done)
        if all(x is not None for x in static_args):
            return sum(int(x) for x in static_args) & self.mask
        return None


def verify() -> dict[str, Any]:
    mmod = cap.decode_module(cap.build_regression_module()); cap.validate(mmod)
    mir = compile_capability(mmod)
    compiler = AliasSafeCapabilityCompiler(mmod, mir, word_bits=WORD_BITS)
    mc, manifest = compiler.compile_export("main")
    regs, mc_steps = run_mc(mc, fuel=5_000_000)
    mc_result = regs[mc.result_register]
    logical_mem = {addr: regs[reg] for addr, reg in manifest["memory_registers"].items()}
    logical_globals = [regs[r] for r in compiler.global_regs]
    two, _primes = compile_multicounter_to_two(mc)

    source = cap.CapabilityWasmRuntime(mmod)
    source_initial_root = source.memory.root
    source_result = source.execute_export("main")
    source_mem = {addr: source.load_i32(addr) for addr in manifest["memory_addresses"]}

    hmod = cap.decode_module(cap.build_host_import_module()); cap.validate(hmod)
    hir = compile_capability(hmod)
    hcompiler = AliasSafeCapabilityCompiler(hmod, hir, word_bits=WORD_BITS, host_specs=(SEND36,))
    hmc, hmanifest = hcompiler.compile_export("main")
    hregs, hsteps = run_mc(hmc, fuel=1_000_000)
    hresult = hregs[hmc.result_register]
    htwo, _hprimes = compile_multicounter_to_two(hmc)
    host_source = cap.CapabilityWasmRuntime(
        hmod,
        host_functions={("w33.kernel", "SEND36"): lambda args, runtime: sum(args) & 0xFFFFFFFF},
    )
    host_source_result = host_source.execute_export("main")

    tiny = tiny_reduction_witness()
    tiny_exact = all(tuple(x["expected"]) == tuple(x["decoded"]) and x["scratch"] == 0 for x in tiny["rows"])
    checks = {
        "prior_aliasing_counterexample_is_fixed": hresult == host_source_result == 50,
        "capability_result_is_5": mc_result == source_result == 5,
        "globals_refine_exactly": logical_globals == source.globals == [2],
        "manifested_memory_refines_merkle_contents": logical_mem == source_mem == {0: 1, 4: 2},
        "source_merkle_root_changes_on_store": source.memory.root != source_initial_root,
        "capability_image_is_constructively_two_counter": len(two.instructions) > 0,
        "host_image_is_constructively_two_counter": len(htwo.instructions) > 0,
        "generic_prime_reduction_still_executes": tiny_exact,
        "host_binding_is_content_addressed": hmanifest["host_spec_ids"] == [SEND36.spec_id],
    }
    out = {
        "schema": "w33.capability-holoir-counter-bridge.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "capability": {
            "result": mc_result,
            "multicounter_steps": mc_steps,
            "multicounter_instructions": len(mc.instructions),
            "two_counter_instructions": len(two.instructions),
            "globals": logical_globals,
            "memory_words": logical_mem,
            "manifest_digest": manifest["manifest_digest"],
        },
        "host_import": {
            "source_result": host_source_result,
            "counter_result": hresult,
            "multicounter_steps": hsteps,
            "two_counter_instructions": len(htwo.instructions),
            "host_spec_id": SEND36.spec_id,
        },
        "bug": "v1 reused the first host argument stack register as call output, clearing argument 1 before summation; v2 snapshots all host arguments into fresh shadow counters before output mutation.",
        "boundary": "This fixes the finite static host-call lowering. Dynamic sparse memory, recursion, and efficient general 32-bit physical execution remain separate claims.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
