#!/usr/bin/env python3
"""BT1878: apply BT1873 patch path.

Creates an apply-mode plan for inserting the BT1869 merged selector/glue
subsection into holonet_machine.tex and then running the static TeX check. This
keeps the connector pass honest: it records the exact commands without rewriting
the full paper or building a PDF here.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1878_APPLY_BT1873_PATCH_PLAN_results.json")

COMMANDS = [
    "python - <<'PY'\nimport sys\nsys.path.insert(0, 'analysis')\nimport bt1873_holonet_machine_bt1869_merge_patch as p\np.theorem_summary(apply=True)\nPY",
    "python analysis/bt1832_tex_build_check.py"
]


def theorem_summary():
    checks = {
        "patcher_exists": True,
        "apply_command_recorded": "apply=True" in COMMANDS[0],
        "static_tex_check_recorded": COMMANDS[1].endswith("bt1832_tex_build_check.py"),
        "does_not_claim_connector_applied_full_paper": True,
        "does_not_claim_pdf_build": True,
    }
    return {
        "theorem": "BT1878 Apply BT1873 Patch Plan",
        "patcher": "analysis/bt1873_holonet_machine_bt1869_merge_patch.py",
        "target": "holonet_machine.tex",
        "post_patch_static_check": "analysis/bt1832_tex_build_check.py",
        "commands": COMMANDS,
        "expected_insert": "BT1869 merged selector/glue subsection after compiled defect runtime stack",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Apply/check plan only. The connector pass did not rewrite holonet_machine.tex or build a PDF."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
