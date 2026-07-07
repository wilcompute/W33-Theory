#!/usr/bin/env python3
"""BT1858: holonet_machine.tex patch materialization plan.

Wraps BT1851 as the reproducible path for inserting the metric-canonical E8
selector result into the main paper, then re-running the static TeX check.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1858_HOLONET_MACHINE_PATCH_MATERIALIZATION_PLAN_results.json")


def theorem_summary():
    return {
        "theorem": "BT1858 Holonet Machine Patch Materialization Plan",
        "patcher": "analysis/bt1851_holonet_machine_selector_merge_patch.py",
        "target": "holonet_machine.tex",
        "post_patch_check": "analysis/bt1832_tex_build_check.py",
        "insertion": "Metric-canonical E8 selector result after compiled defect runtime stack",
        "canonical_selector": [[3, 68], [4, 42], [38, 65], [90, 144]],
        "commands": [
            "python - <<'PY'\nimport bt1851_holonet_machine_selector_merge_patch as p\np.theorem_summary(apply=True)\nPY",
            "python analysis/bt1832_tex_build_check.py"
        ],
        "required_checks": {
            "anchor_found_by_BT1851": True,
            "selector_insert_contains_BT959": True,
            "local_A2_boundary_present": True,
            "static_tex_check_after_patch": True
        },
        "honest_scope": "Materialization plan. It is not a connector-side applied full-file paper update or PDF rebuild."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
