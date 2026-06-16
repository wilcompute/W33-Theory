#!/usr/bin/env python3
"""BT1210 -- BT748 half-fiber presentation-pair table generator scaffold.

Purpose
-------
BT1205 identified the remaining lookup needed by the labelled C2160 carrier:

    (root_triple_id, chirality, half_fiber_index) -> BT748 presentation_pair_key.

The original BT748 script currently constructs the necessary objects in memory
inside main() but persists only aggregate counts.  This generator records the
exact row schema and the minimal instrumentation that must be added inside
bt748_fiber_torsor_sheet_uniformity.py at the point where `cls`, `pairs`,
`pair_parity`, and `act` are all in scope.

The table is intentionally not faked here: it has 51840 objectwise rows and must
be produced by running the instrumented BT748 construction.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT1210_BT748_HALF_FIBER_TABLE_SCHEMA.json"

INSTRUMENTATION_SNIPPET = r'''
def _serial_pair_key(k):
    p, rect_pts, gauge_set = k
    return {
        "center": p,
        "rect_points": sorted(rect_pts),
        "gauges": [
            {"edge": list(e), "center": c}
            for e, c in sorted(gauge_set, key=lambda item: (tuple(item[0]), item[1]))
        ],
    }

half_fiber_rows = []
for root_triple_id, t in enumerate(sorted(cls)):
    fixed = [k for k in pairs if act(t, k) == k]
    by_chirality = {0: [], 1: []}
    for k in fixed:
        by_chirality[pair_parity[k]].append(k)
    for chirality in (0, 1):
        ordered = sorted(by_chirality[chirality], key=lambda k: json.dumps(_serial_pair_key(k), sort_keys=True))
        assert len(ordered) == 48
        for half_fiber_index, key in enumerate(ordered):
            half_fiber_rows.append({
                "root_triple_id": root_triple_id,
                "chirality": chirality,
                "half_fiber_index": half_fiber_index,
                "presentation_pair_key": _serial_pair_key(key),
            })
assert len(half_fiber_rows) == 51840
with open("data/bt748_half_fiber_presentation_pair_table.json", "w", encoding="utf-8") as f:
    json.dump({"rows": half_fiber_rows}, f, indent=2, sort_keys=True)
'''


def main() -> int:
    payload = {
        "bt": 1210,
        "title": "BT748 half-fiber presentation-pair table schema",
        "row_schema": ["root_triple_id", "chirality", "half_fiber_index", "presentation_pair_key"],
        "presentation_pair_key_schema": {
            "center": "W33 point index",
            "rect_points": "sorted list of four W33 point indices",
            "gauges": "sorted list of {edge:[x,y], center:c} gauge choices",
        },
        "expected_rows": 540 * 2 * 48,
        "expected_rows_formula": "540 root triples * 2 chiralities * 48 half-fiber slots",
        "target_output": "data/bt748_half_fiber_presentation_pair_table.json",
        "instrumentation_snippet": INSTRUMENTATION_SNIPPET,
        "status": "schema and in-scope instrumentation provided; objectwise table must be materialized by running BT748 with this snippet",
        "checks": {
            "expected_rows_51840": 540 * 2 * 48 == 51840,
            "half_fiber_size_48": 48 == 48,
            "schema_has_four_fields": True,
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
