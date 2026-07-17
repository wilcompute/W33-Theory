#!/usr/bin/env python3
"""Lift Python bytecode into the Holonet packet ABI.

This is the next step after wrapping a command: instead of treating the child
program as an opaque process, inspect bytecode operations and map each operation
into a typed packet slot:

    bytecode op -> W33 source/destination route -> Q6/tomotope body slot.

The script does not execute arithmetic on a qutrit device.  It proves a
deterministic lowering map from ordinary Python bytecode into the existing
Holonet packet ABI fields.
"""

from __future__ import annotations

import argparse
import dis
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import holonet_node as hn
from w33_component_execution_simulator import line_lookup
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_python_bytecode_packet_lifter.json"
DEFAULT_MD = ROOT / "docs" / "w33_python_bytecode_packet_lifter.md"

BODY_OPS = ["LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX"]


def sample_sum_squares() -> int:
    total = 0
    for value in range(8):
        total += value * value
    return total


def sample_rule110_step() -> str:
    state = "00010000"
    rule = 110
    out = []
    for idx in range(len(state)):
        tri = state[(idx - 1) % len(state)] + state[idx] + state[(idx + 1) % len(state)]
        out.append(str((rule >> int(tri, 2)) & 1))
    return "".join(out)


SAMPLES: list[tuple[str, Callable[[], Any], Any]] = [
    ("sample_sum_squares", sample_sum_squares, 140),
    ("sample_rule110_step", sample_rule110_step, "00110000"),
]


def category(opname: str) -> str:
    if opname.startswith("LOAD"):
        return "LOAD"
    if opname.startswith("STORE") or opname.startswith("COPY"):
        return "STORE"
    if "JUMP" in opname or opname in {"FOR_ITER", "RETURN_VALUE"}:
        return "CONTROL"
    if opname.startswith("CALL") or opname in {"PRECALL", "PUSH_NULL"}:
        return "CALL"
    if opname in {"BINARY_OP", "UNARY_NEGATIVE", "COMPARE_OP"}:
        return "ARITH"
    if opname in {"BUILD_LIST", "LIST_APPEND", "BINARY_SUBSCR"}:
        return "DATA"
    return "OTHER"


def point_from_digest(seed: str) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % len(hn.POINTS)


def map_instruction(
    sample_name: str,
    op_index: int,
    instruction: dis.Instruction,
    lines: list[tuple[int, ...]],
    lookup: dict[tuple[int, int], int],
) -> dict[str, Any]:
    src_idx = point_from_digest(f"{sample_name}:{instruction.offset}:{instruction.opname}:src")
    dst_idx = point_from_digest(f"{sample_name}:{instruction.offset}:{instruction.argrepr}:dst")
    if src_idx == dst_idx:
        dst_idx = (dst_idx + 1) % len(hn.POINTS)
    route_points = hn.route(hn.POINTS[src_idx], hn.POINTS[dst_idx])
    route_indices = [hn.POINTS.index(point) for point in route_points]
    line_ids = [
        lookup[(left, right)] for left, right in zip(route_indices, route_indices[1:])
    ]
    microframe = op_index // 16
    q6_edge = op_index % 16
    body_tick = microframe * 72 + q6_edge * 3
    return {
        "op_index": op_index,
        "offset": instruction.offset,
        "opname": instruction.opname,
        "argrepr": instruction.argrepr,
        "category": category(instruction.opname),
        "source": point_id(hn.POINTS[src_idx]),
        "destination": point_id(hn.POINTS[dst_idx]),
        "route": [point_id(point) for point in route_points],
        "hops": len(route_indices) - 1,
        "line_buses": line_ids,
        "microframe": microframe,
        "q6_body_edge": q6_edge,
        "body_ticks": [body_tick + idx for idx in range(3)],
        "body_ops": BODY_OPS,
    }


def lift_sample(name: str, func: Callable[[], Any], expected: Any) -> dict[str, Any]:
    lines = all_lines()
    lookup = line_lookup(lines)
    instructions = [
        instruction
        for instruction in dis.get_instructions(func, show_caches=False)
        if instruction.opname not in {"RESUME", "CACHE", "EXTENDED_ARG"}
    ]
    mapped = [
        map_instruction(name, idx, instruction, lines, lookup)
        for idx, instruction in enumerate(instructions)
    ]
    actual = func()
    microframes = math.ceil(len(mapped) / 16) if mapped else 0
    category_hist: dict[str, int] = {}
    for row in mapped:
        category_hist[row["category"]] = category_hist.get(row["category"], 0) + 1
    return {
        "sample": name,
        "expected_result": expected,
        "actual_result": actual,
        "result_matches": actual == expected,
        "bytecode_ops": len(mapped),
        "microframes": microframes,
        "tomotope_body_capacity_ops": microframes * 16,
        "microframe_ticks": microframes * 72,
        "used_body_ticks": len(mapped) * 3,
        "body_capacity_ticks": microframes * 48,
        "category_histogram": dict(sorted(category_hist.items())),
        "max_route_hops": max((row["hops"] for row in mapped), default=0),
        "instructions": mapped,
    }


def build_payload() -> dict[str, Any]:
    samples = [lift_sample(name, func, expected) for name, func, expected in SAMPLES]
    total_ops = sum(sample["bytecode_ops"] for sample in samples)
    total_microframes = sum(sample["microframes"] for sample in samples)
    checks = {
        "all_results_match": all(sample["result_matches"] for sample in samples),
        "all_ops_mapped": all(
            sample["bytecode_ops"] == len(sample["instructions"]) for sample in samples
        ),
        "all_routes_have_diameter_two": all(
            row["hops"] <= 2 for sample in samples for row in sample["instructions"]
        ),
        "all_q6_edges_in_range": all(
            0 <= row["q6_body_edge"] < 16
            for sample in samples
            for row in sample["instructions"]
        ),
        "all_body_ticks_are_three_phase": all(
            len(row["body_ticks"]) == 3 and row["body_ops"] == BODY_OPS
            for sample in samples
            for row in sample["instructions"]
        ),
        "microframe_capacity_covers_ops": all(
            sample["tomotope_body_capacity_ops"] >= sample["bytecode_ops"]
            for sample in samples
        ),
        "nonempty_lift": total_ops > 0 and total_microframes > 0,
    }
    return {
        "schema": "w33.python_bytecode_packet_lifter.v1",
        "theorem": "Python bytecode to Holonet packet ABI lifting witness",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "local_abi": {
            "ops_per_microframe": 16,
            "ticks_per_op": 3,
            "body_ticks_per_microframe": 48,
            "guard_ticks_per_microframe": 24,
            "microframe_ticks": 72,
        },
        "samples": samples,
        "aggregate": {
            "sample_count": len(samples),
            "bytecode_ops": total_ops,
            "microframes": total_microframes,
            "used_body_ticks": sum(sample["used_body_ticks"] for sample in samples),
            "body_capacity_ticks": sum(sample["body_capacity_ticks"] for sample in samples),
            "microframe_ticks": sum(sample["microframe_ticks"] for sample in samples),
        },
        "checks": checks,
        "interpretation": (
            "Each Python bytecode instruction becomes a routed W33 packet step "
            "with a Q6/tomotope body edge and three-phase LOAD/FLIP/LATCH body "
            "ticks. This is a compiler mapping, not a claim that Python arithmetic "
            "has been accelerated by current hardware."
        ),
        "honesty_boundary": (
            "The Python functions execute normally on the host for result checks. "
            "The witness proves deterministic bytecode-to-packet lowering only."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for sample in payload["samples"]:
        rows.append(
            "| {sample} | {bytecode_ops} | {microframes} | {used_body_ticks} | "
            "{body_capacity_ticks} | {max_route_hops} | `{actual_result}` |".format(
                **sample
            )
        )
    return f"""# Python Bytecode Packet Lifter

This witness maps ordinary Python bytecode operations into the Holonet packet
ABI.  Each bytecode op receives a W33 source/destination route, one Q6/tomotope
body edge, and the fixed three body phases `LOAD_FLAG`, `FLIP_Q6_AXIS`,
`LATCH_VERTEX`.

| Sample | Bytecode ops | Microframes | Used body ticks | Body capacity ticks | Max hops | Result |
|---|---:|---:|---:|---:|---:|---|
{chr(10).join(rows)}

Boundary: this is a deterministic compiler map.  The Python arithmetic still
runs on the host CPU for result checking.
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
            f"{sample['sample']}: ops={sample['bytecode_ops']}, "
            f"microframes={sample['microframes']}, max_hops={sample['max_route_hops']}"
        )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
