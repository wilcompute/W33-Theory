#!/usr/bin/env python3
"""Executable packet VM for the W(3,3) bytecode lifting layer.

The bytecode lifter proves that ordinary Python operations can be assigned W33
routes and Q6/tomotope packet slots.  This file takes the next step: it runs a
small bytecode interpreter over the same instruction stream, attaches every
executed instruction to its packet metadata, and checks that the VM returns the
same values as the source functions.

This is intentionally conservative.  It is not a replacement for CPython; it is
the minimal executable witness that a wrapped program has a reproducible
operation stream whose control/data events can be routed by W(3,3).
"""

from __future__ import annotations

import argparse
import builtins
import dis
import json
import operator
from collections import Counter
from pathlib import Path
from typing import Any, Callable

from w33_python_bytecode_packet_lifter import SAMPLES, lift_sample
from w33_uor_runtime_model import ROOT

DEFAULT_JSON = ROOT / "data" / "w33_packet_vm.json"
DEFAULT_MD = ROOT / "docs" / "w33_packet_vm.md"


_BINARY_OPS: dict[str, Callable[[Any, Any], Any]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "%": operator.mod,
    ">>": operator.rshift,
    "&": operator.and_,
    "+=": operator.add,
}

TERWILLIGER_OPS: list[dict[str, Any]] = (
    [
        {
            "opcode": f"T_SCALAR_{idx}",
            "block": "Q",
            "channel": "selector/control scalar",
        }
        for idx in range(3)
    ]
    + [
        {
            "opcode": f"T_M2_{row}{col}",
            "block": "M2(Q)",
            "channel": "binary relay/cut-plane channel",
        }
        for row in range(2)
        for col in range(2)
    ]
    + [
        {
            "opcode": f"T_M3_{row}{col}",
            "block": "M3(Q)",
            "channel": "native ternary qutrit processor channel",
        }
        for row in range(3)
        for col in range(3)
    ]
)


def terwilliger_op_for_packet(packet: dict[str, Any] | None) -> dict[str, Any] | None:
    if packet is None:
        return None
    return TERWILLIGER_OPS[int(packet["q6_body_edge"]) % len(TERWILLIGER_OPS)]


class PacketVM:
    """Small stack VM for the sample bytecode subset used by Holonet witnesses."""

    def __init__(
        self, func: Callable[[], Any], packets_by_offset: dict[int, dict[str, Any]]
    ):
        self.func = func
        self.instructions = list(dis.get_instructions(func, show_caches=False))
        self.offset_to_pc = {
            instruction.offset: pc for pc, instruction in enumerate(self.instructions)
        }
        self.packets_by_offset = packets_by_offset
        self.stack: list[Any] = []
        self.locals: dict[str, Any] = {}
        self.trace: list[dict[str, Any]] = []
        self.return_value: Any = None

    def _push(self, value: Any) -> None:
        self.stack.append(value)

    def _pop(self) -> Any:
        if not self.stack:
            raise AssertionError("packet VM stack underflow")
        return self.stack.pop()

    def _global(self, name: str) -> Any:
        if name in self.func.__globals__:
            return self.func.__globals__[name]
        return getattr(builtins, name)

    def _packet_row(self, instruction: dis.Instruction) -> dict[str, Any] | None:
        return self.packets_by_offset.get(instruction.offset)

    def run(self, max_steps: int = 10_000) -> tuple[Any, list[dict[str, Any]]]:
        pc = 0
        steps = 0
        while pc < len(self.instructions):
            if steps > max_steps:
                raise AssertionError("packet VM exceeded max_steps")
            instruction = self.instructions[pc]
            steps += 1
            next_pc = pc + 1
            opname = instruction.opname
            packet = self._packet_row(instruction)

            if opname in {"RESUME", "CACHE", "EXTENDED_ARG", "END_FOR"}:
                pass
            elif opname == "LOAD_CONST":
                self._push(instruction.argval)
            elif opname == "LOAD_FAST":
                self._push(self.locals[instruction.argval])
            elif opname == "STORE_FAST":
                self.locals[instruction.argval] = self._pop()
            elif opname == "LOAD_GLOBAL":
                self._push(self._global(str(instruction.argval)))
            elif opname == "LOAD_ATTR":
                obj = self._pop()
                self._push(getattr(obj, str(instruction.argval)))
            elif opname == "BUILD_LIST":
                self._push([])
            elif opname == "GET_ITER":
                self._push(iter(self._pop()))
            elif opname == "FOR_ITER":
                iterator = self.stack[-1]
                try:
                    self._push(next(iterator))
                except StopIteration:
                    self._pop()
                    next_pc = self.offset_to_pc[int(instruction.argval)]
            elif opname == "CALL":
                argc = int(instruction.arg or 0)
                args = [self._pop() for _ in range(argc)]
                args.reverse()
                func = self._pop()
                self._push(func(*args))
            elif opname == "BINARY_OP":
                right = self._pop()
                left = self._pop()
                op = instruction.argrepr
                if op not in _BINARY_OPS:
                    raise NotImplementedError(f"unsupported BINARY_OP {op!r}")
                self._push(_BINARY_OPS[op](left, right))
            elif opname == "BINARY_SUBSCR":
                index = self._pop()
                obj = self._pop()
                self._push(obj[index])
            elif opname == "POP_TOP":
                self._pop()
            elif opname == "JUMP_BACKWARD":
                next_pc = self.offset_to_pc[int(instruction.argval)]
            elif opname == "RETURN_VALUE":
                self.return_value = self._pop()
                self.trace.append(self._trace_row(steps, instruction, packet))
                break
            else:
                raise NotImplementedError(f"unsupported opcode {opname}")

            self.trace.append(self._trace_row(steps, instruction, packet))
            pc = next_pc
        return self.return_value, self.trace

    def _trace_row(
        self,
        step: int,
        instruction: dis.Instruction,
        packet: dict[str, Any] | None,
    ) -> dict[str, Any]:
        row = {
            "step": step,
            "offset": instruction.offset,
            "opname": instruction.opname,
            "argrepr": instruction.argrepr,
            "stack_depth": len(self.stack),
            "locals": {key: repr(value) for key, value in sorted(self.locals.items())},
            "has_packet_slot": packet is not None or instruction.opname == "RESUME",
        }
        if packet is not None:
            terwilliger_op = terwilliger_op_for_packet(packet)
            row.update(
                {
                    "packet_op_index": packet["op_index"],
                    "category": packet["category"],
                    "route": packet["route"],
                    "hops": packet["hops"],
                    "line_buses": packet["line_buses"],
                    "microframe": packet["microframe"],
                    "q6_body_edge": packet["q6_body_edge"],
                    "body_ticks": packet["body_ticks"],
                    "terwilliger_op": terwilliger_op,
                }
            )
        return row


def execute_sample(name: str, func: Callable[[], Any], expected: Any) -> dict[str, Any]:
    lifted = lift_sample(name, func, expected)
    packets_by_offset = {row["offset"]: row for row in lifted["instructions"]}
    vm = PacketVM(func, packets_by_offset)
    actual, trace = vm.run()
    executed_packet_steps = [
        row for row in trace if row.get("packet_op_index") is not None
    ]
    terwilliger_counts = Counter(
        row["terwilliger_op"]["block"]
        for row in executed_packet_steps
        if row.get("terwilliger_op") is not None
    )
    return {
        "sample": name,
        "expected_result": expected,
        "host_result": func(),
        "packet_vm_result": actual,
        "result_matches_expected": actual == expected,
        "result_matches_host": actual == func(),
        "static_packet_ops": lifted["bytecode_ops"],
        "executed_steps": len(trace),
        "executed_packet_steps": len(executed_packet_steps),
        "loop_expansion_factor": (
            len(executed_packet_steps) / lifted["bytecode_ops"]
            if lifted["bytecode_ops"]
            else 0
        ),
        "max_route_hops": max(
            (row.get("hops", 0) for row in executed_packet_steps), default=0
        ),
        "terwilliger_channel_counts": dict(sorted(terwilliger_counts.items())),
        "trace_preview": trace[:36],
        "trace_tail": trace[-12:],
    }


def build_payload() -> dict[str, Any]:
    samples = [execute_sample(name, func, expected) for name, func, expected in SAMPLES]
    checks = {
        "all_results_match_expected": all(
            sample["result_matches_expected"] for sample in samples
        ),
        "all_results_match_host": all(
            sample["result_matches_host"] for sample in samples
        ),
        "all_executed_packet_steps_nonempty": all(
            sample["executed_packet_steps"] > 0 for sample in samples
        ),
        "all_static_packet_ops_nonempty": all(
            sample["static_packet_ops"] > 0 for sample in samples
        ),
        "all_routes_diameter_two": all(
            sample["max_route_hops"] <= 2 for sample in samples
        ),
        "loop_expansion_observed": any(
            sample["executed_packet_steps"] > sample["static_packet_ops"]
            for sample in samples
        ),
        "terwilliger_ops_attached": all(
            sample["terwilliger_channel_counts"] for sample in samples
        ),
    }
    return {
        "schema": "w33.packet_vm.v1",
        "theorem": "lifted bytecode packet stream has an executable VM semantics",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "samples": samples,
        "checks": checks,
        "interpretation": (
            "The packet VM executes the same operation stream that the bytecode "
            "lifter routes through W33. Static bytecode becomes dynamic routed "
            "packet events; loops expand into repeated packet steps while the "
            "source result remains unchanged. Each packet now also carries the "
            "Terwilliger local-channel opcode selected by its Q6 body edge."
        ),
        "honesty_boundary": (
            "This is a host-side interpreter for a checked bytecode subset. It "
            "does not claim CPython compatibility outside the sampled opcode set "
            "or physical speedup on current hardware."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for sample in payload["samples"]:
        rows.append(
            "| {sample} | `{packet_vm_result}` | {static_packet_ops} | "
            "{executed_packet_steps} | {loop_expansion_factor:.2f} | {max_route_hops} |".format(
                **sample
            )
        )
    return f"""# W(3,3) Packet VM

The bytecode lifter gives each instruction a W33 route and Q6/tomotope packet
slot. The packet VM executes that stream and verifies that the wrapped program
returns the same value as the source function.

| Sample | VM result | Static packet ops | Executed packet steps | Loop expansion | Max hops |
|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

Boundary: this is a compact executable semantics for the current Holonet opcode
subset, not a full CPython replacement.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")

    print(f"status: {payload['status']}")
    for sample in payload["samples"]:
        print(
            f"{sample['sample']}: result={sample['packet_vm_result']!r}, "
            f"static_ops={sample['static_packet_ops']}, "
            f"executed_packet_steps={sample['executed_packet_steps']}, "
            f"max_hops={sample['max_route_hops']}"
        )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
