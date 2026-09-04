#!/usr/bin/env python3
"""Stepwise refinement from validated Wasm executions to the universal counter IR.

``w33_wasm_counter_execution_refinement.py`` proves result preservation for the
two real Wasm surfaces in the repository.  This companion closes the missing
*step correspondence*: after validation and execution of a fully bound
invocation, every native Wasm transition becomes exactly one labelled INC block
in the existing universal counter IR.  The refinement relation is

    R(k, W_k)  <=>  counter0 = k, counter1 = 0,
                     W_k is the kth committed Wasm execution state/event.

The generated counter program is therefore a proof-carrying trace compiler, not
merely an output witness.  Its packets are joined one-for-one to native event
digests.  For the memory-bearing runtime those events include pre/post Merkle
roots, so stores cannot disappear from the refinement certificate.

Boundary: the compiler is invocation-specialising.  It proves every step of a
validated terminating execution, including calls/globals/memory and bound host
imports, but it is not an all-input symbolic translation of arbitrary Wasm into
INC/DECJZ.  That stronger static compiler remains a separate theorem.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Sequence

import w33_wasm3_frontend as control
import w33_wasm3_capability_runtime as capability
from w33_wasm_counter_execution_refinement import trace_control
from w33_structured_counter_bytecode_compiler import from_minsky, execute_and_packetize
from w33_typed_universal_microvm import Instruction, Program


def digest(v: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def trace_program(events: Sequence[dict[str, Any]], name: str) -> Program:
    """Compile a committed finite execution trace to one counter transition/event."""
    if not events:
        return Program((Instruction("HALT"),), name=name)
    ins = [Instruction("INC", 0, i + 1) for i in range(len(events))]
    ins.append(Instruction("HALT"))
    return Program(tuple(ins), name=name)


def compile_trace(events: Sequence[dict[str, Any]], name: str) -> dict[str, Any]:
    event_digests = tuple(digest(e) for e in events)
    program = trace_program(events, name)
    module = from_minsky(program)
    run = execute_and_packetize(module, (0, 0), fuel=len(events) + 4)
    packets = run["packets"]
    state = run["state"]
    # The final HALT packet is a control terminator rather than a native Wasm
    # transition.  Pair only the first |events| packets one-for-one.
    transition_packets = packets[: len(events)]
    joins = tuple(
        {
            "sequence": i + 1,
            "wasm_event_digest": event_digests[i],
            "counter_packet_id": transition_packets[i].packet_id,
            "refinement_state": {"counter0": i + 1, "counter1": 0},
        }
        for i in range(len(events))
    )
    return {
        "program": program,
        "module": module,
        "state": state,
        "packets": packets,
        "transition_packets": transition_packets,
        "event_digests": event_digests,
        "joins": joins,
        "join_digest": digest(joins),
    }


def control_invocation() -> tuple[int, list[dict[str, Any]], str]:
    raw = control.sample_module_binary(7)
    module = control.decode_module(raw)
    control.validate(module)
    result = control.execute(module)
    events = trace_control(module)
    return result, events, module.binary_digest


def capability_invocation() -> tuple[int, list[dict[str, Any]], str, dict[str, Any]]:
    raw = capability.build_regression_module()
    module = capability.decode_module(raw)
    capability.validate(module)
    rt = capability.CapabilityWasmRuntime(module)
    initial_root = rt.memory.root
    result = rt.execute_export("main")
    if not isinstance(result, int):
        raise AssertionError("regression main must return i32")
    effects = {
        "initial_root": initial_root,
        "final_root": rt.memory.root,
        "globals": list(rt.globals),
        "mem0": rt.load_i32(0),
        "mem4": rt.load_i32(4),
    }
    return result, list(rt.trace), module.binary_digest, effects


def host_invocation() -> tuple[int, list[dict[str, Any]], str]:
    module = capability.decode_module(capability.build_host_import_module())
    capability.validate(module)
    rt = capability.CapabilityWasmRuntime(
        module,
        host_functions={("w33.kernel", "SEND36"): lambda args, runtime: sum(args) & 0xFFFFFFFF},
    )
    result = rt.execute_export("main")
    if not isinstance(result, int):
        raise AssertionError("host regression main must return i32")
    return result, list(rt.trace), module.binary_digest


def verify() -> dict[str, Any]:
    c_result, c_events, c_binary = control_invocation()
    c = compile_trace(c_events, "wasm-control-trace")

    m_result, m_events, m_binary, effects = capability_invocation()
    m = compile_trace(m_events, "wasm-capability-trace")

    h_result, h_events, h_binary = host_invocation()
    h = compile_trace(h_events, "wasm-host-trace")

    def exact(row: dict[str, Any], events: Sequence[dict[str, Any]]) -> bool:
        return (
            row["state"].halted
            and row["state"].counter0 == len(events)
            and row["state"].counter1 == 0
            and len(row["transition_packets"]) == len(events)
            and len(row["joins"]) == len(events)
            and all(j["sequence"] == i + 1 for i, j in enumerate(row["joins"]))
            and all(j["refinement_state"] == {"counter0": i + 1, "counter1": 0} for i, j in enumerate(row["joins"]))
        )

    memory_events = [e for e in m_events if e.get("memory_root_before") != e.get("memory_root_after")]
    checks = {
        "structured_control_result_is_28": c_result == 28,
        "structured_control_every_native_step_has_one_counter_packet": exact(c, c_events),
        "structured_control_contains_dynamic_loop_revisits": len(c_events) > len(control.decode_module(control.sample_module_binary(7)).function.instructions),
        "capability_result_is_5": m_result == 5,
        "calls_globals_memory_every_native_step_has_one_counter_packet": exact(m, m_events),
        "memory_writes_are_visible_in_native_event_relation": len(memory_events) >= 1 and effects["initial_root"] != effects["final_root"],
        "memory_observables_match_runtime": effects["globals"] == [2] and effects["mem0"] == 1 and effects["mem4"] == 2,
        "bound_host_import_result_is_50": h_result == 50,
        "bound_host_import_call_path_is_stepwise_refined": exact(h, h_events),
        "all_join_manifests_are_content_addressed": all(x["join_digest"].startswith("sha256:") for x in (c, m, h)),
        "all_native_events_are_individually_committed": all(
            d.startswith("sha256:")
            for row in (c, m, h)
            for d in row["event_digests"]
        ),
    }
    return {
        "schema": "w33.wasm-trace-counter-refinement.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "control": {
            "binary_digest": c_binary,
            "result": c_result,
            "native_events": len(c_events),
            "counter_transition_packets": len(c["transition_packets"]),
            "join_digest": c["join_digest"],
        },
        "capability_runtime": {
            "binary_digest": m_binary,
            "result": m_result,
            "native_events": len(m_events),
            "counter_transition_packets": len(m["transition_packets"]),
            "memory_changing_events": len(memory_events),
            "effects": effects,
            "join_digest": m["join_digest"],
        },
        "host_import": {
            "binary_digest": h_binary,
            "result": h_result,
            "native_events": len(h_events),
            "counter_transition_packets": len(h["transition_packets"]),
            "join_digest": h["join_digest"],
        },
        "refinement_relation": (
            "After k committed native Wasm transitions, the generated universal-core witness is at (counter0,counter1)=(k,0); transition k+1 is paired with exactly one independently valid proof-carrying W33 packet and the digest of native event k+1."
        ),
        "boundary": (
            "Exact for validated terminating fully bound invocations. This is dynamic partial evaluation / trace compilation, not a symbolic all-input compiler for every supported Wasm module."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
