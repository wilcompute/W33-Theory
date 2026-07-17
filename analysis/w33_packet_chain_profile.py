#!/usr/bin/env python3
"""Packet-level chain profile for the W33 stack-bytecode VM.

The spectral-completion witness shows that G40=2I-A is only half of the useful
chain diagnostic: it misses the 24-dimensional A=2 channel carried by
R40=20I+5A-2J.  This script asks what ordinary VM packet traffic sees.

It runs the WASM-like stack bytecode adapter, obtains the full tiny-RISC dynamic
trace, and evaluates every W33 route hop as a delta vector e_src-e_dst under:

    G40 = 2I - A
    R40 = 20I + 5A - 2J
    H40 = G40 + R40

For a valid W33 edge hop, the bill is constant:

    G40 = 6, R40 = 30, H40 = 36.

That converts the abstract chain-operator boundary into an instruction-level
runtime profiler.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_chain_operator_spectral_completion import (
    build_operators,
    delta_vec,
    quadratic_energy,
)
from w33_stack_bytecode_adapter import (
    compile_to_tiny_risc,
    decode_stack_program,
    encode_stack_program,
)
from w33_tiny_risc_packet_isa import execute
from w33_uor_runtime_model import ROOT, point_id


DEFAULT_JSON = ROOT / "data" / "w33_packet_chain_profile.json"
DEFAULT_MD = ROOT / "docs" / "w33_packet_chain_profile.md"


def label_to_index() -> dict[str, int]:
    return {point_id(point): idx for idx, point in enumerate(hn.POINTS)}


def build_payload() -> dict[str, Any]:
    stack_program = decode_stack_program(encode_stack_program())
    tiny_program, lowering = compile_to_tiny_risc(stack_program)
    execution = execute(tiny_program)
    trace = execution["trace"]
    ops = build_operators()
    labels = label_to_index()

    profiled_events = []
    aggregate = Counter()
    opcode_hist = Counter(row["opname"] for row in trace)
    for row in trace:
        hop_rows = []
        route = row["route"]
        for left_label, right_label in zip(route, route[1:]):
            left = labels[left_label]
            right = labels[right_label]
            vec = delta_vec(left, right)
            hop = {
                "from": left_label,
                "to": right_label,
                "G40": quadratic_energy(vec, ops["G40"]),
                "R40": quadratic_energy(vec, ops["R40"]),
                "H40": quadratic_energy(vec, ops["H40"]),
            }
            hop_rows.append(hop)
            aggregate["hops"] += 1
            aggregate["G40"] += hop["G40"]
            aggregate["R40"] += hop["R40"]
            aggregate["H40"] += hop["H40"]
        profiled_events.append(
            {
                "step": row["step"],
                "pc": row["pc"],
                "opname": row["opname"],
                "route": route,
                "hops": len(hop_rows),
                "chain_bill": {
                    "G40": sum(hop["G40"] for hop in hop_rows),
                    "R40": sum(hop["R40"] for hop in hop_rows),
                    "H40": sum(hop["H40"] for hop in hop_rows),
                },
                "hop_rows": hop_rows,
            }
        )

    checks = {
        "stack_result_is_140": execution["output"] == [140],
        "dynamic_steps_114": len(trace) == 114,
        "all_events_profiled": len(profiled_events) == len(trace),
        "all_hops_have_edge_bill": all(
            (hop["G40"], hop["R40"], hop["H40"]) == (6, 30, 36)
            for event in profiled_events
            for hop in event["hop_rows"]
        ),
        "aggregate_bill_matches_hops": (
            aggregate["G40"] == 6 * aggregate["hops"]
            and aggregate["R40"] == 30 * aggregate["hops"]
            and aggregate["H40"] == 36 * aggregate["hops"]
        ),
        "R40_to_G40_ratio_is_five": aggregate["R40"] == 5 * aggregate["G40"],
        "lowering_covers_stack_program": len(lowering) == len(stack_program),
    }
    return {
        "schema": "w33.packet_chain_profile.v1",
        "theorem": "VM packet hops carry a constant two-channel W33 chain bill",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "program": {
            "stack_ops": len(stack_program),
            "tiny_ops": len(tiny_program),
            "dynamic_steps": len(trace),
            "result": execution["output"],
        },
        "operator_bill_per_edge_hop": {"G40": 6, "R40": 30, "H40": 36},
        "aggregate": dict(aggregate),
        "opcode_histogram": dict(sorted(opcode_hist.items())),
        "events_preview": profiled_events[:40],
        "events_tail": profiled_events[-12:],
        "checks": checks,
        "interpretation": (
            "Every routed VM hop is a W33 edge delta, so it has the same chain "
            "bill: 6 in the G40 shadow channel and 30 in the missing R40 channel. "
            "The R channel is not decorative; it contributes five times the G "
            "channel on actual packet traffic."
        ),
        "honesty_boundary": (
            "This profiles the deterministic stack-bytecode sample. It does not "
            "claim the same opcode mix or hop count for arbitrary programs."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    aggregate = payload["aggregate"]
    rows = []
    for op, count in payload["opcode_histogram"].items():
        rows.append(f"| {op} | {count} |")
    return f"""# W(3,3) Packet Chain Profile

The stack-bytecode VM trace is profiled against the two-channel chain operator
`(G40, R40)`. Every route hop is a W33 edge delta with fixed bill:

```text
G40 = 6
R40 = 30
H40 = 36
```

Program result: `{payload['program']['result']}`. Dynamic events:
`{payload['program']['dynamic_steps']}`. Route hops: `{aggregate['hops']}`.
Aggregate bill: `G40={aggregate['G40']}`, `R40={aggregate['R40']}`,
`H40={aggregate['H40']}`.

| Opcode | Dynamic count |
|---|---:|
{chr(10).join(rows)}

Interpretation: the missing `R40` channel contributes five times the `G40`
shadow channel on actual routed packet traffic.
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
    print(f"program: {payload['program']}")
    print(f"aggregate: {payload['aggregate']}")
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
