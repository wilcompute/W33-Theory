#!/usr/bin/env python3
"""BT1863: trace runner selector API overlay.

BT1847 now imports BT1853 directly. This overlay records the same canonical
selector route for BT1848 without replacing the trace-runner file in this
connector pass.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1853_runtime_selector_api as selector_api  # noqa: E402

OUT = Path("data/PART_BT1863_TRACE_RUNNER_SELECTOR_API_OVERLAY_results.json")


def theorem_summary():
    return {
        "theorem": "BT1863 Trace Runner Selector API Overlay",
        "target_runner": "analysis/bt1848_e8_labelled_trace_runner.py",
        "selector_api": "analysis/bt1853_runtime_selector_api.py",
        "metric_winner": selector_api.METRIC_WINNER,
        "canonical_basis_name": selector_api.CANONICAL_BASIS_NAME,
        "selector_pairs_by_striation": {str(k): list(v) for k, v in selector_api.SELECTOR_PAIRS_BY_STRIATION.items()},
        "status_label": "transported_S4_closed_local_A2_open",
        "checks": {
            "metric_winner_two": selector_api.METRIC_WINNER == 2,
            "four_striations_available": sorted(selector_api.SELECTOR_PAIRS_BY_STRIATION) == [0, 1, 2, 3],
            "S4_rigidity_in_source_chain": any("S4" in s for s in selector_api.SOURCE_CHAIN),
            "local_A2_boundary_recorded": "A2" in selector_api.BOUNDARY
        },
        "honest_scope": "Overlay/audit for BT1848 selector routing. The direct BT1848 replacement was skipped in this connector pass."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if all(summary["checks"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
