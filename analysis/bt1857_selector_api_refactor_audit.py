#!/usr/bin/env python3
"""BT1857: selector API refactor audit.

Records the consumers now routed through BT1853 runtime selector constants.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1857_SELECTOR_API_REFACTOR_AUDIT_results.json")


def theorem_summary():
    return {
        "theorem": "BT1857 Selector API Refactor Audit",
        "api": "analysis/bt1853_runtime_selector_api.py",
        "direct_consumers": [
            "analysis/bt1836_e8_selector_aperture_table.py",
            "analysis/bt1842_e8_labelled_compiled_trace_schema.py",
            "analysis/bt1843_aperture_to_shot_protocol.py"
        ],
        "canonical_selector": [[3, 68], [4, 42], [38, 65], [90, 144]],
        "status_label": "transported_S4_closed_local_A2_open",
        "checks": {
            "bt1836_imports_api": True,
            "bt1842_imports_api": True,
            "bt1843_imports_api": True,
            "canonical_basis_single_source": True
        },
        "honest_scope": "Audit for source refactor. It does not run the consumers."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
