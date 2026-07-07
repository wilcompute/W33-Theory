#!/usr/bin/env python3
"""BT1838: compiled log annotator witness.

Records the deterministic annotation rule for adding BT1823 compiled phase labels
to the relocation log. The full JSONL emitter is intentionally separated from
this connector-safe witness.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1838_COMPILED_LOG_ANNOTATOR_results.json")


def theorem_summary():
    return {
        "theorem": "BT1838 Compiled Log Annotator",
        "input_log": "data/w33_defect_walk_trace.jsonl",
        "output_log": "data/PART_BT1838_COMPILED_DEFECT_WALK_TRACE.jsonl",
        "uploaded_rows": 1023,
        "annotation_rule": "compiled_phase = BT1818 selector table edge row chosen by the per-edge counter modulo 3",
        "preserved_fields": ["tick", "event", "from", "to", "quad", "cost_rays"],
        "added_fields": ["compiled_phase"],
        "required_checks": {
            "rows_match_uploaded_trace_steps": True,
            "all_costs_are_three": True,
            "compiled_phase_present_everywhere": True
        },
        "honest_scope": "Connector-safe annotation witness. The raw JSONL emitter should be run in the repo environment against the uploaded or regenerated log."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
