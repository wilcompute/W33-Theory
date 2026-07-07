#!/usr/bin/env python3
"""BT1830: compiled-controller telemetry trace witness.

The uploaded Pass-64 walk trace has 1023 relocation events. This witness records
what the compiled controller telemetry must preserve and extends the schema with
the BT1823 compiled phase row.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1830_COMPILED_CONTROLLER_TELEMETRY_TRACE_results.json")


def theorem_summary():
    return {
        "theorem": "BT1830 Compiled Controller Telemetry Trace",
        "input_trace_reference": {
            "trace_file": "data/w33_defect_walk_trace.jsonl",
            "events": 20000,
            "steps": 1023,
            "coverage_centers": 29,
            "seed": 99,
            "walk_law": "every step lands in the pre-move center quad; every step is an edge; every step costs 3 rays"
        },
        "compiled_schema_extension": {
            "tick": "event counter",
            "event": "relocate",
            "from": "old center",
            "to": "new center",
            "quad": "pre-move allowed center quad",
            "cost_rays": "always 3",
            "compiled_phase": "BT1823 selector phase row = table[(from,to)][counter mod 3]"
        },
        "required_invariants": {
            "edge_step": True,
            "quad_landing": True,
            "cost_rays_three": True,
            "compiled_phase_present": True
        },
        "honest_scope": "Schema and invariant witness. The full compiled JSONL trace is emitted when the patched kernel or telemetry runner is executed."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
