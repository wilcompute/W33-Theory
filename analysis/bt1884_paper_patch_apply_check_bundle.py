#!/usr/bin/env python3
"""BT1884: paper patch apply/check bundle.

Bundles the BT1873/BT1878 paper patch workflow into one reproducible command set:
apply the BT1869 merged selector/glue subsection to holonet_machine.tex, run the
static TeX check, and record expected artifacts. This does not run a PDF build in
this connector pass.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1884_PAPER_PATCH_APPLY_CHECK_BUNDLE_results.json")

COMMANDS = [
    "python - <<'PY'\nimport sys\nsys.path.insert(0, 'analysis')\nimport bt1873_holonet_machine_bt1869_merge_patch as p\np.theorem_summary(apply=True)\nPY",
    "python analysis/bt1832_tex_build_check.py",
    "python analysis/bt1874_final_selector_quotient_certificate.py",
]

EXPECTED_ARTIFACTS = [
    "holonet_machine.tex",
    "data/PART_BT1874_FINAL_SELECTOR_QUOTIENT_CERTIFICATE.json",
    "data/PART_BT1884_PAPER_PATCH_APPLY_CHECK_BUNDLE_results.json",
]


def theorem_summary():
    checks = {
        "apply_command_recorded": "apply=True" in COMMANDS[0],
        "static_tex_check_recorded": "bt1832_tex_build_check.py" in COMMANDS[1],
        "certificate_refresh_recorded": "bt1874_final_selector_quotient_certificate.py" in COMMANDS[2],
        "expected_holonet_target_recorded": "holonet_machine.tex" in EXPECTED_ARTIFACTS,
        "pdf_build_not_claimed": True,
    }
    return {
        "theorem": "BT1884 Paper Patch Apply/Check Bundle",
        "purpose": "apply BT1869 selector/glue subsection via BT1873 and verify TeX/static selector certificate state",
        "commands": COMMANDS,
        "expected_artifacts": EXPECTED_ARTIFACTS,
        "expected_insert": "Metric-canonical selector and remaining sign-kernel lift subsection",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "Command bundle only. It does not claim the connector pass rewrote the paper or built a PDF."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
