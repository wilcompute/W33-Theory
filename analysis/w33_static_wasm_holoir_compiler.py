#!/usr/bin/env python3
"""Static WebAssembly -> authenticated HoloIR compiler.

This closes the specific gap left by the invocation-specialized trace compiler:
compilation happens *before* the guest is executed.  The emitted artifact is a
content-addressed instruction graph whose identity depends only on the validated
Wasm module, not on a completed execution trace.

Two repository Wasm surfaces are covered:

* w33_wasm3_frontend: structured block/loop/br/br_if control and locals;
* w33_wasm3_capability_runtime: calls/imports, globals and persistent Merkle
  linear memory.

The static HoloIR is deliberately close to the validated source semantics.  It
materializes instruction identities, control targets and W33 routing metadata
without evaluating an invocation.  Independent source and HoloIR steppers are
then compared state-for-state on the repository regressions.  The capability
path uses the same persistent memory primitive but executes the statically
compiled instruction records, not the source Function instruction tuples.

Honesty boundary: this is now a true static Wasm->authenticated-HoloIR compiler
for the two finite supported Wasm subsets.  It does NOT yet prove a general
semantics-preserving lowering of arbitrary HoloIR stack/locals/memory state into
the repository's two-counter Minsky core.  The universal two-counter backend
remains a lower layer with its own exact theorem.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

import w33_wasm3_frontend as control
import w33_wasm3_capability_runtime as cap
from w33_merkle_capability_memory import digest as merkle_digest
from w33_typed_universal_microvm import Carrier, GEOMETRY

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_STATIC_WASM_HOLOIR.json"


def digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class IRInstruction:
    function: int
    ip: int
    op: str
    imm: Any
    fallthrough: int | None
    branch_target: int | None
    portal: int
    route: tuple[int, ...]

    @property
    def instruction_id(self) -> str:
        return digest({"schema": "w33.static-holoir-instruction.v1", **asdict(self)})


@dataclass(frozen=True)
class StaticHoloIR:
    source_kind: str
    source_binary_digest: str
    functions: tuple[tuple[IRInstruction, ...], ...]
    imports: tuple[tuple[str, str, int], ...] = ()

    @property
    def image_id(self) -> str:
        return digest({
            "schema": "w33.static-wasm-holoir.v1",
            "source_kind": self.source_kind,
            "source_binary_digest": self.source_binary_digest,
            "functions": [[asdict(i) for i in fn] for fn in self.functions],
            "imports": [list(x) for x in self.imports],
        })


def _route(module_digest: str, function: int, ip: int, op: str, imm: Any, portal: int) -> tuple[int, tuple[int, ...]]:
    seed = f"{module_digest}|{function}|{ip}|{op}|{imm}".encode()
    target = int.from_bytes(hashlib.sha256(seed).digest()[:8], "big") % 40
    route = tuple(int(x) for x in GEOMETRY.route(portal, target))
    return target, route


def compile_control(module: control.WasmModule) -> StaticHoloIR:
    """Compile the structured-control frontend without executing it."""
    control.validate(module)
    insns = module.function.instructions
    match = control._matching_ends(insns)
    stack: list[tuple[str, int, int]] = []  # kind,start,end
    rows: list[IRInstruction] = []
    portal = 0
    for ip, ins in enumerate(insns):
        branch_target = None
        if ins.op in {"block", "loop"}:
            stack.append((ins.op, ip + 1, match[ip]))
        elif ins.op in {"br", "br_if"}:
            depth = int(ins.imm)
            kind, start, end = stack[-1 - depth]
            branch_target = start if kind == "loop" else end + 1
        elif ins.op == "end" and stack and stack[-1][2] == ip:
            stack.pop()
        target, route = _route(module.binary_digest, 0, ip, ins.op, ins.imm, portal)
        rows.append(IRInstruction(0, ip, ins.op, ins.imm, ip + 1 if ip + 1 < len(insns) else None, branch_target, target, route))
        portal = target
    return StaticHoloIR("structured-control", module.binary_digest, (tuple(rows),))


def compile_capability(module: cap.WasmModule) -> StaticHoloIR:
    """Compile calls/globals/linear-memory Wasm without running an export."""
    cap.validate(module)
    functions: list[tuple[IRInstruction, ...]] = []
    portal = 0
    for function_index, fn in enumerate(module.functions, start=len(module.imports)):
        rows = []
        for ip, ins in enumerate(fn.instructions):
            target, route = _route(module.binary_digest, function_index, ip, ins.op, ins.imm, portal)
            rows.append(IRInstruction(function_index, ip, ins.op, ins.imm, ip + 1 if ip + 1 < len(fn.instructions) else None, None, target, route))
            portal = target
        functions.append(tuple(rows))
    imports = tuple((x.module, x.name, x.type_index) for x in module.imports)
    return StaticHoloIR("capability", module.binary_digest, tuple(functions), imports)


def _control_source_steps(module: control.WasmModule, fuel: int = 100000) -> tuple[int, list[dict[str, Any]]]:
    """Independent small-step source semantics for the supported control subset."""
    control.validate(module)
    insns = module.function.instructions
    match = control._matching_ends(insns)
    locals_ = [0] * len(module.function.locals_types)
    stackv: list[int] = []
    frames: list[dict[str, int | str]] = []
    pc = 0
    trace: list[dict[str, Any]] = []

    def snap() -> dict[str, Any]:
        return {"pc": pc, "locals": list(locals_), "stack": list(stackv), "control": [dict(x) for x in frames]}

    for _ in range(fuel):
        before = snap()
        ins = insns[pc]
        op = ins.op
        if op in {"block", "loop"}:
            frames.append({"kind": op, "start": pc + 1, "end": match[pc]}); pc += 1
        elif op == "end":
            if frames and int(frames[-1]["end"]) == pc:
                frames.pop(); pc += 1
            else:
                if len(stackv) != 1: raise RuntimeError("function end result arity mismatch")
                trace.append({"before": before, "op": op, "after": {"result": stackv[-1]}})
                return stackv[-1], trace
        elif op == "local.get": stackv.append(locals_[int(ins.imm)]); pc += 1
        elif op == "local.set": locals_[int(ins.imm)] = stackv.pop(); pc += 1
        elif op == "i32.const": stackv.append(int(ins.imm) & 0xFFFFFFFF); pc += 1
        elif op == "i32.eqz": stackv.append(1 if stackv.pop() == 0 else 0); pc += 1
        elif op == "i32.add":
            b, a = stackv.pop(), stackv.pop(); stackv.append((a + b) & 0xFFFFFFFF); pc += 1
        elif op == "i32.sub":
            b, a = stackv.pop(), stackv.pop(); stackv.append((a - b) & 0xFFFFFFFF); pc += 1
        elif op in {"br", "br_if"}:
            take = True if op == "br" else stackv.pop() != 0
            if not take: pc += 1
            else:
                depth = int(ins.imm); frame = frames[-1-depth]
                del frames[len(frames)-depth:]
                if frame["kind"] == "loop": pc = int(frame["start"])
                else: frames.pop(); pc = int(frame["end"]) + 1
        elif op == "return":
            if len(stackv) != 1: raise RuntimeError("return requires one i32")
            result = stackv.pop(); trace.append({"before": before, "op": op, "after": {"result": result}}); return result, trace
        else: raise RuntimeError(op)
        trace.append({"before": before, "op": op, "after": snap()})
    raise RuntimeError("source control fuel exhausted")


def _control_ir_steps(ir: StaticHoloIR, local_count: int, fuel: int = 100000) -> tuple[int, list[dict[str, Any]]]:
    rows = ir.functions[0]
    locals_ = [0] * local_count
    stackv: list[int] = []
    frames: list[dict[str, int | str]] = []
    pc = 0
    trace: list[dict[str, Any]] = []

    def snap() -> dict[str, Any]:
        return {"pc": pc, "locals": list(locals_), "stack": list(stackv), "control": [dict(x) for x in frames]}

    # Precompute block end from branch-target/fallthrough structure of the static artifact.
    starts: list[int] = []
    end_for: dict[int, int] = {}
    for i, row in enumerate(rows):
        if row.op in {"block", "loop"}: starts.append(i)
        elif row.op == "end" and starts:
            s = starts.pop(); end_for[s] = i

    for _ in range(fuel):
        before = snap(); row = rows[pc]; op = row.op
        if op in {"block", "loop"}:
            frames.append({"kind": op, "start": pc + 1, "end": end_for[pc]}); pc = int(row.fallthrough)
        elif op == "end":
            if frames and int(frames[-1]["end"]) == pc:
                frames.pop(); pc = int(row.fallthrough)
            else:
                if len(stackv) != 1: raise RuntimeError("IR function end arity mismatch")
                trace.append({"before": before, "op": op, "after": {"result": stackv[-1]}}); return stackv[-1], trace
        elif op == "local.get": stackv.append(locals_[int(row.imm)]); pc = int(row.fallthrough)
        elif op == "local.set": locals_[int(row.imm)] = stackv.pop(); pc = int(row.fallthrough)
        elif op == "i32.const": stackv.append(int(row.imm) & 0xFFFFFFFF); pc = int(row.fallthrough)
        elif op == "i32.eqz": stackv.append(1 if stackv.pop() == 0 else 0); pc = int(row.fallthrough)
        elif op == "i32.add":
            b, a = stackv.pop(), stackv.pop(); stackv.append((a + b) & 0xFFFFFFFF); pc = int(row.fallthrough)
        elif op == "i32.sub":
            b, a = stackv.pop(), stackv.pop(); stackv.append((a - b) & 0xFFFFFFFF); pc = int(row.fallthrough)
        elif op in {"br", "br_if"}:
            take = True if op == "br" else stackv.pop() != 0
            if not take: pc = int(row.fallthrough)
            else:
                depth = int(row.imm); frame = frames[-1-depth]
                del frames[len(frames)-depth:]
                if frame["kind"] == "loop": pc = int(row.branch_target)
                else: frames.pop(); pc = int(row.branch_target)
        elif op == "return":
            if len(stackv) != 1: raise RuntimeError("IR return requires one i32")
            result = stackv.pop(); trace.append({"before": before, "op": op, "after": {"result": result}}); return result, trace
        else: raise RuntimeError(op)
        trace.append({"before": before, "op": op, "after": snap()})
    raise RuntimeError("IR control fuel exhausted")


class CapabilityIRRuntime(cap.CapabilityWasmRuntime):
    """Execute the compiled instruction records while reusing exact Merkle memory primitives."""
    def __init__(self, module: cap.WasmModule, ir: StaticHoloIR, carrier: Carrier = Carrier.CIRCUIT_ST81, host_functions: Mapping[tuple[str, str], cap.HostCallable] | None = None):
        super().__init__(module, carrier, host_functions)
        self.ir = ir
        self._by_function = {fn[0].function: fn for fn in ir.functions if fn}

    def _call_ir(self, function_index: int, args: tuple[int, ...], depth: int = 0) -> tuple[int, ...]:
        if depth > 64: raise RuntimeError("Wasm call depth exceeds runtime limit")
        ftype = self.module.function_type(function_index)
        args = tuple(self.i32(x) for x in args)
        if function_index < len(self.module.imports):
            imp = self.module.imports[function_index]
            host = self.host_functions.get((imp.module, imp.name))
            if host is None: raise RuntimeError(f"unbound Wasm import {imp.module}.{imp.name}")
            result = host(args, self)
            if not ftype.results: values = ()
            elif len(ftype.results) == 1: values = result if isinstance(result, tuple) else (int(result),)
            else:
                if not isinstance(result, tuple): raise RuntimeError("multi-result import must return tuple")
                values = result
            return tuple(self.i32(x) for x in values)
        fn = self.module.functions[function_index - len(self.module.imports)]
        rows = self._by_function[function_index]
        locals_ = list(args) + [0] * len(fn.locals_types)
        stack: list[int] = []
        for row in rows:
            op = row.op
            if op == "i32.const": stack.append(self.i32(int(row.imm)))
            elif op == "local.get": stack.append(locals_[int(row.imm)])
            elif op == "local.set": locals_[int(row.imm)] = stack.pop()
            elif op == "local.tee": locals_[int(row.imm)] = stack[-1]
            elif op == "global.get": stack.append(self.globals[int(row.imm)])
            elif op == "global.set": self.globals[int(row.imm)] = self.i32(stack.pop())
            elif op == "i32.add":
                b, a = stack.pop(), stack.pop(); stack.append(self.i32(a + b))
            elif op == "i32.sub":
                b, a = stack.pop(), stack.pop(); stack.append(self.i32(a - b))
            elif op == "i32.load":
                _, offset = row.imm; stack.append(self.load_i32(self.i32(stack.pop()) + offset))
            elif op == "i32.store":
                _, offset = row.imm; value = stack.pop(); address = self.i32(stack.pop()) + offset; self.store_i32(address, value)
            elif op == "call":
                ctype = self.module.function_type(int(row.imm)); call_args = tuple(stack.pop() for _ in ctype.params)[::-1]; stack.extend(self._call_ir(int(row.imm), call_args, depth + 1))
            elif op == "end":
                if len(stack) != len(ftype.results): raise RuntimeError("IR function result arity mismatch")
                return tuple(self.i32(x) for x in stack)
            else: raise RuntimeError(op)
        raise RuntimeError("IR function fell off end")

    def execute_export_ir(self, name: str, args: tuple[int, ...] = ()):
        matches = [(kind, index) for export_name, kind, index in self.module.exports if export_name == name]
        if len(matches) != 1 or matches[0][0] != 0: raise KeyError(name)
        values = self._call_ir(matches[0][1], args)
        if not values: return None
        return values[0] if len(values) == 1 else values


def verify() -> dict[str, Any]:
    # Structured control: compile first, then compare every bounded small step.
    cbin = control.sample_module_binary(7)
    cmod = control.decode_module(cbin)
    cir = compile_control(cmod)
    csrc_result, csrc_trace = _control_source_steps(cmod)
    cir_result, cir_trace = _control_ir_steps(cir, len(cmod.function.locals_types))
    control_bisim = csrc_result == cir_result and csrc_trace == cir_trace

    # Calls/globals/Merkle linear memory: compile before either runtime executes.
    mbin = cap.build_regression_module()
    mmod = cap.decode_module(mbin)
    mir = compile_capability(mmod)
    source = cap.CapabilityWasmRuntime(mmod, Carrier.CIRCUIT_ST81)
    source_result = source.execute_export("main")
    target = CapabilityIRRuntime(mmod, mir, Carrier.CIRCUIT_ST81)
    target_result = target.execute_export_ir("main")
    capability_equal = (
        source_result == target_result == 5
        and source.globals == target.globals == [2]
        and source.load_i32(0) == target.load_i32(0) == 1
        and source.load_i32(4) == target.load_i32(4) == 2
        and source.memory.root == target.memory.root
    )

    # Imported call path is also compiled statically; host binding stays a runtime capability.
    hmod = cap.decode_module(cap.build_host_import_module())
    hir = compile_capability(hmod)
    host = {("w33.kernel", "SEND36"): lambda args, runtime: sum(args) & 0xFFFFFFFF}
    hsource = cap.CapabilityWasmRuntime(hmod, host_functions=host)
    htarget = CapabilityIRRuntime(hmod, hir, host_functions=host)
    host_equal = hsource.execute_export("main") == htarget.execute_export_ir("main") == 50

    all_rows = [row for fn in cir.functions + mir.functions + hir.functions for row in fn]
    checks = {
        "control_module_is_compiled_before_execution": cir.source_binary_digest == cmod.binary_digest,
        "structured_control_small_steps_are_bisimilar": control_bisim,
        "control_result_is_28": csrc_result == cir_result == 28,
        "calls_globals_memory_compile_before_execution": mir.source_binary_digest == mmod.binary_digest,
        "capability_runtime_final_state_matches_static_HoloIR": capability_equal,
        "bound_host_import_path_matches_static_HoloIR": host_equal,
        "static_artifacts_are_content_addressed": all(x.image_id.startswith("sha256:") for x in (cir, mir, hir)),
        "every_compiled_instruction_is_content_addressed": all(row.instruction_id.startswith("sha256:") for row in all_rows),
        "all_static_routes_obey_W33_diameter_two": all(len(row.route) - 1 <= 2 for row in all_rows),
        "compilation_identity_does_not_depend_on_completed_trace": compile_control(cmod).image_id == cir.image_id and compile_capability(mmod).image_id == mir.image_id,
    }
    out = {
        "schema": "w33.static-wasm-holoir-compiler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "control": {"image_id": cir.image_id, "source": cmod.binary_digest, "steps": len(csrc_trace), "result": csrc_result},
        "capability": {"image_id": mir.image_id, "source": mmod.binary_digest, "result": target_result, "memory_root": target.memory.root, "globals": target.globals},
        "host_import": {"image_id": hir.image_id, "source": hmod.binary_digest, "result": 50},
        "refinement": "Validated Wasm is translated to a static authenticated instruction graph before execution; the repository regressions then match the source semantics step-for-step for structured control and state-for-state for calls/globals/Merkle linear memory.",
        "boundary": "This closes static compilation to authenticated HoloIR for the currently supported Wasm subsets. A separate theorem is still required to encode the full HoloIR operand stack, locals, call stack and Merkle-memory state into the two-counter universal core without bounded-state assumptions.",
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
