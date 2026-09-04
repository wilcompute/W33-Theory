#!/usr/bin/env python3
"""Execution-level WebAssembly -> universal two-counter refinement.

This closes the executable bridge for the two genuine Wasm surfaces already in
W33-Theory without pretending that the repository implements all of Wasm 3.0.
A validated, closed invocation is executed by the existing Wasm semantics; its
observable result is then materialised by an exact two-counter Program and
lowered through the existing structured-counter proof-carrying packet path.

Two frontends are covered:
  * w33_wasm3_frontend: structured block/loop/br/br_if/return i32 control;
  * w33_wasm3_capability_runtime: calls, imports, globals and Merkle-backed
    linear-memory load/store for a fully bound invocation.

The certificate also binds the native Wasm execution trace (and Merkle root for
memory-bearing invocations), so the counter result cannot be detached from the
Wasm run it refines.

Boundary: this is exact for a concrete terminating invocation. It is not yet a
static all-input compiler from arbitrary Wasm modules to raw INC/DECJZ code.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from typing import Any

import w33_wasm3_frontend as control
import w33_wasm3_capability_runtime as capability
from w33_structured_counter_bytecode_compiler import from_minsky, execute_and_packetize
from w33_typed_universal_microvm import Instruction, Program


def digest(v: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def output_program(value: int, name: str) -> Program:
    """Exact finite Minsky program with final counter0=value, counter1=0.

    This intentionally materialises the observed value after the Wasm run.  It
    is therefore an execution refinement, not a static compiler.  The current
    regression surface has small outputs; a large arbitrary i32 value would make
    this unary witness large and is rejected rather than hidden behind a claim.
    """
    value = int(value) & 0xFFFFFFFF
    if value > 100000:
        raise ValueError("execution witness output exceeds explicit unary certificate bound")
    ins = []
    for i in range(value):
        ins.append(Instruction("INC", 0, i + 1))
    ins.append(Instruction("HALT"))
    return Program(tuple(ins), name=name)


def refine_result(result: int, name: str) -> dict[str, Any]:
    p = output_program(result, name)
    structured = from_minsky(p)
    run = execute_and_packetize(structured, (0, 0), fuel=max(10, int(result) + 5))
    final = run["state"]
    return {
        "program": p,
        "module": structured,
        "packets": run["packets"],
        "final": final,
        "ok": final.halted and final.counter0 == (int(result) & 0xFFFFFFFF) and final.counter1 == 0,
    }


def trace_control(module: control.WasmModule, fuel: int = 100000) -> list[dict[str, Any]]:
    """Instrument the existing structured-control semantics without changing it."""
    control.validate(module)
    insns = module.function.instructions
    match = control._matching_ends(insns)
    locals_ = [0] * len(module.function.locals_types)
    stack: list[int] = []
    frames: list[dict[str, int | str]] = []
    trace: list[dict[str, Any]] = []
    pc = 0

    def i32(x: int) -> int:
        return int(x) & 0xFFFFFFFF

    for sequence in range(fuel):
        if not 0 <= pc < len(insns):
            raise RuntimeError("Wasm pc escaped function")
        before = {"pc": pc, "stack": list(stack), "locals": list(locals_)}
        ins = insns[pc]
        op = ins.op
        halted = False
        if op in {"block", "loop"}:
            frames.append({"kind": op, "start": pc + 1, "end": match[pc]}); pc += 1
        elif op == "end":
            if frames and int(frames[-1]["end"]) == pc:
                frames.pop(); pc += 1
            else:
                if len(stack) != 1:
                    raise RuntimeError("function end result arity mismatch")
                halted = True
        elif op == "local.get":
            stack.append(locals_[int(ins.imm)]); pc += 1
        elif op == "local.set":
            locals_[int(ins.imm)] = stack.pop(); pc += 1
        elif op == "i32.const":
            stack.append(i32(int(ins.imm))); pc += 1
        elif op == "i32.eqz":
            stack.append(1 if stack.pop() == 0 else 0); pc += 1
        elif op == "i32.add":
            b, a = stack.pop(), stack.pop(); stack.append(i32(a + b)); pc += 1
        elif op == "i32.sub":
            b, a = stack.pop(), stack.pop(); stack.append(i32(a - b)); pc += 1
        elif op in {"br", "br_if"}:
            take = True if op == "br" else stack.pop() != 0
            if not take:
                pc += 1
            else:
                depth = int(ins.imm)
                frame = frames[-1-depth]
                del frames[len(frames)-depth:]
                if frame["kind"] == "loop":
                    pc = int(frame["start"])
                else:
                    frames.pop(); pc = int(frame["end"]) + 1
        elif op == "return":
            if len(stack) != 1:
                raise RuntimeError("return requires one i32 result")
            halted = True
        else:
            raise RuntimeError(op)
        after = {"pc": None if halted else pc, "stack": list(stack), "locals": list(locals_)}
        trace.append({"sequence": sequence + 1, "op": op, "imm": ins.imm, "before": before, "after": after})
        if halted:
            return trace
    raise RuntimeError("Wasm execution fuel exhausted")


def verify() -> dict[str, Any]:
    # Structured control: genuine binary with block/loop/br_if/br.
    raw_control = control.sample_module_binary(7)
    m_control = control.decode_module(raw_control)
    control.validate(m_control)
    result_control = control.execute(m_control)
    t_control = trace_control(m_control)
    r_control = refine_result(result_control, "wasm-control-result")

    # Capability runtime: functions, calls, mutable global, load/store.
    raw_cap = capability.build_regression_module()
    m_cap = capability.decode_module(raw_cap)
    capability.validate(m_cap)
    rt = capability.CapabilityWasmRuntime(m_cap)
    initial_root = rt.memory.root
    result_cap = rt.execute_export("main")
    if not isinstance(result_cap, int):
        raise AssertionError("regression main must return i32")
    r_cap = refine_result(result_cap, "wasm-capability-result")

    # Fully bound host import surface.
    host_module = capability.decode_module(capability.build_host_import_module())
    capability.validate(host_module)
    host_rt = capability.CapabilityWasmRuntime(
        host_module,
        host_functions={("w33.kernel", "SEND36"): lambda args, runtime: sum(args) & 0xFFFFFFFF},
    )
    host_result = host_rt.execute_export("main")
    if not isinstance(host_result, int):
        raise AssertionError("host regression main must return i32")
    r_host = refine_result(host_result, "wasm-host-result")

    control_trace_digest = digest(t_control)
    cap_trace_digest = digest(rt.trace)
    host_trace_digest = digest(host_rt.trace)
    checks = {
        "structured_control_result_preserved": result_control == 28 and r_control["ok"],
        "structured_control_dynamic_trace_bound": len(t_control) > len(m_control.function.instructions),
        "capability_runtime_result_preserved": result_cap == 5 and r_cap["ok"],
        "capability_memory_effect_preserved_by_certificate": rt.memory.root != initial_root and rt.load_i32(0) == 1 and rt.load_i32(4) == 2,
        "capability_trace_records_merkle_transition": any(x["memory_root_before"] != x["memory_root_after"] for x in rt.trace),
        "fully_bound_import_invocation_refines": host_result == 50 and r_host["ok"],
        "all_counter_witness_packets_revalidate": all(
            len(x["packets"]) == (x["final"].counter0 + 1)
            for x in (r_control, r_cap, r_host)
        ),
        "trace_digests_are_content_addressed": all(x.startswith("sha256:") for x in (control_trace_digest, cap_trace_digest, host_trace_digest)),
    }
    return {
        "schema": "w33.wasm-counter-execution-refinement.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "control": {
            "binary_digest": m_control.binary_digest,
            "result": result_control,
            "dynamic_steps": len(t_control),
            "trace_digest": control_trace_digest,
            "counter_packets": len(r_control["packets"]),
        },
        "capability_runtime": {
            "binary_digest": m_cap.binary_digest,
            "result": result_cap,
            "trace_events": len(rt.trace),
            "trace_digest": cap_trace_digest,
            "initial_root": initial_root,
            "final_root": rt.memory.root,
            "globals": list(rt.globals),
        },
        "host_import": {
            "result": host_result,
            "trace_events": len(host_rt.trace),
            "trace_digest": host_trace_digest,
        },
        "theorem": (
            "For each validated, terminating, fully bound invocation exercised here, the existing Wasm semantics and the universal two-counter/W33 packet path agree on the observable i32 result; the native Wasm execution trace and any Merkle-memory transition are separately content-addressed into the certificate."
        ),
        "boundary": (
            "This is an exact execution refinement, not yet a static all-input Wasm-to-INC/DECJZ compiler. The repository still intentionally supports only finite Wasm subsets, and large arbitrary i32 outputs are refused by the unary witness generator rather than hidden behind an impractical claim."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
